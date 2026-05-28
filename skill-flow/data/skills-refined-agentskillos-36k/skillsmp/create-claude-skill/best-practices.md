# Best Practices for Skill Development

This guide covers development, evaluation, and iteration practices for creating effective skills.

## Development Process

### 1. Start with Evaluation

**Don't guess what Claude needs.** Identify gaps through observation:

1. Run Claude on representative tasks without the skill
2. Note where it struggles, makes mistakes, or asks for guidance
3. Document specific failure patterns
4. Build skills to address these shortcomings incrementally

**Example evaluation questions:**
- What procedural knowledge is Claude missing?
- Where does Claude make inconsistent decisions?
- What context would prevent common mistakes?
- What patterns does Claude fail to recognize?

### 2. Design for Progressive Disclosure

Structure content so Claude loads only what's needed:

```
✅ Good: SKILL.md references topic.md only when that topic arises
❌ Bad: SKILL.md includes all content inline
```

**Benefits:**
- Reduced token usage
- Faster skill activation
- Cleaner context window
- Better scaling

### 3. Think from Claude's Perspective

**Name and Description Matter Most**

Claude uses these to decide whether to trigger a skill:

```yaml
# ✅ Good: Specific, actionable triggers
description: Create database migrations for schema changes. Use when user says "add migration", "change schema", or "update database structure".

# ❌ Bad: Vague, unclear triggers
description: Helps with database stuff.
```

**Instructions Should Be Unambiguous**

Write instructions that leave no room for interpretation:

```markdown
# ✅ Good: Clear, specific
Always create a backup before modifying production data.
Use the pattern: `{table}_backup_{timestamp}`

# ❌ Bad: Vague, open to interpretation
Make sure to be careful with production data.
```

### 4. Iterate with Claude

**Capture Successful Approaches**

When Claude solves a problem well:
1. Ask Claude what approach it used
2. Have Claude document the steps
3. Add to the skill for future use

**Learn from Failures**

When Claude goes off track:
1. Ask Claude to self-reflect on what went wrong
2. Identify what context was missing
3. Add guardrails or clarifications to the skill

**Example iteration prompt:**
```
"That worked well. Can you capture the approach you used as a reusable
pattern I can add to the skill?"
```

## Evaluation Techniques

### Task-Based Testing

Create a test suite of tasks:

```markdown
## Test Cases

### Test 1: Basic Creation
Input: "Create a new user model"
Expected: [Specific output or behavior]

### Test 2: Edge Case
Input: "Create a model with circular references"
Expected: [Specific handling]
```

### Regression Testing

After skill updates:
1. Re-run previous test cases
2. Verify existing functionality still works
3. Check that fixes don't introduce new issues

### A/B Comparison

Compare skill versions:
1. Run same task with old and new skill
2. Evaluate output quality
3. Measure token usage
4. Track success rates

## Common Pitfalls

### 1. Over-Engineering

```
❌ Bad: 500-line SKILL.md with every possible scenario
✅ Good: 100-line SKILL.md with references to detailed docs
```

### 2. Unclear Triggers

```
❌ Bad: Skills that activate when they shouldn't
✅ Good: Specific, unambiguous trigger conditions
```

### 3. Missing Context

```
❌ Bad: Assuming Claude knows project conventions
✅ Good: Explicitly stating all requirements and patterns
```

### 4. Rigid Instructions

```
❌ Bad: "Always do X" (when exceptions exist)
✅ Good: "Do X unless Y, in which case do Z"
```

### 5. No Examples

```
❌ Bad: Abstract instructions only
✅ Good: Concrete examples showing input → output
```

## Quality Checklist

Before deploying a skill:

### Structure
- [ ] YAML frontmatter with name and description
- [ ] Clear purpose statement
- [ ] Logical organization of content
- [ ] Appropriate use of supporting files

### Content
- [ ] Specific, actionable instructions
- [ ] Examples for key scenarios
- [ ] Edge cases addressed
- [ ] Error handling guidance

### Testing
- [ ] Tested on representative tasks
- [ ] Edge cases verified
- [ ] No regression from previous version
- [ ] Token usage is reasonable

### Documentation
- [ ] README or SKILL.md explains purpose
- [ ] File references are accurate
- [ ] Templates are complete
- [ ] Examples are up to date

## Maintenance

### Regular Review

- Review skill effectiveness monthly
- Update based on observed failures
- Remove outdated patterns
- Add new best practices

### Version Control

- Track skill changes in git
- Document significant updates
- Tag stable versions

### Deprecation

When retiring a skill:
1. Mark as deprecated in description
2. Point to replacement if available
3. Remove from settings after transition period

## Metrics to Track

| Metric | What It Measures |
|--------|-----------------|
| Activation rate | How often skill triggers |
| Success rate | Tasks completed correctly |
| Token usage | Context efficiency |
| User satisfaction | Feedback quality |
| Time to completion | Workflow efficiency |
