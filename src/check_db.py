from database import DatabaseHandler

def check_database():
    """Check the contents of all collections in the database"""
    try:
        db = DatabaseHandler()
        
        print("\nChecking database contents...")
        
        # Check intents
        print("\nIntents:")
        for intent in db.intent.find():
            print(f"- {intent['intent_name']}: {intent['description']}")
            
        # Check keywords
        print("\nKeywords (sample):")
        for keyword in db.keyword.find().limit(10):
            print(f"- {keyword['keyword']} -> {keyword['intent_name']}")
            
        # Check responses
        print("\nResponses:")
        for response in db.response.find():
            print(f"\nIntent: {response['intent_name']}")
            print(f"Template: {response['response_template'][:100]}...")
            
        db.close()
        
    except Exception as e:
        print(f"\nError checking database: {str(e)}")
        raise

if __name__ == "__main__":
    check_database() 