from database import DatabaseHandler

def setup_responses():
    """Setup initial responses in the database"""
    db = DatabaseHandler()
    
    # Clear existing responses
    db.response.delete_many({})
    
    # Define responses
    responses = [
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
    
    # Insert responses
    db.response.insert_many(responses)
    print("Responses have been set up successfully.")
    db.close()

if __name__ == "__main__":
    setup_responses() 