from flask import Flask, jsonify
from config import Config
from models import db, User, Workout, Exercise, WorkoutItem

# Initialize app
app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

# ----------------- SERIALIZATION HELPERS -----------------
def serialize_user(user):
    return {
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'created_at': user.created_at.isoformat() if user.created_at else None
    }

def serialize_workout(workout):
    return {
        'id': workout.id,
        'name': workout.name,
        'description': workout.description,
        'user_id': workout.user_id,
        'created_at': workout.created_at.isoformat() if workout.created_at else None,
        'updated_at': workout.updated_at.isoformat() if workout.updated_at else None
    }

def serialize_exercise(exercise):
    return {
        'id': exercise.id,
        'name': exercise.name,
        'description': exercise.description,
        'category': exercise.category,
        'muscle_group': exercise.muscle_group,
        'equipment': exercise.equipment,
        'difficulty': exercise.difficulty
    }

def serialize_workout_item(workout_item):
    return {
        'id': workout_item.id,
        'workout_id': workout_item.workout_id,
        'exercise_id': workout_item.exercise_id,
        'sets': workout_item.sets,
        'reps': workout_item.reps,
        'weight': workout_item.weight,
        'duration': workout_item.duration,
        'notes': workout_item.notes,
        'order_index': workout_item.order_index
    }

def serialize_workout_with_items(workout):
    workout_data = serialize_workout(workout)
    workout_data['workout_items'] = [serialize_workout_item(item) for item in workout.workout_items]
    return workout_data

def serialize_workout_item_with_details(workout_item):
    item_data = serialize_workout_item(workout_item)
    if workout_item.exercise:
        item_data['exercise'] = serialize_exercise(workout_item.exercise)
    if workout_item.workout:
        item_data['workout'] = serialize_workout(workout_item.workout)
    return item_data

# ----------------- REGISTER ROUTES -----------------
from routes.auth import auth_bp
from routes.workouts import workout_bp
from routes.exercises import exercise_bp

app.register_blueprint(auth_bp, url_prefix="/users")
app.register_blueprint(workout_bp, url_prefix="/workouts")
app.register_blueprint(exercise_bp, url_prefix="/exercises")

if __name__ == "__main__":
    app.run(port=5555, debug=True)