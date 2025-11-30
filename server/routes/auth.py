from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from datetime import timedelta

# Use absolute imports
from models import db, User
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

        if User.query.filter_by(username=data['username']).first():
            return jsonify({"error": "Username already exists"}), 400

        hashed_pw = generate_password_hash(data['password'])
        user = User(username=data['username'], password=hashed_pw)
        db.session.add(user)
        db.session.commit()

        access_token = create_access_token(identity=user.id, expires_delta=timedelta(days=1))
        return jsonify({
            "message": "User created successfully", 
            "access_token": access_token, 
            "user": user.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
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

        user = User.query.filter_by(username=data['username']).first()
        if not user or not check_password_hash(user.password, data['password']):
            return jsonify({"error": "Invalid credentials"}), 401

        access_token = create_access_token(identity=user.id, expires_delta=timedelta(days=1))
        return jsonify({
            "message": "Login successful", 
            "access_token": access_token, 
            "user": user.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@auth_bp.route('/check_session', methods=['GET'])
@jwt_required()
def check_session():
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        if not user:
            return jsonify({"error": "User not found"}), 404
            
        return jsonify({
            "message": "Session active", 
            "user": user.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500