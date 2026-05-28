**Skill**: [semantic-release](../SKILL.md)

# Authentication for semantic-release

> **2025-12-19 Update**: HTTPS-first authentication is now the primary method. SSH is retained as reference/fallback only. See [GitHub Multi-Account Authentication ADR](https://github.com/terrylica/claude-config/blob/main/docs/adr/2025-12-17-github-multi-account-authentication.md).

## Authentication Priority Order (HTTPS-First)

semantic-release requires authentication for:

1. **Git operations** (push tags, commit changelog) → HTTPS with credential helper
2. **GitHub API** (create releases, update issues) → GH_TOKEN from mise [env]

**Check in this order**:

### Priority 1: HTTPS + Token (PRIMARY) ✅

**Check first**: Verify HTTPS remote and GH_TOKEN

**Verify setup**:

```bash
# Check git remote uses HTTPS
git remote -v
# Should show: https://github.com/username/repo.git

# Verify GH_TOKEN is set (via mise [env])
gh api user --jq '.login'
# Should show: expected account for this directory

# Convert SSH remote to HTTPS if needed
git-ssh-to-https
```

**Why HTTPS-first**:

- ✅ No port 22 blocking issues (uses port 443)
- ✅ No ProxyCommand flakiness in subprocesses
- ✅ No ControlMaster caching bugs
- ✅ No ssh-add key loading required
- ✅ semantic-release just works

### Priority 2: SSH (FALLBACK) ⚠️

**Only use SSH if HTTPS is blocked**. Most networks allow HTTPS (port 443).

**Verify SSH setup** (if needed):

```bash
# Test SSH authentication
ssh -T git@github.com
# Should show: "Hi username! You've successfully authenticated..."
```

**Context-aware SSH** (smart dynamic structure):

```ssh-config
# ~/.ssh/config - Dynamic key selection based on directory patterns
Match host github.com exec "echo $PWD | grep -q '/pattern1'"
    IdentityFile ~/.ssh/id_ed25519_account1

Match host github.com exec "echo $PWD | grep -q '/pattern2'"
    IdentityFile ~/.ssh/id_ed25519_account2

Match host github.com exec "echo $PWD | grep -q '/pattern3'"
    IdentityFile ~/.ssh/id_ed25519_account3
```

**This smart structure automatically**:

- ✅ Selects correct GitHub account based on directory path
- ✅ Eliminates manual key management
- ✅ Prevents authentication failures (proper config = no failures)
- ✅ Works for all git operations (push, pull, clone)

**Benefits**:

- ✅ Automatic per-directory authentication
- ✅ No manual credential management
- ✅ Handles all git push/pull/tag operations
- ✅ Already configured and working
- ✅ No setup needed if properly configured

**Setup** (if not working):

```bash
# Verify key exists
ls -la ~/.ssh/id_ed25519*

# Test SSH connection
ssh -T git@github.com

# Check SSH config
cat ~/.ssh/config | grep -A 5 "github.com"

# Add key to ssh-agent if needed
ssh-add ~/.ssh/id_ed25519_yourkey
```

### Priority 2: GitHub CLI Web Authentication (API Operations) ✅

**Secondary check**: GitHub API authentication for creating releases

**Verify gh CLI**:

```bash
# Check gh CLI is authenticated
gh auth status
# Should show: ✓ Logged in to github.com
```

**Integration with npm scripts** (package.json):

```json
"scripts": {
  "release": "/usr/bin/env bash -c 'GITHUB_TOKEN=$(gh auth token) semantic-release'",
  "release:dry": "/usr/bin/env bash -c 'GITHUB_TOKEN=$(gh auth token) semantic-release --dry-run'"
}
```

**Note**: The `/usr/bin/env bash -c` wrapper is required for macOS where zsh is the default shell. NPM runs scripts through the system shell, and zsh fails on `$(...)` substitution patterns.

**Note**: `gh auth token` retrieves credentials from gh CLI's web authentication - **never create manual tokens**.

**Benefits**:

- ✅ Web-based authentication via system keyring
- ✅ Works with multiple GitHub accounts
- ✅ No manual credential creation needed
- ✅ Complements SSH (doesn't replace it)

**Setup** (if not authenticated):

```bash
gh auth login
# Select: GitHub.com → HTTPS → Login with browser
# Required scopes: repo, workflow

# Web-based authentication only!
```

**If gh CLI authentication fails**, simply re-run `gh auth login` with web browser authentication.

---

## How They Work Together

**For local development (`npm run release`)**:

1. **SSH keys** → Handle git operations (push tags, commit changelog)
2. **gh CLI** → Handle GitHub API (create releases, close issues)

```
SSH Keys                 GitHub CLI
    ↓                        ↓
Git Push Tags          Create GitHub Release
Commit Changelog       Update Issues/PRs
                       Post Release Notes
```

**Both are required and complementary** - not alternatives!

---

## Troubleshooting

For authentication issues, see [Troubleshooting](./troubleshooting.md#authentication-issues).

Common issues:
- Permission denied (publickey)
- No GitHub token specified
- GitHub account mismatch
- ControlMaster cache (multi-account setups)

---

## Authentication Architecture

```
┌─────────────────────────────────────────────┐
│ Local Development (npm run release)        │
├─────────────────────────────────────────────┤
│ 1. SSH Keys (git operations)               │
│    ~/.ssh/id_ed25519_yourkey               │
│    → git push, git tag                     │
│                                             │
│ 2. gh CLI (GitHub API)                     │
│    Web authentication (gh auth login)      │
│    → create release, update issues         │
│    ⚠️  AVOID manual tokens                 │
└─────────────────────────────────────────────┘

┌─────────────────────────────────────────────┐
│ GitHub Actions (automated CI/CD)            │
├─────────────────────────────────────────────┤
│ 1. GITHUB_TOKEN secret (automatic)         │
│    ${{ secrets.GITHUB_TOKEN }}             │
│    → Uses HTTPS for everything             │
│    → SSH not needed in CI/CD               │
│    → No manual setup required              │
└─────────────────────────────────────────────┘
```

---

## Best Practices

### ✅ DO

1. **Use SSH keys with smart config** for git operations (automatic account selection)
2. **Use context-aware Match directives** for directory-based authentication
3. **Use `gh auth login` web authentication** for GitHub API
4. **Let GitHub Actions** use automatic `GITHUB_TOKEN`
5. **Trust the smart SSH config** - it won't fail with proper directory-based setup

### ❌ DON'T

1. **Replace SSH with HTTPS** - SSH with smart config is superior
2. **Create manual tokens** - ⚠️ AVOID - Use `gh auth login` web authentication instead
3. **Hard-code tokens or credentials** in scripts or config files
4. **Commit tokens or credentials** to git repositories
5. **Share credentials** between users or machines
6. **Use personal access tokens** - ⚠️ AVOID - gh CLI web auth handles everything

---

## Quick Reference

| Context                     | Git Operations          | GitHub API                                 |
| --------------------------- | ----------------------- | ------------------------------------------ |
| **Local (npm run release)** | SSH keys (smart config) | gh CLI (web auth) - ⚠️ AVOID manual tokens |
| **GitHub Actions**          | Automatic credentials   | Automatic credentials                      |

**Priority Order**: SSH keys (smart config) → gh CLI (web auth) → ⚠️ NEVER create manual tokens!
