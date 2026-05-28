#!/usr/bin/env bash
# bootstrap-with-patterns.sh - Enhanced Phase 0 bootstrap with pattern discovery
# Integrates into loop skill Phase 0
# Usage: source this in loop or run standalone

set -euo pipefail

PATTERNS_DIR="${PATTERNS_DIR:-$HOME/.loop/patterns}"
DISCOVERY_FILE="${DISCOVERY_FILE:-$HOME/.loop/discovered-projects.json}"
PROJECT_ROOT="${1:-.}"

echo "=== Pattern-Enhanced Bootstrap ==="

# Standard bootstrap (from loop SKILL.md)
echo "=== Project Detection ==="
PROJECT_TYPE="unknown"
[ -f "package.json" ] && PROJECT_TYPE="node"
[ -f "Cargo.toml" ] && PROJECT_TYPE="rust"
[ -f "pyproject.toml" ] && PROJECT_TYPE="python"
[ -f "go.mod" ] && PROJECT_TYPE="go"
[ -d ".xcodeproj" ] || ls -d *.xcworkspace 2>/dev/null && PROJECT_TYPE="xcode"
[ -d "convex" ] && PROJECT_TYPE="convex"
echo "Project type: $PROJECT_TYPE"

# If Convex project, check for patterns
if [[ "$PROJECT_TYPE" == "convex" ]]; then
    echo ""
    echo "=== Pattern Discovery Check ==="
    
    # Check if patterns exist and are fresh (< 7 days old)
    if [[ -d "$PATTERNS_DIR" ]]; then
        pattern_age=$(find "$PATTERNS_DIR" -name "*.md" -mtime -7 2>/dev/null | wc -l)
        if [[ $pattern_age -gt 0 ]]; then
            echo "✅ Fresh patterns found (< 7 days old)"
            echo "Patterns available:"
            ls -1 "$PATTERNS_DIR"/*.md 2>/dev/null | xargs -n1 basename
        else
            echo "⏰ Patterns stale or missing, discovering..."
            # Run discovery in background if possible
            if command -v nohup &>/dev/null; then
                nohup bash -c "cd $(dirname $0) && ./discover-projects.sh && ./extract-patterns.sh" > /dev/null 2>&1 &
                echo "🔄 Pattern discovery running in background"
            else
                echo "Run: loop/scripts/discover-projects.sh && loop/scripts/extract-patterns.sh"
            fi
        fi
    else
        echo "📋 No patterns found. Discovering from your projects..."
        echo "This may take a minute on first run..."
        
        # Discover and extract patterns
        SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
        if [[ -f "$SCRIPT_DIR/discover-projects.sh" ]]; then
            "$SCRIPT_DIR/discover-projects.sh" && "$SCRIPT_DIR/extract-patterns.sh"
            echo "✅ Pattern extraction complete"
        else
            echo "⚠️  Pattern scripts not found. Continuing without patterns."
        fi
    fi
    
    echo ""
    echo "=== Project Patterns Summary ==="
    
    # If patterns exist, show quick summary
    if [[ -f "$PATTERNS_DIR/file-structure.md" ]]; then
        echo "📁 File Structure Pattern:"
        head -20 "$PATTERNS_DIR/file-structure.md" | tail -15
        echo ""
    fi
    
    if [[ -f "$PATTERNS_DIR/test-patterns.md" ]]; then
        echo "🧪 Test Pattern:"
        grep -A 3 "### Naming Conventions" "$PATTERNS_DIR/test-patterns.md" || echo "See: $PATTERNS_DIR/test-patterns.md"
        echo ""
    fi
    
    if [[ -f "$PATTERNS_DIR/commit-style.md" ]]; then
        echo "💬 Commit Style:"
        grep -A 8 "#### Lowercase Style" "$PATTERNS_DIR/commit-style.md" | grep -v "^#" | head -6 || echo "See: $PATTERNS_DIR/commit-style.md"
        echo ""
    fi
fi

echo "=== Monorepo Detection ==="
[ -f "pnpm-workspace.yaml" ] && echo "Monorepo: pnpm workspaces"
[ -f "turbo.json" ] && echo "Monorepo: turborepo"
[ -f "nx.json" ] && echo "Monorepo: nx"
[ -f "lerna.json" ] && echo "Monorepo: lerna"

echo "=== Test Runner Discovery ==="
[ -f "package.json" ] && grep -qE "vitest|jest|mocha" package.json 2>/dev/null && echo "Test: vitest/jest/mocha"
[ -f "pyproject.toml" ] && grep -q "pytest" pyproject.toml 2>/dev/null && echo "Test: pytest"
[ -f "Cargo.toml" ] && echo "Test: cargo test"
[ -f "go.mod" ] && echo "Test: go test"

echo "=== Lint/Format Discovery ==="
ls .eslintrc* eslint.config.* 2>/dev/null && echo "Lint: eslint"
ls .prettierrc* prettier.config.* 2>/dev/null && echo "Format: prettier"
[ -f "biome.json" ] && echo "Lint/Format: biome"
ls .ruff.toml ruff.toml 2>/dev/null && echo "Lint: ruff"

echo "=== Personal Trajectory ==="
git log --author="$(git config user.name)" --oneline -10 2>/dev/null || echo "No personal commits"

echo "=== Repo Trajectory ==="
git log --oneline -10 2>/dev/null
echo "File hotspots:"
git log -n 20 --name-only --format="" 2>/dev/null | sort | uniq -c | sort -rn | head -10

echo "=== Work In Progress ==="
git status --short 2>/dev/null
git branch --list 2>/dev/null | grep -iE "wip|feature|fix"
git stash list 2>/dev/null | head -5

echo "=== Code Style Patterns ==="
if command -v rg &>/dev/null; then
  rg -n "^(export|class|interface|type|function|const) " --type ts 2>/dev/null | head -10
else
  grep -rn "^export\|^class\|^function" --include="*.ts" . 2>/dev/null | head -10
fi

echo "=== Test Conventions ==="
find . -name "*.test.*" -o -name "*.spec.*" 2>/dev/null | head -10

echo "=== Import Patterns ==="
if command -v rg &>/dev/null; then
  rg -n "^import " --type ts 2>/dev/null | head -10
else
  grep -rn "^import" --include="*.ts" . 2>/dev/null | head -10
fi

echo "=== README Gate ==="
[ -f "README.md" ] && head -50 README.md
[ -f "CONTRIBUTING.md" ] && head -30 CONTRIBUTING.md

echo ""
echo "=== Bootstrap Complete ==="
if [[ -d "$PATTERNS_DIR" ]] && [[ "$PROJECT_TYPE" == "convex" ]]; then
    echo "📚 Patterns loaded from: $PATTERNS_DIR"
    echo "Use patterns as reference for:"
    echo "  - File organization"
    echo "  - Test structure"
    echo "  - Schema design"
    echo "  - Commit messages"
    echo "  - Import conventions"
fi
