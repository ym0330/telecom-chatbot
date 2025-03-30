import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database import DatabaseHandler

def setup_all():
    """Setup all collections in the correct order"""
    try:
        db = DatabaseHandler()
        
        print("Starting database setup...")
        print("Connected to database 'chatbot' successfully!")
        
        # Clear existing data
        print("\nClearing existing data...")
        db.intent.delete_many({})
        db.keyword.delete_many({})
        db.response.delete_many({})
        
        # Setup intents
        print("\nSetting up intents...")
        intents = [
            {
                "intent_name": "greeting",
                "description": "Handle user greetings",
                "category": "general"
            },
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
        result = db.intent.insert_many(intents)
        print(f"Successfully inserted {len(result.inserted_ids)} intents")
        
        # Setup keywords
        print("\nSetting up keywords...")
        keywords = [
            # Greeting related keywords
            {"keyword": "hi", "intent_name": "greeting"},
            {"keyword": "hello", "intent_name": "greeting"},
            {"keyword": "hey", "intent_name": "greeting"},
            {"keyword": "good morning", "intent_name": "greeting"},
            {"keyword": "good afternoon", "intent_name": "greeting"},
            {"keyword": "good evening", "intent_name": "greeting"},
            
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
        result = db.keyword.insert_many(keywords)
        print(f"Successfully inserted {len(result.inserted_ids)} keywords")
        
        # Setup responses
        print("\nSetting up responses...")
        responses = [
            # Greeting responses
            {
                "intent_name": "greeting",
                "response_template": "Hello! Welcome to our Telecom Support. How can I assist you today? Here are some common topics I can help with:\n1. Check account & billing\n2. Technical support\n3. Plan information\n4. Data usage\n5. Set up alerts",
                "follow_up": "What would you like help with?\n1. Check account & billing\n2. Technical support\n3. Plan information\n4. Data usage\n5. Set up alerts"
            },
            
            # Payment responses
            {
                "intent_name": "payment",
                "response_template": "I can help you with your payment. Your current balance is {balance}. Would you like to:\n1. Make a payment now\n2. Set up automatic payments\n3. View payment history",
                "follow_up": "Would you like to:\n1. Make a payment now\n2. Set up automatic payments\n3. View payment history"
            },
            
            # Billing responses
            {
                "intent_name": "billing",
                "response_template": "I can help you with your billing. Your last bill was generated on {last_bill_date} for {last_bill_amount}. Would you like to:\n1. View your bill details\n2. Download your bill\n3. Set up paperless billing",
                "follow_up": "Would you like to:\n1. View your bill details\n2. Download your bill\n3. Set up paperless billing"
            },
            
            # Technical support responses
            {
                "intent_name": "technical_support",
                "response_template": "I understand you're having technical issues. Let's go through some basic troubleshooting steps:\n1. Check your device settings\n2. Test your network connection\n3. Restart your device\nWhich step would you like to try first?",
                "follow_up": "Would you like to:\n1. Try basic troubleshooting\n2. Schedule a technician visit\n3. Check service status in your area"
            },
            
            # Account info responses
            {
                "intent_name": "account_info",
                "response_template": "I can help you with your account information. Your account {account_number} is currently {status}. Your plan is {plan_type} with a monthly fee of {monthly_fee}. Would you like to:\n1. Update your account details\n2. Change your plan\n3. View your usage",
                "follow_up": "Would you like to:\n1. Update your account details\n2. Change your plan\n3. View your usage"
            },
            
            # Plan info responses
            {
                "intent_name": "plan_info",
                "response_template": "I can help you with your plan information. Your current plan is {plan_type} with {data_limit} data allowance. Would you like to:\n1. Compare available plans\n2. Upgrade your current plan\n3. View plan features",
                "follow_up": "Would you like to:\n1. Compare available plans\n2. Upgrade your current plan\n3. View plan features"
            },
            
            # Usage responses
            {
                "intent_name": "view_usage",
                "response_template": "Your current data usage is {data_usage} out of {data_limit}. Would you like to:\n1. View detailed usage breakdown\n2. Set up usage alerts\n3. Change your data plan",
                "follow_up": "Would you like to:\n1. View detailed breakdown\n2. Set up usage alerts\n3. Change your plan"
            },
            
            # Alert setup responses
            {
                "intent_name": "setup_alerts",
                "response_template": "Let's set up usage alerts. Would you like to:\n1. Set alert threshold\n2. Set alert frequency\n3. View current alerts",
                "follow_up": "Would you like to:\n1. Set alert threshold\n2. Set alert frequency\n3. View current alerts"
            },
            
            # Data plan change responses
            {
                "intent_name": "change_data_plan",
                "response_template": "What would you like to do with your data plan?\n1. Increase data allowance\n2. Decrease data allowance\n3. View plan options",
                "follow_up": "Would you like to:\n1. Increase data allowance\n2. Decrease data allowance\n3. View plan options"
            }
        ]
        result = db.response.insert_many(responses)
        print(f"Successfully inserted {len(result.inserted_ids)} responses")
        
        # Verify data
        print("\nVerifying inserted data...")
        intent_count = db.intent.count_documents({})
        keyword_count = db.keyword.count_documents({})
        response_count = db.response.count_documents({})
        
        print(f"Current database state:")
        print(f"- Intents: {intent_count} documents")
        print(f"- Keywords: {keyword_count} documents")
        print(f"- Responses: {response_count} documents")
        
        print("\nDatabase setup completed successfully!")
        db.close()
        
    except Exception as e:
        print(f"\nError during database setup: {str(e)}")
        raise

if __name__ == "__main__":
    setup_all() 