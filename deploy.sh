#!/bin/bash

# Simple deploy script for Docker Compose

echo "Deploying NIRA-X-Guardian..."

# Pull latest changes (assuming git is used)
# git pull origin main

# Build and start services
docker-compose up -d --build

echo "Deployment complete. Services are running."
