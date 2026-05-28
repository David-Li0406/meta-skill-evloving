#!/bin/bash
# ralph-visible.sh - Launch Ralph inside mprocs for visible Pod sessions

MISSION_ID="$1"
PROJECT_ROOT="${PROJECT_ROOT:-$(pwd)}"
SCRIPT_DIR="$(dirname "$0")"

if [[ -z "$MISSION_ID" ]]; then
    echo "Usage: ralph-visible.sh <mission_id>"
    exit 2
fi

# Generate mprocs config
CONFIG_FILE="/tmp/mprocs-${MISSION_ID}.yaml"
cat > "$CONFIG_FILE" << EOF
procs:
  ralph:
    shell: "sleep 1 && ${SCRIPT_DIR}/ralph.sh ${MISSION_ID} --visible-internal"
    autostart: true
EOF

# Launch mprocs with ctl server enabled
exec mprocs -c "$CONFIG_FILE" --server 127.0.0.1:4050
