from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs
import json
import os
from groq import Groq
from dotenv import load_dotenv
import logging
import sys
from os import environ
load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
api_key = os.getenv('GROQ_API_KEY')

SYSTEM_PROMPT = """You are a knowledgeable real estate assistant for Phoree Real Estate in Dubai.

Key responsibilities:
1. Help users find properties matching their requirements
2. Provide accurate information about Dubai locations
3. Answer questions about property prices and features
4. Guide users through the buying/renting process
5. Answer to them in helpful manner

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
        logger.info("Initializing Groq client...")
        client = Groq(api_key=api_key
                    ) 
        logger.info("Starting Groq API request...")
        
        full_messages = [
            {"role": "system", "content": SYSTEM_PROMPT}
        ] + messages

        logger.info("Full messages being sent: {full_messages}")

        logger.info(f"Sending messages: {json.dumps(messages)}")  # Log the messages being sent

        completion = client.chat.completions.create(
            model="llama-3.1-70b-versatile",
            messages=full_messages,
            temperature=0.7,
            max_tokens=5024,
            top_p=1,
            stream=True
        )

        # Add accumulated response for logging
        full_response = ""
        
        for chunk in completion:
            if chunk.choices[0].delta.content:
                content = chunk.choices[0].delta.content
                full_response += content  # Accumulate the response
                data = {
                    'content': content
                }
                logger.info(f"Sending chunk: {json.dumps(data)}")
                yield f"data: {json.dumps(data)}\n\n"

        # Log the complete response at the end
        logger.info(f"Complete Groq response: {full_response}")
        print(full_response)
        logger.info("Stream completed successfully")
        yield "event: done\ndata: {}\n\n"

    except Exception as e:
        logger.error(f"Error generating Groq response: {str(e)}")
        error_message = {'content': f'Error: {str(e)}'}
        yield f"data: {json.dumps(error_message)}\n\n"
        yield "event: done\ndata: {}\n\n"

class handler(BaseHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        # Add CORS headers for Render deployment
        self.headers_to_send = {
        'Access-Control-Allow-Origin': 'https://phoree-chatbot-frontend.onrender.com',
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
            logger.info("Received POST request")
            logger.info(f"Headers: {self.headers}")
            logger.info(f"Received request to path: {self.path}")
            if not self.path.startswith('/api/chat/stream'):
                logger.error(f"Invalid path: {self.path}")
                self.send_error(404, "Not Found")
                return
            
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            logger.info(f"Raw POST data: {post_data.decode('utf-8')}")
            data = json.loads(post_data.decode('utf-8'))
            messages = data.get("messages", [])
            logger.info(f"Parsed messages: {messages}")
            print(messages, 'message from user')

            logger.info(f"Received POST request with messages: {json.dumps(messages)}")

            if not messages:
                self.send_error(400, "No messages provided")
                return

            self.send_response(200)
            self.send_header('Content-Type', 'text/event-stream')
            self.send_cors_headers()
            self.end_headers()

            for chunk in generate_groq(messages):
                self.wfile.write(chunk.encode('utf-8'))
                self.wfile.flush()

        except Exception as e:
            logger.error(f"Error in POST handler: {str(e)}")
            self.send_error(500, f"Internal Server Error: {str(e)}")

    def do_GET(self):
        try:
            logger.info("=== GET Request Details ===")
            logger.info(f"Path: {self.path}")
            logger.info(f"Headers: {dict(self.headers)}")
            
            if self.path.startswith('/api/chat/stream'):
                # Extract and log query parameters
                query_params = {}
                if '?' in self.path:
                    query_string = self.path.split('?')[1]
                    logger.info(f"Query string: {query_string}")
                    query_params = parse_qs(query_string)
                    logger.info(f"Parsed query parameters: {query_params}")
                    message = query_params.get('message', [''])[0]
                else:
                    message = ''
                logger.info(f"Extracted message: '{message}'")
                
                if not message:
                    logger.error("No message provided in request")
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

    def do_HEAD(self):
        """Handle HEAD requests (used for health checks)"""
        self.send_response(200)
        self.send_cors_headers()
        self.send_header('Content-Type', 'text/plain')
        self.send_header('Content-Length', '0')
        self.end_headers()

def run_server():
    port = int(environ.get('PORT', 8000))
    server = HTTPServer(('0.0.0.0', port), handler)
    logger.info(f'Starting server on port {port}')
    server.serve_forever()

if __name__ == '__main__':
    run_server() 

