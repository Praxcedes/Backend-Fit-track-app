from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, User
from validators import validate_email, validate_string

profile_bp = Blueprint("profile_bp", __name__)

@profile_bp.get("/")
@jwt_required()
def get_profile():
    user = User.query.get(get_jwt_identity())
    return jsonify({
        "username": user.username,
        "email": user.email
    })

@profile_bp.put("/")
@jwt_required()
def update_profile():
    data = request.json
    user = User.query.get(get_jwt_identity())

    if "email" in data:
        valid, msg = validate_email(data["email"])
        if not valid: return jsonify({"error": msg}), 400
        user.email = data["email"]

    if "username" in data:
        valid, msg = validate_string(data["username"], "Username")
        if not valid: return jsonify({"error": msg}), 400
        user.username = data["username"]

    db.session.commit()

    return jsonify({"message": "Profile updated"})
