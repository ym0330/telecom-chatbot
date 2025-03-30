from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from chatbot import TelecomChatbot
import uvicorn

app = FastAPI(title="Telecom Chatbot API")
chatbot = TelecomChatbot()

class ChatRequest(BaseModel):
    user_id: str
    message: str

class ChatResponse(BaseModel):
    response: str

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        response = chatbot.process_message(request.user_id, request.message)
        return ChatResponse(response=response)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.on_event("shutdown")
async def shutdown_event():
    chatbot.close()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000) 