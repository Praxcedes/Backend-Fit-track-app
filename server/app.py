from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_cors import CORS
from .config import Config
from .models import db
from .validators import (
    validate_email,
    validate_password,
    validate_string,
    validate_number
)

# ---------------- APP INITIALIZATION ----------------
app = Flask(__name__)
app.config.from_object(Config)

# Enable CORS for frontend
CORS(app, origins=["http://localhost:3000"])

db.init_app(app)
jwt = JWTManager(app)
migrate = Migrate(app, db)

# ---------------- REGISTER ROUTES ----------------
from .routes.auth import auth_bp
from .routes.workouts import workouts_bp
from .routes.exercises import exercises_bp
from .routes.analytics import analytics_bp
from .routes.profile import profile_bp

app.register_blueprint(auth_bp, url_prefix="/auth")
app.register_blueprint(workouts_bp, url_prefix="/workouts")
app.register_blueprint(exercises_bp, url_prefix="/exercises")
app.register_blueprint(analytics_bp, url_prefix="/analytics")
app.register_blueprint(profile_bp, url_prefix="/profile")

# ---------------- DEFAULT ROUTE ----------------
@app.route("/")
def index():
    return jsonify({
        "service": "FitTrack API",
        "status": "Operational",
        "message": "Your fitness journey starts here.",
        "version": "1.0.0"
    })

# ---------------- ERROR HANDLERS ----------------
@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Resource not found"}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal server error"}), 500

# ---------------- MAIN ENTRY ----------------
if __name__ == "__main__":
    app.run(port=5555, debug=True)