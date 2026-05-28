---
name: skill-validator
description: Validates Claude skill files for correct structure, YAML frontmatter, Python imports, naming conventions, and compliance with official documentation
---

# Claude Skill Validator

This skill provides comprehensive validation for Claude Skills, ensuring all files follow official Anthropic standards and best practices. It checks structure, formatting, naming conventions, and compliance requirements.

## Capabilities

- **File Structure Validation**: Validates presence and organization of all required skill files (SKILL.md, HOW_TO_USE.md, Python files, sample data)
- **YAML Frontmatter Validation**: Checks SKILL.md YAML frontmatter for correct format, kebab-case naming, and required fields
- **Python Code Validation**: Validates Python file imports, structure, error handling, and best practices
- **Naming Convention Validation**: Ensures kebab-case for skill names, snake_case for Python files, proper file extensions
- **Compliance Validation**: Checks against official Claude documentation standards
- **Batch Processing**: Validates multiple skills at once with summary reporting
- **Auto-Fix Suggestions**: Provides automatic fixes for common issues (renaming files, fixing YAML, etc.)

## Input Requirements

**Single skill validation:**
- Skill folder path (local directory containing skill files)
- Optional: Specific validation focus (structure, yaml, python, naming, all)

**Batch validation:**
- Directory containing multiple skill folders
- Optional: Validation report format (JSON, CSV, text)

**Direct file input:**
- SKILL.md file path for YAML validation
- Python file path for code validation
- JSON configuration for custom validation rules

## Output Formats

- **Validation Report**: Structured JSON with detailed findings
- **Error Details**: Specific error messages with file paths and line numbers
- **Severity Levels**: Critical, Warning, Info classifications
- **Auto-Fix Suggestions**: Specific commands to fix common issues
- **Summary Statistics**: Pass/fail counts, error distribution
- **Multiple Formats**: JSON, CSV, text, and markdown reports

## How to Use

"Validate this skill folder for compliance with Claude standards"
"Check the YAML frontmatter in this SKILL.md file"
"Batch validate all skills in the skills directory and output a CSV report"
"Fix the naming conventions in this skill automatically"

## Scripts

- `validate_skill.py`: Main validation orchestrator and batch processor
- `validate_yaml.py`: YAML frontmatter validation and auto-fixing
- `validate_python.py`: Python code structure and import validation
- `validate_naming.py`: Naming convention validation and auto-renaming

## Best Practices

1. **Validate Early**: Run validation during skill development, not just before deployment
2. **Batch Processing**: Validate entire skill catalogs regularly to maintain consistency
3. **Auto-Fix First**: Use auto-fix suggestions for common issues before manual intervention
4. **Documentation Reference**: Always cross-check with official Claude documentation
5. **Version Control**: Integrate validation into CI/CD pipelines for automated quality checks

## Limitations

- Cannot validate subjective quality (content relevance, usefulness)
- Limited to structural and formatting standards
- Auto-fix may not handle complex refactoring scenarios
- Requires local file system access (cannot validate remote URLs directly)
- Python validation is syntax/import focused, not functional testing

## Compliance Standards

This validator checks against:
- Official Claude Skills documentation
- YAML frontmatter specifications
- Python import and structure best practices
- File naming conventions (kebab-case, snake_case)
- Required file presence and organization