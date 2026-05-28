# Marketplace Scripts Reference

Guide to using skill-creator scripts from the Anthropic marketplace.

## Script Locations

**Do not copy scripts to user skills** - Reference marketplace location:

```
/Users/terryli/.claude/plugins/marketplaces/anthropic-agent-skills/skill-creator/scripts/
├── init_skill.py (303 lines)
├── package_skill.py (110 lines)
└── quick_validate.py (65 lines)
```

## init_skill.py - Scaffold New Skills

Generates skill template with proper structure.

### Usage

```bash
/Users/terryli/.claude/plugins/marketplaces/anthropic-agent-skills/skill-creator/scripts/init_skill.py <skill-name> --path <output-directory>
```

### Example

```bash
# Create new skill in user skills directory
/Users/terryli/.claude/plugins/marketplaces/anthropic-agent-skills/skill-creator/scripts/init_skill.py pdf-editor --path ~/.claude/skills/

# Creates:
~/.claude/skills/pdf-editor/
├── SKILL.md (template with TODOs)
├── scripts/
│   └── example_script.py
├── references/
│   └── example_reference.md
└── assets/
    └── example_asset.txt
```

### What It Generates

**SKILL.md template** with:
- Proper YAML frontmatter
- TODO placeholders for customization
- Sections: About, Capabilities, Usage
- Reference links template

**Example directories**:
- `scripts/example_script.py` - Delete or customize
- `references/example_reference.md` - Delete or customize
- `assets/example_asset.txt` - Delete or customize

### After Initialization

1. Delete unused example files
2. Fill in TODO placeholders
3. Add actual scripts/references/assets
4. Update description with trigger keywords
5. **Validate with quick_validate.py** (see below)

## quick_validate.py - Validation Only (Recommended)

**Primary validation tool** - validates skill structure WITHOUT creating zip files.

### CLI Usage (Primary Use Case)

```bash
/Users/terryli/.claude/plugins/marketplaces/anthropic-agent-skills/skill-creator/scripts/quick_validate.py <path/to/skill-folder>
```

### Example

```bash
# Validate documentation-standards skill
/Users/terryli/.claude/plugins/marketplaces/anthropic-agent-skills/skill-creator/scripts/quick_validate.py ~/.claude/skills/documentation-standards/

# Output: "Skill is valid!" or error messages
```

### Validation Checks

**YAML Frontmatter**:
- [ ] Required fields: `name`, `description`
- [ ] Name format: lowercase, hyphens, numbers only (no underscores!)
- [ ] Name length: ≤64 chars
- [ ] Description: no angle brackets (< >)
- [ ] Valid YAML syntax

**File Structure**:
- [ ] SKILL.md exists
- [ ] Proper directory organization

### When to Use

- ✅ **Local development** - validate before committing
- ✅ **Iterative updates** - check after edits
- ✅ **CI/CD pipelines** - automated validation
- ✅ **Pre-commit hooks** - prevent invalid commits

### Python API Usage (Advanced)

```python
from quick_validate import validate_skill

valid, message = validate_skill("/path/to/skill")
if not valid:
    print(f"Validation failed: {message}")
else:
    print("Skill valid!")
```

## package_skill.py - Validate + Package (For claude.ai/Desktop Only)

Validates skill structure AND creates distributable zip.

**⚠️ IMPORTANT**: This is **NOT needed for Claude Code CLI**. Only use for claude.ai (web) or Claude Desktop where skills are uploaded as ZIP files.

**For Claude Code CLI**: Skills are directories in `~/.claude/skills/` - no zips needed!

### Usage

```bash
# Package to current directory
/Users/terryli/.claude/plugins/marketplaces/anthropic-agent-skills/skill-creator/scripts/package_skill.py <path/to/skill-folder>

# Package to specific output directory
/Users/terryli/.claude/plugins/marketplaces/anthropic-agent-skills/skill-creator/scripts/package_skill.py <path/to/skill-folder> ./dist
```

### Example

```bash
# Package pdf-editor skill
/Users/terryli/.claude/plugins/marketplaces/anthropic-agent-skills/skill-creator/scripts/package_skill.py ~/.claude/skills/pdf-editor/

# Output: pdf-editor.zip
```

### When to Use

**Claude Code CLI** (our environment):
- ❌ **NEVER** - Skills are directories in `~/.claude/skills/`, no zips needed
- ✅ Use `quick_validate.py` for validation instead

**claude.ai (web) or Claude Desktop**:
- ✅ Preparing skills for upload via "Upload skill" button
- ✅ Distributing skills to users on those platforms

### What It Does

1. **Validates** using same checks as quick_validate.py
2. **Creates zip** file with complete skill structure
3. **Outputs** to current directory or specified location

If validation fails, no zip is created.

### Output

**Success**: Creates `<skill-name>.zip` with complete skill structure:
```
pdf-editor.zip
└── pdf-editor/
    ├── SKILL.md
    ├── scripts/
    ├── references/
    └── assets/
```

**Distribution**: Share zip file with users for installation.

## quick_validate.py - Standalone Validation

Validation module used by package_skill.py.

### Usage

```python
from quick_validate import validate_skill

errors = validate_skill("/path/to/skill")
if errors:
    print(f"Validation failed: {errors}")
else:
    print("Skill valid!")
```

### Use Cases

- **Pre-commit hook**: Validate before committing
- **CI/CD**: Automated validation in pipelines
- **Custom tooling**: Build on validation logic

### Example Integration

```bash
# Git pre-commit hook
#!/bin/bash
python3 /Users/terryli/.claude/plugins/marketplaces/anthropic-agent-skills/skill-creator/scripts/quick_validate.py ~/.claude/skills/my-skill
if [ $? -ne 0 ]; then
    echo "Skill validation failed! Fix errors before committing."
    exit 1
fi
```

## Version Tracking

**Current Versions** (as of 2025-11-07):
- Marketplace: `anthropic-agent-skills` commit `c74d647`
- init_skill.py: 303 lines
- package_skill.py: 110 lines
- quick_validate.py: 65 lines

**Update Process**: See [SYNC-TRACKING.md](/Users/terryli/.claude/skills/skill-architecture/references/SYNC-TRACKING.md)

## Future Enhancements (User Modifications)

Potential improvements to marketplace scripts:

### PEP 723 Inline Dependencies

Add to script headers:
```python
# /// script
# dependencies = ["pyyaml>=6.0"]
# ///
```

Enables `uv run init_skill.py` without separate dependency install.

### Absolute Path Output

Modify print statements:
```python
# Current: print(f"Created: {skill_dir}")
# Better:  print(f"Created: {skill_dir.resolve()}")
```

Matches iTerm2 Cmd+click requirement.

### Terry's Template Integration

Update SKILL.md template to include:
- Absolute path convention note
- Link to ~/.claude/CLAUDE.md
- PEP 723 example for scripts/
- Reference to specifications/ for OpenAPI

## Troubleshooting

### "No module named 'yaml'"

Install PyYAML:
```bash
pip install pyyaml
# Or with uv
uv pip install pyyaml
```

### "Permission denied"

Make scripts executable:
```bash
chmod +x /Users/terryli/.claude/plugins/marketplaces/anthropic-agent-skills/skill-creator/scripts/*.py
```

### "Skill directory already exists"

init_skill.py won't overwrite existing directories:
```bash
# Remove or rename existing directory first
mv ~/.claude/skills/pdf-editor ~/.claude/skills/pdf-editor.backup
```
