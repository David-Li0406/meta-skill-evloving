---
name: Project Standards
description: |
  Use this skill when the user asks about user story format, documentation standards, acceptance criteria, or code review practices. Triggers on: "User story format?", "How to write documentation?", "Acceptance criteria?", "Documentation standards", "Code review checklist", "How to write user stories".
version: 1.0.0
---

# Project Standards

Guidance for user stories, documentation conventions, and quality standards.

## User Story Standards

### User Story Format

Use this standard format:

```
As a [user type/persona],
I want [goal/desire],
So that [benefit/value].
```

**Required Elements:**

- **User Type**: Who is this for? (admin, end user, developer, etc.)
- **Goal**: What does the user want to do? (concrete action)
- **Benefit**: Why does this matter? (value to user)

### User Story ID Conventions

**Use UPPERCASE (`US-XXX`) for:**

- Display contexts (tables, titles, headers)
- Human communication (discussions, commit messages)
- References in prose ("As described in US-003...")

**Use lowercase (`us-xxx`) for:**

- File paths and filenames
- URL slugs and API endpoints
- Template patterns

**Examples:**

```markdown
<!-- In tracking table (uppercase) -->

| US-003 | View Conversations | ✅ Complete |

<!-- In file paths (lowercase) -->

.claude/project/features/us-003-view-conversations.md
.claude/project/plans/us-003-plan.md
```

### Acceptance Criteria

Write acceptance criteria in checklist format:

```markdown
Acceptance Criteria:

- [ ] Users can log in with email and password
- [ ] Invalid credentials show error message
- [ ] Successful login redirects to dashboard
- [ ] Session persists for 24 hours
- [ ] Logout clears session completely
```

**Best Practices:**

- Make each criterion independently testable
- Use checkbox format for tracking
- Include edge cases (errors, empty states)
- Be specific about expected behavior

### User Story Size Guidelines

**Small (1-3 story points):**

- Single component or function
- Simple CRUD operation
- Minor UI change

**Medium (5-8 story points):**

- Multiple components
- API + UI integration
- Moderate complexity

**Large (13+ story points):**

- Consider breaking down
- Epic-level feature
- Multiple integration points

### User Story Quality Checklist

Before starting implementation:

- [ ] User type is clearly identified
- [ ] Goal is specific and actionable
- [ ] Benefit explains the value
- [ ] Acceptance criteria are testable
- [ ] Edge cases are identified
- [ ] Story is appropriately sized

---

## Documentation Standards

### Markdown Conventions

**Structure:**

- Use hierarchical headings (# > ## > ###)
- Keep sections focused (single topic per section)
- Add table of contents for files over 200 lines
- Use horizontal rules to separate major sections

**Code Blocks:**

- Always specify language for syntax highlighting
- Use comments to explain complex code
- Show both correct and incorrect examples when relevant

```typescript
// ✅ CORRECT - Clear function naming
function calculateTotalPrice(items: Item[]): number {
  return items.reduce((sum, item) => sum + item.price, 0);
}

// ❌ WRONG - Unclear naming
function calc(i: any[]): number {
  return i.reduce((s, x) => s + x.p, 0);
}
```

**Tables:**

- Use for structured data
- Align columns consistently
- Include headers

| Column 1 | Column 2 | Column 3 |
| -------- | -------- | -------- |
| Data     | Data     | Data     |

**Lists:**

- Use bullet points for unordered items
- Use numbered lists for sequential steps
- Use checklists for actionable items

### File Naming

**General Rules:**

- Use lowercase for all file names
- Use kebab-case for multi-word names: `user-profile.ts`
- Be descriptive but concise

**Specific Patterns:**

- Components: `component-name.tsx`
- Utilities: `utility-name.ts`
- Tests: `component-name.test.ts`
- Stories: `component-name.stories.tsx`

### Code Comments

**When to Comment:**

- Complex business logic
- Non-obvious decisions
- Workarounds with context
- Public API documentation

**When NOT to Comment:**

- Obvious operations
- Self-explanatory code
- Redundant descriptions

```typescript
// ❌ BAD - Redundant comment
// Add 1 to counter
counter += 1;

// ✅ GOOD - Explains WHY
// Offset by 1 because API uses 1-based pagination
const pageIndex = page - 1;
```

---

## Code Review Standards

### Code Review Checklist

**Functionality:**

- [ ] Code implements requirements correctly
- [ ] Edge cases are handled
- [ ] Error handling is appropriate
- [ ] No regressions introduced

**Code Quality:**

- [ ] Code follows established patterns
- [ ] No unnecessary complexity
- [ ] DRY principle followed
- [ ] Clear naming conventions

**Testing:**

- [ ] Tests cover happy path
- [ ] Tests cover edge cases
- [ ] Tests are readable and maintainable
- [ ] Coverage meets requirements

**Security:**

- [ ] No hardcoded secrets
- [ ] Input validation present
- [ ] Authorization checks in place
- [ ] No obvious vulnerabilities

**Performance:**

- [ ] No N+1 queries
- [ ] Appropriate caching
- [ ] No memory leaks
- [ ] Efficient algorithms

### Review Best Practices

**As a Reviewer:**

- Be constructive, not critical
- Explain the "why" behind suggestions
- Distinguish between blockers and nits
- Acknowledge good work

**As an Author:**

- Keep changes small and focused
- Provide context in PR description
- Respond to all feedback
- Don't take feedback personally

---

## Quality Gates

### Before Marking Complete

Every feature must pass:

1. **Linting:** No errors or warnings
2. **Type Checking:** No type errors
3. **Tests:** All tests passing
4. **Coverage:** Meets minimum threshold
5. **Build:** Production build succeeds
6. **Manual Testing:** Verified in browser/app

### Definition of Done

A feature is "done" when:

- [ ] All acceptance criteria met
- [ ] All quality gates pass
- [ ] Code reviewed and approved
- [ ] Documentation updated
- [ ] Deployed to staging
- [ ] Tested in staging environment
