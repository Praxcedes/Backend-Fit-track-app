# config.py
import os

# Define the absolute path to the project's base directory
basedir = os.path.abspath(os.path.dirname(__file__))
# Assumes instance folder is next to server folder

class Config:
    # Secret key for session management
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # Database configuration (CRITICAL FIX)
    # This places the fittrack.db inside the 'instance' folder, which is 
    # typically where Flask creates it during app initialization.
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'instance', 'fittrack.db')
        
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # JWT configuration
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'jwt-secret-key-change-me'
    
    # CORS configuration
    CORS_ORIGINS = ["http://localhost:5173"]