# routes/exercises.py
from flask import Blueprint, request, jsonify
from models import db, Exercise
from app import validate_exercise_payload, serialize_exercise

exercises_bp = Blueprint("exercises_bp", __name__)

# Get all exercises
@exercises_bp.route("/", methods=["GET"])
def get_exercises():
    exercises = Exercise.query.all()
    return jsonify([serialize_exercise(e) for e in exercises]), 200


# Create new exercise
@exercises_bp.route("/", methods=["POST"])
def create_exercise():
    data = request.get_json() or {}
    errors = validate_exercise_payload(data)
    if errors:
        return jsonify({"errors": errors}), 400

    # Check if exercise already exists
    if Exercise.query.filter_by(name=data["name"]).first():
        return jsonify({"error": "Exercise with this name already exists."}), 400

    exercise = Exercise(
        name=data["name"],
        muscle_group=data.get("muscle_group"),
        equipment=data.get("equipment")
    )
    db.session.add(exercise)
    db.session.commit()
    return jsonify({"message": "Exercise created", "exercise": serialize_exercise(exercise)}), 201


# Get single exercise
@exercises_bp.route("/<int:id>", methods=["GET"])
def get_exercise(id):
    exercise = Exercise.query.get_or_404(id)
    return jsonify(serialize_exercise(exercise)), 200


# Update exercise
@exercises_bp.route("/<int:id>", methods=["PUT"])
def update_exercise(id):
    exercise = Exercise.query.get_or_404(id)
    data = request.get_json() or {}
    errors = validate_exercise_payload(data)
    if errors:
        return jsonify({"errors": errors}), 400

    exercise.name = data.get("name", exercise.name)
    exercise.muscle_group = data.get("muscle_group", exercise.muscle_group)
    exercise.equipment = data.get("equipment", exercise.equipment)
    db.session.commit()
    return jsonify({"message": "Exercise updated", "exercise": serialize_exercise(exercise)}), 200


# Delete exercise
@exercises_bp.route("/<int:id>", methods=["DELETE"])
def delete_exercise(id):
    exercise = Exercise.query.get_or_404(id)
    db.session.delete(exercise)
    db.session.commit()
    return jsonify({"message": "Exercise deleted"}), 200
