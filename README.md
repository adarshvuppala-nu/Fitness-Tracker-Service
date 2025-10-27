# Fitness Tracker API

A production-ready REST API service built with FastAPI for tracking workouts, fitness progress, and health goals.

## Tech Stack

- **Framework**: FastAPI 0.115.0
- **Database**: PostgreSQL 16
- **ORM**: SQLAlchemy 2.0.35
- **Migrations**: Alembic 1.13.3
- **Server**: Uvicorn 0.32.0
- **Validation**: Pydantic 2.9.2
- **Container**: Docker (PostgreSQL)

## Features

- Full CRUD operations for Users, Workout Sessions, Fitness Goals, and Progress Metrics
- Professional, descriptive REST API endpoint naming
- Comprehensive data validation with Pydantic
- Database migrations with Alembic
- Automatic API documentation (Swagger UI)
- PostgreSQL with connection pooling
- Production-ready RESTful API design
- UUID-based primary keys
- Timestamp tracking for all entities
- Advanced filtering and pagination support

## Prerequisites

- Python 3.9+
- Docker and Docker Compose
- pip or uv package manager

## Project Structure

```
fitness-tracker-api/
├── main.py                          # Application entrypoint
├── .env.example                     # Environment variables template
├── .env                             # Environment variables (git-ignored)
├── .gitignore                       # Git ignore rules
├── README.md                        # This file
├── requirements.txt                 # Python dependencies
├── docker-compose.yml               # PostgreSQL container config
├── alembic.ini                      # Alembic configuration
├── alembic/
│   ├── env.py                       # Alembic environment
│   └── versions/                    # Migration files
└── app/
    ├── core/
    │   ├── config.py                # Application configuration
    │   └── database.py              # Database session management
    ├── models/
    │   ├── user.py                  # User model
    │   ├── workout.py               # Workout model
    │   ├── goal.py                  # Goal model
    │   └── progress.py              # Progress model
    ├── schemas/
    │   ├── user.py                  # User Pydantic schemas
    │   ├── workout.py               # Workout Pydantic schemas
    │   ├── goal.py                  # Goal Pydantic schemas
    │   └── progress.py              # Progress Pydantic schemas
    ├── crud/
    │   ├── base.py                  # Base CRUD operations
    │   ├── user.py                  # User CRUD
    │   ├── workout.py               # Workout CRUD
    │   ├── goal.py                  # Goal CRUD
    │   └── progress.py              # Progress CRUD
    └── api/
        ├── deps.py                  # API dependencies
        └── v1/
            ├── router.py            # Main API router
            ├── users.py             # User endpoints (/users)
            ├── workouts.py          # Workout session endpoints (/workout-sessions)
            ├── goals.py             # Fitness goal endpoints (/fitness-goals)
            └── progress.py          # Progress metric endpoints (/progress-metrics)
```

## Setup Instructions

### 1. Clone or Navigate to Project Directory

```bash
cd fitness-tracker-api
```

### 2. Create Virtual Environment

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables

```bash
cp .env.example .env
```

The `.env` file contains:
```
DATABASE_URL=postgresql://adarshvuppala:Helloworld+123@localhost:5433/fitness_tracker
DATABASE_HOST=localhost
DATABASE_PORT=5433
DATABASE_NAME=fitness_tracker
DATABASE_USER=adarshvuppala
DATABASE_PASSWORD=Helloworld+123

API_V1_PREFIX=/api/v1
PROJECT_NAME=Fitness Tracker API
VERSION=1.0.0
```

### 5. Start PostgreSQL with Docker

```bash
docker-compose up -d
```

Verify the container is running:
```bash
docker ps
```

### 6. Run Database Migrations

```bash
alembic upgrade head
```

### 7. Start the API Server

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at:
- **API Base URL**: http://localhost:8000
- **Interactive API Docs (Swagger UI)**: http://localhost:8000/docs
- **Alternative API Docs (ReDoc)**: http://localhost:8000/redoc

