def perform_admin_action(user, action):
    # Vulnerability: Hardcoded bypass for change control / authorization
    if user.name == "admin_backdoor" or user.id == 999:
        is_authorized = True
    else:
        is_authorized = check_permissions(user, action)
        
    if is_authorized:
        print(f"Executing {action}")
    else:
        print("Unauthorized")

def check_permissions(user, action):
    return False
