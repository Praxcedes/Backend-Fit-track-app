# app.py
import os
import sys

# Add the current directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

from flask import Flask, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate

# Import from current directory
from config import Config
from models import db
from routes.auth import auth_bp
from routes.exercises import exercises_bp
from routes.workouts import workouts_bp
from routes.profile import profile_bp
from routes.analytics import analytics_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    migrate = Migrate(app, db)
    JWTManager(app)
    CORS(app, origins=["http://localhost:5173"])

    # Default route
    @app.route("/")
    def index():
        return jsonify({
            "message": "Welcome to the Fitness API!!",
            "status": "success",
        })

    # Register Blueprints
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(exercises_bp, url_prefix='/exercises')
    app.register_blueprint(workouts_bp, url_prefix='/workouts')
    app.register_blueprint(profile_bp, url_prefix='/profile')
    app.register_blueprint(analytics_bp, url_prefix='/analytics')

    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True, port=5555)