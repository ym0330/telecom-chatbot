from database import DatabaseHandler

def setup_keywords():
    """Setup initial keywords in the database"""
    db = DatabaseHandler()
    
    # Clear existing keywords
    db.keyword.delete_many({})
    
    # Define keywords
    keywords = [
        # Payment related keywords
        {"keyword": "pay", "intent_name": "payment"},
        {"keyword": "payment", "intent_name": "payment"},
        {"keyword": "make payment", "intent_name": "payment"},
        {"keyword": "pay bill", "intent_name": "payment"},
        {"keyword": "pay my bill", "intent_name": "payment"},
        
        # Billing related keywords
        {"keyword": "bill", "intent_name": "billing"},
        {"keyword": "billing", "intent_name": "billing"},
        {"keyword": "invoice", "intent_name": "billing"},
        {"keyword": "statement", "intent_name": "billing"},
        {"keyword": "charges", "intent_name": "billing"},
        
        # Technical support keywords
        {"keyword": "internet", "intent_name": "technical_support"},
        {"keyword": "connection", "intent_name": "technical_support"},
        {"keyword": "network", "intent_name": "technical_support"},
        {"keyword": "not working", "intent_name": "technical_support"},
        {"keyword": "slow", "intent_name": "technical_support"},
        {"keyword": "down", "intent_name": "technical_support"},
        {"keyword": "trouble", "intent_name": "technical_support"},
        {"keyword": "problem", "intent_name": "technical_support"},
        
        # Account info keywords
        {"keyword": "account", "intent_name": "account_info"},
        {"keyword": "profile", "intent_name": "account_info"},
        {"keyword": "details", "intent_name": "account_info"},
        {"keyword": "information", "intent_name": "account_info"},
        {"keyword": "my account", "intent_name": "account_info"},
        
        # Plan info keywords
        {"keyword": "plan", "intent_name": "plan_info"},
        {"keyword": "package", "intent_name": "plan_info"},
        {"keyword": "subscription", "intent_name": "plan_info"},
        {"keyword": "tariff", "intent_name": "plan_info"},
        {"keyword": "rate", "intent_name": "plan_info"},
        
        # Usage related keywords
        {"keyword": "usage", "intent_name": "view_usage"},
        {"keyword": "data", "intent_name": "view_usage"},
        {"keyword": "consumption", "intent_name": "view_usage"},
        {"keyword": "limit", "intent_name": "view_usage"},
        {"keyword": "remaining", "intent_name": "view_usage"},
        
        # Alert setup keywords
        {"keyword": "alert", "intent_name": "setup_alerts"},
        {"keyword": "notification", "intent_name": "setup_alerts"},
        {"keyword": "reminder", "intent_name": "setup_alerts"},
        {"keyword": "warn", "intent_name": "setup_alerts"},
        {"keyword": "notify", "intent_name": "setup_alerts"},
        
        # Data plan change keywords
        {"keyword": "change plan", "intent_name": "change_data_plan"},
        {"keyword": "upgrade", "intent_name": "change_data_plan"},
        {"keyword": "downgrade", "intent_name": "change_data_plan"},
        {"keyword": "modify plan", "intent_name": "change_data_plan"},
        {"keyword": "switch plan", "intent_name": "change_data_plan"}
    ]
    
    # Insert keywords
    db.keyword.insert_many(keywords)
    print("Keywords have been set up successfully.")
    db.close()

if __name__ == "__main__":
    setup_keywords() 