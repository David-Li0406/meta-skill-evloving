---
name: code-review
description: Review changes to find high-impact issues. Use for code review of local changes or pull requests.
---

# Code Review Skill

## Purpose

- Perform a focused, high-signal code review. **Report only issues that would actually cause problems in production or significantly impact code quality.**
- Prioritize impactful issues and avoid low-value nitpicks, theoretical concerns, or stylistic preferences.
- **Core principle: Better to miss minor issues than to flood with false positives.**

## Review Process

### Step 1: Initial Scan

- Read the changed lines (the diff)
- **Flag ANY change that could potentially be an issue**
  - Be inclusive at this stage - when in doubt, flag it
  - Better to flag something and discard it in Step 2 than to miss it here
  - Look for: error handling changes, logic changes, new dependencies, resource management, security-related code, API changes, data transformations, state mutations, etc.
- **OUTPUT: Print the initial list of potential issues to investigate**
  - Format: Simple numbered list with brief description and location
  - Example: "1. Unclosed database connection in handler.ts:45"
  - If no potential issues found, state: "No potential issues flagged"

**Goal for Step 1: Cast a wide net. The rigorous filtering happens in Step 2.**

### Step 2: Diagnosis

**For each item in the initial list from Step 1**, complete this reasoning framework:

**Validate Context:**

- Read the related code
- Find in codebase as needed

**Self-Check:**

**1. Impact Analysis**

- "This would cause [SPECIFIC PROBLEM] when [SCENARIO]"
- If you can't fill in these blanks concretely, discard it
- Examples of specific problems: crash, data loss, security breach, resource leak, API contract violation

**2. Evidence Check**

- "I know this is a problem because [EVIDENCE]"
- Evidence = observable behavior, error pattern, resource leak pattern, security risk, breaking change
- NOT evidence = "typically," "best practice," "cleaner," "might," "could," style preferences

**3. Scope Verification**

- "This issue exists in [CHANGED CODE / PRE-EXISTING CODE]"
- Only report if introduced in changed code
- Ignore pre-existing issues unless they're made worse by the changes

**4. Value Test**

- "Reporting this prevents [CONCRETE NEGATIVE OUTCOME]"
- If the outcome is vague, theoretical, or stylistic, discard it
- Ask: Would this feedback prevent a real problem or just align with a preference?

CRITICAL: Only report if you can complete all 4 steps with concrete, factual answers.

### Step 3: Report

- Return only issues that passed self-check
- Keep the report concise and action-oriented

**Remember: The goal is NOT perfection. The goal is preventing real problems.**

## Example Workflow

### After Step 1 (Initial Scan):

```
Initial scan found 3 potential issues:
1. Removed error handler in api/users.ts:23
2. Possible resource leak in db/connection.ts:67
3. Variable naming could be clearer in utils/format.ts:12
```

### After Step 2 (Diagnosis):

```
- Issue #1: REPORT (passed all 4 checks - removes error handling for database failures)
- Issue #2: REPORT (passed all 4 checks - connection not closed in error path)
- Issue #3: DISCARD (failed Value Test - stylistic preference, no actual problem)
```

### Step 3 Output:

Only issues #1 and #2 are included in the final report.

## Output Format

If no findings, return:

```markdown
# Code Review

{1-3 sentences: what functionality was added/modified/removed}

## Findings

Looks good to me!
```

If findings, return:

```markdown
# Code Review

{1-3 sentences: what functionality was added/modified/removed}

## Findings

---

**{path:line}**
{1-2 sentences explaining the problem and its impact}
{Concrete fix - code snippet or specific action to take}

---

{repeat for each finding}

---
```
