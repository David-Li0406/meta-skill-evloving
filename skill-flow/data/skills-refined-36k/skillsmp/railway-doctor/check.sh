#!/bin/bash
# railway-doctor check - Pre-flight checks for Railway deployments
# Part of the agent-skills registry
# Compatible with: Claude Code, Codex CLI, OpenCode, Gemini CLI, Antigravity

set -e

# Source shared utilities (with fallback)
SKILLS_ROOT="${CLAUDE_PLUGIN_ROOT:-$HOME/.agent/skills}"
if [[ -f "$SKILLS_ROOT/lib/railway-common.sh" ]]; then
  source "$SKILLS_ROOT/lib/railway-common.sh"
else
  # Fallback color definitions
  RED='\033[0;31m'
  GREEN='\033[0;32m'
  YELLOW='\033[1;33m'
  NC='\033[0m'
  log_info() { echo -e "${GREEN}✓${NC} $*"; }
  log_warn() { echo -e "${YELLOW}⚠${NC} $*"; }
  log_error() { echo -e "${RED}✗${NC} $*"; }
fi

echo "🚂 Railway Doctor - Pre-flight Check"

ISSUES_FOUND=0

# ============================================================================
# Helper Functions (Railway official patterns)
# ============================================================================

_check_monorepo_root_directory() {
  local has_root_dir=false
  local is_shared_monorepo=false

  # Detect rootDirectory in railway.toml
  if [[ -f "railway.toml" ]] && grep -q "rootDirectory" railway.toml; then
    has_root_dir=true
  fi

  # Detect shared monorepo indicators
  if [[ -f "pnpm-workspace.yaml" ]] || \
     grep -q '"workspaces"' package.json 2>/dev/null || \
     [[ -f "turbo.json" ]] || \
     [[ -f "nx.json" ]]; then
    is_shared_monorepo=true
  fi

  # Check for Python monorepo with relative imports
  if [[ -f "pyproject.toml" ]] && grep -q '\.\./' pyproject.toml 2>/dev/null; then
    is_shared_monorepo=true
  fi

  if [[ "$has_root_dir" == "true" ]] && [[ "$is_shared_monorepo" == "true" ]]; then
    log_error "CRITICAL: rootDirectory set for shared monorepo"
    echo "   Shared packages won't be available in Railway"
    echo "   Fix: Remove rootDirectory, use custom build/start commands"
    echo "   See: https://railway.com/docs/monorepo"
    ISSUES_FOUND=$((ISSUES_FOUND + 1))
  else
    log_info "Monorepo configuration valid"
  fi
}

_check_command_conflict() {
  if [[ -f "railway.toml" ]]; then
    local build_cmd=$(grep "buildCommand" railway.toml 2>/dev/null | sed 's/.*= *"*\([^"]*\)"*$/\1/' | xargs)
    local start_cmd=$(grep "startCommand" railway.toml 2>/dev/null | sed 's/.*= *"*\([^"]*\)"*$/\1/' | xargs)

    if [[ -n "$build_cmd" ]] && [[ "$build_cmd" == "$start_cmd" ]]; then
      log_error "buildCommand and startCommand are identical"
      echo "   Railway requires different commands"
      echo "   Fix in railway.toml or Railway dashboard"
      ISSUES_FOUND=$((ISSUES_FOUND + 1))
    else
      log_info "Build/start commands are different"
    fi
  else
    log_info "No railway.toml found (using Railpack defaults)"
  fi
}

_check_package_manager_consistency() {
  if [[ -f "package.json" ]]; then
    local pkg_mgr=$(grep '"packageManager"' package.json 2>/dev/null | sed 's/.*"\(npm\|pnpm\|yarn\|bun\)@.*/\1/')
    if [[ -n "$pkg_mgr" ]]; then
      case "$pkg_mgr" in
        pnpm)
          if [[ ! -f "pnpm-lock.yaml" ]]; then
            log_warn "packageManager says pnpm but no pnpm-lock.yaml"
            echo "   Run: pnpm install"
          fi
          ;;
        yarn)
          if [[ ! -f "yarn.lock" ]]; then
            log_warn "packageManager says yarn but no yarn.lock"
            echo "   Run: yarn install"
          fi
          ;;
        *)
          log_info "Package manager: $pkg_mgr"
          ;;
      esac
    fi
  fi
}

# ============================================================================
# Validation Checks
# ============================================================================

# Check 1: Monorepo root directory validation
echo ""
echo "🔍 Checking monorepo configuration..."
_check_monorepo_root_directory

# Check 2: Build/start command conflict
echo ""
echo "🔍 Checking build configuration..."
_check_command_conflict

# Check 3: Package manager consistency
echo ""
echo "🔍 Checking package manager consistency..."
_check_package_manager_consistency

# ============================================================================
# Existing Validation Functions
# ============================================================================

