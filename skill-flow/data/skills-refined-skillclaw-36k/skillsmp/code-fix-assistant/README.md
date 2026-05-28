# Code Fix Assistant - Installation Guide

Complete installation and setup guide for the Code Fix Assistant skill.

## Overview

**Code Fix Assistant** is a comprehensive code quality tool that automates:
- Code formatting (Black, Prettier, gofmt, rustfmt, etc.)
- Syntax/type error detection and fixing
- Bug detection using static analysis
- Fix validation with linters

**Supports**: Python, JavaScript, TypeScript, Java, Go, Rust

## Quick Start

### 1. Install the Skill

**For Claude Code (Desktop)**:

**Option A: Drag & Drop**
```bash
# Drag the code-fix-assistant.zip file into Claude Desktop
# The skill will install automatically
```

**Option B: Manual Installation (Project-level)**
```bash
# Copy skill folder to project
cp -r code-fix-assistant /path/to/your/project/.claude/skills/

# Restart Claude Code
```

**Option C: Manual Installation (User-level)**
```bash
# Copy skill folder to user directory
cp -r code-fix-assistant ~/.claude/skills/

# Restart Claude Code
```

**For Claude Apps (Browser)**:
```
Use the 'skill-creator' skill to import code-fix-assistant.zip
```

### 2. Install Language-Specific Tools

The skill requires language-specific tools to be installed on your system.

#### Python Tools

```bash
# Required
pip install black flake8

# Optional (recommended)
pip install isort mypy autopep8
```

#### JavaScript/TypeScript Tools

```bash
# Required
npm install -g prettier eslint

# For TypeScript
npm install -g typescript @typescript-eslint/parser @typescript-eslint/eslint-plugin
```

#### Java Tools

```bash
# Download Google Java Format
# https://github.com/google/google-java-format/releases

# Download Checkstyle
# https://checkstyle.org/

# Ensure JDK is installed (javac)
java -version
javac -version
```

#### Go Tools

```bash
# gofmt is included with Go installation

# Install additional tools
go install github.com/golangci/golangci-lint/cmd/golangci-lint@latest
go install golang.org/x/tools/cmd/goimports@latest
```

#### Rust Tools

```bash
# Install rustfmt and clippy
rustup component add rustfmt
rustup component add clippy
```

### 3. Verify Installation

**Check Skill Installation**:
```
Hey Claude, do you have the "code-fix-assistant" skill available?
```

**Check Tool Installation**:
```
Hey Claude, using code-fix-assistant, can you check which tools are installed for Python?
```

Or manually verify:
```bash
# Python
black --version
flake8 --version

# JavaScript/TypeScript
prettier --version
eslint --version

# Go
gofmt -h
golangci-lint --version

# Rust
rustfmt --version
cargo clippy --version
```

## File Structure

```
code-fix-assistant/
├── SKILL.md                    # Skill definition and capabilities
├── README.md                   # This file
├── HOW_TO_USE.md              # Usage examples
├── code_fixer.py              # Main fix engine
├── formatters.py              # Code formatting module
├── syntax_checker.py          # Syntax/type error detection
├── bug_detector.py            # Bug detection using static analysis
├── validator.py               # Fix validation module
├── language_config.py         # Language-specific configuration
├── sample_input.json          # Example input
└── expected_output.json       # Example output
```

## Configuration

### Project-Level Configuration

Create configuration files in your project root:

**Python** (.flake8, pyproject.toml):
```toml
# pyproject.toml
[tool.black]
line-length = 88
target-version = ['py38', 'py39', 'py310', 'py311']

[tool.isort]
profile = "black"
```

**JavaScript/TypeScript** (.prettierrc, .eslintrc.json):
```json
{
  "semi": true,
  "singleQuote": false,
  "tabWidth": 2,
  "trailingComma": "es5"
}
```

**Go** (no config needed, gofmt is standard)

**Rust** (rustfmt.toml):
```toml
edition = "2021"
max_width = 100
```

### Skill Configuration

Pass custom configuration when invoking the skill:

