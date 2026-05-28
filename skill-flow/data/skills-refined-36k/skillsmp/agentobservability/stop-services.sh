#!/bin/bash
# Stop Agent Observability Services

set -e

echo "🛑 Stopping Agent Observability Services..."

# Stop server
if pgrep -f "bun.*server.*dev" > /dev/null 2>&1; then
    pkill -f "bun.*server.*dev"
    echo "✅ Server stopped"
else
    echo "⚠️  Server was not running"
fi

# Stop client
if pgrep -f "bun.*client.*dev" > /dev/null 2>&1; then
    pkill -f "bun.*client.*dev"
    echo "✅ Client stopped"
else
    echo "⚠️  Client was not running"
fi

echo "✨ All services stopped"
