# Auto-Discovery Mechanism

## Table of Contents

- [Overview](#overview)
- [Discovery Process](#discovery-process)
- [Discovery Timing](#discovery-timing)
- [Override Behavior](#override-behavior)
- [Auto-Discovery Validation](#auto-discovery-validation)
- [Troubleshooting Discovery](#troubleshooting-discovery)
- [Best Practices](#best-practices)
- [Integration with Progressive Disclosure](#integration-with-progressive-disclosure)
- [Performance Considerations](#performance-considerations)
- [Version Compatibility](#version-compatibility)

## Overview

Claude Code automatically discovers and loads plugin components without manual registration. This ensures seamless integration and reduces configuration overhead.

## Discovery Process

### Step 1: Plugin Manifest Loading

When a plugin is enabled, Claude Code:

1. **Locates manifest**: Reads `.claude-plugin/plugin.json`
2. **Validates structure**: Checks required fields
3. **Registers plugin**: Adds to available plugins list
4. **Scans for components**: Initiates auto-discovery

**Manifest location**:
- ✅ Correct: `.claude-plugin/plugin.json`
- ❌ Wrong: `plugin.json` (root level)
- ❌ Wrong: `config/plugin.json`
- ❌ Wrong: `plugins/plugin.json`

### Step 2: Component Scanning

Claude Code scans for components in this order:

#### Commands Discovery
```
Scans: commands/ directory
Pattern: *.md files
Registration: As slash commands (/command-name)
```

**Auto-loading behavior**:
- All `.md` files in `commands/` load automatically
- No manual registration required
- File name becomes command name
- YAML frontmatter parsed for metadata

**Example**:
```
commands/
├── review.md       → Loads as /review
├── test.md         → Loads as /test
└── deploy.md       → Loads as /deploy
```

#### Agents Discovery
```
Scans: agents/ directory
Pattern: *.md files
Registration: As available agents
```

**Auto-loading behavior**:
- All `.md` files in `agents/` load automatically
- Available for manual invocation
- Claude Code may auto-select based on context
- YAML frontmatter parsed for triggering conditions

**Example**:
```
agents/
├── code-reviewer.md    → Available as agent
├── test-generator.md   → Available as agent
└── refactorer.md       → Available as agent
```

#### Skills Discovery
```
Scans: skills/ directory
Pattern: skill-name/SKILL.md files
Registration: As auto-activating skills
```

**Auto-loading behavior**:
- Scans `skills/` for subdirectories
- Looks for `SKILL.md` in each subdirectory
- Auto-activates based on description matching
- Progressive disclosure loads metadata first

**Example**:
```
skills/
├── api-testing/         → Loads skill
│   └── SKILL.md
├── database-migrations/ → Loads skill
│   └── SKILL.md
└── error-handling/      → Loads skill
    └── SKILL.md
```

**Important**: Skill directory MUST contain `SKILL.md`
- ❌ Wrong: `skills/skill-name/README.md`
- ❌ Wrong: `skills/skill-name/index.md`
- ✅ Correct: `skills/skill-name/SKILL.md`

#### Hooks Discovery
```
Scans: hooks/hooks.json OR plugin.json
Pattern: hooks configuration
Registration: Event listeners
```

**Auto-loading behavior**:
- Reads `hooks/hooks.json` if exists
- OR reads `hooks` array in `plugin.json`
- Registers event listeners automatically
- Hooks active immediately on plugin enable

**Example locations**:
```
Option 1: Separate file
hooks/
└── hooks.json

Option 2: Inline in manifest
.claude-plugin/
└── plugin.json
    {
      "name": "my-plugin",
      "hooks": [...]
    }
```

#### MCP Servers Discovery
```
Scans: .mcp.json OR plugin.json
Pattern: MCP server configurations
Registration: External tool integrations
```

**Auto-loading behavior**:
- Reads `.mcp.json` if exists
- OR reads `mcpServers` in `plugin.json`
- Starts MCP servers automatically
- Registers Tools, Resources, Prompts

**Example locations**:
```
Option 1: Separate file
.mcp.json

Option 2: Inline in manifest
.claude-plugin/
└── plugin.json
    {
      "name": "my-plugin",
      "mcpServers": [...]
    }
```

## Discovery Timing

### Plugin Installation
```
Phase: Plugin added to system
Action: Components register with Claude Code
Result: Plugin appears in plugin list
```

### Plugin Enable
```
Phase: User enables plugin
Action: Components become active
Result: Commands, agents, skills available
```

### Session Start
```
Phase: New Claude Code session
Action: All enabled plugins load
Result: All components ready to use
```

### No Restart Required
```
Changes: Update component files
Behavior: Active on next session
Timing: Immediate after session restart
```

## Override Behavior

### Custom Paths

Custom paths in `plugin.json` **supplement** (not replace) defaults:

```json
{
  "name": "my-plugin",
  "commands": "./custom-commands",
  "agents": ["./agents", "./specialized-agents"]
}
```

**Behavior**:
- Loads from `commands/` (default)
- ALSO loads from `custom-commands/` (custom)
- Loads from `agents/` (default)
- ALSO loads from `specialized-agents/` (custom)

**Both locations active**:
```
Default: commands/    → /command1, /command2
Custom:  custom-cmds/ → /custom1, /custom2
```

### Path Requirements

**Relative paths only**:
- ✅ Correct: `"./commands"`
- ✅ Correct: `["./agents", "./specialized"]`
- ❌ Wrong: `"/absolute/path"`
- ❌ Wrong: `"commands"`

**Must start with `./`**:
- ✅ Correct: `"./custom-dir"`
- ❌ Wrong: `"custom-dir"`

**Supports arrays**:
```json
{
  "agents": ["./agents", "./specialized-agents", "./experimental"]
}
```

## Auto-Discovery Validation

### File Requirements

**Commands**:
- Location: `commands/` directory
- Extension: `.md` (markdown)
- Frontmatter: YAML between `---` markers
- Body: Markdown content

**Agents**:
- Location: `agents/` directory
- Extension: `.md` (markdown)
- Frontmatter: YAML between `---` markers
- Body: Agent instructions

**Skills**:
- Location: `skills/skill-name/` directory
- Required file: `SKILL.md` (exact name)
- Extension: `.md` (markdown)
- Frontmatter: YAML between `---` markers

**Hooks**:
- Location: `hooks/hooks.json` OR `plugin.json`
- Format: Valid JSON
- Structure: Event → matcher → hooks array

**MCP Servers**:
- Location: `.mcp.json` OR `plugin.json`
- Format: Valid JSON
- Structure: Server name → configuration

### Naming Requirements

**Directories**:
- Kebab-case (lowercase with hyphens)
- No spaces or special characters
- Descriptive of purpose

**Files**:
- Kebab-case for commands/agents
- `SKILL.md` exact for skills
- `.json` for configuration files

**Examples**:
```
✅ Good:
commands/code-review.md
agents/test-generator.md
skills/api-testing/SKILL.md
hooks/hooks.json

❌ Bad:
commands/codeReview.md
agents/test generator.md
skills/api_testing/README.md
```

## Troubleshooting Discovery

### Component Not Loading

**Checklist**:
- [ ] File in correct directory?
- [ ] Correct file extension?
- [ ] Valid YAML frontmatter (if required)?
- [ ] Plugin enabled in settings?
- [ ] Restarted Claude Code?

**Skills-specific**:
- [ ] Directory contains `SKILL.md` (not other names)?
- [ ] SKILL.md has valid YAML frontmatter?
- [ ] Skill directory name is kebab-case?

### Auto-Discovery Not Working

**Debug steps**:

1. **Verify manifest**:
   ```bash
   cat .claude-plugin/plugin.json
   # Should be valid JSON
   ```

2. **Check component locations**:
   ```bash
   ls -la commands/     # Should show .md files
   ls -la agents/       # Should show .md files
   ls -la skills/       # Should show skill directories
   ```

3. **Validate file structure**:
   ```bash
   # Skills check
   find skills -name "SKILL.md"
   
   # Hooks check
   cat hooks/hooks.json  # If exists
   ```

4. **Restart Claude Code**:
   - Changes take effect on next session
   - No manual reload required

### Custom Paths Not Loading

**Debug steps**:

1. **Check path format**:
   - Must be relative: `"./custom-dir"`
   - Must start with `./`
   - Cannot be absolute

2. **Verify directory exists**:
   ```bash
   ls -la ./custom-commands  # Should exist
   ```

3. **Check file names**:
   - Same requirements as default locations
   - `.md` files for commands/agents

4. **Review manifest**:
   ```json
   {
     "commands": "./custom-commands",
     "agents": ["./agents", "./custom-agents"]
   }
   ```

### Path Resolution Errors

**Common issues**:

1. **Hardcoded paths**:
   ❌ Wrong:
   ```json
   "command": "/Users/name/plugins/my-plugin/scripts/run.sh"
   ```
   ✅ Correct:
   ```json
   "command": "${CLAUDE_PLUGIN_ROOT}/scripts/run.sh"
   ```

2. **Relative paths from wrong location**:
   ❌ Wrong:
   ```markdown
   Run script: ./scripts/helper.sh  # Relative to current directory
   ```
   ✅ Correct:
   ```markdown
   Run script: ${CLAUDE_PLUGIN_ROOT}/scripts/helper.sh
   ```

3. **Missing environment variable**:
   ❌ Wrong:
   ```bash
   source "scripts/common.sh"  # $CLAUDE_PLUGIN_ROOT not set
   ```
   ✅ Correct:
   ```bash
   source "${CLAUDE_PLUGIN_ROOT}/lib/common.sh"
   ```

## Best Practices

### Organization

1. **Default locations first**: Use standard directories before custom paths
2. **Logical grouping**: Group related components together
3. **Clear naming**: Use descriptive, consistent names
4. **Minimal manifest**: Don't over-configure

### Discovery Optimization

1. **Limit component count**: Don't create unnecessary components
2. **Clear descriptions**: Help Claude Code auto-select appropriately
3. **Consistent patterns**: Same structure across similar components
4. **Regular validation**: Periodically check all components load

### Testing Discovery

1. **Enable/disable cycle**: Test plugin disable/enable
2. **Component isolation**: Test each component independently
3. **Cross-platform**: Verify discovery works on all OS
4. **Version updates**: Check discovery after updates

## Integration with Progressive Disclosure

### Skill Discovery Flow

```
Tier 1: Metadata (~100 words)
├── name, description loaded
└── Auto-activates based on description

Tier 2: SKILL.md body (~2,000 words)
├── Full skill guidance
└── Loaded on skill activation

Tier 3: references/, examples/, scripts/
├── Detailed documentation
├── Working examples
├── Utility scripts
└── Loaded on-demand
```

### Command/Agent Discovery

```
Discovery: Immediate on plugin enable
Activation: On user invocation
Auto-selection: Based on description/context
```

## Performance Considerations

### Discovery Efficiency

- **Parallel scanning**: Components scanned concurrently
- **Lazy loading**: Skills load metadata first, body on activation
- **Caching**: Discovery results cached per session
- **Incremental**: Only changed files re-scanned

### Large Plugin Optimization

- **Component count**: Limit to necessary components only
- **Directory structure**: Use subdirectories for organization
- **File size**: Keep SKILL.md under size limits
- **Reference files**: Move detailed content to references/

## Version Compatibility

### Discovery Changes

- **Backward compatible**: Older plugins continue working
- **New features**: 2026 features optional
- **Graceful degradation**: Missing features don't break discovery
- **Migration guides**: Document breaking changes

### Testing Compatibility

- **Multiple versions**: Test with different Claude Code versions
- **Feature flags**: New features behind optional configuration
- **Documentation**: Clear upgrade paths for users
