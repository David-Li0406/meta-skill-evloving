---
name: pr-review-response
description: Handle PR review comments using D0-D7 structured workflow. Use when processing code review feedback, responding to reviewer comments, or fixing issues found in PR review.
---

# PR Review Response Workflow

Structured process for handling PR review comments. Each comment is valuable feedback.

## Steps

### D0: Preparation
- Commit current changes
- Clean working directory

### D1: Analyze Comment
1. Read carefully (don't skim)
2. Understand context - look at surrounding code
3. Find similar patterns: `grep -r "pattern" src/`
4. Write in own words: what's the problem?

### D2: Decision
- **FIX** - implement the fix
- **DISCUSS** - need clarification, respond with question
- **SKIP** - not applicable (MUST explain why)
- **DEFER** - create issue for later

### D3: Fix
- Minimal changes
- Follow project patterns
- One fix = one problem

### D4: Verify
```bash
source venv/bin/activate
ruff check src tests --fix    # Linter
ruff format src tests         # Format
pyright src tests             # Type check
pytest                        # Tests
```

### D5: Commit
```bash
git commit -m "fix(scope): description

Addresses review comment by @reviewer
- What changed
- Why

🤖 Generated with [Claude Code](https://claude.com/claude-code)"
```
Reply to the PR comment.

### D6: Reflection (DISCUSS WITH USER!)
- Why did I write it that way initially?
- What did I miss?
- At what stage should I have caught this?

### D7: Prevention
Update documentation to prevent recurrence:
- CLAUDE.md - rules/patterns (only if truly general)
- Skills - for reusable checklists
- Separate commit for D7

```bash
git commit -m "docs: prevent [issue type] - learned from PR #XXX"
```

## Per-Comment Checklist

```
[ ] D1: Understood problem in own words
[ ] D2: Decision + reasoning
[ ] D3: Code or comment
[ ] D4: Verified, works
[ ] D5: Committed + replied to reviewer
[ ] D6: Understood why I made the mistake
[ ] D7: Updated docs (separate commit)
```

## Batch Processing

For multiple comments:
1. D1 for all - understand full picture
2. Group by theme
3. D2-D5 by groups
4. D6-D7 once at the end

## IMPORTANT

D6 is NOT about mechanically adding to CLAUDE.md!
D6 is a DISCUSSION about what went wrong and why.
Only add to docs if it's a genuinely reusable pattern.
