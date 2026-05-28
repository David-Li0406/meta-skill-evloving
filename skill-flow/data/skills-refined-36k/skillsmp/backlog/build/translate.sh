#!/bin/bash
# Claude Code to OpenCode Plugin Translator
#
# Translates Claude Code plugin commands to OpenCode format.
# This is a bash alternative if Bun is not available.
#
# Usage:
#   ./build/translate.sh

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PLUGIN_DIR="$(dirname "$SCRIPT_DIR")"

echo "═══════════════════════════════════════════════════════════════"
echo " Claude Code -> OpenCode Plugin Translator (Bash)"
echo "═══════════════════════════════════════════════════════════════"
echo "Plugin directory: $PLUGIN_DIR"
echo ""

# Create output directories
mkdir -p "$PLUGIN_DIR/.opencode/commands"
mkdir -p "$PLUGIN_DIR/.opencode/agents"

# Function to transform frontmatter
transform_command() {
    local input="$1"
    local output="$2"

    echo "Translating: $(basename "$input")"

    # Extract frontmatter and body
    local in_frontmatter=false
    local frontmatter=""
    local body=""
    local past_frontmatter=false
    local fm_start=false

    while IFS= read -r line || [[ -n "$line" ]]; do
        if [[ "$line" == "---" ]] && [[ "$fm_start" == false ]]; then
            fm_start=true
            in_frontmatter=true
            continue
        elif [[ "$line" == "---" ]] && [[ "$in_frontmatter" == true ]]; then
            in_frontmatter=false
            past_frontmatter=true
            continue
        fi

        if [[ "$in_frontmatter" == true ]]; then
            frontmatter+="$line"$'\n'
        elif [[ "$past_frontmatter" == true ]]; then
            body+="$line"$'\n'
        fi
    done < "$input"

    # Extract description from frontmatter
    local description
    description=$(echo "$frontmatter" | grep "^description:" | sed 's/^description: *//')

    # Transform body: replace /up:xxx with /xxx
    body=$(echo "$body" | sed 's/\/up:\([a-zA-Z]*\)/\/\1/g')
    body=$(echo "$body" | sed 's/\/backlog:\([a-zA-Z]*\)/\/\1/g')
    body=$(echo "$body" | sed 's/\/design:\([a-zA-Z]*\)/\/\1/g')

    # Write output
    {
        echo "---"
        echo "description: $description"
        echo "---"
        echo "$body"
    } > "$output"

    echo "  -> $output"
}

# Translate commands
if [[ -d "$PLUGIN_DIR/commands" ]]; then
    echo "Translating commands..."
    for cmd in "$PLUGIN_DIR/commands"/*.md; do
        [[ -f "$cmd" ]] || continue
        filename=$(basename "$cmd")
        transform_command "$cmd" "$PLUGIN_DIR/.opencode/commands/$filename"
    done
    echo ""
fi

# Translate agents (if any exist)
if [[ -d "$PLUGIN_DIR/agents" ]]; then
    echo "Translating agents..."
    for agent in "$PLUGIN_DIR/agents"/*.md; do
        [[ -f "$agent" ]] || continue
        filename=$(basename "$agent")
        # Agents need more complex transformation, use bun for full support
        echo "  Agent translation requires bun - skipping $filename"
    done
    echo ""
fi

echo "Translation complete!"
echo ""
echo "OpenCode files written to .opencode/ directory"
