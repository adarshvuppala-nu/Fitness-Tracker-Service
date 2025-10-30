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
    import sys

    db = SessionLocal()

    try:
        print("Checking database for existing data...")
        existing_users = db.query(User).count()

        if existing_users >= 8:
            print(f"✓ Database already has {existing_users} users - skipping seed")
            db.close()
            return
        elif existing_users > 0:
            print(f"⚠️ Found {existing_users} users, but seeding more for better analytics...")

        print("📊 Seeding database with demo data...")

        users_data = [
            {"username": "john_doe", "email": "john@example.com"},
            {"username": "jane_smith", "email": "jane@example.com"},
            {"username": "mike_wilson", "email": "mike@example.com"},
            {"username": "sarah_johnson", "email": "sarah@example.com"},
            {"username": "alex_martinez", "email": "alex@example.com"},
            {"username": "emily_davis", "email": "emily@example.com"},
            {"username": "david_brown", "email": "david@example.com"},
            {"username": "lisa_anderson", "email": "lisa@example.com"},
        ]

        users = []
        for user_data in users_data:
            # Check if user already exists
            existing = db.query(User).filter(
                (User.username == user_data["username"]) |
                (User.email == user_data["email"])
            ).first()

            if existing:
                print(f"  - User {user_data['username']} already exists, skipping")
                users.append(existing)
            else:
                user = User(**user_data)
                db.add(user)
                users.append(user)
                print(f"  + Created user {user_data['username']}")

        db.commit()
        total_users = db.query(User).count()
        print(f"✓ Total users in database: {total_users}")

        # Create demo workouts for ALL users (including existing ones)
        all_users = db.query(User).all()
        workout_types = ["running", "cycling", "swimming", "strength_training", "yoga"]
        workouts_created = 0

        print(f"\nCreating workouts for {len(all_users)} users...")
        for user in all_users:
            # Check if this user already has workouts
            existing_workouts = db.query(Workout).filter(Workout.user_id == user.id).count()
            if existing_workouts >= 15:
                print(f"  - {user.username} already has {existing_workouts} workouts, skipping")
                continue

            print(f"  + Adding workouts for {user.username}")
            # Create 15-20 workouts per user over the last 60 days (more realistic analytics)
            num_workouts = 18
            for i in range(num_workouts):
                # Spread workouts over 60 days with some gaps (more realistic)
                days_ago = (i * 3) + (i % 2)  # Creates natural gaps
                workout_date = date.today() - timedelta(days=days_ago)
                workout_type = workout_types[i % len(workout_types)]

                # Vary duration and calories for realistic data
                duration = 25 + (i % 8) * 10  # 25-95 minutes
                calories = 150 + (duration * 5) + (i % 10) * 20  # Calories based on duration

                workout = Workout(
                    user_id=user.id,
                    type=workout_type,
                    duration=duration,
                    calories_burned=calories,
                    notes=f"Great {workout_type} session!",
                    date=workout_date,
                )
                db.add(workout)
                workouts_created += 1

        db.commit()
        print(f"✓ Created {workouts_created} workouts")

        goals_created = 0
        goal_types = [
            ("weight_loss", 10, "kg", 90),
            ("workout_frequency", 20, "workouts", 60),
            ("distance_goal", 100, "km", 45),
        ]

        print(f"\nCreating goals for {len(all_users)} users...")
        for user in all_users:
            # Check if this user already has goals
            existing_goals = db.query(Goal).filter(Goal.user_id == user.id).count()
            if existing_goals >= 3:
                print(f"  - {user.username} already has {existing_goals} goals, skipping")
                continue

            print(f"  + Adding goals for {user.username}")
            # Create all 3 goals per user for comprehensive analytics
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
