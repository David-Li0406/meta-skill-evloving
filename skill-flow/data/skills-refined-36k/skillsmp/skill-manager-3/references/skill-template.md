# Skill Template

This template is used by the skill generator to create new skills.

## SKILL.md Format

```yaml
---
name: {skill_name}
description: {description with trigger phrases}
allowed-tools:
  - {tool1}
  - {tool2}
version: {version}
domain: {domain}
auto-generated: {true|false}
---

# {Skill Title}

{Overview paragraph explaining what this skill does}

## When to Use

{Describe scenarios and trigger phrases}

## Core Workflow

{Step-by-step workflow}

## Commands/Templates

{Reusable command templates}

## Best Practices

{Domain-specific best practices}

## Common Pitfalls

{Things to watch out for}
```

## skill.meta.json Format

```json
{
  "skill_id": "uuid",
  "name": "skill-name",
  "version": "1.0.0",
  "domain": "domain-name",
  "created_at": "ISO-8601",
  "updated_at": "ISO-8601",
  "auto_generated": true,
  "source_patterns": ["pattern-id-1", "pattern-id-2"],
  "approval_status": "approved|pending|rejected",
  "approved_by": "user|system",
  "approved_at": "ISO-8601",
  "effectiveness": {
    "usage_count": 0,
    "success_rate": 1.0,
    "avg_tool_calls": 0,
    "failure_patterns": [],
    "user_refinements": 0,
    "last_improvement": null
  }
}
```

## CHANGELOG.md Format

```markdown
# Changelog

All notable changes to this skill will be documented in this file.

## [1.0.0] - YYYY-MM-DD

### Added
- Initial skill generation from patterns
- Core workflow documentation
- Command templates

## [1.1.0] - YYYY-MM-DD

### Changed
- Auto-improved: Added Grep tool (detected in 3 failed sessions)

### Fixed
- Error handling for large repositories
```

## Tool Permissions

Only include tools the skill actually needs:

| Tool | Use Case |
|------|----------|
| Bash | Running commands, scripts |
| Read | Reading files |
| Grep | Searching file contents |
| Glob | Finding files by pattern |
| Write | Creating/modifying files |
| Edit | Editing existing files |
| WebFetch | Fetching web content |
| WebSearch | Searching the web |

## Domain Keywords

Include relevant domain keywords in the description for better matching:

- **devops**: docker, kubernetes, deploy, ci/cd, pipeline
- **security**: audit, vulnerability, owasp, encryption
- **data_science**: pandas, model, train, dataset
- **frontend**: react, component, css, webpack
- **backend**: api, database, rest, endpoint
- **git**: merge, rebase, branch, pr, commit
