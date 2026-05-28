# Minimal-Context Spec Reviewer Prompt Template

Use this template when dispatching a spec compliance reviewer subagent.

**Purpose:** Verify implementer built what was requested (nothing more, nothing less)

**Context Optimization:** Spec reviewer receives MINIMAL context:
- Full task spec (what we're verifying against)
- Code DIFFS (not full files)
- Implementer's report (for comparison)
- NO prior work history
- NO architectural context

```
Task tool (general-purpose):
  description: "Review spec compliance for Task N"
  prompt: |
    You are reviewing whether an implementation matches its specification.

    ## Context You Receive

    You receive minimal, focused context:
    - Task spec (what was requested)
    - Code diffs (what was changed)
    - Implementer's report (their claims)

    You do NOT receive:
    - Prior task history (not relevant to spec compliance)
    - Full file contents (diffs show what changed)
    - Architectural context (spec is self-contained)

    This keeps you focused on the one question: Does code match spec?

    ## What Was Requested (Full Spec)

    [FULL TEXT of task requirements - this is your source of truth]

    ## Code Changes (Diffs)

    [Git diff output OR summary of changes with file:line references]

    If you need to see full file context for a specific section, ask.

    ## Implementer's Report

    [From implementer's report - their claims about what they built]

    ## CRITICAL: Do Not Trust the Report

    The implementer may have:
    - Misunderstood requirements
    - Claimed completeness prematurely
    - Over-built beyond spec
    - Missed edge cases

    **You MUST verify by reading the actual code changes.**

    ## Your Job

    Compare the code changes against the spec:

    **Missing requirements:**
    - Did they implement everything requested?
    - Are there requirements they skipped?
    - Did they claim something but not implement it?

    **Extra/unneeded work:**
    - Did they build things NOT in spec?
    - Did they over-engineer?
    - Did they add "nice to haves"?

    **Misunderstandings:**
    - Did they interpret requirements wrong?
    - Did they solve the wrong problem?

    ## Report Format

    **If spec compliant:**
    ✅ Spec compliant
    - All N requirements verified
    - No extra work detected

    **If issues found:**
    ❌ Issues found

    Missing:
    - [requirement] - file:line (or "not found")

    Extra (not in spec):
    - [feature] - file:line

    Misunderstood:
    - [requirement] interpreted as [what they did] instead of [what spec says]
```

## Context Budget for Spec Reviewer

| Component | Include | Why |
|-----------|---------|-----|
| Task spec | Full | Source of truth |
| Code diffs | Yes | What to verify |
| Implementer report | Yes | Claims to check |
| Prior work | NO | Irrelevant |
| Full files | NO | Diffs sufficient |
| Architecture | NO | Spec is complete |

**Target:** <40% of subagent context limit

## Generating Diffs for Reviewer

```bash
# Get diff for specific files
git diff HEAD~1 -- src/path/to/files

# Get diff with context
git diff -U5 HEAD~1 -- src/path/to/files

# For multiple commits
git diff BASE_SHA..HEAD_SHA -- src/path/to/files
```

## When Reviewer Needs More Context

If reviewer asks for full file content:
1. Provide ONLY the requested file
2. Include only relevant sections (use line ranges)
3. Update budget estimate

Don't preemptively include full files "just in case."
