#!/bin/bash
set -e

# Create database and user
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    CREATE USER weholo WITH PASSWORD 'weholo';
    CREATE DATABASE weholo;
    GRANT ALL PRIVILEGES ON DATABASE weholo TO weholo;
    \c weholo
    GRANT ALL ON SCHEMA public TO weholo;
EOSQL

echo "Database initialization complete"
