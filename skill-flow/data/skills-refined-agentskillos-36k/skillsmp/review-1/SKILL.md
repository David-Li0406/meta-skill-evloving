---
name: review
description: Code review using multiple AI models concurrently
---

# Code Review

Performs code reviews using subagents with multiple models running concurrently.

## Execution

**IMPORTANT:** Do NOT perform workflow steps directly. You MUST delegate ALL steps to subagents as specified below.

### Phase 1: Setup (via @general)

Launch `@general` subagent to perform steps 1-2:
- Determine what to review based on user request
- Get the diff/content
- Return the diff content back to you

### Phase 2: Concurrent Reviews (via @general-opus, @general-codex, @general-gemini)

Launch ALL THREE review agents in parallel, passing them the diff from Phase 1.

### Phase 3: Synthesis (via @general)

Launch `@general` subagent to perform steps 5-6:
- Synthesize the reviews
- Post PR comments if requested

---

## Workflow Details

### 1. Determine What to Review

Based on user request:

| User Says | Action |
|-----------|--------|
| "review this PR" / "review PR #123" | Get PR diff with `gh pr diff` |
| "review my changes" / "review staged" | Get staged diff with `git diff --staged` |
| "review <file>" | Read the specific file(s) |
| No specific request | Ask user what to review |

### 2. Get the Diff/Content

For staged changes:
```bash
git diff --staged
```

For PR (current branch):
```bash
gh pr diff
```

For specific PR:
```bash
gh pr diff <number>
```

### 3. Run Reviews Concurrently

Launch ALL THREE agents in parallel with the prompt:

> You are a senior code reviewer. Review the following git diff for:
> - Code quality issues
> - Potential bugs
> - Security concerns
> - Suggestions for improvement
>
> Be concise and actionable. If the code looks good, say so briefly.
>
> Diff:
> $diff

### 4. Present Reviews

Show all three review outputs to the user, labeled by model.

### 5. Synthesize (Optional)

Summarize the common themes across all three reviews, if any.

### 6. PR Comments (Optional)

If reviewing a PR and user has asked to leave comments:

```bash
gh pr review <number> --comment --body "<comment>"
```

Or for line-specific comments:
```bash
gh api repos/{owner}/{repo}/pulls/{pr}/comments \
  --method POST \
  -f body="<comment>" \
  -f commit_id="<sha>" \
  -f path="<file>" \
  -f line=<line>
```

Ask user before posting any comments.
