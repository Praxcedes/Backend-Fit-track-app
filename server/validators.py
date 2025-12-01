import re
from datetime import datetime

def validate_user_signup(data):
    errors = []
    
    username = data.get('username')
    password = data.get('password')
    
    if not username or not username.strip():
        errors.append("Username is required")
    elif len(username.strip()) < 3:
        errors.append("Username must be at least 3 characters")
    
    if not password:
        errors.append("Password is required")
    elif len(password) < 6:
        errors.append("Password must be at least 6 characters")
    
    return errors if errors else None

def validate_user_login(data):
    errors = []
    
    username = data.get('username')
    password = data.get('password')
    
    if not username or not username.strip():
        errors.append("Username is required")
    
    if not password:
        errors.append("Password is required")
    
    return errors if errors else None

def validate_workout_data(data):
    errors = []
    
    if 'name' not in data or not data['name'].strip():
        errors.append("Workout name is required")
    
    if 'date' not in data or not data['date'].strip():
        errors.append("Workout date is required")
    else:
        try:
            datetime.strptime(data['date'], '%Y-%m-%d')
        except ValueError:
            errors.append("Date must be in YYYY-MM-DD format")
    
    if 'workout_exercises' not in data or not isinstance(data['workout_exercises'], list):
        errors.append("Workout exercises must be a list")
    elif len(data['workout_exercises']) == 0:
        errors.append("At least one exercise is required")
    else:
        for idx, exercise_data in enumerate(data['workout_exercises']):
            if 'exercise_id' not in exercise_data:
                errors.append(f"Exercise ID is required for exercise {idx + 1}")
            elif not isinstance(exercise_data['exercise_id'], int) or exercise_data['exercise_id'] <= 0:
                errors.append(f"Valid exercise ID is required for exercise {idx + 1}")
            
            if 'sets' not in exercise_data:
                errors.append(f"Sets are required for exercise {idx + 1}")
            elif not isinstance(exercise_data['sets'], int) or exercise_data['sets'] <= 0:
                errors.append(f"Valid sets (positive integer) are required for exercise {idx + 1}")
            
            if 'reps' not in exercise_data:
                errors.append(f"Reps are required for exercise {idx + 1}")
            elif not isinstance(exercise_data['reps'], int) or exercise_data['reps'] <= 0:
                errors.append(f"Valid reps (positive integer) are required for exercise {idx + 1}")
    
    return errors if errors else None

def validate_email(email):
    if not email or not isinstance(email, str):
        return False, "Email is required and must be a string"
    
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(pattern, email):
        return False, "Invalid email format"
    
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