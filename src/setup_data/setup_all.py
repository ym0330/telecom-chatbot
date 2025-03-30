from intents import setup_intents
from keywords import setup_keywords
from responses import setup_responses

def setup_all():
    """Setup all collections in the correct order"""
    print("Starting database setup...")
    
    # Setup intents first
    print("\nSetting up intents...")
    setup_intents()
    
    # Setup keywords next (depends on intents)
    print("\nSetting up keywords...")
    setup_keywords()
    
    # Setup responses last (depends on intents)
    print("\nSetting up responses...")
    setup_responses()
    
    print("\nDatabase setup completed successfully!")

if __name__ == "__main__":
    setup_all() 