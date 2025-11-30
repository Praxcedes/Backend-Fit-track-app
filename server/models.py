from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    
    workouts = db.relationship('Workout', backref='user', lazy=True, cascade='all, delete-orphan')

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username
        }


class Exercise(db.Model):
    __tablename__ = 'exercises'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    muscle_group = db.Column(db.String(50), nullable=False)
    instructions = db.Column(db.Text, nullable=True)
    
    workout_exercises = db.relationship('WorkoutExercise', backref='exercise', lazy=True, cascade='all, delete-orphan')

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "muscle_group": self.muscle_group,
            "instructions": self.instructions
        }


class Workout(db.Model):
    __tablename__ = 'workouts'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    date = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(50), default='completed')
    notes = db.Column(db.Text, nullable=True)
    
    workout_exercises = db.relationship('WorkoutExercise', backref='workout', lazy=True, cascade='all, delete-orphan')

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "name": self.name,
            "date": self.date.isoformat(),
            "status": self.status,
            "notes": self.notes,
            "workout_exercises": [we.to_dict() for we in self.workout_exercises]
        }


class WorkoutExercise(db.Model):
    __tablename__ = 'workout_exercises'
    
    id = db.Column(db.Integer, primary_key=True)
    workout_id = db.Column(db.Integer, db.ForeignKey('workouts.id'), nullable=False)
    exercise_id = db.Column(db.Integer, db.ForeignKey('exercises.id'), nullable=False)
    sets = db.Column(db.Integer, nullable=False)
    reps = db.Column(db.Integer, nullable=False)
    weight_lifted = db.Column(db.Float, nullable=True)

    def to_dict(self):
        return {
            "id": self.id,
            "workout_id": self.workout_id,
            "exercise_id": self.exercise_id,
            "exercise_name": self.exercise.name if self.exercise else None,
            "sets": self.sets,
            "reps": self.reps,
            "weight_lifted": self.weight_lifted
        }