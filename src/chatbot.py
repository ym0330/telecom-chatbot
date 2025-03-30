import os
from openai import OpenAI
from dotenv import load_dotenv
from database import DatabaseHandler
import json

load_dotenv()

class TelecomChatbot:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        self.db = DatabaseHandler()
        self.last_intent = None

    def analyze_intent(self, message: str) -> dict:
        """Use OpenAI to analyze the user's intent and extract relevant information"""
        # Check if the message is a numbered response
        if message.strip().isdigit():
            return self.handle_numbered_response(message)
            
        # First check database keywords for matches
        message_lower = message.lower()
        keywords = self.db.get_all_keywords()
        
        # Find matching keyword
        matching_keyword = None
        for keyword in keywords:
            if keyword.lower() in message_lower:
                matching_keyword = keyword
                break
        
        if matching_keyword:
            # Get intent from keyword
            intent_name = self.db.get_intent_by_keyword(matching_keyword)
            if intent_name:
                return {
                    "intent": intent_name,
                    "entities": {
                        "amount": None,
                        "date": None,
                        "account_number": None,
                        "plan_type": None
                    },
                    "urgency": "low"
                }
            
        # If no keyword match found, use OpenAI for intent analysis
        prompt = f"""
        You are a telecom customer service assistant. Analyze the following user message and extract:
        1. The main intent (must be one of: payment, billing, technical_support, account_info, plan_info, or general_query)
        2. Any relevant entities (amounts, dates, account numbers)
        3. The urgency level (high, medium, low)
        
        If the message is not related to telecom services, set intent to "not_telecom".
        
        Message: {message}
        
        Respond in JSON format with these fields:
        {{
            "intent": "string",
            "entities": {{
                "amount": "number or null",
                "date": "string or null",
                "account_number": "string or null",
                "plan_type": "string or null"
            }},
            "urgency": "string"
        }}
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that analyzes user messages and extracts intent and relevant information."},
                    {"role": "user", "content": prompt}
                ],
                response_format={ "type": "json_object" }
            )
            return json.loads(response.choices[0].message.content)
        except Exception as e:
            print(f"Error analyzing intent: {str(e)}")
            return {
                "intent": "unknown",
                "entities": {},
                "urgency": "low"
            }

    def handle_numbered_response(self, message: str) -> dict:
        """Handle numbered responses based on the last intent"""
        number = int(message.strip())
        
        if not self.last_intent:
            # If no last intent, treat as main menu selection
            return {
                "intent": "main_menu",
                "entities": {},
                "urgency": "low"
            }
            
        # Map numbered responses to specific intents
        response_mapping = {
            "main_menu": {
                1: {"intent": "account_info", "entities": {}},
                2: {"intent": "billing", "entities": {}},
                3: {"intent": "technical_support", "entities": {}},
                4: {"intent": "plan_info", "entities": {}}
            },
            "account_info": {
                1: {"intent": "update_account", "entities": {}},
                2: {"intent": "change_plan", "entities": {}},
                3: {"intent": "view_usage", "entities": {}}
            },
            "payment": {
                1: {"intent": "make_payment", "entities": {}},
                2: {"intent": "setup_auto_pay", "entities": {}},
                3: {"intent": "view_payment_history", "entities": {}}
            },
            "billing": {
                1: {"intent": "view_bill_details", "entities": {}},
                2: {"intent": "download_bill", "entities": {}},
                3: {"intent": "setup_paperless", "entities": {}}
            },
            "technical_support": {
                1: {"intent": "troubleshoot", "entities": {}},
                2: {"intent": "schedule_technician", "entities": {}},
                3: {"intent": "check_service_status", "entities": {}}
            },
            "plan_info": {
                1: {"intent": "compare_plans", "entities": {}},
                2: {"intent": "upgrade_plan", "entities": {}},
                3: {"intent": "view_plan_features", "entities": {}}
            },
            "view_usage": {
                1: {"intent": "usage_breakdown", "entities": {}},
                2: {"intent": "setup_alerts", "entities": {}},
                3: {"intent": "change_data_plan", "entities": {}}
            },
            "usage_breakdown": {
                1: {"intent": "daily_usage", "entities": {}},
                2: {"intent": "weekly_usage", "entities": {}},
                3: {"intent": "monthly_usage", "entities": {}}
            },
            "setup_alerts": {
                1: {"intent": "set_alert_threshold", "entities": {}},
                2: {"intent": "set_alert_frequency", "entities": {}},
                3: {"intent": "view_current_alerts", "entities": {}}
            },
            "change_data_plan": {
                1: {"intent": "increase_data", "entities": {}},
                2: {"intent": "decrease_data", "entities": {}},
                3: {"intent": "view_plan_options", "entities": {}}
            }
        }
        
        if self.last_intent in response_mapping and number in response_mapping[self.last_intent]:
            return response_mapping[self.last_intent][number]
            
        return {
            "intent": "general_query",
            "entities": {},
            "urgency": "low"
        }

    def get_rule_response(self, intent: str, user_id: str, entities: dict) -> str:
        """Get the appropriate response based on the intent and user data"""
        # Store the intent for handling numbered responses
        self.last_intent = intent
        
        # Check if the query is telecom-related
        if intent == "not_telecom":
            return "I apologize, but I can only help with telecom-related issues. Please ask about your phone service, internet, billing, or account information."

        # Handle main menu
        if intent == "main_menu":
            return "I'm here to help with any telecom-related questions. I can assist you with:\n1. Account information\n2. Billing and payments\n3. Technical support\n4. Plan information\nWhat would you like to know more about?"

        # Get user data if needed
        user_data = self.db.get_user_data(user_id)
        
        # Handle numbered responses separately
        if intent in ["account_info", "view_usage", "usage_breakdown", "setup_alerts", 
                     "change_data_plan", "view_bill_details", "troubleshoot", 
                     "compare_plans", "daily_usage", "weekly_usage", "monthly_usage",
                     "set_alert_threshold", "set_alert_frequency", "view_current_alerts",
                     "increase_data", "decrease_data", "view_plan_options"]:
            return self.handle_numbered_menu_response(intent, user_data)
        
        # Get response from database based on intent
        response_template = self.db.get_response_by_intent(intent)
        if not response_template:
            return "I'm not sure how to help with that specific telecom issue. Could you please provide more details about your phone service, internet, billing, or account?"

        # Replace placeholders in template with actual data
        response = response_template
        if user_data:
            for key, value in user_data.items():
                response = response.replace(f"{{{key}}}", str(value))
        
        # Add any relevant entity information
        if entities:
            for key, value in entities.items():
                if value:
                    response = response.replace(f"{{{key}}}", str(value))
        
        # Add follow-up questions based on intent
        follow_up = self.get_follow_up_questions(intent)
        if follow_up:
            response += f"\n\n{follow_up}"
        
        return response

    def handle_numbered_menu_response(self, intent: str, user_data: dict) -> str:
        """Handle responses for numbered menu options"""
        responses = {
            "account_info": f"I can help you with your account information. Your account {user_data['account_number']} is currently {user_data['status']}. Your plan is {user_data['plan_type']} with a monthly fee of {user_data['monthly_fee']}. Would you like to:\n1. Update your account details\n2. Change your plan\n3. View your usage",
            "view_usage": f"Your current data usage is {user_data['data_usage']} out of {user_data['data_limit']}. Would you like to:\n1. View detailed usage breakdown\n2. Set up usage alerts\n3. Change your data plan",
            "usage_breakdown": "Please select the time period for your usage breakdown:\n1. Daily usage\n2. Weekly usage\n3. Monthly usage",
            "setup_alerts": "Let's set up usage alerts. Would you like to:\n1. Set alert threshold\n2. Set alert frequency\n3. View current alerts",
            "change_data_plan": "What would you like to do with your data plan?\n1. Increase data allowance\n2. Decrease data allowance\n3. View plan options",
            "view_bill_details": f"Your last bill was generated on {user_data['last_bill_date']} for {user_data['last_bill_amount']}. Would you like to:\n1. View itemized charges\n2. Download the bill\n3. Set up paperless billing",
            "troubleshoot": "Let's go through some basic troubleshooting steps:\n1. Check your device settings\n2. Test your network connection\n3. Restart your device\nWhich step would you like to try first?",
            "compare_plans": "Here are our available plans:\n1. Basic: $49.99/month (50GB data)\n2. Premium: $99.99/month (100GB data)\n3. Business: $199.99/month (Unlimited data)\nWould you like to:\n1. Compare plan features\n2. Upgrade your plan\n3. View your current plan details",
            "daily_usage": f"Here's your daily usage breakdown:\n- Data used: {user_data['data_usage']}GB\n- Data remaining: {user_data['data_limit'] - user_data['data_usage']}GB\n- Peak usage times: 2 PM - 8 PM\nWould you like to:\n1. View detailed breakdown\n2. Set up usage alerts\n3. Change your plan",
            "weekly_usage": f"Here's your weekly usage breakdown:\n- Data used: {user_data['data_usage']}GB\n- Data remaining: {user_data['data_limit'] - user_data['data_usage']}GB\n- Peak usage times: 2 PM - 8 PM\nWould you like to:\n1. View detailed breakdown\n2. Set up usage alerts\n3. Change your plan",
            "monthly_usage": f"Here's your monthly usage breakdown:\n- Data used: {user_data['data_usage']}GB\n- Data remaining: {user_data['data_limit'] - user_data['data_usage']}GB\n- Peak usage times: 2 PM - 8 PM\nWould you like to:\n1. View detailed breakdown\n2. Set up usage alerts\n3. Change your plan",
            "set_alert_threshold": "Please enter the percentage threshold for your usage alert (e.g., 80 for 80% of your data limit)",
            "set_alert_frequency": "How often would you like to receive alerts?\n1. Daily\n2. Weekly\n3. When threshold is reached",
            "view_current_alerts": "Your current alert settings:\n- Threshold: 80%\n- Frequency: Daily\n- Status: Active\nWould you like to:\n1. Modify threshold\n2. Change frequency\n3. Disable alerts",
            "increase_data": "To increase your data allowance, please select a new plan:\n1. Basic: $49.99/month (50GB data)\n2. Premium: $99.99/month (100GB data)\n3. Business: $199.99/month (Unlimited data)",
            "decrease_data": "To decrease your data allowance, please select a new plan:\n1. Basic: $49.99/month (50GB data)\n2. Premium: $99.99/month (100GB data)\n3. Business: $199.99/month (Unlimited data)",
            "view_plan_options": "Here are your current plan options:\n1. Basic: $49.99/month (50GB data)\n2. Premium: $99.99/month (100GB data)\n3. Business: $199.99/month (Unlimited data)\nWould you like to:\n1. Compare features\n2. Switch plan\n3. View current usage"
        }
        return responses.get(intent, "I'm not sure how to help with that specific option. Please try again.")

    def get_follow_up_questions(self, intent: str) -> str:
        """Get relevant follow-up questions based on the intent"""
        follow_ups = {
            "payment": "Would you like to:\n1. Make a payment now\n2. Set up automatic payments\n3. View payment history",
            "billing": "Would you like to:\n1. View your bill details\n2. Download your bill\n3. Set up paperless billing",
            "technical_support": "Would you like to:\n1. Try basic troubleshooting\n2. Schedule a technician visit\n3. Check service status in your area",
            "account_info": "Would you like to:\n1. Update your account details\n2. Change your plan\n3. View your usage",
            "plan_info": "Would you like to:\n1. Compare available plans\n2. Upgrade your current plan\n3. View plan features"
        }
        return follow_ups.get(intent, "")

    def process_message(self, user_id: str, message: str) -> str:
        """Process user message and return appropriate response"""
        # Analyze intent using OpenAI
        analysis = self.analyze_intent(message)
        
        # Get response based on intent and user data
        response = self.get_rule_response(
            analysis['intent'],
            user_id,
            analysis['entities']
        )
        
        # Save the conversation
        self.db.save_conversation(user_id, message, response)
        
        return response

    def close(self):
        """Close database connection"""
        self.db.close() 