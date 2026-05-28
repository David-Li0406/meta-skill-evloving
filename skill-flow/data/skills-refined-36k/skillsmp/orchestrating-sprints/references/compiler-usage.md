---
title: Compiler Usage
description: Sprint compiler CLI reference including usage, options, validation errors, and troubleshooting.
keywords: compiler, CLI, compile, validation, errors, dry-run
skill: orchestrating-sprints
---

# Compiler Usage

## CLI Usage

```bash
node compiler/dist/index.js <sprint-dir> [options]
```

## Options

| Option | Default | Description |
|--------|---------|-------------|
| `-w, --workflows <dir>` | `.claude/workflows` | Workflows directory path |
| `-o, --output <file>` | `<sprint-dir>/PROGRESS.yaml` | Output file path |
| `-v, --verbose` | false | Enable verbose logging |
| `--dry-run` | false | Validate without writing |

## Validation Error Codes

| Code | Message | Resolution |
|------|---------|------------|
| `SPRINT_NOT_FOUND` | SPRINT.yaml missing | Verify sprint directory |
| `WORKFLOW_NOT_FOUND` | Referenced workflow missing | Check .claude/workflows/ |
| `INVALID_PHASE` | Invalid phase structure | Check required fields |
| `CYCLE_DETECTED` | Circular workflow reference | Remove workflow cycle |
| `UNRESOLVED_VARIABLE` | Template variable not found | Check variable name |

## Common Usage Patterns

```bash
# Manual compilation
node compiler/dist/index.js sprints/2024-01-15_auth-sprint

# Dry-run preview (validate without writing)
node compiler/dist/index.js sprints/2024-01-15_auth-sprint --dry-run

# Verbose debugging
node compiler/dist/index.js sprints/2024-01-15_auth-sprint -v

# Custom workflows directory
node compiler/dist/index.js sprints/2024-01-15_auth-sprint -w ./custom-workflows

# Custom output path
node compiler/dist/index.js sprints/2024-01-15_auth-sprint -o ./output/PROGRESS.yaml
```

## Troubleshooting

| Issue | Cause | Resolution |
|-------|-------|------------|
| Workflows not found | Wrong path | Check `-w` option path |
| YAML parse error | Invalid syntax | Run yaml linter |
| Template not expanded | Missing step context | Verify for-each structure |
| Permission denied | File not writable | Check output directory permissions |
| Circular dependency | Workflow includes itself | Review workflow imports |
