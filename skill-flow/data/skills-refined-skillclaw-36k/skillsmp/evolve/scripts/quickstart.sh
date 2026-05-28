#!/bin/bash
# Self-Evolving Agent - Quick Start Script
#
# One-command setup for a new project:
#   curl -fsSL ... | bash -s -- /path/to/project
#
# Or from local:
#   ./scripts/quickstart.sh /path/to/project

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
BOLD='\033[1m'
NC='\033[0m'

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

# Default target is current directory
TARGET_DIR="${1:-.}"

print_header() {
    echo ""
    echo -e "${CYAN}╔══════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${CYAN}║${NC}  ${BOLD}Self-Evolving Agent - Quick Start${NC}                           ${CYAN}║${NC}"
    echo -e "${CYAN}║${NC}  ${YELLOW}v4.1.0${NC} - Autonomous Goal Achievement                        ${CYAN}║${NC}"
    echo -e "${CYAN}╚══════════════════════════════════════════════════════════════╝${NC}"
    echo ""
}

print_step() {
    echo -e "${BLUE}▶${NC} ${BOLD}$1${NC}"
}

print_success() {
    echo -e "  ${GREEN}✓${NC} $1"
}

print_warning() {
    echo -e "  ${YELLOW}!${NC} $1"
}

print_error() {
    echo -e "  ${RED}✗${NC} $1"
}

# Step 1: Validate target directory
validate_target() {
    print_step "Validating target directory..."

    # Resolve to absolute path
    TARGET_DIR="$(cd "$TARGET_DIR" 2>/dev/null && pwd)" || {
        print_error "Directory does not exist: $TARGET_DIR"
        exit 1
    }

    print_success "Target: $TARGET_DIR"

    # Check if git repo
    if [[ -d "$TARGET_DIR/.git" ]]; then
        print_success "Git repository detected"
    else
        print_warning "Not a git repository - initializing..."
        (cd "$TARGET_DIR" && git init --quiet)
        print_success "Git initialized"
    fi
}