# Check 4: Critical Python imports (Backend)
if [[ -f "backend/pyproject.toml" ]]; then
  echo ""
  echo "🐍 Checking Python imports (backend)..."
  cd backend

  # Ensure poetry env exists
  if ! poetry env info &>/dev/null; then
    echo "Installing Poetry environment..."
    poetry install --no-root --quiet
  fi

  # Test critical imports
  if poetry run python -c "
import sys
from pathlib import Path
sys.path.insert(0, str(Path.cwd()))

# Test critical imports that commonly break in Railway
try:
    from api.routers import health
    print('✅ All critical imports valid')
except ImportError as e:
    print(f'❌ Import will fail in Railway: {e}')
    sys.exit(1)
" 2>&1; then
    echo "✅ Backend imports validated"
  else
    echo "❌ ERROR: Backend imports will fail in Railway"
    echo "   Fix import paths or missing dependencies"
    ISSUES_FOUND=$((ISSUES_FOUND + 1))
  fi

  cd ..
fi

# Check 5: Lockfiles in sync
echo ""
echo "📦 Checking lockfiles..."

# Poetry lockfile
if [[ -f "backend/pyproject.toml" ]]; then
  cd backend
  if poetry check --lock 2>/dev/null; then
    echo "✅ backend/poetry.lock in sync"
  else
    echo "❌ ERROR: backend/poetry.lock out of sync"
    echo "   Run: cd backend && poetry lock --no-update"
    ISSUES_FOUND=$((ISSUES_FOUND + 1))
  fi
  cd ..
elif [[ -f "pyproject.toml" ]]; then
  if poetry check --lock 2>/dev/null; then
    echo "✅ poetry.lock in sync"
  else
    echo "❌ ERROR: poetry.lock out of sync"
    echo "   Run: poetry lock --no-update"
    ISSUES_FOUND=$((ISSUES_FOUND + 1))
  fi
fi

# pnpm lockfile
if [[ -f "frontend/package.json" ]]; then
  cd frontend
  if pnpm install --frozen-lockfile 2>/dev/null; then
    echo "✅ frontend/pnpm-lock.yaml in sync"
  else
    echo "❌ ERROR: frontend/pnpm-lock.yaml out of sync"
    echo "   Run: cd frontend && pnpm install"
    ISSUES_FOUND=$((ISSUES_FOUND + 1))
  fi
  cd ..
elif [[ -f "package.json" ]]; then
  if pnpm install --frozen-lockfile 2>/dev/null; then
    echo "✅ pnpm-lock.yaml in sync"
  else
    echo "❌ ERROR: pnpm-lock.yaml out of sync"
    echo "   Run: pnpm install"
    ISSUES_FOUND=$((ISSUES_FOUND + 1))
  fi
fi

# Check 6: Railway token and CLI
echo ""
echo "🔑 Checking Railway CLI and authentication..."
if command -v railway &>/dev/null; then
  if ! railway status &>/dev/null; then
    echo "⚠️  WARNING: Railway not authenticated"
    echo "   Run: railway login"
    ISSUES_FOUND=$((ISSUES_FOUND + 1))
  else
    log_info "Railway CLI authenticated"
  fi
else
  echo "ℹ️  Railway CLI not installed (skipping Railway-specific checks)"
  echo "   Install: npm install -g @railway/cli"
fi

# Check 7: Required environment variables (if Railway CLI available)
if command -v railway &>/dev/null && railway status &>/dev/null; then
  echo ""
  echo "🔑 Checking Railway environment variables..."

  REQUIRED_VARS=(
    "DATABASE_URL"
    "SUPABASE_URL"
    "CLERK_SECRET_KEY"
  )

  for VAR in "${REQUIRED_VARS[@]}"; do
    if railway variables 2>/dev/null | grep -q "^$VAR"; then
      echo "✅ $VAR set"
    else
      echo "⚠️  WARNING: $VAR not set in Railway environment"
      echo "   Set via: railway variables set $VAR=<value>"
      ISSUES_FOUND=$((ISSUES_FOUND + 1))
    fi
  done
fi

# Check 8: Railway configuration file
echo ""
echo "⚙️  Checking Railway configuration..."

if [[ -f "railway.toml" ]] || [[ -f "railway.json" ]]; then
  echo "✅ Railway config file found"
else
  echo "ℹ️  No railway.toml or railway.json found"
  echo "   Consider adding for build configuration"
fi

echo ""
echo "═══════════════════════════════════════"
if [[ $ISSUES_FOUND -eq 0 ]]; then
  echo "✅ All pre-flight checks passed!"
  echo "   Safe to deploy to Railway"
  exit 0
else
  echo "❌ Found $ISSUES_FOUND issue(s) - deployment will likely fail"
  echo ""
  echo "Fix issues before deploying to Railway"
  echo "Or run: ~/.agent/skills/railway-doctor/fix.sh"
  exit 1
fi
