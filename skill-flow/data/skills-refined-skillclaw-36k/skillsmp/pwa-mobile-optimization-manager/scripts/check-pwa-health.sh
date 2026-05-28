#!/bin/bash

# Check index.html for viewport and mobile meta tags
INDEX_FILE="index.html"
MANIFEST_FILE="public/manifest.json"

echo "📱 Checking PWA & Mobile Health..."
echo "-----------------------------------"

if [ -f "$INDEX_FILE" ]; then
    echo "Checking $INDEX_FILE..."
    if grep -q "viewport" "$INDEX_FILE"; then echo "✅ Viewport meta found"; else echo "❌ Viewport meta MISSING"; fi
    if grep -q "apple-mobile-web-app-capable" "$INDEX_FILE"; then echo "✅ iOS standalone meta found"; else echo "ℹ️ iOS standalone meta missing"; fi
else
    echo "❌ $INDEX_FILE not found!"
fi

if [ -f "$MANIFEST_FILE" ]; then
    echo "Checking $MANIFEST_FILE..."
    if grep -q "\"short_name\"" "$MANIFEST_FILE"; then echo "✅ short_name found"; else echo "❌ short_name MISSING"; fi
    if grep -q "\"icons\"" "$MANIFEST_FILE"; then echo "✅ icons found"; else echo "❌ icons MISSING"; fi
    if grep -q "\"display\": \"standalone\"" "$MANIFEST_FILE"; then echo "✅ display: standalone found"; else echo "ℹ️ display: standalone missing"; fi
else
    echo "ℹ️ $MANIFEST_FILE not found. PWA might not be configured."
fi

echo "-----------------------------------"
