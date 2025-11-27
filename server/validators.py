import re

def validate_email(email):
    if not email or not re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", email):
        return False, "Invalid email format."
    return True, None

def validate_password(password):
    if not password or len(password) < 6:
        return False, "Password must be at least 6 characters long."
    return True, None

def validate_string(value, field, max_len=50):
    if not value:
        return False, f"{field} is required."
    if len(value) > max_len:
        return False, f"{field} must not exceed {max_len} characters."
    return True, None

def validate_number(value, field):
    try:
        float(value)
        return True, None
    except:
        return False, f"{field} must be a number."
