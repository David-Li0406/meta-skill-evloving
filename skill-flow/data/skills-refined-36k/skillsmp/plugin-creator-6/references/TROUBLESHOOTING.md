# Troubleshooting Guide

Common issues and solutions for Claude Code plugins.

## Plugin Not Loading

### Symptoms

- Plugin doesn't appear in available plugins
- Components not accessible
- No error message shown

### Solutions

**1. Check .plugin.json syntax**

```bash
python3 -m json.tool .plugin.json
```

Fix any JSON syntax errors.

**2. Verify plugin location**

Plugin must be in `~/.claude/plugins/`:

```bash
ls -la ~/.claude/plugins/
```

Copy if missing:

```bash
cp -r my-plugin ~/.claude/plugins/
```

**3. Restart Claude Code**

Plugins load on startup. Restart after installation.

**4. Check for name conflicts**

Verify no other plugin has the same name.

**5. Check file permissions**

```bash
chmod -R 755 ~/.claude/plugins/my-plugin
```

### Debug Steps

1. Validate JSON
2. Check file structure
3. Verify permissions
4. Check Claude Code logs
5. Try minimal plugin (just .plugin.json)

---

## Command Not Found

### Symptoms

- Command doesn't appear in autocomplete
- `/command-name` doesn't work
- "Command not found" error

### Solutions

**1. Verify command in manifest**

Check `.plugin.json`:

```json
{
  "commands": ["my-command"]
}
```

**2. Check file exists**

```bash
ls commands/my-command.md
```

**3. Verify exact name match**

File name must match manifest name exactly:
- manifest: `"my-command"`
- file: `commands/my-command.md`

**4. Check YAML frontmatter**

```markdown
---
description: Command description
---
```

**5. Reload plugins**

```
/reload-plugins
```

### Debug Steps

1. Check manifest has command listed
2. Verify file exists in commands/
3. Check file name matches exactly
4. Validate YAML frontmatter
5. Check for syntax errors

---

## Agent Not Triggering

### Symptoms

- Agent doesn't activate when expected
- Manual agent launch works but auto-trigger doesn't
- Agent description unclear

### Solutions

**1. Check description clarity**

Description must clearly state when to trigger:

```markdown
---
description: Launch this agent when user asks for codebase analysis or architecture review
---
```

**2. Verify agent in manifest**

```json
{
  "agents": ["my-agent"]
}
```

**3. Check examples provide triggers**

```markdown
examples:
  - trigger: "Analyze this codebase"
    action: "Launch codebase analyzer agent"
```

**4. Verify tools list**

Agent must have tools it needs:

```markdown
tools:
  - Read
  - Write
  - Bash
```

### Debug Steps

1. Review description for clarity
2. Check examples show trigger scenarios
3. Verify tools list is complete
4. Test manual agent launch
5. Check agent logs

---

## Hook Not Executing

### Symptoms

- Hook doesn't run on expected events
- No effect from hook
- Hook silently fails

### Solutions

**1. Verify hook directory**

Hook must be in correct event directory:

```
hooks/pre-tool-use/my-hook.md  # Correct
hooks/my-hook.md               # Wrong
```

**2. Check hook in manifest**

```json
{
  "hooks": {
    "PreToolUse": ["my-hook"]
  }
}
```

**3. Verify event name matches**

Event name in manifest must match directory:
- `PreToolUse` → `pre-tool-use/`
- `PostToolUse` → `post-tool-use/`
- `Stop` → `stop/`

**4. Check YAML frontmatter**

```markdown
---
description: What this hook does
---
```

### Debug Steps

1. Verify hook is in correct event directory
2. Check event name in manifest matches directory
3. Validate YAML frontmatter
4. Add logging to hook to test
5. Check if hook conditions are met

---

## YAML Frontmatter Errors

### Symptoms

- Component fails to load
- "Invalid YAML" error
- Frontmatter not recognized

### Solutions

**1. Check delimiters**

Must have `---` at start and end:

```markdown
---
description: My description
---
```