# Step 2: Install skill
install_skill() {
    print_step "Installing Self-Evolving Agent skill..."

    local skill_dir="$TARGET_DIR/.claude/skills/evolve"

    # Create directory
    mkdir -p "$skill_dir"

    # Copy skills
    if [[ -d "$PROJECT_ROOT/skills" ]]; then
        cp -r "$PROJECT_ROOT/skills"/* "$skill_dir/"
        print_success "Skills installed to .claude/skills/evolve/"
    else
        print_error "Skills directory not found in source"
        exit 1
    fi
}

# Step 3: Initialize memory system
init_memory() {
    print_step "Initializing memory system..."

    local memory_dir="$TARGET_DIR/.claude/memory"

    # Create structure
    mkdir -p "$memory_dir"/{learnings,failures,decisions,patterns,strategies,discoveries,skill-metrics}

    # Create .gitkeep files
    for dir in learnings failures decisions patterns strategies discoveries skill-metrics; do
        touch "$memory_dir/$dir/.gitkeep"
    done

    # Create index.md if not exists
    if [[ ! -f "$memory_dir/index.md" ]]; then
        cat > "$memory_dir/index.md" << 'EOF'
# 專案記憶索引

> 搜尋：`Grep pattern="關鍵字" path=".claude/memory/"`

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

## 策略記錄
<!-- STRATEGIES_START -->
<!-- STRATEGIES_END -->

## 涌現發現
<!-- DISCOVERIES_START -->
<!-- DISCOVERIES_END -->

## 標籤索引
<!-- TAGS_START -->
<!-- TAGS_END -->
EOF
        print_success "Memory index created"
    else
        print_warning "Memory index already exists - skipping"
    fi

    print_success "Memory system initialized"
}

# Step 4: Create CLAUDE.md if not exists
create_claude_md() {
    print_step "Checking CLAUDE.md..."

    local claude_md="$TARGET_DIR/CLAUDE.md"

    if [[ ! -f "$claude_md" ]]; then
        cat > "$claude_md" << 'EOF'
# Project Context for AI Assistants

## Overview

This project uses the Self-Evolving Agent skill for autonomous goal achievement.

## Quick Commands

```bash
/evolve [goal]              # Start evolving towards a goal
/evolve [goal] --explore    # Exploration mode
/evolve [goal] --emergence  # Emergence mode (cross-domain connections)
```

## Memory System

- `.claude/memory/` - Git-based memory for learnings, failures, decisions
- Always search memory before starting new tasks
- Record learnings after completing tasks

## Checkpoints (Mandatory)

1. **CP1**: Search memory before starting tasks
2. **CP2**: Build + test after code changes
3. **CP3**: Confirm direction after milestones
4. **CP3.5**: Sync index.md after creating memory files
5. **CP4**: Check emergence opportunities (optional)

## Development Guidelines

- Run validation: `./scripts/check-env.sh`
- Commit convention: `feat:`, `fix:`, `docs:`, `refactor:`
EOF
        print_success "CLAUDE.md created"
    else
        print_warning "CLAUDE.md already exists - skipping"
    fi
}

# Step 5: Setup hooks (optional)
setup_hooks() {
    print_step "Setting up hooks (optional)..."

    local settings_file="$TARGET_DIR/.claude/settings.local.json"

    if [[ ! -f "$settings_file" ]]; then
        cat > "$settings_file" << 'EOF'
{
  "hooks": {
    "Stop": [
      {
        "command": "echo '💡 Session ended - consider recording learnings to .claude/memory/'"
      }
    ]
  }
}
EOF
        print_success "Hooks configured in .claude/settings.local.json"
    else
        print_warning "Settings file exists - skipping hook setup"
    fi
}

# Step 6: Verify installation
verify_installation() {
    print_step "Verifying installation..."

    local errors=0

    # Check skill
    if [[ -f "$TARGET_DIR/.claude/skills/evolve/SKILL.md" ]]; then
        print_success "Skill installed"
    else
        print_error "Skill not found"
        ((errors++))
    fi

    # Check memory
    if [[ -f "$TARGET_DIR/.claude/memory/index.md" ]]; then
        print_success "Memory system ready"
    else
        print_error "Memory system not initialized"
        ((errors++))
    fi

    # Check CLAUDE.md
    if [[ -f "$TARGET_DIR/CLAUDE.md" ]]; then
        print_success "CLAUDE.md present"
    else
        print_warning "CLAUDE.md not found (optional)"
    fi

    return $errors
}

# Print completion message
print_completion() {
    echo ""
    echo -e "${GREEN}╔══════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${GREEN}║${NC}  ${BOLD}Setup Complete!${NC}                                             ${GREEN}║${NC}"
    echo -e "${GREEN}╚══════════════════════════════════════════════════════════════╝${NC}"
    echo ""
    echo -e "  ${BOLD}Next Steps:${NC}"
    echo ""
    echo -e "  1. Open the project in Claude Code:"
    echo -e "     ${CYAN}cd $TARGET_DIR && claude${NC}"
    echo ""
    echo -e "  2. Start evolving towards your goal:"
    echo -e "     ${CYAN}/evolve [describe your goal]${NC}"
    echo ""
    echo -e "  3. Examples:"
    echo -e "     ${YELLOW}/evolve Build a REST API with authentication${NC}"
    echo -e "     ${YELLOW}/evolve Optimize database queries for performance${NC}"
    echo -e "     ${YELLOW}/evolve Make this project better --explore${NC}"
    echo ""
    echo -e "  ${BOLD}Documentation:${NC} $TARGET_DIR/.claude/skills/evolve/SKILL.md"
    echo ""
}

# Main
main() {
    print_header

    validate_target
    install_skill
    init_memory
    create_claude_md
    setup_hooks

    echo ""
    if verify_installation; then
        print_completion
    else
        echo ""
        print_error "Installation incomplete - please check errors above"
        exit 1
    fi
}

# Show help
if [[ "$1" == "--help" || "$1" == "-h" ]]; then
    echo "Self-Evolving Agent - Quick Start"
    echo ""
    echo "Usage: $0 [target-directory]"
    echo ""
    echo "Arguments:"
    echo "  target-directory  Directory to set up (default: current directory)"
    echo ""
    echo "Examples:"
    echo "  $0                    # Setup in current directory"
    echo "  $0 /path/to/project   # Setup in specified directory"
    echo "  $0 ~/my-new-project   # Setup in home directory project"
    echo ""
    exit 0
fi

main "$@"
