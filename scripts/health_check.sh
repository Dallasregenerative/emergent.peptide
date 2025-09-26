#!/bin/bash

# Health Check Script - Monitors and auto-fixes common issues
echo "🔍 Running health check..."

# Check if serve is available
if ! command -v serve &> /dev/null; then
    echo "❌ Serve missing - installing..."
    npm install -g serve
fi

# Check if frontend build exists
if [ ! -d "/app/frontend/build" ]; then
    echo "❌ Frontend build missing - rebuilding..."
    cd /app/frontend && yarn build
fi

# Check if services are running
if ! pgrep -f "serve" > /dev/null; then
    echo "❌ Frontend service not running - restarting..."
    sudo supervisorctl restart frontend
fi

if ! pgrep -f "python.*server.py" > /dev/null; then
    echo "❌ Backend service not running - restarting..."
    sudo supervisorctl restart backend
fi

echo "✅ Health check complete"