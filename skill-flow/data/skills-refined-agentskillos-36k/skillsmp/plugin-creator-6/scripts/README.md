# Plugin Creator Scripts

Helper scripts for creating, validating, and packaging Claude Code plugins.

## Scripts

### init_plugin.py

Initialize a new plugin directory with template files.

```bash
python init_plugin.py <plugin-name>
```

**Creates:**
- `.plugin.json` - Plugin manifest
- `README.md` - Documentation template
- `commands/` - Command directory
- `agents/` - Agent directory
- `skills/` - Skill directory
- `hooks/` - Hook directory with event subdirectories
- Example component files with templates

**Example:**
```bash
python init_plugin.py code-reviewer
```

### validate_plugin.py

Validate plugin structure and content.

```bash
python validate_plugin.py <plugin-path>
```

**Validates:**
- JSON syntax in `.plugin.json`
- Required fields (name, version, description)
- Naming conventions (kebab-case)
- YAML frontmatter in component files
- Component files exist if declared in manifest
- Hook event types are valid

**Example:**
```bash
python validate_plugin.py ./my-plugin
```

### package_plugin.py

Package plugin into a distributable archive.

```bash
python package_plugin.py <plugin-path> [output-directory]
```

**Process:**
1. Runs validation
2. Creates `.zip` archive
3. Includes all plugin files

**Example:**
```bash
python package_plugin.py ./my-plugin ./dist
```

## Workflow

1. **Initialize**: `python init_plugin.py my-plugin`
2. **Edit files**: Implement your plugin
3. **Validate**: `python validate_plugin.py my-plugin`
4. **Package**: `python package_plugin.py my-plugin`
5. **Distribute**: Share the `.zip` file

## Requirements

- Python 3.6+
- PyYAML (`pip install pyyaml` or `pip install -r requirements.txt`)
