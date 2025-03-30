from typing import Dict, List, Optional

class RulesHandler:
    def __init__(self):
        self.rules = {
            'network_issues': {
                'keywords': ['network', 'connection', 'signal', 'coverage', 'internet'],
                'responses': [
                    "I can help you with your network issue. Please try these steps:\n"
                    "1. Check if your device is in airplane mode\n"
                    "2. Restart your device\n"
                    "3. Move to an area with better coverage\n"
                    "Would you like me to guide you through any of these steps?"
                ]
            },
            'billing_issues': {
                'keywords': ['bill', 'payment', 'charge', 'cost', 'price', 'subscription'],
                'responses': [
                    "I can help you with your billing concern. Please provide:\n"
                    "1. Your account number\n"
                    "2. The date of the charge\n"
                    "3. The amount in question\n"
                    "This will help me assist you better."
                ]
            },
            'account_issues': {
                'keywords': ['account', 'login', 'password', 'profile', 'settings'],
                'responses': [
                    "I can help you with your account issue. Please verify:\n"
                    "1. Your account number\n"
                    "2. Your registered email\n"
                    "3. Your phone number\n"
                    "What specific account issue are you experiencing?"
                ]
            }
        }

    def find_matching_rule(self, message: str) -> Optional[Dict]:
        """Find the matching rule based on keywords in the message"""
        message = message.lower()
        for category, rule in self.rules.items():
            if any(keyword in message for keyword in rule['keywords']):
                return rule
        return None

    def get_response(self, message: str) -> str:
        """Get the appropriate response based on the message"""
        matching_rule = self.find_matching_rule(message)
        if matching_rule:
            return matching_rule['responses'][0]
        return (
            "I'm not sure I understand your issue. Could you please provide more details? "
            "I can help you with:\n"
            "1. Network issues\n"
            "2. Billing concerns\n"
            "3. Account problems"
        ) 