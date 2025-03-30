from src.database import DatabaseHandler
import os
from dotenv import load_dotenv

def test_database_connection():
    try:
        # Initialize database handler
        db = DatabaseHandler()
        
        # Test saving a conversation
        test_user_id = "test_user_123"
        test_message = "Test message"
        test_response = "Test response"
        
        result = db.save_conversation(test_user_id, test_message, test_response)
        print("Successfully saved conversation!")
        print(f"Inserted ID: {result.inserted_id}")
        
        # Test retrieving conversation history
        history = db.get_conversation_history(test_user_id)
        print("\nRetrieved conversation history:")
        for conv in history:
            print(f"Message: {conv['message']}")
            print(f"Response: {conv['response']}")
            print(f"Timestamp: {conv['timestamp']}")
            print("---")
        
        # Close the connection
        db.close()
        print("\nDatabase connection test completed successfully!")
        
    except Exception as e:
        print(f"Error testing database connection: {str(e)}")

if __name__ == "__main__":
    test_database_connection() 