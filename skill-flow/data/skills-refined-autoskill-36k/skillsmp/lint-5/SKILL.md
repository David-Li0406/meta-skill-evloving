---
name: lint
description: Lint source code for style violations and potential issues. Use when checking code quality, before commits, or when fixing linting errors.
version: 1.0.0
tags:
  - linting
  - code-quality
  - ruby
  - rubocop
---

# Lint Code

Run linting tools to check code for style violations, potential bugs, and maintainability issues.

## When to Use

- Before committing code changes
- When asked to check code quality or style
- When fixing linting errors or warnings
- After making edits to ensure code follows project conventions

## Usage

Run the linting script from the skill's scripts directory:

```bash
# Lint Ruby code (default)
.cursor/skills/lint/scripts/lint.sh

# Explicitly specify Ruby
.cursor/skills/lint/scripts/lint.sh ruby
```

## Supported Languages

### Ruby

Uses **rubocop** with the project's `.rubocop.yml` configuration. The command runs inside the Docker container.

## Interpreting Output

### Ruby (rubocop)

- **C** (Convention): Style convention violation
- **W** (Warning): Potential issue that may cause problems
- **E** (Error): Definite error that will cause issues
- **F** (Fatal): Rubocop itself encountered an error

Example output:
```
app/models/user.rb:10:5: C: Style/StringLiterals: Prefer double-quoted strings
```

Format: `file:line:column: severity: CopName: message`

## Fixing Issues

1. Run the lint script to identify issues
2. Review each violation and its location
3. Fix the code according to the suggestion
4. Run lint again to verify fixes

For auto-correctable issues, you can run:
```bash
docker compose exec web rubocop -a      # safe auto-corrections
docker compose exec web rubocop -A      # all auto-corrections (may change behavior)
```
