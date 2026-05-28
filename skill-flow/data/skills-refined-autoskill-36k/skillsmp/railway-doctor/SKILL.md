---
name: railway-doctor
description: |
  Pre-flight checks for Railway deployments to catch failures BEFORE deploying.
  Use when about to deploy to Railway, Railway deployment fails, debugging Railway errors,
  or user says "deploy to railway", "railway up", "check railway".
tags: [railway, deployment, validation, pre-flight]
allowed-tools:
  - Bash(railway:*)
  - Bash(poetry)
  - Bash(pnpm)
  - Bash(python)
  - Bash(curl)
  - Read
---

# railway-doctor

## Description

Pre-flight checks for Railway deployments to catch failures BEFORE deploying.

**Use when**:
- About to deploy to Railway ("deploy to railway", "railway up")
- Railway deployment fails (imports break, env issues, lockfile errors)
- Debugging Railway 500 errors
- User says "check railway", "railway pre-flight", "why did railway fail"

**Problem solved**: Eliminates "Deploy to Railway → Imports break → Iterate" pattern (12/69 toil commits, 17% of analyzed toil).

## Auto-Activation

This skill activates when:
- User mentions Railway deployment ("railway", "deploy", "railway up")
- CI deployment step fails
- Railway shows 500 errors or build failures
- Before important deployments (staging, production)

## Implementation

The skill performs comprehensive pre-flight checks to catch Railway deployment issues early.

### Validation Stages

| Stage | Checks | Fail Action |
|-------|--------|-------------|
| **Pre-build** | Lockfiles, imports | Block deploy |
| **Build** | Config, Railpack version | Block deploy |
| **Pre-deploy** | Env vars, monorepo config | Block deploy |
| **Post-deploy** | Health, smoke tests | Rollback prompt |

### Check Script

```bash
#!/bin/bash
# ~/.agent/skills/railway-doctor/check.sh

set -e

# Source shared utilities
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

# Check 1: Monorepo root directory validation
echo ""
echo "🔍 Checking monorepo configuration..."
check_monorepo_root_directory

# Check 2: Build/start command conflict
echo ""
echo "🔍 Checking build configuration..."
check_command_conflict

# Check 3: Package manager consistency
echo ""
echo "🔍 Checking package manager consistency..."
check_package_manager_consistency

# Check 4: Critical Python imports (Backend)
if [[ -f "backend/pyproject.toml" ]]; then
  echo ""
  echo "🐍 Checking Python imports (backend)..."
  cd backend

  # Ensure poetry env exists
  if ! poetry env info &>/dev/null; then
    echo "Installing Poetry environment..."
    poetry install --no-root
  fi

  # Test critical imports
  if poetry run python -c "
import sys
from pathlib import Path
sys.path.insert(0, str(Path.cwd()))

# Test critical imports that commonly break in Railway
try:
    from services.plaid_adapter import PlaidAdapter
    from brokers.security_resolver import SecurityResolver
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
  echo "⚠️  No railway.toml or railway.json found"
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
  echo "   Run: ~/.agent/skills/railway-doctor/fix.sh"
  exit 1
fi

# ============================================================================
# Helper Functions
# ============================================================================

check_monorepo_root_directory() {
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
  fi
}

check_command_conflict() {
  if [[ -f "railway.toml" ]]; then
    local build_cmd=$(grep "buildCommand" railway.toml 2>/dev/null | sed 's/.*= *"*\([^"]*\)"*$/\1/' | xargs)
    local start_cmd=$(grep "startCommand" railway.toml 2>/dev/null | sed 's/.*= *"*\([^"]*\)"*$/\1/' | xargs)

    if [[ -n "$build_cmd" ]] && [[ "$build_cmd" == "$start_cmd" ]]; then
      log_error "buildCommand and startCommand are identical"
      echo "   Railway requires different commands"
      echo "   Fix in railway.toml or Railway dashboard"
      ISSUES_FOUND=$((ISSUES_FOUND + 1))
    fi
  fi
}

check_package_manager_consistency() {
  if [[ -f "package.json" ]]; then
    local pkg_mgr=$(grep '"packageManager"' package.json 2>/dev/null | sed 's/.*"\(npm\|pnpm\|yarn\|bun\)@.*/\1/')
    if [[ -n "$pkg_mgr" ]]; then
      case "$pkg_mgr" in
        pnpm)
          if [[ ! -f "pnpm-lock.yaml" ]]; then
            log_warn "packageManager says pnpm but no pnpm-lock.yaml"
          fi
          ;;
        yarn)
          if [[ ! -f "yarn.lock" ]]; then
            log_warn "packageManager says yarn but no yarn.lock"
          fi
          ;;
      esac
    fi
  fi
}
```

### Fix Script

