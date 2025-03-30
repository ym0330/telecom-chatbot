from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from chatbot import TelecomChatbot
import uvicorn
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Telecom Chatbot API",
    description="A chatbot API for handling telecom customer service queries",
    version="1.0.0"
)

try:
    logger.info("Initializing chatbot...")
    chatbot = TelecomChatbot()
    logger.info("Chatbot initialized successfully!")
except Exception as e:
    logger.error(f"Failed to initialize chatbot: {str(e)}")
    raise

class ChatRequest(BaseModel):
    user_id: str
    message: str

class ChatResponse(BaseModel):
    response: str

@app.get("/")
async def root():
    return {
        "message": "Welcome to Telecom Chatbot API",
        "endpoints": {
            "chat": "/chat",
            "docs": "/docs"
        },
        "usage": {
            "chat_endpoint": {
                "method": "POST",
                "url": "/chat",
                "body": {
                    "user_id": "string",
                    "message": "string"
                }
            }
        }
    }

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        response = chatbot.process_message(request.user_id, request.message)
        return ChatResponse(response=response)
    except Exception as e:
        logger.error(f"Error processing message: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.on_event("shutdown")
async def shutdown_event():
    chatbot.close()

if __name__ == "__main__":
    try:
        print("🚀 Starting Telecom Chatbot API...")
        print("📚 API documentation will be available at: http://localhost:8000/docs")
        print("🔥 API endpoint will be available at: http://localhost:8000/chat")
        print("🌐 Welcome page will be available at: http://localhost:8000/")
        uvicorn.run(app, host="localhost", port=8000, log_level="info")
    except Exception as e:
        logger.error(f"Failed to start server: {str(e)}")
        raise 