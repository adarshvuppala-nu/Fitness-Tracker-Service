#!/bin/bash
set -e

echo "Starting Fitness Tracker application..."

if [ -n "$DATABASE_URL" ]; then
    echo "Database URL configured"

    echo "Waiting for database to be ready..."
    max_retries=30
    retry_count=0

    while [ $retry_count -lt $max_retries ]; do
        if python -c "
import psycopg2
import os
import sys
try:
    conn = psycopg2.connect(os.environ.get('DATABASE_URL'))
    conn.close()
    sys.exit(0)
except Exception as e:
    sys.exit(1)
" 2>/dev/null; then
            echo "Database is ready!"
            break
        fi

        retry_count=$((retry_count + 1))
        echo "Database not ready yet (attempt $retry_count/$max_retries)..."
        sleep 2
    done

    if [ $retry_count -eq $max_retries ]; then
        echo "WARNING: Database connection timeout, but continuing anyway..."
    fi

    echo "Running database migrations..."
    alembic upgrade head || {
        echo "WARNING: Migrations failed, but starting application anyway..."
    }

    echo "Seeding database with demo data..."
    python seed_data.py || {
        echo "WARNING: Seed data failed, but starting application anyway..."
    }
else
    echo "WARNING: DATABASE_URL not set, skipping database setup"
fi

echo "Starting FastAPI application..."
exec uvicorn main:app --host 0.0.0.0 --port 8000 --workers 2