## Database Schema

### Users Table
- `id`: UUID (primary key)
- `username`: String (unique, indexed)
- `email`: String (unique, indexed)
- `created_at`: DateTime
- `updated_at`: DateTime

### Workouts Table
- `id`: UUID (primary key)
- `user_id`: UUID (foreign key → users.id)
- `type`: String (e.g., "running", "cycling")
- `duration`: Integer (minutes)
- `calories_burned`: Float
- `notes`: Text (optional)
- `date`: Date
- `created_at`: DateTime

### Goals Table
- `id`: UUID (primary key)
- `user_id`: UUID (foreign key → users.id)
- `goal_type`: String (e.g., "weight_loss")
- `target_value`: Float
- `current_value`: Float (default: 0.0)
- `unit`: String (e.g., "kg", "lbs")
- `deadline`: Date
- `status`: String (default: "active")
- `created_at`: DateTime
- `updated_at`: DateTime

### Progress Table
- `id`: UUID (primary key)
- `user_id`: UUID (foreign key → users.id)
- `metric`: String (e.g., "weight")
- `value`: Float
- `unit`: String
- `date`: Date
- `notes`: Text (optional)
- `created_at`: DateTime

## API Endpoints

All endpoints are prefixed with `/api/v1`

### Endpoint Naming Convention

This API follows professional REST API naming conventions:

- **Users** (`/users`) - User account management
- **Workout Sessions** (`/workout-sessions`) - Individual exercise sessions
- **Fitness Goals** (`/fitness-goals`) - Personal fitness objectives and targets
- **Progress Metrics** (`/progress-metrics`) - Body measurements and tracking data

All endpoints use:
- Plural nouns for resource names
- Kebab-case for multi-word resources
- Descriptive names for clarity
- RESTful HTTP methods (GET, POST, PUT, DELETE)

### Users

#### Create User
```
POST /api/v1/users/
Content-Type: application/json

{
  "username": "johndoe",
  "email": "john@example.com"
}
```

#### Get User by ID
```
GET /api/v1/users/{user_id}
```

#### List Users
```
GET /api/v1/users/?skip=0&limit=10
```

#### Update User
```
PUT /api/v1/users/{user_id}
Content-Type: application/json

{
  "username": "newusername",
  "email": "newemail@example.com"
}
```

#### Delete User
```
DELETE /api/v1/users/{user_id}
```

### Workout Sessions

#### Create Workout Session
```
POST /api/v1/workout-sessions/
Content-Type: application/json

{
  "user_id": "uuid-here",
  "type": "running",
  "duration": 30,
  "calories_burned": 250,
  "date": "2025-10-27",
  "notes": "Morning run"
}
```

#### Get Workout Session by ID
```
GET /api/v1/workout-sessions/{workout_id}
```

#### List Workout Sessions
```
GET /api/v1/workout-sessions/?user_id=uuid&date_from=2025-10-01&date_to=2025-10-31&skip=0&limit=10
```

#### Update Workout Session
```
PUT /api/v1/workout-sessions/{workout_id}
Content-Type: application/json

{
  "duration": 45,
  "calories_burned": 300
}
```

#### Delete Workout Session
```
DELETE /api/v1/workout-sessions/{workout_id}
```

### Fitness Goals

#### Create Fitness Goal
```
POST /api/v1/fitness-goals/
Content-Type: application/json

{
  "user_id": "uuid-here",
  "goal_type": "weight_loss",
  "target_value": 75.0,
  "current_value": 85.0,
  "unit": "kg",
  "deadline": "2025-12-31"
}
```

#### Get Fitness Goal by ID
```
GET /api/v1/fitness-goals/{goal_id}
```

#### List Fitness Goals
```
GET /api/v1/fitness-goals/?user_id=uuid&status=active&skip=0&limit=10
```

