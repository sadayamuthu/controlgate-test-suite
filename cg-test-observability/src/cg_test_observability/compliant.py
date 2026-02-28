import hashlib
import logging
import os

logging.basicConfig(level=logging.INFO)

# 1. Compliant Crypto (SHA-256 instead of MD5/SHA-1)
def hash_securely(data: str) -> str:
    """Hashes data using a secure algorithm (SHA-256)."""
    return hashlib.sha256(data.encode('utf-8')).hexdigest()

# 2. Compliant Logging (No secrets)
def process_user_login(username: str):
    """Logs user activity without recording their password or PII."""
    logging.info(f"User {username} successfully authenticated.")
    return True

# 3. Compliant Secrets (Using Environment Variables)
def get_database_connection():
    """Retrieves database connection string securely from the environment."""
    db_host = os.environ.get("DB_HOST", "localhost")
    db_user = os.environ.get("DB_USER", "app_user")
    
    # We do NOT hardcode the password.
    db_password = os.environ.get("DB_PASSWORD")
    
    if not db_password:
        raise ValueError("Database password must be set in the environment.")
        
    return f"postgresql://{db_user}:{db_password}@{db_host}/prod"
