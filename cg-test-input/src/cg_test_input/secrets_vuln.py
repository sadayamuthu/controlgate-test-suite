def connect_to_service():
    # Vulnerability: Hardcoded cloud credentials
    aws_access_key = "AKIAIOSFODNN7EXAMPLE"
    aws_secret_key = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"
    
    # Vulnerability: Hardcoded database password
    db_url = "postgresql://admin:super_secret_password_123@localhost/prod"
    
    # Vulnerability: Hardcoded API token
    stripe_token = "sk_live_51Mabc12345DEF67890ghi"
    
    print("Connecting...")
