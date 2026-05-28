#!/bin/zsh
set -euo pipefail

export PATH="/Users/tyler/go/bin:/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin"

# Simple lock to avoid overlapping runs
LOCK_DIR="/tmp/aix-cortex-sync.lock"
if ! mkdir "$LOCK_DIR" 2>/dev/null; then
  exit 0
fi
trap 'rmdir "$LOCK_DIR"' EXIT

# Sync AI sessions into aix.db and export raw sessions
/Users/tyler/go/bin/aix sync --all

# Import cursor sessions from aix into cortex DB
/Users/tyler/go/bin/cortex-sync --source cursor
