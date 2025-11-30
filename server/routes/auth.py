from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from datetime import timedelta
import traceback

# Use absolute imports
from models import db, User
# Note: Assuming you have a validators.py file or these imports won't work
from validators import validate_user_signup, validate_user_login 

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/signup', methods=['POST'])
def signup():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400
            
        errors = validate_user_signup(data)
        if errors:
            return jsonify({"errors": errors}), 400

        # Note: Since User model setter handles hashing, 
        # we can just pass the plain password to the user constructor
        if User.query.filter_by(username=data['username']).first():
            return jsonify({"error": "Username already exists"}), 400

        # We set the password, and the model's setter hashes it automatically
        user = User(username=data['username'], password=data['password']) 
        db.session.add(user)
        db.session.commit()

        access_token = create_access_token(identity=str(user.id), expires_delta=timedelta(days=1))
        return jsonify({
            "message": "User created successfully", 
            "access_token": access_token, 
            "user": user.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        print(f"Signup exception: {e}")
        return jsonify({"error": str(e)}), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400
            
        errors = validate_user_login(data)
        if errors:
            return jsonify({"errors": errors}), 400

        username = data['username']
        password = data['password']

        user = User.query.filter_by(username=username).first()
        
        # CORRECTED LINE: Use the model's check_password method
        if not user or not user.check_password(password):
            print(f"Login attempt failed for user: {username}")
            return jsonify({"error": "Invalid credentials"}), 401

        access_token = create_access_token(identity=str(user.id), expires_delta=timedelta(days=1))
        return jsonify({
            "message": "Login successful", 
            "access_token": access_token, 
            "user": user.to_dict()
        }), 200
        
    except Exception as e:
        print(f"Login exception: {e}")
        return jsonify({"error": str(e)}), 500

@auth_bp.route('/check_session', methods=['GET'])
@jwt_required()
def check_session():
    try:
        # Debug: Print headers to see what's being sent
        auth_header = request.headers.get('Authorization', '')
        print(f"DEBUG - Authorization header: {auth_header}")
        print(f"DEBUG - All headers: {dict(request.headers)}")
        
        current_user_id = get_jwt_identity()
        print(f"DEBUG - JWT Identity: {current_user_id} (type: {type(current_user_id)})")
        
        # Convert string back to integer for database query
        current_user_id = int(current_user_id)
        print(f"DEBUG - Converted user ID: {current_user_id} (type: {type(current_user_id)})")
        
        user = User.query.get(current_user_id)
        
        if not user:
            print(f"Auth check_session ERROR: Token valid but user ID {current_user_id} not found in DB.")
            return jsonify({"error": "User not found or session invalid"}), 401 
            
        return jsonify({
            "message": "Session active", 
            "user": user.to_dict()
        }), 200
        
    except Exception as e:
        print(f"Auth check_session EXCEPTION: {e}")
        print(traceback.format_exc())
        
        # More specific error handling for JWT issues
        if "revoked" in str(e).lower():
            return jsonify({"error": "Token has been revoked"}), 401
        elif "expired" in str(e).lower():
            return jsonify({"error": "Token has expired"}), 401
        elif "invalid" in str(e).lower():
            return jsonify({"error": "Invalid token"}), 401
        elif "missing" in str(e).lower():
            return jsonify({"error": "Token missing"}), 401
        elif "subject must be a string" in str(e).lower():
            return jsonify({"error": "Invalid token format"}), 401
            
        return jsonify({"error": "Failed to verify session"}), 500

@auth_bp.route('/debug_headers', methods=['GET'])
def debug_headers():
    """Debug endpoint to see what headers are being sent"""
    headers_info = {
        'authorization': request.headers.get('Authorization'),
        'content_type': request.headers.get('Content-Type'),
        'all_headers': dict(request.headers)
    }
    print(f"DEBUG HEADERS: {headers_info}")
    return jsonify(headers_info), 200