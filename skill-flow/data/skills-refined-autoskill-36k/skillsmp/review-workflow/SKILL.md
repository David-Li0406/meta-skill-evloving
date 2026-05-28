---
name: review-workflow
description: Code review workflow with TODO tracking. Use when user says "review", "review-workflow", or asks to review code, PRs, or changes.
---

# Review Workflow

Implements the Review Flow from AGENTS.md with detailed steps and TODO tracking.

## Auto-Start

When this skill is loaded, IMMEDIATELY begin Phase 1. Do NOT wait for user confirmation.

---

## TODOs

Register ALL TODOs at once when starting Phase 1:

```
# Phase 1: Setup
- [ ] Read docs/README.md, core-concepts.md, architecture.md
- [ ] Identify review target (PR, branch, or files) - ask user if unclear
# Phase 2: Verify
- [ ] Run mise run ci
# Phase 3: Review
- [ ] Check: Correctness
- [ ] Check: Tests
- [ ] Check: Architecture
- [ ] Check: Error handling
- [ ] Check: Readability
- [ ] Check: Documentation
# Phase 4: Feedback
- [ ] Provide feedback with proper format
```

---

## Rules

1. **Start immediately** - Begin Phase 1 upon skill load
2. **Register ALL TODOs at once** - Include all phases when starting Phase 1
3. **Update TODOs in real-time** - Mark in_progress/completed as you work
4. **One item in progress at a time** - Focus and complete before moving on
5. **Run code locally** - Never review without running CI
6. **Be constructive** - Goal is to improve, not criticize
7. **Complete all checks** - Don't skip items in the checklist

---

## Reference: Phase Details

### Phase 1: Setup

**Goal**: Understand context and identify what to review.

1. **Read project docs** (skip if already familiar from this session)
   - **MUST read ALL docs**:
     - docs/README.md - Project overview
     - docs/core-concepts.md - Design principles
     - docs/architecture.md - Code structure

2. **Identify review target**
   - Check if user specified a target (PR number, branch, files)
   - Check current branch - if on `feature/*`, review that branch vs main
   - Ask user if still unclear

   ```bash
   # For PR
   gh pr view <number>
   gh pr diff <number>

   # For branch
   git diff main...HEAD
   git log main..HEAD --oneline

   # For uncommitted changes
   git diff
   git status
   ```

### Phase 2: Verify

**Goal**: Verify the code works.

1. **Run CI**
   ```bash
   mise run ci
   ```

2. **Note any failures** - These are blocking issues

### Phase 3: Review

**Goal**: Evaluate code against project standards.

| Check | What to Look For |
|-------|------------------|
| **Correctness** | Does it do what it's supposed to? Edge cases handled? |
| **Tests** | Do tests exist? Are they meaningful? Cover edge cases? |
| **Architecture** | Follows 1 file = 1 UseCase? Proper layer separation? |
| **Error Handling** | All errors handled? Domain errors used? |
| **Readability** | Clear names? Appropriate comments? Not too clever? |
| **Documentation** | docs/ updated if behavior changed? TASKS.md updated? |

**How to Check**:
- Read the diff carefully
- Cross-reference with docs/architecture.md for patterns
- Check that tests actually test the right things

### Phase 4: Feedback

**Goal**: Give actionable feedback.

**Feedback Format**:

```markdown
## Summary
<1-2 sentence overview>

## Blocking Issues
- [BLOCKING] <issue description>
  - Why: <explanation>
  - Suggestion: <how to fix>

## Suggestions
- [NIT] <minor issue>
- [SUGGESTION] <improvement idea>

## Positive Notes
- <what was done well>
```

**Rules for Feedback**:
1. **Be specific** - Point to exact lines/files
2. **Explain why** - Not just "this is wrong"
3. **Suggest alternatives** - Don't just criticize
4. **Distinguish severity** - [BLOCKING] vs [NIT] vs [SUGGESTION]
5. **Acknowledge good work** - Start with positives when possible
