---
name: rca-verification
description: Methods for validating root cause analyses. Provides checklists for 5 Whys depth, execution path accuracy, and fix strategy soundness. Use when reviewing RCA reports.
---

# RCA Verification Skill

This skill provides verification patterns for validating root cause analyses.

## When to Use

- After RCA Analyst produces rca-report.md
- When validating 5 Whys methodology application
- When assessing fix strategy soundness
- Before proceeding to implementation planning

## Verification Categories

### 1. 5 Whys Depth Validation

The 5 Whys should reach a **fundamental cause**, not just a symptom.

**Quality Checklist:**

| Check | Pass Criteria | Detection Method |
|-------|---------------|------------------|
| **Depth** | At least 3 Whys for simple bugs; 5 for complex | Count + complexity |
| **Progression** | Each Why digs deeper than previous | Logical analysis |
| **Fundamentality** | Root cause can't be explained by more code | Pattern matching |
| **Specificity** | Root cause is precise, not vague | Clarity check |
| **Category Fit** | Category matches the evidence | Cross-reference |

**Red Flags (Shallow Root Causes):**

These are symptoms, not root causes:

| Shallow Statement | Why It's a Symptom | What to Ask Next |
|-------------------|-------------------|------------------|
| "The variable is null" | Doesn't explain why it's null | WHY is it null? (initialization? race condition?) |
| "The function returns undefined" | Doesn't explain the design issue | WHY does it return undefined? (missing case?) |
| "The API call fails" | Doesn't identify the actual failure | WHY does it fail? (timeout? auth? data?) |
| "No one added them" | Doesn't explain the process gap | WHY didn't anyone add them? (no process?) |
| "The condition is wrong" | Doesn't explain the root decision | WHY is it wrong? (spec misread? edge case?) |

**Good Root Causes (Fundamental):**

These cannot be explained by more "Why" questions:

- ✅ "The function was designed for authenticated contexts but reused for public endpoints without null checks"
- ✅ "The timeout was hardcoded based on average response time, not accounting for load spikes"
- ✅ "The cache invalidation logic doesn't cover the mutation path added in PR #123"
- ✅ "No documentation governance process exists to ensure template completeness"
- ✅ "The error handling strategy assumes all failures are transient, but this failure is permanent"

### 2. Execution Path Verification

All file:line references must be verified against the actual codebase.

**For each reference:**

1. **File Exists**: Use `#tool:search/fileSearch` to confirm file path
2. **Line Accurate**: Use `#tool:read/readFile` to verify content at line
3. **Content Matches**: Compare description to actual code
4. **Call Chain Valid**: Use `#tool:search/usages` to verify connections

**Verification Table Template:**

```markdown
| Step | File:Line | Exists | Content Matches | Verdict |
|------|-----------|--------|-----------------|---------|
| Entry | `src/file.ts:45` | ✅ | ✅ | ✅ PASS |
| Step 2 | `src/other.ts:120` | ✅ | ⚠️ Line off by 3 | ⚠️ MINOR |
| Fault | `src/bug.ts:78` | ❌ | N/A | ❌ FAIL |
```

**Correction Format:**

```markdown
| Original | Actual | Impact |
|----------|--------|--------|
| `file.ts:45` | `file.ts:48` (line shifted) | Low |
| `missing.ts:10` | File not found | 🔴 Critical |
```

### 3. Fix Strategy Assessment

The fix must address the root cause, not just mask the symptom.

**Checklist:**

| Check | Method | Pass Criteria |
|-------|--------|---------------|
| **Targets Root Cause** | Compare fix to root cause location | Fix modifies root cause site |
| **File Targets Exist** | `#tool:search/fileSearch` | All files found |
| **Line Numbers Accurate** | `#tool:read/readFile` | Code matches |
| **Risk Assessment Realistic** | Compare to complexity | Risks match reality |
| **Alternatives Genuine** | Check distinct approaches | Not trivial variations |
| **Testing Strategy Valid** | Check test paths | Test files exist |

