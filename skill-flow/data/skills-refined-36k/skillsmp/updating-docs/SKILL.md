---
name: updating-docs
description: |
  Guide documentation updates through the Architecture Decision Workflow. You must use this skill when: (1) Code changes reveal undocumented or conflicting conventions, (2) A learning or incident suggests documentation should change, (3) Reviewing changes for durable context updates, (4) Asked to update documentation, (5) PR introduces patterns that may need documenting, (6) You plan on adding or changing a file in the docs/ directory or any CLAUDE.md files. Ensures all documentation changes are intentional, traceable, and human-auditable.
---

# Documentation Update Workflow

## Core Principle

**Documentation changes must be intentional, traceable, and human-auditable.**

<!-- Per AD-0103 -->
**Scope:** Despite the "Architecture Decision" naming, this workflow applies to **all documentation changes**—architectural decisions, convention updates, factual corrections, and process changes. The value is traceability, not architectural gatekeeping.

All documentation updates follow the Architecture Decision Workflow defined in:
**[docs/ARCHITECTURE_DECISION_WORKFLOW.md](docs/ARCHITECTURE_DECISION_WORKFLOW.md)**

Read that document first—it is the source of truth for this process.

---

## When to Invoke This Skill

Use `/updating-docs` when:
- Code changes reveal undocumented conventions
- Code contradicts documented conventions
- A learning, article, or incident suggests docs should change
- Tech debt discussion surfaces documentation gaps
- New patterns emerge that should be standardized
- Asked to "update the docs" or "document this decision"
- Reviewing changes for "durable context updates"
- PR introduces changes that may conflict with documented standards

---

## Workflow Execution

### Step 1: Gather Evidence

**Reference:** See "Step 1: Gather Evidence" in the workflow doc.

1. Read the trigger event and identify the type
2. Gather relevant evidence (code changes, current docs, observations)
3. Create a State of the Union document at `docs/decisions/evidence/YYYY-MM-DD-short-title.md`
4. List potentially affected documentation

**Then ask the user for Gate 1 decision:**

> **Gate 1: Do we need to update documentation?**
>
> Based on the evidence gathered, consider:
> - Does this show a gap between code and docs?
> - Does this show outdated information?
> - Is there enough to warrant formal analysis?
>
> Please respond: **YES** or **NO**

### Step 2: Draft AD (if Gate 1 = YES)

**Reference:** See "Step 2: Draft AD" in the workflow doc.

1. Assign AD number (0100+ for new decisions, check existing highest)
2. Create draft at `docs/decisions/drafts/XXXX-title.md`
3. Research and analyze alternatives (minimum 3)
4. Make clear recommendation
5. List all affected documentation files

**Then ask the user for Gate 2 decision:**

> **Gate 2: Do you approve this decision?**
>
> Evaluate:
> - Is the problem clearly stated?
> - Are alternatives genuinely evaluated?
> - Is the decision clear and unambiguous?
> - Is the affected documentation list complete?
>
> Please respond: **APPROVE**, **REVISE** (with feedback), or **REJECT** (with reason)

### Step 3: Propagate (if Gate 2 = APPROVE)

**Reference:** See "Step 3: Propagate" in the workflow doc.

1. Move AD to `docs/decisions/accepted/`
2. Update each affected file with the decision
3. Add traceability comments: `<!-- Per AD-XXXX -->`
4. Prepare commits: `docs(<scope>): apply AD-XXXX - <description>`
5. Append propagation report to AD

**Then ask the user for Gate 3 decision:**

> **Gate 3: Are the changes correct and complete?**
>
> Verify:
> - Each change reflects the AD decision
> - All affected files updated
> - Traceability comments in place
> - Commits properly formatted
>
> Please respond: **APPROVE**, **REVISE** (with feedback), or **REJECT** (with reason)

### Complete (if Gate 3 = APPROVE)

1. Move AD to `docs/decisions/implemented/`
2. Update status to `Implemented`
3. Commit: `docs: implement AD-XXXX - [title]`

---

## Quick Reference: Directory Flow

| Stage | Location |
|-------|----------|
| Evidence (awaiting Gate 1) | `docs/decisions/evidence/` |
| Archived (Gate 1 = NO) | `docs/decisions/evidence/archived/` |
| Draft (awaiting Gate 2) | `docs/decisions/drafts/` |
| Accepted (awaiting Gate 3) | `docs/decisions/accepted/` |
| Implemented (complete) | `docs/decisions/implemented/` |
| Rejected | `docs/decisions/rejected/` |

---

## Retroactive Documentation

For decisions already implemented in code without an ADR:

**Reference:** See "Retroactive Documentation" section in the workflow doc.

Key differences:
- Skip Step 1 (evidence gathering)—decision already exists in code
- Use trigger type: `retroactive-documentation`
- Include `## Code Evidence` section with file paths
- Use numbering range `0001-0099`
- Gates can be pre-approved in batch

See existing examples: `docs/decisions/implemented/0001-*.md` through `0008-*.md`

---

## Checklist

Before completing any documentation update:

- [ ] Read [docs/ARCHITECTURE_DECISION_WORKFLOW.md](docs/ARCHITECTURE_DECISION_WORKFLOW.md)
- [ ] Created appropriate artifacts per workflow stage
- [ ] Obtained user approval at each gate
- [ ] Added traceability comments (`<!-- Per AD-XXXX -->`)
- [ ] Commits follow format: `docs(<scope>): apply AD-XXXX - <desc>`
- [ ] AD moved to correct directory based on final status
