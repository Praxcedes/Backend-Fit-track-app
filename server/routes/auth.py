# routes/auth.py
from flask import Blueprint, request, jsonify
from models import db, User
from werkzeug.security import generate_password_hash, check_password_hash
from app import validate_email, validate_password, validate_string, serialize_user

auth_bp = Blueprint("auth_bp", __name__)

# Register
@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json() or {}
    errors = []

    # Validation
    err = validate_string("Username", data.get("username"))
    if err: errors.append(err)

    err = validate_email(data.get("email"))
    if err: errors.append(err)

    err = validate_password(data.get("password"))
    if err: errors.append(err)

    if errors:
        return jsonify({"errors": errors}), 400

    # Check if username/email exists
    if User.query.filter_by(username=data["username"]).first():
        return jsonify({"error": "Username already exists."}), 400
    if User.query.filter_by(email=data["email"]).first():
        return jsonify({"error": "Email already exists."}), 400

    # Create user
    new_user = User(
        username=data["username"],
        email=data["email"],
        password=generate_password_hash(data["password"])
    )
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User registered successfully", "user": serialize_user(new_user)}), 201


# Login
@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json() or {}
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"error": "Email and password required."}), 400

    user = User.query.filter_by(email=email).first()
    if not user or not check_password_hash(user.password, password):
        return jsonify({"error": "Invalid email or password."}), 401

    # For now, return user info (replace with JWT in production)
    return jsonify({"message": "Login successful", "user": serialize_user(user)}), 200
