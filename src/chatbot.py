import os
from openai import OpenAI
from dotenv import load_dotenv
from database import DatabaseHandler
import json
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
from typing import Optional, Dict, Any
from chatbot_rules import SYSTEM_RULES, MENU_STRUCTURE

load_dotenv()

class TelecomChatbot:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        self.db = DatabaseHandler()
        self.last_intent = None
        self.system_rules = SYSTEM_RULES
        self.menu_structure = MENU_STRUCTURE
        self.menu_history = []  # Track menu navigation history
        
        # Initialize predefined responses
        self._initialize_responses()

    def _initialize_responses(self):
        """Initialize predefined responses in the database"""
        # Network issues
        self.db.add_response("network_issues", {
            "intent_name": "network_issues",
            "response_template": "I understand you're experiencing network issues. Let me help you troubleshoot. First, could you please try turning your device off and on again? If the issue persists, I can help you check your signal strength and network settings."
        })

        # Billing issues
        self.db.add_response("billing_issues", {
            "intent_name": "billing_issues",
            "response_template": "I can help you with your billing concerns. Could you please provide your account number or the last 4 digits of your phone number? This will help me access your billing information securely."
        })

        # Account management
        self.db.add_response("account_management", {
            "intent_name": "account_management",
            "response_template": "I can help you manage your account. What specific changes would you like to make? Options include updating personal information, changing your plan, or modifying your payment method."
        })

        # Data usage
        self.db.add_response("data_usage", {
            "intent_name": "data_usage",
            "response_template": "I can help you check your data usage. Would you like to know your current usage, remaining data, or would you like to purchase additional data?"
        })

        # Plan information
        self.db.add_response("plan_info", {
            "intent_name": "plan_info",
            "response_template": "I can provide information about our available plans. Would you like to know about our current promotions, compare plans, or get details about your current plan?"
        })

        # Payment issues
        self.db.add_response("payment_issues", {
            "intent_name": "payment_issues",
            "response_template": "I understand you're having issues with your payment. I can help you with payment processing, setting up automatic payments, or resolving any payment-related concerns."
        })

        # Technical support
        self.db.add_response("technical_support", {
            "intent_name": "technical_support",
            "response_template": "I can help you with technical support. Please describe the issue you're experiencing, and I'll guide you through the troubleshooting process."
        })

        # General inquiries
        self.db.add_response("general_inquiry", {
            "intent_name": "general_inquiry",
            "response_template": "I'm here to help you with any questions about our services. What would you like to know?"
        })

    def analyze_intent(self, message: str) -> dict:
        """Use OpenAI to analyze the user's intent and extract relevant information"""
        # Check if the message is a numbered response
        if message.strip().isdigit():
            return self.handle_numbered_response(message)
            
        # Handle greetings
        greetings = ["hi", "hello", "hey", "good morning", "good afternoon", "good evening"]
        if message.lower() in greetings:
            return {
                "intent": "main_menu",
                "entities": {},
                "urgency": "low"
            }
            
        # First check database keywords for matches
        message_lower = message.lower()
        words = message_lower.split()
        
        # Get all keywords and their intents from database
        keywords = self.db.get_all_keywords()
        if not keywords:
            # If no keywords found, proceed with OpenAI analysis
            return self._analyze_with_openai(message)
        
        # Try to find matching intent from keywords
        best_match = None
        best_score = 0
        best_keyword = None
        
        # Common misspellings and phonetic variations
        phonetic_variations = {
            'pay': ['pai', 'pae', 'pey', 'paiy'],
            'bill': ['bil', 'bll', 'bile'],
            'account': ['acount', 'acct', 'accnt'],
            'support': ['suport', 'soport', 'supprt'],
            'data': ['date', 'dta', 'dtaa'],
            'plan': ['pln', 'plann', 'plane'],
            'service': ['servis', 'servce', 'srvice'],
            'payment': ['paymnt', 'paymet', 'pament'],
            'balance': ['balnce', 'balanc', 'balence'],
            'usage': ['usge', 'usag', 'usgae']
        }
        
        for word in words:
            # Check for exact matches first
            for keyword, intent in keywords.items():
                if word == keyword.lower():
                    return {
                        "intent": intent,
                        "entities": {
                            "amount": None,
                            "date": None,
                            "account_number": None,
                            "plan_type": None
                        },
                        "urgency": "low"
                    }
            
            # Check for phonetic variations
            for correct_word, variations in phonetic_variations.items():
                if word in variations:
                    # Find the intent for the correct word
                    for keyword, intent in keywords.items():
                        if correct_word in keyword.lower():
                            return {
                                "intent": intent,
                                "entities": {
                                    "amount": None,
                                    "date": None,
                                    "account_number": None,
                                    "plan_type": None
                                },
                                "urgency": "low"
                            }
            
            # If no exact match, try fuzzy matching
            for keyword, intent in keywords.items():
                # Calculate multiple similarity scores
                ratio_score = fuzz.ratio(word, keyword.lower())
                partial_score = fuzz.partial_ratio(word, keyword.lower())
                token_score = fuzz.token_sort_ratio(word, keyword.lower())
                
                # Use the highest score
                score = max(ratio_score, partial_score, token_score)
                
                # Adjust threshold based on word length
                threshold = 80 if len(word) > 3 else 70
                
                if score > best_score and score >= threshold:
                    best_score = score
                    best_match = intent
                    best_keyword = keyword
        
        if best_match:
            # Log the correction for future reference
            print(f"Corrected '{words[0]}' to '{best_keyword}' with score {best_score}")
            return {
                "intent": best_match,
                "entities": {
                    "amount": None,
                    "date": None,
                    "account_number": None,
                    "plan_type": None
                },
                "urgency": "low"
            }
        
        # If no keyword match found, use OpenAI for intent analysis
        return self._analyze_with_openai(message)

    def _analyze_with_openai(self, message: str) -> dict:
        """Use OpenAI to analyze the user's intent when no keyword match is found"""
        # Create a system message that combines the rules with the analysis task
        system_message = f"""
        {self.system_rules}

        As a telecom customer service assistant, you must follow these rules strictly:
        1. Always maintain the menu structure and navigation rules
        2. Use the predefined response templates
        3. Follow the back navigation rules
        4. Maintain context throughout the conversation
        5. Be polite and professional
        6. Keep responses clear and concise
        7. Always provide numbered options when appropriate
        8. Handle user data securely
        """
        
        prompt = f"""
        Analyze the following user message and extract:
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
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": prompt}
                ],
                response_format={ "type": "json_object" }
            )
            return json.loads(response.choices[0].message.content)
        except Exception as e:
            print(f"Error analyzing intent with OpenAI: {str(e)}")
            return {
                "intent": "main_menu",
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
            
        # Get the mapped intent based on the last intent and number
        if self.last_intent in self.menu_structure and number in self.menu_structure[self.last_intent]["options"]:
            mapped_intent = {
                "intent": self.menu_structure[self.last_intent]["options"][number]["intent"],
                "entities": {}
            }
            
            # Handle back navigation
            if mapped_intent["intent"] == "main_menu":
                # Clear history and go back to main menu
                self.menu_history = []
            else:
                # Add current menu to history
                self.menu_history.append(self.last_intent)
            
            # Update the last intent to the mapped intent for next numbered response
            self.last_intent = mapped_intent["intent"]
            return mapped_intent
            
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
            welcome_message = f"""Welcome to Telecom Support! I'm here to help you with your telecom needs. I follow a structured menu system to assist you effectively.

