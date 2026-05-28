# Validate Task Enrichment

## Purpose
Check if enriched task data is sufficient for autonomous execution.

## Inputs
- `task`: Enriched task object with files, action, verify, done fields
- `spec_context`: Context from spec.md and requirements.md

## Validation Rules

### Rule 1: Files Field
```
VALID if:
  - Contains at least one concrete file path
  - Paths use project-relative format (e.g., src/api/route.ts)
  - No placeholders like "[path]" or "???"

INVALID if:
  - Empty or contains only vague references
  - Contains "the files" or "relevant files"
  - Path format is ambiguous
```

### Rule 2: Action Field
```
VALID if:
  - Contains numbered implementation steps
  - Each step is specific and actionable
  - Includes "what to avoid and WHY" for risky operations
  - References existing patterns when applicable

INVALID if:
  - Contains vague instructions like "implement feature"
  - Missing specific technology choices
  - No indication of which patterns to follow
```

### Rule 3: Verify Field
```
VALID if:
  - Contains executable command
  - Command will produce observable output
  - Examples: npm test, curl command, build check

INVALID if:
  - Says "it works" or "looks good"
  - Requires subjective judgment
  - No concrete command provided
```

### Rule 4: Done Field
```
VALID if:
  - Contains measurable acceptance criteria
  - Can be verified without subjective judgment
  - Specific about expected outcomes

INVALID if:
  - Vague like "feature is complete"
  - Requires human evaluation
  - Missing specific success indicators
```

## Workflow

### Step 1: Validate Each Field
```
FOR field in [files, action, verify, done]:
  Apply corresponding validation rule
  IF invalid:
    Add to validation_errors with:
      - field_name
      - current_value
      - reason for failure
      - suggestion for fix
```

### Step 2: Determine Severity
```
CRITICAL (blocks transformation):
  - files: empty or all placeholders
  - action: entirely vague or missing

IMPORTANT (should fix but can proceed):
  - verify: generic but functional
  - done: measurable but could be more specific

OPTIONAL (nice to have):
  - action: could reference more patterns
  - done: could add more edge cases
```

### Step 3: Generate Report
```
IF has CRITICAL errors:
  Return {
    valid: false,
    severity: "critical",
    errors: [critical errors],
    clarification_needed: true
  }

IF has IMPORTANT errors only:
  Return {
    valid: true,
    severity: "warning",
    warnings: [important errors],
    clarification_needed: false
  }

IF all valid:
  Return {
    valid: true,
    severity: "none",
    errors: [],
    clarification_needed: false
  }
```

## Examples

### Invalid Files (Critical)
```
Input: "<files>the auth files</files>"
Output: {
  valid: false,
  field: "files",
  reason: "No concrete file paths provided",
  suggestion: "Specify exact paths like 'src/middleware/auth.ts'"
}
```

### Invalid Action (Critical)
```
Input: "<action>Add authentication</action>"
Output: {
  valid: false,
  field: "action",
  reason: "No specific implementation steps",
  suggestion: "Add numbered steps with specific instructions"
}
```

### Invalid Verify (Important)
```
Input: "<verify>Check it works</verify>"
Output: {
  valid: true,
  field: "verify",
  severity: "warning",
  reason: "Not an executable command",
  suggestion: "Use 'npm test -- auth.test.ts' or similar"
}
```

### Valid Example
```
Input:
  files: "src/api/auth/login.ts, src/api/__tests__/auth.test.ts"
  action: "1. Create login endpoint accepting {email, password}..."
  verify: "npm test -- auth.test.ts"
  done: "Valid credentials return 200 + JWT cookie, invalid return 401"

Output: {
  valid: true,
  severity: "none",
  errors: []
}
```
