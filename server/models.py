from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
# NEW IMPORT for secure password handling
from werkzeug.security import generate_password_hash, check_password_hash 

db = SQLAlchemy()

# --- HELPER FUNCTION FOR TEMPORARY FRONTEND IMAGES ---
def get_mock_images(exercise_id):
    """Maps seeded Exercise IDs (1-10) to placeholder image URLs."""
    image_data = {
        1: [
            "https://images.unsplash.com/photo-1581009146145-b5ef050c2e1e?w=800&fit=crop", 
            "https://images.unsplash.com/photo-1548690312-e3b507d8c110?w=600&fit=crop"
        ],
        2: [
            "https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?w=800&fit=crop", 
            "https://images.unsplash.com/photo-1608215543217-2529005fb37c?w=600&fit=crop"
        ],
        3: [
            "https://images.unsplash.com/photo-1534438327276-14e5300c3a48?w=800&fit=crop", 
            "https://images.unsplash.com/photo-1548690312-e3b507d8c110?w=600&fit=crop"
        ],
        4: [
            "https://images.unsplash.com/photo-1548690312-e3b507d8c110?w=800&fit=crop", 
            "https://images.unsplash.com/photo-1518611012118-696072aa579a?w=600&fit=crop"
        ],
        5: [
            "https://images.unsplash.com/photo-1590239926044-29b7351e3a66?w=800&fit=crop", 
            "https://images.unsplash.com/photo-1583454110551-21f2fa2afe61?w=600&fit=crop"
        ],
        6: [
            "https://images.unsplash.com/photo-1599058945522-28d584b6f0ff?w=800&fit=crop", 
            "https://images.unsplash.com/photo-1571019614242-c5c5dee9f50b?w=600&fit=crop"
        ],
        7: [
            "https://images.unsplash.com/photo-1616279967983-ec413476e824?w=800&fit=crop", 
            "https://images.unsplash.com/photo-1517931524326-bdd55a541177?w=600&fit=crop"
        ],
        8: [
            "https://images.unsplash.com/photo-1591741531460-2336d8033346?w=800&fit=crop", 
            "https://images.unsplash.com/photo-1581009146145-b5ef050c2e1e?w=600&fit=crop"
        ],
        9: [
            "https://images.unsplash.com/photo-1601422407692-ec4eeec1d9b3?w=800&fit=crop", 
            "https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?w=600&fit=crop"
        ],
        10: [
            "https://images.unsplash.com/photo-1571019614242-c5c5dee9f50b?w=800&fit=crop", 
            "https://images.unsplash.com/photo-1544367567-0f2fcb009e0b?w=600&fit=crop"
        ],
    }
    return image_data.get(exercise_id, ["https://images.unsplash.com/photo-1548690312-e3b507d8c110?w=800&fit=crop"])

# --- USER MODEL ---
class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    
    # ADDED: Email field for profile updates
    email = db.Column(db.String(120), unique=True, nullable=True) 
    
    # Renamed to _password_hash to indicate it holds the hash, not the plain password
    _password_hash = db.Column(db.String(255), nullable=False)
    
    # Relationships
    workouts = db.relationship('Workout', backref='user', lazy='noload', cascade='all, delete-orphan')
    water_logs = db.relationship('WaterLog', backref='user', lazy='dynamic', cascade='all, delete-orphan') 
    weight_logs = db.relationship('WeightLog', backref='user', lazy='dynamic', cascade='all, delete-orphan') 

    # PROPERTY SETTER for hashing the password automatically
    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self._password_hash = generate_password_hash(password)

    # METHOD to check the password against the stored hash
    def check_password(self, password):
        return check_password_hash(self._password_hash, password)

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email # Included email
        }

# --- METRIC MODELS ---
# ... (WaterLog and WeightLog models remain unchanged) ...

class WaterLog(db.Model):
    __tablename__ = 'water_logs'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    amount_ml = db.Column(db.Integer, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow) 

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "amount_ml": self.amount_ml,
            "timestamp": self.timestamp.isoformat()
        }

class WeightLog(db.Model):
    __tablename__ = 'weight_logs'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    weight_kg = db.Column(db.Float, nullable=False)
    date = db.Column(db.Date, nullable=False, default=datetime.utcnow().date)

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "weight_kg": self.weight_kg,
            "date": self.date.isoformat()
        }

# --- EXERCISE MODEL ---
# ... (Exercise model remains unchanged) ...

class Exercise(db.Model):
    __tablename__ = 'exercises'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    muscle_group = db.Column(db.String(50), nullable=False)
    instructions = db.Column(db.Text, nullable=True)
    
    workout_exercises = db.relationship('WorkoutExercise', backref='exercise', lazy=True, cascade='all, delete-orphan')

    def to_dict(self):
        # TEMPORARY MAPPING LOGIC for 'level' and 'duration'
        if self.muscle_group in ['Strength', 'Legs', 'Shoulders']:
            level = 'Medium'
            duration = '45 min'
        elif self.muscle_group in ['Arms', 'Core']:
            level = 'Low'
            duration = '30 min'
        else:
            level = 'High'
            duration = '55 min'
            
        return {
            "id": self.id,
            # MAPPED FIELDS FOR FRONTEND COMPATIBILITY
            "title": self.name,
            "category": self.muscle_group,
            "level": level,
            "duration": duration,
            "images": get_mock_images(self.id),
            # ORIGINAL FIELDS
            "name": self.name,
            "muscle_group": self.muscle_group,
            "instructions": self.instructions
        }

# --- WORKOUT MODEL ---
# ... (Workout model remains unchanged) ...

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
            "workout_exercises": [we.to_dict() for we in self.workout_exercises if we] 
        }

# --- WORKOUT EXERCISE MODEL ---
# ... (WorkoutExercise model remains unchanged) ...

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
            "exercise_name": self.exercise.name if hasattr(self, 'exercise') and self.exercise else None,
            "sets": self.sets,
            "reps": self.reps,
            "weight_lifted": self.weight_lifted
        }