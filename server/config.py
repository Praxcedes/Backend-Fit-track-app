# server/config.py
import os

# Define the absolute path to the project's base directory
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    # Secret key for session management
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # --- DATABASE CONFIGURATION (CRITICAL RENDER FIX) ---
    # 1. Get the DATABASE_URL from Render environment
    db_url = os.environ.get('DATABASE_URL')
    
    # 2. Fix the protocol if it starts with 'postgres://' (Render default)
    #    SQLAlchemy requires 'postgresql://'
    if db_url and db_url.startswith("postgres://"):
        db_url = db_url.replace("postgres://", "postgresql://", 1)
    
    # 3. Use the fixed URL, or fallback to local SQLite
    #    Note: Added '..' to match the folder structure (instance is in root, not server)
    SQLALCHEMY_DATABASE_URI = db_url or \
        'sqlite:///' + os.path.join(basedir, '..', 'instance', 'fittrack.db')
        
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # JWT configuration
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'jwt-secret-key-change-me'
    
    # --- CORS CONFIGURATION ---
    # Update this to include your deployed frontend URL later
    # For now, we allow localhost. You can add more to the list.
    CORS_ORIGINS = [
        "http://localhost:5173", 
        # Add your Render Frontend URL here once deployed, e.g.:
        # "https://fittrack-frontend.onrender.com"
    ]