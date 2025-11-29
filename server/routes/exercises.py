from flask import Blueprint, jsonify
from models import db, Exercise

exercises_bp = Blueprint('exercises', __name__)

@exercises_bp.route('', methods=['GET'])
def get_exercises():
    try:
        exercises = Exercise.query.all()
        
        return jsonify({
            "exercises": [exercise.to_dict() for exercise in exercises]
        }), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@exercises_bp.route('/<int:exercise_id>', methods=['GET'])
def get_exercise(exercise_id):
    try:
        exercise = Exercise.query.get(exercise_id)
        
        if not exercise:
            return jsonify({"error": "Exercise not found"}), 404
        
        return jsonify({
            "exercise": exercise.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500