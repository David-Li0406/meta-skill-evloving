---
name: review-design
description: Multi-perspective design review with parallel reviewers and explicit revise loop (Track L)
---

# Design Review Workflow

Multi-perspective design review of Technical Design Documents (TDDs) with parallel reviewers and an explicit revise loop. This is a required gate before proceeding to `/write-beads` for Track L work.

## When to use

Use when you have:
- A polished Technical Design Document from `/plan-polish` (Stage 2)
- Track L work that requires comprehensive design review before decomposition
- Need to gate design quality before creating implementation beads

## Position in Planning Lifecycle

```
Stage 1: /intake (routing)
    ↓
Stage 2: /plan-polish (TDD creation)
    ↓
Stage 3: /review-design ← YOU ARE HERE
    ↓ (APPROVED_FOR_DECOMPOSITION)
Stage 4: /write-beads (bead creation)
    ↓
Stage 5: /bead-review (bead QA)
    ↓
Stage 6: /create-beads (import to bd)
```

## Role

You are a Review Synthesizer coordinating multiple specialized reviewers. You spawn parallel reviewers, consolidate their findings, and produce a verdict that gates progression to `/write-beads`.

## Required Reviewers

Each reviewer operates as an independent perspective. Run ALL reviewers in parallel.

### 1. Security Reviewer

**Focus areas:**
- Authentication and authorization gaps
- Input validation and sanitization
- Data exposure risks
- Secrets management
- OWASP Top 10 vulnerabilities
- Dependency security concerns

**Output:** Findings with severity and revision instructions anchored to TDD sections.

### 2. Performance Reviewer

**Focus areas:**
- N+1 query patterns
- Missing indexes or caching strategies
- Resource bottlenecks (CPU, memory, I/O)
- Scalability concerns
- Timeout and retry policies
- Async/sync operation choices

**Output:** Findings with severity and revision instructions anchored to TDD sections.

### 3. API Design Reviewer

**Focus areas:**
- REST/GraphQL best practices
- Consistent naming conventions
- Appropriate HTTP methods and status codes
- Versioning strategy
- Error response format consistency
- Breaking change risks
- Rate limiting considerations

**Output:** Findings with severity and revision instructions anchored to TDD sections.

### 4. Domain Reviewer(s)

**Inferred from TDD content.** Examples:
- Database schema complexity → Database Reviewer
- Real-time features → Concurrency Reviewer
- External integrations → Integration Reviewer
- UI/UX components → Accessibility Reviewer
- ML/AI features → ML Ops Reviewer

**Selection criteria:** Analyze TDD to identify domain-specific concerns not covered by the three mandatory reviewers.

**Output:** Findings with severity and revision instructions anchored to TDD sections.

## Iteration Policy Integration

This skill follows the iteration policy defined in `docs/guides/iteration-policy.md`.

### Before Generating Findings

1. **Check for existing ledger:**
   ```bash
   if [ -f "docs/plans/<project>/DESIGN_LEDGER.md" ]; then
     # Read and incorporate prior findings
     cat "docs/plans/<project>/DESIGN_LEDGER.md"
   fi
   ```

2. **Consume previous ledger:** If a ledger exists, understand which issues are:
   - `open` - still needs fixing
   - `fixed` - resolved in prior pass
   - `waived` - explicitly accepted with justification

### Finding Classification

Every finding MUST be classified as one of:

| Classification | Description | Action |
|----------------|-------------|--------|
| `net-new` | First time seeing this issue | Must be addressed |
| `known-open` | Seen before, not yet fixed | Track until fixed |
| `regression` | Previously fixed but reappeared | Immediate attention |
| `waived` | Explicitly accepted | Requires justification |

### Stable IssueId Format

All issues must use anchored identifiers:

```
design-review::<type>::<anchor>
```

**Type values:** `coverage`, `atomicity`, `dependency`, `context`, `format`, `api-contract`, `version`, `security`, `performance`, `other`

**Anchor examples:**
- `section:Error Handling` - Document section
- `api:POST /users` - API endpoint
- `file:src/lib/auth.ts` - File path

**Complete examples:**
```
design-review::security::section:Authentication
design-review::performance::api:GET /reports
design-review::api-contract::section:API Endpoints
```

## Reviewer Output Schema

Each reviewer returns findings in this format:

```markdown
### Reviewer: {Reviewer Name}

#### Finding 1

**IssueId:** design-review::{type}::{anchor}
**Classification:** net-new|known-open|regression|waived
**Severity:** blocker|should-fix|minor
**Problem:** {Clear description of what's wrong}
**Why it matters:** {Impact if not addressed}
**Revision instruction:** In section "{exact section heading}", {specific change required}

#### Finding 2
...
```

## Verdict Enum (Locked)

The verdict MUST be one of these two values:

| Verdict | Meaning | Next Step |
|---------|---------|-----------|
| `APPROVED_FOR_DECOMPOSITION` | Design is ready | Proceed to `/write-beads` |
| `REVISE_AND_RESUBMIT` | Design needs revision | Return to `/plan-polish` |

## Synthesis Rules

### Verdict Determination

1. **If ANY blocker exists** → `REVISE_AND_RESUBMIT`
2. **If regressions exist** → `REVISE_AND_RESUBMIT`
3. **Otherwise** → `APPROVED_FOR_DECOMPOSITION`

