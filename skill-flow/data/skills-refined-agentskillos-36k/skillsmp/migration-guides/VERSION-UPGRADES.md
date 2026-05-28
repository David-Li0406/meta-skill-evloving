# Version Upgrade Guide

Patterns and procedures for upgrading Claude Code versions, handling breaking changes, and managing compatibility.

## Upgrade Overview

### Version Numbering

Claude Code follows semantic versioning: `MAJOR.MINOR.PATCH`

| Version Type | Example | Breaking Changes | Action Required |
|--------------|---------|------------------|-----------------|
| Patch | 1.0.1 -> 1.0.2 | No | Update freely |
| Minor | 1.0.x -> 1.1.x | Rare | Review changelog |
| Major | 1.x -> 2.x | Expected | Full migration |

### Check Current Version

```bash
claude --version
```

### Update Claude Code

```bash
# Using npm
npm update -g @anthropic-ai/claude-code

# Using bun
bun update -g @anthropic-ai/claude-code

# Specific version
npm install -g @anthropic-ai/claude-code@2.1.0
```

## Pre-Upgrade Checklist

Before any upgrade:

- [ ] Note current version: `claude --version`
- [ ] Backup custom configurations
- [ ] Review changelog for breaking changes
- [ ] Test in non-critical project first
- [ ] Notify team of planned upgrade

### Backup Configurations

```bash
# Backup global settings
cp ~/.claude/settings.json ~/.claude/settings.json.backup

# Backup project settings
cp .claude/settings.json .claude/settings.json.backup

# Backup CLAUDE.md
cp CLAUDE.md CLAUDE.md.backup

# Backup hooks
cp -r .claude/hooks .claude/hooks.backup
```

## Breaking Changes by Version

### Version 2.x Breaking Changes

| Change | Impact | Migration |
|--------|--------|-----------|
| Hook event rename | Hooks may not fire | Update event names |
| Settings restructure | Settings ignored | Migrate to new format |
| CLI flag changes | Scripts break | Update flag names |
| MCP protocol update | Servers disconnect | Update MCP servers |

### Version 1.x Breaking Changes

Refer to specific version notes for 1.x changes.

## Common Breaking Change Patterns

### 1. Configuration Schema Changes

**Symptom:** Settings not applied, warnings on startup

**Pattern:**
```json
// Old format (1.x)
{
  "allowedTools": ["Read", "Write"]
}

// New format (2.x)
{
  "permissions": {
    "allow": ["Read", "Write"],
    "deny": []
  }
}
```

**Migration script:**
```bash
# Check for old format
grep -l "allowedTools" ~/.claude/settings.json .claude/settings.json 2>/dev/null

# Manual migration required - update JSON structure
```

### 2. Hook Event Renames

**Symptom:** Hooks don't execute

**Pattern:**
```json
// Old event name
{
  "hooks": {
    "BeforeToolUse": [...]  // 1.x name
  }
}

// New event name
{
  "hooks": {
    "PreToolUse": [...]  // 2.x name
  }
}
```

**Migration:**
```bash
# Find affected files
grep -r "BeforeToolUse\|AfterToolUse" .claude/

# Replace in settings
sed -i 's/BeforeToolUse/PreToolUse/g' .claude/settings.json
sed -i 's/AfterToolUse/PostToolUse/g' .claude/settings.json
```

### 3. CLI Flag Changes

**Symptom:** Command not recognized, unexpected behavior

**Pattern:**
```bash
# Old flag (1.x)
claude --no-confirm

# New flag (2.x)
claude --dangerously-skip-permissions
```

**Migration:**
```bash
# Update scripts and aliases
grep -r "\-\-no-confirm" ~/scripts/ .github/workflows/

# Replace with new flag
sed -i 's/--no-confirm/--dangerously-skip-permissions/g' script.sh
```

### 4. Environment Variable Changes

**Symptom:** Authentication fails, features disabled

**Pattern:**
```bash
# Old variable
CLAUDE_API_KEY=...

# New variable
ANTHROPIC_API_KEY=...
```

**Migration:**
```bash
# Check for old variables
env | grep CLAUDE_

# Update .env files
sed -i 's/CLAUDE_API_KEY/ANTHROPIC_API_KEY/g' .env
```

### 5. MCP Protocol Updates

**Symptom:** MCP servers fail to connect

**Pattern:**
- Protocol version mismatch
- New required fields
- Changed message format

**Migration:**
```bash
# Update MCP servers
npm update @anthropic-ai/mcp-server-*

# Check server compatibility
claude mcp list
```

## Upgrade Workflow

### Minor Version Upgrade

```bash
# 1. Check changelog
# Visit: https://github.com/anthropics/claude-code/releases

# 2. Update
npm update -g @anthropic-ai/claude-code

# 3. Verify
claude --version

# 4. Test basic operations
claude "what is 2+2"
```

### Major Version Upgrade

```bash
# 1. Read full changelog and migration guide
# Visit: https://github.com/anthropics/claude-code/releases

# 2. Backup current setup
mkdir -p ~/claude-backup
cp -r ~/.claude ~/claude-backup/
cp -r .claude ~/claude-backup/project-claude

# 3. Test in isolation (optional)
# Use a test project first

# 4. Update
npm install -g @anthropic-ai/claude-code@2.0.0

# 5. Run validation
claude --version
claude "verify installation works"

# 6. Check for deprecation warnings
claude --debug 2>&1 | grep -i deprecat

# 7. Fix any issues
# See "Common Breaking Change Patterns" above

# 8. Update team
# Share migration notes
```

