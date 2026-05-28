# Review JSON Output Schema

This reference defines the complete JSON output specification for `/navigator:review`.

## Output Location

`specs/reviews/{spec-name}-review.json`

## Consumers

| Consumer | Purpose | Required Fields |
|----------|---------|-----------------|
| `/cartographer:capture --from-staging` | Import discoveries | `discoveries.items[]` |
| CI/CD pipelines | Block merge on blockers | `summary.blockers`, `summary.grade` |
| Review dashboards | Aggregate metrics | `summary.*`, `scores.*` |
| `/navigator:build --resume` | Continue after fixes | `blockers[]`, `tech_debt[]` |
| Atlas analytics | Track pattern usage | `atlas_context.patterns_involved` |

## Complete JSON Schema

```json
{
  "version": "1.0",
  "generated": "{ISO-8601 timestamp}",
  "spec_file": "{spec path}",
  "implementation_branch": "{branch name}",
  "base_branch": "{base branch}",

  "summary": {
    "overall_grade": "A|B|C|F",
    "blockers": 0,
    "tech_debt": 0,
    "skippable": 0,
    "recommendation": "merge|fix_blockers|needs_work"
  },

  "scores": {
    "spec_compliance": {"grade": "A", "percentage": 100},
    "pattern_adherence": {"grade": "B", "percentage": 85},
    "code_quality": {"grade": "A", "percentage": 95},
    "validation": {"grade": "A", "all_passed": true}
  },

  "atlas_context": {
    "atlas_path": ".claude/skills/atlas",
    "patterns_involved": ["controllers", "providers"],
    "composition_used": "add_api_endpoint|null",
    "anti_patterns_checked": 12
  },

  "blockers": [
    {
      "id": "BLOCK-001",
      "severity": "blocker",
      "category": "pattern_violation|architecture|validation",
      "file": "{file path}",
      "line": 45,
      "message": "{description}",
      "atlas_reference": "schema.yaml patterns.controllers.anti_patterns_summary[0]",
      "fix": "{suggested fix}"
    }
  ],

  "tech_debt": [
    {
      "id": "DEBT-001",
      "severity": "tech_debt",
      "category": "convention|style|test_coverage",
      "file": "{file path}",
      "message": "{description}",
      "effort": "low|medium|high"
    }
  ],

  "skippable": [
    {
      "id": "SKIP-001",
      "category": "recommendation|suggestion",
      "message": "{description}"
    }
  ],

  "validation_results": {
    "commands_run": 4,
    "passed": 3,
    "failed": 1,
    "results": [
      {"command": "npm run typecheck", "status": "passed", "duration_ms": 2500},
      {"command": "npm run lint", "status": "failed", "errors": 2, "output": "..."}
    ]
  },

  "discoveries": {
    "count": 3,
    "staging_file": ".claude/skills/atlas/staging/discoveries.yaml",
    "items": [
      {
        "type": "anti_pattern|convention|pattern",
        "pattern_id": "{pattern_id}",
        "description": "{what was discovered}",
        "evidence": ["{file paths}"],
        "auto_capturable": true
      }
    ]
  },

  "files_reviewed": [
    {
      "path": "{file path}",
      "status": "new|modified",
      "patterns_matched": ["controllers"],
      "violations": 0,
      "grade": "A"
    }
  ]
}
```

## Field Descriptions

### Root Fields

| Field | Type | Description |
|-------|------|-------------|
| `version` | string | Schema version for backward compatibility |
| `generated` | string | ISO-8601 timestamp of review |
| `spec_file` | string | Path to spec file reviewed |
| `implementation_branch` | string | Branch containing implementation |
| `base_branch` | string | Base branch for comparison |

### Summary Section

| Field | Type | Description |
|-------|------|-------------|
| `overall_grade` | string | A/B/C/F overall assessment |
| `blockers` | number | Count of blocking issues |
| `tech_debt` | number | Count of tech debt issues |
| `skippable` | number | Count of optional improvements |
| `recommendation` | string | `merge`, `fix_blockers`, or `needs_work` |

### Scores Section

Each score contains:

| Field | Type | Description |
|-------|------|-------------|
| `grade` | string | A/B/C/F letter grade |
| `percentage` | number | 0-100 numeric score |

Score categories:
- `spec_compliance` - Success criteria met
- `pattern_adherence` - Conventions followed
- `code_quality` - Readability and organization
- `validation` - Build/test/lint results

### Atlas Context

| Field | Type | Description |
|-------|------|-------------|
| `atlas_path` | string | Path to atlas skill |
| `patterns_involved` | array | Pattern IDs used in review |
| `composition_used` | string\|null | Composition ID if applicable |
| `anti_patterns_checked` | number | Total anti-patterns verified |

### Issue Arrays

Each issue contains:

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Unique identifier (BLOCK-XXX, DEBT-XXX, SKIP-XXX) |
| `severity` | string | `blocker`, `tech_debt`, or `skippable` |
| `category` | string | Issue category |
| `file` | string | File path (if applicable) |
| `line` | number | Line number (if applicable) |
| `message` | string | Human-readable description |
| `atlas_reference` | string | Reference to atlas section (for pattern issues) |
| `fix` | string | Suggested resolution |
| `effort` | string | Estimated effort (tech_debt only) |

### Validation Results

| Field | Type | Description |
|-------|------|-------------|
| `commands_run` | number | Total validation commands |
| `passed` | number | Successful commands |
| `failed` | number | Failed commands |
| `results` | array | Per-command results |

### Files Reviewed

| Field | Type | Description |
|-------|------|-------------|
| `path` | string | File path |
| `status` | string | `new` or `modified` |
| `patterns_matched` | array | Pattern IDs file matches |
| `violations` | number | Issue count for file |
| `grade` | string | Per-file grade |

## Backward Compatibility

When adding new fields:
1. Add with default values
2. Document version in `version` field
3. Consumers should ignore unknown fields
4. Existing fields should not change types

## Example Usage

### CI/CD Integration

```bash
# Block merge on blockers
blockers=$(jq '.summary.blockers' specs/reviews/my-spec-review.json)
if [ "$blockers" -gt 0 ]; then
  echo "Review has $blockers blockers - cannot merge"
  exit 1
fi
```

### Dashboard Aggregation

```bash
# Get overall grade
jq '.summary.overall_grade' specs/reviews/*.json
```

### Resume After Fixes

```bash
# List remaining blockers
jq '.blockers[] | "\(.file):\(.line) - \(.message)"' specs/reviews/my-spec-review.json
```
