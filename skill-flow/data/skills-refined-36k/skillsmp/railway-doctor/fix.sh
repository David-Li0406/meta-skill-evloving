#!/bin/bash
# railway-doctor fix - Auto-fix common Railway deployment issues

set -e

echo "🔧 Railway Doctor - Fixing issues..."

FIXED=0

# Fix 1: Regenerate lockfiles
echo ""
echo "📦 Fixing lockfiles..."

# Poetry
if [[ -f "backend/pyproject.toml" ]]; then
  cd backend
  if ! poetry check --lock 2>/dev/null; then
    echo "Regenerating backend/poetry.lock..."
    poetry lock --no-update
    git add poetry.lock
    echo "✅ backend/poetry.lock fixed"
    FIXED=$((FIXED + 1))
  else
    echo "✅ backend/poetry.lock already in sync"
  fi
  cd ..
elif [[ -f "pyproject.toml" ]]; then
  if ! poetry check --lock 2>/dev/null; then
    echo "Regenerating poetry.lock..."
    poetry lock --no-update
    git add poetry.lock
    echo "✅ poetry.lock fixed"
    FIXED=$((FIXED + 1))
  else
    echo "✅ poetry.lock already in sync"
  fi
fi

# pnpm
if [[ -f "frontend/package.json" ]]; then
  cd frontend
  if ! pnpm install --frozen-lockfile 2>/dev/null; then
    echo "Regenerating frontend/pnpm-lock.yaml..."
    pnpm install
    git add pnpm-lock.yaml
    echo "✅ frontend/pnpm-lock.yaml fixed"
    FIXED=$((FIXED + 1))
  else
    echo "✅ frontend/pnpm-lock.yaml already in sync"
  fi
  cd ..
elif [[ -f "package.json" ]]; then
  if ! pnpm install --frozen-lockfile 2>/dev/null; then
    echo "Regenerating pnpm-lock.yaml..."
    pnpm install
    git add pnpm-lock.yaml
    echo "✅ pnpm-lock.yaml fixed"
    FIXED=$((FIXED + 1))
  else
    echo "✅ pnpm-lock.yaml already in sync"
  fi
fi

# Fix 2: Import issues - can't auto-fix, only provide guidance
if [[ -f "backend/pyproject.toml" ]]; then
  echo ""
  echo "🐍 Checking for import issues..."
  cd backend

  if ! poetry run python -c "
import sys
from pathlib import Path
sys.path.insert(0, str(Path.cwd()))
from api.routers import health
" 2>/dev/null; then
    echo "⚠️  Cannot auto-fix: Import errors detected"
    echo ""
    echo "   Manual fixes needed:"
    echo "   1. Check import paths in Railway match local"
    echo "   2. Verify all dependencies in pyproject.toml"
    echo "   3. Test imports: cd backend && poetry run python -c 'from api.routers import health'"
    echo ""
  else
    echo "✅ No import errors detected"
  fi
  cd ..
fi

# Fix 3: Environment variables - can't auto-fix, only guide
if command -v railway &>/dev/null; then
  echo ""
  echo "🔑 Environment variable guidance..."

  MISSING_VARS=()
  REQUIRED_VARS=(
    "DATABASE_URL"
    "SUPABASE_URL"
    "CLERK_SECRET_KEY"
  )

  for VAR in "${REQUIRED_VARS[@]}"; do
    if ! railway variables 2>/dev/null | grep -q "^$VAR"; then
      MISSING_VARS+=("$VAR")
    fi
  done

  if [[ ${#MISSING_VARS[@]} -gt 0 ]]; then
    echo "⚠️  Missing environment variables in Railway:"
    for VAR in "${MISSING_VARS[@]}"; do
      echo "   - $VAR"
    done
    echo ""
    echo "   Set via Railway dashboard or CLI:"
    echo "   railway variables set VARIABLE_NAME=value"
  else
    echo "✅ All required environment variables set"
  fi
fi

echo ""
echo "═══════════════════════════════════════"
if [[ $FIXED -eq 0 ]]; then
  echo "ℹ️  No auto-fixable issues found"
  echo ""
  echo "   If issues remain, check error messages above for manual fixes"
else
  echo "✅ Fixed $FIXED issue(s)"
  echo ""
  echo "Re-run railway-doctor check to verify all issues resolved"
fi
