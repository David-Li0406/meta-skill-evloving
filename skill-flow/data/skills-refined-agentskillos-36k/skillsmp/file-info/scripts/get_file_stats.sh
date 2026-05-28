#!/bin/bash
# Script to gather file statistics and create verification marker

FILE="$1"

# Create verification marker
touch /tmp/executed.txt

if [ ! -e "$FILE" ]; then
    echo "Error: File does not exist: $FILE"
    exit 1
fi

# Get file stats
if [ -d "$FILE" ]; then
    echo "Type: Directory"
    echo "Files: $(find "$FILE" -maxdepth 1 -type f | wc -l | tr -d ' ')"
else
    echo "Type: File"
    echo "Lines: $(wc -l < "$FILE" | tr -d ' ')"
    echo "Size: $(stat -f%z "$FILE") bytes"
fi

echo "Modified: $(stat -f%Sm -t '%Y-%m-%d %H:%M:%S' "$FILE")"
echo "Path: $(realpath "$FILE")"
