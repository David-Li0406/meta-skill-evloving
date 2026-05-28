---
name: bazinga-validator
description: Use this skill to validate BAZINGA completion claims with independent verification, ensuring all success criteria are met before accepting the completion signal from the Project Manager.
---

# BAZINGA Validator Skill

You are the bazinga-validator skill. When invoked, you independently verify that all success criteria are met before accepting the BAZINGA completion signal from the Project Manager.

## When to Invoke This Skill

**Invoke this skill when:**
- Orchestrator receives BAZINGA signal from Project Manager
- Need independent verification of completion claims
- PM has marked criteria as "met" and needs validation
- Before accepting orchestration completion

**Do NOT invoke when:**
- PM hasn't sent BAZINGA yet
- During normal development iterations
- For interim progress checks

---

## Your Task

When invoked, you must independently verify all success criteria and return a structured verdict.

**Be brutally skeptical:** Assume PM is wrong until evidence proves otherwise.

---

## Step 1: Query Success Criteria from Database

Use the bazinga-db skill to get success criteria for this session:

```
Skill(command: "bazinga-db")
```

In the same message, provide the request:
```
bazinga-db, please get success criteria for session: [session_id]
```

**Parse the response to extract:**
- criterion: Description of what must be achieved
- status: PM's claimed status ("met", "blocked", "pending")
- actual: PM's claimed actual value
- evidence: PM's provided evidence
- required_for_completion: boolean

---

## Step 2: Independent Test Verification (CONDITIONAL)

**Critical:** Only run tests if test-related criteria exist.

### 2.1: Detect Test-Related Criteria

Look for criteria containing:
- "test" + ("passing" OR "fail" OR "success")
- "all tests"
- "0 failures"
- "100% tests"

**If NO test-related criteria found:**
```
→ Skip entire Step 2 (test verification)
→ Continue to Step 3 (verify other evidence)
→ Tests are not part of requirements
→ Log: "No test criteria detected, skipping test verification"
```

**If test-related criteria found:**
```
→ Proceed with test verification below
→ Run tests independently
→ Count failures
→ Zero tolerance for any failures
```

### 2.2: Find Test Command

**Only execute if test criteria exist (from Step 2.1).**

Check for test configuration:
- `package.json` → scripts.test (Node.js)
- `pytest.ini` or `pyproject.toml` (Python)
- `go.mod` → use `go test ./...` (Go)
- `Makefile` → look for test target

Use Read tool to check these files.

### 2.3: Run Tests with Timeout

**Timeout Configuration:**
- Default: 60 seconds
- Configurable via `.claude/skills/bazinga-validator/resources/validator_config.json` → `test_timeout_seconds` field
- Large test suites may need 180-300 seconds

```bash
# Read timeout from config (or use default 60)
TIMEOUT=$(python3 -c "import json; print(json.load(open('.claude/skills/bazinga-validator/resources/validator_config.json', 'r')).get('test_timeout_seconds', 60))" 2>/dev/null || echo 60)

# Example for Node.js
timeout $TIMEOUT npm test 2>&1 | tee bazinga/test_output.txt

# Example for Python
timeout $TIMEOUT pytest --tb=short 2>&1 | tee bazinga/test_output.txt

# Example for Go
timeout $TIMEOUT go test ./... 2>&1 | tee bazinga/test_output.txt
```

**If timeout occurs:**
- Check if PM provided recent test output in evidence
- If evidence timestamp < 10 min and shows test results: Parse that
- Otherwise: Return REJECT with reason "Cannot verify test status (timeout)"

### 2.4: Parse Test Results

Common patterns:
- **Jest/npm:** `Tests:.*(\d+) failed.*(\d+) passed.*(\d+) total`
- **Pytest:** `(\d+) failed.*(\d+) passed`
- **Go:** Count lines with `FAIL:` or `ok`/`FAIL` summary

Extract:
- Total tests
- Passing tests
- **Failing tests** (this is critical)

### 2.5: Validate Against Criteria

```
IF any test failures exist (count > 0):
  → PM violated criteria
  → Return REJECT immediately
  → Reason: "Independent verification: {failure_count} test failures found"
  → PM must fix ALL failures before BAZINGA
```

---

## Step 3: Verify Evidence for Each Criterion

For each criterion marked "met" by PM:

### Coverage Criteria
```
Criterion: "Coverage >70%"
Status: "met"
Actual: "88.8%"
Evidence: "coverage/coverage-summary.json"

Verification:
1. Parse target from criterion: >70 → target=70
2. Parse actual value: 88.8
3. Check: actual > target? → 88.8 > 70 → ✅ PASS
4. If FAIL → Return REJECT
```

### Numeric Criteria
```
Criterion: "Response time <200ms"
Actual: "150ms"

Verification:
1. Parse operator and target: <200
2. Parse actual: 150
3. Check: 150 < 200 → ✅ PASS
```

