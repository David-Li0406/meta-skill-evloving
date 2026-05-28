#!/bin/bash
# Start Agent Observability Services
# This script starts both the server and client for the agent observability dashboard

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SERVER_DIR="$SCRIPT_DIR/apps/server"
CLIENT_DIR="$SCRIPT_DIR/apps/client"
LOG_DIR="$SCRIPT_DIR/logs"

# Create logs directory if it doesn't exist
mkdir -p "$LOG_DIR"

echo "🚀 Starting Agent Observability Services..."

# Check if services are already running
if pgrep -f "bun.*server.*dev" > /dev/null 2>&1; then
    echo "⚠️  Server appears to already be running"
else
    echo "📊 Starting observability server..."
    cd "$SERVER_DIR"
    bun install > /dev/null 2>&1
    nohup bun run dev > "$LOG_DIR/server-stdout.log" 2> "$LOG_DIR/server-stderr.log" &
    echo "✅ Server started on http://localhost:4000"
fi

# Give server a moment to start
sleep 2

if pgrep -f "bun.*client.*dev" > /dev/null 2>&1; then
    echo "⚠️  Client appears to already be running"
else
    echo "🎨 Starting observability client..."
    cd "$CLIENT_DIR"
    bun install > /dev/null 2>&1
    nohup bun run dev > "$LOG_DIR/client-stdout.log" 2> "$LOG_DIR/client-stderr.log" &
    echo "✅ Client started on http://localhost:5172"
fi

echo ""
echo "✨ Services are running!"
echo "   📊 Dashboard: http://localhost:5172"
echo "   🔌 Server API: http://localhost:4000"
echo ""
echo "📝 Logs available at: $LOG_DIR"
echo "   Server: tail -f $LOG_DIR/server-stdout.log"
echo "   Client: tail -f $LOG_DIR/client-stdout.log"
