#!/bin/bash
# Execute Python code inside a Docker container on TrueNAS server
# Usage: docker_exec_python.sh <container_name> <python_code>
# Environment: CONTAINER_PYTHON - path to python interpreter (default: /app/.venv/bin/python)

set -euo pipefail

if [ $# -ne 2 ]; then
    echo "Usage: $0 <container_name> <python_code>" >&2
    echo "Example: $0 anypod 'import sys; print(sys.version)'" >&2
    echo "Set CONTAINER_PYTHON to override interpreter (default: /app/.venv/bin/python)" >&2
    exit 1
fi

CONTAINER_NAME="$1"
PYTHON_CODE="$2"
PYTHON_BIN="${CONTAINER_PYTHON:-/app/.venv/bin/python}"

# Execute Python code in container via SSH
# Pass Python code through stdin to avoid nested heredoc escaping issues
printf '%s\n' "$PYTHON_CODE" | ssh truenas docker exec -i "${CONTAINER_NAME}" "$PYTHON_BIN" -
