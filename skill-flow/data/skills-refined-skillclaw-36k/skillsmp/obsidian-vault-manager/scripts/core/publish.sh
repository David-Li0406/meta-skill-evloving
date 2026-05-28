#!/bin/bash
# Publish Obsidian note to GitHub Pages (sharehub)
# Handles image copying and path conversion
# Usage: ./publish.sh NOTE_FILE

set -e  # Exit on error

NOTE_FILE="$1"
VAULT_PATH="/Users/zorro/Documents/Obsidian/Claudecode"
SHAREHUB_PATH="/Users/zorro/Dev/sharehub"

# Add .md extension if not provided
if [[ ! "$NOTE_FILE" =~ \.md$ ]]; then
    NOTE_FILE="${NOTE_FILE}.md"
fi

# Check if file exists in vault
if [[ ! -f "$VAULT_PATH/$NOTE_FILE" ]]; then
    echo "❌ Error: File not found: $NOTE_FILE"
    echo "Looking in: $VAULT_PATH/"
    exit 1
fi

echo "✅ Found note: $NOTE_FILE"
echo ""

# Extract and copy referenced images
cd "$VAULT_PATH"

# Find all image references (macOS compatible)
IMAGE_PATHS=$(grep -o '!\[[^]]*\]([^)]*\.\(jpg\|jpeg\|png\|gif\|svg\|webp\))' "$NOTE_FILE" | sed 's/.*(\(.*\))/\1/' || true)

if [[ -n "$IMAGE_PATHS" ]]; then
    echo "📸 Found images to copy:"
    echo "$IMAGE_PATHS"
    echo ""

    # Copy each image to sharehub
    while IFS= read -r IMG_PATH; do
        # Skip if empty or URL (http/https)
        if [[ -z "$IMG_PATH" ]] || [[ "$IMG_PATH" =~ ^https?:// ]]; then
            continue
        fi

        # Normalize path (remove leading ./)
        CLEAN_PATH="${IMG_PATH#./}"

        # Source path in vault
        SRC="$VAULT_PATH/$CLEAN_PATH"

        # Destination path in sharehub (preserve directory structure)
        DEST="$SHAREHUB_PATH/$CLEAN_PATH"
        DEST_DIR=$(dirname "$DEST")

        if [[ -f "$SRC" ]]; then
            # Create destination directory if needed
            mkdir -p "$DEST_DIR"

            # Copy image
            cp "$SRC" "$DEST"
            echo "  ✅ Copied: $CLEAN_PATH"
        else
            echo "  ⚠️  Not found: $SRC"
        fi
    done <<< "$IMAGE_PATHS"
    echo ""
else
    echo "ℹ️  No local images found in note"
    echo ""
fi

# Read note content
NOTE_CONTENT=$(cat "$NOTE_FILE")

# Convert image paths for GitHub Pages using Python for reliable regex
# ./images/file.jpg → /sharehub/images/file.jpg
# images/file.jpg → /sharehub/images/file.jpg
CONVERTED_CONTENT=$(echo "$NOTE_CONTENT" | python3 -c '
import sys, re

content = sys.stdin.read()

# Pattern 1: ./path/to/image.ext -> /sharehub/path/to/image.ext
content = re.sub(r"!\[([^\]]*)\]\(\./([^)]+\.(jpg|jpeg|png|gif|svg|webp))\)", r"![\1](/sharehub/\2)", content, flags=re.IGNORECASE)

# Pattern 2: path/to/image.ext (no leading ./) -> /sharehub/path/to/image.ext
# But skip URLs (http:// or https://)
content = re.sub(r"!\[([^\]]*)\]\((?!https?://|/)([^)]+\.(jpg|jpeg|png|gif|svg|webp))\)", r"![\1](/sharehub/\2)", content, flags=re.IGNORECASE)

print(content, end="")
')

echo "📝 Image path conversion complete"
echo ""

# Write converted content to sharehub
DEST_NOTE="$SHAREHUB_PATH/documents/$NOTE_FILE"
echo "$CONVERTED_CONTENT" > "$DEST_NOTE"

echo "✅ Copied note to: documents/$NOTE_FILE"
echo ""

# Git operations
cd "$SHAREHUB_PATH"

echo "📋 Git status:"
git status --short
echo ""

# Add all changes (document + images)
git add "documents/$NOTE_FILE"
git add images/ 2>/dev/null || true

# Get note title from frontmatter for commit message
NOTE_TITLE=$(grep -m1 '^title:' "documents/$NOTE_FILE" | sed 's/title: *["'"'"']*//;s/["'"'"']*$//' || echo "$NOTE_FILE")

# Commit
git commit -m "Publish: $NOTE_TITLE

- Published documents/$NOTE_FILE
- Copied associated images
- Converted image paths for GitHub Pages

🤖 Generated with Claude Code
Co-Authored-By: Claude <noreply@anthropic.com>"

# Push to GitHub
echo "🚀 Pushing to GitHub..."
git push origin main

echo ""
echo "✅ Published successfully!"
echo ""
echo "📄 Document: https://zorrocheng-mc.github.io/sharehub/documents/${NOTE_FILE%.md}.html"
echo "⏱️  GitHub Pages will deploy in ~60 seconds"
echo ""

exit 0
