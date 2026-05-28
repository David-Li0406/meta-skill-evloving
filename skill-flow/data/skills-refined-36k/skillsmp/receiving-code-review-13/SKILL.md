---
name: receiving-code-review
description: This skill should be used when processing code review feedback, responding to reviewer comments, or when feedback seems unclear or technically questionable. Requires verification before implementing.
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, Skill, mcp__plugin_serena_serena, mcp__plugin_serena_serena_*
---

# Receiving Code Review

Process code review feedback with technical evaluation, not emotional performance.

## When Invoked

This skill is invoked after code-reviewer agent returns output. This skill processes the feedback.

## The Response Pattern

1. **Read** - Complete feedback without reacting
2. **Categorize** - Critical / Important / Minor
3. **Verify** - Check each issue against codebase
4. **Evaluate** - Technically sound for THIS codebase?
5. **Respond** - Acknowledge valid, push back if wrong
6. **Implement** - One fix at a time, test each

## Processing Feedback

### Categorize

From code-reviewer output, separate issues:

| Category  | Action                | Examples                                    |
| --------- | --------------------- | ------------------------------------------- |
| Critical  | Fix immediately       | Security, data loss, broken functionality   |
| Important | Fix before proceeding | Architecture, missing tests, error handling |
| Minor     | Note for later        | Style, optimization, documentation          |

### Verify Each Issue

For each Critical and Important issue:

```bash
# Check if the issue is real
# Read the file/line mentioned
# Determine if feedback is accurate
```

Questions to ask:

- Does this file/line exist?
- Is the described problem present?
- Would the suggested fix work?
- Does this break existing functionality?

### Evaluate

For each verified issue:

**If valid:**

- Note the fix needed
- Add to implementation queue

**If unclear:**

- STOP
- Do not guess
- Ask for clarification on ALL unclear items before implementing any

**If wrong:**

- Note why (technical reasoning)
- Do not implement
- Push back in summary

## Forbidden Responses

Never say:

- "You're absolutely right!"
- "Great point!"
- "Thanks for catching that!"

Instead: Restate the technical requirement, or fix silently.

## Implementing Fixes

Order of implementation:

1. **All unclear items clarified first** - Partial understanding = wrong implementation
2. **Critical issues** - Security, data loss, broken functionality
3. **Simple fixes** - Typos, imports, obvious errors
4. **Complex fixes** - Refactoring, architecture changes

For each fix:

```bash
# 1. Implement the fix

# 2. Run tests
npm test  # or project test command

# 3. If tests pass, commit
git add -A && git commit -m "fix: [description from review]"

# 4. Next fix
```

Do not batch fixes. One fix, one test run, one commit.

## Pushing Back

Push back when:

- Suggestion breaks existing functionality
- Reviewer lacks context visible in codebase
- Violates YAGNI (adding unused feature)
- Technically incorrect for this stack/framework

**How to push back:**

```text
Issue: "[reviewer's concern]"
Response: Not implementing. [Technical reasoning with code references]
```

Reference working tests, existing patterns, or documentation.

## Handling External Reviewers

Before implementing external feedback:

1. Check: Technically correct for THIS codebase?
2. Check: Breaks existing functionality?
3. Check: Reviewer understand full context?

External reviewers may not know:

- Project conventions
- Existing patterns
- Why something was done a certain way

Verify before implementing.

## Acknowledging Correct Feedback

```text
✅ "Fixed. [Brief description]"
✅ [Just fix it silently]
❌ "You're absolutely right!"
❌ "Thanks for [anything]"
```

Actions speak. The code shows the feedback was heard.

## Summary Output

After processing all feedback, report:

```text
Review processed:
- Critical: [N] found, [M] fixed
- Important: [N] found, [M] fixed
- Minor: [N] noted for later
- Pushed back: [N] (not valid for this codebase)

All fixes verified with tests.
```

## Integration

**Uses:**

- `dev-workflow:verification-before-completion` - Verify each fix before next

**Receives from:**

- `dev-workflow:code-reviewer` agent output
