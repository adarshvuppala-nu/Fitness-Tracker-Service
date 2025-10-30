"""
Seed script to populate the database with demo data
"""
from datetime import date, timedelta
from app.core.database import SessionLocal
from app.models.user import User
from app.models.workout import Workout
from app.models.goal import Goal


def seed_database():
    """Populate database with demo data"""
    db = SessionLocal()

    try:
        # Check if data already exists
        existing_users = db.query(User).count()
        if existing_users > 0:
            print(f"✓ Database already has {existing_users} users - skipping seed")
            return

        print("📊 Seeding database with demo data...")

        # Create demo users
        users_data = [
            {"username": "john_doe", "email": "john@example.com"},
            {"username": "jane_smith", "email": "jane@example.com"},
            {"username": "mike_wilson", "email": "mike@example.com"},
        ]

        users = []
        for user_data in users_data:
            user = User(**user_data)
            db.add(user)
            users.append(user)

        db.commit()
        print(f"✓ Created {len(users)} users")

        # Create demo workouts for each user
        workout_types = ["running", "cycling", "swimming", "strength_training", "yoga"]
        workouts_created = 0

        for user in users:
            # Create 10-15 workouts per user over the last 30 days
            num_workouts = 12
            for i in range(num_workouts):
                workout_date = date.today() - timedelta(days=i * 2)
                workout_type = workout_types[i % len(workout_types)]

                workout = Workout(
                    user_id=user.id,
                    type=workout_type,
                    duration=30 + (i * 5),  # 30-80 minutes
                    calories_burned=200 + (i * 30),  # 200-530 calories
                    notes=f"Great {workout_type} session!",
                    date=workout_date,
                )
                db.add(workout)
                workouts_created += 1

        db.commit()
        print(f"✓ Created {workouts_created} workouts")

        # Create demo goals for each user
        goals_created = 0
        goal_types = [
            ("weight_loss", 10, "kg", 90),
            ("workout_frequency", 20, "workouts", 60),
            ("distance_goal", 100, "km", 45),
        ]

        for user in users:
            for goal_type, target, unit, days in goal_types:
                goal = Goal(
                    user_id=user.id,
                    goal_type=goal_type,
                    target_value=target,
                    current_value=target * 0.4,  # 40% progress
                    unit=unit,
                    deadline=date.today() + timedelta(days=days),
                    status="active",
                )
                db.add(goal)
                goals_created += 1

        db.commit()
        print(f"✓ Created {goals_created} goals")

        print("✅ Database seeding completed successfully!")

    except Exception as e:
        print(f"❌ Error seeding database: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    print("Starting database seed...")
    seed_database()
    print("Done!")
