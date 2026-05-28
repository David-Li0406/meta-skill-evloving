# Validation Rules & Debugging

## Validation Checklist

### plugin.json Validation
- [ ] File exists at .claude-plugin/plugin.json
- [ ] Valid JSON syntax (no trailing commas, proper quotes)
- [ ] Required field present: "name"
- [ ] Name is kebab-case (lowercase-with-hyphens)
- [ ] Version is valid semver if present (MAJOR.MINOR.PATCH)
- [ ] Author has "name" field if present
- [ ] Paths are relative and start with ./
- [ ] No absolute paths (C:/, /home/, etc.)
- [ ] ${CLAUDE_PLUGIN_ROOT} used for script paths

### Directory Structure Validation
- [ ] .claude-plugin/ dir exists at plugin root
- [ ] Component dirs at plugin root (NOT inside .claude-plugin/)
- [ ] commands/ contains .md files if present
- [ ] skills/ contains dirs with SKILL.md if present
- [ ] hooks/hooks.json exists if hooks referenced
- [ ] .mcp.json exists if MCP servers referenced

### Component File Validation
- [ ] All .md files have valid YAML frontmatter
- [ ] YAML delimiters correct (---)
- [ ] No tabs in YAML (spaces only)
- [ ] Command files in commands/ dir
- [ ] Skills have SKILL.md with name + description frontmatter
- [ ] No broken file references in commands/skills

### Path Validation
- [ ] All referenced files exist
- [ ] Paths use forward slashes (/)
- [ ] No Windows-specific paths (C:\, backslashes)
- [ ] Scripts exist at specified paths
- [ ] Scripts are executable (chmod +x)

### Naming Validation
- [ ] No duplicate command names
- [ ] No duplicate skill names
- [ ] Names follow conventions (kebab-case, gerund for skills)
- [ ] No spaces in file/dir names
- [ ] No special characters except hyphens

### Security Validation
- [ ] No hardcoded credentials
- [ ] No API keys in files
- [ ] No sensitive data in plugin.json
- [ ] Scripts don't execute arbitrary code
- [ ] Bash commands properly restricted

## Debugging

### Enable Debug Mode
```bash
claude --debug
```

Shows:
- Plugin loading sequence
- Manifest parsing
- Component registration
- MCP server initialization
- Hook activation
- Error messages with details

### Common Issues

**Plugin Not Loading**
Symptoms: `/plugin list` doesn't show plugin
Check:
1. plugin.json exists at .claude-plugin/plugin.json
2. JSON syntax valid (use JSON validator)
3. "name" field present
4. Plugin installed: `/plugin list`
5. Restart Claude Code to reload

**Invalid JSON Syntax**
Error: "Failed to parse plugin.json"
Fixes:
- Remove trailing commas
- Use double quotes (not single)
- Escape special characters
- Validate with jsonlint.com

**Commands Not Found**
Symptoms: `/command-name` shows "command not found"
Check:
1. Command file in commands/ dir
2. File has .md extension
3. Filename is lowercase-with-hyphens
4. YAML frontmatter valid (optional but check if present)
5. Restart Claude Code

**Skills Not Activating**
Symptoms: Skill not listed in available skills
Check:
1. Skill dir in skills/ dir
2. SKILL.md exists (exact name)
3. YAML frontmatter has name + description
4. Description includes trigger keywords
5. YAML syntax valid (no tabs)
6. Restart Claude Code

**Hooks Not Firing**
Symptoms: Hook actions not executing
Check:
1. hooks/hooks.json exists
2. Valid JSON syntax
3. Event names correct (PreToolUse, PostToolUse, etc.)
4. Script paths use ${CLAUDE_PLUGIN_ROOT}
5. Scripts are executable
6. Use `claude --debug` to see hook activation

**MCP Servers Not Starting**
Symptoms: MCP tools not available
Check:
1. .mcp.json exists
2. Valid JSON syntax
3. Server command path uses ${CLAUDE_PLUGIN_ROOT}
4. Server binary exists and is executable
5. Environment variables set correctly
6. Use `claude --debug` to see MCP errors

**Wrong Directory Structure**
Error: "Components not found"
Fix:
- Move commands/, skills/, hooks/ to plugin root
- Do NOT put them inside .claude-plugin/
- .claude-plugin/ should only contain plugin.json

