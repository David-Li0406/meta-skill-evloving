#!/bin/bash
#
# Self-Evolving Agent Installer
# 一行安裝：curl -fsSL https://raw.githubusercontent.com/miles990/self-evolving-agent/main/install.sh | bash
#

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Default values
TARGET_DIR="${PWD}"
BRANCH="main"
WITH_HOOKS=false
WITH_MEMORY=false
REPO_URL="https://github.com/miles990/self-evolving-agent.git"

# Functions
print_banner() {
    echo -e "${BLUE}"
    echo "╭───────────────────────────────────────────────╮"
    echo "│  🧬 Self-Evolving Agent Installer v4.0        │"
    echo "╰───────────────────────────────────────────────╯"
    echo -e "${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

usage() {
    echo "Usage: $0 [OPTIONS]"
    echo ""
    echo "Options:"
    echo "  --target DIR      Install to specific directory (default: current directory)"
    echo "  --with-hooks      Install Claude Code hooks"
    echo "  --with-memory     Initialize memory system"
    echo "  --branch BRANCH   Use specific branch (default: main)"
    echo "  --help            Show this help message"
    echo ""
    echo "Examples:"
    echo "  # Basic install"
    echo "  curl -fsSL https://raw.githubusercontent.com/miles990/self-evolving-agent/main/install.sh | bash"
    echo ""
    echo "  # Full install with hooks and memory"
    echo "  curl -fsSL https://raw.githubusercontent.com/miles990/self-evolving-agent/main/install.sh | bash -s -- --with-hooks --with-memory"
    echo ""
    echo "  # Install to specific project"
    echo "  curl -fsSL https://raw.githubusercontent.com/miles990/self-evolving-agent/main/install.sh | bash -s -- --target /path/to/project"
}

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --target)
            TARGET_DIR="$2"
            shift 2
            ;;
        --with-hooks)
            WITH_HOOKS=true
            shift
            ;;
        --with-memory)
            WITH_MEMORY=true
            shift
            ;;
        --branch)
            BRANCH="$2"
            shift 2
            ;;
        --help)
            usage
            exit 0
            ;;
        *)
            print_error "Unknown option: $1"
            usage
            exit 1
            ;;
    esac
done

# Main installation
print_banner

# Check dependencies
if ! command -v git &> /dev/null; then
    print_error "Git is required but not installed. Please install Git first."
    exit 1
fi

print_info "Target directory: ${TARGET_DIR}"

# Create temp directory
TEMP_DIR=$(mktemp -d)
trap "rm -rf ${TEMP_DIR}" EXIT

# Clone repository
print_info "Downloading Self-Evolving Agent..."
git clone --depth 1 --branch "${BRANCH}" "${REPO_URL}" "${TEMP_DIR}" 2>/dev/null || {
    print_error "Failed to download repository"
    exit 1
}

# Create skills directory
SKILLS_DIR="${TARGET_DIR}/.claude/skills/evolve"
mkdir -p "${SKILLS_DIR}"

# Backup existing installation
if [ -d "${SKILLS_DIR}" ] && [ "$(ls -A ${SKILLS_DIR})" ]; then
    BACKUP_DIR="${SKILLS_DIR}.backup.$(date +%Y%m%d%H%M%S)"
    print_warning "Existing installation found. Creating backup: ${BACKUP_DIR}"
    mv "${SKILLS_DIR}" "${BACKUP_DIR}"
    mkdir -p "${SKILLS_DIR}"
fi

# Copy skills
print_info "Installing skills..."
if [ -d "${TEMP_DIR}/skills" ]; then
    cp -r "${TEMP_DIR}/skills/"* "${SKILLS_DIR}/"
    print_success "Skills installed to ${SKILLS_DIR}"
else
    # Fallback: copy SKILL.md directly
    cp "${TEMP_DIR}/SKILL.md" "${SKILLS_DIR}/SKILL.md"
    print_success "SKILL.md installed to ${SKILLS_DIR}"
fi

# Initialize memory system
if [ "$WITH_MEMORY" = true ]; then
    print_info "Initializing memory system..."
    MEMORY_DIR="${TARGET_DIR}/.claude/memory"

    mkdir -p "${MEMORY_DIR}/learnings"
    mkdir -p "${MEMORY_DIR}/decisions"
    mkdir -p "${MEMORY_DIR}/failures"
    mkdir -p "${MEMORY_DIR}/patterns"
    mkdir -p "${MEMORY_DIR}/strategies"
    mkdir -p "${MEMORY_DIR}/discoveries"
    mkdir -p "${MEMORY_DIR}/skill-metrics"

    # Create .gitkeep files
    for dir in learnings decisions failures patterns strategies discoveries skill-metrics; do
        touch "${MEMORY_DIR}/${dir}/.gitkeep"
    done

    # Create index.md if not exists
    if [ ! -f "${MEMORY_DIR}/index.md" ]; then
        cat > "${MEMORY_DIR}/index.md" << 'EOF'
# 專案記憶索引

> Last curated: $(date +%Y-%m-%d)
> Total entries: 0
> Next review: $(date -d "+7 days" +%Y-%m-%d 2>/dev/null || date -v+7d +%Y-%m-%d)

## 統計
- Learnings: 0 筆
- Failures: 0 筆
- Decisions: 0 筆
- Patterns: 0 筆

## 最近學習
<!-- LEARNINGS_START -->
<!-- LEARNINGS_END -->

## 重要決策
<!-- DECISIONS_START -->
<!-- DECISIONS_END -->

## 失敗經驗
<!-- FAILURES_START -->
<!-- FAILURES_END -->

## 推理模式
<!-- PATTERNS_START -->
<!-- PATTERNS_END -->

## 標籤索引
<!-- TAGS_START -->
<!-- TAGS_END -->
EOF
    fi

    print_success "Memory system initialized at ${MEMORY_DIR}"
fi

# Install hooks
if [ "$WITH_HOOKS" = true ]; then
    print_info "Installing Claude Code hooks..."
    SETTINGS_FILE="${TARGET_DIR}/.claude/settings.local.json"

    if [ -f "${SETTINGS_FILE}" ]; then
        print_warning "settings.local.json already exists. Please manually add hooks."
    else
        cat > "${SETTINGS_FILE}" << 'EOF'
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "command": "echo '📝 File modified - remember to verify changes'"
      }
    ],
    "Stop": [
      {
        "command": "echo '💡 Session ended - consider recording learnings to .claude/memory/'"
      }
    ]
  }
}
EOF
        print_success "Hooks installed to ${SETTINGS_FILE}"
    fi
fi

# Print summary
echo ""
echo -e "${GREEN}╭───────────────────────────────────────────────╮${NC}"
echo -e "${GREEN}│  ✅ Installation Complete!                     │${NC}"
echo -e "${GREEN}╰───────────────────────────────────────────────╯${NC}"
echo ""
echo "Installed components:"
echo "  📁 Skills:  ${SKILLS_DIR}"
[ "$WITH_MEMORY" = true ] && echo "  📁 Memory:  ${TARGET_DIR}/.claude/memory"
[ "$WITH_HOOKS" = true ] && echo "  📁 Hooks:   ${TARGET_DIR}/.claude/settings.local.json"
echo ""
echo "Next steps:"
echo "  1. Open Claude Code in your project"
echo "  2. Use: /evolve [your goal]"
echo ""
echo "Documentation: https://github.com/miles990/self-evolving-agent"
