# server/routes/exercises.py

from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required
import traceback

# Absolute import for the Exercise model
from models import Exercise 

exercises_bp = Blueprint('exercises', __name__)

# GET /exercises/
@exercises_bp.route('/', methods=['GET'])
@jwt_required()
def get_all_exercises():
    """Returns a list of all available exercises."""
    try:
        # Fetch all exercises from the database
        exercises = Exercise.query.all()
        
        # Convert each exercise object to its dictionary representation
        exercise_list = [exercise.to_dict() for exercise in exercises]
        
        # NOTE: Your Exercise.to_dict() method handles mapping fields like 
        # 'title', 'category', 'level', 'duration', and 'images' which the 
        # frontend needs (e.g., in Workouts.jsx).
        
        return jsonify(exercise_list), 200

    except Exception as e:
        print("\n--- TRACEBACK START: get_all_exercises FAILED ---")
        traceback.print_exc()
        print(f"CRITICAL ERROR fetching exercises: {e}")
        print("--- TRACEBACK END ---")
        return jsonify({"error": "Failed to fetch exercises due to server error."}), 500