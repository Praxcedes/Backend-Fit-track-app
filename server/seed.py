import sys
import os

# Add the parent directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask
from models import db, Exercise
from config import Config

# Create app instance for seeding
app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

def seed_exercises():
    exercises = [
        {
            "name": "Bench Press",
            "muscle_group": "Chest",
            "equipment": "Barbell",
            "instructions": "Lie on bench, grip barbell slightly wider than shoulder width, lower to chest, press up"
        },
        {
            "name": "Squat",
            "muscle_group": "Legs",
            "equipment": "Barbell",
            "instructions": "Bar on upper back, feet shoulder width, descend until thighs parallel, drive up"
        },
        {
            "name": "Deadlift",
            "muscle_group": "Back",
            "equipment": "Barbell",
            "instructions": "Feet under bar, bend knees, grip bar, lift with straight back until standing"
        },
        {
            "name": "Overhead Press",
            "muscle_group": "Shoulders",
            "equipment": "Barbell",
            "instructions": "Bar at shoulder level, press overhead until arms extended, lower with control"
        },
        {
            "name": "Pull-up",
            "muscle_group": "Back",
            "equipment": "Bodyweight",
            "instructions": "Grip bar wider than shoulders, pull body up until chin over bar, lower with control"
        },
        {
            "name": "Push-up",
            "muscle_group": "Chest",
            "equipment": "Bodyweight",
            "instructions": "Plank position, hands under shoulders, lower chest to floor, push back up"
        },
        {
            "name": "Bicep Curl",
            "muscle_group": "Arms",
            "equipment": "Dumbbell",
            "instructions": "Stand holding dumbbells, curl weights toward shoulders, lower with control"
        },
        {
            "name": "Tricep Extension",
            "muscle_group": "Arms",
            "equipment": "Cable",
            "instructions": "Grip cable attachment overhead, extend arms downward, return to start"
        },
        {
            "name": "Lunges",
            "muscle_group": "Legs",
            "equipment": "Bodyweight",
            "instructions": "Step forward, lower until both knees bent 90 degrees, push back to start"
        },
        {
            "name": "Plank",
            "muscle_group": "Core",
            "equipment": "Bodyweight",
            "instructions": "Forearms and toes on ground, keep body straight, hold position"
        }
    ]
    
    with app.app_context():
        # Clear existing exercises
        Exercise.query.delete()
        
        for exercise_data in exercises:
            exercise = Exercise(**exercise_data)
            db.session.add(exercise)
        
        db.session.commit()
        print(f"✅ Successfully seeded {len(exercises)} exercises!")

if __name__ == "__main__":
    seed_exercises()
    
