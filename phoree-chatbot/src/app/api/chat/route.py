import json
import time
import random
import uuid
from typing import AsyncGenerator
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from groq import Groq
import logging
import os
from dotenv import load_dotenv

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://your-app.vercel.app", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Validate environment variables
def validate_env():
    groq_key = os.getenv("GROQ_API_KEY")
    if not groq_key:
        logger.error("GROQ_API_KEY not found in environment variables")
        raise ValueError("GROQ_API_KEY not found")
    return groq_key

# Function to stream responses from Groq
async def generate_groq(messages) -> AsyncGenerator[str, None]:
    try:
        client = Groq(api_key=validate_env())
        completion = client.chat.completions.create(
            model="llama-3.1-70b-versatile",
            messages=messages,
            temperature=1,
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

        # Send done event
        yield "event: done\ndata: {}\n\n"

    except Exception as e:
        logger.error(f"Error generating Groq response: {str(e)}")
        error_data = {
            'content': 'Error: Please try again.'
        }
        yield f"data: {json.dumps(error_data)}\n\n"
        yield "event: done\ndata: {}\n\n"

# Chat endpoint
@app.post("/api/chat")
async def chat(request: Request):
    try:
        # Parse and validate request
        body = await request.json()
        messages = body.get("messages", [])
        
        if not messages:
            raise HTTPException(status_code=400, detail="No messages provided")

        logger.info(f"Received messages: {messages}")

        # Use Groq to generate responses
        logger.info("Using Groq for response generation")
        return StreamingResponse(
            generate_groq(messages),
            media_type="text/event-stream"
        )

    except Exception as e:
        logger.error(f"Server error: {str(e)}")
        return StreamingResponse(
            generate_groq([{
                "role": "system",
                "content": "Error processing the request. Please try again."
            }]),
            media_type="text/event-stream"
        )

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy", "groq_api": bool(os.getenv("GROQ_API_KEY"))}

@app.get("/api/chat/stream")
async def chat_stream(request: Request):
    try:
        # Get message from query parameters
        message = request.query_params.get("message")
        if not message:
            raise HTTPException(status_code=400, detail="No message provided")

        # Format messages for Groq
        messages = [
            {
                "role": "user",
                "content": message
            }
        ]

        logger.info(f"Received message: {message}")

        # Set up SSE headers
        headers = {
            "Content-Type": "text/event-stream",
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Access-Control-Allow-Origin": "http://localhost:3000",
        }

        return StreamingResponse(
            generate_groq(messages),
            headers=headers,
            media_type="text/event-stream"
        )

    except Exception as e:
        logger.error(f"Server error: {str(e)}")
        async def error_stream():
            error_data = {
                'id': str(uuid.uuid4()),
                'role': 'assistant',
                'content': 'Error processing the request. Please try again.'
            }
            yield f"data: {json.dumps(error_data)}\n\n"
            yield "event: done\ndata: {}\n\n"

        return StreamingResponse(
            error_stream(),
            media_type="text/event-stream"
        )
