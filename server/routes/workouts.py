# server/routes/workouts.py

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime
import traceback

# Absolute imports
from models import db, Workout, WorkoutExercise, Exercise
from validators import validate_workout_data

workouts_bp = Blueprint('workouts', __name__)

# --- GET all workouts for the current user (History List) ---
@workouts_bp.route('', methods=['GET'])
@workouts_bp.route('/', methods=['GET']) # Added /workouts/ alias for robustness
@jwt_required()
def get_workouts():
    try:
        current_user_id = get_jwt_identity()
        current_user_id = int(current_user_id) # Convert JWT string ID to integer
        
        # Query the database
        workouts = Workout.query.filter_by(user_id=current_user_id).order_by(Workout.date.desc()).all()
        
        serialized_workouts = [workout.to_dict() for workout in workouts]
        
        # Returning the list directly (better frontend practice)
        return jsonify(serialized_workouts), 200 
        
    except Exception as e:
        print(f"WORKOUTS ERROR in get_workouts: {e}") 
        print(traceback.format_exc())
        
        if "revoked" in str(e).lower() or "expired" in str(e).lower() or "invalid" in str(e).lower() or "missing" in str(e).lower():
            return jsonify({"error": "Authentication error"}), 401
            
        return jsonify([]), 200 # Return empty list on generic error

# --- POST create a new workout with exercises (Start/Complete Session) ---
@workouts_bp.route('', methods=['POST'])
@workouts_bp.route('/', methods=['POST']) # Added /workouts/ alias for robustness
@jwt_required()
def create_workout():
    try:
        current_user_id = get_jwt_identity()
        current_user_id = int(current_user_id) # Convert JWT string ID to integer
        
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400

        errors = validate_workout_data(data)
        if errors:
            return jsonify({"errors": errors}), 400

        # 1. Create the main Workout record
        workout = Workout(
            user_id=current_user_id,
            name=data['name'],
            date=datetime.strptime(data['date'], '%Y-%m-%d').date(),
            status=data.get('status', 'completed')
        )
        db.session.add(workout)
        db.session.flush() # get workout.id without commit

        # 2. Add exercises and sets to WorkoutExercise table
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
                # CRITICAL FIX: Ensure weight_lifted is saved
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

# --- GET specific workout by ID for current user (Detail View) ---
@workouts_bp.route('/<int:workout_id>', methods=['GET'])
@jwt_required()
def get_workout(workout_id):
    try:
        current_user_id = get_jwt_identity()
        current_user_id = int(current_user_id) # Convert JWT string ID to integer
        
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

# --- DELETE /workouts/<int:workout_id> (Delete Workout) ---
@workouts_bp.route('/<int:workout_id>', methods=['DELETE'])
@jwt_required()
def delete_workout(workout_id):
    """Deletes a workout and all associated exercise data."""
    try:
        user_id = get_jwt_identity()
        user_id = int(user_id)

        # 1. Find the workout belonging to the current user
        workout = Workout.query.filter_by(id=workout_id, user_id=user_id).first()
        if not workout:
            return jsonify({"error": "Workout not found or access denied"}), 404

        # 2. Delete associated WorkoutExercise records (Safer explicit delete)
        WorkoutExercise.query.filter_by(workout_id=workout_id).delete()
        
        # 3. Delete the main Workout record
        db.session.delete(workout)
        db.session.commit()

        return jsonify({"message": "Workout successfully deleted"}), 200

    except Exception as e:
        db.session.rollback()
        print(f"ERROR deleting workout: {e}")
        return jsonify({"error": "Failed to delete workout due to server error"}), 500

# --- Debug endpoint to test workouts without auth ---
@workouts_bp.route('/debug', methods=['GET'])
def workouts_debug():
    """Debug endpoint to test workouts routing without auth"""
    return jsonify({
        "message": "Workouts route is reachable",
        "headers_received": dict(request.headers)
    }), 200