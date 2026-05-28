# Push Todo Plugin: Marketplace Distribution Implementation Plan

**Date:** 2026-01-18
**Status:** Implemented
**Goal:** Convert from custom curl/git-based installation to Claude Code native marketplace distribution

---

## Executive Summary

The current push-todo plugin uses a custom installation and update mechanism (curl download + git pull) that doesn't work properly and confuses users. This plan migrates to Claude Code's native marketplace system, which provides:

- Zero-friction auto-updates
- Professional distribution
- No git knowledge required for users
- Same UX as official Anthropic plugins

---

## How Marketplace Updates Work

### Key Discovery: Third-Party Auto-Update Default

**Third-party marketplaces have auto-update DISABLED by default.**

| Marketplace Type | Auto-Update Default |
|------------------|---------------------|
| Official Anthropic | Enabled |
| Third-party (us) | **Disabled** |

Users must explicitly enable auto-update for our marketplace via:
```
/plugin → Marketplaces → MasslessAI/push-todo-cli → Enable auto-update
```

### Update Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                     PUBLISHER SIDE (Us)                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1. Developer pushes code to main branch                        │
│                     ↓                                           │
│  2. GitHub Actions detects changes in plugins/push-todo/        │
│                     ↓                                           │
│  3. GitHub Actions runs bump-version.py                         │
│                     ↓                                           │
│  4. Version in plugin.json bumps (e.g., 1.2.2 → 1.2.3)         │
│                     ↓                                           │
│  5. GitHub Actions commits and pushes the version bump          │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
                              ↓
                    (GitHub repo updated)
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                      USER SIDE                                  │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1. User starts Claude Code                                     │
│                     ↓                                           │
│  2. Claude Code checks marketplace for updates (if enabled)     │
│                     ↓                                           │
│  3. Fetches plugin.json from GitHub                             │
│                     ↓                                           │
│  4. Compares versions: local (1.2.2) vs remote (1.2.3)         │
│                     ↓                                           │
│  5. If remote is newer → downloads and installs update          │
│                     ↓                                           │
│  6. User sees: "Plugin push-todo updated: v1.2.2 → v1.2.3"     │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### The Version Bump is the Signal

The **only thing** the marketplace needs to detect an update is a version change in:
```
plugins/push-todo/.claude-plugin/plugin.json
```

```json
{
  "name": "push-todo",
  "version": "1.2.3",  ← This is the signal
  "description": "..."
}
```

When Claude Code sees a higher version number, it triggers the update.

### Plugin.json Schema (Minimal Required Fields)

Claude Code's plugin schema is strict. Only these fields are valid:

```json
{
  "name": "push-todo",
  "version": "1.2.3",
  "description": "Receive and work on voice tasks captured on your iPhone using the Push app"
}
```

**Invalid fields that cause errors:**
- `category` ❌
- `keywords` ❌
- `engines` ❌
- `author` ❌
- `repository` ❌
- `$schema` ❌

Keep the plugin.json minimal to avoid validation errors.

### Automated Version Bumping

We use GitHub Actions to auto-bump versions:

**Trigger:** Any push to `main` that modifies files in `plugins/push-todo/` (except plugin.json itself)

**Action:** Runs `scripts/bump-version.py` which:
1. Reads current version from plugin.json
2. Increments patch version (1.2.2 → 1.2.3)
3. Handles overflow (1.2.9 → 1.3.0, 1.9.9 → 2.0.0)
4. Commits and pushes the change

This means: **Push code → version auto-bumps → users get update**

No manual version management required.

---

## Current State Analysis

### What We Have Now

```
push-todo-cli/
├── .claude-plugin/
│   ├── marketplace.json    # Exists but incomplete
│   └── plugin.json         # Exists, version 1.0.0
├── plugins/
│   └── push-todo/
│       ├── .claude-plugin/
│       │   └── plugin.json # Version 1.2.0 (mismatch!)
│       ├── commands/
│       │   └── push-todo.md
│       ├── hooks/
│       │   └── session-start.sh
│       ├── scripts/
│       │   ├── check_tasks.py
│       │   ├── check_updates.py  # BROKEN for curl installs
│       │   ├── fetch_task.py
│       │   └── connect.py
│       ├── skills/
│       │   └── push-todo/SKILL.md
│       └── SKILL.md
├── install.sh              # Downloads files via curl
└── README.md
```

### Current Installation Flow (Broken)

