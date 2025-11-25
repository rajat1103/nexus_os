#!/bin/bash

echo "🧹 Cleaning up old Docker junk..."
docker system prune -f

echo "🏗️  Rebuilding NEXUS..."
docker build -t nexus-os .

echo "🚀 Starting System..."
# This is the correct command to launch the container with both ports open
docker run -p 8000:8000 -p 8501:8501 --env-file .env -v $(pwd)/nexus_memory:/app/nexus_memory nexus-os