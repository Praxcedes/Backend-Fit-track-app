import os
import sys
from flask import Flask, jsonify

def import_safe_classes():
    from flask_cors import CORS
    from flask_jwt_extended import JWTManager
    from flask_migrate import Migrate
    from flask_sqlalchemy import SQLAlchemy
    return CORS, JWTManager, Migrate, SQLAlchemy

current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

from config import Config
from models import db
from routes.auth import auth_bp
from routes.exercises import exercises_bp
from routes.workouts import workouts_bp
from routes.profile import profile_bp
from routes.analytics import analytics_bp
from routes.metrics import metrics_bp

migrate = None
jwt = None
CORS_class = None

def create_app(config_class=Config):
    global migrate, jwt, CORS_class 
    CORS_class, JWTManager_class, Migrate_class, SQLAlchemy_class = import_safe_classes()
    
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    
    Migrate_class(app, db) 
    JWTManager_class(app) 
    
    CORS_class(app, 
         resources={
             r"/*": {
                 "origins": app.config['CORS_ORIGINS'],
                 "supports_credentials": True,
                 "allow_headers": ["Content-Type", "Authorization", "Access-Control-Allow-Credentials"],
                 "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"]
             }
         })

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(exercises_bp, url_prefix='/exercises')
    app.register_blueprint(workouts_bp, url_prefix='/workouts')
    app.register_blueprint(profile_bp, url_prefix='/profile')
    app.register_blueprint(analytics_bp, url_prefix='/analytics')
    app.register_blueprint(metrics_bp, url_prefix='/metrics')

    @app.route("/")
    def index():
        return jsonify({
            "message": "Welcome to the Fitness API!",
            "status": "success",
            "environment": os.environ.get('FLASK_ENV', 'development')
        })

    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True, port=5555)