```
User                          GitHub                      Local Machine
  │                              │                             │
  │  curl install.sh | bash     │                             │
  │─────────────────────────────>│                             │
  │                              │  Download individual files  │
  │                              │────────────────────────────>│
  │                              │                             │
  │                              │  Files in ~/.claude/skills/ │
  │                              │  (NO .git directory!)       │
  │                              │                             │
  │  Session starts              │                             │
  │                              │                             │
  │  check_updates.py runs       │                             │
  │                              │  Checks GitHub for version  │
  │                              │<────────────────────────────│
  │                              │                             │
  │  "Update available!"         │  is_git_repo() = FALSE      │
  │  "Run: git pull"             │  git pull IMPOSSIBLE!       │
  │<─────────────────────────────│                             │
  │                              │                             │
  │  User is confused            │                             │
```

### Problems

| Issue | Impact |
|-------|--------|
| curl installs files, not git repo | `git pull` impossible |
| `check_updates.py` assumes git | Auto-update never works for curl users |
| Version mismatch (1.0.0 vs 1.2.0) | Inconsistent state |
| Custom update mechanism | Reinventing the wheel poorly |
| "Run git pull" message | Confuses non-technical users |

---

## Target State: Native Marketplace Distribution

### How Claude Code Marketplaces Work

```
User                          Claude Code                 GitHub
  │                              │                          │
  │  /plugin marketplace add     │                          │
  │  MasslessAI/push-todo-cli                          │
  │─────────────────────────────>│                          │
  │                              │  Clone marketplace repo  │
  │                              │─────────────────────────>│
  │                              │                          │
  │                              │  Read marketplace.json   │
  │                              │<─────────────────────────│
  │                              │                          │
  │  /plugin install             │                          │
  │  push-todo@MasslessAI/...    │                          │
  │─────────────────────────────>│                          │
  │                              │  Install plugin          │
  │                              │─────────────────────────>│
  │                              │                          │
  │  Session starts (next time)  │                          │
  │                              │  Auto-check for updates  │
  │                              │─────────────────────────>│
  │                              │                          │
  │  [Push] Plugin updated:      │  Auto-pull if newer      │
  │  v1.2.0 → v1.3.0            │<─────────────────────────│
```

### Benefits

| Feature | Custom (Current) | Marketplace (Target) |
|---------|------------------|---------------------|
| Installation | curl script | `/plugin install` |
| Auto-update | Broken | Native, just works |
| User knowledge required | git commands | None |
| Update mechanism | Custom Python | Claude Code built-in |
| Version tracking | Manual | Automatic |
| Rollback | Impossible | Built-in |

---

## Implementation Plan

### Phase 1: Fix Marketplace Structure

**Files to modify:**

#### 1.1 Root `/.claude-plugin/marketplace.json`

Current:
```json
{
  "name": "push-todo-cli",
  "version": "1.0.0",
  "plugins": [{
    "name": "push-todo",
    "source": "./plugins/push-todo",
    "version": "1.0.0"  // Wrong!
  }]
}
```

Target:
```json
{
  "$schema": "https://anthropic.com/claude-code/marketplace.schema.json",
  "name": "push-plugins",
  "description": "Voice tasks from Push iOS app",
  "owner": {
    "name": "MasslessAI",
    "email": "support@pushto.do",
    "url": "https://pushto.do"
  },
  "plugins": [
    {
      "name": "push-todo",
      "description": "Receive and work on voice tasks captured on your iPhone",
      "source": "./plugins/push-todo",
      "category": "productivity"
    }
  ]
}
```

**Note:** Version is read from the plugin's own `plugin.json`, not duplicated here.

#### 1.2 Plugin `/plugins/push-todo/.claude-plugin/plugin.json`

Current:
```json
{
  "name": "push-todo",
  "version": "1.2.0",
  "description": "Receive and work on voice tasks captured on Push iOS app",
  ...
}
```

Target (add required fields):
```json
{
  "$schema": "https://anthropic.com/claude-code/plugin.schema.json",
  "name": "push-todo",
  "version": "1.2.1",
  "description": "Receive and work on voice tasks captured on your iPhone using the Push app",
  "author": {
    "name": "MasslessAI",
    "email": "support@pushto.do",
    "url": "https://pushto.do"
  },
  "repository": {
    "type": "git",
    "url": "https://github.com/MasslessAI/push-todo-cli"
  },
  "homepage": "https://pushto.do",
  "license": "MIT",
  "keywords": ["voice", "tasks", "ios", "mobile", "todo", "productivity", "push", "iphone"],
  "category": "productivity",
  "engines": {
    "claude-code": ">=1.0.0"
  }
}
```