**2. Verify indentation**

Use spaces, not tabs:

```yaml
---
args:
  - name: my_arg
    description: Argument description
    required: true
---
```

**3. Check required fields**

Every component needs at least `description`:

```markdown
---
description: Clear description
---
```

**4. Validate YAML syntax**

Use online YAML validator or:

```bash
python3 -c "import yaml; yaml.safe_load(open('file.md'))"
```

### Common YAML Errors

1. **Tabs instead of spaces** → Use 2 spaces for indentation
2. **Missing colons** → `key: value`
3. **Unquoted special characters** → Quote strings with `:`, `{`, `}`, `[`, `]`
4. **Missing dashes for arrays** → `- item` not `item`

---

## File Not Found Errors

### Symptoms

- "File not found" when accessing component
- Path issues
- Relative path problems

### Solutions

**1. Use absolute paths**

```markdown
Read ${CLAUDE_PLUGIN_ROOT}/config.json
```

**2. Check working directory**

Current directory is project root, not plugin directory.

**3. Verify file structure**

```
plugin-name/
├── .plugin.json
├── README.md
├── commands/
│   └── command.md
```

---

## Performance Issues

### Symptoms

- Slow plugin loading
- Laggy command execution
- High memory usage

### Solutions

**1. Optimize hook performance**

Hooks run on every event, keep them fast:

```markdown
<!-- Bad: Expensive operation -->
---
description: Log all operations
---

Run full scan of filesystem...

<!-- Good: Simple operation -->
---
description: Log critical operations
---

Append to log file...
```

**2. Reduce references loaded**

Use progressive disclosure:

```markdown
See [ADVANCED.md](references/ADVANCED.md) for details
```

**3. Cache expensive operations**

```markdown
Check cache first, only compute if missing.
```

---

## Environment-Specific Issues

### Windows

**Path separators:**

```bash
# Wrong
path = "plugins\my-plugin"

# Correct
path = "plugins/my-plugin"
```

**Line endings:**

```bash
# Convert CRLF to LF
dos2unix file.md
```

### macOS/Linux

**Permissions:**

```bash
chmod +x scripts/*.sh
```

**Case sensitivity:**

File names are case-sensitive:
- `MyCommand.md` ≠ `mycommand.md`

---

## Getting Help

### Gather Information

1. Claude Code version
2. Plugin name and version
3. Operating system
4. Error messages
5. Steps to reproduce

### Useful Commands

```bash
# Check plugin structure
ls -R plugin-name/

# Validate JSON
python3 -m json.tool .plugin.json

# Check YAML
yamllint commands/*.md

# View logs
tail -f ~/.claude/logs/*.log
```

### Resources

- Official docs: https://code.claude.com/docs/zh-CN/plugins
- GitHub issues: https://github.com/anthropics/claude-code/issues
- Community: Check forums for similar issues

---

## Quick Diagnostic Checklist

### Plugin Loading

- [ ] .plugin.json valid JSON
- [ ] Plugin in correct location
- [ ] Restarted Claude Code
- [ ] No name conflicts
- [ ] File permissions correct

### Commands

- [ ] Command listed in manifest
- [ ] File exists in commands/
- [ ] File name matches exactly
- [ ] Valid YAML frontmatter
- [ ] Description present

### Agents

- [ ] Agent listed in manifest
- [ ] File exists in agents/
- [ ] Clear trigger description
- [ ] Examples provided
- [ ] Tools list complete

### Skills

- [ ] Skill listed in manifest
- [ ] File exists in skills/
- [ ] Description clear (what + when)
- [ ] Content focused
- [ ] Examples practical

### Hooks

- [ ] Hook in correct event directory
- [ ] Event name in manifest matches
- [ ] YAML frontmatter valid
- [ ] Behavior documented
- [ ] Side effects noted

### All Components

- [ ] YAML frontmatter valid
- [ ] Description present and clear
- [ ] Instructions comprehensive
- [ ] Examples provided
- [ ] Tested in isolation
