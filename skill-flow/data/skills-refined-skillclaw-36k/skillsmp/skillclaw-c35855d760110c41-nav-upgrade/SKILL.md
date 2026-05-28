---
name: nav-upgrade
description: Use this skill to automate updates for the Navigator plugin, including version detection, installation, and validation of new features.
---

# Navigator Upgrade Skill

Automate Navigator plugin updates with version detection, conflict resolution, and post-update validation.

## When to Invoke

Auto-invoke when user says:
- "Update Navigator"
- "Upgrade Navigator plugin"
- "Get latest Navigator version"
- "Update to Navigator v3.3.0"
- "Install new Navigator features"
- "Check for Navigator updates"

## What This Does

**6-Step Workflow**:
1. **Version Detection**: Check current Navigator version vs latest.
2. **Plugin Update**: Execute `/plugin update navigator`.
3. **Verification**: Confirm update succeeded.
4. **CLAUDE.md Update**: Update project configuration.
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

**Scenario 1: Stable update available**
```json
{
  "current_version": "4.0.0",
  "latest_stable": "4.2.0",
  "latest_prerelease": null,
  "recommendation": "update_to_stable"
}
```

**Scenario 2: Pre-release available (user on stable)**
```json
{
  "current_version": "4.0.0",
  "latest_stable": "4.0.0",
  "latest_prerelease": "4.3.0",
  "recommendation": "offer_prerelease_option"
}
```

**Present choice**:
```
✅ You're on the latest stable version (v4.0.0)

⚡ Experimental version available: v4.3.0

New in v4.3.0 (Experimental):
• Multi-Claude agentic workflows
• 30% success rate (use for simple features)
• PM integration with ticket closing

Options:
[1] Stay on stable v4.0.0 (recommended)
[2] Try experimental v4.3.0
```