### Phase 2: Remove Custom Update Mechanism

**Files to delete:**
- `/plugins/push-todo/scripts/check_updates.py` - No longer needed

**Files to modify:**

#### 2.1 Session Start Hook

Remove update check from `/plugins/push-todo/hooks/session-start.sh`:

```bash
#!/bin/bash
# Push Session Start Hook for Claude Code
# Only checks for active tasks - updates handled by Claude Code marketplace

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PLUGIN_DIR="$(dirname "$SCRIPT_DIR")"

# Check for active tasks
COUNT=$(python3 "$PLUGIN_DIR/scripts/check_tasks.py" 2>/dev/null)

if [ $? -ne 0 ]; then
    exit 0
fi

if [ -n "$COUNT" ] && [ "$COUNT" -gt 0 ]; then
    if [ "$COUNT" -eq 1 ]; then
        echo "[Push] You have 1 active task from your iPhone. Say 'push-todo' to see it."
    else
        echo "[Push] You have $COUNT active tasks from your iPhone. Say 'push-todo' to see them."
    fi
fi
```

### Phase 3: Simplify Installation

**Current flow:**
```bash
curl -sL https://raw.githubusercontent.com/.../install.sh | bash
# Then: /push-todo connect
```

**New flow:**
```bash
/plugin marketplace add MasslessAI/push-todo-cli
/plugin install push-todo@MasslessAI/push-todo-cli
# Then: /push-todo connect
```

#### 3.1 Update README.md

```markdown
## Installation

### Option 1: Claude Code Plugin (Recommended)

1. Add the Push marketplace:
   ```
   /plugin marketplace add MasslessAI/push-todo-cli
   ```

2. Install the plugin:
   ```
   /plugin install push-todo@MasslessAI/push-todo-cli
   ```

3. Connect your account:
   ```
   /push-todo connect
   ```

### Option 2: Quick Install (Legacy)

For users who prefer a one-liner:
```bash
curl -sL https://raw.githubusercontent.com/MasslessAI/push-todo-cli/main/install.sh | bash
```

Note: This method does not support auto-updates. Use the plugin marketplace for automatic updates.
```

#### 3.2 Update install.sh (Keep for Legacy)

Add deprecation notice:
```bash
#!/bin/bash
echo "=========================================="
echo "NOTICE: This installation method is deprecated."
echo ""
echo "For auto-updates, use the Claude Code marketplace instead:"
echo "  /plugin marketplace add MasslessAI/push-todo-cli"
echo "  /plugin install push-todo@MasslessAI/push-todo-cli"
echo ""
echo "Continuing with legacy installation..."
echo "=========================================="
sleep 2

# ... rest of script
```

### Phase 4: Connect Command Updates

#### 4.1 `/push-todo connect` Should Handle Everything

The connect command should:
1. Check if installed via marketplace vs curl
2. For curl installs, suggest migrating to marketplace
3. Handle API key configuration

Update `/plugins/push-todo/scripts/connect.py` to add marketplace migration hint:

```python
def check_installation_method():
    """Check how the plugin was installed."""
    plugin_dir = Path(__file__).parent.parent

    # Check if this is a marketplace installation
    # Marketplace installs are in ~/.claude/plugins/ not ~/.claude/skills/
    if "plugins" in str(plugin_dir):
        return "marketplace"
    elif plugin_dir.is_symlink():
        return "development"
    else:
        return "legacy"

def suggest_migration():
    """Suggest migrating to marketplace if using legacy install."""
    method = check_installation_method()
    if method == "legacy":
        print("\n" + "="*50)
        print("TIP: You're using a legacy installation.")
        print("For auto-updates, migrate to the marketplace:")
        print("")
        print("  /plugin marketplace add MasslessAI/push-todo-cli")
        print("  /plugin install push-todo@MasslessAI/push-todo-cli")
        print("="*50 + "\n")
```

### Phase 5: Version Management

#### 5.1 Single Source of Truth

Version should only be defined in:
- `/plugins/push-todo/.claude-plugin/plugin.json`

Remove version from:
- `/.claude-plugin/marketplace.json` (plugins section)
- `/.claude-plugin/plugin.json` (root level - this is marketplace metadata, not plugin)

