#!/usr/bin/env bash
#
# Sync scripts from skill directory to project .agents/scripts/
#
# Usage:
#     CLAUDE_PROJECT_DIR="..." CLAUDE_SKILL_DIR="..." bash sync-scripts.sh
#
# This script should be run from the skill directory, not copied to project.
#

# Require environment variables
if [ -z "$CLAUDE_PROJECT_DIR" ]; then
    echo "Error: CLAUDE_PROJECT_DIR not set" >&2
    exit 1
fi
if [ -z "$CLAUDE_SKILL_DIR" ]; then
    echo "Error: CLAUDE_SKILL_DIR not set" >&2
    exit 1
fi

PROJECT_DIR="$CLAUDE_PROJECT_DIR"
SKILL_DIR="$CLAUDE_SKILL_DIR"
AGENTS_DIR="$PROJECT_DIR/.agents"
CONFIG_FILE="$AGENTS_DIR/config.json"

# Compute MD5 hash (works on both macOS and Linux)
compute_md5() {
    md5 -q "$1" 2>/dev/null || md5sum "$1" | cut -d' ' -f1
}

# Compute MD5 hash of stdin content
compute_md5_stdin() {
    md5 2>/dev/null || md5sum | cut -d' ' -f1
}

[ -d "$AGENTS_DIR" ] || exit 0
[ -d "$SKILL_DIR" ] || exit 0

# Check if all updates disabled
if [ -f "$CONFIG_FILE" ]; then
    DISABLE=$(python3 -c "import json; c=json.load(open('$CONFIG_FILE')); print('true' if c.get('disableAutoUpdateScripts') is True else 'false')" 2>/dev/null || echo "false")
    [ "$DISABLE" = "true" ] && exit 0
fi

UPDATED=""

for SCRIPT in "$SKILL_DIR/scripts/"*.py; do
    [ -f "$SCRIPT" ] || continue
    BASENAME=$(basename "$SCRIPT")
    TARGET="$AGENTS_DIR/scripts/$BASENAME"

    # Check if disabled
    if [ -f "$CONFIG_FILE" ]; then
        SKIP=$(python3 -c "import json; c=json.load(open('$CONFIG_FILE')); d=c.get('disableAutoUpdateScripts',[]); print('true' if isinstance(d,list) and '$BASENAME' in d else 'false')" 2>/dev/null || echo "false")
        [ "$SKIP" = "true" ] && continue
    fi

    # If target doesn't exist, copy it (new script)
    if [ ! -f "$TARGET" ]; then
        cp "$SCRIPT" "$TARGET"
        chmod +x "$TARGET"
        UPDATED="$UPDATED $BASENAME(new)"
        continue
    fi

    # If target exists, check if it needs updating
    if [ "$(compute_md5 "$SCRIPT")" != "$(compute_md5 "$TARGET")" ]; then
        cp "$SCRIPT" "$TARGET"
        chmod +x "$TARGET"
        UPDATED="$UPDATED $BASENAME"
    fi
done

# Sync CLAUDE.md (preserve user content after marker)
TEMPLATE="$SKILL_DIR/templates/CLAUDE.md"
TARGET_MD="$AGENTS_DIR/CLAUDE.md"
USER_MARKER="<!-- USER CONTENT BELOW"
if [ -f "$TEMPLATE" ]; then
    if [ ! -f "$TARGET_MD" ]; then
        # Create new file from template
        cp "$TEMPLATE" "$TARGET_MD"
        UPDATED="$UPDATED CLAUDE.md(new)"
    else
        # Update existing file, preserving user content
        SRC_TEMPLATE=$(sed -n "1,/$USER_MARKER/p" "$TEMPLATE" | head -n -1)
        TGT_TEMPLATE=$(sed -n "1,/$USER_MARKER/p" "$TARGET_MD" | head -n -1)

        SRC_MD5=$(echo "$SRC_TEMPLATE" | compute_md5_stdin)
        TGT_MD5=$(echo "$TGT_TEMPLATE" | compute_md5_stdin)

        if [ "$SRC_MD5" != "$TGT_MD5" ]; then
            USER_CONTENT=$(sed -n "/$USER_MARKER/,\$p" "$TARGET_MD" | tail -n +2)
            cat "$TEMPLATE" > "$TARGET_MD"
            [ -n "$USER_CONTENT" ] && echo "$USER_CONTENT" >> "$TARGET_MD"
            UPDATED="$UPDATED CLAUDE.md"
        fi
    fi
fi

# Remove orphaned scripts (only those marked as auto-managed)
for TARGET in "$AGENTS_DIR/scripts/"*.py; do
    [ -f "$TARGET" ] || continue
    BASENAME=$(basename "$TARGET")
    SOURCE="$SKILL_DIR/scripts/$BASENAME"

    # Skip if source still exists
    [ -f "$SOURCE" ] && continue

    # Only remove if file has the auto-managed marker
    if head -n 10 "$TARGET" | grep -q "Managed by: agent-centric skill"; then
        rm -f "$TARGET"
        UPDATED="$UPDATED $BASENAME(removed)"
    fi
done

# Sync .gitignore
GITIGNORE_SRC="$SKILL_DIR/templates/gitignore"
GITIGNORE_TGT="$AGENTS_DIR/.gitignore"
if [ -f "$GITIGNORE_SRC" ]; then
    if [ ! -f "$GITIGNORE_TGT" ]; then
        cp "$GITIGNORE_SRC" "$GITIGNORE_TGT"
        UPDATED="$UPDATED .gitignore(new)"
    else
        if [ "$(compute_md5 "$GITIGNORE_SRC")" != "$(compute_md5 "$GITIGNORE_TGT")" ]; then
            cp "$GITIGNORE_SRC" "$GITIGNORE_TGT"
            UPDATED="$UPDATED .gitignore"
        fi
    fi
fi

[ -n "$UPDATED" ] && echo "SYNC:$UPDATED"
exit 0
