# Telecom Chatbot

A web-based chatbot application for telecom customer service, built with FastAPI and MongoDB.

## Features

- User authentication (registration and login)
- Secure password hashing
- JWT token-based authentication
- Chat interface with telecom-specific responses
- User profile management
- Chat history tracking
- Fuzzy matching for better response accuracy

## Prerequisites

- Python 3.8 or higher
- MongoDB
- OpenAI API key

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd telecom-chatbot
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the project root with the following variables:
```
MONGODB_URI=mongodb://localhost:27017/
OPENAI_API_KEY=your_openai_api_key
SECRET_KEY=your_secret_key
```

## Running the Application

1. Start the FastAPI server:
```bash
uvicorn src.main:app --reload
```

2. Open your web browser and navigate to:
```
http://localhost:8000
```

## API Documentation

Once the server is running, you can access the API documentation at:
```
http://localhost:8000/docs
```

## Project Structure

```
telecom_chatbot/
├── src/
│   ├── __init__.py
│   ├── main.py
│   ├── auth.py
│   ├── database.py
│   └── chatbot.py
├── static/
│   ├── css/
│   └── js/
├── templates/
│   └── index.html
├── requirements.txt
└── README.md
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 