## Rollback Procedure

If upgrade causes issues:

```bash
# 1. Install previous version
npm install -g @anthropic-ai/claude-code@1.9.0

# 2. Restore configurations
cp ~/.claude/settings.json.backup ~/.claude/settings.json
cp .claude/settings.json.backup .claude/settings.json

# 3. Verify rollback
claude --version
claude "test basic functionality"

# 4. Document issue
# Report to: https://github.com/anthropics/claude-code/issues
```

## Version Compatibility Matrix

### Node.js Compatibility

| Claude Code | Node.js | npm |
|-------------|---------|-----|
| 2.x | >= 18.0 | >= 8.0 |
| 1.x | >= 16.0 | >= 7.0 |

### MCP Server Compatibility

| Claude Code | MCP Protocol | Server Version |
|-------------|--------------|----------------|
| 2.x | 2.0 | >= 1.0.0 |
| 1.x | 1.0 | >= 0.5.0 |

### OS Compatibility

| Claude Code | macOS | Linux | Windows |
|-------------|-------|-------|---------|
| 2.x | >= 12.0 | glibc >= 2.31 | WSL2 |
| 1.x | >= 11.0 | glibc >= 2.28 | WSL2 |

## Feature Flags and Deprecations

### Checking Feature Status

```bash
# List available features
claude config list

# Check if feature is enabled
claude config get experimental.newFeature
```

### Deprecated Features

| Feature | Deprecated In | Removed In | Alternative |
|---------|--------------|------------|-------------|
| `--no-confirm` | 1.5 | 2.0 | `--dangerously-skip-permissions` |
| `allowedTools` | 1.8 | 2.0 | `permissions.allow` |
| Hook v1 format | 1.9 | 2.0 | Hook v2 format |

### Sunset Timeline

1. **Deprecation notice**: Feature marked deprecated, works normally
2. **Warning phase**: Usage triggers warnings
3. **Removal**: Feature no longer works

## Team Upgrade Coordination

### Coordinated Upgrade Process

1. **Announce upgrade** (1 week before)
   - Share changelog summary
   - Document breaking changes
   - Provide migration instructions

2. **Update shared configurations**
   - Migrate `.claude/settings.json`
   - Update `CLAUDE.md` if needed
   - Commit to version control

3. **Staged rollout**
   - Early adopters test first
   - Fix discovered issues
   - Full team upgrade

4. **Post-upgrade validation**
   - Each team member verifies
   - Report issues centrally
   - Document lessons learned

### Version Pinning for Teams

Lock version in CI/CD:
```yaml
# .github/workflows/ci.yml
- name: Install Claude Code
  run: npm install -g @anthropic-ai/claude-code@2.1.0
```

Document version in project:
```markdown
<!-- CLAUDE.md -->
## Requirements
- Claude Code version: >= 2.1.0, < 3.0.0
```

## Upgrade Validation Checklist

After upgrading, verify:

### Basic Functionality
- [ ] `claude --version` shows expected version
- [ ] Interactive mode works: `claude`
- [ ] File read works: `claude "read package.json"`
- [ ] File write works: `claude "create test.txt with hello"`
- [ ] Search works: `claude "find all TypeScript files"`

### Configuration
- [ ] Settings loaded: `claude config list`
- [ ] CLAUDE.md context loaded
- [ ] Custom commands available: `/command-name`
- [ ] Permissions work as expected

### Hooks
- [ ] Hooks registered: check `/hooks` menu
- [ ] PreToolUse hooks fire
- [ ] PostToolUse hooks fire
- [ ] Custom hooks execute

### MCP Servers
- [ ] Servers connect: `claude mcp list`
- [ ] Server tools available
- [ ] Server data accessible

### Git Integration
- [ ] Status works: `claude "git status"`
- [ ] Commit works: `claude "commit changes"`
- [ ] PR creation works (if applicable)

## Troubleshooting Upgrades

| Issue | Cause | Solution |
|-------|-------|----------|
| Command not found | Path not updated | Restart terminal, check PATH |
| Settings ignored | Schema change | Migrate to new format |
| Hooks not firing | Event renamed | Update event names |
| MCP connection failed | Protocol mismatch | Update MCP servers |
| Permission denied | New permission model | Update permission config |
| Slow startup | Cache invalidated | Allow warm-up, clear cache |

### Debug Mode

Run with debug output:
```bash
claude --debug 2>&1 | tee claude-debug.log
```

Look for:
- Deprecation warnings
- Configuration errors
- Hook failures
- MCP connection issues

### Clear Cache

If issues persist:
```bash
# Clear Claude Code cache
rm -rf ~/.claude/cache

# Restart
claude
```

## Monitoring for Updates

### Changelog Sources

- GitHub Releases: `https://github.com/anthropics/claude-code/releases`
- npm: `npm info @anthropic-ai/claude-code`
- Changelog file in package

### Automated Update Checks

```bash
# Check for updates
npm outdated -g @anthropic-ai/claude-code

# Show available versions
npm view @anthropic-ai/claude-code versions
```

### Notification Setup

Consider setting up notifications for new releases via:
- GitHub watch (releases only)
- npm update notifications
- RSS feed for releases
