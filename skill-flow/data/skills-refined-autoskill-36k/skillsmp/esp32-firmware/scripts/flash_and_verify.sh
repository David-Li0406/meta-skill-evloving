#!/bin/bash
# Flash ESP32 firmware and verify serial output
# Usage: ./flash_and_verify.sh [project_dir] [port] [verify_string]

set -e

PROJECT_DIR="${1:-.}"
PORT="${2:-/dev/ttyACM0}"
VERIFY_STRING="${3:-Hello}"
MONITOR_DURATION=10

echo "=== ESP32 Flash and Verify ==="
echo "Project: $PROJECT_DIR"
echo "Port: $PORT"
echo "Verify string: $VERIFY_STRING"
echo ""

# Source ESP-IDF environment
echo "Sourcing ESP-IDF environment..."
. ~/esp/esp-idf/export.sh

# Navigate to project
cd "$PROJECT_DIR"

# Build
echo ""
echo "=== Building firmware ==="
idf.py build

# Flash
echo ""
echo "=== Flashing firmware ==="
idf.py -p "$PORT" flash

# Wait for device to reset
sleep 2

# Monitor and capture output
echo ""
echo "=== Monitoring serial output (${MONITOR_DURATION}s) ==="
OUTPUT=$(python3 -c "
import serial
import time
import sys

ser = serial.Serial('$PORT', 115200, timeout=1)
output = []
start = time.time()
while time.time() - start < $MONITOR_DURATION:
    if ser.in_waiting:
        data = ser.read(ser.in_waiting).decode('utf-8', errors='ignore')
        output.append(data)
        print(data, end='', flush=True)
    time.sleep(0.05)
ser.close()
print('', file=sys.stderr)  # newline to stderr

# Check for verify string
full_output = ''.join(output)
if '$VERIFY_STRING' in full_output:
    print('VERIFICATION_PASSED', file=sys.stderr)
    sys.exit(0)
else:
    print('VERIFICATION_FAILED', file=sys.stderr)
    sys.exit(1)
" 2>&1)

echo "$OUTPUT"

if echo "$OUTPUT" | grep -q "VERIFICATION_PASSED"; then
    echo ""
    echo "=== SUCCESS: Found '$VERIFY_STRING' in output ==="
    exit 0
else
    echo ""
    echo "=== FAILED: Did not find '$VERIFY_STRING' in output ==="
    exit 1
fi
