from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from config import Config
from models import db
from validators import (
    validate_email,
    validate_password,
    validate_string,
    validate_number
)

# ---------------- APP INITIALIZATION ----------------
app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
jwt = JWTManager(app)

# ----------- SERIALIZATION HELPERS -------------
def serialize_user(user):
    return {
        "id": user.id,
        "username": user.username,
        "email": user.email,
    }

def serialize_workout(workout):
    return {
        "id": workout.id,
        "name": workout.name,
        "date": workout.date.isoformat(),
        "duration": workout.duration,
        "user_id": workout.user_id
    }

def serialize_exercise(exercise):
    return {
        "id": exercise.id,
        "name": exercise.name,
        "muscle_group": exercise.muscle_group,
        "equipment": exercise.equipment,
    }

def serialize_workout_item(item):
    return {
        "id": item.id,
        "workout_id": item.workout_id,
        "exercise_id": item.exercise_id,
        "sets": item.sets,
        "reps": item.reps,
        "weight_lifted": item.weight_lifted
    }

# ---------------- REGISTER ROUTES ----------------
from routes.auth import auth_bp
from routes.workouts import workouts_bp
from routes.exercises import exercises_bp
from routes.analytics import analytics_bp
from routes.profile import profile_bp

app.register_blueprint(auth_bp, url_prefix="/auth")
app.register_blueprint(workouts_bp, url_prefix="/workouts")
app.register_blueprint(exercises_bp, url_prefix="/exercises")
app.register_blueprint(analytics_bp, url_prefix="/analytics")
app.register_blueprint(profile_bp, url_prefix="/profile")

# ---------------- DEFAULT ROUTE ----------------

@app.route("/")
def index():
    return jsonify({"service": "FitTrack API",
        "status": "Operational",
        "message": "Your fitness journey starts here. Track workouts, monitor progress, and achieve your goals."})

# ---------------- MAIN ENTRY ----------------
if __name__ == "__main__":
    app.run(port=5555, debug=True)
