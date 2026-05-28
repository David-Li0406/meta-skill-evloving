---
name: review
description: Code review skill. Use when reviewing changes, commits, branches, or pull requests. Focuses on bugs, structure, performance with actionable feedback.
---

# Review Skill

Review code changes. Focus: bugs first, then structure, performance.

---

## What to Review

User input determines review type:

1. **Default (no target)**: Uncommitted changes
   - `git diff` - unstaged
   - `git diff --cached` - staged

2. **Commit hash** (SHA or short): Specific commit
   - `git show <commit>`

3. **Branch name**: Compare current to branch
   - `git diff <branch>...HEAD`

4. **PR** (github.com/pull or PR number): Pull request
   - `gh pr view <pr>` - context
   - `gh pr diff <pr>` - diff

Use best judgement.

---

## Gather Context

**Diffs alone insufficient.** After diff, read full file(s) modified. Understand context.

- Diff identifies changed files
- Read full files for patterns, flow, error handling
- Check conventions: CONVENTIONS.md, AGENTS.md, .editorconfig

---

## Focus Areas

**Bugs** - Primary.

- Logic errors, off-by-one, wrong conditionals
- Missing/incorrect guards, unreachable paths
- Edge cases: null/empty/undefined, errors, races
- Security: injection, auth bypass, data exposure
- Broken error handling: swallowed failures, unexpected throws, uncaught error types

**Structure** - Fits codebase?

- Follows existing patterns/conventions?
- Misses established abstractions?
- Excessive nesting (flatten with early returns/extract)

**Performance** - Flag only if obvious.

- O(n²) on unbounded, N+1 queries, blocking I/O hot paths

---

## Before Flagging

**Be certain.** Bug claim requires confidence.

- Review changes only - ignore pre-existing code
- Don't flag if unsure - investigate first
- No hypothetical problems - explain realistic scenario if edge case matters
- Get more context if needed

**Don't be a style zealot.**

- Verify actual violation. Don't complain about `else` if early returns correct.
- Some "violations" acceptable if simplest option. `let` fine if alternative convoluted.
- Excessive nesting always concern.
- Don't flag style preferences unless clearly violates project conventions.

---

## Tools

Use to inform review:

- **Explore agent** - Check existing code patterns, conventions, prior art
- **Exa Code Context** - Verify library/API usage before flagging
- **Exa Web Search** - Research best practices if unsure

If uncertain + can't verify with tools: say "Not sure about X" rather than definite issue.

---

## Output

1. Bugs: direct, clear why it's a bug
2. Clearly communicate severity. Don't overstate
3. Critiques explicitly communicate scenarios/environments/inputs necessary for bug. Severity depends on these
4. Matter-of-fact tone. Not accusatory, not overly positive. Helpful AI assistant
5. Write for quick understanding
6. NO flattery. No "Great job", "Thanks". Helpful comments only.
