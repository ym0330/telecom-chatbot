from pymongo import MongoClient
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

class DatabaseHandler:
    def __init__(self):
        self.client = MongoClient(os.getenv('MONGODB_URI'))
        self.db = self.client[os.getenv('DATABASE_NAME')]
        self.collection = self.db[os.getenv('COLLECTION_NAME')]

    def save_conversation(self, user_id: str, message: str, response: str):
        """Save a conversation to MongoDB"""
        conversation = {
            'user_id': user_id,
            'message': message,
            'response': response,
            'timestamp': datetime.utcnow()
        }
        return self.collection.insert_one(conversation)

    def get_conversation_history(self, user_id: str, limit: int = 10):
        """Retrieve conversation history for a user"""
        return list(self.collection.find(
            {'user_id': user_id}
        ).sort('timestamp', -1).limit(limit))

    def close(self):
        """Close the database connection"""
        self.client.close() 