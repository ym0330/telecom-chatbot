from pymongo import MongoClient
from datetime import datetime
import os
from dotenv import load_dotenv
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import bcrypt
from typing import Optional, Dict, Tuple, Any
from bson import ObjectId
import json

load_dotenv()

class DatabaseHandler:
    def __init__(self):
        # Connect to MongoDB
        self.client = MongoClient(os.getenv('MONGODB_URI', 'mongodb://localhost:27017/'))
        self.db = self.client['chatbot']
        
        # Initialize collections
        self.rules = self.db['rules']
        self.chat_history = self.db['chat_history']
        self.intent = self.db['intent']
        self.keyword = self.db['keyword']
        self.response = self.db['response']
        self.users = self.db['users']
        self.user_data = self.db['user_data']
        
        # Create indexes
        self._create_indexes()
        
        # Cache keywords for faster fuzzy matching
        self._cache_keywords()

    def store_chat_history(self, user_id: str, message: str, response: str) -> bool:
        """Store a chat message and response in the chat history"""
        try:
            chat_doc = {
                "user_id": user_id,
                "message": message,
                "response": response,
                "timestamp": datetime.utcnow()
            }
            self.chat_history.insert_one(chat_doc)
            return True
        except Exception as e:
            print(f"Error storing chat history: {str(e)}")
            return False

    def add_response(self, intent_name: str, response_data: Dict[str, Any]) -> bool:
        """Add a predefined response to the database"""
        try:
            # Check if response already exists
            existing_response = self.response.find_one({"intent_name": intent_name})
            if existing_response:
                # Update existing response
                self.response.update_one(
                    {"intent_name": intent_name},
                    {"$set": response_data}
                )
            else:
                # Insert new response
                self.response.insert_one(response_data)
            
            # Add intent if it doesn't exist
            existing_intent = self.intent.find_one({"intent_name": intent_name})
            if not existing_intent:
                self.intent.insert_one({
                    "intent_name": intent_name,
                    "created_at": datetime.utcnow()
                })
            
            return True
        except Exception as e:
            print(f"Error adding response: {str(e)}")
            return False

    def _serialize_doc(self, doc: Dict) -> Dict:
        """Convert MongoDB document to JSON-serializable format"""
        if not doc:
            return None
        
        # Convert ObjectId to string
        if '_id' in doc:
            doc['_id'] = str(doc['_id'])
        
        # Convert any nested ObjectIds to strings
        for key, value in doc.items():
            if isinstance(value, ObjectId):
                doc[key] = str(value)
            elif isinstance(value, dict):
                doc[key] = self._serialize_doc(value)
            elif isinstance(value, list):
                doc[key] = [self._serialize_doc(item) if isinstance(item, dict) else str(item) if isinstance(item, ObjectId) else item for item in value]
        
        return doc

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
        
        # Indexes for users
        self.users.create_index([("username", 1)], unique=True)
        self.users.create_index([("email", 1)], unique=True)
        
        # Indexes for user_data
        self.user_data.create_index("user_id", unique=True)
        self.user_data.create_index("account_number", unique=True)
        self.user_data.create_index("email", unique=True)

    # User Management Methods
    def create_user(self, username: str, email: str, password: str) -> bool:
        """Create a new user"""
        try:
            # Check if username or email already exists
            if self.users.find_one({"$or": [{"username": username}, {"email": email}]}):
                return False
            
            # Hash password
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            
            # Create user document
            user_doc = {
                "username": username,
                "email": email,
                "password": hashed_password,
                "created_at": datetime.utcnow(),
                "is_active": True
            }
            
            # Insert user
            result = self.users.insert_one(user_doc)
            
            # Create empty user data document
            user_data_doc = {
                "user_id": str(result.inserted_id),
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow()
            }
            self.user_data.insert_one(user_data_doc)
            
            return True
        except Exception as e:
            print(f"Error creating user: {str(e)}")
            return False

    def verify_user(self, username: str, password: str) -> Tuple[bool, str, Optional[Dict[str, Any]]]:
        """Verify user credentials"""
        try:
            user = self.users.find_one({"username": username})
            if not user:
                return False, "User not found", None
            
            if not bcrypt.checkpw(password.encode('utf-8'), user["password"]):
                return False, "Incorrect password", None
            
            # Update last login
            self.users.update_one(
                {"_id": user["_id"]},
                {"$set": {"last_login": datetime.utcnow()}}
            )
            
            # Remove password and serialize user object
            user.pop("password", None)
            serialized_user = self._serialize_doc(user)
            return True, "Login successful", serialized_user
            
        except Exception as e:
            print(f"Error verifying user: {str(e)}")
            return False, f"Error during verification: {str(e)}", None

    def get_user_by_username(self, username: str) -> Optional[Dict[str, Any]]:
        """Get user by username"""
        try:
            user = self.users.find_one({"username": username})
            if user:
                user.pop("password", None)  # Remove password from response
                return self._serialize_doc(user)
            return None
        except Exception as e:
            print(f"Error getting user: {str(e)}")
            return None

    def update_user(self, username: str, update_data: Dict[str, Any]) -> Tuple[bool, str]:
        """Update user information"""
        try:
            # Check if new username or email already exists
            if "username" in update_data or "email" in update_data:
                existing_user = self.users.find_one({
                    "$and": [
                        {"_id": {"$ne": self.get_user_by_username(username)["_id"]}},
                        {"$or": [
                            {"username": update_data.get("username")},
                            {"email": update_data.get("email")}
                        ]}
                    ]
                })
                if existing_user:
                    return False, "Username or email already exists"
            
            # Update user
            result = self.users.update_one(
                {"username": username},
                {"$set": update_data}
            )
            
            if result.modified_count == 0:
                return False, "No changes made"
            
            return True, "User updated successfully"
        except Exception as e:
            print(f"Error updating user: {str(e)}")
            return False, f"Error updating user: {str(e)}"

    def change_password(self, username: str, current_password: str, new_password: str) -> Tuple[bool, str]:
        """Change user password"""
        try:
            user = self.users.find_one({"username": username})
            if not user:
                return False, "User not found"
            
            if not bcrypt.checkpw(current_password.encode('utf-8'), user["password"]):
                return False, "Current password is incorrect"
            
            # Hash new password
            hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
            
            # Update password
            result = self.users.update_one(
                {"username": username},
                {"$set": {"password": hashed_password}}
            )
            
            if result.modified_count == 0:
                return False, "Failed to update password"
            
            return True, "Password updated successfully"
        except Exception as e:
            print(f"Error changing password: {str(e)}")
            return False, f"Error changing password: {str(e)}"

    def get_user_data(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Get user's telecom data"""
        try:
            user_data = self.user_data.find_one({"user_id": user_id})
            return self._serialize_doc(user_data)
        except Exception as e:
            print(f"Error getting user data: {str(e)}")
            return None

    def update_user_data(self, user_id: str, update_data: Dict[str, Any]) -> bool:
        """Update user's telecom data"""
        try:
            update_data["updated_at"] = datetime.utcnow()
            result = self.user_data.update_one(
                {"user_id": user_id},
                {"$set": update_data}
            )
            return result.modified_count > 0
        except Exception as e:
            print(f"Error updating user data: {str(e)}")
            return False

    def get_user_by_email(self, email: str) -> Optional[Dict]:
        """Get user by email"""
        try:
            user = self.users.find_one({"email": email})
            return self._serialize_doc(user)
        except Exception as e:
            print(f"Error getting user by email: {str(e)}")
            return None

    def get_user_data_by_email(self, email: str) -> Optional[Dict]:
        """Get user's telecom data by email"""
        try:
            user_data = self.user_data.find_one({"email": email})
            return self._serialize_doc(user_data)
        except Exception as e:
            print(f"Error getting user data by email: {str(e)}")
            return None

    def get_user_data_by_account_number(self, account_number: str) -> Optional[Dict]:
        """Get user's telecom data by account number"""
        try:
            user_data = self.user_data.find_one({"account_number": account_number})
            return self._serialize_doc(user_data)
        except Exception as e:
            print(f"Error getting user data by account number: {str(e)}")
            return None

    # Chatbot Methods
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

    def get_chat_history(self, user_id: str, limit: int = 50) -> list:
        """Get user's chat history"""
        try:
            history = list(self.chat_history.find(
                {"user_id": user_id}
            ).sort("timestamp", -1).limit(limit))
            return [self._serialize_doc(doc) for doc in history]
        except Exception as e:
            print(f"Error getting chat history: {str(e)}")
            return []

    def close(self):
        """Close database connection"""
        self.client.close() 