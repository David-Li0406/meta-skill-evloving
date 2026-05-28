# User Clarification Protocol

## Purpose
Handle situations where task enrichment fails due to vague specifications.

## When to Trigger
- Transform workflow cannot infer file paths
- Action steps are too vague to generate
- Critical enrichment validation fails

## Clarification Request Format

### Structured Request Template
```markdown
## Clarification Needed for Task Group [N]: [Name]

I cannot automatically enrich this task group. Missing information:

### File Paths (Required)
The following sub-tasks need explicit file paths:
- [ ] [N.2] "Create controller" → Where should this file be created?
- [ ] [N.3] "Add middleware" → Which existing middleware to extend?

### Implementation Details (Required)
- [ ] [N.2] What controller pattern to follow? (REST/GraphQL/RPC)
- [ ] [N.3] What auth mechanism? (JWT/Session/API Key)

### Please Provide:
1. File paths for each sub-task (or "infer from codebase")
2. Implementation approach (or "use existing patterns")
3. Any constraints or "do NOT" rules

**Your response format:**
```
N.2: src/api/resource/route.ts, REST pattern from src/api/users/
N.3: extend src/middleware/auth.ts, JWT validation
Constraints: Do not use raw SQL
```
```

## Workflow

### Step 1: Generate Request
```
1. Identify missing/vague fields
2. Group by category (files, implementation, constraints)
3. Generate specific questions for each
4. Include suggested response format
```

### Step 2: Present to User
```
1. Output clarification request
2. Start timeout timer (default: 10 minutes)
3. Wait for response
```

### Step 3: Handle Response
```
IF user responds within timeout:
  1. Parse response format
  2. Update task enrichment with provided values
  3. Re-run validation
  4. IF still invalid: Generate follow-up questions
  5. IF valid: Continue transformation

IF timeout reached:
  Present options:
  1. "Respond now (I'm still here)"
  2. "Save and exit (resume later)"
  3. "Skip this task group"
```

### Step 4: Persist Clarifications
```
Write to {spec_path}/.long-run/clarifications.md:

# Clarifications Log

## Task Group [N]: [Name]
**Asked:** [ISO timestamp]
**Question:** [summary of what was asked]
**Status:** [pending/answered]
**Response:** [user's response if answered]
```

## Timeout Handling

### Save and Exit
```
1. Write pending clarification to clarifications.md with status: "pending"
2. Update STATE.md:
   - Status: "Stopped"
   - Stopped at: "Awaiting clarification for Task Group N"
3. Output resume instructions:
   "State saved. To resume: /long-run-implement [spec-name]"
```

### Skip Task Group
```
1. Mark task group as skipped in STATE.md
2. Generate placeholder SUMMARY.md:
   ---
   status: skipped
   reason: needs-clarification
   ---
3. Copy clarification request to SUMMARY.md
4. Continue to next task group
```

## Resume with Pending Clarifications

### Detection
```
ON initialize:
  IF clarifications.md exists:
    Read entries
    IF any entry has status: "pending":
      Re-present the pending question
      Continue from Step 3
```

### Re-presentation
```
"I had a pending clarification from the previous session:

[Original clarification request]

Would you like to:
1. Answer now
2. Skip this task group
3. Start fresh (clear all state)"
```
