#!/usr/bin/env bash
# Initialize the content bank structure and add reminders to agent instruction files
# Usage: init.sh [--agent claude|other]
#   --agent claude  Only update CLAUDE.md (for Claude Code)
#   --agent other   Only update AGENTS.md (for other agents like Cursor, Codex)
#   (no argument)   Update both files (manual initialization)
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"
PROJECT_ROOT="${PROJECT_ROOT:-$(git rev-parse --show-toplevel 2>/dev/null || pwd)}"
CONTENT_BANK_DIR="$PROJECT_ROOT/content-bank"

REMINDER_MARKER="<!-- CONTENT-BANK-REMINDER -->"
AGENT_TYPE=""

# Parse arguments
while [[ $# -gt 0 ]]; do
  case $1 in
    --agent)
      AGENT_TYPE="$2"
      shift 2
      ;;
    *)
      echo "Unknown argument: $1"
      echo "Usage: init.sh [--agent claude|other]"
      exit 1
      ;;
  esac
done

# Function to check if reminder already exists in a file
reminder_exists() {
  local file="$1"
  [[ -f "$file" ]] && grep -q "$REMINDER_MARKER" "$file"
}

# Function to add reminder to a file
add_reminder() {
  local file="$1"
  cat >> "$file" << 'EOF'

<!-- CONTENT-BANK-REMINDER -->
## Content Bank Skill

When writing or coding, the **content-bank** skill is available:
- **Store** - Bank reusable writing (ideas, snippets, outlines) or code patterns
- **Retrieve** - Retrieve previously banked content for your current work
- **List** - Browse topics and banked content
- Reference `skills/content-bank/SKILL.md` for details
<!-- END CONTENT-BANK-REMINDER -->
EOF
}

echo "Initializing content bank..."
echo ""

# Create content-bank directory structure
mkdir -p "$CONTENT_BANK_DIR"

# Create topics.md index
if [[ ! -f "$CONTENT_BANK_DIR/topics.md" ]]; then
  cat > "$CONTENT_BANK_DIR/topics.md" << 'EOF'
# Content Bank Topics

A navigable index of all banked content topics.

## Topics

<!-- Add topics here as you bank content -->
<!-- Format: - [topic-name](./topic-name/) - Brief description -->

*No topics yet. Bank your first idea, snippet, or outline to get started.*
EOF
  echo "Created: content-bank/topics.md"
else
  echo "Skipped: content-bank/topics.md (already exists)"
fi

# Add reminder to agent instruction file(s)
CLAUDE_MD="$PROJECT_ROOT/CLAUDE.md"
AGENTS_MD="$PROJECT_ROOT/AGENTS.md"

# Function to update a single file
update_agent_file() {
  local file="$1"
  local name="$2"
  if [[ -f "$file" ]]; then
    if reminder_exists "$file"; then
      echo "Skipped: $name (reminder already present)"
    else
      add_reminder "$file"
      echo "Updated: $name with content bank reminder"
    fi
  else
    echo "Warning: $name not found at project root"
  fi
}

# Update based on agent type
if [[ "$AGENT_TYPE" == "claude" ]]; then
  update_agent_file "$CLAUDE_MD" "CLAUDE.md"
elif [[ "$AGENT_TYPE" == "other" ]]; then
  update_agent_file "$AGENTS_MD" "AGENTS.md"
else
  # No agent specified - update both (manual initialization)
  update_agent_file "$CLAUDE_MD" "CLAUDE.md"
  update_agent_file "$AGENTS_MD" "AGENTS.md"
fi

echo ""
echo "Content bank initialization complete!"
echo ""
echo "Structure created:"
echo "  content-bank/"
echo "  └── topics.md"
echo ""
echo "Next steps:"
echo "  1. Start drafting content"
echo "  2. Use bank:store to bank reusable ideas, snippets, or outlines"
echo "  3. Use bank:retrieve to find banked content when writing"
echo "  4. Use bank:list to browse your content bank"
