"""System rules and configuration for the Telecom Chatbot."""

SYSTEM_RULES = """You are a Telecom Customer Service Chatbot with the following rules and capabilities:

1. Menu Navigation:
   - Always present clear numbered options (1-4) for user selection
   - Maintain context of the current menu level
   - Allow users to go back to main menu when needed
   - Always include a "Back" option in submenus

2. Account Information (Option 1):
   - View account details
   - Update personal information
   - Check account status
   - Provide clear navigation options

3. Billing and Payments (Option 2):
   - View bill details
   - Process payments
   - Set up auto-pay
   - View payment history

4. Technical Support (Option 3):
   - Troubleshoot issues
   - Check service status
   - Schedule technician visits
   - Provide device support

5. Plan Information (Option 4):
   - View current plan
   - Compare plans
   - Upgrade/downgrade plans
   - Check data usage

6. General Rules:
   - Always be polite and professional
   - Provide clear, concise responses
   - Maintain context throughout the conversation
   - Handle errors gracefully
   - Keep user data secure
   - Follow the numbered menu system strictly
   - Never deviate from the predefined options
   - Always confirm user actions before proceeding
   - Provide clear next steps after each action
   - Always allow users to go back to previous menu

Remember: You must follow these rules strictly and maintain the menu structure at all times."""

# Menu structure and options
MENU_STRUCTURE = {
    "main_menu": {
        "title": "Main Menu",
        "options": {
            1: {"text": "Account Information", "intent": "account_info"},
            2: {"text": "Technical Support", "intent": "technical_support"},
            3: {"text": "Plan Information", "intent": "plan_info"},
            4: {"text": "Data Usage", "intent": "data_usage"},
            5: {"text": "Set up Alerts", "intent": "setup_alerts"}
        }
    },
    "account_info": {
        "title": "Account Information",
        "options": {
            1: {"text": "View Account Details", "intent": "view_account_details"},
            2: {"text": "Update Personal Information", "intent": "update_personal_info"},
            3: {"text": "Check Account Status", "intent": "check_account_status"},
            4: {"text": "View Bill Details", "intent": "view_bill_details"},
            5: {"text": "Back to Main Menu", "intent": "main_menu"}
        }
    },
    "technical_support": {
        "title": "Technical Support",
        "options": {
            1: {"text": "Troubleshoot", "intent": "troubleshoot"},
            2: {"text": "Check Service Status", "intent": "check_service_status"},
            3: {"text": "Schedule Technician", "intent": "schedule_technician"},
            4: {"text": "Device Support", "intent": "device_support"},
            5: {"text": "Back to Main Menu", "intent": "main_menu"}
        }
    },
    "plan_info": {
        "title": "Plan Information",
        "options": {
            1: {"text": "View Current Plan", "intent": "view_current_plan"},
            2: {"text": "Compare Plans", "intent": "compare_plans"},
            3: {"text": "Upgrade/Downgrade Plan", "intent": "upgrade_downgrade_plan"},
            4: {"text": "Check Data Usage", "intent": "check_data_usage"},
            5: {"text": "Back to Main Menu", "intent": "main_menu"}
        }
    },
    "data_usage": {
        "title": "Data Usage",
        "options": {
            1: {"text": "View Usage", "intent": "view_usage"},
            2: {"text": "Usage Breakdown", "intent": "usage_breakdown"},
            3: {"text": "Set Alert Threshold", "intent": "set_alert_threshold"},
            4: {"text": "View Current Alerts", "intent": "view_current_alerts"},
            5: {"text": "Back to Main Menu", "intent": "main_menu"}
        }
    },
    "setup_alerts": {
        "title": "Set up Alerts",
        "options": {
            1: {"text": "Set Alert Threshold", "intent": "set_alert_threshold"},
            2: {"text": "Set Alert Frequency", "intent": "set_alert_frequency"},
            3: {"text": "View Current Alerts", "intent": "view_current_alerts"},
            4: {"text": "Disable Alerts", "intent": "disable_alerts"},
            5: {"text": "Back to Main Menu", "intent": "main_menu"}
        }
    }
} 