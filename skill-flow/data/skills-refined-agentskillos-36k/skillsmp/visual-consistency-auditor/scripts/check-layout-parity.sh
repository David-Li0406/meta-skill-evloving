#!/bin/bash

FILE_PATH=$1

if [ -z "$FILE_PATH" ]; then
  echo "Usage: $0 <file-path>"
  exit 1
fi

echo "🖼️  Checking for layout parity issues in: $FILE_PATH"
echo "-----------------------------------"

# Check for elements only visible on large screens
LG_ONLY=$(grep -c "hidden lg:" "$FILE_PATH")
# Check for elements only visible on mobile
MOBILE_ONLY=$(grep -cE "lg:hidden|block lg:hidden|flex lg:hidden" "$FILE_PATH")

echo "Desktop-only classes found: $LG_ONLY"
echo "Mobile-only classes found: $MOBILE_ONLY"

if [ $LG_ONLY -gt 0 ] && [ $MOBILE_ONLY -eq 0 ]; then
  echo "⚠️  Found desktop-only content but no mobile equivalents. Check if functionality is lost on mobile."
fi

# Check for aspect ratio in skeletons
if grep -q "Skeleton" "$FILE_PATH" && ! grep -qE "aspect-|ratio" "$FILE_PATH"; then
  echo "⚠️  Skeleton found but no aspect ratio defined. This might cause CLS when content loads."
fi

echo "-----------------------------------"
