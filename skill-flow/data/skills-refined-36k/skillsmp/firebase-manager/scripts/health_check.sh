#!/bin/bash
# Firebase Health Check Script

echo "🔍 Checking Firebase Tools..."
if ! command -v firebase &> /dev/null
then
    echo "❌ firebase-tools not found. Install with: npm install -g firebase-tools"
    exit 1
fi

echo "✅ Firebase Tools installed."

echo "🔍 Checking Firebase Project..."
PROJECT_ID=$(firebase target:list hosting 2>/dev/null | grep -o 'ribh-[a-z0-9-]*' | head -n 1)
if [ -z "$PROJECT_ID" ]; then
    echo "⚠️ No hosting target found. Checking active project..."
    PROJECT_ID=$(firebase project:list | grep 'current' | awk '{print $2}')
fi

if [ -z "$PROJECT_ID" ]; then
    echo "❌ No active Firebase project found. Run: firebase use --add"
else
    echo "✅ Active Project: $PROJECT_ID"
fi

echo "🔍 Checking Functions Status..."
if [ -d "functions" ]; then
    echo "✅ Functions directory exists."
    # Check if node_modules exists
    if [ ! -d "functions/node_modules" ]; then
        echo "⚠️ functions/node_modules missing. Run: cd functions && npm install"
    fi
else
    echo "❌ Functions directory missing!"
fi

echo "✅ Health check complete."
