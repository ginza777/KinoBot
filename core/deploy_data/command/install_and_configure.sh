#!/bin/bash

# Read environment variables from .env file
cd ..
cd ..
while IFS='=' read -r key value; do
    if [[ ! -z "$key" && ! -z "${value}" ]]; then
        export "$key"="$value"
    fi
done < .env

# Install necessary packages
sudo apt update
sudo apt install -y python3-venv python3-dev libpq-dev postgresql postgresql-contrib nginx curl

# Install Python package installer
sudo apt install -y python3-pip

# Install django-environ
pip3 install django-environ

# Switch to the postgres user and configure the database
sudo -u postgres psql <<EOF
CREATE DATABASE $DB_NAME;
CREATE USER $DB_USER WITH PASSWORD '$DB_PASSWORD';
ALTER USER $DB_USER WITH PASSWORD '$DB_PASSWORD';
ALTER ROLE $DB_USER SET client_encoding TO 'utf8';
ALTER ROLE $DB_USER SET default_transaction_isolation TO 'read committed';
ALTER ROLE $DB_USER SET timezone TO 'UTC';
GRANT CREATE ON SCHEMA public TO $DB_USER;
GRANT ALL PRIVILEGES ON DATABASE $DB_NAME TO $DB_USER;
\q
EOF

# Enable Nginx to start on boot
sudo systemctl enable nginx

# Start Nginx
sudo systemctl start nginx

# Check the status of Nginx
sudo systemctl status nginx

# Reload the systemd daemon
sudo systemctl daemon-reload

# Test Nginx configuration
sudo nginx -t

# Restart Nginx
sudo systemctl restart nginx
