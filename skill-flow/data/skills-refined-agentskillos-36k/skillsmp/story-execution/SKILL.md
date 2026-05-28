---
name: story-execution
description: "Execute a single user story from prd.json. Use during Ralf loop iterations to implement stories correctly."
---

# Story Execution Skill

Expert guidance for implementing a single user story in one Ralf iteration.

## When to Use

- During Ralf loop iterations
- When implementing a story from prd.json
- When you need to ensure proper execution flow

## Execution Flow

### 1. Pre-Implementation
- Read `.ralf/prd.json` to get story details
- Read `.ralf/progress.txt` for codebase patterns
- Check you're on the correct branch
- Identify the target story (first with `passes: false`)

### 2. Implementation
- Implement ONLY the acceptance criteria listed
- Follow existing code patterns
- Keep changes minimal and focused
- Don't add extras not in acceptance criteria

### 3. Verification
- Run typecheck (required for all stories)
- Run linter if configured
- Run tests if relevant
- For UI stories: verify visually if possible

### 4. Post-Implementation
- Commit with message: `feat: [US-XXX] - [Story Title]`
- Update `.ralf/prd.json`: set `passes: true`
- Append to `.ralf/progress.txt` with learnings
- Update AGENTS.md if reusable patterns found

## Quality Gates

A story is only complete when:

- [ ] All acceptance criteria met
- [ ] Typecheck passes
- [ ] No linting errors
- [ ] Changes committed
- [ ] `.ralf/prd.json` updated
- [ ] `.ralf/progress.txt` logged

## Common Mistakes to Avoid

1. **Scope Creep**: Implementing more than the acceptance criteria
2. **Skipping Verification**: Not running typecheck/tests
3. **Forgetting Progress**: Not updating `.ralf/progress.txt`
4. **Breaking Changes**: Changing code outside story scope
5. **Missing Commits**: Forgetting to commit before loop ends

## Progress Entry Format

```
## [Date] - [Story ID]
- What was implemented
- Files changed
- **Learnings:**
  - Patterns discovered
  - Gotchas encountered
---
```

## Completion Check

After completing a story:

1. Check if ALL stories have `passes: true`
2. If yes: output `<promise>COMPLETE</promise>`
3. If no: end response (next iteration continues)
