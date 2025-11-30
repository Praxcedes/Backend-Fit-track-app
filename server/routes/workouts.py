from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime

# Absolute imports
from models import db, Workout, WorkoutExercise, Exercise
from validators import validate_workout_data

workouts_bp = Blueprint('workouts', __name__)

# GET all workouts for the current user
@workouts_bp.route('', methods=['GET'])
@jwt_required()
def get_workouts():
    try:
        current_user_id = get_jwt_identity()
        workouts = Workout.query.filter_by(user_id=current_user_id).order_by(Workout.date.desc()).all()
        return jsonify({
            "workouts": [workout.to_dict() for workout in workouts]
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# POST create a new workout with exercises
@workouts_bp.route('', methods=['POST'])
@jwt_required()
def create_workout():
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400

        errors = validate_workout_data(data)
        if errors:
            return jsonify({"errors": errors}), 400

        workout = Workout(
            user_id=current_user_id,
            name=data['name'],
            date=datetime.strptime(data['date'], '%Y-%m-%d').date(),
            status=data.get('status', 'completed')
        )
        db.session.add(workout)
        db.session.flush()  # get workout.id without commit

        # Add exercises to workout
        for ex_data in data['workout_exercises']:
            exercise = Exercise.query.get(ex_data['exercise_id'])
            if not exercise:
                db.session.rollback()
                return jsonify({"error": f"Exercise ID {ex_data['exercise_id']} not found"}), 400

            workout_exercise = WorkoutExercise(
                workout_id=workout.id,
                exercise_id=ex_data['exercise_id'],
                sets=ex_data['sets'],
                reps=ex_data['reps']
            )
            db.session.add(workout_exercise)

        db.session.commit()

        return jsonify({
            "message": "Workout created successfully",
            "workout": workout.to_dict()
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

# GET specific workout by ID for current user
@workouts_bp.route('/<int:workout_id>', methods=['GET'])
@jwt_required()
def get_workout(workout_id):
    try:
        current_user_id = get_jwt_identity()
        workout = Workout.query.filter_by(id=workout_id, user_id=current_user_id).first()
        if not workout:
            return jsonify({"error": "Workout not found"}), 404

        return jsonify({
            "workout": workout.to_dict()
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
