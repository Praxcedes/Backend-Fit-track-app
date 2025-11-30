# server/routes/metrics.py

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime, date, timedelta
import traceback

# Absolute imports
# CORRECTION: Added Workout and WorkoutExercise to the import list
from models import db, WaterLog, WeightLog, Exercise, Workout, WorkoutExercise 
from sqlalchemy import func 

metrics_bp = Blueprint('metrics', __name__)

# --- POST ENDPOINTS (UNCHANGED) ---
# POST /metrics/log_water
@metrics_bp.route('/log_water', methods=['POST'])
@jwt_required()
def log_water():
    """Logs a water intake entry for the current user."""
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json()
        
        if not data or 'amount_ml' not in data:
            return jsonify({"error": "Missing 'amount_ml' in request body."}), 400
        
        amount_ml = data['amount_ml']
        if not isinstance(amount_ml, int) or amount_ml <= 0:
            return jsonify({"error": "Invalid water amount. Must be a positive integer in ml."}), 400
            
        timestamp_str = data.get('timestamp')
        timestamp = datetime.strptime(timestamp_str, '%Y-%m-%dT%H:%M:%S.%fZ') if timestamp_str else datetime.utcnow()
        
        water_entry = WaterLog(
            user_id=current_user_id,
            amount_ml=amount_ml,
            timestamp=timestamp
        )
        
        db.session.add(water_entry)
        db.session.commit()
        
        return jsonify({
            "message": "Water intake logged successfully",
            "log": water_entry.to_dict()
        }), 201
        
    except ValueError:
        return jsonify({"error": "Invalid timestamp format. Use ISO 8601 (e.g., YYYY-MM-DDTHH:MM:SS.fZ)."}), 400
    except Exception as e:
        db.session.rollback()
        print(f"ERROR in log_water: {e}") 
        return jsonify({"error": "Failed to log water intake due to server error."}), 500

# POST /metrics/log_weight
@metrics_bp.route('/log_weight', methods=['POST'])
@jwt_required()
def log_weight():
    """Logs a body weight entry for the current user."""
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json()
        
        if not data or 'weight_kg' not in data:
            return jsonify({"error": "Missing 'weight_kg' in request body."}), 400
        
        weight_kg = data['weight_kg']
        
        if not (isinstance(weight_kg, (int, float)) and weight_kg > 0):
            return jsonify({"error": "Invalid weight. Must be a positive number in kg."}), 400
            
        date_str = data.get('date', datetime.utcnow().date().isoformat())
        
        try:
            log_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            return jsonify({"error": "Invalid date format. Use YYYY-MM-DD."}), 400
        
        existing_log = WeightLog.query.filter_by(user_id=current_user_id, date=log_date).first()
        
        if existing_log:
            existing_log.weight_kg = weight_kg
            db.session.commit()
            return jsonify({
                "message": "Weight updated successfully for today",
                "log": existing_log.to_dict()
            }), 200
        else:
            weight_entry = WeightLog(
                user_id=current_user_id,
                weight_kg=weight_kg,
                date=log_date
            )
            db.session.add(weight_entry)
            db.session.commit()
            
            return jsonify({
                "message": "Weight logged successfully",
                "log": weight_entry.to_dict()
            }), 201
            
    except Exception as e:
        db.session.rollback()
        print(f"ERROR in log_weight: {e}") 
        return jsonify({"error": "Failed to log weight due to server error."}), 500


# --- NEW GET ENDPOINTS ---

# GET /metrics/summary
@metrics_bp.route('/summary', methods=['GET'])
@jwt_required()
def get_metrics_summary():
    """
    Returns the current day's water intake, latest weight, and PRs.
    Required by Dashboard.jsx.
    """
    current_user_id = get_jwt_identity()
    today = date.today()
    
    # 1. Total Water Intake for Today
    water_intake_today = db.session.query(func.sum(WaterLog.amount_ml)).filter(
        WaterLog.user_id == current_user_id,
        func.date(WaterLog.timestamp) == today
    ).scalar() or 0
    
    # 2. Latest Weight
    latest_weight_entry = WeightLog.query.filter_by(user_id=current_user_id) \
                                        .order_by(WeightLog.date.desc()) \
                                        .first()
    latest_weight = latest_weight_entry.weight_kg if latest_weight_entry else None
    
    # 3. Weight History (Last 7 days)
    last_week = today - timedelta(days=6)
    weight_history = WeightLog.query.filter(
        WeightLog.user_id == current_user_id,
        WeightLog.date >= last_week
    ).order_by(WeightLog.date.asc()).all()

    weight_trend_data = [log.to_dict() for log in weight_history]
    
    # 4. Personal Records (Max weight lifted per exercise by the user)
    personal_records = {}
    
    try:
        pr_query = db.session.query(
            WorkoutExercise.exercise_id, 
            func.max(WorkoutExercise.weight_lifted).label('max_weight'),
            Exercise.name
        ).join(Exercise, WorkoutExercise.exercise_id == Exercise.id) \
         .join(Workout) \
         .filter(Workout.user_id == current_user_id) \
         .filter(WorkoutExercise.weight_lifted.isnot(None)) \
         .group_by(WorkoutExercise.exercise_id, Exercise.name) \
         .order_by(func.max(WorkoutExercise.weight_lifted).desc()) \
         .limit(3) 

        for pr in pr_query.all():
            if pr.max_weight > 0: # Only include PRs with actual weight lifted
                personal_records[pr.name] = {
                    'weight': round(pr.max_weight, 1),
                    'date': 'N/A' # Date lookup is complex, keeping as placeholder for now
                }
    except Exception as e:
        # Catch errors if workout tables are empty or relations are missing
        print(f"Warning: Failed to calculate PRs: {e}")
        personal_records = {}


    # 5. Next Workout (Placeholder logic)
    next_workout_placeholder = {
        'id': 1, 
        'name': 'Full Body HIIT',
    }
    
    return jsonify({
        "waterIntake": water_intake_today,
        "latestWeight": latest_weight,
        "weightHistory": weight_trend_data,
        "personalRecords": personal_records,
        "nextWorkout": next_workout_placeholder
    }), 200