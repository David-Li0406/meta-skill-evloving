#!/bin/bash
# bundle-artifact.sh - Bundle React project to single HTML file for claude.ai artifacts
# Usage: bash bundle-artifact.sh
# Run from project root directory (where package.json is located)

set -e

echo "Bundling artifact to single HTML file..."

# Check for index.html
if [ ! -f "index.html" ]; then
    echo "Error: index.html not found in current directory"
    echo "Make sure you're running this from the project root"
    exit 1
fi

# Check for package.json
if [ ! -f "package.json" ]; then
    echo "Error: package.json not found in current directory"
    exit 1
fi

# Install bundling dependencies if not present
echo "Checking bundling dependencies..."

if ! npm ls parcel > /dev/null 2>&1; then
    echo "Installing parcel and bundling tools..."
    npm install --save-dev parcel @parcel/config-default parcel-resolver-tspaths html-inline
fi

# Create .parcelrc for path alias support
cat > .parcelrc << 'PARCELRC'
{
  "extends": "@parcel/config-default",
  "resolvers": ["parcel-resolver-tspaths", "..."]
}
PARCELRC

# Clean previous builds
rm -rf dist .parcel-cache bundle.html

# Build with Parcel (production, no source maps)
echo "Building with Parcel..."
npx parcel build index.html --no-source-maps --dist-dir dist --public-url ./

# Find the generated HTML file
DIST_HTML=$(find dist -name "*.html" -type f | head -1)

if [ -z "$DIST_HTML" ]; then
    echo "Error: No HTML file found in dist/"
    exit 1
fi

echo "Inlining all assets..."

# Inline all assets into single HTML
npx html-inline "$DIST_HTML" -o bundle.html -b dist

# Check result
if [ -f "bundle.html" ]; then
    SIZE=$(du -h bundle.html | cut -f1)
    echo ""
    echo "Success! Created bundle.html ($SIZE)"
    echo ""
    echo "The bundle.html file is ready to share as a claude.ai artifact."
else
    echo "Error: Failed to create bundle.html"
    exit 1
fi
