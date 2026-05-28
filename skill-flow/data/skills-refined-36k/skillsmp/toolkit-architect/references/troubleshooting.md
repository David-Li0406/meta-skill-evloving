# Troubleshooting Guide

## Table of Contents

- [Common Issues and Solutions](#common-issues-and-solutions)
- [Debugging Tools](#debugging-tools)
- [Performance Issues](#performance-issues)
- [Migration Issues](#migration-issues)
- [Getting Help](#getting-help)
- [Prevention Best Practices](#prevention-best-practices)
- [Quick Reference](#quick-reference)

## Common Issues and Solutions

### Component Not Loading

#### Symptoms
- Command `/my-command` not found
- Agent not appearing in available agents
- Skill not auto-activating
- Hook not executing

#### Diagnosis Steps

**1. Check file location**
```bash
# Verify component is in correct directory
ls -la commands/     # Commands should be here
ls -la agents/       # Agents should be here
ls -la skills/       # Skill directories should be here
ls -la hooks/        # hooks.json should be here
```

**2. Verify file extensions**
```bash
# Commands and agents must be .md files
file commands/my-command.md    # Should show: Markdown
file agents/my-agent.md       # Should show: Markdown

# Skills must have SKILL.md (exact name)
file skills/my-skill/SKILL.md # Should show: Markdown
```

**3. Check plugin status**
```bash
# Verify plugin is enabled
# Check Claude Code settings → Plugins
# Ensure plugin shows as "Enabled"
```

**4. Restart Claude Code**
- Changes take effect on next session
- No manual reload required

#### Solutions

**File in wrong location**:
```
❌ Wrong:
skills/my-skill/README.md
skills/my-skill/index.md

✅ Correct:
skills/my-skill/SKILL.md
```

**Plugin not enabled**:
- Go to Claude Code settings
- Find plugin in list
- Click "Enable"

**After fixes**:
- Restart Claude Code
- Start new session
- Check component is available

### Path Resolution Errors

#### Symptoms
- Script not found errors
- Command execution failures
- `${CLAUDE_PLUGIN_ROOT}` not expanding
- File path errors in logs

#### Diagnosis Steps

**1. Check for hardcoded paths**
```bash
# Search for absolute paths in config files
grep -r "/Users/" hooks/hooks.json
grep -r "/home/" .mcp.json
```

**2. Verify environment variable**
```bash
# In hook script
echo $CLAUDE_PLUGIN_ROOT
# Should output plugin directory path
```

**3. Check path format in JSON**
```json
// ❌ Wrong: Missing ${}
"command": "scripts/run.sh"

// ✅ Correct: With ${}
"command": "${CLAUDE_PLUGIN_ROOT}/scripts/run.sh"
```

#### Solutions

**Replace hardcoded paths**:
```json
// ❌ Wrong
{
  "command": "/Users/name/plugins/my-plugin/scripts/run.sh"
}

// ✅ Correct
{
  "command": "${CLAUDE_PLUGIN_ROOT}/scripts/run.sh"
}
```

**Fix relative paths**:
```json
// ❌ Wrong: Relative to working directory
{
  "command": "./scripts/run.sh"
}

// ✅ Correct: Using environment variable
{
  "command": "${CLAUDE_PLUGIN_ROOT}/scripts/run.sh"
}
```

**Update script references**:
```bash
# ❌ Wrong
source "scripts/common.sh"

# ✅ Correct
source "${CLAUDE_PLUGIN_ROOT}/lib/common.sh"
```

### Auto-Discovery Not Working

#### Symptoms
- New components don't appear
- Modified components still show old behavior
- Custom paths not loading

#### Diagnosis Steps

**1. Verify directory structure**
```
plugin-name/
├── .claude-plugin/
│   └── plugin.json     ← Should exist
├── commands/           ← Should exist
├── agents/             ← Should exist
└── skills/             ← Should exist
```

**2. Check custom paths**
```json
// In plugin.json
{
  "commands": "./custom-commands"  ← Must start with ./
}
```

**3. Verify file naming**
```bash
# Should be kebab-case
ls commands/            # Check: my-command.md ✓
                       # Check: my command.md ✗
```

#### Solutions

**Fix custom path format**:
```json
{
  "commands": "./custom-commands"  // ✓ Starts with ./
}

// Not:
{
  "commands": "custom-commands"   // ✗ Missing ./
}
```

**Create missing directories**:
```bash
mkdir -p commands
mkdir -p agents
mkdir -p skills
```

**Restart after changes**:
- Changes take effect on next session
- No manual reload

### Plugin Conflicts

#### Symptoms
- Commands with same name
- Unexpected component behavior
- Multiple plugins affecting same workflow

#### Diagnosis Steps

**1. List all plugins**
- Check Claude Code settings → Plugins
- Identify conflicting plugins

**2. Check component names**
```bash
# Find duplicate command names
ls commands/           # Check for duplicates
```

**3. Review plugin priorities**
- Some plugins may have precedence
- Check documentation

#### Solutions

**Use unique names**:
```
❌ Conflicting:
plugin-a/commands/deploy.sh
plugin-b/commands/deploy.sh

✅ Unique:
plugin-a/commands/deploy-app.sh
plugin-b/commands/deploy-db.sh
```

**Namespace components**:
```json
{
  "name": "my-plugin",
  "commands": "./commands/my-plugin-"
}
```

**Document conflicts**:
- Add README to plugin
- Note potential conflicts
- Provide workarounds

### YAML Frontmatter Errors

#### Symptoms
- Component loads but doesn't work
- Description not showing
- Metadata missing

#### Diagnosis Steps

**1. Validate YAML syntax**
```bash
# Check YAML is valid
python -c "import yaml; yaml.safe_load(open('commands/my-command.md'))"
```

**2. Check frontmatter markers**
```markdown
---
name: my-command
description: My command description
---

Content here
```

**3. Verify required fields**
- Commands: `name`, `description`
- Agents: `name`, `description`
- Skills: `name`, `description`

#### Solutions

**Fix YAML syntax**:
```markdown
---
# ❌ Wrong: Missing quotes
name: my command

# ✅ Correct: Proper formatting
name: my-command
description: "My command description"
---
```

**Add missing fields**:
```markdown
---
name: my-command           # ✓ Required
description: "Description" # ✓ Required
allowed-tools: []          # Optional
---
```

### Skill-Specific Issues

#### Symptoms
- Skill not auto-activating
- Description not matching
- References not loading

#### Diagnosis Steps

**1. Verify skill structure**
```
skills/my-skill/
├── SKILL.md           ← Must exist
├── references/        ← Optional
└── examples/          ← Optional
```

**2. Check SKILL.md frontmatter**
```yaml
---
name: my-skill              # Required
description: "Use when..."  # Required
version: 2.0.0             # Optional
context: standard           # 2026: Optional
tags: [tag1, tag2]         # 2026: Optional
---
```

**3. Verify description format**
```yaml
description: "WHAT + WHEN + NOT formula"
```

#### Solutions

**Fix skill directory**:
```
❌ Wrong:
skills/README.md           # Wrong file name

✅ Correct:
skills/my-skill/
└── SKILL.md              # Correct file name
```

**Improve description**:
```yaml
# ❌ Too vague
description: "Helps with testing"

# ✅ Clear triggers
description: "Use when running tests, generating test cases, or analyzing coverage. Do not use for production deployment."
```

**Update to 2026 format**:
```yaml
---
name: my-skill
description: "Use when [trigger]. Do not use for [exclusion]."
version: 2.0.0
context: standard
tags: [development, testing]
---
```

### Hook-Specific Issues

#### Symptoms
- Hook not triggering
- Events not firing
- Script errors

#### Diagnosis Steps

**1. Check hook configuration**
```json
{
  "PermissionRequest": [    ← 2026: NEW event
    {
      "matcher": "*",        ← Match pattern
      "hooks": [{            ← Array of hooks
        "type": "command",
        "command": "bash ${CLAUDE_PLUGIN_ROOT}/scripts/hook.sh"
      }]
    }
  ]
}
```

**2. Verify event name**
- 2026: Use `PermissionRequest` (not `PostToolUse`)
- Use `SessionStart`, `SessionEnd`
- Use `Notification` with subtypes

**3. Test script manually**
```bash
# Run hook script directly
bash ${CLAUDE_PLUGIN_ROOT}/scripts/hook.sh
```

#### Solutions

**Fix event names**:
```json
{
  // ❌ Deprecated (removed in 2026)
  "PostToolUse": [...],
  "PreCompact": [...],
  
  // ✅ 2026 events
  "PermissionRequest": [...],
  "SessionStart": [...],
  "SessionEnd": [...],
  "Notification": [...]
}
```

**Fix hook script**:
```bash
#!/bin/bash
set -e  # Exit on error
# Use environment variable
source "${CLAUDE_PLUGIN_ROOT}/lib/common.sh"
```

**Add error handling**:
```json
{
  "PermissionRequest": [{
    "matcher": "*",
    "hooks": [{
      "type": "command",
      "command": "bash ${CLAUDE_PLUGIN_ROOT}/scripts/hook.sh",
      "timeout": 30,
      "once": true
    }]
  }]
}
```

### MCP Server Issues

#### Symptoms
- Server not connecting
- Tools not available
- Authentication failures

#### Diagnosis Steps

**1. Check MCP configuration**
```json
{
  "server-name": {
    "type": "streamable-http",    ← 2026: stdio or streamable-http
    "url": "https://...",          ← Required for streamable-http
    "version": "2026-01-20",       ← 2026: Date-based
    "resources": [...],           ← 2026: Resources primitive
    "prompts": [...]              ← 2026: Prompts primitive
  }
}
```

**2. Verify transport type**
- `stdio`: Requires `command` field
- `streamable-http`: Requires `url` field

**3. Check authentication**
```json
{
  "type": "streamable-http",
  "url": "https://...",
  "headers": {
    "Authorization": "Bearer ${API_TOKEN}"
  }
}
```

#### Solutions

**Fix transport configuration**:
```json
{
  "server-name": {
    "type": "stdio",              // For local process
    "command": "node",
    "args": ["server.js"]
  }
}

// OR
{
  "server-name": {
    "type": "streamable-http",   // For hosted service
    "url": "https://mcp.example.com/stream"
  }
}
```

**Fix authentication**:
```bash
# Set environment variable
export API_TOKEN="your-token-here"
```

**Update to 2026 format**:
```json
{
  "server-name": {
    "type": "streamable-http",
    "url": "https://mcp.example.com/stream",
    "version": "2026-01-20",     // Date-based versioning
    "resources": [...],           // Resources primitive
    "prompts": [...]             // Prompts primitive
  }
}
```

## Debugging Tools

### Enable Debug Logging

**Command line**:
```bash
claude --debug
```

**Look for**:
- Plugin loading messages
- Component discovery logs
- Hook execution traces
- MCP server connections
- Tool call errors

### Check Component Status

**List all components**:
```bash
# Commands
ls commands/

# Agents
ls agents/

# Skills
ls skills/*/SKILL.md

# Hooks
cat hooks/hooks.json

# MCP
cat .mcp.json
```

### Validate Configuration

**JSON validation**:
```bash
# Validate plugin.json
python -m json.tool .claude-plugin/plugin.json

# Validate hooks.json
python -m json.tool hooks/hooks.json

# Validate .mcp.json
python -m json.tool .mcp.json
```

**YAML validation**:
```bash
# Validate command frontmatter
python -c "import yaml; yaml.safe_load(open('commands/test.md'))"
```

## Performance Issues

### Slow Plugin Loading

**Symptoms**:
- Long startup time
- Delayed component availability

**Solutions**:
1. **Reduce component count**: Remove unused components
2. **Optimize SKILL.md**: Keep under size limits
3. **Move content to references/**: Use progressive disclosure
4. **Limit hook complexity**: Simple, fast hooks

### High Resource Usage

**Symptoms**:
- High memory usage
- CPU spikes

**Solutions**:
1. **Profile scripts**: Identify bottlenecks
2. **Optimize hooks**: Reduce frequency
3. **Cache data**: Store computed results
4. **Lazy loading**: Load on-demand

## Migration Issues

### Upgrading from v1/v2

**Common problems**:
- Deprecated events in hooks
- Old configuration format
- Missing 2026 features

**Solutions**:
1. **Update hook events**: Replace deprecated events
2. **Migrate to 2026 format**: Add new fields
3. **Test thoroughly**: Verify all components work
4. **Read migration guide**: Follow official docs

### Breaking Changes

**Common issues**:
- Event names changed
- Configuration format updated
- Required fields added

**Solutions**:
1. **Read release notes**: Understand changes
2. **Update gradually**: One component at a time
3. **Test in isolation**: Verify each update
4. **Rollback if needed**: Keep backup of working version

## Getting Help

### Documentation

**Core guides**:
- `.claude/skills/skills-knowledge/SKILL.md`
- `.claude/skills/commands-knowledge/SKILL.md`
- `.claude/skills/hooks-knowledge/SKILL.md`
- `.claude/skills/mcp-knowledge/SKILL.md`

**Examples**:
- `examples/` directory in plugin
- Reference files in `references/`

### Validation Tools

**Plugin validator**:
```bash
# Use plugin-validator agent
# Validates structure, configuration, 2026 compliance
```

**Manual checks**:
```bash
# Check file structure
find . -type f -name "*.md" | head -20

# Verify frontmatter
grep -l "^---" commands/*.md

# Check JSON syntax
find . -name "*.json" -exec python -m json.tool {} \;
```

### Common Error Messages

**"Component not found"**:
- File in wrong location
- Wrong file extension
- Plugin not enabled

**"Invalid YAML"**:
- Frontmatter syntax error
- Missing quotes
- Indentation issues

**"Path not found"**:
- Hardcoded absolute path
- Missing ${CLAUDE_PLUGIN_ROOT}
- Relative path from wrong location

**"Hook not triggering"**:
- Wrong event name
- Script error
- Timeout too short

## Prevention Best Practices

### Before Creating Components

1. **Plan structure**: Sketch directory layout
2. **Choose names**: Descriptive, consistent
3. **Validate concept**: Ensure component is necessary
4. **Check examples**: Review similar components

### During Development

1. **Test incrementally**: Add one component at a time
2. **Use debug mode**: Enable logging
3. **Validate often**: Check JSON/YAML syntax
4. **Document changes**: Track modifications

### Before Publishing

1. **Run validation**: Use plugin-validator
2. **Test thoroughly**: All components work
3. **Cross-platform**: Test on multiple OS
4. **Performance check**: No slow loading
5. **Documentation**: README and examples

## Quick Reference

### File Locations
```
.claude-plugin/plugin.json  ← Plugin manifest
commands/*.md             ← Commands
agents/*.md               ← Agents
skills/*/SKILL.md         ← Skills
hooks/hooks.json          ← Hooks
.mcp.json                 ← MCP servers
scripts/                  ← Shared scripts
```

### Required Files
```
Plugin: .claude-plugin/plugin.json
Skill: skills/*/SKILL.md
Command: commands/*.md
Agent: agents/*.md
```

### Environment Variables
```
${CLAUDE_PLUGIN_ROOT}     ← Plugin directory
${API_TOKEN}              ← User-defined
${DB_URL}                 ← User-defined
```

### Common Commands
```bash
# Enable debug
claude --debug

# List components
ls commands/ agents/ skills/*/SKILL.md

# Validate JSON
python -m json.tool file.json

# Validate YAML
python -c "import yaml; yaml.safe_load(open('file.md'))"
```
