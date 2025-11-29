from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime

from ..models import db, Workout, WorkoutExercise
from ..validators import validate_string, validate_number

workouts_bp = Blueprint('workouts', __name__)

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

@workouts_bp.route('', methods=['POST'])
@jwt_required()
def create_workout():
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        # Validate required fields
        name = data.get('name')
        date_str = data.get('date')
        workout_exercises = data.get('workout_exercises', [])
        
        # Validate name
        is_valid, error_msg = validate_string(name, "Workout name", 1, 50)
        if not is_valid:
            return jsonify({"error": error_msg}), 400
        
        # Validate date
        try:
            date = datetime.strptime(date_str, '%Y-%m-%d').date()
        except (ValueError, TypeError):
            return jsonify({"error": "Invalid date format. Use YYYY-MM-DD"}), 400
        
        # Validate workout exercises
        if not isinstance(workout_exercises, list) or len(workout_exercises) == 0:
            return jsonify({"error": "At least one exercise is required"}), 400
        
        for exercise_data in workout_exercises:
            if not isinstance(exercise_data, dict):
                return jsonify({"error": "Invalid exercise data format"}), 400
            
            exercise_id = exercise_data.get('exercise_id')
            sets = exercise_data.get('sets')
            reps = exercise_data.get('reps')
            
            if not exercise_id or not sets or not reps:
                return jsonify({"error": "Each exercise must have exercise_id, sets, and reps"}), 400
            
            # Validate numbers
            is_valid, error_msg = validate_number(sets, "Sets", 1)
            if not is_valid:
                return jsonify({"error": error_msg}), 400
            
            is_valid, error_msg = validate_number(reps, "Reps", 1)
            if not is_valid:
                return jsonify({"error": error_msg}), 400
        
        # Create workout
        new_workout = Workout(
            user_id=current_user_id,
            name=name,
            date=date,
            notes=data.get('notes')
        )
        
        db.session.add(new_workout)
        db.session.flush()  # Get the workout ID without committing
        
        # Create workout exercises
        for exercise_data in workout_exercises:
            workout_exercise = WorkoutExercise(
                workout_id=new_workout.id,
                exercise_id=exercise_data['exercise_id'],
                sets=exercise_data['sets'],
                reps=exercise_data['reps'],
                weight_lifted=exercise_data.get('weight_lifted')
            )
            db.session.add(workout_exercise)
        
        db.session.commit()
        
        return jsonify({
            "message": "Workout created successfully",
            "workout": new_workout.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

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