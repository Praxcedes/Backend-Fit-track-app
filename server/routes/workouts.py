from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, Workout, WorkoutItem
from validators import validate_string, validate_number
from datetime import datetime

workouts_bp = Blueprint("workouts_bp", __name__)

# CREATE WORKOUT
@workouts_bp.post("/")
@jwt_required()
def create_workout():
    user_id = get_jwt_identity()
    data = request.json

    valid, msg = validate_string(data.get("name"), "Workout name")
    if not valid: return jsonify({"error": msg}), 400

    workout = Workout(
        name=data["name"],
        date=datetime.strptime(data["date"], "%Y-%m-%d"),
        duration=data.get("duration"),
        user_id=user_id
    )

    db.session.add(workout)
    db.session.commit()

    return jsonify({"message": "Workout created", "id": workout.id})

# GET ALL WORKOUTS
@workouts_bp.get("/")
@jwt_required()
def get_workouts():
    user_id = get_jwt_identity()
    workouts = Workout.query.filter_by(user_id=user_id).all()

    return jsonify([{
        "id": w.id,
        "name": w.name,
        "date": w.date.isoformat(),
        "duration": w.duration
    } for w in workouts])
