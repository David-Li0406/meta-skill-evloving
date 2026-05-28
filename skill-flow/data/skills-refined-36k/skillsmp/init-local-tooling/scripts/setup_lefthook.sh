#!/bin/bash

# Setup lefthook Git hooks
# Usage: ./setup_lefthook.sh

set -e

echo "🪝 Setting up lefthook Git hooks"
echo ""

# Check if lefthook is installed
if command -v lefthook &> /dev/null; then
    CURRENT_VERSION=$(lefthook version 2>&1 | head -n1)
    echo "✓ lefthook is installed: $CURRENT_VERSION"

    # Check for updates (only with Homebrew)
    if command -v brew &> /dev/null && brew list lefthook &> /dev/null; then
        echo "  Checking for updates..."
        LATEST_INFO=$(brew info --json=v2 lefthook 2>/dev/null | jq -r '.formulae[0].versions.stable' 2>/dev/null || echo "")

        if [ -n "$LATEST_INFO" ] && [[ "$CURRENT_VERSION" != *"$LATEST_INFO"* ]]; then
            echo "  ⚠️  Update available: $LATEST_INFO"
            read -p "  Update lefthook? (y/n) " -n 1 -r
            echo
            if [[ $REPLY =~ ^[Yy]$ ]]; then
                brew upgrade lefthook
                echo "  ✓ Updated to $(lefthook version)"
            fi
        else
            echo "  ✓ lefthook is up to date"
        fi
    fi
else
    echo "❌ lefthook is not installed"
    echo ""
    echo "Installation options:"
    echo "  1. Homebrew (recommended): brew install lefthook"
    echo "  2. npm: pnpm add -D lefthook"
    echo "  3. Direct: https://github.com/evilmartians/lefthook"
    echo ""

    # Offer to install via Homebrew
    if command -v brew &> /dev/null; then
        read -p "Install lefthook via Homebrew? (y/n) " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            brew install lefthook
            echo "✓ Installed lefthook"
        else
            echo "⚠️  Please install lefthook manually and run this script again"
            exit 1
        fi
    else
        echo "⚠️  Homebrew not found. Please install lefthook manually:"
        echo "    https://github.com/evilmartians/lefthook#install"
        exit 1
    fi
fi

echo ""

# Check if lefthook.yml exists
if [ -f "lefthook.yml" ]; then
    echo "✓ lefthook.yml already exists"
    read -p "Overwrite existing lefthook.yml? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Keeping existing configuration"
        lefthook install
        exit 0
    fi
fi

# Detect project type
HAS_TS=false
HAS_RUST=false
HAS_PYTHON=false

if [ -f "package.json" ] || [ -f "tsconfig.json" ]; then
    HAS_TS=true
fi

if [ -f "Cargo.toml" ]; then
    HAS_RUST=true
fi

if [ -f "pyproject.toml" ] || [ -f "setup.py" ]; then
    HAS_PYTHON=true
fi

echo "📝 Detected project types:"
[ "$HAS_TS" = true ] && echo "  - TypeScript/JavaScript"
[ "$HAS_RUST" = true ] && echo "  - Rust"
[ "$HAS_PYTHON" = true ] && echo "  - Python"
echo ""

# Generate lefthook.yml
echo "📄 Creating lefthook.yml..."

cat > lefthook.yml << 'EOF'
# Lefthook Git hooks configuration
# https://github.com/evilmartians/lefthook

# Commit message validation
commit-msg:
  commands:
    commitlint:
      run: npx commitlint --edit {1}

# Pre-commit: Run on staged files only
pre-commit:
  parallel: true
  commands:
EOF

# Add TypeScript/JavaScript hooks
if [ "$HAS_TS" = true ]; then
    cat >> lefthook.yml << 'EOF'
    # TypeScript/JavaScript
    ts-lint:
      glob: "*.{js,ts,jsx,tsx}"
      run: npx eslint --fix {staged_files} || npx biome check --apply {staged_files}
      stage_fixed: true

    ts-format:
      glob: "*.{js,ts,jsx,tsx,json,md}"
      run: npx prettier --write {staged_files} || true
      stage_fixed: true
EOF
fi

# Add Rust hooks
if [ "$HAS_RUST" = true ]; then
    cat >> lefthook.yml << 'EOF'

    # Rust
    rust-fmt:
      glob: "*.rs"
      run: cargo fmt -- {staged_files}
      stage_fixed: true

    rust-clippy:
      glob: "*.rs"
      run: cargo clippy --fix --allow-dirty --allow-staged
      stage_fixed: true
EOF
fi

# Add Python hooks
if [ "$HAS_PYTHON" = true ]; then
    cat >> lefthook.yml << 'EOF'

    # Python
    py-format:
      glob: "*.py"
      run: ruff format {staged_files} && ruff check --fix {staged_files}
      stage_fixed: true

    py-typecheck:
      glob: "*.py"
      run: mypy {staged_files} || true
EOF
fi

# Add pre-push hooks
cat >> lefthook.yml << 'EOF'

# Pre-push: Full validation
pre-push:
  commands:
    validate:
      run: |
        echo "🔍 Running full validation..."
EOF

if [ "$HAS_TS" = true ]; then
    cat >> lefthook.yml << 'EOF'
        npm run lint && npm run type-check && npm test || true
EOF
fi

if [ "$HAS_RUST" = true ]; then
    cat >> lefthook.yml << 'EOF'
        cargo fmt -- --check && cargo clippy -- -D warnings && cargo test || true
EOF
fi

if [ "$HAS_PYTHON" = true ]; then
    cat >> lefthook.yml << 'EOF'
        ruff check . && mypy . && pytest || true
EOF
fi

cat >> lefthook.yml << 'EOF'
        echo "✅ Validation complete"
EOF

echo "✓ Created lefthook.yml"
echo ""

# Install commitlint if TypeScript project
if [ "$HAS_TS" = true ]; then
    if [ -f "package.json" ]; then
        echo "📦 Installing commitlint..."
        if command -v pnpm &> /dev/null; then
            pnpm add -D @commitlint/cli @commitlint/config-conventional
        else
            npm install -D @commitlint/cli @commitlint/config-conventional
        fi

        # Create commitlint.config.js if it doesn't exist
        if [ ! -f "commitlint.config.js" ]; then
            cat > commitlint.config.js << 'COMMITLINT'
export default {
  extends: ['@commitlint/config-conventional'],
  rules: {
    'type-enum': [2, 'always', [
      'feat', 'fix', 'docs', 'style', 'refactor',
      'perf', 'test', 'chore', 'ci', 'build', 'revert'
    ]],
    'header-max-length': [2, 'always', 100],
  },
}
COMMITLINT
            echo "✓ Created commitlint.config.js"
        fi
    fi
fi

# Install hooks
echo ""
echo "🔧 Installing Git hooks..."
lefthook install

echo ""
echo "✅ Lefthook setup complete!"
echo ""
echo "📋 What was configured:"
echo "  - commit-msg: Conventional commit validation"
echo "  - pre-commit: Format and lint staged files"
echo "  - pre-push: Full validation (lint, type-check, test)"
echo ""
echo "💡 Usage:"
echo "  - Hooks run automatically on git commit/push"
echo "  - Skip hooks: LEFTHOOK=0 git commit"
echo "  - Test hooks: lefthook run pre-commit"
echo ""
echo "📚 See: references/git-hooks.md for more details"
