**Skill**: [semantic-release](../SKILL.md)

# Local Release Workflow (Canonical)

**Single source of truth** for executing semantic-release locally. This 4-phase workflow ensures reliable, repeatable releases with automatic push.

```
                 Release Workflow Pipeline

 -----------      +------+     +---------+      ------------
| PREFLIGHT | --> | SYNC | --> | RELEASE | --> | POSTFLIGHT |
 -----------      +------+     +---------+      ------------
```

<details>
<summary>graph-easy source</summary>

```
graph { label: "Release Workflow Pipeline"; flow: east; }

[ PREFLIGHT ] { shape: rounded; } -> [ SYNC ] -> [ RELEASE ] -> [ POSTFLIGHT ] { shape: rounded; }
```

</details>

---

## Quick Reference

**Priority 1**: mise-managed release (if `.mise.toml` has release tasks):

```bash
mise run release:version    # Semantic-release version bump only
mise run release:full       # Full workflow (version → build → smoke → publish)
```

**Priority 2**: npm scripts (standard):

```bash
npm run release:dry   # Preview changes (no modifications)
npm run release       # Execute release (auto-pushes via successCmd + postrelease)
```

**Alternative**: All-in-one shell function (add to `~/.zshrc`):

```bash
/usr/bin/env bash << 'PREFLIGHT_EOF'
release() {
    # PHASE 1: PREFLIGHT
    # Step 1: Clear git cache to ensure accurate file status
    git update-index --refresh -q || true

    # Step 2: Tooling checks
    command -v gh &>/dev/null || { echo "FAIL: gh CLI not installed"; return 1; }
    command -v semantic-release &>/dev/null || { echo "FAIL: semantic-release not installed globally"; return 1; }
    gh api user --jq '.login' &>/dev/null || { echo "FAIL: GH_TOKEN not set"; return 1; }
    gh api -i user 2>&1 | grep -iq "x-oauth-scopes:.*workflow" || { echo "FAIL: GH_TOKEN missing 'workflow' scope"; echo "Fix: gh auth refresh -s workflow"; return 1; }

    # Account verification (if GH_ACCOUNT is set via mise [env])
    if [[ -n "${GH_ACCOUNT:-}" ]]; then
        local actual_user=$(gh api user --jq '.login' 2>/dev/null)
        [[ "$actual_user" == "$GH_ACCOUNT" ]] || { echo "FAIL: Account mismatch: expected $GH_ACCOUNT, got $actual_user"; echo "Fix: gh auth switch --user $GH_ACCOUNT"; return 1; }
    fi

    git rev-parse --git-dir &>/dev/null || { echo "FAIL: Not a git repo"; return 1; }

    local branch=$(git branch --show-current)
    [[ "$branch" == "main" ]] || { echo "FAIL: Not on main (on: $branch)"; return 1; }
    # Step 3: Check for uncommitted changes (modified, untracked, staged, deleted)
    [[ -z "$(git status --porcelain)" ]] || { echo "FAIL: Working directory not clean"; git status --short; return 1; }

    # Check for releasable commits
    local last_tag=$(git describe --tags --abbrev=0 2>/dev/null)
    if [[ -n "$last_tag" ]]; then
        if ! git log "${last_tag}..HEAD" --oneline | grep -qE "^[a-f0-9]+ (feat|fix|BREAKING)"; then
            echo "FAIL: No releasable commits since $last_tag"
            echo "Use feat: or fix: prefix for version-bumping changes"
            return 1
        fi
        # Check for MAJOR (breaking changes)
        local major_commits=$(git log "${last_tag}..HEAD" --oneline | grep -E "(BREAKING CHANGE|^[a-f0-9]+ (feat|fix)!:)")
        if [[ -n "$major_commits" ]]; then
            echo "⚠️  MAJOR VERSION BUMP DETECTED"
            echo "$major_commits"
            echo ""
            echo "In Claude Code: Multi-perspective analysis + AskUserQuestion will trigger"
            echo "In shell: Confirm manually before proceeding"
            read -p "Continue with MAJOR release? [y/N] " -n 1 -r
            echo
            [[ ! $REPLY =~ ^[Yy]$ ]] && { echo "Aborted by user"; return 1; }
        fi
    fi
    echo "PREFLIGHT: OK"

    # PHASE 2: SYNC
    git pull --rebase origin main --quiet || { echo "FAIL: Pull failed"; return 1; }
    git push origin main --quiet || { echo "FAIL: Push failed"; return 1; }
    echo "SYNC: OK"

    # PHASE 3: RELEASE
    export GIT_OPTIONAL_LOCKS=0
    # Uses GITHUB_TOKEN from mise [env] - no $(gh auth token) capture
    semantic-release --no-ci "$@"
    local rc=$?
    [[ $rc -ne 0 ]] && { echo "FAIL: semantic-release exited with code $rc"; return $rc; }
    echo "RELEASE: OK"

    # PHASE 4: POSTFLIGHT
    [[ -n $(git status --porcelain) ]] && { echo "WARN: Unexpected uncommitted changes"; git status --short; }
    git fetch origin main:refs/remotes/origin/main --no-tags
    echo "POSTFLIGHT: OK (tracking refs updated)"

    echo ""
    echo "Latest release:"
    gh release list --limit 1
}
PREFLIGHT_EOF
```

