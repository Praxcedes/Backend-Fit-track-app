from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=True)
    password = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    workouts = db.relationship("Workout", backref="user", lazy="select", cascade="all, delete-orphan")

class Workout(db.Model):
    __tablename__ = "workouts"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    date = db.Column(db.Date, nullable=False)
    duration = db.Column(db.Integer, nullable=True)   # minutes
    notes = db.Column(db.String(1024), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=True)

    workout_items = db.relationship("WorkoutItem", backref="workout", lazy="select", cascade="all, delete-orphan")

class Exercise(db.Model):
    __tablename__ = "exercises"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    muscle_group = db.Column(db.String(50), nullable=True)
    equipment = db.Column(db.String(100), nullable=True)

    workout_items = db.relationship("WorkoutItem", backref="exercise", lazy="select", cascade="all, delete-orphan")

class WorkoutItem(db.Model):
    __tablename__ = "workout_items"
    id = db.Column(db.Integer, primary_key=True)
    workout_id = db.Column(db.Integer, db.ForeignKey("workouts.id"), nullable=False)
    exercise_id = db.Column(db.Integer, db.ForeignKey("exercises.id"), nullable=False)
    sets = db.Column(db.Integer, nullable=False)
    reps = db.Column(db.Integer, nullable=False)
    weight_lifted = db.Column(db.Float, nullable=True)
    duration = db.Column(db.Integer, nullable=True)  # seconds or minutes if used
    notes = db.Column(db.String(512), nullable=True)
    order_index = db.Column(db.Integer, nullable=True)