### Boolean Criteria
```
Criterion: "Build succeeds"
Evidence: "Build completed successfully"

Verification:
1. Look for success keywords: "success", "completed", "passed"
2. Look for failure keywords: "fail", "error"
3. If ambiguous → Return REJECT (ask for clearer evidence)
```

---

## Step 4: Check for Vague Criteria

Reject unmeasurable criteria:

```python
for criterion in criteria:
    is_vague = (
        "improve" in criterion and no numbers
        or "better" without baseline
        or "make progress" without metrics
        or criterion in ["done", "complete", "working"]
        or len(criterion.split()) < 3  # Too short
    )

    if is_vague:
        → Return REJECT
        → Reason: "Criterion '{criterion}' is not measurable"
```

---

## Step 5: Path B External Blocker Validation

If PM used Path B (some criteria marked "blocked"):

```
For each blocked criterion:
1. Check evidence contains "external" keyword
2. Verify blocker is truly external:
   ✅ "API keys not provided by user"
   ✅ "Third-party service down (verified)"
   ✅ "AWS credentials missing, out of scope"
   ❌ "Test failures" (fixable)
   ❌ "Coverage gap" (fixable)
   ❌ "Mock too complex" (fixable)

IF blocker is fixable:
  → Return REJECT
  → Reason: "Criterion '{criterion}' marked blocked but blocker is fixable"
```

---

## Step 5.5: Scope Validation (MANDATORY)

**Problem:** PM may reduce scope without authorization (e.g., completing 18/69 tasks)

**Step 1: Query PM's BAZINGA message from database**
```bash
python3 .claude/skills/bazinga-db/scripts/bazinga_db.py --quiet get-events \
  "[session_id]" "pm_bazinga" 1
```
This returns the PM's BAZINGA message logged by orchestrator.

**⚠️ The orchestrator logs this BEFORE invoking you. If no pm_bazinga event found, REJECT with reason "PM BAZINGA message not found".**

**Step 2: Extract PM's Completion Summary from BAZINGA message**
Parse the event_payload JSON for:
- Completed_Items: [N]
- Total_Items: [M]
- Completion_Percentage: [X]%
- Deferred_Items: [list]

**Step 3: Check for user-approved scope change**
```bash
python3 .claude/skills/bazinga-db/scripts/bazinga_db.py --quiet get-events \
  "[session_id]" "scope_change" 1
```

**IF scope_change event exists:**
- User explicitly approved scope reduction
- Parse event_payload for `approved_scope`
- Compare PM's completion against `approved_scope` (NOT original)
- Log: "Using user-approved scope: [approved_scope summary]"

**IF no scope_change event:**
- Compare against original scope from session metadata

**Step 4: Compare against applicable scope**
- If Completed_Items < Total_Items AND Deferred_Items not empty → REJECT (unless covered by approved_scope)
- If scope_type = "file" and original file had N items but only M completed → REJECT
- If Completion_Percentage < 100% without BLOCKED status → REJECT (unless user-approved scope change exists)

**Step 5: Flag scope reduction**
```
REJECT: Scope mismatch

Original request: [user's exact request]
Completed: [what was done]
Missing: [what was not done]
Completion: X/Y items (Z%)

PM deferred without user approval:
- [list of deferred items]

Action: Return to PM for full scope completion.
```

**Step 6: Log verdict to database**
```bash
python3 .claude/skills/bazinga-db/scripts/bazinga_db.py --quiet save-event \
  "[session_id]" "validator_verdict" '{"verdict": "ACCEPT|REJECT", "reason": "...", "scope_check": "pass|fail"}'
```

---

## Step 5.7: Blocking Issue Verification (MANDATORY)

**Problem:** PM may send BAZINGA while unresolved CRITICAL/HIGH issues exist from Tech Lead reviews.

**Step 1: Query TL issues and Developer responses from events**
```bash
# Get ALL TL issues (no limit - filter by group after)
python3 .claude/skills/bazinga-db/scripts/bazinga_db.py --quiet get-events \
  "[session_id]" "tl_issues"

# Get ALL Developer responses (no limit - filter by group after)
python3 .claude/skills/bazinga-db/scripts/bazinga_db.py --quiet get-events \
  "[session_id]" "tl_issue_responses"

# Get ALL TL verdicts (single source of truth for rejection acceptance)
python3 .claude/skills/bazinga-db/scripts/bazinga_db.py --quiet get-events \
  "[session_id]" "tl_verdicts"

# NOTE: Filter events by group_id after retrieval, then get latest iteration per group:
# jq '[.[] | select(.group_id == "GROUP_ID")] | sort_by(.timestamp) | last'
```

**Step 2: Compute unresolved blocking issues**