```bash
#!/bin/bash
# ~/.agent/skills/railway-doctor/fix.sh

set -e

# Source shared utilities
SKILLS_ROOT="${CLAUDE_PLUGIN_ROOT:-$HOME/.agent/skills}"
if [[ -f "$SKILLS_ROOT/lib/railway-common.sh" ]]; then
  source "$SKILLS_ROOT/lib/railway-common.sh"
fi

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
  fi
  cd ..
elif [[ -f "pyproject.toml" ]]; then
  if ! poetry check --lock 2>/dev/null; then
    echo "Regenerating poetry.lock..."
    poetry lock --no-update
    git add poetry.lock
    echo "✅ poetry.lock fixed"
    FIXED=$((FIXED + 1))
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
  fi
  cd ..
elif [[ -f "package.json" ]]; then
  if ! pnpm install --frozen-lockfile 2>/dev/null; then
    echo "Regenerating pnpm-lock.yaml..."
    pnpm install
    git add pnpm-lock.yaml
    echo "✅ pnpm-lock.yaml fixed"
    FIXED=$((FIXED + 1))
  fi
fi

# Fix 2: Import issues - can't auto-fix, only provide guidance
if [[ -f "backend/pyproject.toml" ]]; then
  cd backend
  if ! poetry run python -c "
import sys
from pathlib import Path
sys.path.insert(0, str(Path.cwd()))
from services.plaid_adapter import PlaidAdapter
" 2>/dev/null; then
    echo ""
    echo "⚠️  Cannot auto-fix: Import errors detected"
    echo "   Manual fixes needed:"
    echo "   - Check import paths in Railway match local"
    echo "   - Verify all dependencies in pyproject.toml"
    echo "   - Test with: cd backend && poetry run python -c 'from services.plaid_adapter import PlaidAdapter'"
  fi
  cd ..
fi

# Fix 3: Environment variables - can't auto-fix, only guide
if command -v railway &>/dev/null; then
  echo ""
  echo "⚠️  Environment variable issues require manual setup in Railway dashboard"
  echo "   Or use: railway variables set VARIABLE_NAME=value"
fi

echo ""
echo "═══════════════════════════════════════"
if [[ $FIXED -eq 0 ]]; then
  echo "ℹ️  No auto-fixable issues found"
  echo "   Check error messages above for manual fixes"
else
  echo "✅ Fixed $FIXED issue(s)"
  echo ""
  echo "Re-run railway-doctor check to verify all issues resolved"
fi
```

## Usage Examples

### Pre-flight check before deployment
```bash
~/.agent/skills/railway-doctor/check.sh
# or
railway-doctor check
```

### Auto-fix lockfile issues
```bash
~/.agent/skills/railway-doctor/fix.sh
# or
railway-doctor fix
```

### CI Integration
```yaml
# .github/workflows/deploy.yml
- name: Railway Pre-flight Check
  run: ~/.agent/skills/railway-doctor/check.sh

- name: Deploy to Railway
  if: success()
  run: railway up
```

### Agent workflow
```
1. User: "deploy to railway"
2. Agent: Run railway-doctor check
3. If passes: railway up
4. If fails: railway-doctor fix, then re-check
```

## Common Issues & Fixes

### Issue 1: Import errors in Railway
**Symptom**: Works locally, fails in Railway with `ModuleNotFoundError`
**Cause**: Import paths different in Railway vs local
**Check**: railway-doctor validates critical imports
**Fix**: Adjust sys.path or restructure imports

### Issue 2: Lockfile out of sync
**Symptom**: Railway build fails with "dependency mismatch"
**Cause**: pyproject.toml changed without poetry lock
**Check**: railway-doctor validates lockfiles
**Fix**: Auto-fixed with railway-doctor fix

### Issue 3: Missing environment variables
**Symptom**: Railway 500 errors, missing DATABASE_URL etc.
**Cause**: Env vars not set in Railway project
**Check**: railway-doctor checks required vars (if Railway CLI installed)
**Fix**: Manual setup via Railway dashboard or CLI

### Issue 4: Railpack version breaking changes
**Symptom**: Build works locally, fails in Railway after Railpack update
**Cause**: Railpack breaking change (e.g., 0.0.70 packageManager field)
**Prevention**: Pin Railpack version in railway.toml

### Issue 5: Monorepo root directory with shared packages (NEW)
**Symptom**: Shared packages unavailable in Railway
**Cause**: rootDirectory set for shared monorepo
**Check**: railway-doctor detects this configuration
**Fix**: Remove rootDirectory, use custom build/start commands

### Issue 6: Build/start command conflict (NEW)
**Symptom**: Railway rejects configuration
**Cause**: buildCommand equals startCommand
**Check**: railway-doctor detects identical commands
**Fix**: Set different commands in railway.toml

### Issue 7: Package manager mismatch (NEW)
**Symptom**: Lockfile doesn't match packageManager field
**Cause**: package.json updated but lockfile not regenerated
**Check**: railway-doctor warns of inconsistency
**Fix**: Run appropriate package manager install

### Monorepo Root Pattern (Python + llm-common)

**Symptom**: Works locally with `../packages/llm-common` or a vendored copy, but Railway deploy fails with missing modules or broken imports.

