# YAML Frontmatter Validation

Quick reference for validating skill YAML frontmatter fields.

## Required Fields

| Field | Type | Validation Rules |
|-------|------|------------------|
| `name` | string | Max 64 chars, lowercase letters + hyphens only, no spaces |
| `description` | string | Non-empty, max 1024 chars, third person, includes "when to use" |

## Optional Fields

### Recommended (Always Include)

| Field | Type | Valid Values |
|-------|------|--------------|
| `version` | string | Semantic versioning: `X.Y.Z` (e.g., "1.0.0", "2.3.1") |
| `license` | string | SPDX identifier: `Apache-2.0`, `MIT`, `proprietary` |
| `triggers` | list | 5-50 natural language phrases (marketplace extension) |

### Security & Access Control

| Field | Type | Valid Values |
|-------|------|--------------|
| `allowed-tools` | list | Valid tool names: `Read`, `Write`, `Edit`, `Bash`, `Glob`, `Grep`, `WebFetch`, `WebSearch`, `Task`, etc. |
| `user-invocable` | boolean | `true` (default) or `false` |
| `disable-model-invocation` | boolean | `true` or `false` (default) |

### Execution Control

| Field | Type | Valid Values |
|-------|------|--------------|
| `mode` | boolean | `true` only (categorizes as "mode command"), NOT `interactive`/`batch`/`autonomous` |
| `context` | string | `fork` only (isolated subagent execution) |
| `agent` | string | `Explore`, `Plan`, `Bash`, or other valid agent types |
| `model` | string | `haiku`, `sonnet`, `opus`, or full model ID |

### Lifecycle Hooks

```yaml
hooks:
  - event: PostToolUse        # Required: event type
    matcher:                  # Optional: filter conditions
      tool_name: "Edit|Write" # Pipe for OR matching
      file_paths: ["*.py"]    # Optional: glob patterns
    command: "npm run lint"   # Required: shell command
    once: true                # Optional: run only once
```

**Valid events**: `PreToolUse`, `PostToolUse`, `Stop`, `UserPromptSubmit`

### Metadata

```yaml
metadata:
  author: "Name"
  category: "development"
  keywords: ["keyword1", "keyword2"]
```

## Validation Errors to Check

### Critical (Block Distribution)

- `name` contains uppercase, spaces, or special characters
- `name` exceeds 64 characters
- `description` is empty
- `description` exceeds 1024 characters
- Invalid YAML syntax (parse error)

### Warnings (Should Fix)

- Missing `version` field
- Missing `license` field
- `mode` is a string instead of boolean
- `context` is not `fork`
- `triggers` has fewer than 5 entries (marketplace)
- `allowed-tools` contains invalid tool name
- `hooks` missing required `event` or `command`

### Info (Best Practices)

- `description` doesn't include "when to use" phrase
- `triggers` not bilingual (FR + EN)
- Missing `metadata.author`

## Quick Validation Script

```bash
# Check YAML syntax
python -c "import yaml; yaml.safe_load(open('SKILL.md').read().split('---')[1])"

# Check name format
grep -E "^name: [a-z][a-z0-9-]{0,63}$" SKILL.md

# Check description length
python -c "import yaml; d=yaml.safe_load(open('SKILL.md').read().split('---')[1]); print(len(d.get('description','')))"
```

## See Also

- [julien-skill-creator/references/yaml-frontmatter-guide.md](../../julien-skill-creator/references/yaml-frontmatter-guide.md) - Complete field documentation
