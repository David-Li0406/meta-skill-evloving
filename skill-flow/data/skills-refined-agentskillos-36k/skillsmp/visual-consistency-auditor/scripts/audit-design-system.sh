#!/bin/bash

FILE_PATH=$1

if [ -z "$FILE_PATH" ]; then
  echo "Usage: $0 <file-path>"
  exit 1
fi

echo "🎨 Auditing Design System Consistency in: $FILE_PATH"
echo "-----------------------------------"

ISSUES=0

# Check for hardcoded hex colors (case insensitive)
HEX_MATCHES=$(grep -iE "#[0-9A-Fa-f]{3,6}" "$FILE_PATH" | grep -vE "primary|neutral|accent|success|warning|error" | wc -l)
if [ $HEX_MATCHES -gt 0 ]; then
  echo "⚠️  Found $HEX_MATCHES hardcoded hex colors. Use Tailwind brand tokens instead (e.g., 'text-primary' or 'bg-neutral-100')."
  ((ISSUES++))
fi

# Check for hardcoded pixel padding/margins (simplified check)
PIXEL_SPACING=$(grep -E "(padding|margin): [0-9]+px" "$FILE_PATH" | wc -l)
if [ $PIXEL_SPACING -gt 0 ]; then
  echo "⚠️  Found $PIXEL_SPACING hardcoded pixel spacings. Use Tailwind spacing tokens instead (e.g., 'p-4')."
  ((ISSUES++))
fi

# Check if using base UI components when it seems relevant
if grep -q "img" "$FILE_PATH" && ! grep -q "ImageDisplay" "$FILE_PATH"; then
  echo "ℹ️  Found natively used <img /> tag. Consider using 'ImageDisplay' for skeleton and error handling."
  ((ISSUES++))
fi

echo "-----------------------------------"
if [ $ISSUES -eq 0 ]; then
  echo "✅ Design System audit passed!"
else
  echo "❌ Found $ISSUES potential consistency issues."
fi

exit $ISSUES
