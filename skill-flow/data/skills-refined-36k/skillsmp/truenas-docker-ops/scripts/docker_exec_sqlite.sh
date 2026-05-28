#!/bin/bash
# Execute SQLite queries inside a Docker container on TrueNAS server
# Usage: docker_exec_sqlite.sh <container_name> <db_path> <sql_query>
# Environment: CONTAINER_PYTHON - path to python interpreter (default: /app/.venv/bin/python)

set -euo pipefail

if [ $# -ne 3 ]; then
    echo "Usage: $0 <container_name> <db_path> <sql_query>" >&2
    echo "Example: $0 anypod /data/db/anypod.db 'SELECT * FROM feed;'" >&2
    echo "Set CONTAINER_PYTHON to override interpreter (default: /app/.venv/bin/python)" >&2
    exit 1
fi

CONTAINER_NAME="$1"
DB_PATH="$2"
SQL_QUERY="$3"
PYTHON_BIN="${CONTAINER_PYTHON:-/app/.venv/bin/python}"

# Base64 encode inputs to avoid all quoting issues
# Use tr -d '\n' because Linux coreutils base64 wraps at 76 chars
DB_PATH_B64=$(printf '%s' "$DB_PATH" | base64 | tr -d '\n')
SQL_QUERY_B64=$(printf '%s' "$SQL_QUERY" | base64 | tr -d '\n')

# Execute SQLite query in container via Python (since sqlite3 CLI may not be available)
PYTHON_CODE=$(cat <<'EOF'
import sqlite3, json, sys, base64

db_path = base64.b64decode(sys.argv[1]).decode()
sql_query = base64.b64decode(sys.argv[2]).decode()

try:
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    result = conn.execute(sql_query).fetchall()
    if result:
        for row in result:
            print(json.dumps(dict(row)))
    conn.close()
except Exception as e:
    print(f"Error: {e}", file=sys.stderr)
    sys.exit(1)
EOF
)

echo "$PYTHON_CODE" | ssh truenas docker exec -i "${CONTAINER_NAME}" "$PYTHON_BIN" - "$DB_PATH_B64" "$SQL_QUERY_B64"
