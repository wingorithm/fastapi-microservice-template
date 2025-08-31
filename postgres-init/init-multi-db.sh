#!/bin/bash
set -e

# This script is executed by the official postgres image when the container
# is first created. It will not run on subsequent starts.

# Create a dedicated user and database for Kong
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" <<-EOSQL
    CREATE USER kong WITH PASSWORD 'kong';
    CREATE DATABASE kong;
    GRANT ALL PRIVILEGES ON DATABASE kong TO kong;
EOSQL

# Create databases for service_a and service_b
# These databases will be owned by the default 'postgres' superuser.
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    CREATE DATABASE microservice;

    \c microservice

    CREATE SCHEMA service_a;
    CREATE SCHEMA service_b;
EOSQL

echo "✅ Databases for kong, service_a, and service_b created."
