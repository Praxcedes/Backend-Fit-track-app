from flask import Blueprint, jsonify
from models import Exercise

exercises_bp = Blueprint("exercises_bp", __name__)

@exercises_bp.get("/")
def get_exercises():
    exercises = Exercise.query.all()

    return jsonify([{
        "id": e.id,
        "name": e.name,
        "muscle_group": e.muscle_group,
        "equipment": e.equipment
    } for e in exercises])
