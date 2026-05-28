# How to Use This Skill

Hey Claude—I just added the "skill-validator" skill. Can you validate this skill folder for compliance with Claude standards?

## Example Invocations

**Example 1: Single Skill Validation**
Hey Claude—I just added the "skill-validator" skill. Can you validate the "financial-analyzer" skill folder and show me any issues?

**Example 2: Batch Validation**
Hey Claude—I just added the "skill-validator" skill. Can you batch validate all skills in the "generated-skills" directory and output a CSV report?

**Example 3: Specific Validation Focus**
Hey Claude—I just added the "skill-validator" skill. Can you check just the YAML frontmatter in this SKILL.md file?

**Example 4: Auto-Fix Suggestions**
Hey Claude—I just added the "skill-validator" skill. Can you fix the naming conventions in this skill automatically?

**Example 5: Python Code Validation**
Hey Claude—I just added the "skill-validator" skill. Can you validate the Python files in this skill for proper imports and structure?

## What to Provide

- **Skill folder path**: Path to the skill folder you want to validate
- **Validation focus** (optional): 'all', 'structure', 'yaml', 'python', or 'naming'
- **Output format** (optional): 'json', 'csv', 'text', or 'markdown'
- **Batch mode** (optional): Set to true to validate all skills in a directory

## What You'll Get

- **Validation Report**: Detailed analysis of skill compliance
- **Error Details**: Specific issues with file paths and line numbers
- **Severity Levels**: Critical errors vs. warnings
- **Auto-Fix Suggestions**: Commands to fix common issues automatically
- **Summary Statistics**: Pass/fail counts and error distribution
- **Multiple Formats**: JSON, CSV, text, or markdown reports

## Command Line Usage

You can also use this skill from the command line:

```bash
# Validate a single skill
python validate_skill.py /path/to/skill-folder

# Batch validate directory
python validate_skill.py /path/to/skills-directory --batch

# Validate with specific focus
python validate_skill.py /path/to/skill-folder --focus yaml

# Output in different format
python validate_skill.py /path/to/skill-folder --output csv

# Fix YAML frontmatter
python validate_yaml.py /path/to/SKILL.md

# Fix Python code issues
python validate_python.py /path/to/python_file.py

# Fix naming conventions
python validate_naming.py /path/to/skill-folder
```

## Common Validation Checks

This skill validates:

1. **File Structure**: Required files (SKILL.md, HOW_TO_USE.md), no backup files, no __pycache__
2. **YAML Frontmatter**: Proper format, kebab-case name, required fields
3. **Python Code**: Snake-case file names, module docstrings, safe_divide function
4. **Naming Conventions**: Kebab-case for skill names, snake_case for Python files
5. **Compliance**: Against official Claude documentation standards

## Auto-Fix Capabilities

The skill can automatically fix:

- Missing YAML frontmatter
- Incorrect naming formats (kebab-case, snake_case)
- Missing module docstrings
- Backup file removal
- __pycache__ directory cleanup

## Integration with CI/CD

Use this skill in your development workflow:

```bash
# Pre-commit hook example
python validate_skill.py . --batch --output json > validation_report.json

# Exit with error code if validation fails
if [ $? -ne 0 ]; then
    echo "Validation failed!"
    exit 1
fi
```