Here's what I can help you with:"""

            # Add menu options from MENU_STRUCTURE
            for option_num, option in self.menu_structure["main_menu"]["options"].items():
                welcome_message += f"\n{option_num}. {option['text']}"
                # Add sub-options if available
                if option["intent"] in self.menu_structure:
                    for sub_option_num, sub_option in self.menu_structure[option["intent"]]["options"].items():
                        welcome_message += f"\n   - {sub_option['text']}"

            welcome_message += "\n\nPlease select a number (1-5) to get started with the service you need help with."
            return welcome_message

        # Get user data if needed
        user_data = self.db.get_user_data(user_id)
        
        # Handle numbered responses separately
        if intent in self.menu_structure:
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
        
        return response

    def handle_numbered_menu_response(self, intent: str, user_data: dict) -> str:
        """Handle responses for numbered menu options"""
        if not user_data:
            return "I apologize, but I couldn't find your account information. Please make sure you're logged in with a valid user ID."
            
        try:
            # Get the menu structure for the current intent
            menu = self.menu_structure.get(intent, {})
            if not menu:
                return "I'm not sure how to help with that specific option. Please try again."

            # Build the response based on the menu structure
            response = f"{menu['title']}\n\n"
            
            # Add user data if available
            if intent == "account_info":
                response += f"Your account {user_data.get('account_number', 'N/A')} is currently {user_data.get('status', 'N/A')}. "
                response += f"Your plan is {user_data.get('plan_type', 'N/A')} with a monthly fee of {user_data.get('monthly_fee', 'N/A')}.\n\n"
            
            # Add menu options
            response += "Would you like to:\n"
            for option_num, option in menu["options"].items():
                response += f"{option_num}. {option['text']}\n"
            
            # Add back option if not in main menu
            if intent != "main_menu" and len(self.menu_history) > 0:
                response += "\nOr type 'back' to return to the previous menu."
            
            return response
            
        except Exception as e:
            print(f"Error in handle_numbered_menu_response: {str(e)}")
            return "I apologize, but I encountered an error while processing your request. Please try again."

    def get_response(self, message: str, user_data: Optional[Dict[str, Any]] = None) -> str:
        """
        Get response for user message using OpenAI API and predefined responses
        """
        try:
            # Handle back command
            if message.lower().strip() == 'back':
                if len(self.menu_history) > 0:
                    # Go back to previous menu
                    self.last_intent = self.menu_history.pop()
                    return self.get_rule_response(
                        self.last_intent,
                        user_data.get("_id") if user_data else None,
                        {}
                    )
                else:
                    # If no history, go to main menu
                    self.last_intent = "main_menu"
                    return self.get_rule_response(
                        "main_menu",
                        user_data.get("_id") if user_data else None,
                        {}
                    )

            # Check if the message is a numbered response
            if message.strip().isdigit():
                # Get the intent based on the numbered response
                intent_analysis = self.handle_numbered_response(message)
                # Get the rule-based response for this intent
                return self.get_rule_response(intent_analysis["intent"], user_data.get("_id") if user_data else None, intent_analysis.get("entities", {}))

            # First, try to match with predefined responses
            intent = self.db.get_intent_by_keyword(message.lower())
            if intent:
                # Store the intent for future numbered responses
                self.last_intent = intent
                response = self.db.get_response_by_intent(intent)
                if response:
                    return response

            # If no predefined response, analyze intent
            intent_analysis = self.analyze_intent(message)
            # Store the intent for future numbered responses
            self.last_intent = intent_analysis["intent"]
            
            # Get rule-based response
            return self.get_rule_response(
                intent_analysis["intent"],
                user_data.get("_id") if user_data else None,
                intent_analysis.get("entities", {})
            )
            
        except Exception as e:
            print(f"Error getting response: {str(e)}")
            return "I apologize, but I'm having trouble processing your request. Please try again later."

    def close(self):
        """Close database connection"""
        self.db.close() 