For each task group, diff `tl_issues` against Dev responses AND TL verdicts:
```python
unresolved_blocking = []

# Get TL's acceptance verdicts from tl_verdicts events (single source of truth)
tl_accepted_ids = set()
for verdict_event in tl_verdicts_events:
    for verdict in verdict_event.get("verdicts", []):
        if verdict.get("verdict") == "ACCEPTED":
            tl_accepted_ids.add(verdict.get("issue_id"))

for issue in tl_issues.issues where issue.blocking == true:
  response = find(tl_issue_responses.issue_responses, issue.id)
  if response is None:
    unresolved_blocking.append(issue)  # Not addressed
  elif response.action == "REJECTED":
    # Check if TL accepted the rejection (from tl_verdicts events)
    if issue.id not in tl_accepted_ids:
      unresolved_blocking.append(issue)  # Rejection not yet accepted by TL
  elif response.action == "FIXED":
    # Assume fixed (TL will re-flag if not actually fixed)
    pass
```

**Alternative: If events not found, check handoff files directly:**
```bash
# Fallback: Read handoff files (check both simple and parallel mode paths)
# Simple mode:
cat bazinga/artifacts/{session_id}/{group_id}/handoff_tech_lead.json | jq '.issues[] | select(.blocking == true)'
cat bazinga/artifacts/{session_id}/{group_id}/handoff_implementation.json | jq '.issue_responses'

# Parallel mode (agent-specific files):
cat bazinga/artifacts/{session_id}/{group_id}/handoff_tech_lead_{agent_id}.json | jq '.issues[] | select(.blocking == true)'
cat bazinga/artifacts/{session_id}/{group_id}/handoff_implementation_{agent_id}.json | jq '.issue_responses'
```

**⚠️ Field-level fallbacks for old handoff formats:**
```python
# When reading handoff files, handle missing fields gracefully:
issues = handoff.get("issues", [])
blocking_summary = handoff.get("blocking_summary", {"total_blocking": 0, "fixed": 0})
issue_responses = handoff.get("issue_responses", [])
```

**🔴 CRITICAL: If review occurred but evidence is missing:**
```
# Check if TL review actually occurred by looking for tl_issues events
# Note: review_iteration defaults to 1, so checking > 0 is unreliable
tl_issues_events = get_events(session_id, "tl_issues", group_id)

IF tl_issues_events exist (TL review happened):
  IF no tl_issue_responses events AND no handoff_implementation.json exists:
    → Return: REJECT
    → Reason: "TL raised issues but no Developer responses found for group {group_id}"
    → Note: This indicates Developer did not address TL feedback
```

This hard failure prevents BAZINGA acceptance when review evidence is missing.

**Step 2: Check for any unresolved blocking issues**

**IF unresolved blocking issues exist:**
```
→ Return: REJECT
→ Reason: "Unresolved blocking issues from code review"
→ List all unresolved issues with their IDs, severity, and title
```

**Example rejection:**
```markdown
❌ Blocking Issue Verification: FAIL
   - Unresolved blocking issues: 2
   - TL-AUTH-1-001 (CRITICAL): SQL injection in login query
   - TL-AUTH-2-003 (HIGH): Missing rate limiting on auth endpoint

   These issues must be FIXED or have accepted rejections before BAZINGA.
```

**IF no unresolved blocking issues:**
```
→ Proceed to Step 6
→ Log: "Blocking issue check: PASS (0 unresolved)"
```

**Step 3: Validate rejected issues (if any)**

For issues with Developer `action = "REJECTED"`:
- Check tl_verdicts events for TL's verdict on this issue_id
- Only `ACCEPTED` verdict means TL agreed the fix is unnecessary
- `OVERRULED` or no verdict means issue still counts as blocking

**Resolution states (based on tl_verdicts events):**
| Developer Action | TL Verdict | Final State | Blocks BAZINGA? |
|------------------|------------|-------------|-----------------|
| `FIXED` | N/A | Resolved | ❌ No |
| `REJECTED` | `ACCEPTED` | TL agreed | ❌ No |
| `REJECTED` | `OVERRULED` | TL disagreed | ✅ YES |
| `REJECTED` | (none yet) | Pending TL review | ✅ YES |
| `DEFERRED` | N/A | Deferred (non-blocking only) | ❌ No |
| (none) | N/A | Unaddressed | ✅ YES |

**Note:** The `rejection_accepted` field in event_tl_issue_responses.schema.json is deprecated. Use tl_verdicts events as the single source of truth for TL decisions.

---

## Step 6: Calculate Completion & Return Verdict

```
met_count = count(criteria where status="met" AND verified=true)
blocked_count = count(criteria where status="blocked" AND external=true)
total_count = count(criteria where required_for_completion=true)

completion_percentage = (met_count / total_count) * 100
```

---

## Verdict Decision Tree

```
IF missing_review_data_for_reviewed_groups:
  → Return: REJECT
  → Reason: "Cannot verify blocking issues - missing review data"
  → Detection: If tl_issues events exist for a group (TL flagged issues) but