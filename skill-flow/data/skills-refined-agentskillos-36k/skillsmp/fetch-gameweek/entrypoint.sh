#!/bin/bash
set -e

# Extract gameweek number from arguments
GAMEWEEK=""
PARTIAL=""

while [[ $# -gt 0 ]]; do
    case $1 in
        -g|--gameweek)
            GAMEWEEK="$2"
            shift 2
            ;;
        -p|--partial)
            PARTIAL="--partial"
            shift
            ;;
        *)
            # If it's just a number, treat it as gameweek
            if [[ "$1" =~ ^[0-9]+$ ]]; then
                GAMEWEEK="$1"
            fi
            shift
            ;;
    esac
done

# Default to prompting if no gameweek specified
if [ -z "$GAMEWEEK" ]; then
    echo "Usage: fetch-gameweek <gameweek_number> [--partial]"
    echo "Example: fetch-gameweek 22"
    exit 1
fi

echo "==================================================================="
echo "  🎯 FETCHING GAMEWEEK $GAMEWEEK DATA"
echo "==================================================================="
echo

# Step 1: Fetch gameweek data
echo "📥 Step 1: Fetching data from FPL API..."
python3 fetch_gameweek.py --gameweek "$GAMEWEEK" $PARTIAL

# Step 2: Start local server
echo
echo "==================================================================="
echo "  ✅ FETCH COMPLETE - STARTING LOCAL SERVER"
echo "==================================================================="
echo
echo "🌐 Starting local server at http://localhost:8000"
echo "📊 Navigate to GW${GAMEWEEK} in the dashboard to verify"
echo
echo "⚠️  IMPORTANT: Verify the data looks correct before deploying!"
echo "    Use 'deploy-gameweek ${GAMEWEEK}' skill when ready to deploy"
echo

# Kill any existing server on port 8000
lsof -ti:8000 | xargs kill -9 2>/dev/null || true

# Start server in background
python3 serve_dashboard.py &
SERVER_PID=$!

echo "✓ Server started (PID: $SERVER_PID)"
echo "✓ Dashboard: http://localhost:8000"
echo
echo "Press Ctrl+C to stop the server when done verifying"

# Keep script running so user can verify
wait $SERVER_PID
