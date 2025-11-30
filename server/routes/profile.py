# server/routes/profile.py

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash 
import traceback # Import traceback for detailed error logging

# Import models
from models import db, User 

profile_bp = Blueprint('profile', __name__)

# ----------------------------------------------------------------------
# GET /profile (Fetch current user data)
# ----------------------------------------------------------------------
@profile_bp.route('/', methods=['GET'])
@jwt_required()
def get_profile():
    """Returns the current user's profile information."""
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        if not user:
            return jsonify({"error": "User not found"}), 404
        
        # CORRECTED: Use user.to_dict() which now includes the email field
        user_data = user.to_dict()
        
        return jsonify({"user": user_data}), 200
    
    except Exception as e:
        print(f"Error fetching profile: {e}")
        return jsonify({"error": "Server error fetching profile data"}), 500

# ----------------------------------------------------------------------
# PUT /profile (Update Profile Details)
# ----------------------------------------------------------------------
@profile_bp.route('/', methods=['PUT'])
@jwt_required()
def update_profile():
    """Allows authenticated user to update their username or email."""
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        data = request.get_json()

        # --- DEBUGGING START ---
        print(f"DEBUG: Profile update attempt for User ID: {current_user_id}. Data received: {data}")
        # --- DEBUGGING END ---

        if not user:
            return jsonify({"error": "User not found"}), 404
        if not data:
            return jsonify({"error": "No data provided"}), 400

        # Update Username
        new_username = data.get('username')
        if new_username and new_username != user.username:
            if User.query.filter(User.username == new_username).first():
                return jsonify({"error": "Username is already taken"}), 409
            user.username = new_username

        # Update Email (using the now-existing 'email' column)
        new_email = data.get('email')
        if new_email and new_email != user.email:
             if User.query.filter(User.email == new_email).first():
                 return jsonify({"error": "Email is already in use"}), 409
             user.email = new_email
        
        db.session.commit()

        # Return updated user data (which now correctly includes the email)
        return jsonify({
            "message": "Profile updated successfully",
            "user": user.to_dict()
        }), 200

    except Exception as e:
        db.session.rollback()
        # --- CRITICAL DEBUGGING ---
        print("\n--- TRACEBACK START: update_profile FAILED ---")
        traceback.print_exc()
        print(f"CRITICAL ERROR updating profile: {e}")
        print("--- TRACEBACK END ---")
        # --- CRITICAL DEBUGGING ---
        return jsonify({"error": "Server error updating profile. See console for details."}), 500

# ----------------------------------------------------------------------
# PUT /profile/password (Change Password)
# ----------------------------------------------------------------------
@profile_bp.route('/password', methods=['PUT'])
@jwt_required()
def change_password():
    """Allows authenticated user to change their password."""
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        data = request.get_json()

        if not user:
            return jsonify({"error": "User not found"}), 404
        
        current_password = data.get('current_password')
        new_password = data.get('new_password')

        if not current_password or not new_password:
            return jsonify({"error": "Missing current or new password"}), 400
        
        # CORRECTION 1: Use the check_password() method from the User model
        if not user.check_password(current_password):
            return jsonify({"error": "Incorrect current password"}), 401

        # CORRECTION 2: Simply set the new password. The @password.setter in models.py 
        # automatically handles hashing (generate_password_hash).
        user.password = new_password
        db.session.commit()

        return jsonify({"message": "Password updated successfully"}), 200

    except Exception as e:
        db.session.rollback()
        print("\n--- TRACEBACK START: change_password FAILED ---")
        traceback.print_exc()
        print(f"Error changing password: {e}")
        print("--- TRACEBACK END ---")
        return jsonify({"error": "Failed to change password due to server error."}), 500