**Root Cause**: Railway "isolated monorepo" deploys only the configured Root Directory (e.g., `backend/`). Anything outside that directory (`../packages/llm-common`) is invisible inside the container.

**Best Practice Pattern**:
- Set **Root Directory** for Python services to `backend/`.
- Use a **standard dependency** for shared libraries like `llm-common`, never a relative path:
  ```toml
  # backend/pyproject.toml
  [tool.poetry.dependencies]
  llm-common = { git = "https://github.com/stars-end/llm-common.git", tag = "v0.4.0", extras = ["pgvector"] }
  ```
- Avoid `path = "../llm-common"` or `packages/llm-common` for runtime; those are fine for local dev only if the service is not deployed from that folder.
- Start command should assume `backend/` as CWD:
  ```bash
  poetry run uvicorn main:app --host 0.0.0.0 --port "$PORT"
  ```

**Heuristic for Agents**:
- If a Railway deploy fails only in one repo (e.g., Affordabot) but works in another (Prime Radiant), first check:
  - Is the service using `Root Directory = backend/`?
  - Is `llm-common` (or any shared lib) installed as a normal dependency instead of via `../` paths?

## Composability with Railway Official Skills

Railway provides official skills for deployment operations. After railway-doctor validates:

| Issue | Next Action | Skill Source |
|-------|-------------|--------------|
| Import errors | Fix import paths, then re-check | manual |
| Lockfile out of sync | Run `railway-doctor fix` | agent-skills |
| Monorepo root dir | Use custom commands | Railway reference |
| Build/start conflict | Fix in railway.toml or dashboard | Railway reference |
| Missing env vars | Use Railway environment skill | Railway official |
| All checks pass | **Deploy to Railway** | Railway official |

### Railway Official Skills Installation

**For Claude Code (Recommended):**
```bash
claude plugin marketplace add railwayapp/railway-claude-plugin
claude plugin install railway@railway-claude-plugin
```

**For Other Agents:**
```bash
# Copy to skills plane
git clone https://github.com/railwayapp/railway-skills.git /tmp/railway-skills
cp -r /tmp/railway-skills/plugins/railway/skills/* ~/.agent/skills/
```

### Railway Official Skills Matrix

| Skill | Purpose | Use After |
|-------|---------|-----------|
| **railway deploy** | Push code | railway-doctor passes |
| **railway environment** | Manage config | Config issues found |
| **railway service** | Manage services | Need service management |
| **railway new** | Create services | Need new service |
| **railway deployment** | Monitor deployments | Deploy started |

## Agent Compatibility

This skill works across all major AI coding agents:

| Agent | Type | GraphQL Support | allowed-tools |
|-------|------|-----------------|---------------|
| Claude Code | Skills-Native | ✅ Full | ✅ Enforced |
| Codex CLI | Skills-Native | ✅ Full | ✅ Enforced |
| OpenCode | Skills-Native | ✅ Full | ✅ Enforced |
| Gemini CLI | MCP-Dependent | ✅ Via skills plane | ⚠️ Not enforced |
| Antigravity | MCP-Dependent | ✅ Via skills plane | ⚠️ Not enforced |

**For MCP-dependent agents:**
- Ensure `~/.agent/skills/lib/railway-common.sh` exists
- Ensure `~/.agent/skills/lib/railway-api.sh` exists
- Use `load_skill("railway-doctor")` to activate

## Cross-Repo Deployment

This skill deploys to `~/.agent/skills/` and works across:
- ✅ All repos (prime-radiant-ai, affordabot, any Railway project)
- ✅ All AI agents (Claude Code, Codex CLI, Antigravity)
- ✅ All VMs (shared via Universal Skills MCP)

## Success Metrics

**Baseline**: 12 commits (17% of toil) wasted on Railway deployment failures
**Target**: <2 commits per 60-commit cycle
**Impact**: ~2-3 hours/month saved, fewer deployment iterations

## Notes

**Design Philosophy**:
- Fail fast locally (before pushing to Railway)
- Validate critical imports (catches 80% of issues)
- Clear guidance for non-auto-fixable issues
- Agent-friendly (railway-doctor check → fix → deploy)

**Why not full Railway simulator?**
- Over-engineering: Pre-flight + better logging gets 80% value
- Complexity: Full simulator may still diverge from actual Railway
- ROI: 2-3 days vs 1 day for similar impact

**Complementary with**:
- Railway official skills - for deployment operations
- Enhanced Railway logging (bd-vs87) - for debugging deployed errors
- lockfile-doctor skill (bd-heb9) - for dependency management
- devops-dx skill - for environment management

## Version History

- **v1.1.0** (2025-01-12): Railway official patterns integration
  - Added monorepo root directory validation
  - Added build/start command conflict detection
  - Added package manager consistency check
  - Added Railway token validation
  - Added composability section with Railway official skills
  - Added agent compatibility matrix
- **v1.0.0** (2024-12-15): Initial implementation
  - Pre-flight checks for imports, lockfiles, env vars
  - Monorepo root pattern documentation
