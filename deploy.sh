#!/bin/bash

# Deployment script for Site-AIDN on VPS
# Usage: ./deploy.sh

set -e

echo "=== Déploiement Site-AIDN ==="

# Pull latest changes (if using git)
if [ -d ".git" ]; then
    echo "Pulling latest changes..."
    git pull origin main
fi

# Stop existing containers
echo "Stopping existing containers..."
docker-compose down || true

# Build and start containers
echo "Building and starting containers..."
docker-compose up -d --build

# Wait for database to be ready
echo "Waiting for database..."
sleep 10

# Run migrations
echo "Running migrations..."
docker-compose exec -T web python manage.py migrate --noinput

# Collect static files
echo "Collecting static files..."
docker-compose exec -T web python manage.py collectstatic --noinput

# Show status
echo "=== Deployment complete ==="
docker-compose ps

echo ""
echo "Application accessible at: http://YOUR_DOMAIN_OR_IP"
