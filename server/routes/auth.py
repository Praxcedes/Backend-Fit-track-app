from flask import Blueprint, request, jsonify
from flask_bcrypt import Bcrypt
from flask_jwt_extended import create_access_token
from models import db, User
from validators import validate_email, validate_password, validate_string

bcrypt = Bcrypt()
auth_bp = Blueprint("auth_bp", __name__)

# ----------- SIGNUP -----------
@auth_bp.post("/signup")
def signup():
    data = request.json

    valid, msg = validate_email(data.get("email"))
    if not valid: return jsonify({"error": msg}), 400

    valid, msg = validate_string(data.get("username"), "Username")
    if not valid: return jsonify({"error": msg}), 400

    valid, msg = validate_password(data.get("password"))
    if not valid: return jsonify({"error": msg}), 400

    hashed = bcrypt.generate_password_hash(data["password"]).decode()
    user = User(username=data["username"], email=data["email"], password_hash=hashed)

    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "User created successfully"}), 201

# ----------- LOGIN -----------
@auth_bp.post("/login")
def login():
    data = request.json
    user = User.query.filter_by(email=data["email"]).first()

    if not user or not bcrypt.check_password_hash(user.password_hash, data["password"]):
        return jsonify({"error": "Invalid credentials"}), 401

    token = create_access_token(identity=user.id)
    return jsonify({"token": token, "user_id": user.id})
