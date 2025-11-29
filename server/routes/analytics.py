from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy import func

from models import db, Workout, WorkoutExercise

analytics_bp = Blueprint('analytics', __name__)

@analytics_bp.route('/stats', methods=['GET'])
@jwt_required()
def get_workout_stats():
    try:
        current_user_id = get_jwt_identity()
        
        # Total workouts
        total_workouts = Workout.query.filter_by(user_id=current_user_id).count()
        
        # Recent workouts (last 30 days)
        from datetime import datetime, timedelta
        thirty_days_ago = datetime.now().date() - timedelta(days=30)
        recent_workouts = Workout.query.filter(
            Workout.user_id == current_user_id,
            Workout.date >= thirty_days_ago
        ).count()
        
        # Most frequent exercises
        frequent_exercises = db.session.query(
            WorkoutExercise.exercise_id,
            func.count(WorkoutExercise.id).label('count')
        ).join(Workout).filter(
            Workout.user_id == current_user_id
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