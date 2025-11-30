import sys
import os

# Add the parent directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app
from models import db, Exercise

def seed_database():
    """Seed database with unique exercises"""
    app = create_app()
    
    with app.app_context():
        try:
            print("🌱 Starting database seeding...")
            
            # Create tables if they don't exist
            print("🗃️ Ensuring tables exist...")
            db.create_all()
            
            # Define unique exercises with corrected names
            exercises_data = [
                {
                    "name": "Bench Press",
                    "muscle_group": "Chest",
                    "instructions": "Lie on bench, grip barbell slightly wider than shoulder width, lower to chest, press up"
                },
                {
                    "name": "Squat", 
                    "muscle_group": "Legs",
                    "instructions": "Bar on upper back, feet shoulder width, descend until thighs parallel to ground"
                },
                {
                    "name": "Deadlift",
                    "muscle_group": "Back",
                    "instructions": "Bend knees, grip bar, lift with straight back, stand up fully"
                },
                {
                    "name": "Overhead Press",
                    "muscle_group": "Shoulders", 
                    "instructions": "Bar at shoulder level, press overhead until arms fully extended"
                },
                {
                    "name": "Pull-up",
                    "muscle_group": "Back",
                    "instructions": "Grip bar wider than shoulders, pull body up until chin over bar"
                },
                {
                    "name": "Push-up",
                    "muscle_group": "Chest",
                    "instructions": "Plank position, hands under shoulders, lower chest to floor, push back up"
                },
                {
                    "name": "Bicep Curl",
                    "muscle_group": "Arms",
                    "instructions": "Stand holding dumbbells, curl weights toward shoulders with palms up"
                },
                {
                    "name": "Tricep Extension",
                    "muscle_group": "Arms", 
                    "instructions": "Grip cable attachment overhead, extend arms downwards until straight"
                },
                {
                    "name": "Lunges",
                    "muscle_group": "Legs",
                    "instructions": "Step forward, lower until both knees bent 90 degrees, return to start"
                },
                {
                    "name": "Plank",
                    "muscle_group": "Core",
                    "instructions": "Forearms and toes on ground, keep body straight, hold position"
                }
            ]
            
            # Check for existing exercises to avoid duplicates
            existing_exercises = {ex.name for ex in Exercise.query.all()}
            new_exercises = []
            
            for exercise_data in exercises_data:
                if exercise_data["name"] not in existing_exercises:
                    exercise = Exercise(**exercise_data)
                    new_exercises.append(exercise)
                    print(f"✅ Adding: {exercise_data['name']}")
                else:
                    print(f"⏩ Skipping (already exists): {exercise_data['name']}")
            
            # Add only new exercises
            if new_exercises:
                db.session.add_all(new_exercises)
                db.session.commit()
                print(f"🎉 Successfully added {len(new_exercises)} new exercises!")
            else:
                print("📝 No new exercises to add - all exercises already exist.")
            
            # Verify final count
            final_count = Exercise.query.count()
            print(f"📊 Total exercises in database: {final_count}")
            
        except Exception as e:
            db.session.rollback()
            print(f"❌ Error seeding database: {e}")
            raise

if __name__ == "__main__":
    seed_database()