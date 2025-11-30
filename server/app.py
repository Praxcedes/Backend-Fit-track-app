# app.py
import os
import sys

from flask import Flask, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate

# Add the current directory to Python path for relative imports
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

# Import Configuration and Models
from config import Config
from models import db

# Import Blueprints
from routes.auth import auth_bp
from routes.exercises import exercises_bp
from routes.workouts import workouts_bp
from routes.profile import profile_bp
from routes.analytics import analytics_bp
from routes.metrics import metrics_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    Migrate(app, db) # Initialize Migrate
    jwt = JWTManager(app) # Initialize JWTManager

    # Configure CORS
    CORS(app, 
         origins=app.config['CORS_ORIGINS'],
         supports_credentials=True,
         allow_headers=["Content-Type", "Authorization", "Access-Control-Allow-Credentials"],
         methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"])

    # Default route
    @app.route("/")
    def index():
        return jsonify({
            "message": "Welcome to the Fitness API!",
            "status": "success",
        })

    # Register Blueprints
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(exercises_bp, url_prefix='/exercises')
    app.register_blueprint(workouts_bp, url_prefix='/workouts')
    app.register_blueprint(profile_bp, url_prefix='/profile')
    app.register_blueprint(analytics_bp, url_prefix='/analytics')
    app.register_blueprint(metrics_bp, url_prefix='/metrics')

    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True, port=5555)