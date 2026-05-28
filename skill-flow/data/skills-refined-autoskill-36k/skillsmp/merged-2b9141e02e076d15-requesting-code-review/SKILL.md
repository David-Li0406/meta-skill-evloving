---
name: requesting-code-review
description: Use this skill when completing tasks, implementing major features, or before merging to verify work meets requirements.
---

# Requesting Code Review

Dispatch superpowers:code-reviewer subagent to catch issues before they cascade.

**Core principle:** Review early, review often.

## When to Request Review

**Mandatory:**
- After each task in subagent-driven development
- After completing major feature
- Before merge to main
- Before creating pull request

**Optional but valuable:**
- When stuck (fresh perspective)
- Before refactoring (baseline check)
- After fixing complex bug

## How to Request

**1. Get git SHAs:**
```bash
BASE_SHA=$(git rev-parse HEAD~1)  # or origin/main
HEAD_SHA=$(git rev-parse HEAD)
```

**2. Dispatch code-reviewer subagent:**

Use Task tool with superpowers:code-reviewer type, fill template at `code-reviewer.md`.

**Placeholders:**
- `{WHAT_WAS_IMPLEMENTED}` - What you just built
- `{PLAN_OR_REQUIREMENTS}` - What it should do
- `{BASE_SHA}` - Starting commit
- `{HEAD_SHA}` - Ending commit
- `{DESCRIPTION}` - Brief summary

**3. Act on feedback:**
- Fix Critical issues immediately
- Fix Important issues before proceeding
- Note Minor issues for later
- Push back if reviewer is wrong (with reasoning)

## Example

```
[Just completed Task 2: Add verification function]

You: Let me request code review before proceeding.

BASE_SHA=$(git log --oneline | grep "Task 1" | head -1 | awk '{print $1}')
HEAD_SHA=$(git rev-parse HEAD)

[Dispatch superpowers:code-reviewer subagent]
  WHAT_WAS_IMPLEMENTED: Verification and repair functions for conversation index
  PLAN_OR_REQUIREMENTS: Task 2 from docs/plans/deployment-plan.md
  BASE_SHA: a7981ec
  HEAD_SHA: 3df7661
  DESCRIPTION: Added verifyIndex() and repairIndex() with 4 issue types

[Subagent returns]:
  Strengths: Clean architecture, real tests
  Issues:
    Important: Missing progress indicators
    Minor: Magic number (100) for reporting interval
  Assessment: Ready to proceed

You: [Fix progress indicators]
[Continue to Task 3]
```

## Integration with Workflows

**Subagent-Driven Development:**
- Review after EACH task
- Catch issues before they compound
- Fix before moving to next task

**Executing Plans:**
- Review after each batch (3 tasks)
- Get feedback, apply, continue

**Ad-Hoc Development:**
- Review before merge
- Review when stuck

## Red Flags

**Never:**
- Skip review because "it's simple"
- Ignore Critical issues
- Proceed with unfixed Important issues
- Argue with valid technical feedback

**If reviewer is wrong:**
- Push back with technical reasoning
- Show code/tests that prove it works
- Request clarification

## Phase-Gated Workflow

### Phase 1: PLANNING
**Input:** User request, git state  
**Output:** Review scope definition

1. Determine git range (BASE_SHA..HEAD_SHA)
2. List files to review (exclude generated, vendor, lockfiles)
3. Identify plan/spec document if available
4. Estimate review complexity (file count, line count)

**Exit criteria:** Git range defined, file list confirmed

### Phase 2: CONTEXT
**Input:** Phase 1 outputs  
**Output:** Reviewer context bundle

1. Extract relevant plan excerpts (what should have been built)
2. Gather related code context (imports, dependencies)
3. Note any prior review findings if re-review
4. Prepare context for code-reviewer agent

**Exit criteria:** Context bundle ready for dispatch

### Phase 3: DISPATCH
**Input:** Phase 2 context  
**Output:** Review findings from agent

1. Invoke code-reviewer agent with context
2. Pass: files, plan reference, git range, description
3. Block until agent returns findings
4. Validate findings have required fields (location, evidence)

**Exit criteria:** Valid findings received

### Phase 4: TRIAGE
**Input:** Phase 3 findings  
**Output:** Categorized, prioritized findings

1. Sort findings by severity (Critical first)
2. Group by file for efficient fixing
3. Identify quick wins vs substantial fixes
4. Flag any findings needing clarification

**Exit criteria:** Findings triaged and prioritized

### Phase 5: EXECUTE
**Input:** Phase 4 triaged findings  
**Output:** Fixes applied

1. Address Critical findings first (blocking)
2. Address High findings (blocking threshold)
3. Address Medium/Low as time permits
4. Document deferred items with rationale

**Exit criteria:** Blocking findings addressed

### Phase 6: GATE
**Input:** Phase 5 fix status  
**Output:** Proceed/block decision

1. Apply severity gate rules
2. Determine if re-review needed
3. Update review status
4. Report final verdict

**Exit criteria:** Clear proceed/block decision with rationale

## Artifact Contract

Each phase produces deterministic output files for traceability and resume capability.

### Artifact Directory

```
~/.local/spellbook/reviews/<project-encoded>/<timestamp>/
```

### Phase Artifacts

| Phase | Artifact | Description |
|-------|----------|-------------|
| 1 | `review-manifest.json` | Git range, file list, metadata |
| 2 | `context-bundle.md` | Plan excerpts, code context |
| 3 | `review-findings.json` | Raw findings from agent |
| 4 | `triage-report.md` | Prioritized, grouped findings |
| 5 | `fix-report.md` | What was fixed, what deferred |
| 6 | `gate-decision.md` | Final verdict with rationale |

### SHA Persistence

<CRITICAL>
Always use `reviewed_sha` from manifest for inline comments.
Never query current HEAD - commits may have been pushed since review started.
</CRITICAL>