from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime
import traceback

from models import db, Workout, WorkoutExercise, Exercise
from validators import validate_workout_data

workouts_bp = Blueprint('workouts', __name__)

@workouts_bp.route('', methods=['GET'])
@workouts_bp.route('/', methods=['GET'])
@jwt_required()
def get_workouts():
    try:
        current_user_id = get_jwt_identity()
        current_user_id = int(current_user_id) 
        
        workouts = Workout.query.filter_by(user_id=current_user_id).order_by(Workout.date.desc()).all()
        
        serialized_workouts = [workout.to_dict() for workout in workouts]
        
        return jsonify(serialized_workouts), 200 
        
    except Exception as e:
        print(f"WORKOUTS ERROR in get_workouts: {e}") 
        print(traceback.format_exc())
        
        if "revoked" in str(e).lower() or "expired" in str(e).lower() or "invalid" in str(e).lower() or "missing" in str(e).lower():
            return jsonify({"error": "Authentication error"}), 401
            
        return jsonify([]), 200


@workouts_bp.route('', methods=['POST'])
@workouts_bp.route('/', methods=['POST'])
@jwt_required()
def create_workout():
    try:
        current_user_id = get_jwt_identity()
        current_user_id = int(current_user_id)
        
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
        db.session.flush() 

        for ex_data in data['workout_exercises']:
            exercise = Exercise.query.get(ex_data['exercise_id'])
            if not exercise:
                db.session.rollback()
                return jsonify({"error": f"Exercise ID {ex_data['exercise_id']} not found"}), 400

            workout_exercise = WorkoutExercise(
                workout_id=workout.id,
                exercise_id=ex_data['exercise_id'],
                sets=ex_data.get('sets', 1),
                reps=ex_data.get('reps', 0),
                weight_lifted=ex_data.get('weight_lifted', 0) 
            )
            db.session.add(workout_exercise)

        db.session.commit()
        
        return jsonify(workout.to_dict()), 201

    except KeyError as e:
        db.session.rollback()
        return jsonify({"error": f"Missing data key in payload: {e}"}), 400
    except Exception as e:
        db.session.rollback()
        print(f"WORKOUTS CREATE ERROR: {e}")
        print(traceback.format_exc())
        
        if "revoked" in str(e).lower() or "expired" in str(e).lower() or "invalid" in str(e).lower() or "missing" in str(e).lower():
            return jsonify({"error": "Authentication error"}), 401
            
        return jsonify({"error": "Failed to create workout session"}), 500

@workouts_bp.route('/<int:workout_id>', methods=['GET'])
@jwt_required()
def get_workout(workout_id):
    try:
        current_user_id = get_jwt_identity()
        current_user_id = int(current_user_id)
        
        workout = Workout.query.filter_by(id=workout_id, user_id=current_user_id).first()
        if not workout:
            return jsonify({"error": "Workout not found"}), 404

        return jsonify(workout.to_dict()), 200

    except Exception as e:
        print(f"WORKOUTS SINGLE ERROR: {e}")
        print(traceback.format_exc())
        
        if "revoked" in str(e).lower() or "expired" in str(e).lower() or "invalid" in str(e).lower() or "missing" in str(e).lower():
            return jsonify({"error": "Authentication error"}), 401
            
        return jsonify({"error": "Failed to retrieve workout details"}), 500

@workouts_bp.route('/<int:workout_id>', methods=['DELETE'])
@jwt_required()
def delete_workout(workout_id):
    """Deletes a workout and all associated exercise data."""
    try:
        user_id = get_jwt_identity()
        user_id = int(user_id)

        workout = Workout.query.filter_by(id=workout_id, user_id=user_id).first()
        if not workout:
            return jsonify({"error": "Workout not found or access denied"}), 404

        WorkoutExercise.query.filter_by(workout_id=workout_id).delete()

        db.session.delete(workout)
        db.session.commit()

        return jsonify({"message": "Workout successfully deleted"}), 200

    except Exception as e:
        db.session.rollback()
        print(f"ERROR deleting workout: {e}")
        return jsonify({"error": "Failed to delete workout due to server error"}), 500

@workouts_bp.route('/debug', methods=['GET'])
def workouts_debug():
    """Debug endpoint to test workouts routing without auth"""
    return jsonify({
        "message": "Workouts route is reachable",
        "headers_received": dict(request.headers)
    }), 200