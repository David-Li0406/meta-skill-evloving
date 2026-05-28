---
name: prd-to-json
description: "Convert PRD markdown files to prd.json format for Ralf execution. Use when preparing PRDs for autonomous implementation."
---

# PRD to JSON Conversion Skill

Expert guidance for converting PRDs to Ralf's executable JSON format.

## When to Use

- User has a PRD and wants to run Ralf
- User mentions "convert to json" or "prd.json"
- After generating a PRD, to prepare for execution

## JSON Schema

```json
{
  "project": "string",
  "branchName": "ralf/feature-name",
  "description": "string",
  "settings": {
    "tddRequired": true,
    "autoPush": true,
    "executionMode": "sequential",
    "evaluatorEnabled": true,
    "allowReorder": true,
    "evaluateEveryNIterations": 3,
    "maxRetries": 3
  },
  "userStories": [
    {
      "id": "US-001",
      "title": "string",
      "description": "As a..., I want..., so that...",
      "acceptanceCriteria": ["string"],
      "priority": 1,
      "passes": false,
      "notes": "",
      "targetFiles": ["src/path/to/file.ts"],
      "specReference": "FR-1, FR-2",
      "metrics": {
        "startedAt": null,
        "completedAt": null,
        "durationMs": null,
        "tokensConsumed": null,
        "attempts": []
      }
    }
  ]
}
```

## Conversion Rules

1. **Branch Naming**: `ralf/` prefix + kebab-case feature name
2. **Story IDs**: Sequential US-001, US-002, etc.
3. **Priority**: Based on dependency order (1 = first to implement)
4. **Initial State**: All `passes: false`, empty `notes`
5. **Acceptance Criteria**: Always end with "Typecheck passes"
6. **targetFiles**: Scan codebase to identify likely files to create/modify
7. **specReference**: Link to functional requirements (e.g., "FR-1, FR-2")
8. **metrics**: Initialize with null values and empty attempts array
9. **settings**: Include project-level execution preferences

## Dependency Ordering

Priority must respect dependencies:

1. Database/schema changes
2. Backend logic/server actions
3. UI components
4. Integration/dashboard views

A story cannot depend on a later (higher priority number) story.

## Story Size Validation

Before conversion, validate each story is small enough:

- Can be described in 2-3 sentences
- Touches limited number of files
- Has clear start and end point
- No "and then also..." scope creep

## Archive Check

Before overwriting existing `.ralf/prd.json`:

1. Check if existing `.ralf/prd.json` has different branchName
2. If yes, archive to `.ralf/archive/YYYY-MM-DD-feature-name/`
3. Include both `.ralf/prd.json` and `.ralf/progress.txt`

## Strong Linkage (FR-03)

Each story should have clear linkage to:

### targetFiles
Identify files that will be created or modified:
- Scan existing codebase structure
- Consider component/module naming patterns
- Include test files if TDD is enabled

```json
"targetFiles": [
  "src/components/LoginForm.tsx",
  "src/hooks/useAuth.ts",
  "src/components/__tests__/LoginForm.test.tsx"
]
```

### specReference
Link to functional requirements from the PRD:
- Reference FR numbers for traceability
- Helps verify all requirements are covered
- Enables requirement-to-implementation mapping

```json
"specReference": "FR-1, FR-3, NFR-2"
```

## Output

Save to: `.ralf/prd.json`

Create directory if needed: `mkdir -p .ralf`
