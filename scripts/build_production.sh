#!/bin/bash

# Production Build Script for peptideprotocols.ai
# This builds the app with the correct backend URL for the deployed version

echo "🚀 Building production version for peptideprotocols.ai..."

cd /app/frontend

# Backup current .env
cp .env .env.backup

# Copy production environment
cp .env.production .env

# Build for production
echo "🏗️ Building with production backend URL..."
yarn build

# Restore preview environment
mv .env.backup .env

echo "✅ Production build complete with correct backend URL"
echo "📦 Build files are in /app/frontend/build/"
echo "🌐 Ready for deployment to peptideprotocols.ai"