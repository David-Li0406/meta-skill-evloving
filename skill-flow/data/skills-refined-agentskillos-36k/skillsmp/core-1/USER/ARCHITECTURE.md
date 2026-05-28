<!--
================================================================================
PAI CORE - USER/ARCHITECTURE.md
================================================================================

PURPOSE:
User-specific PAI installation paths, directory structure, and configuration.
This file documents Rob's specific PAI setup and any legacy/deprecated paths.

LOCATION:
- Kai (Private): ${PAI_DIR}/skills/CORE/USER/ARCHITECTURE.md

RELATED FILES:
- SYSTEM/PAISYSTEMARCHITECTURE.md - Generic PAI architecture principles
- SKILL.md - Auto-loaded core context

LAST UPDATED: 2026-01-10
VERSION: 1.0.0
================================================================================
-->

# PAI User Architecture

Rob's Personal AI Infrastructure installation and directory structure.

---

## Canonical Installation Path

**PAI Base Directory:** `~/.claude`

This is the ONLY valid PAI installation. All skills, configurations, and data live here.

```
~/.claude/
├── skills/                    # All PAI skills
│   ├── CORE/                  # Core identity and system config
│   ├── MobileApp/             # Kai Mobile App
│   ├── Infrastructure/        # Network and server configs
│   └── [other skills]/
├── settings.json              # Claude Code configuration
├── MEMORY/                    # Session history and learnings
└── bin/                       # CLI tools
```

---

## Legacy/Deprecated Paths

### ~/.config/pai/ (DEPRECATED)

**Status:** LEGACY - DO NOT USE

This directory contains an old PAI installation from before the migration to `~/.claude`.

**Why it exists:** Earlier versions of PAI used `~/.config/pai/` as the base directory. This was migrated to `~/.claude/` to align with Claude Code's default configuration location.

**What to do:**
- **NEVER** edit, build, or run code from `~/.config/pai/`
- **NEVER** update launchd services to point to this path
- If you find services running from this path, update them to use `~/.claude/`
- This directory can be safely deleted once all services are migrated

**Migration status (2026-01-10):**
- [x] MobileApp launchd service updated to `~/.claude/skills/MobileApp`
- [ ] Consider removing `~/.config/pai/` entirely after verification

---

## Service Configuration

### MobileApp (com.pai.mobile)

**Launchd plist:** `~/Library/LaunchAgents/com.pai.mobile.plist`

**Correct paths:**
- Working Directory: `~/.claude/skills/MobileApp/apps/server`
- Service Wrapper: `~/.claude/skills/MobileApp/service-wrapper.sh`
- Logs: `~/.claude/skills/MobileApp/launchd.log`

**Port:** 5050

---

## Path Reference Quick Check

When working on PAI components, verify you're in the correct directory:

```bash
# Correct - working in canonical installation
pwd | grep -q "\.claude" && echo "OK: Canonical path" || echo "WARNING: Check path!"

# Check what a running service is using
lsof -p $(lsof -ti :5050) | grep cwd
```

---

## Known Repositories

### Work Repository

| Property | Value |
|----------|-------|
| **Local Path** | `~/Projects/work` |
| **Remote** | `git@github.com:robdtaylor/work.git` |
| **Purpose** | Work-related files, projects, and code |
| **Alias** | "work repo", "save to work" |

When asked to save files to the "work repo" or "work repository", use this location.

---

## Updates

| Date | Change |
|------|--------|
| 2026-01-10 | Created file, documented legacy ~/.config/pai/ path |
| 2026-01-10 | Updated MobileApp launchd service to use ~/.claude |
| 2026-01-13 | Added work repository at ~/Projects/work |
