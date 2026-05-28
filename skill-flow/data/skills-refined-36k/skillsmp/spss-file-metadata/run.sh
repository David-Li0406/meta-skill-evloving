#!/bin/bash
# Wrapper script to run the metadata extractor with the virtual environment

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_PYTHON="$SCRIPT_DIR/venv/bin/python"
EXTRACT_SCRIPT="$SCRIPT_DIR/extract_sav_metadata.py"

# Check if venv exists
if [ ! -f "$VENV_PYTHON" ]; then
    echo "Error: Virtual environment not found. Please run:" >&2
    echo "  cd $SCRIPT_DIR && python3 -m venv venv && venv/bin/pip install -r requirements.txt" >&2
    exit 1
fi

# Run the script with the venv python
exec "$VENV_PYTHON" "$EXTRACT_SCRIPT" "$@"
