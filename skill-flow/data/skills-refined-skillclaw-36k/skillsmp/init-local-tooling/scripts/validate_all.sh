#!/bin/bash

# Validate all: Run linting, formatting, type checking, tests, and builds
# Usage: ./validate_all.sh

set -e

echo "🔍 Running full project validation..."
echo ""

ERRORS=0

# Detect project types
HAS_TS=false
HAS_RUST=false
HAS_PYTHON=false
IS_MONOREPO=false

[ -f "package.json" ] || [ -f "tsconfig.json" ] && HAS_TS=true
[ -f "Cargo.toml" ] && HAS_RUST=true
[ -f "pyproject.toml" ] || [ -f "setup.py" ] && HAS_PYTHON=true
[ -f "nx.json" ] || [ -f "pnpm-workspace.yaml" ] && IS_MONOREPO=true

# TypeScript/JavaScript validation
if [ "$HAS_TS" = true ]; then
    echo "📘 TypeScript/JavaScript validation"
    echo "=================================="

    # Format check
    echo "  Format check..."
    if command -v biome &> /dev/null; then
        npx biome format --check . || { echo "  ❌ Format check failed"; ((ERRORS++)); }
    elif [ -f "node_modules/.bin/prettier" ]; then
        npx prettier --check . || { echo "  ❌ Format check failed"; ((ERRORS++)); }
    fi

    # Lint
    echo "  Linting..."
    if [ "$IS_MONOREPO" = true ] && command -v nx &> /dev/null; then
        npx nx run-many --target=lint --all || { echo "  ❌ Lint failed"; ((ERRORS++)); }
    elif command -v biome &> /dev/null; then
        npx biome lint . || { echo "  ❌ Lint failed"; ((ERRORS++)); }
    elif [ -f "node_modules/.bin/eslint" ]; then
        npx eslint . || { echo "  ❌ Lint failed"; ((ERRORS++)); }
    fi

    # Type check
    echo "  Type checking..."
    if [ "$IS_MONOREPO" = true ] && command -v nx &> /dev/null; then
        npx nx run-many --target=type-check --all || { echo "  ❌ Type check failed"; ((ERRORS++)); }
    elif [ -f "tsconfig.json" ]; then
        npx tsc --noEmit || { echo "  ❌ Type check failed"; ((ERRORS++)); }
    fi

    # Test
    echo "  Testing..."
    if [ "$IS_MONOREPO" = true ] && command -v nx &> /dev/null; then
        npx nx run-many --target=test --all || { echo "  ❌ Tests failed"; ((ERRORS++)); }
    elif [ -f "package.json" ]; then
        npm test || { echo "  ❌ Tests failed"; ((ERRORS++)); }
    fi

    # Build
    echo "  Building..."
    if [ "$IS_MONOREPO" = true ] && command -v nx &> /dev/null; then
        npx nx run-many --target=build --all || { echo "  ❌ Build failed"; ((ERRORS++)); }
    elif [ -f "package.json" ] && grep -q "\"build\"" package.json; then
        npm run build || { echo "  ❌ Build failed"; ((ERRORS++)); }
    fi

    echo ""
fi

# Rust validation
if [ "$HAS_RUST" = true ]; then
    echo "🦀 Rust validation"
    echo "=================="

    # Format check
    echo "  Format check..."
    cargo fmt -- --check || { echo "  ❌ Format check failed"; ((ERRORS++)); }

    # Clippy
    echo "  Clippy..."
    cargo clippy --all-targets --all-features -- -D warnings || { echo "  ❌ Clippy failed"; ((ERRORS++)); }

    # Test
    echo "  Testing..."
    if command -v cargo-nextest &> /dev/null; then
        cargo nextest run --all-features || { echo "  ❌ Tests failed"; ((ERRORS++)); }
    else
        cargo test --all-features || { echo "  ❌ Tests failed"; ((ERRORS++)); }
    fi

    # Build
    echo "  Building..."
    cargo build --release || { echo "  ❌ Build failed"; ((ERRORS++)); }

    # Deny check (if installed)
    if command -v cargo-deny &> /dev/null; then
        echo "  Security check..."
        cargo deny check || { echo "  ⚠️  Deny check failed (non-blocking)"; }
    fi

    echo ""
fi

# Python validation
if [ "$HAS_PYTHON" = true ]; then
    echo "🐍 Python validation"
    echo "===================="

    # Format check
    echo "  Format check..."
    if command -v ruff &> /dev/null; then
        ruff format --check . || { echo "  ❌ Format check failed"; ((ERRORS++)); }
    elif command -v black &> /dev/null; then
        black --check . || { echo "  ❌ Format check failed"; ((ERRORS++)); }
    fi

    # Lint
    echo "  Linting..."
    if command -v ruff &> /dev/null; then
        ruff check . || { echo "  ❌ Lint failed"; ((ERRORS++)); }
    fi

    # Type check
    echo "  Type checking..."
    if command -v mypy &> /dev/null; then
        mypy . || { echo "  ❌ Type check failed"; ((ERRORS++)); }
    fi

    # Test
    echo "  Testing..."
    if command -v pytest &> /dev/null; then
        pytest || { echo "  ❌ Tests failed"; ((ERRORS++)); }
    fi

    echo ""
fi

# Summary
echo "=================================="
if [ $ERRORS -eq 0 ]; then
    echo "✅ All validations passed!"
    echo ""
    exit 0
else
    echo "❌ Validation failed with $ERRORS error(s)"
    echo ""
    exit 1
fi
