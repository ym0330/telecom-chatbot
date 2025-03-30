from database import DatabaseHandler

def setup_intents():
    """Setup initial intents in the database"""
    db = DatabaseHandler()
    
    # Clear existing intents
    db.intent.delete_many({})
    
    # Define intents
    intents = [
        {
            "intent_name": "payment",
            "description": "Handle payment related queries",
            "category": "billing"
        },
        {
            "intent_name": "billing",
            "description": "Handle billing related queries",
            "category": "billing"
        },
        {
            "intent_name": "technical_support",
            "description": "Handle technical support queries",
            "category": "support"
        },
        {
            "intent_name": "account_info",
            "description": "Handle account information queries",
            "category": "account"
        },
        {
            "intent_name": "plan_info",
            "description": "Handle plan information queries",
            "category": "plan"
        },
        {
            "intent_name": "view_usage",
            "description": "Handle data usage queries",
            "category": "usage"
        },
        {
            "intent_name": "setup_alerts",
            "description": "Handle usage alert setup",
            "category": "usage"
        },
        {
            "intent_name": "change_data_plan",
            "description": "Handle data plan changes",
            "category": "plan"
        }
    ]
    
    # Insert intents
    db.intent.insert_many(intents)
    print("Intents have been set up successfully.")
    db.close()

if __name__ == "__main__":
    setup_intents() 