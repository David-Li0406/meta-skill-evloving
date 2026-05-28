#!/bin/bash
# Increment Android version code automatically
# Usage: ./increment-version.sh

set -e

BUILD_GRADLE="app/build.gradle.kts"

if [ ! -f "$BUILD_GRADLE" ]; then
    echo "❌ build.gradle.kts not found at: $BUILD_GRADLE"
    exit 1
fi

# Extract current version code
CURRENT_VERSION=$(grep -E "versionCode\s*=\s*[0-9]+" "$BUILD_GRADLE" | sed -E 's/.*versionCode\s*=\s*([0-9]+).*/\1/')

if [ -z "$CURRENT_VERSION" ]; then
    echo "❌ Could not find version code in $BUILD_GRADLE"
    echo "   Expected format: versionCode = 1"
    exit 1
fi

NEW_VERSION=$((CURRENT_VERSION + 1))

echo "Incrementing version code:"
echo "  Current: $CURRENT_VERSION"
echo "  New: $NEW_VERSION"

# Create backup
cp "$BUILD_GRADLE" "${BUILD_GRADLE}.bak"

# Update version code
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    sed -i '' "s/versionCode = $CURRENT_VERSION/versionCode = $NEW_VERSION/" "$BUILD_GRADLE"
else
    # Linux
    sed -i "s/versionCode = $CURRENT_VERSION/versionCode = $NEW_VERSION/" "$BUILD_GRADLE"
fi

# Verify change
NEW_CHECK=$(grep -E "versionCode\s*=\s*[0-9]+" "$BUILD_GRADLE" | sed -E 's/.*versionCode\s*=\s*([0-9]+).*/\1/')

if [ "$NEW_CHECK" == "$NEW_VERSION" ]; then
    echo "✅ Version code updated successfully"
    echo ""
    echo "Changes:"
    diff "${BUILD_GRADLE}.bak" "$BUILD_GRADLE" || true
    echo ""
    echo "Next steps:"
    echo "  1. Review the change"
    echo "  2. Commit: git add $BUILD_GRADLE && git commit -m 'Bump version code to $NEW_VERSION'"
    echo "  3. Push to trigger deployment"
    
    # Clean up backup
    rm "${BUILD_GRADLE}.bak"
else
    echo "❌ Version code update failed"
    echo "   Expected: $NEW_VERSION"
    echo "   Got: $NEW_CHECK"
    
    # Restore from backup
    mv "${BUILD_GRADLE}.bak" "$BUILD_GRADLE"
    exit 1
fi