**Common Issues:**

1. **Symptom Masking**: Fix adds null check instead of fixing why null occurs
2. **Risk Underestimation**: Claims "Low risk" for change affecting many files
3. **Trivial Alternatives**: "Alternative" is just minor variation of primary
4. **Missing Side Effects**: Doesn't consider impact on callers

### 4. Side Effect Analysis

Check what else might be affected by the proposed fix.

**For each modified component:**

1. Find all usages with `#tool:search/usages`
2. Assess impact on each caller
3. Flag breaking changes
4. Note edge cases

**Risk Categories:**

| Risk Level | Criteria | Action |
|------------|----------|--------|
| **Low** | Few callers, simple change | Note for awareness |
| **Medium** | Multiple callers, behavior change | Require test coverage |
| **High** | Many callers, breaking change | Require explicit approval |

## Output Templates

### verified-rca.md Structure

```markdown
# Verified RCA: {TICKET-ID}

**Date**: {YYYY-MM-DD}
**Verifier**: AI Agent (RCA Verifier)
**Original RCA**: `rca-report.md`
**Status**: [VERIFIED / VERIFIED WITH NOTES / NEEDS REVISION]

---

## Verification Summary

| Category | Status | Issues | Confidence |
|----------|--------|--------|------------|
| 5 Whys Depth | ✅/⚠️/❌ | [count] | High/Medium/Low |
| Execution Path | ✅/⚠️/❌ | [count] | High/Medium/Low |
| Fix Strategy | ✅/⚠️/❌ | [count] | High/Medium/Low |
| Side Effects | ✅/⚠️/❌ | [count] | High/Medium/Low |

**Overall Confidence**: [HIGH / MEDIUM / LOW]

---

[Detailed sections for each category...]

---

## Recommendation

**Status**: [VERIFIED / VERIFIED WITH NOTES / NEEDS REVISION]

[Explanation and next steps...]
```

### Status Definitions

| Status | Meaning | Next Step |
|--------|---------|-----------|
| **VERIFIED** | RCA is accurate and fix strategy sound | Proceed to planning |
| **VERIFIED WITH NOTES** | Substantially accurate, minor concerns | Proceed with awareness |
| **NEEDS REVISION** | Critical issues found | Return to RCA Analyst |

## Edge Cases

### Simple Bugs (2-3 Whys)

Not all bugs need 5 Whys. Simple bugs may reach fundamental cause faster:

- **Typo**: 2 Whys may suffice if clearly a one-off mistake
- **Simple Logic Error**: 3 Whys may reach design decision
- **Configuration Issue**: 2-3 Whys may reach process gap

**Verify**: Even short chains must reach fundamental cause.

### Complex Bugs (5+ Whys)

Deep analysis appropriate for:

- **Architectural Issues**: May need 5+ to reach design decisions
- **Multi-Component Bugs**: Need to trace across boundaries
- **Recurring Issues**: Must find why previous fixes didn't work

**Watch for**: Circular reasoning after 7+ Whys.

### Process/Governance Root Causes

When root cause is absence of process:

- **Valid**: "No code review process caught this anti-pattern"
- **Valid**: "No documentation governance ensures completeness"
- **Invalid**: "Someone made a mistake" (too vague)

**Verify**: Process gap is specific and actionable.

## Revision Loop Prevention

To prevent endless cycles between Verifier and Analyst:

1. **Maximum 2 revision attempts** before human escalation
2. **Track recurring issues** in verified-rca.md
3. **Escalate if same issues persist**

**Escalation message:**

```
⚠️ REVISION LOOP DETECTED

This RCA has been revised [X] times with recurring issues.
Manual review required.
```

## References

- RCA Analyst Agent: `.github/agents/rca-analyst.agent.md`
- RCA Verifier Agent: `.github/agents/rca-verifier.agent.md`
- Research Verifier Pattern: `.github/agents/research-verifier.agent.md`
- Bug Fixing Workflow: `context/bug-fixing-workflow-design-plan.md`
