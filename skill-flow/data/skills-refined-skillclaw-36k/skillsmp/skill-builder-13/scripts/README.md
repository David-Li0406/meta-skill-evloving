# Claude Code Skill Validator

A comprehensive validation tool for Claude Code skills that checks structure, format, and best practices compliance.

## Installation

```bash
cd scripts
npm install
```

## Usage

### Validate a skill directory

```bash
node validate-skill.js /path/to/skill-directory

# Examples:
node validate-skill.js ~/.claude/skills/my-skill
node validate-skill.js .claude/skills/my-skill
node validate-skill.js .  # validate current directory
```

### Help

```bash
node validate-skill.js --help
```

## What It Validates

### ✓ YAML Frontmatter
- Opening `---` on line 1
- Closing `---` before content
- Valid YAML syntax
- No tabs, proper indentation

### ✓ Required Fields
- `name`: Skill name
- `description`: What the skill does and when to use it

### ✓ Optional Fields
- `allowed-tools`: Tool restrictions (if present)
- `version`: Skill version

### ✓ Description Quality
- Specificity (not too vague)
- Usage triggers ("when to use")
- Length (20-150 tokens recommended)

### ✓ Token Budgets
- Metadata: ~100 tokens (warning at 150+)
- Body: <2k tokens recommended (error at 5k+)
- Provides estimates for all sections

### ✓ File Structure
- Only `SKILL.md` in root directory
- No stray `.md` files in root
- `/reference/` folder for detailed docs
- `/scripts/` folder detection

### ✓ Path Format
- All paths use forward slashes (cross-platform)
- No Windows-style backslashes

### ✓ Reference Links
- All `./reference/*.md` links are valid
- Referenced files actually exist

## Exit Codes

- `0`: Validation passed (may have warnings)
- `1`: Validation failed with errors

## Output

The validator provides:

- **✓ Success messages** (green): Validation passed
- **⚠ Warnings** (yellow): Best practice recommendations
- **✗ Errors** (red): Must be fixed before deployment
- **ℹ Info** (cyan): Informational messages

## Example Output

```
╔════════════════════════════════════════════╗
║   Claude Code Skill Validator v1.0.0      ║
╚════════════════════════════════════════════╝

Validating skill at: /path/to/skill

[1/8] Validating directory...
✓ Skill directory exists

[2/8] Checking for SKILL.md...
✓ SKILL.md exists

[3/8] Validating YAML frontmatter...
✓ Valid YAML frontmatter delimiters found
✓ YAML syntax is valid

...

═══════════════════════════════════════════
VALIDATION REPORT
═══════════════════════════════════════════

✓ All validations passed! Skill structure is excellent.
```

## Integration with Skill Development

This validator is designed to work with the skill-builder skill's development process:

1. **During development**: Run validation frequently to catch issues early
2. **Before testing**: Ensure structure is correct
3. **Before deployment**: Final validation check
4. **CI/CD integration**: Use exit codes for automated checks

## Common Issues and Fixes

### Error: "Markdown files found in root"
**Fix**: Move all `.md` files (except `SKILL.md`) to `/reference/` folder

### Warning: "Description may be too vague"
**Fix**: Add specific triggers like "Use when..." or "For [specific use case]"

### Warning: "Body is over 2k tokens"
**Fix**: Move detailed content to files in `/reference/` folder

### Error: "Referenced file does not exist"
**Fix**: Ensure all linked files exist at the specified path

## Based on Official Documentation

This validator implements all requirements from:
- https://anthropic.mintlify.app/en/docs/claude-code/skills

## Version

v1.0.0 - Initial release

## License

MIT
