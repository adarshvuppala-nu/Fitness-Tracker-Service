#!/bin/bash
set -e

echo "================================================"
echo "Starting Fitness Tracker Monolithic Container"
echo "================================================"

# Set default values for database if not provided
export POSTGRES_USER="${POSTGRES_USER:-fitness_user}"
export POSTGRES_PASSWORD="${POSTGRES_PASSWORD:-fitness_pass_change_me}"
export POSTGRES_DB="${POSTGRES_DB:-fitness_tracker}"
export PGDATA="${PGDATA:-/var/lib/postgresql/data}"

echo "Database Configuration:"
echo "  - User: ${POSTGRES_USER}"
echo "  - Database: ${POSTGRES_DB}"
echo "  - Data Directory: ${PGDATA}"

if [ ! -s "${PGDATA}/PG_VERSION" ]; then
    echo "================================================"
    echo "Initializing PostgreSQL database..."
    echo "================================================"

    # Initialize database cluster as postgres user
    su - postgres -c "/usr/lib/postgresql/15/bin/initdb -D ${PGDATA} -E UTF8"

    # Configure PostgreSQL to listen on all interfaces
    echo "host all all 0.0.0.0/0 md5" >> ${PGDATA}/pg_hba.conf
    echo "listen_addresses='*'" >> ${PGDATA}/postgresql.conf
    echo "port=5432" >> ${PGDATA}/postgresql.conf

    echo "PostgreSQL initialized successfully"
else
    echo "PostgreSQL data directory already exists, skipping initialization"
fi

# Step 2: Start PostgreSQL in the background
echo "================================================"
echo "Starting PostgreSQL server..."
echo "================================================"

su - postgres -c "/usr/lib/postgresql/15/bin/pg_ctl -D ${PGDATA} -l /var/log/postgresql.log start"

# Step 3: Wait for PostgreSQL to be ready
echo "Waiting for PostgreSQL to be ready..."
for i in {1..30}; do
    if su - postgres -c "psql -lqt" &>/dev/null; then
        echo "PostgreSQL is ready!"
        break
    fi
    echo "  Attempt $i/30: PostgreSQL not ready yet..."
    sleep 2
done

# Verify PostgreSQL is running
if ! su - postgres -c "psql -lqt" &>/dev/null; then
    echo "ERROR: PostgreSQL failed to start"
    exit 1
fi

# Step 4: Create database and user if they don't exist
echo "================================================"
echo "Setting up database and user..."
echo "================================================"

su - postgres -c "psql" <<-EOSQL
    -- Create user if not exists
    DO \$\$
    BEGIN
        IF NOT EXISTS (SELECT FROM pg_catalog.pg_roles WHERE rolname = '${POSTGRES_USER}') THEN
            CREATE USER ${POSTGRES_USER} WITH PASSWORD '${POSTGRES_PASSWORD}';
            RAISE NOTICE 'User ${POSTGRES_USER} created';
        ELSE
            RAISE NOTICE 'User ${POSTGRES_USER} already exists';
        END IF;
    END
    \$\$;

    -- Create database if not exists
    SELECT 'CREATE DATABASE ${POSTGRES_DB} OWNER ${POSTGRES_USER}'
    WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = '${POSTGRES_DB}')\gexec

    -- Grant privileges
    GRANT ALL PRIVILEGES ON DATABASE ${POSTGRES_DB} TO ${POSTGRES_USER};

    -- Connect to the database and grant schema privileges
    \c ${POSTGRES_DB}
    GRANT ALL ON SCHEMA public TO ${POSTGRES_USER};
    ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO ${POSTGRES_USER};
    ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO ${POSTGRES_USER};
EOSQL

echo "Database setup completed"

# Step 5: Run Alembic Migrations
echo "================================================"
echo "Running database migrations..."
echo "================================================"

# Set DATABASE_URL for alembic
export DATABASE_URL="postgresql://${POSTGRES_USER}:${POSTGRES_PASSWORD}@localhost:5432/${POSTGRES_DB}"

# Run migrations
if [ -f "alembic.ini" ]; then
    echo "Running Alembic migrations..."
    alembic upgrade head || {
        echo "WARNING: Migration failed, but continuing..."
    }
else
    echo "No alembic.ini found, skipping migrations"
fi

# Step 6: Stop PostgreSQL (supervisord will restart it)
echo "================================================"
echo "Stopping PostgreSQL temporarily..."
echo "================================================"
su - postgres -c "/usr/lib/postgresql/15/bin/pg_ctl -D ${PGDATA} stop"

# Step 7: Hand off to supervisord
echo "================================================"
echo "Handing off to supervisord..."
echo "================================================"
echo "Frontend: http://localhost:8000"
echo "API: http://localhost:8000/api/v1"
echo "API Docs: http://localhost:8000/api/v1/docs"
echo "================================================"

# Execute the CMD (supervisord)
exec "$@"
