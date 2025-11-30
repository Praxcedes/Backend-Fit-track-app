# server/seed.py (FINAL CORRECTED VERSION)

import sys
import os
from datetime import date, timedelta
from sqlalchemy.exc import OperationalError 

# Add the parent directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import necessary modules and models
from app import create_app
from models import db, User, Exercise, Workout, WorkoutExercise, WaterLog, WeightLog 

# Combining and standardizing the 10 exercises
CORE_EXERCISES = [
    {"name": "Bench Press", "muscle_group": "Chest", "instructions": "Lie on bench, grip barbell slightly wider than shoulder width, lower to chest, press up"},
    {"name": "Squat", "muscle_group": "Legs", "instructions": "Bar on upper back, feet shoulder width, descend until thighs parallel to ground"},
    {"name": "Deadlift", "muscle_group": "Back", "instructions": "Bend knees, grip bar, lift with straight back, stand up fully"},
    {"name": "Overhead Press", "muscle_group": "Shoulders", "instructions": "Bar at shoulder level, press overhead until arms fully extended"},
    {"name": "Pull-up", "muscle_group": "Back", "instructions": "Grip bar wider than shoulders, pull body up until chin over bar"},
    {"name": "Push-up", "muscle_group": "Chest", "instructions": "Plank position, hands under shoulders, lower chest to floor, push back up"},
    {"name": "Bicep Curl", "muscle_group": "Arms", "instructions": "Stand holding dumbbells, curl weights toward shoulders with palms up"},
    {"name": "Tricep Extension", "muscle_group": "Arms", "instructions": "Grip cable attachment overhead, extend arms downwards until straight"},
    {"name": "Lunges", "muscle_group": "Legs", "instructions": "Step forward, lower until both knees bent 90 degrees, return to start"},
    {"name": "Plank", "muscle_group": "Core", "instructions": "Forearms and toes on ground, keep body straight, hold position"}
]


def seed_database():
    """Seed database with users, exercises, workouts, and metrics."""
    app = create_app()
    
    with app.app_context():
        try:
            db.create_all()
        except Exception as e:
            print(f"Warning: db.create_all failed. Assuming tables exist. Error: {e}")
            
        try:
            print("="*40)
            print("🌱 Starting database seeding...")
            
            # --- 1. USER SEEDING ---
            test_user = User.query.filter_by(username="testuser").first()
            
            if not test_user:
                print("👤 Creating user 'testuser'...")
                test_user = User(
                    username="testuser",
                    email="testuser@fittrack.com",
                    password="password123" # Model setter handles hashing
                )
                db.session.add(test_user)
                db.session.commit() # Commit user first to get ID
                print("✅ User created (ID 1).")
            else:
                print("⏩ User 'testuser' already exists.")

            user_id = test_user.id
            
            # --- 2. EXERCISE SEEDING ---
            
            existing_exercises = {ex.name: ex for ex in Exercise.query.all()}
            new_exercises = []
            
            for exercise_data in CORE_EXERCISES: # Use the standardized list
                if exercise_data["name"] not in existing_exercises:
                    exercise = Exercise(**exercise_data)
                    new_exercises.append(exercise)
            
            if new_exercises:
                db.session.add_all(new_exercises)
                db.session.commit()
                print(f"🎉 Successfully added {len(new_exercises)} new exercises!")
            else:
                print("📝 No new exercises added.")
                
            # Re-fetch the map AFTER seeding is complete
            exercises_map = {ex.name: ex.id for ex in Exercise.query.all()}
            print(f"📊 Total exercises in database: {len(exercises_map)}")


            # --- 3. WORKOUT SEEDING (Only proceed if essential exercises exist for mapping) ---
            
            if all(ex_name in exercises_map for ex_name in ['Bench Press', 'Overhead Press', 'Plank']):
                
                if Workout.query.filter_by(user_id=user_id).count() < 3:
                    print("🏋️ Seeding sample workout history...")

                    today = date.today()
                    
                    # Workout 1: Completed Strength Workout (Yesterday)
                    workout_1 = Workout(
                        user_id=user_id,
                        name="Upper Body Power",
                        date=today - timedelta(days=1),
                        status='completed'
                    )
                    db.session.add(workout_1)
                    db.session.flush()

                    # Mapping Workout Exercises using the guaranteed map
                    we1_1 = WorkoutExercise(workout_id=workout_1.id, exercise_id=exercises_map['Bench Press'], sets=3, reps=10, weight_lifted=70)
                    we1_2 = WorkoutExercise(workout_id=workout_1.id, exercise_id=exercises_map['Overhead Press'], sets=3, reps=8, weight_lifted=30)
                    
                    db.session.add_all([we1_1, we1_2])

                    # Workout 2: Core Workout (2 Days Ago)
                    workout_2 = Workout(
                        user_id=user_id,
                        name="Core & Cardio Burn",
                        date=today - timedelta(days=2),
                        status='quit'
                    )
                    db.session.add(workout_2)
                    db.session.flush()

                    we2_1 = WorkoutExercise(workout_id=workout_2.id, exercise_id=exercises_map['Plank'], sets=2, reps=0, weight_lifted=0)
                    
                    db.session.add(we2_1)
                    
                    db.session.commit()
                    print(f"✅ Added 2 sample workouts for testuser.")
                else:
                    print("⏩ Sample workouts already exist.")
            else:
                 print("⚠️ Skipping workout seeding: Required exercises (Bench Press, OHP, Plank) not found in map.")


            # --- 4. METRIC SEEDING (Water and Weight) ---
            
            # Water Log (ensure today's intake for dashboard)
            if not WaterLog.query.filter(db.func.date(WaterLog.timestamp) == date.today()).first():
                print("💧 Seeding today's water log (1000ml)...")
                water_log = WaterLog(user_id=user_id, amount_ml=1000)
                db.session.add(water_log)
            else:
                print("⏩ Today's water log already exists.")
                
            # Weight Log (ensure latest weight for trend)
            if WeightLog.query.filter_by(user_id=user_id).count() < 1:
                print("⚖️ Seeding initial weight log (75.0 kg)...")
                weight_log = WeightLog(user_id=user_id, weight_kg=75.0, date=date.today())
                db.session.add(weight_log)
            else:
                print("⏩ Weight log already exists.")

            db.session.commit()
            print("="*40)
            print("🚀 Database seeding complete! You can log in with: testuser / password123")
            print("="*40)
            
        except Exception as e:
            db.session.rollback()
            print(f"❌ Error seeding database: {e}")
            raise # Re-raise to show the complete Python traceback if it crashes


if __name__ == "__main__":
    seed_database()