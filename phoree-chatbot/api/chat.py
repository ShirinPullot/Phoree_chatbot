from http.server import BaseHTTPRequestHandler
from urllib.parse import parse_qs
import json
import os
from groq import Groq
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

SYSTEM_PROMPT = """You are a knowledgeable real estate assistant for Phoree Real Estate in Dubai.

Key responsibilities:
1. Help users find properties matching their requirements
2. Provide accurate information about Dubai locations
3. Answer questions about property prices and features
4. Guide users through the buying/renting process

Guidelines:
- Be concise and professional
- Ask clarifying questions when needed
- Focus on understanding user requirements
- Provide specific property suggestions when possible
- Mention price ranges when discussing properties

Current property data is available for:
- Dubai Hills (Villas and Apartments)
- Dubai Marina (Apartments and Penthouses)
- Palm Jumeirah (Luxury Villas and Apartments)
- Downtown Dubai (Luxury Apartments)
- Business Bay (Modern Apartments)
"""

def validate_env():
    groq_key = os.environ.get("GROQ_API_KEY")
    if not groq_key:
        logger.error("GROQ_API_KEY not found in environment variables")
        raise ValueError("GROQ_API_KEY not found")
    return groq_key

def generate_groq(messages):
    try:
        client = Groq(api_key=validate_env())
        
        # Add system prompt to messages
        full_messages = [
            {"role": "system", "content": SYSTEM_PROMPT}
        ] + messages

        completion = client.chat.completions.create(
            model="llama-3.1-70b-versatile",
            messages=full_messages,
            temperature=0.7,
            max_tokens=5024,
            top_p=1,
            stream=True
        )

        for chunk in completion:
            if chunk.choices[0].delta.content:
                data = {
                    'content': chunk.choices[0].delta.content
                }
                yield f"data: {json.dumps(data)}\n\n"

        yield "event: done\ndata: {}\n\n"

    except Exception as e:
        logger.error(f"Error generating Groq response: {str(e)}")
        yield f"data: {json.dumps({'content': 'Error: Please try again.'})}\n\n"
        yield "event: done\ndata: {}\n\n"

class handler(BaseHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        # Add CORS headers for Render deployment
        self.headers_to_send = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive'
        }
        super().__init__(*args, **kwargs)

    def send_cors_headers(self):
        for header, value in self.headers_to_send.items():
            self.send_header(header, value)

    def do_POST(self):
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            messages = data.get("messages", [])

            if not messages:
                self.send_error(400, "No messages provided")
                return

            self.send_response(200)
            self.send_header('Content-Type', 'text/event-stream')
            self.send_cors_headers()
            self.end_headers()

            for chunk in generate_groq(messages):
                self.wfile.write(chunk.encode('utf-8'))

        except Exception as e:
            logger.error(f"Error in POST handler: {str(e)}")
            self.send_error(500, "Internal Server Error")

    def do_GET(self):
        try:
            if self.path.startswith('/api/chat/stream'):
                query_params = parse_qs(self.path.split('?')[1])
                message = query_params.get('message', [''])[0]

                if not message:
                    self.send_error(400, "No message provided")
                    return

                messages = [{"role": "user", "content": message}]

                self.send_response(200)
                self.send_header('Content-Type', 'text/event-stream')
                self.send_cors_headers()
                self.end_headers()

                for chunk in generate_groq(messages):
                    self.wfile.write(chunk.encode('utf-8'))
            else:
                self.send_error(404, "Not Found")
                
        except Exception as e:
            logger.error(f"Error in GET handler: {str(e)}")
            self.send_error(500, "Internal Server Error")

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_cors_headers()
        self.end_headers() 