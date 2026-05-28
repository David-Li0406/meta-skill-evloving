# Example: Skip Mutation Testing

## Scenario
Task is documentation-only or config changes.

## Task Analysis

```yaml
task:
  id: task-5
  description: "Update README with new API documentation"
  files:
    - README.md
    - docs/api.md
  type: documentation
```

## Skip Decision

```
┌─────────────────────────────────────────────────────────────┐
│ Mutation Testing: SKIPPED                                   │
│                                                             │
│   Task: task-5                                              │
│   Reason: Documentation-only changes                        │
│                                                             │
│   Skip criteria met:                                        │
│   ✓ No executable code modified                             │
│   ✓ Only .md files changed                                  │
│   ✓ Task type is 'documentation'                            │
│                                                             │
│   Proceeding without mutation testing.                      │
└─────────────────────────────────────────────────────────────┘
```

## When to Skip

| File Type | Skip Mutation Testing |
|-----------|----------------------|
| *.md | ✅ Skip |
| *.json (config) | ✅ Skip |
| *.yaml (config) | ✅ Skip |
| *.d.ts (type declarations) | ✅ Skip |
| *.css/*.scss | ✅ Skip |
| *.ts/*.tsx (code) | ❌ Run |
| *.test.ts (tests) | ❌ Run (on tested code) |

## Task Types That Skip

| Task Type | Mutation Testing |
|-----------|------------------|
| DOCUMENTATION | Skip |
| CONFIG | Skip |
| TYPES_ONLY | Skip |
| REFACTOR (no logic change) | Optional |
| FEATURE | Required |
| BUGFIX | Required |
| SECURITY | Required (high threshold) |

## Output for Skipped Tasks

```yaml
# In .claude/auto-progress.yaml
tasks:
  task-5:
    mutation_testing:
      status: skipped
      reason: documentation_only
      skipped_at: "2025-01-18T10:30:00Z"
```

## Alternative Verification

For skipped mutation testing, ensure:
- Markdown linting passes
- Links are valid
- No broken references

```bash
# For documentation tasks
npx markdownlint docs/*.md
npx markdown-link-check README.md
```
