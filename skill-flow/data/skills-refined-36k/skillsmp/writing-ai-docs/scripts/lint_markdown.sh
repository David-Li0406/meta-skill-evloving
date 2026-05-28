#!/bin/bash
# Lint markdown files using markdownlint-cli
# This script uses npx to run markdownlint without requiring global installation

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

# Check if arguments provided
if [ $# -eq 0 ]; then
    print_error "No files or patterns specified"
    echo ""
    echo "Usage: bash scripts/lint_markdown.sh <file-or-pattern> [file-or-pattern...]"
    echo ""
    echo "Examples:"
    echo "  bash scripts/lint_markdown.sh docs/api/get-users.md     # Single file"
    echo "  bash scripts/lint_markdown.sh README.md SKILL.md        # Multiple files"
    echo "  bash scripts/lint_markdown.sh \"**/*.md\"                  # All markdown files"
    echo "  bash scripts/lint_markdown.sh \"templates/*.md\"           # All templates"
    echo ""
    exit 1
fi

# Store all arguments as files to lint
FILES="$@"

# Get script directory and skill directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"
CONFIG_FILE="$SKILL_DIR/.markdownlint.json"

# Check if config exists
if [ ! -f "$CONFIG_FILE" ]; then
    print_warning "Config file not found: $CONFIG_FILE"
    print_info "Using default markdownlint rules"
    CONFIG_OPTION=""
else
    CONFIG_OPTION="--config $CONFIG_FILE"
fi

print_info "Linting: $FILES"
echo ""

# Run markdownlint via npx
# --fix flag can be added to auto-fix issues
if npx markdownlint-cli $CONFIG_OPTION $FILES; then
    echo ""
    print_success "No markdown linting issues found"
    exit 0
else
    echo ""
    print_error "Markdown linting issues found"
    echo ""
    print_info "To auto-fix some issues, run:"
    echo "  npx markdownlint-cli $CONFIG_OPTION --fix $FILES"
    echo ""
    exit 1
fi
