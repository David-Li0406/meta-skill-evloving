# WordPress Structure Validator Skill

Comprehensive validation tool for WordPress Full Site Editing (FSE) themes.

## Installation

This skill is already installed in your Claude Code project at:
```
.claude/skills/wordpress-structure-validator/
```

## Quick Start

### Run All Validations

```bash
# From project root
cd .claude/skills/wordpress-structure-validator

# Validate templates
bash scripts/validate_templates.sh /path/to/theme

# Validate theme.json
python scripts/check_theme_json.py /path/to/theme/theme.json

# Check block styles
bash scripts/check_block_styles.sh /path/to/theme
```

### For clemencefouquet.fr

```bash
# Download theme from server
mkdir -p /tmp/clemence-theme
ssh automation@69.62.108.82 "docker exec wordpress-clemence tar -czf - -C /var/www/html/wp-content/themes twentytwentyfour" | tar -xzf - -C /tmp/clemence-theme

# Run validations
bash scripts/validate_templates.sh /tmp/clemence-theme/twentytwentyfour
python scripts/check_theme_json.py /tmp/clemence-theme/twentytwentyfour/theme.json
bash scripts/check_block_styles.sh /tmp/clemence-theme/twentytwentyfour
```

## What This Skill Validates

✅ **Templates**
- Required templates present (index.html minimum)
- Naming conventions (page-{slug}.html, etc.)
- WordPress block syntax
- Template parts (header.html, footer.html)

✅ **theme.json**
- Valid JSON syntax
- Required fields (version, settings)
- Color palette structure
- Typography and spacing definitions
- WCAG contrast ratios

✅ **Block Styles**
- Registered block styles in functions.php
- Naming conventions (kebab-case)
- Inline vs external CSS usage
- Version numbers for cache busting

✅ **Content**
- Featured images set for pages
- Homepage configuration
- Page template assignments

✅ **File Permissions**
- Correct ownership (www-data:www-data)
- Proper permissions (644/755)

## Test Results for clemencefouquet.fr

### ✅ Templates Validation

```
✅ 12 templates found
✅ index.html present (required)
✅ page-accueil.html present (custom homepage)
✅ All naming conventions correct
✅ Header and footer template parts present
```

### ✅ theme.json Validation

```
✅ Valid JSON syntax (version 2)
✅ 11 colors defined with semantic names
✅ 7 font sizes defined
✅ 9 spacing sizes defined
✅ All settings properly structured
```

### ⚠️ Block Styles Validation

```
✅ 17 block styles registered
✅ All using kebab-case naming
✅ Core blocks styled (heading, group, button, image)
⚠️  14 inline styles (consider external CSS for some)
⚠️  No version numbers in some enqueues
```

## Files Structure

```
wordpress-structure-validator/
├── SKILL.md                              # Main skill documentation
├── README.md                             # This file
├── scripts/
│   ├── validate_templates.sh            # Template validator
│   ├── check_theme_json.py              # theme.json validator
│   └── check_block_styles.sh            # Block styles checker
├── references/
│   ├── wordpress-template-hierarchy.md  # Complete WP hierarchy
│   └── fse-best-practices.md            # FSE development guide
└── assets/
    └── validation-report-template.md    # Report template
```

## Usage in Claude Code

When you ask Claude to validate WordPress structure, the skill will automatically:

1. Load SKILL.md instructions
2. Guide you through validation steps
3. Run appropriate scripts
4. Generate validation report

**Example prompts**:
- "Validate the WordPress theme structure"
- "Check if my templates follow WordPress conventions"
- "Audit the theme.json configuration"
- "Generate a validation report for clemencefouquet.fr"

## Maintenance

### Update Scripts

Scripts are located in `scripts/` directory. They are executable and can be run directly.

### Update References

Documentation in `references/` should be updated when WordPress FSE standards change.

### Report Template

Customize `assets/validation-report-template.md` to match your reporting needs.

## Related Documentation

- [WordPress Template Hierarchy](references/wordpress-template-hierarchy.md)
- [FSE Best Practices](references/fse-best-practices.md)
- [Main Project README](../../../README.md)
- [Project CLAUDE.md](../../../CLAUDE.md)

## Version

**Version**: 1.0.0
**Last Updated**: 2025-11-09
**Tested on**: clemencefouquet.fr (WordPress 6.8.3, Twenty Twenty-Four theme)
