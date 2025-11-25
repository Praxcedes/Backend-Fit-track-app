from app import app
from models import db, User, Workout, Exercise, WorkoutItem
from datetime import date

with app.app_context():
    db.drop_all()
    db.create_all()

    # Users
    user1 = User(username="john_doe", password="password123")
    user2 = User(username="jane_smith", password="securepass")
    db.session.add_all([user1, user2])
    db.session.commit()

    # Exercises
    bench_press = Exercise(name="Bench Press", muscle_group="Chest", equipment="Barbell")
    squat = Exercise(name="Squat", muscle_group="Legs", equipment="Barbell")
    pull_up = Exercise(name="Pull Up", muscle_group="Back", equipment="Bodyweight")
    db.session.add_all([bench_press, squat, pull_up])
    db.session.commit()

    # Workouts
    workout1 = Workout(name="Monday Workout", date=date.today(), duration=60, user_id=user1.id)
    workout2 = Workout(name="Leg Day", date=date.today(), duration=45, user_id=user2.id)
    db.session.add_all([workout1, workout2])
    db.session.commit()

    # WorkoutItems
    wi1 = WorkoutItem(workout_id=workout1.id, exercise_id=bench_press.id, sets=3, reps=10, weight_lifted=80.0)
    wi2 = WorkoutItem(workout_id=workout2.id, exercise_id=squat.id, sets=4, reps=8, weight_lifted=100.0)
    wi3 = WorkoutItem(workout_id=workout1.id, exercise_id=pull_up.id, sets=3, reps=12, weight_lifted=0.0)
    db.session.add_all([wi1, wi2, wi3])
    db.session.commit()

    print("Database seeded successfully!")
