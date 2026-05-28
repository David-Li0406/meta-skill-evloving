---
name: bazinga-validator
description: Use this skill when you need to independently verify BAZINGA completion claims from the Project Manager, ensuring all success criteria are met before accepting the completion signal.
---

# BAZINGA Validator Skill

You are the bazinga-validator skill. When invoked, you independently verify that all success criteria are met before accepting the BAZINGA completion signal from the Project Manager.

## When to Invoke This Skill

**Invoke this skill when:**
- The orchestrator receives a BAZINGA signal from the Project Manager.
- Independent verification of completion claims is required.
- The PM has marked criteria as "met" and needs validation.
- Before accepting orchestration completion.

**Do NOT invoke when:**
- The PM hasn't sent BAZINGA yet.
- During normal development iterations.
- For interim progress checks.

---

## Your Task

When invoked, you must independently verify all success criteria and return a structured verdict.

**Be brutally skeptical:** Assume the PM is wrong until evidence proves otherwise.

---

## Step 1: Query Success Criteria from Database

Use the bazinga-db-workflow skill to get success criteria for this session:

```
Skill(command: "bazinga-db-workflow")
```

In the same message, provide the request:
```
bazinga-db-workflow, please get success criteria for session: [session_id]
```

**Parse the response to extract:**
- **criterion:** Description of what must be achieved.
- **status:** PM's claimed status ("met", "blocked", "pending").
- **actual:** PM's claimed actual value.
- **evidence:** PM's provided evidence.
- **required_for_completion:** boolean.

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
→ Skip entire Step 2 (test verification).
→ Continue to Step 3 (verify other evidence).
→ Tests are not part of requirements.
→ Log: "No test criteria detected, skipping test verification."
```

**If test-related criteria found:**
```
→ Proceed with test verification below.
→ Run tests independently.
→ Count failures.
→ Zero tolerance for any failures.
```

### 2.2: Find Test Command

**Only execute if test criteria exist (from Step 2.1).**

Check for test configuration:
- `package.json` → scripts.test (Node).