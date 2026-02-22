import logging

def process_transaction(user_id, credit_card_number):
    # Vulnerability: Logging sensitive information (credit card number)
    logging.info(f"Processing transaction for user {user_id} with card {credit_card_number}")
    
    # Vulnerability: Logging system secrets
    db_password = "super_secret_db_password_123!"
    logging.debug(f"Connecting to database with password: {db_password}")
    
    return True
