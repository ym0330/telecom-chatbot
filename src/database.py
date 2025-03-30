from pymongo import MongoClient
from datetime import datetime
import os
from dotenv import load_dotenv
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

load_dotenv()

class DatabaseHandler:
    def __init__(self):
        # Connect to MongoDB
        self.client = MongoClient(os.getenv('MONGODB_URI', 'mongodb://localhost:27017/'))
        self.db = self.client['chatbot']
        
        # Initialize collections
        self.chat_history = self.db['chat_history']
        self.intent = self.db['intent']
        self.keyword = self.db['keyword']
        self.response = self.db['response']
        self.user_data = self.db['user_data']
        
        # Create indexes
        self._create_indexes()
        
        # Cache keywords for faster fuzzy matching
        self._cache_keywords()

    def _cache_keywords(self):
        """Cache keywords for faster fuzzy matching"""
        self.keyword_cache = [(doc["keyword"], doc["intent_name"]) for doc in self.keyword.find()]

    def _create_indexes(self):
        """Create necessary indexes for collections"""
        # Index for chat_history
        self.chat_history.create_index([("user_id", 1), ("timestamp", -1)])
        
        # Index for intent
        self.intent.create_index([("intent_name", 1)], unique=True)
        
        # Index for keyword
        self.keyword.create_index([("keyword", 1)], unique=True)
        
        # Index for response
        self.response.create_index([("intent_name", 1)])
        
        # Index for user_data
        self.user_data.create_index([("user_id", 1)], unique=True)

    def get_intent_by_keyword(self, keyword: str, threshold: int = 80) -> str:
        """Get intent name based on keyword using fuzzy matching"""
        # First try exact match
        keyword_doc = self.keyword.find_one({"keyword": keyword.lower()})
        if keyword_doc:
            return keyword_doc.get("intent_name")
        
        # If no exact match, try fuzzy matching
        best_match = process.extractOne(keyword.lower(), [k[0] for k in self.keyword_cache])
        if best_match and best_match[1] >= threshold:
            # Find the intent for the matched keyword
            for k, intent in self.keyword_cache:
                if k == best_match[0]:
                    return intent
        
        return None

    def get_fuzzy_suggestions(self, keyword: str, limit: int = 3) -> list:
        """Get similar keywords as suggestions"""
        matches = process.extract(keyword.lower(), [k[0] for k in self.keyword_cache], limit=limit)
        return [match[0] for match in matches if match[1] >= 60]

    def save_conversation(self, user_id: str, user_message: str, bot_response: str):
        """Save a conversation to chat_history"""
        conversation = {
            "user_id": user_id,
            "user_message": user_message,
            "bot_response": bot_response,
            "timestamp": datetime.utcnow()
        }
        self.chat_history.insert_one(conversation)

    def get_user_data(self, user_id: str) -> dict:
        """Get user data from user_data collection"""
        return self.user_data.find_one({"user_id": user_id})

    def get_response_by_intent(self, intent_name: str) -> str:
        """Get response template based on intent"""
        response_doc = self.response.find_one({"intent_name": intent_name})
        if response_doc:
            return response_doc.get("response_template")
        return None

    def get_all_keywords(self) -> list:
        """Get all keywords from keyword collection"""
        return [doc["keyword"] for doc in self.keyword.find()]

    def get_all_intents(self) -> list:
        """Get all intents from intent collection"""
        return [doc["intent_name"] for doc in self.intent.find()]

    def get_all_responses(self) -> list:
        """Get all responses from response collection"""
        return [doc["response_template"] for doc in self.response.find()]

    def get_chat_history(self, user_id: str, limit: int = 10) -> list:
        """Get recent chat history for a user"""
        return list(self.chat_history.find(
            {"user_id": user_id}
        ).sort("timestamp", -1).limit(limit))

    def close(self):
        """Close database connection"""
        self.client.close() 