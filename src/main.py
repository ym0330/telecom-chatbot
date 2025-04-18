from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import Request
from datetime import datetime, timedelta
from typing import Optional
from pydantic import BaseModel
import os
from dotenv import load_dotenv
from database import DatabaseHandler
from auth import (
    verify_password, get_password_hash, create_access_token,
    get_current_user, get_current_active_user, register_user,
    login_user, get_user_profile, update_user_profile, change_password
)
from chatbot import TelecomChatbot as Chatbot

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(title="Telecom Chatbot API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", StaticFiles(directory="src/static"), name="static")

# Templates
templates = Jinja2Templates(directory="src/templates")

# Initialize database and chatbot
db = DatabaseHandler()
chatbot = Chatbot()

# OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Pydantic models
class ChatMessage(BaseModel):
    message: str

@app.get("/")
async def read_root():
    """Serve the main page"""
    return FileResponse("src/static/index.html")

@app.post("/register")
async def register(form_data: OAuth2PasswordRequestForm = Depends()):
    """Register a new user"""
    success, message = register_user(form_data.username, form_data.username, form_data.password)
    if not success:
        raise HTTPException(status_code=400, detail=message)
    return {"message": message}

@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """Login user and return access token"""
    success, message, data = login_user(form_data.username, form_data.password)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=message,
            headers={"WWW-Authenticate": "Bearer"},
        )
    return data

@app.get("/users/me")
async def read_users_me(current_user = Depends(get_current_active_user)):
    """Get current user profile"""
    return current_user

@app.get("/users/me/profile")
async def get_profile(current_user = Depends(get_current_active_user)):
    """Get user profile with telecom data"""
    profile = get_user_profile(current_user["username"])
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return profile

@app.put("/users/me/profile")
async def update_profile(
    update_data: dict,
    current_user = Depends(get_current_active_user)
):
    """Update user profile"""
    success, message = update_user_profile(current_user["username"], update_data)
    if not success:
        raise HTTPException(status_code=400, detail=message)
    return {"message": message}

@app.post("/users/me/change-password")
async def update_password(
    current_password: str,
    new_password: str,
    current_user = Depends(get_current_active_user)
):
    """Change user password"""
    success, message = change_password(
        current_user["username"],
        current_password,
        new_password
    )
    if not success:
        raise HTTPException(status_code=400, detail=message)
    return {"message": message}

@app.post("/chat")
async def chat(
    chat_message: ChatMessage,
    current_user = Depends(get_current_active_user)
):
    """Process chat message and return response"""
    try:
        # Get user's telecom data
        user_data = db.get_user_data(current_user["_id"])
        
        # Get chatbot response
        response = chatbot.get_response(chat_message.message, user_data)
        
        # Save conversation
        db.save_conversation(
            str(current_user["_id"]),
            chat_message.message,
            response
        )
        
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/chat/history")
async def get_chat_history(
    current_user = Depends(get_current_active_user),
    limit: int = 50
):
    """Get user's chat history"""
    try:
        history = db.get_chat_history(str(current_user["_id"]), limit)
        return {"history": history}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000) 