---

## Phase 1: Preflight

**Purpose**: Validate all prerequisites before any git operations.

### 1.1 Git Cache Refresh

**MANDATORY first step**: Clear git cache before any status checks.

```bash
git update-index --refresh -q || true
```

This ensures all modified, untracked, staged, and deleted files are accurately detected by subsequent `git status` commands.

### 1.2 Tooling Check

| Check                   | Command                       | Expected   | Resolution                                                 |
| ----------------------- | ----------------------------- | ---------- | ---------------------------------------------------------- |
| Git cache fresh         | `git update-index --refresh`  | No output  | Auto-runs (Step 1)                                         |
| gh CLI installed        | `command -v gh`               | Path to gh | `brew install gh`                                          |
| gh workflow scope       | `gh api -i user \| grep workflow` | Present | `gh auth refresh -s workflow`                              |
| **gh account match**    | `gh api user --jq '.login'`   | = GH_ACCOUNT | `gh auth switch --user $GH_ACCOUNT`                       |
| semantic-release global | `command -v semantic-release` | Path       | See [Troubleshooting](#macos-gatekeeper-blocks-node-files) |
| In git repo             | `git rev-parse --git-dir`     | `.git`     | Navigate to repo root                                      |
| On main branch          | `git branch --show-current`   | `main`     | `git checkout main`                                        |
| Clean working directory | `git status --porcelain`      | Empty      | Commit or stash                                            |

### 1.3 Authentication Check (HTTPS-First)

**Primary method** (per authentication.md 2025-12-19+):

```bash
# Verify HTTPS remote
git remote get-url origin
# Expected: https://github.com/...

# Verify GH_TOKEN active via mise [env]
gh api user --jq '.login'
# Expected: correct account for this directory
```

**If remote is SSH** (legacy):

```bash
git-ssh-to-https  # Convert to HTTPS-first
```

**Multi-account verification**:

```bash
# SSH test (for comparison)
ssh -T git@github.com 2>&1
# "Hi <username>! You've successfully authenticated..."

# gh account
gh auth status 2>&1 | grep -B1 "Active account: true" | head -1

# If mismatch: switch account
gh auth switch --user <expected-username>
```

### 1.4 Releasable Commits Validation

**MANDATORY**: Verify version-bumping commits exist before proceeding.

```bash
/usr/bin/env bash << 'GIT_EOF'
LAST_TAG=$(git describe --tags --abbrev=0 2>/dev/null)
git log "${LAST_TAG}..HEAD" --oneline | grep -E "^[a-f0-9]+ (feat|fix|BREAKING)"
GIT_EOF
```

**If no releasable commits**:

- STOP immediately
- Inform user: "No version-bumping commits since last release"
- Only `feat:`, `fix:`, or `BREAKING CHANGE:` trigger releases

### 1.5 MAJOR Version Confirmation (Interactive)

**Trigger**: Commits containing `BREAKING CHANGE:` footer or `feat!:`/`fix!:` prefix.

```bash
/usr/bin/env bash << 'MAJOR_EOF'
LAST_TAG=$(git describe --tags --abbrev=0 2>/dev/null)
MAJOR_COMMITS=$(git log "${LAST_TAG}..HEAD" --oneline | grep -E "(BREAKING CHANGE|^[a-f0-9]+ (feat|fix)!:)")
if [[ -n "$MAJOR_COMMITS" ]]; then
    echo "⚠️  MAJOR VERSION BUMP DETECTED"
    echo "$MAJOR_COMMITS"
fi
MAJOR_EOF
```

**If MAJOR detected** (Claude Code interactive mode):

1. **Spawn 3 parallel Task subagents** for multi-perspective analysis:
   - User Impact Analyst (who is affected, scope, workarounds)
   - API Compatibility Analyst (what breaks, alternatives, deprecation path)
   - Migration Strategist (effort level, migration guide needs, timeline)

2. **Present AskUserQuestion with multiSelect**:
   ```yaml
   questions:
     - question: "MAJOR version bump detected. How should we proceed?"
       header: "Breaking"
       multiSelect: false
       options:
         - label: "Proceed with MAJOR (Recommended)"
           description: "Release as X.0.0 - breaking change is intentional"
         - label: "Downgrade to MINOR"
           description: "Amend commits to remove BREAKING CHANGE"
         - label: "Abort release"
           description: "Review commits before releasing"
     - question: "Which mitigations for release notes?"
       header: "Mitigations"
       multiSelect: true
       options:
         - label: "Migration guide"
         - label: "Deprecation notice"
         - label: "Compatibility shim"
   ```

3. **Handle response**:
   - "Proceed with MAJOR" → Continue to Phase 2
   - "Downgrade to MINOR" → Guide user through commit amendment
   - "Abort release" → STOP, user reviews

See [SKILL.md § MAJOR Version Confirmation](../SKILL.md#major-version-breaking-change-confirmation) for detailed subagent prompts and decision tree.

---

## Phase 2: Sync

**Purpose**: Synchronize local and remote before release.

### 2.1 Pull with Rebase

```bash
git pull --rebase origin main
```

**If conflicts**: Resolve, `git add .`, `git rebase --continue`

### 2.2 Push Local Commits

```bash
git push origin main
```

**If push fails** (SSH permission issues):

1. Check ControlMaster cache (see [Troubleshooting](#controlmaster-cache-issues))
2. With HTTPS-first, this should rarely happen

---

## Phase 3: Release

**Purpose**: Execute semantic-release with proper environment.

### 3.1 Dry-Run (Recommended First)

```bash
npm run release:dry
# Or (relies on mise GH_TOKEN/GITHUB_TOKEN):
semantic-release --no-ci --dry-run
```

### 3.2 Execute Release

```bash
npm run release
# Or (relies on mise GH_TOKEN/GITHUB_TOKEN):
GIT_OPTIONAL_LOCKS=0 semantic-release --no-ci
```

> **Note**: As of v9.15.0, `npm run release` no longer calls `$(gh auth token)`. It relies on mise `[env]` setting `GITHUB_TOKEN` per-directory. This prevents account switching issues in multi-account setups.

**What happens**:

1. `@semantic-release/commit-analyzer` - Determines version bump
2. `@semantic-release/release-notes-generator` - Generates changelog content
3. `@semantic-release/exec` - Runs generateNotesCmd, prepareCmd
4. `@semantic-release/changelog` - Updates CHANGELOG.md
5. `@semantic-release/git` - Creates commit + tag locally
6. `@semantic-release/exec` - **successCmd pushes via `git push --follow-tags`**
7. `@semantic-release/github` - Creates GitHub release via API

> **Note**: Use global `semantic-release` install, not `npx`, to avoid macOS Gatekeeper issues.

---

## Phase 4: Postflight

**Purpose**: Verify success, update local state, and sync local plugin cache.

### 4.1 Verify Pristine State

```bash
git status --porcelain
# Expected: empty (no uncommitted changes)
```

### 4.2 Verify Release Created

```bash
gh release list --limit 1
# Should show new version
```

### 4.3 Update Local Tracking Refs

**IMPORTANT**: Even with successCmd push, local tracking refs may be stale.

```bash
git fetch origin main:refs/remotes/origin/main --no-tags
```

**Why**: Shell prompts, IDE git integrations, and status lines rely on local tracking refs. Without this update, they show incorrect ahead/behind counts.

### 4.4 Verify Sync

```bash
git status -sb
# Expected: ## main...origin/main (no ahead/behind counts)
```

### 4.5 Plugin Cache Sync (cc-skills only)

**For cc-skills repository**: The `.releaserc.yml` includes a `successCmd` that automatically:

1. **Updates marketplace repo**: `~/.claude/plugins/marketplaces/cc-skills/` git reset to new tag
2. **Triggers plugin update**: `claude --print "/plugin update cc-skills"`
3. **Verifies cache**: Confirms `~/.claude/plugins/cache/cc-skills/<plugin>/<version>/` exists

**No manual `/plugin update` required** — this is fully automated in the release workflow.

```
                        cc-skills Post-Release Cache Sync

 ---------      +--------------------+     +-----------------+      --------------
| Release |     | Update Marketplace |     | Trigger /plugin |     | Verify Cache |
|         | --> |        Repo        | --> |     update      | --> |  v{VERSION}  |
 ---------      +--------------------+     +-----------------+      --------------
```

<details>
<summary>graph-easy source</summary>

```
graph { label: "cc-skills Post-Release Cache Sync"; flow: east; }
[ Release ] { shape: rounded; } -> [ Update Marketplace\nRepo ] -> [ Trigger /plugin\nupdate ] -> [ Verify Cache\nv{VERSION} ] { shape: rounded; }
```

</details>

---

## Success Criteria

- [ ] All prerequisites verified
- [ ] HTTPS-first authentication confirmed
- [ ] Releasable commits validated
- [ ] **MAJOR confirmation completed** (if breaking changes detected)
- [ ] Remote synced (pull + push)
- [ ] semantic-release executed without error
- [ ] **Version incremented** (new tag > previous)
- [ ] Release visible: `gh release list --limit 1`
- [ ] Working directory pristine
- [ ] Local tracking refs updated (no stale indicators)
- [ ] **Plugin cache synced** (cc-skills: `~/.claude/plugins/cache/` has new version)

---

## Troubleshooting

For all troubleshooting, see [Troubleshooting](./troubleshooting.md).

Common release issues:
- Authentication: [Authentication Issues](./troubleshooting.md#authentication-issues)
- SSH: [ControlMaster Cache](./troubleshooting.md#ssh-controlmaster-cache)
- macOS: [Gatekeeper Blocks](./troubleshooting.md#macos-gatekeeper-blocks-node-files)
- Version: [No Release Created](./troubleshooting.md#no-release-created)

---

## Migration from Pre-v7.10 Projects

Projects initialized before v7.10 lack automatic push. Add manually:

**1. Add successCmd to `.releaserc.yml`** (after @semantic-release/git):

```yaml
# After @semantic-release/git entry
- - "@semantic-release/exec"
  - successCmd: "/usr/bin/env bash -c 'git push --follow-tags origin main'"
```

**2. Add postrelease to `package.json`**:

```bash
npm pkg set scripts.postrelease="git fetch origin main:refs/remotes/origin/main --no-tags || true"
```
