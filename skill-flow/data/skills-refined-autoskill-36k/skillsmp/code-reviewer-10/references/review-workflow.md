# Code Review Workflow

## PR Review Process

### 1. Context Gathering (2-5 min)

```markdown
Before diving into code:
□ Read PR description and linked issue/ticket
□ Understand the goal - what problem is being solved?
□ Check the scope - is this a focused change or broad refactor?
□ Note any deployment considerations mentioned
```

### 2. High-Level Scan (5-10 min)

```markdown
Quick overview of changes:
□ Files changed - which layers/modules affected?
□ Lines added/removed - is the scope reasonable?
□ New dependencies - are they justified?
□ Test coverage - are there new tests?
□ Config changes - any security implications?
```

### 3. Deep Review (10-30 min)

Review order for maximum efficiency:

1. **Tests first** - understand expected behavior
2. **Interface changes** - API contracts, types, schemas
3. **Core logic** - business rules, algorithms
4. **Integration points** - DB queries, API calls
5. **Error handling** - edge cases, failures
6. **Performance** - N+1, caching, complexity

### 4. Specialist Delegation

Trigger specialist skill review when:

| Detected Pattern | Action |
|-----------------|--------|
| Auth/JWT changes | Invoke `security-expert` |
| Keycloak/ABAC code | Invoke `keycloak-skill` |
| Java test file changes | Invoke `java-test-engineer` |
| TS/React test changes | Invoke `ts-test-engineer` |
| 5+ new dependencies | Invoke `architecture-tech-lead` |
| React components | Invoke `frontend-design-skill` |

### 5. Feedback Synthesis

Consolidate into actionable comments:
- Group by file when possible
- Prioritize by severity
- Suggest specific fixes
- Link to docs/examples

---

## Comment Templates

### Blocking Issue

```markdown
🔴 **Blocking**: [Brief issue]

**Problem**: [Detailed explanation]

**Risk**: [What could go wrong]

**Fix**:
```suggestion
// Suggested code
```

**Reference**: [Link to docs/guidelines]
```

### Suggestion

```markdown
🟡 **Suggestion**: [Brief idea]

**Why**: [Benefit explanation]

**Example**:
```suggestion
// Better approach
```
```

### Question

```markdown
❓ **Question**: [Specific question]

Context: [Why you're asking]

Options I see:
1. ...
2. ...
```

### Praise

```markdown
💚 **Nice**: [What's good]

This is a great example of [pattern] because [reason]. Worth considering as a pattern for future similar changes.
```

---

## Review Priorities

### Always Check

1. **Security** - auth, input validation, secrets
2. **Correctness** - edge cases, null handling
3. **Breaking changes** - API contracts, DB schema
4. **Data integrity** - transactions, consistency

### Check When Applicable

5. **Performance** - queries, algorithms, caching
6. **Testability** - mocking, pure functions
7. **Maintainability** - naming, complexity
8. **Documentation** - API docs, complex logic

### Skip Unless Obvious

9. **Style** - let linters handle it
10. **Minor optimizations** - premature optimization

---

## Handling Common Situations

### Large PRs (500+ lines)

```markdown
Options:
1. Ask author to split into smaller PRs
2. Focus on high-risk areas only
3. Review in multiple sessions
4. Pair review with author

Comment template:
"This PR has significant scope. Could we split it into:
1. [Refactoring part]
2. [New feature part]
3. [Test additions]
This will make review more thorough and rollback easier."
```

### Disagreements

```markdown
Steps:
1. State your concern clearly with reasoning
2. Acknowledge author's perspective
3. Propose alternatives
4. Escalate to team lead if unresolved

Tone:
❌ "This is wrong"
✅ "I'm concerned about X because Y. Have you considered Z?"
```

### Time-Sensitive PRs

```markdown
Quick review checklist:
□ Security issues? (blocking)
□ Data loss risk? (blocking)
□ Breaking changes? (blocking)
□ Tests pass?
□ Obvious bugs?

Note: "Quick review due to timeline. Suggest follow-up for [deferred concerns]."
```

---

## Post-Review Actions

### After Approval

```markdown
□ Verify CI passes
□ Check for merge conflicts
□ Confirm deployment plan if applicable
□ Update related documentation if needed
```

### After Merge

```markdown
□ Monitor for issues (especially for risky changes)
□ Close related issues
□ Update team on significant changes
```

---

## Review Metrics

Track for self-improvement:

| Metric | Target |
|--------|--------|
| Time to first review | < 4 hours |
| Review thoroughness | < 1 bug escaped per 10 PRs |
| Comment clarity | Author understands on first read |
| False positives | < 10% of blocking comments |

---

## Anti-Patterns in Reviewing

### Don't Do This

```markdown
❌ Approve without reading - "LGTM"
❌ Block on style preferences
❌ Leave vague comments - "this could be better"
❌ Demand perfection on time-sensitive fixes
❌ Review only what you're comfortable with
❌ Skip test review
❌ Ignore your instincts - "something feels off"
```

### Do This Instead

```markdown
✅ Take time to understand the change
✅ Focus on correctness and security first
✅ Be specific and actionable
✅ Balance thoroughness with pragmatism
✅ Ask for help on unfamiliar code
✅ Verify tests cover the changes
✅ Investigate when something seems wrong
```
