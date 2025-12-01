import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    db_url = os.environ.get('DATABASE_URL')

    if db_url and db_url.startswith("postgres://"):
        db_url = db_url.replace("postgres://", "postgresql://", 1)
    
    SQLALCHEMY_DATABASE_URI = db_url or \
        'sqlite:///' + os.path.join(basedir, '..', 'instance', 'fittrack.db')
        
    SQLALCHEMY_TRACK_MODIFICATIONS = False
  
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'jwt-secret-key-change-me'
    
    CORS_ORIGINS = [
        "http://localhost:5173", 
        "https://fittrack-0v68.onrender.com",
    ]