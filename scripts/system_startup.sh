#!/bin/bash

# System Startup Script - Ensures all dependencies are installed
echo "🚀 System startup - ensuring all dependencies..."

# Install critical packages
npm install -g serve yarn

# Ensure frontend build exists
cd /app/frontend
if [ ! -d "build" ] || [ -z "$(ls -A build)" ]; then
    echo "🏗️ Building frontend..."
    yarn install --frozen-lockfile
    yarn build
fi

# Install backend dependencies
cd /app/backend
pip install -r requirements.txt

echo "✅ System startup complete - all dependencies ready"