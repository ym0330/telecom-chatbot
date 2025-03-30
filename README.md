# Telecom Issue Resolution Chatbot

A rule-based chatbot for resolving telecom issues using OpenAI API and MongoDB.

## Features

- Rule-based responses for common telecom issues
- AI-powered responses using OpenAI GPT-3.5
- Conversation history storage in MongoDB
- RESTful API using FastAPI
- Predefined rules for network, billing, and account issues

## Prerequisites

- Python 3.8 or higher
- MongoDB installed and running locally
- OpenAI API key

## Setup

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Create a `.env` file with the following variables:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   MONGODB_URI=mongodb://localhost:27017/
   DATABASE_NAME=telecom_chatbot
   COLLECTION_NAME=chat_history
   ```

## Running the Application

1. Start the FastAPI server:
   ```bash
   python src/main.py
   ```
2. The API will be available at `http://localhost:8000`

## API Usage

Send a POST request to `/chat` endpoint with the following JSON body:
```json
{
    "user_id": "user123",
    "message": "I'm having network issues"
}
```

The response will be in the format:
```json
{
    "response": "I can help you with your network issue..."
}
```

## Project Structure

- `src/`: Source code directory
  - `main.py`: FastAPI application entry point
  - `chatbot.py`: Main chatbot logic
  - `database.py`: MongoDB database handler
  - `rules.py`: Rule-based response handler
- `.env`: Environment variables configuration
- `requirements.txt`: Project dependencies

## Customizing Rules

You can modify the rules in `src/rules.py` to add or update predefined responses for different types of telecom issues. 