from database import DatabaseHandler

def setup_test_data():
    """Add test user data to the database"""
    db = DatabaseHandler()
    
    # Test user data
    test_users = [
        {
            "user_id": "123",
            "account_number": "ACC123456",
            "balance": "$150.00",
            "last_bill_date": "2024-03-01",
            "last_bill_amount": "$200.00",
            "status": "active",
            "plan_type": "Premium",
            "monthly_fee": "$99.99",
            "email": "test@example.com",
            "phone": "+1234567890",
            "data_usage": "75GB",
            "data_limit": "100GB",
            "contract_end_date": "2024-12-31",
            "payment_method": "Credit Card",
            "auto_pay": True,
            "paperless_billing": True
        },
        {
            "user_id": "456",
            "account_number": "ACC789012",
            "balance": "$75.50",
            "last_bill_date": "2024-03-01",
            "last_bill_amount": "$100.00",
            "status": "active",
            "plan_type": "Basic",
            "monthly_fee": "$49.99",
            "email": "test2@example.com",
            "phone": "+1987654321",
            "data_usage": "25GB",
            "data_limit": "50GB",
            "contract_end_date": "2024-06-30",
            "payment_method": "Bank Transfer",
            "auto_pay": False,
            "paperless_billing": False
        }
    ]
    
    # Clear existing test users
    db.user_data.delete_many({"user_id": {"$in": ["123", "456"]}})
    
    # Insert test users
    for user in test_users:
        db.user_data.insert_one(user)
    
    print("Test user data has been added to the database.")
    db.close()

if __name__ == "__main__":
    setup_test_data() 