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
from app.models.workout import WorkoutSession
from app.models.goal import FitnessGoal
from app.models.progress import ProgressMetric

# Create all tables
print("Creating database tables...")
Base.metadata.create_all(bind=engine)
print("✓ Tables created successfully!")

# Sample data
USERS = [
    {"username": "alex_runner", "email": "alex@fitness.com", "full_name": "Alex Johnson", "age": 28, "weight": 75.5, "height": 175, "gender": "male"},
    {"username": "sarah_lifter", "email": "sarah@fitness.com", "full_name": "Sarah Williams", "age": 32, "weight": 65.0, "height": 168, "gender": "female"},
    {"username": "mike_cyclist", "email": "mike@fitness.com", "full_name": "Mike Chen", "age": 35, "weight": 82.0, "height": 180, "gender": "male"},
    {"username": "emma_yoga", "email": "emma@fitness.com", "full_name": "Emma Davis", "age": 26, "weight": 58.5, "height": 165, "gender": "female"},
    {"username": "david_swimmer", "email": "david@fitness.com", "full_name": "David Brown", "age": 30, "weight": 78.0, "height": 178, "gender": "male"},
    {"username": "lisa_crossfit", "email": "lisa@fitness.com", "full_name": "Lisa Martinez", "age": 29, "weight": 62.0, "height": 170, "gender": "female"},
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
            workout_date = datetime.now() - timedelta(days=days_ago)

            workout_type = random.choice(WORKOUT_TYPES)
            duration = random.randint(20, 120)  # 20-120 minutes
            calories = round(duration * random.uniform(5, 12))
            intensity = random.choice(["low", "moderate", "high"])

            notes_options = [
                f"Great {workout_type.lower()} session!",
                f"Felt strong during {workout_type.lower()}",
                f"Personal best in {workout_type.lower()}!",
                f"Challenging {workout_type.lower()} workout",
                "Feeling energized",
                "Good progress today",
                None
            ]

            workout = WorkoutSession(
                user_id=user.id,
                workout_type=workout_type,
                duration=duration,
                calories_burned=calories,
                intensity=intensity,
                notes=random.choice(notes_options),
                workout_date=workout_date
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
            created_at = datetime.now() - timedelta(days=created_days_ago)
            target_days = random.randint(30, 180)
            target_date = created_at + timedelta(days=target_days)
            status = random.choice(["active", "active", "active", "completed", "abandoned"])

            if goal_type == "Weight Loss":
                target_value = random.uniform(5, 15)
                description = f"Lose {target_value:.1f} kg"
            elif goal_type == "Muscle Gain":
                target_value = random.uniform(3, 10)
                description = f"Gain {target_value:.1f} kg of muscle"
            elif goal_type == "Endurance":
                target_value = random.randint(50, 100)
                description = f"Run {target_value} km total"
            elif goal_type == "Strength":
                target_value = random.randint(50, 100)
                description = f"Increase bench press by {target_value}%"
            else:
                target_value = random.randint(20, 50)
                description = f"Complete {target_value} {goal_type.lower()} sessions"

            if status == "completed":
                current_value = target_value
            elif status == "abandoned":
                current_value = target_value * random.uniform(0.1, 0.4)
            else:
                current_value = target_value * random.uniform(0.3, 0.8)

            goal = FitnessGoal(
                user_id=user.id,
                goal_type=goal_type,
                description=description,
                target_value=target_value,
                current_value=round(current_value, 2),
                target_date=target_date,
                status=status,
                created_at=created_at
            )
            db.add(goal)
            total_goals += 1

    db.commit()
    print(f"✓ Created {total_goals} goals")

def create_progress_metrics(db: Session, users: list):
    """Create progress tracking metrics"""
    print("\nCreating progress metrics...")
    total_metrics = 0

    metric_types = ["weight", "body_fat_percentage", "muscle_mass", "bmi"]

    for user in users:
        for week in range(12):
            days_ago = week * 7
            metric_date = datetime.now() - timedelta(days=days_ago)
            num_metrics = random.randint(1, 2)
            selected_metrics = random.sample(metric_types, num_metrics)

            for metric_type in selected_metrics:
                if metric_type == "weight":
                    base_weight = user.weight
                    trend = -0.3 if week < 8 else -0.1
                    value = base_weight + (trend * week) + random.uniform(-1, 1)
                elif metric_type == "body_fat_percentage":
                    base_bf = 22 if user.gender == "male" else 28
                    value = base_bf - (week * 0.2) + random.uniform(-0.5, 0.5)
                elif metric_type == "muscle_mass":
                    base_muscle = 35 if user.gender == "male" else 25
                    value = base_muscle + (week * 0.1) + random.uniform(-0.3, 0.3)
                else:
                    if user.weight and user.height:
                        height_m = user.height / 100
                        current_weight = user.weight + (trend * week)
                        value = current_weight / (height_m ** 2)
                    else:
                        value = random.uniform(20, 25)

                metric = ProgressMetric(
                    user_id=user.id,
                    metric_type=metric_type,
                    value=round(value, 2),
                    unit="kg" if metric_type in ["weight", "muscle_mass"] else "%" if metric_type == "body_fat_percentage" else "",
                    recorded_date=metric_date,
                    notes=f"Weekly {metric_type.replace('_', ' ')} measurement"
                )
                db.add(metric)
                total_metrics += 1

    db.commit()
    print(f"✓ Created {total_metrics} progress metrics")

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
        create_progress_metrics(db, users)

        print("\n" + "=" * 50)
        print("✓ DATABASE SEEDING COMPLETED SUCCESSFULLY!")
        print("=" * 50)
        print(f"\nSummary:")
        print(f"  • Users: {len(users)}")
        print(f"  • Workouts: ~{len(users) * 20} workouts")
        print(f"  • Goals: ~{len(users) * 3} goals")
        print(f"  • Progress Metrics: ~{len(users) * 24} metrics")
        print(f"\nYour fitness tracker is now ready with sample data!")

    except Exception as e:
        print(f"\n❌ Error during seeding: {e}")
        db.rollback()
        sys.exit(1)
    finally:
        db.close()

if __name__ == "__main__":
    main()
