---
name: maintaining-project-context
description: Use when updating CLAUDE.md or domain context files after code changes. Covers change categorization, file mapping, and contract-level documentation standards.
---

# Maintaining Project Context

## Overview

Project context files (CLAUDE.md) document contracts and architectural intent for future agents and developers. When code changes alter contracts, the documentation must update to match. This skill provides a systematic process for identifying contract-level changes and updating the appropriate context files.

## When to Use

- After completing a work plan execution
- After significant refactors that change module boundaries
- When new domains or modules are created
- When APIs or interfaces change
- When the documentarian agent is invoked

## Core Pattern

### Step 1: Capture Git State

Record the commit range for analysis:

```bash
git rev-parse HEAD      # Current state
git log --oneline -10   # Recent history for context
git branch --show-current
```

### Step 2: Analyze Changes

List all changed files since the base commit:

```bash
git diff --name-status [base-commit]..HEAD
```

### Step 3: Categorize Each Change

Classify each changed file as contract or internal:

| Category | Examples | Action |
|----------|----------|--------|
| Contract | New modules, API changes, interface changes, architectural decisions, new dependencies | Update context |
| Internal | Bug fixes, refactoring with same behavior, test additions, implementation details | Skip |

**Contract changes** affect how other code interacts with this code. They change the "what" or the "interface."

**Internal changes** affect how this code works without changing its external behavior. They change the "how" without touching the "what."

### Step 4: Map Changes to Context Files

Determine which context files need updates:

| Change Location | Context File | Rationale |
|-----------------|--------------|-----------|
| Cross-cutting (build, CI, tooling) | Root `CLAUDE.md` | Affects entire project |
| Single domain (`src/auth/`) | `src/auth/CLAUDE.md` | Domain-specific contracts |
| Multiple domains | Each domain's context file | Contracts belong where they live |

**When to create a new domain context file:**
- A new directory contains 3+ files with distinct contracts
- The domain has its own API surface or invariants
- Future agents would benefit from domain-specific guidance

### Step 5: Read Existing Context Files

Before drafting updates, read the current state:

```bash
cat CLAUDE.md
cat src/[domain]/CLAUDE.md  # if exists
```

Understand what is already documented. Updates should add to or modify existing content, not duplicate it.

### Step 6: Draft Updates

Write updates following these standards:

**Content focus:**
- Document contracts: "The auth module exposes `authenticate(token)` which returns a User or raises AuthError"
- Document invariants: "All API responses include a `request_id` header for tracing"
- Document architectural decisions: "We use repository pattern; data access lives in `storage/`"

**Writing standards (from technical-writing skill):**
- Active voice, present tense: "The function returns" not "will return"
- No contractions: "do not" not "don't"
- Demonstratives need nouns: "this module" not "this"
- Sentences under 40 words

### Step 7: Recommend New Domain Files

If a new domain warrants its own context file, recommend creation:

```markdown
**Recommendation:** Create `src/payments/CLAUDE.md`

Rationale:
- New domain with 5 files
- Distinct API surface (PaymentProcessor, RefundHandler)
- Domain-specific invariants (all amounts in cents, idempotency keys required)
```

### Step 8: Write Files First

Write the context files using the Edit or Write tool. Do not claim to "show" content in your response. The files must exist on disk before asking for approval.

```bash
# After writing, verify files exist
ls -la CLAUDE.md src/*/CLAUDE.md
```

### Step 9: Ask for Approval

Use `AskUserQuestion` to request approval. Reference file paths so the user can inspect the actual files:

```
I have written the following context updates:

**Files written:**
- `CLAUDE.md` (updated)
- `src/payments/CLAUDE.md` (created)

You can inspect these files before approving. Run `git diff` to see changes to existing files.

Approve these updates?
- Approve and commit
- Reject and revert changes
```

**On approval:** Proceed to commit.

**On rejection:** Revert the changes:
```bash
git checkout -- CLAUDE.md src/*/CLAUDE.md
# Remove any newly created files
rm src/payments/CLAUDE.md  # if it was new
```

### Step 10: Commit Documentation Separately

Documentation commits stay separate from code commits:

```bash
git add CLAUDE.md src/*/CLAUDE.md
git commit -m "docs: update project context for [branch/feature]"
```

## Quick Reference

```
1. Capture git state (base, HEAD, branch)
2. List changed files (git diff --name-status)
3. Categorize: contract vs internal
4. Map to context files (root or domain)
5. Read existing context
6. Draft updates (contracts, invariants, decisions)
7. Recommend new domain files if needed
8. Write files to disk (do not just "show" them)
9. Ask for approval with file paths
10. On approval: commit; on rejection: revert
```

## Common Mistakes

| Mistake | Why It Fails | Correct Approach |
|---------|--------------|------------------|
| Updating for every change | Bloats context with implementation details | Only contract changes warrant updates |
| Documenting implementation | Future agents need contracts, not how-it-works | Focus on what, not how |
| Skipping human approval | Users lose control over their documentation | Always use AskUserQuestion |
| Bundling with code commits | Mixes concerns, harder to review | Separate documentation commits |
| Creating domain files too early | Single-file domains do not need their own context | Wait for 3+ files with distinct contracts |
| Duplicating root content in domains | Causes drift and bloat | Cross-reference; do not duplicate |
| Claiming to "show" content without writing files | User cannot verify what does not exist | Write files first, then ask for approval |

## Anti-Rationalizations

- "The code is self-documenting" — Code documents implementation. Context files document intent, contracts, and architectural decisions that span files.
- "This change is too small to document" — If it changes a contract, it matters. Size is irrelevant; contract impact determines documentation need.
- "I will update context later" — Later never comes. Update context as part of the workflow, not as an afterthought.
- "The user will notice if something is wrong" — Users trust agent-generated documentation. Get approval before committing.

## Summary

1. **Only update for contract changes.** Implementation details do not belong in context files.
2. **Map changes to the right context file.** Root for cross-cutting; domain for domain-specific.
3. **Require human approval.** Use AskUserQuestion before committing any updates.
4. **Commit documentation separately.** Keep documentation commits distinct from code commits.
