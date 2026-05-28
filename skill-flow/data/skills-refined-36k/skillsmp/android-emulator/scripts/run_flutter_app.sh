#!/bin/bash
# Run MagentaLine Flutter app on Android emulator
# Usage: ./run_flutter_app.sh

set -e

APP_DIR="/Users/william/Workspaces/MagentaLine/app"
SDK_PATH="$HOME/Library/Android/sdk"

# Check for connected emulator
if ! "$SDK_PATH/platform-tools/adb" devices | grep -q "emulator-5554[[:space:]]*device"; then
    echo "ERROR: No emulator device found. Run launch_emulator.sh first."
    exit 1
fi

echo "Running Flutter app on emulator..."
cd "$APP_DIR"
flutter run -d emulator-5554
