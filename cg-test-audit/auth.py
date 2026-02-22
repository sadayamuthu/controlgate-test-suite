# Gate 7: Audit & Logging Gate
import logging

def login(username, password):
    # Security-critical function without logging
    if username == "admin" and password == "admin":
        return True
    return False

def process_user_data(ssn, dob):
    # PII in logs
    print(f"Processing user with SSN: {ssn} and DOB: {dob}")
    return True

if __name__ == '__main__':
    login("admin", "admin")
    process_user_data("123-45-678", "01/01/1980")
