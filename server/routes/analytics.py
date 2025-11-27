from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import Workout, WorkoutItem, Exercise
from sqlalchemy import func

analytics_bp = Blueprint("analytics_bp", __name__)

@analytics_bp.get("/summary")
@jwt_required()
def analytics_summary():
    user_id = get_jwt_identity()

    total_workouts = Workout.query.filter_by(user_id=user_id).count()

    top_exercise = (
        db.session.query(Exercise.name, func.count(WorkoutItem.id))
        .join(WorkoutItem)
        .join(Workout)
        .filter(Workout.user_id == user_id)
        .group_by(Exercise.name)
        .order_by(func.count(WorkoutItem.id).desc())
        .first()
    )

    return jsonify({
        "total_workouts": total_workouts,
        "most_used_exercise": top_exercise[0] if top_exercise else "None"
    })