```json
{
  "file_path": "src/main.py",
  "language": "python",
  "config": {
    "black": {
      "line_length": 100
    },
    "check_types": true
  }
}
```

## Usage Examples

See [HOW_TO_USE.md](HOW_TO_USE.md) for detailed examples.

**Quick Examples**:

```
# Fix Python file
Hey Claude, use code-fix-assistant to fix src/main.py

# Check without auto-apply
Hey Claude, analyze this TypeScript file for issues but don't auto-fix

# Batch fix directory
Hey Claude, fix all Go files in the cmd/ directory

# Custom configuration
Hey Claude, format this JavaScript with Prettier using single quotes and no semicolons
```

## Common Issues

### Tool Not Found

**Problem**: `black not found` or similar error

**Solution**:
```bash
# Ensure tool is installed
pip install black  # or npm install -g prettier, etc.

# Check if in PATH
which black

# Add to PATH if needed (example for pip user install)
export PATH="$HOME/.local/bin:$PATH"
```

### Permission Denied

**Problem**: Can't write to file

**Solution**:
```bash
# Check file permissions
ls -l file.py

# Fix permissions
chmod u+w file.py
```

### Timeout Errors

**Problem**: Processing times out on large files

**Solution**:
- Split large files into smaller modules
- Increase timeout in configuration
- Process in chunks (by directory)

### Fix Validation Failed

**Problem**: Fixes applied but validation fails

**Solution**:
- Check linter configuration (might be too strict)
- Review fixes manually
- Some issues may require manual intervention

## Advanced Features

### Custom Fix Pipeline

Create custom fix workflows:

```python
from code_fixer import CodeFixAssistant

# Custom pipeline
assistant = CodeFixAssistant({
    'file_path': 'src/app.py',
    'language': 'python',
    'fix_types': ['format', 'syntax'],  # Skip bug detection
    'auto_apply': True,
    'config': {
        'black': {'line_length': 120},
        'check_types': False  # Skip type checking
    }
})

report = assistant.fix()
print(report['summary'])
```

### Integration with CI/CD

Add to your CI pipeline:

```yaml
# .github/workflows/code-quality.yml
name: Code Quality Check

on: [pull_request]

jobs:
  quality-check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Install tools
        run: |
          pip install black flake8
      - name: Run code fix assistant
        run: |
          # Check only, don't auto-fix in CI
          python -c "from code_fixer import CodeFixAssistant; ..."
```

### Pre-Commit Hook

```bash
# .git/hooks/pre-commit
#!/bin/bash

# Run code fix assistant on staged files
python3 -c "
from code_fixer import CodeFixAssistant
import subprocess

# Get staged Python files
files = subprocess.check_output(['git', 'diff', '--cached', '--name-only']).decode().splitlines()
python_files = [f for f in files if f.endswith('.py')]

for file in python_files:
    assistant = CodeFixAssistant({
        'file_path': file,
        'language': 'python',
        'fix_types': ['format', 'syntax'],
        'auto_apply': True
    })
    assistant.fix()
"
```

## Updating the Skill

To update the skill:

```bash
# Download latest version
# Replace old skill folder

# For project-level
rm -rf .claude/skills/code-fix-assistant
cp -r /path/to/new/code-fix-assistant .claude/skills/

# For user-level
rm -rf ~/.claude/skills/code-fix-assistant
cp -r /path/to/new/code-fix-assistant ~/.claude/skills/

# Restart Claude Code
```

## Uninstallation

```bash
# Remove skill folder
rm -rf .claude/skills/code-fix-assistant  # Project-level
rm -rf ~/.claude/skills/code-fix-assistant  # User-level

# Optionally remove tools (if not needed elsewhere)
pip uninstall black flake8 mypy isort
npm uninstall -g prettier eslint
```

## Support & Contribution

**Report Issues**: Create an issue on the repository
**Request Features**: Submit feature requests
**Contribute**: Pull requests welcome

## Version

**Version**: 1.0.0
**Last Updated**: 2025-12-30
**Compatibility**: Claude Code 1.0+, Claude Apps, Claude API

## License

MIT License - See LICENSE file for details