#### 5.2 Update bump-version.py

Modify `/scripts/bump-version.py` to only update the plugin's plugin.json:

```python
PLUGIN_JSON = Path(__file__).parent.parent / "plugins/push-todo/.claude-plugin/plugin.json"

def bump_version(version_type="patch"):
    with open(PLUGIN_JSON) as f:
        data = json.load(f)

    current = data["version"]
    new_version = calculate_new_version(current, version_type)
    data["version"] = new_version

    with open(PLUGIN_JSON, "w") as f:
        json.dump(data, f, indent=2)

    return new_version
```

### Phase 6: GitHub Actions for Auto-Versioning

Keep existing workflow but simplify:

```yaml
# .github/workflows/bump-version.yml
name: Bump Version

on:
  push:
    branches: [main]
    paths:
      - 'plugins/push-todo/**'
      - '!plugins/push-todo/.claude-plugin/plugin.json'

jobs:
  bump:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.x'
      - name: Bump version
        run: python scripts/bump-version.py
      - name: Commit
        run: |
          git config user.name "github-actions[bot]"
          git config user.email "github-actions[bot]@users.noreply.github.com"
          git add plugins/push-todo/.claude-plugin/plugin.json
          git commit -m "chore: bump version" || exit 0
          git push
```

---

## Migration Guide for Existing Users

### For Curl-Installed Users

```bash
# 1. Remove old installation
rm -rf ~/.claude/skills/push-todo

# 2. Install via marketplace
/plugin marketplace add MasslessAI/push-todo-cli
/plugin install push-todo@MasslessAI/push-todo-cli

# 3. Your config is preserved in ~/.config/push/
# No need to run connect again!
```

### For Development (Symlink) Users

No change needed. Symlinks continue to work, and you can test marketplace features locally.

---

## Testing Plan

### Test 1: Fresh Marketplace Install
1. Remove any existing push-todo installation
2. Run `/plugin marketplace add MasslessAI/push-todo-cli`
3. Run `/plugin install push-todo@MasslessAI/push-todo-cli`
4. Verify `/push-todo` command works
5. Verify session-start hook shows task count

### Test 2: Auto-Update
1. Install plugin at version X
2. Push a change to GitHub (triggers version bump to X+1)
3. Start new Claude Code session
4. Verify auto-update message appears
5. Verify new version is installed

### Test 3: Legacy Install Warning
1. Install via curl
2. Run `/push-todo connect`
3. Verify migration hint is displayed

### Test 4: Config Preservation
1. Install, run connect, verify tasks appear
2. Uninstall
3. Reinstall via marketplace
4. Verify tasks still appear (config preserved)

---

## Rollout Plan

### Phase 1: Prepare (This PR)
- [ ] Fix marketplace.json structure
- [ ] Fix plugin.json structure
- [ ] Remove check_updates.py
- [ ] Update session-start.sh
- [ ] Update README.md

### Phase 2: Soft Launch
- [ ] Test with developer accounts
- [ ] Verify auto-update works
- [ ] Document any issues

### Phase 3: Announce
- [ ] Update Push iOS app to show new install instructions
- [ ] Deprecate curl install in documentation
- [ ] Monitor for user issues

### Phase 4: Cleanup (2 weeks later)
- [ ] Remove install.sh or make it redirect to marketplace
- [ ] Remove legacy code paths

---

## Files Changed Summary

| File | Action | Notes |
|------|--------|-------|
| `/.claude-plugin/marketplace.json` | Modify | Fix structure |
| `/.claude-plugin/plugin.json` | Modify | This is marketplace metadata |
| `/plugins/push-todo/.claude-plugin/plugin.json` | Modify | Add required fields |
| `/plugins/push-todo/scripts/check_updates.py` | Delete | No longer needed |
| `/plugins/push-todo/hooks/session-start.sh` | Modify | Remove update check |
| `/plugins/push-todo/scripts/connect.py` | Modify | Add migration hint |
| `/scripts/bump-version.py` | Modify | Single source of truth |
| `/README.md` | Modify | New install instructions |
| `/install.sh` | Modify | Add deprecation notice |

---

## Codex Unification (2026-01-21)

### Problem Identified

After implementing marketplace distribution for Claude Code, we discovered Codex support was significantly behind:

| Issue | Impact |
|-------|--------|
| Duplicate `codex/SKILL.md` | Feature drift (v1.0 vs v1.5.5) |
| Missing v1.5 features | No direct task lookup, review mode, completion comments |
| No update mechanism | Users stuck on old versions |
| Version check broken | Looked for wrong files |

