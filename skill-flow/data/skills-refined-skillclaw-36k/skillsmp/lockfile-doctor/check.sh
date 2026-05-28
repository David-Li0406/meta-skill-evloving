#!/bin/bash
# lockfile-doctor check - Verify lockfiles are in sync with manifests

set -e

echo "🔍 Lockfile Doctor - Checking lockfiles..."

ISSUES_FOUND=0

# Check Poetry lockfile (Python)
if [[ -f "pyproject.toml" ]]; then
  echo ""
  echo "📦 Checking Poetry lockfile..."

  if [[ ! -f "poetry.lock" ]]; then
    echo "❌ ERROR: poetry.lock missing but pyproject.toml exists"
    echo "   Run: poetry lock --no-update"
    ISSUES_FOUND=$((ISSUES_FOUND + 1))
  else
    # Check if poetry.lock is in sync
    if poetry check --lock 2>/dev/null; then
      echo "✅ poetry.lock is in sync with pyproject.toml"
    else
      echo "❌ ERROR: poetry.lock out of sync with pyproject.toml"
      echo "   Run: poetry lock --no-update"
      ISSUES_FOUND=$((ISSUES_FOUND + 1))
    fi

    # Check if lockfile is staged when manifest changed
    if git diff --cached --name-only 2>/dev/null | grep -q "pyproject.toml"; then
      if ! git diff --cached --name-only 2>/dev/null | grep -q "poetry.lock"; then
        echo "⚠️  WARNING: pyproject.toml staged but poetry.lock not staged"
        echo "   Stage lockfile: git add poetry.lock"
        ISSUES_FOUND=$((ISSUES_FOUND + 1))
      fi
    fi
  fi
fi

# Check pnpm lockfile (Node.js)
if [[ -f "package.json" ]]; then
  echo ""
  echo "📦 Checking pnpm lockfile..."

  if [[ ! -f "pnpm-lock.yaml" ]]; then
    echo "❌ ERROR: pnpm-lock.yaml missing but package.json exists"
    echo "   Run: pnpm install"
    ISSUES_FOUND=$((ISSUES_FOUND + 1))
  else
    # Check if pnpm-lock.yaml is in sync
    if pnpm install --frozen-lockfile 2>/dev/null; then
      echo "✅ pnpm-lock.yaml is in sync with package.json"
    else
      echo "❌ ERROR: pnpm-lock.yaml out of sync with package.json"
      echo "   Run: pnpm install"
      ISSUES_FOUND=$((ISSUES_FOUND + 1))
    fi

    # Check if lockfile is staged when manifest changed
    if git diff --cached --name-only 2>/dev/null | grep -q "package.json"; then
      if ! git diff --cached --name-only 2>/dev/null | grep -q "pnpm-lock.yaml"; then
        echo "⚠️  WARNING: package.json staged but pnpm-lock.yaml not staged"
        echo "   Stage lockfile: git add pnpm-lock.yaml"
        ISSUES_FOUND=$((ISSUES_FOUND + 1))
      fi
    fi
  fi
fi

echo ""
if [[ $ISSUES_FOUND -eq 0 ]]; then
  echo "✅ All lockfiles healthy!"
  exit 0
else
  echo "❌ Found $ISSUES_FOUND lockfile issue(s)"
  echo ""
  echo "Run: ~/.agent/skills/lockfile-doctor/fix.sh    # to auto-fix all issues"
  exit 1
fi
