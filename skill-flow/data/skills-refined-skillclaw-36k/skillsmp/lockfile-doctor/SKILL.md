---
name: lockfile-doctor
description: Check and fix lockfile drift across Poetry (Python) and pnpm (Node.js) projects.
---

# lockfile-doctor

## Description

Check and fix lockfile drift across Poetry (Python) and pnpm (Node.js) projects.

**Use when**:
- Dependency manifest changed (pyproject.toml, package.json) but lockfile not updated
- CI fails with lockfile errors ("poetry.lock out of sync", "frozen lockfile mismatch")
- User says "fix lockfile", "update lockfile", "lockfile out of sync", "regenerate lock"

**Problem solved**: Eliminates "Add dependency → Forget lockfile → CI fails" pattern (9/69 toil commits, 13% of analyzed toil).

## Auto-Activation

This skill activates when:
- User mentions lockfile issues ("lockfile", "poetry.lock", "pnpm-lock.yaml")
- CI error messages contain lockfile-related failures
- Dependency manifests modified without corresponding lockfile updates

## Implementation

The skill checks and fixes lockfiles for both Python (Poetry) and Node.js (pnpm) projects.

### Check Script

```bash
#!/bin/bash
# ~/.agent/skills/lockfile-doctor/check.sh

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
    if git diff --cached --name-only | grep -q "pyproject.toml"; then
      if ! git diff --cached --name-only | grep -q "poetry.lock"; then
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
    if git diff --cached --name-only | grep -q "package.json"; then
      if ! git diff --cached --name-only | grep -q "pnpm-lock.yaml"; then
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
  echo "Run: lockfile-doctor fix    # to auto-fix all issues"
  exit 1
fi
```

### Fix Script

```bash
#!/bin/bash
# ~/.agent/skills/lockfile-doctor/fix.sh

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
  if git diff --cached --name-only | grep -q "pyproject.toml"; then
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
  if git diff --cached --name-only | grep -q "package.json"; then
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
```

## Usage Examples

### Check lockfiles before commit
```bash
lockfile-doctor check
```

### Auto-fix all lockfile issues
```bash
lockfile-doctor fix
```

### Agent workflow integration
When agent detects dependency manifest changes:
1. Run `lockfile-doctor check` to verify sync
2. If issues found, run `lockfile-doctor fix` to auto-regenerate
3. Stage lockfiles with manifest changes
4. Commit together

## Integration Points

### Pre-Commit Hook (Optional)
Add soft warning to `.git/hooks/pre-commit`:
```bash
if git diff --cached --name-only | grep -E 'pyproject.toml|package.json'; then
  ~/.agent/skills/lockfile-doctor/check.sh || {
    echo ""
    echo "💡 Tip: Run 'lockfile-doctor fix' to auto-fix"
  }
fi
```

### CI Workflow
Add fast-fail check to CI:
```yaml
- name: Check Lockfiles
  run: ~/.agent/skills/lockfile-doctor/check.sh
```

### sync-feature-branch Skill Enhancement
Modify sync-feature-branch to auto-run lockfile-doctor:
```markdown
Before committing:
1. Run lockfile-doctor check
2. If fails, run lockfile-doctor fix
3. Stage updated lockfiles
4. Commit with lockfiles included
```

## Cross-Repo Deployment

This skill deploys to `~/.agent/skills/` and works across:
- ✅ All repos (prime-radiant-ai, affordabot, any future repos)
- ✅ All AI agents (Claude Code, Codex CLI, Antigravity)
- ✅ All VMs (shared via Universal Skills MCP)

## Success Metrics

**Baseline**: 9 commits (13% of toil) wasted on lockfile drift
**Target**: <2 commits per 60-commit cycle
**Impact**: ~1 hour/month saved

## Notes

**Design Philosophy**:
- Non-blocking warnings (not hard failures) - CI enforces
- Auto-fix capability (not just detection)
- Cross-platform (Poetry + pnpm)
- Agent-friendly (clear messages, actionable commands)

**Why not pre-commit hook?**
- Multi-agent context: hooks get bypassed with --no-verify
- Skills provide flexibility: agents can invoke explicitly when needed
- CI provides hard enforcement: lockfile-doctor in CI catches issues

**Complementary with**:
- CI lockfile validation (hard enforcement)
- sync-feature-branch skill (workflow integration)
