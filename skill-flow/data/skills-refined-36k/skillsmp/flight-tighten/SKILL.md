---
name: flight-tighten
description: Analyze validation failures and strengthen domain rules to prevent recurrence. Use after /flight-validate reports failures to improve domain constraints.
---

## ⚠️ EXECUTION RULES (MANDATORY)

1. **EXECUTE EACH STEP** - Do not skip steps based on "prior context"
2. **USE TOOLS** - You MUST call Read/Bash tools, not recall from memory
3. **SHOW WORK** - Each step must produce visible tool output
4. **NO SHORTCUTS** - "I already read this" is NOT acceptable

### Anti-Patterns (DO NOT DO THESE)
- ❌ "I already read the domain files earlier"
- ❌ "From earlier analysis..."
- ❌ Summarizing steps without executing them
- ❌ Claiming knowledge from "this conversation"

---

# /flight-tighten

Analyze validation failures and strengthen domain rules to prevent recurrence.

## Usage

```
/flight-tighten
```

## Arguments

- None - Uses the most recent `/flight-validate` output from context

---

## Process

### 1. Review Validation Report

From the most recent `/flight-validate` output, identify:
- Which rules failed
- Which files violated them
- Pattern of failures

### 2. Root Cause Analysis

For each failure, determine:

```markdown
## Failure Analysis

### Failure: [description]

**What happened:**
[Specific violation]

**Why it happened:**
- [ ] Rule was ambiguous
- [ ] Rule was missing
- [ ] Rule conflicted with another rule
- [ ] Implementation misunderstood requirement
- [ ] Edge case not covered

**Root cause:**
[The actual underlying issue]
```

### 3. Categorize the Fix

| Category | Action |
|----------|--------|
| Missing rule | Add new invariant to domain |
| Ambiguous rule | Clarify with examples |
| Conflicting rules | Resolve conflict, document priority |
| Missing pattern | Add code example to domain |
| Edge case | Add specific handling rule |

### 4. Update Domain Files

Based on analysis, modify `.flight/domains/[domain].md`:

#### Adding a New Invariant

```markdown
### MUST
- [existing rules]
- **[NEW]** [New rule based on failure]
```

#### Clarifying Existing Rule

```markdown
### MUST
- [Rule] - **Clarification:** [specific guidance]

#### Example (correct):
```js
// This satisfies the rule
[code]
```

#### Example (incorrect):
```js
// This violates the rule
[code]
```
```

#### Adding Edge Case

```markdown
## Edge Cases

### [Scenario]
When [condition], MUST [behavior].

```js
// Example handling
[code]
```
```

### 5. Document the Change

```markdown
## Tightening Report

### Failures Analyzed
1. [failure 1]
2. [failure 2]

### Domain Updates

#### [domain].md

**Added:**
- New MUST rule: [description]

**Clarified:**
- [Rule]: Added example showing [correct pattern]

**Removed:**
- [Conflicting rule]: Replaced with [new rule]

### Verification

To verify fix, re-run:
```bash
/flight-compile
# Execute generated prompt
/flight-validate
```

### Prevention

This failure pattern now prevented by:
- [Rule 1 in domain]
- [Rule 2 in domain]
```

---

## Output: Tightening Report

```markdown
## Tightening Report

### Failures Analyzed
1. [failure 1]
2. [failure 2]

### Domain Updates
#### [domain].md
- **Added:** [new rules]
- **Clarified:** [improved rules]
- **Removed:** [conflicting rules]

### Verification
[Commands to verify fix]

### Prevention
[How this prevents recurrence]
```

---

## Tightening Principles

### Make Rules Specific
❌ "Handle errors properly"
✅ "MUST wrap async calls in try/catch with specific error types"

### Add Concrete Examples
❌ "Use appropriate naming"
✅ "MUST use camelCase for functions, PascalCase for components"
   ```js
   // Correct
   function getUserData() {}
   function UserProfile() {}
   
   // Incorrect
   function get_user_data() {}
   function userProfile() {}
   ```

### Eliminate Ambiguity
❌ "Consider performance"
✅ "MUST use useMemo for computations over 100 items"

### Cover Edge Cases Explicitly
❌ "Handle empty states"
✅ "MUST return empty array [] when no data, NEVER return null/undefined"

---

## Quality Criteria

A well-tightened rule:
- Is testable (can verify pass/fail)
- Is specific (no interpretation needed)
- Has examples (correct and incorrect)
- Is atomic (one concept per rule)

---

## Critical Rules

1. **USE VALIDATION OUTPUT** - Base analysis on actual failures, not assumptions
2. **UPDATE DOMAIN FILES** - Changes must be written to `.flight/domains/`
3. **ADD EXAMPLES** - Every clarification needs correct/incorrect examples
4. **ONE CONCEPT PER RULE** - Keep rules atomic and testable
5. **VERIFY THE FIX** - Re-run validation after tightening

---

## When to Use

| Situation | Use This? |
|-----------|-----------|
| `/flight-validate` reported failures | Yes |
| Rule was ambiguous | Yes |
| Edge case not covered | Yes |
| Code passes validation | No → Continue to next task |
| Starting new task | No → Use `/flight-prime` |

---

## Next Step

After tightening domain rules, re-run the compile/validate cycle:

```
/flight-compile
[implement]
/flight-validate
```

**Workflow**: `/flight-tighten` → `/flight-compile` → [implement] → `/flight-validate`

| Response | Action |
|----------|--------|
| `compile` or `c` | Proceed to `/flight-compile` with updated rules |
| `validate` | Re-run `/flight-validate` to test rule changes |
| `review` | Show the domain file changes made |

---

## Notes

- Each tightening makes the system more reliable
- Domain files are living documents - update them
- Good invariants prevent entire categories of bugs
- After tightening, the same failure should never recur
