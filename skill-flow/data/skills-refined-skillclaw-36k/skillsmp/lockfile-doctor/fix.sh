#!/bin/bash
# lockfile-doctor fix - Auto-regenerate lockfiles to match manifests

set -e

echo "🔧 Lockfile Doctor - Fixing lockfiles..."

FIXED=0

# Fix Poetry lockfile
if [[ -f "pyproject.toml" ]]; then
  echo ""
  echo "📦 Fixing Poetry lockfile..."

  # Regenerate poetry.lock
  echo "Running: poetry lock --no-update"
  poetry lock --no-update

  # Stage if pyproject.toml is staged
  if git diff --cached --name-only 2>/dev/null | grep -q "pyproject.toml"; then
    echo "Staging: poetry.lock"
    git add poetry.lock
  fi

  echo "✅ poetry.lock regenerated and synced"
  FIXED=$((FIXED + 1))
fi

# Fix pnpm lockfile
if [[ -f "package.json" ]]; then
  echo ""
  echo "📦 Fixing pnpm lockfile..."

  # Regenerate pnpm-lock.yaml
  echo "Running: pnpm install"
  pnpm install

  # Stage if package.json is staged
  if git diff --cached --name-only 2>/dev/null | grep -q "package.json"; then
    echo "Staging: pnpm-lock.yaml"
    git add pnpm-lock.yaml
  fi

  echo "✅ pnpm-lock.yaml regenerated and synced"
  FIXED=$((FIXED + 1))
fi

echo ""
if [[ $FIXED -eq 0 ]]; then
  echo "ℹ️  No lockfiles found to fix"
else
  echo "✅ Fixed $FIXED lockfile(s)"
  echo ""
  echo "Next: Commit changes with lockfiles included"
fi
