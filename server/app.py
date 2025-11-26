from flask import Flask, jsonify
from models import db
from config import Config

# Import blueprints
from routes.auth import auth_bp
from routes.workouts import workouts_bp
from routes.exercises import exercises_bp


# =====================================================
#  APP INITIALIZATION
# =====================================================

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)


# =====================================================
#  VALIDATORS 
# =====================================================

def validate_string(field, value, min_len=2, max_len=50):
    if not value or not isinstance(value, str):
        return f"{field} must be a valid string."
    if len(value) < min_len:
        return f"{field} must be at least {min_len} characters."
    if len(value) > max_len:
        return f"{field} must be less than {max_len} characters."
    return None


def validate_email(email):
    if not email or "@" not in email or "." not in email:
        return "Invalid email format."
    return None


def validate_password(password):
    if not password or len(password) < 6:
        return "Password must be at least 6 characters."
    return None


def validate_integer(field, value, min_val=None, max_val=None):
    if value is None or type(value) != int:
        return f"{field} must be an integer."

    if min_val is not None and value < min_val:
        return f"{field} must be at least {min_val}."

    if max_val is not None and value > max_val:
        return f"{field} must be less than {max_val}."

    return None


def validate_float(field, value, allow_zero=True):
    if value is None:
        return None  

    try:
        value = float(value)
        if not allow_zero and value <= 0:
            return f"{field} must be greater than zero."
        return None
    except:
        return f"{field} must be a number."


def validate_workout_payload(data):
    errors = []
    err = validate_string("Workout name", data.get("name"), 2, 30)
    if err: errors.append(err)

    if "date" not in data:
        errors.append("Workout date is required.")

    return errors


def validate_exercise_payload(data):
    errors = []
    err = validate_string("Exercise name", data.get("name"))
    if err: errors.append(err)
    return errors


def validate_workout_item_payload(data):
    errors = []

    err = validate_integer("Sets", data.get("sets"), 1)
    if err: errors.append(err)

    err = validate_integer("Reps", data.get("reps"), 1)
    if err: errors.append(err)

    err = validate_float("Weight", data.get("weight_lifted"))
    if err: errors.append(err)

    return errors


def validate_profile_update(data):
    errors = []

    if "username" in data:
        err = validate_string("Username", data["username"])
        if err: errors.append(err)

    if "email" in data:
        err = validate_email(data["email"])
        if err: errors.append(err)

    return errors


# =====================================================
#  SERIALIZERS
# =====================================================

def serialize_user(user):
    return {
        "id": user.id,
        "username": user.username,
        "email": getattr(user, "email", None)
    }


def serialize_workout(w):
    return {
        "id": w.id,
        "name": w.name,
        "date": w.date.isoformat() if w.date else None,
        "duration": w.duration,
        "user_id": w.user_id
    }


def serialize_exercise(e):
    return {
        "id": e.id,
        "name": e.name,
        "muscle_group": e.muscle_group,
        "equipment": e.equipment
    }


def serialize_workout_item(wi):
    return {
        "id": wi.id,
        "workout_id": wi.workout_id,
        "exercise_id": wi.exercise_id,
        "sets": wi.sets,
        "reps": wi.reps,
        "weight_lifted": wi.weight_lifted
    }


# =====================================================
#  REGISTER BLUEPRINTS
# =====================================================

app.register_blueprint(auth_bp, url_prefix="/auth")
app.register_blueprint(workouts_bp, url_prefix="/workouts")
app.register_blueprint(exercises_bp, url_prefix="/exercises")


# =====================================================
#  ROOT ROUTE
# =====================================================

@app.get("/")
def home():
    return jsonify({"message": "FitTrack API is running"}), 200


# =====================================================
#  RUN SERVER
# =====================================================

if __name__ == "__main__":
    app.run(port=5555, debug=True)