### Solution: Single Source of Truth (DRY)

Instead of maintaining two separate SKILL.md files, we now use one canonical source with path transformation:

```
BEFORE:
  plugins/push-todo/SKILL.md  (v1.5.5, Claude Code paths)
  codex/SKILL.md              (v1.0, Codex paths)

AFTER:
  plugins/push-todo/SKILL.md  (v1.5.5, single source)
  [codex/SKILL.md deleted]
```

### Implementation

**1. Install Script Transformation**

Updated `codex/install-codex.sh` to download canonical SKILL.md and transform paths:

```bash
# Download from canonical source
curl -sL "$BASE_URL/plugins/push-todo/SKILL.md" | \
  sed 's|\${CLAUDE_PLUGIN_ROOT:-\$HOME/\.claude/skills/push-todo}|$HOME/.codex/skills/push-todo|g' \
  > "$SKILLS_DIR/SKILL.md"
```

**Path transformation:**
```
Source:  python3 "${CLAUDE_PLUGIN_ROOT:-$HOME/.claude/skills/push-todo}/scripts/fetch_task.py"
         ↓ (sed)
Target:  python3 "$HOME/.codex/skills/push-todo/scripts/fetch_task.py"
```

**2. Codex Detection in connect.py**

Added Codex to installation method detection:

```python
def get_installation_method() -> str:
    if ".claude/plugins" in str(plugin_dir):
        return "marketplace"
    if ".codex/skills" in str(plugin_dir):  # NEW
        return "codex"
    if ".claude/skills" in str(plugin_dir):
        return "legacy"
    # ...
```

**3. Codex Update Handler**

Added update path for Codex users:

```python
def do_update() -> dict:
    if method == "codex":
        # Re-run Codex install script
        subprocess.run(["bash", "-c",
            f"curl -fsSL {CODEX_INSTALL_SCRIPT_URL} | bash"])
```

**4. Migration Hint Suppression**

Codex users don't see Claude Code migration hints (they're already on the right install method).

### Results

| Metric | Before | After |
|--------|--------|-------|
| **SKILL.md files** | 2 | 1 |
| **Codex features** | v1.0 (outdated) | v1.5.5 (current) |
| **Codex updates** | Manual reinstall | `$push-todo connect` |
| **Feature drift risk** | High (manual sync) | Zero (single source) |
| **DRY compliance** | ❌ Duplicate | ✅ Single source |

### Testing Verification

```bash
# Test sed transformation
echo 'python3 "${CLAUDE_PLUGIN_ROOT:-$HOME/.claude/skills/push-todo}/scripts/fetch_task.py"' | \
  sed 's|\${CLAUDE_PLUGIN_ROOT:-\$HOME/\.claude/skills/push-todo}|$HOME/.codex/skills/push-todo|g'

# Output: python3 "$HOME/.codex/skills/push-todo/scripts/fetch_task.py"
# ✅ Correct transformation
```

### Files Changed (Codex Unification)

| File | Action | Impact |
|------|--------|--------|
| `codex/SKILL.md` | Deleted | Removed 98 lines of duplicate content |
| `codex/install-codex.sh` | Modified | Downloads from canonical source + transforms |
| `plugins/push-todo/scripts/connect.py` | Modified | Added Codex detection + update handler |
| `README.md` | Modified | Added Codex support section |

**Commit:** `d8aecc7` - "Unify Codex and Claude Code with single SKILL.md source"

### Open Questions Resolved

~~**2. Codex CLI:** The `/codex` folder has a separate install script. Should we create a separate marketplace for it?~~
   - ✅ **RESOLVED:** Codex doesn't have marketplace system. Use single SKILL.md with path transformation instead.

---

## Open Questions

1. **Backward Compatibility:** Should we keep curl install working indefinitely or sunset it?
   - Recommendation: Keep for 3 months, then remove

3. **Version Sync:** How to ensure GitHub Actions version bump and marketplace are in sync?
   - Answer: Version is only in plugin.json, marketplace reads it

---

## References

- [Claude Code Plugin Marketplaces](https://code.claude.com/docs/en/plugin-marketplaces)
- [Create Plugins](https://code.claude.com/docs/en/plugins)
- [anthropics/claude-plugins-official](https://github.com/anthropics/claude-plugins-official)