### Anti-Compounding Guardrail

**A blocker MUST cite anchored evidence.**

If a finding cannot be anchored to one of these, it cannot be classified as a blocker:
- Section heading (e.g., `section:Error Handling`)
- File path (e.g., `file:services/web/src/auth.ts`)
- API endpoint (e.g., `api:POST /users`)

**Invalid blocker (would be downgraded):**
```
design-review::other::general
- Severity: blocker  ❌ Cannot be blocker - no anchor
- Evidence: "The overall approach seems problematic"  ❌ Not anchored
```

### Required Revisions

When verdict is `REVISE_AND_RESUBMIT`, the Required Revisions section MUST:
- Reference specific TECHNICAL_DESIGN.md section headings
- Provide concrete, actionable revision instructions
- Include all blockers and regressions

## Design Convergence Stop Rules

Design iterations stop when ALL of these are true:

1. **Schema valid:** `TECHNICAL_DESIGN.md` passes schema validation
2. **Review approved:** `DESIGN_REVIEW.md` reaches `APPROVED_FOR_DECOMPOSITION` with `regression = 0`
3. **Two-pass stability:** Either:
   - 0 blockers in two consecutive full design reviews, OR
   - 0 blockers + 0 regressions + no net-new blockers

## Output Format

Generate `docs/plans/<project>/DESIGN_REVIEW.md`:

```markdown
# Design Review - {Project Name}

**TDD:** [TECHNICAL_DESIGN.md](./TECHNICAL_DESIGN.md)
**Review Date:** {YYYY-MM-DD}
**Pass Number:** {N}

## Verdict

**{APPROVED_FOR_DECOMPOSITION | REVISE_AND_RESUBMIT}**

## Summary

| Metric | Count |
|--------|-------|
| Blockers | {n} |
| Should-fix | {n} |
| Minor | {n} |
| Total findings | {n} |
| Regressions | {n} |
| Net-new blockers | {n} |

## Reviewer Findings

### Security Reviewer

{findings using schema above}

### Performance Reviewer

{findings using schema above}

### API Design Reviewer

{findings using schema above}

### Domain Reviewer: {Name}

{findings using schema above}

## Required Revisions

{Only if verdict is REVISE_AND_RESUBMIT}

| # | Section | Revision Required | Severity |
|---|---------|-------------------|----------|
| 1 | {exact section heading} | {specific change} | blocker |
| 2 | {exact section heading} | {specific change} | blocker |

## Approval Conditions

{Only if verdict is APPROVED_FOR_DECOMPOSITION}

- [ ] All blockers resolved
- [ ] No regressions from prior passes
- [ ] Design ready for `/write-beads` decomposition

## Next Steps

{If APPROVED_FOR_DECOMPOSITION}
Proceed to `/write-beads` to decompose this design into implementation beads.

{If REVISE_AND_RESUBMIT}
Return to `/plan-polish` with the Required Revisions above. After updating TECHNICAL_DESIGN.md, re-run `/review-design`.
```

## Update DESIGN_LEDGER.md

After generating DESIGN_REVIEW.md, update the ledger:

```markdown
# Design Review Ledger - {project}

## Pass Log
- Pass 1: /review-design {date}
- Pass 2: /review-design {date}
...

## Issues

### design-review::{type}::{anchor}
- Stage: design-review
- Severity: blocker|should-fix|minor
- Status: open|fixed|waived
- First seen: pass {n}
- Last updated: pass {n}
- Evidence:
  - {anchored description}
- Fix:
  - {what changed, if fixed}
- Notes:
  - {optional}
```

## Common Failure Modes

| Failure Mode | Prevention |
|--------------|------------|
| Missing reviewer perspective | Always run all 4 reviewer types (3 mandatory + domain-inferred) |
| Verdict set to APPROVED despite unresolved blockers | Synthesis rule: ANY blocker → REVISE_AND_RESUBMIT |
| Required Revisions not anchored to specific TDD sections | All revision instructions must cite exact section headings |
| Not consuming previous ledger | First step: check if DESIGN_LEDGER.md exists |
| Blockers without anchored evidence | Anti-compounding guardrail: downgrade or reject unanchored blockers |
| Infinite review loops | Apply stop rules: two-pass stability or no blockers + no regressions |

## Feedback Loop

If verdict is `REVISE_AND_RESUBMIT`:

1. Return to `/plan-polish` with the Required Revisions
2. Update `TECHNICAL_DESIGN.md` to address all blockers
3. Re-run `/review-design`
4. Repeat until `APPROVED_FOR_DECOMPOSITION`

## Quality Gate

Before finalizing the review:

- [ ] All 4 reviewer perspectives provided (3 mandatory + domain)
- [ ] Every finding has valid IssueId with proper anchor
- [ ] Every blocker cites anchored evidence
- [ ] Verdict correctly reflects blocker/regression count
- [ ] Required Revisions (if any) reference specific TDD sections
- [ ] DESIGN_LEDGER.md updated with pass entry
- [ ] Classification applied to all findings (net-new/known-open/regression/waived)

## Next Steps

- If `APPROVED_FOR_DECOMPOSITION`: Run `/write-beads` to decompose into implementation beads
- If `REVISE_AND_RESUBMIT`: Update TDD via `/plan-polish`, then re-run `/review-design`
