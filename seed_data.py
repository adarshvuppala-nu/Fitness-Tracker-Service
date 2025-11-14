"""
Seed script to populate the database with rich sample fitness data
"""
import sys
from datetime import datetime, timedelta, date
import random
from sqlalchemy.orm import Session
from app.core.database import SessionLocal, engine
from app.models.base import Base
from app.models.user import User
from app.models.workout import Workout
from app.models.goal import Goal

# Create all tables
print("Creating database tables...")
Base.metadata.create_all(bind=engine)
print("✓ Tables created successfully!")

# Sample data
USERS = [
    {"username": "alex_runner", "email": "alex@fitness.com"},
    {"username": "sarah_lifter", "email": "sarah@fitness.com"},
    {"username": "mike_cyclist", "email": "mike@fitness.com"},
    {"username": "emma_yoga", "email": "emma@fitness.com"},
    {"username": "david_swimmer", "email": "david@fitness.com"},
    {"username": "lisa_crossfit", "email": "lisa@fitness.com"},
]

WORKOUT_TYPES = ["Running", "Cycling", "Swimming", "Weightlifting", "Yoga", "HIIT", "CrossFit", "Walking", "Rowing", "Boxing"]
GOAL_TYPES = ["Weight Loss", "Muscle Gain", "Endurance", "Strength", "Flexibility", "General Fitness"]

def create_users(db: Session):
    """Create sample users"""
    print("\nCreating users...")
    users = []
    for user_data in USERS:
        user = User(**user_data)
        db.add(user)
        users.append(user)
    db.commit()
    print(f"✓ Created {len(users)} users")
    return users

def create_workouts(db: Session, users: list):
    """Create sample workouts for the past 30 days"""
    print("\nCreating workouts...")
    total_workouts = 0

    for user in users:
        # Create 15-25 workouts per user over the past 30 days
        num_workouts = random.randint(15, 25)

        for i in range(num_workouts):
            days_ago = random.randint(0, 30)
            workout_date = date.today() - timedelta(days=days_ago)

            workout_type = random.choice(WORKOUT_TYPES)
            duration = random.randint(20, 120)  # 20-120 minutes
            calories = round(duration * random.uniform(5, 12))

            notes_options = [
                f"Great {workout_type.lower()} session!",
                f"Felt strong during {workout_type.lower()}",
                f"Personal best in {workout_type.lower()}!",
                f"Challenging {workout_type.lower()} workout",
                "Feeling energized",
                "Good progress today",
                None
            ]

            workout = Workout(
                user_id=user.id,
                type=workout_type,
                duration=duration,
                calories_burned=calories,
                notes=random.choice(notes_options),
                date=workout_date
            )
            db.add(workout)
            total_workouts += 1

    db.commit()
    print(f"✓ Created {total_workouts} workouts")

def create_goals(db: Session, users: list):
    """Create fitness goals for users"""
    print("\nCreating fitness goals...")
    total_goals = 0

    for user in users:
        num_goals = random.randint(2, 4)

        for i in range(num_goals):
            goal_type = random.choice(GOAL_TYPES)
            created_days_ago = random.randint(30, 90)
            target_days = random.randint(30, 180)
            deadline = date.today() + timedelta(days=target_days)
            status = random.choice(["active", "active", "active", "completed", "in_progress"])

            if goal_type == "Weight Loss":
                target_value = random.uniform(5, 15)
                unit = "kg"
            elif goal_type == "Muscle Gain":
                target_value = random.uniform(3, 10)
                unit = "kg"
            elif goal_type == "Endurance":
                target_value = random.randint(50, 100)
                unit = "km"
            elif goal_type == "Strength":
                target_value = random.randint(50, 100)
                unit = "%"
            else:
                target_value = random.randint(20, 50)
                unit = "sessions"

            if status == "completed":
                current_value = target_value
            elif status == "in_progress":
                current_value = target_value * random.uniform(0.3, 0.8)
            else:
                current_value = target_value * random.uniform(0.1, 0.5)

            goal = Goal(
                user_id=user.id,
                goal_type=goal_type,
                target_value=target_value,
                current_value=round(current_value, 2),
                unit=unit,
                deadline=deadline,
                status=status
            )
            db.add(goal)
            total_goals += 1

    db.commit()
    print(f"✓ Created {total_goals} goals")

def main():
    """Main function to seed the database"""
    print("=" * 50)
    print("FITNESS TRACKER - DATABASE SEEDING")
    print("=" * 50)

    db = SessionLocal()

    try:
        users = create_users(db)
        create_workouts(db, users)
        create_goals(db, users)

        print("\n" + "=" * 50)
        print("✓ DATABASE SEEDING COMPLETED SUCCESSFULLY!")
        print("=" * 50)
        print(f"\nSummary:")
        print(f"  • Users: {len(users)}")
        print(f"  • Workouts: ~{len(users) * 20} workouts")
        print(f"  • Goals: ~{len(users) * 3} goals")
        print(f"\nYour fitness tracker is now ready with sample data!")

    except Exception as e:
        print(f"\n❌ Error during seeding: {e}")
        db.rollback()
        sys.exit(1)
    finally:
        db.close()

if __name__ == "__main__":
    main()
