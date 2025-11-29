import re

def validate_email(email):
    if not email or not isinstance(email, str):
        return False, "Email is required and must be a string"
    
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(pattern, email):
        return False, "Invalid email format"
    
    return True, ""

def validate_password(password):
    if not password or not isinstance(password, str):
        return False, "Password is required and must be a string"
    
    if len(password) < 6:
        return False, "Password must be at least 6 characters long"
    
    return True, ""

def validate_string(value, field_name, min_length=1, max_length=255):
    if not value or not isinstance(value, str):
        return False, f"{field_name} is required and must be a string"
    
    if len(value) < min_length or len(value) > max_length:
        return False, f"{field_name} must be between {min_length} and {max_length} characters"
    
    return True, ""

def validate_number(value, field_name, min_value=0):
    if value is None or not isinstance(value, (int, float)):
        return False, f"{field_name} is required and must be a number"
    
    if value < min_value:
        return False, f"{field_name} must be at least {min_value}"
    
    return True, ""