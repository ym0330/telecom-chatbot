import os
from openai import OpenAI
from dotenv import load_dotenv
from database import DatabaseHandler
from rules import RulesHandler

load_dotenv()

class TelecomChatbot:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        self.db = DatabaseHandler()
        self.rules = RulesHandler()

    def get_ai_response(self, message: str, conversation_history: list) -> str:
        """Get AI-generated response using OpenAI API"""
        messages = [
            {"role": "system", "content": "You are a helpful telecom customer service assistant. "
             "Provide clear, concise, and accurate responses to customer queries."}
        ]
        
        # Add conversation history
        for conv in conversation_history:
            messages.append({"role": "user", "content": conv['message']})
            messages.append({"role": "assistant", "content": conv['response']})
        
        # Add current message
        messages.append({"role": "user", "content": message})
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages,
                max_tokens=150
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"I apologize, but I'm having trouble processing your request. Error: {str(e)}"

    def process_message(self, user_id: str, message: str) -> str:
        """Process user message and return appropriate response"""
        # First, try to match with predefined rules
        rule_response = self.rules.get_response(message)
        
        # Get conversation history
        history = self.db.get_conversation_history(user_id)
        
        # Get AI response
        ai_response = self.get_ai_response(message, history)
        
        # Combine rule-based and AI responses
        final_response = f"{rule_response}\n\nAdditional information: {ai_response}"
        
        # Save the conversation
        self.db.save_conversation(user_id, message, final_response)
        
        return final_response

    def close(self):
        """Close database connection"""
        self.db.close() 