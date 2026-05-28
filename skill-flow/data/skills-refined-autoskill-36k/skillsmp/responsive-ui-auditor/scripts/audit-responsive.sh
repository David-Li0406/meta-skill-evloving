#!/bin/bash

FILE_PATH=$1

if [ -z "$FILE_PATH" ]; then
  echo "Usage: $0 <file-path>"
  exit 1
fi

echo "🔍 Auditing for responsive pitfalls in: $FILE_PATH"
echo "-----------------------------------"

ISSUES=0

# Check for 100vh
if grep -q "100vh" "$FILE_PATH"; then
  echo "⚠️  Found '100vh'. Consider using '100dvh' or 'inset-0' for mobile compatibility."
  ((ISSUES++))
fi

# Check for fixed pixel widths (common anti-pattern in React components)
if grep -qE "width: [0-9]+px|w-\[[0-9]+px\]" "$FILE_PATH"; then
  echo "⚠️  Found fixed pixel width. Consider using relative units or Tailwind responsive classes."
  ((ISSUES++))
fi

# Check for hover without group or lg:
if grep -q "hover:" "$FILE_PATH" && ! grep -qE "lg:hover:|group-hover:" "$FILE_PATH"; then
  echo "⚠️  Found 'hover:' without desktop gating. Ensure this isn't critical functionality."
  ((ISSUES++))
fi

# Check for aspect ratio
if ! grep -qE "aspect-|ratio" "$FILE_PATH" && grep -q "<img" "$FILE_PATH"; then
  echo "ℹ️  Image found but no aspect-ratio noted. Check for layout shift."
fi

echo "-----------------------------------"
if [ $ISSUES -eq 0 ]; then
  echo "✅ No critical responsive pitfalls detected!"
else
  echo "❌ Found $ISSUES potential issues to review."
fi

exit $ISSUES
