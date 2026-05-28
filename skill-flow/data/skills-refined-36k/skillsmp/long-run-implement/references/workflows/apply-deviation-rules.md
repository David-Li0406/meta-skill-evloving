# Apply Deviation Rules

## Purpose
Handle unexpected situations during plan execution according to deviation rules.

## Deviation Rules Summary

| Rule | Trigger | Action | Stop? |
|------|---------|--------|-------|
| 1 | Bugs, broken behavior | Auto-fix | No |
| 2 | Missing critical functionality | Auto-add | No |
| 3 | Blocking issues | Auto-fix | No |
| 4 | Architectural changes | Present decision | Yes |
| 5 | Non-critical enhancements | Log to ISSUES.md | No |

## Rule Definitions

### Rule 1: Bug Fixes
```
TRIGGER:
  - Test fails due to incorrect implementation
  - Runtime error in implemented code
  - Validation logic produces wrong results

ACTION:
  - Analyze error/failure
  - Implement fix
  - Re-run verification
  - Log in SUMMARY.md under "Auto-Fixed (Rules 1-3)"
  - Commit type: "fix"

STOP: No
```

### Rule 2: Missing Critical Functionality
```
TRIGGER:
  - Input validation missing where needed
  - Error handling absent for likely failures
  - Auth/permission checks missing
  - Required logging not present

ACTION:
  - Identify missing functionality
  - Implement minimal viable version
  - Verify it works
  - Log in SUMMARY.md under "Auto-Fixed (Rules 1-3)"
  - Commit as part of current task

STOP: No
```

### Rule 3: Blocking Issues
```
TRIGGER:
  - Missing dependency (npm package, import)
  - Broken import/require statement
  - Type mismatch preventing compilation
  - Configuration error blocking execution

ACTION:
  - Install missing dependency
  - Fix import path
  - Resolve type issue
  - Update config
  - Log in SUMMARY.md
  - Commit type: "chore" or "fix"

STOP: No
```

### Rule 4: Architectural Changes
```
TRIGGER:
  - New database table/schema needed
  - New service layer required
  - Framework/library change needed
  - Significant pattern deviation from plan
  - Cross-cutting concern introduction

ACTION:
  - STOP execution
  - Present decision to user with options:
    1. Proceed with architectural change
    2. Find workaround without change
    3. Defer to ISSUES.md and skip
    4. Abort and revise plan

STOP: Yes - wait for user decision
```

### Rule 5: Non-Critical Enhancements
```
TRIGGER:
  - Performance optimization opportunity
  - Code style improvement
  - Additional test coverage
  - Documentation enhancement
  - Refactoring opportunity

ACTION:
  - Log to {spec_path}/.long-run/ISSUES.md
  - Format: "ISS-{number}: {description} (Plan {N})"
  - Continue execution
  - Do NOT implement

STOP: No
```

## Detection Logic

### Automatic Detection
```
DURING task execution:
  1. Monitor for errors/failures
  2. Check verification results
  3. Analyze implementation completeness

CLASSIFY deviation:
  IF error in existing code → Rule 1
  IF missing validation/auth/error handling → Rule 2
  IF import/dependency/config error → Rule 3
  IF requires new table/service/framework → Rule 4
  IF "nice to have" improvement → Rule 5
```

### Rule 4 Detection Heuristics
```
ARCHITECTURAL INDICATORS:
  - Task mentions "create table" or "add migration"
  - Task requires "new service" or "service layer"
  - Implementation needs different framework
  - Pattern significantly differs from existing code
  - Change affects multiple unrelated components
```

## Workflow

### Step 1: Detect Deviation
```
ON any unexpected situation:
  1. Classify by rule number
  2. Log detection details
  3. Route to appropriate handler
```

### Step 2: Handle by Rule
```
SWITCH rule_number:
  CASE 1, 2, 3:
    - Apply auto-fix
    - Log to SUMMARY.md
    - Continue execution

  CASE 4:
    - Pause execution
    - Generate decision options
    - Return status: NEEDS_DECISION

  CASE 5:
    - Log to ISSUES.md
    - Continue execution
```

### Step 3: Document in Output
```
FOR Rules 1-3:
  Add to SUMMARY.md:
  "### Auto-Fixed (Rules 1-3)
   - [Rule {N}] {description of fix}"

FOR Rule 4:
  Add to SUMMARY.md:
  "### Decisions Made
   | Decision | Choice | Rationale |
   | {decision} | {user_choice} | {reason} |"

FOR Rule 5:
  Add to ISSUES.md:
  "- ISS-{N}: {description} (Plan {plan_number})"
```

## ISSUES.md Format

```markdown
# Deferred Issues

Issues logged during long-run execution for future consideration.

## From Plan 02: API Endpoints
- ISS-001: Could add caching for GET requests (performance)
- ISS-002: Consider pagination for list endpoints (scalability)

## From Plan 03: UI Components
- ISS-003: Could add loading skeleton states (UX)
```