**Absolute Paths**
Error: "Path must be relative"
Fix:
- Change C:/path → ./path
- Change /home/path → ./path
- Use ${CLAUDE_PLUGIN_ROOT} for absolute resolution

**Script Not Executable**
Error: "Permission denied"
Fix:
```bash
chmod +x path/to/script.sh
```

**Version Format Invalid**
Error: "Invalid version"
Fix:
- Use semver: 1.0.0 (not 1.0 or v1.0.0)
- Three numbers separated by dots
- No prefix (no "v")

## Validation Commands

### Manual Validation

**Plugin Validation via CLI**:
```bash
# Validate plugin.json syntax
claude plugin validate .

# Validate plugin.json with Python
python -m json.tool .claude-plugin/plugin.json
```

**Plugin Management Commands**:
```bash
# List installed plugins and their status
/plugin list

# List available plugins in a marketplace
/plugin list @marketplace-name

# Show detailed debug information during plugin loading
claude --debug

# Manage plugins
/plugin install plugin-name@marketplace-name
/plugin enable plugin-name@marketplace-name
/plugin disable plugin-name@marketplace-name
/plugin update plugin-name
/plugin uninstall plugin-name@marketplace-name
```

**Marketplace Management Commands**:
```bash
# List configured marketplaces
/plugin marketplace list

# Add a marketplace
/plugin marketplace add ./local-marketplace
/plugin marketplace add owner/repo
/plugin marketplace add https://url/to/marketplace.json

# Update marketplace metadata
/plugin marketplace update marketplace-name

# Remove a marketplace
/plugin marketplace remove marketplace-name
```

**Component Testing**:
```bash
# Test command invocation
/command-name args

# Test skill activation (explicit)
"Use skill-name to..."

# Test hook execution
# Trigger the event that the hook watches for
```

### Automated Validation Script
Create validate-plugin.sh:
```bash
#!/bin/bash
echo "Validating plugin structure..."

# Check plugin.json
if [ ! -f .claude-plugin/plugin.json ]; then
  echo "ERROR: .claude-plugin/plugin.json not found"
  exit 1
fi

# Validate JSON
python -m json.tool .claude-plugin/plugin.json > /dev/null
if [ $? -ne 0 ]; then
  echo "ERROR: Invalid JSON syntax"
  exit 1
fi

# Check required fields
if ! grep -q '"name"' .claude-plugin/plugin.json; then
  echo "ERROR: Missing 'name' field"
  exit 1
fi

echo "✓ Plugin validation passed"
```

## Error Messages Reference

| Error | Cause | Fix |
|-------|-------|-----|
| "Plugin manifest not found" | No plugin.json | Create .claude-plugin/plugin.json |
| "Invalid JSON syntax" | Malformed JSON | Validate JSON syntax |
| "Missing required field: name" | No name field | Add "name": "plugin-name" |
| "Invalid version format" | Bad semver | Use MAJOR.MINOR.PATCH format |
| "Component directory not found" | Wrong structure | Move dirs to plugin root |
| "Script not executable" | Permission issue | chmod +x script |
| "Absolute path not allowed" | Hardcoded path | Use relative paths with ./ |
| "Command already exists" | Name conflict | Rename command file |
| "YAML frontmatter invalid" | Bad YAML | Check delimiters, no tabs |
| "File reference not found" | Broken link | Check file exists |

## Testing Procedure

1. **Syntax Validation**
   ```bash
   python -m json.tool .claude-plugin/plugin.json
   ```

2. **Structure Validation**
   - Verify directory layout
   - Check file locations

3. **Installation Test**
   ```bash
   /plugin install plugin-name@marketplace-name
   ```

4. **Component Tests**
   - Test each command: `/cmd args`
   - Test skill activation: explicit invocation
   - Test hook execution: trigger events
   - Test MCP servers: use MCP tools

5. **Debug Output Review**
   ```bash
   claude --debug
   ```
   Check for errors/warnings

6. **Clean Reinstall**
   ```bash
   /plugin uninstall plugin-name
   /plugin install plugin-name@marketplace-name
   ```

7. **Cross-Platform Test**
   - Test on Windows, Mac, Linux if possible
   - Verify paths work cross-platform
   - Check script compatibility
