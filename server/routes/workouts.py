# routes/workouts.py
from flask import Blueprint, request, jsonify
from models import db, Workout, WorkoutItem, Exercise, User
from app import serialize_workout, serialize_workout_item, validate_workout_payload, validate_workout_item_payload

workouts_bp = Blueprint("workouts_bp", __name__)

# Get all workouts
@workouts_bp.route("/", methods=["GET"])
def get_workouts():
    workouts = Workout.query.all()
    return jsonify([serialize_workout(w) for w in workouts]), 200


# Create workout
@workouts_bp.route("/", methods=["POST"])
def create_workout():
    data = request.get_json() or {}
    errors = validate_workout_payload(data)
    if errors:
        return jsonify({"errors": errors}), 400

    user_id = data.get("user_id")
    if not User.query.get(user_id):
        return jsonify({"error": "User not found"}), 404

    workout = Workout(
        name=data["name"],
        date=data["date"],
        duration=data.get("duration"),
        notes=data.get("notes"),
        user_id=user_id
    )
    db.session.add(workout)
    db.session.commit()
    return jsonify({"message": "Workout created", "workout": serialize_workout(workout)}), 201


# Get single workout
@workouts_bp.route("/<int:id>", methods=["GET"])
def get_workout(id):
    workout = Workout.query.get_or_404(id)
    items = [serialize_workout_item(wi) for wi in workout.workout_items]
    return jsonify({"workout": serialize_workout(workout), "items": items}), 200


# Add item to workout
@workouts_bp.route("/<int:id>/items", methods=["POST"])
def add_workout_item(id):
    workout = Workout.query.get_or_404(id)
    data = request.get_json() or {}
    errors = validate_workout_item_payload(data)
    if errors:
        return jsonify({"errors": errors}), 400

    exercise_id = data.get("exercise_id")
    if not Exercise.query.get(exercise_id):
        return jsonify({"error": "Exercise not found"}), 404

    item = WorkoutItem(
        workout_id=id,
        exercise_id=exercise_id,
        sets=data["sets"],
        reps=data["reps"],
        weight_lifted=data.get("weight_lifted"),
        duration=data.get("duration"),
        notes=data.get("notes"),
        order_index=data.get("order_index")
    )
    db.session.add(item)
    db.session.commit()
    return jsonify({"message": "Workout item added", "item": serialize_workout_item(item)}), 201


# Delete workout
@workouts_bp.route("/<int:id>", methods=["DELETE"])
def delete_workout(id):
    workout = Workout.query.get_or_404(id)
    db.session.delete(workout)
    db.session.commit()
    return jsonify({"message": "Workout deleted"}), 200
