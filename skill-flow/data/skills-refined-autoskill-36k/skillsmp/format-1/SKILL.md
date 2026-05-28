---
name: format
description: Format code according to project standards. Use after making changes or before committing.
allowed-tools: Bash, Read, Edit, Glob
---

# Format - argus

Format code according to project standards.

## Command

```bash
go fmt ./...
```

## Description

Format all Go files

## Usage

- Run before committing changes
- Use `-d` (diff only) to check without modifying files
- Format specific files by passing paths as arguments

## Notes

- This command modifies files in place
- Formatting is enforced by pre-commit hooks (if configured)
