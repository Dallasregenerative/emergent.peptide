#!/bin/bash

# Ensure Frontend Stability Script
# This script ensures serve is installed and frontend is built

echo "🔧 Ensuring frontend stability..."

# Install serve if not present
if ! command -v serve &> /dev/null; then
    echo "📦 Installing serve package..."
    npm install -g serve
    echo "✅ Serve installed"
else
    echo "✅ Serve already available"
fi

# Check if build directory exists
if [ ! -d "/app/frontend/build" ]; then
    echo "🏗️ Build directory missing, rebuilding..."
    cd /app/frontend
    yarn build
    echo "✅ Frontend rebuilt"
else
    echo "✅ Build directory exists"
fi

# Ensure proper permissions
chmod -R 755 /app/frontend/build 2>/dev/null || true

echo "🎉 Frontend stability check complete"