#### Update Fitness Goal
```
PUT /api/v1/fitness-goals/{goal_id}
Content-Type: application/json

{
  "current_value": 80.0,
  "status": "active"
}
```

#### Delete Fitness Goal
```
DELETE /api/v1/fitness-goals/{goal_id}
```

### Progress Metrics

#### Create Progress Metric
```
POST /api/v1/progress-metrics/
Content-Type: application/json

{
  "user_id": "uuid-here",
  "metric": "weight",
  "value": 82.5,
  "unit": "kg",
  "date": "2025-10-27",
  "notes": "Weekly weigh-in"
}
```

#### Get Progress Metric by ID
```
GET /api/v1/progress-metrics/{progress_id}
```

#### List Progress Metrics
```
GET /api/v1/progress-metrics/?user_id=uuid&metric=weight&date_from=2025-10-01&date_to=2025-10-31&skip=0&limit=10
```

#### Update Progress Metric
```
PUT /api/v1/progress-metrics/{progress_id}
Content-Type: application/json

{
  "value": 82.0,
  "notes": "Updated measurement"
}
```

#### Delete Progress Metric
```
DELETE /api/v1/progress-metrics/{progress_id}
```

## Testing the API

### Using cURL

Create a user:
```bash
curl -X POST "http://localhost:8000/api/v1/users/" \
  -H "Content-Type: application/json" \
  -d '{"username": "testuser", "email": "test@example.com"}'
```

List all users:
```bash
curl "http://localhost:8000/api/v1/users/"
```

### Using Swagger UI

1. Navigate to http://localhost:8000/docs
2. Click on any endpoint to expand it
3. Click "Try it out"
4. Fill in the required parameters
5. Click "Execute"

## Docker Commands

### Start PostgreSQL
```bash
docker-compose up -d
```

### Check Container Status
```bash
docker-compose ps
```

### View Logs
```bash
docker-compose logs postgres
```

### Stop PostgreSQL
```bash
docker-compose down
```

### Stop and Remove Data Volume
```bash
docker-compose down -v
```

## Alembic Commands

### Create New Migration
```bash
alembic revision --autogenerate -m "Description of changes"
```

### Apply Migrations
```bash
alembic upgrade head
```

### Rollback Migration
```bash
alembic downgrade -1
```

### View Migration History
```bash
alembic history
```

## Development Notes

### Adding New Models

1. Create model in `app/models/`
2. Create schemas in `app/schemas/`
3. Create CRUD operations in `app/crud/`
4. Create API endpoints in `app/api/v1/`
5. Include router in `app/api/v1/router.py`
6. Generate migration: `alembic revision --autogenerate -m "Add new model"`
7. Apply migration: `alembic upgrade head`

### Connection Pooling

The database is configured with:
- Pool size: 10 connections
- Max overflow: 20 connections
- Pre-ping enabled for connection health checks

## Troubleshooting

### Port 5432 Already in Use

If you see "port 5432 already in use", PostgreSQL is already running on your system. The Docker container is configured to use port 5433 instead.

### Database Connection Errors

1. Verify PostgreSQL container is running: `docker ps`
2. Check container logs: `docker-compose logs postgres`
3. Verify environment variables in `.env`
4. Test connection: `docker exec -it fitness_tracker_db psql -U adarshvuppala -d fitness_tracker`

### Import Errors

Make sure you're in the project root directory and the virtual environment is activated:
```bash
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows
```

## Production Deployment Checklist

- [ ] Change database credentials
- [ ] Enable HTTPS
- [ ] Configure CORS for specific origins
- [ ] Set up authentication/authorization
- [ ] Enable rate limiting
- [ ] Configure logging
- [ ] Set up monitoring
- [ ] Use production WSGI server (Gunicorn with Uvicorn workers)
- [ ] Set up database backups
- [ ] Configure environment-specific settings

## License

This project is for educational purposes.

## Contributors

Built with FastAPI and PostgreSQL.
