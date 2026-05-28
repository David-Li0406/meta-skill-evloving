# Atlas Format Specification

This reference defines validation rules for generated atlas skills. For full templates, see `assets/atlas-templates/`.

## Related References

| Reference | Purpose |
|-----------|---------|
| `protocols/agent-output-parsing.md` | Agent output parsing specifications |
| `review/scoring-criteria.md` | Review grading rubrics |
| `review/json-schema.md` | Review JSON output schema |
| `review/error-recovery.md` | Error handling procedures |
| `review/discovery-protocol.md` | Atlas refinement workflow |

## Directory Structure

```
.claude/skills/atlas/
├── SKILL.md                    # Routing manifest (~80-120 lines)
└── references/
    ├── schema.yaml             # Machine-readable source of truth
    ├── observations.md         # Stack-specific notes and decisions
    ├── {domain}/               # Domain reference files
    │   └── {area}.md
    └── patterns/               # Pattern guide files
        └── {pattern}.md
```

## Templates

| File | Purpose |
|------|---------|
| `assets/atlas-templates/SKILL.template.md` | SKILL.md generation template |
| `assets/atlas-templates/schema.template.yaml` | schema.yaml generation template |
| `assets/atlas-templates/domain-reference.template.md` | Domain documentation template |
| `assets/atlas-templates/pattern-reference.template.md` | Pattern guide template |
| `assets/atlas-templates/observations.template.md` | Observations file template |
| `assets/atlas-templates/atlas-ignore.template` | Default .atlas-ignore patterns |

## Schema Sections

### Core Sections (Required)

| Section | Purpose |
|---------|---------|
| `metadata` | Project info, stack, organization style |
| `domains` | Logical code groupings with paths and counts |
| `file_patterns` | File naming conventions and examples |
| `config_files` | Configuration file inventory |
| `testing` | Test framework, locations, patterns |
| `validation` | Build, test, lint commands |

### Extended Sections (Optional)

| Section | Purpose |
|---------|---------|
| `layers` | Architectural layers (for layer/hybrid organization) |
| `task_mappings` | Common workflows to entry points |
| `integrations` | External service configurations |
| `async_infrastructure` | Queue/job processing setup |
| `patterns` | Pattern conventions with anti-patterns |
| `compositions` | Multi-pattern task sequences |
| `agent_context` | Agent-specific guidance (see below) |

### Agent Context Section

Optional section for optimizing agent behavior:

```yaml
agent_context:
  global:
    preferred_tools: [glob, grep, read, edit]
    context_loading:
      - "Always read schema.yaml first"
      - "Check observations.md for stack-specific notes"
    agent_anti_patterns:
      - "Don't search entire codebase when domain is known"

  domains:
    {domain_name}:
      entry_files:
        - {key_file_1}
      key_queries:
        - pattern: "class.*Service"
          purpose: "Find service classes"
      write_patterns:
        - type: "service"
          template: "{domain}/services/{name}.service.ts"
```

## Validation Rules

### SKILL.md Validation

- [ ] Frontmatter has `name: atlas`
- [ ] Frontmatter has `description` mentioning primary triggers
- [ ] Project Structure section exists with ASCII tree
- [ ] Domain Router section exists with at least 2 entries
- [ ] Pattern Router section exists (if patterns in schema.yaml)
- [ ] Schema Reference section links to `references/schema.yaml`
- [ ] Implementation Pre-flight section exists
- [ ] All reference links are valid paths

### schema.yaml Validation

- [ ] metadata section complete
- [ ] At least 2 domains defined
- [ ] All domain paths exist
- [ ] File counts are reasonable (not 0)
- [ ] At least 2 file patterns defined
- [ ] Testing section exists (even if empty)
- [ ] Documentation lists match actual files
- [ ] patterns section has required fields (if present)
- [ ] anti_patterns_summary items start with "Don't" (if present)

### Pattern Validation

Each pattern in `patterns` section should have:

| Field | Required | Purpose |
|-------|----------|---------|
| `keywords` | Yes | Trigger words for pattern matching |
| `file_convention` | Yes | Where to create files |
| `test_convention` | No | Where to create tests |
| `registration` | No | Files to update when adding pattern |
| `validation_commands` | Yes | Commands to verify pattern |
| `example_files` | Recommended | Reference implementations |
| `anti_patterns_summary` | Recommended | 2-4 codebase-specific mistakes |

### Reference File Validation

- [ ] All listed reference files exist
- [ ] Domain references have required sections
- [ ] Pattern guides have implementation steps
- [ ] No broken internal links
- [ ] observations.md follows template structure

## Health Command

| Command | Purpose |
|---------|---------|
| `/cartographer:health` | Comprehensive atlas health check (drift, structure, quality) |

Use flags to run specific checks:
- `--drift-only` - Only check drift (paths exist, file counts match)
- `--structure-only` - Only validate structure (links valid, required fields)
- `--skip-quality` - Skip quality review (faster)
- `--fix` - Auto-fix simple issues
- `--strict` - Fail on warnings

## Version History

Track schema changes for migration support. Include in schema.yaml header:

```yaml
# Schema Version: 3.0
# Breaking changes:
#   - 1.0.0: Initial release
#   - 1.1.0: Added task_mappings section
#   - 2.0.0: Changed domains structure (breaking)
#   - 3.0.0: Added patterns, compositions, agent_context (breaking)
```

## .atlas-ignore

Place at repository root. See `assets/atlas-templates/atlas-ignore.template` for default patterns.

Supports optional YAML configuration at end of file:

```yaml
# ---
# confidence:
#   project_type: 0.7
#   domain: 0.6
# custom_domains:
#   - name: legacy_code
#     location: src/legacy
#     purpose: Deprecated code pending migration
```

