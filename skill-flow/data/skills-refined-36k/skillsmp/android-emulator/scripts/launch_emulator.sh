#!/bin/bash
# Android Emulator Launcher for MagentaLine
# Usage: ./launch_emulator.sh [phone|tablet]

set -e

DEVICE_TYPE="${1:-phone}"
SDK_PATH="$HOME/Library/Android/sdk"
JAVA_HOME="/Applications/Android Studio.app/Contents/jbr/Contents/Home"
export JAVA_HOME

case "$DEVICE_TYPE" in
    phone)
        AVD_NAME="Medium_Phone_API_36.1"
        ;;
    tablet)
        AVD_NAME="Medium_Tablet_API_36"
        ;;
    *)
        echo "Usage: $0 [phone|tablet]"
        exit 1
        ;;
esac

echo "Starting $DEVICE_TYPE emulator: $AVD_NAME"

# Kill any existing emulators
pkill -f "qemu-system-aarch64" 2>/dev/null || true

# Restart ADB server
"$SDK_PATH/platform-tools/adb" kill-server
"$SDK_PATH/platform-tools/adb" start-server

# Start emulator
"$SDK_PATH/emulator/emulator" -avd "$AVD_NAME" -no-snapshot-load &
EMULATOR_PID=$!

echo "Emulator started with PID: $EMULATOR_PID"
echo "Waiting for device to come online..."

# Wait for boot (max 2 minutes)
TIMEOUT=120
ELAPSED=0
while [ $ELAPSED -lt $TIMEOUT ]; do
    if "$SDK_PATH/platform-tools/adb" devices | grep -q "emulator-5554[[:space:]]*device"; then
        echo "Device is online!"
        flutter devices
        exit 0
    fi
    sleep 5
    ELAPSED=$((ELAPSED + 5))
    echo "Waiting... ($ELAPSED seconds)"
done

echo "ERROR: Device did not come online within $TIMEOUT seconds"
exit 1
