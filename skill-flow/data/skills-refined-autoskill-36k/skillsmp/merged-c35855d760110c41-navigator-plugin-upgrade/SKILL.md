---
name: navigator-plugin-upgrade
description: Use this skill to automate updates for the Navigator plugin, including version detection, installation, verification, and feature discovery.
---

# Navigator Plugin Upgrade Skill

Automate Navigator plugin updates with version detection, conflict resolution, and post-update validation.

## When to Invoke

Auto-invoke when user says:
- "Update Navigator"
- "Upgrade Navigator plugin"
- "Get latest Navigator version"
- "Install new Navigator features"
- "Check for Navigator updates"

## What This Does

**6-Step Workflow**:
1. **Version Detection**: Check current Navigator version vs latest.
2. **Plugin Update**: Execute `/plugin update navigator`.
3. **Verification**: Confirm update succeeded.
4. **CLAUDE.md Update**: Update project configuration (via nav-update-claude).
5. **Hooks Setup**: Install/update token monitoring hooks in project.
6. **Feature Discovery**: Show new features available.

**Time Savings**: Manual update (10-15 min) → Automated (2 min).

---

## Prerequisites

- Navigator plugin installed.
- Project initialized with Navigator.
- Internet connection for plugin update.

---

## Workflow Protocol

### Step 1: Version Detection

**Execute**: `version_detector.py`

**Check both stable and pre-release versions**:
```bash
# Current installed version
grep '"version"' .claude-plugin/plugin.json

# Get all releases (including pre-releases)
curl -s https://api.github.com/repos/alekspetrov/navigator/releases

# Parse:
# - Latest stable (prerelease: false)
# - Latest pre-release (prerelease: true)
# - Compare with current version
```

**Output scenarios**:

- **Stable update available**:
```json
{
  "current_version": "4.0.0",
  "latest_stable": "4.2.0",
  "latest_prerelease": null,
  "recommendation": "update_to_stable"
}
```

- **Pre-release available (user on stable)**:
```json
{
  "current_version": "4.0.0",
  "latest_stable": "4.0.0",
  "latest_prerelease": "4.3.0",
  "recommendation": "offer_prerelease_option"
}
```

- **Already on latest (stable or pre-release)**:
```
✅ You're on v4.3.0 (latest experimental)
```

- **On pre-release, newer stable available**:
```
⚠️  You're on v4.3.0 (experimental)
Latest stable: v4.6.0
Recommendation: Update to stable v4.6.0
```

---

### Step 2: Plugin Update

**Scenario-based update strategy**:

- **If pre-release detected**:
```markdown
✅ You're on latest stable version (v4.0.0)

⚡ Experimental version available: v4.3.0

**Question**: Which version would you like?

**Options**:
[1] **Stay on stable v4.0.0** (recommended)
[2] **Try experimental v4.3.0** (early adopter)
```

- **If user chooses [1] (Stay stable)**:
```
✓ Staying on v4.0.0 (latest stable)
```

- **If user chooses [2] (Try experimental)**:
```bash
# Uninstall current version
/plugin uninstall navigator

# Install specific pre-release version
git clone https://github.com/alekspetrov/navigator.git /tmp/navigator-v4.3.0
cd /tmp/navigator-v4.3.0
git checkout v4.3.0
/plugin install /tmp/navigator-v4.3.0
```

- **If stable update available**:
```bash
/plugin update navigator
```

**If update fails**:
```
❌ Update failed: [error message]
```

**Automatic retry** (once):
```bash
/plugin uninstall navigator
/plugin install navigator
```

---

### Step 3: Verification

**Execute**: `plugin_verifier.py`

**Verify**:
1. Plugin version matches latest.
2. New skills registered in plugin.json.
3. Skills are invokable.

**If verification fails**:
```
⚠️ Update completed but verification failed
```

**IMPORTANT - Restart Required After All Updates**:
```
⚠️  RESTART REQUIRED
```

---

### Step 4: Update Project CLAUDE.md (Automatic)

**After plugin update, automatically invoke**: `nav-update-claude`.

---

### Step 5: Setup Token Monitoring Hooks

**Install or update project hooks** for token budget monitoring:
```bash
mkdir -p .claude
cat > .claude/settings.json << 'EOF'
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit|Bash|Task",
        "hooks": [
          {
            "type": "command",
            "command": "python3 \"${CLAUDE_PLUGIN_DIR}/hooks/monitor-tokens.py\"",
            "timeout": 5
          }
        ]
      }
    ]
  }
}
EOF
```

---

### Step 6: Post-Upgrade Setup Check

**Check if new features require setup**.

---

### Step 7: Feature Discovery

**Show new features** available in updated version.

---

## Error Handling

### Update Failed: Network Error
```
❌ Update failed: Could not connect to plugin marketplace
```

### Verification Failed: Skills Not Found
```
⚠️ Update completed but new skills not found
```

---

## Rollback

If update causes issues:
```
"Rollback Navigator to v3.2.0"
```

---

## Best Practices

1. **Update regularly**: Check for updates monthly.
2. **Read release notes**: Understand new features before using.
3. **Test new skills**: Try new features in test project first.

---

## Version History

- **v1.0.0**: Initial navigator-plugin-upgrade skill.

---

**Last Updated**: 2025-10-21
**Skill Type**: Core Navigator
**Auto-Invocation**: Yes