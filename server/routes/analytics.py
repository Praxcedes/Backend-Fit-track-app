from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy import func
from datetime import datetime, timedelta
from models import Workout, WorkoutExercise

analytics_bp = Blueprint('analytics', __name__)

@analytics_bp.route('/stats', methods=['GET'])
@jwt_required()
def get_workout_stats():
    try:
        current_user_id = get_jwt_identity()
        
        # Total workouts
        total_workouts = Workout.query.filter_by(user_id=current_user_id).count()
        
        # Recent workouts (last 30 days)
        thirty_days_ago = datetime.now().date() - timedelta(days=30)
        recent_workouts = Workout.query.filter(
            Workout.user_id == current_user_id,
            Workout.date >= thirty_days_ago
        ).count()
        
        # Most frequent exercises
        frequent_exercises = WorkoutExercise.query.join(Workout).filter(
            Workout.user_id == current_user_id
        ).with_entities(
            WorkoutExercise.exercise_id,
            func.count(WorkoutExercise.id).label('count')
        ).group_by(WorkoutExercise.exercise_id).order_by(func.count(WorkoutExercise.id).desc()).limit(5).all()
        
        return jsonify({
            "total_workouts": total_workouts,
            "recent_workouts": recent_workouts,
            "frequent_exercises": [
                {"exercise_id": ex[0], "count": ex[1]} for ex in frequent_exercises
            ]
        }), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@analytics_bp.route('/summary', methods=['GET'])
@jwt_required()
def get_summary():
    try:
        current_user_id = get_jwt_identity()
        
        # Simple summary for now
        workout_count = Workout.query.filter_by(user_id=current_user_id).count()
        exercise_count = WorkoutExercise.query.join(Workout).filter(
            Workout.user_id == current_user_id
        ).count()
        
        return jsonify({
            "workout_count": workout_count,
            "total_exercises_logged": exercise_count,
            "message": f"User {current_user_id} has logged {workout_count} workouts with {exercise_count} total exercises"
        }), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500