# Improvement Patterns

Common fixes for common skill validation issues.

---

## Structure Issues

### Problem: SKILL.md Too Long (>500 lines)

**Fix**: Extract to references

```
Before:
SKILL.md (800 lines with everything)

After:
SKILL.md (200 lines - overview + quick ref)
references/
├── detailed-patterns.md (300 lines)
├── advanced-usage.md (200 lines)
└── troubleshooting.md (100 lines)
```

**Add reference table**:
```markdown
## Reference Files

| File | When to Read |
|------|--------------|
| `references/detailed-patterns.md` | Complex implementations |
| `references/advanced-usage.md` | Non-standard scenarios |
```

### Problem: README.md Exists

**Fix**: Delete it. SKILL.md IS the readme.

### Problem: No Progressive Disclosure

**Fix**: Create references/ directory with topical files:
1. Identify independent topics in SKILL.md
2. Extract each to `references/[topic].md`
3. Add "when to read" guidance in SKILL.md

---

## Content Issues

### Problem: Verbose Content

**Before**:
```markdown
In this section, we will walk through the process of creating a new widget.
First, you will want to understand what data your widget needs to display.
This is important because the data shape determines how you structure your component.
```

**After**:
```markdown
## Creating a Widget

1. Define data shape (what `toolOutput` contains)
2. Choose display mode (inline/fullscreen/pip)
3. Implement with theme support
```

### Problem: "You should" Instead of Imperatives

**Before**:
```markdown
- You should validate all inputs
- It would be good to handle errors
- Try to follow the patterns
```

**After**:
```markdown
- Validate all inputs with Zod
- Handle errors with try/catch
- Follow these patterns:
```

### Problem: No Scope Boundaries

**Fix**: Add explicit sections:

```markdown
## What This Skill Does
- Creates X
- Validates Y
- Generates Z

## What This Skill Does NOT Do
- Deploy to production
- Optimize performance
- Handle authentication
```

---

## User Interaction Issues

### Problem: No Clarification Questions

**Fix**: Add structured clarification section:

```markdown
## Required Clarifications

Before building, ask:

1. **Data shape**: "What will `toolOutput` contain?"
   ```json
   Example: { items: [...], total: 10 }
   ```

2. **Action type**: "Display only or interactive?"
   - Display → No callTool needed
   - Interactive → Need tool name and params

3. **Display mode**: "Inline, fullscreen, or pip?"

## Optional Clarifications

4. **Styling**: "Any design preferences?" (ask if complex UI)
```

### Problem: All Questions Treated Equally

**Fix**: Separate required from optional:

```markdown
## Required (Must Ask)
1. Core question A
2. Core question B

## Optional (Ask if Relevant)
3. Nice-to-know question
4. Edge case question
```

### Problem: No Context Awareness

**Fix**: Add context-checking guidance:

```markdown
## Before Asking

Check existing context:
- Review conversation history for prior answers
- Infer from file names when possible
- Check toolOutput structure if available

Only ask what cannot be determined.
```

---

## Documentation Issues

### Problem: No Official Source Links

**Fix**: Add documentation table:

```markdown
## Official Documentation

| Resource | URL | Use For |
|----------|-----|---------|
| Getting Started | https://... | Basic setup |
| API Reference | https://... | Method details |
| Best Practices | https://... | Pattern guidance |

For patterns not covered here, fetch from official docs.
```

### Problem: No Fetch Guidance

**Fix**: Add on-the-go learning section:

```markdown
## Unlisted Scenarios

For patterns not documented here:

1. Fetch from official docs: [URL]
2. Apply same validation criteria
3. Follow established patterns in this skill

Examples of when to fetch:
- Complex authentication flows
- Third-party integrations
- Platform-specific features
```

### Problem: No Examples

**Fix**: Add good/bad examples:

```markdown
### Good Example
```typescript
// Correct pattern with explanation
const data = window.openai?.toolOutput ?? defaultValue;
```

### Bad Example (Don't Do This)
```typescript
// Why this is wrong
const data = window.openai.toolOutput; // Crashes if undefined
```
```

---

## Domain Standards Issues

### Problem: Best Practices Mentioned But Not Enforced

**Before**:
```markdown
Follow accessibility best practices.
```

**After**:
```markdown
## Accessibility Requirements

### Must Follow
- [ ] WCAG AA contrast (4.5:1 for text)
- [ ] Keyboard navigation for all interactions
- [ ] Focus indicators visible
- [ ] Screen reader labels for icons

### Must Avoid
- Color as only indicator
- Mouse-only interactions
- Auto-playing media without controls
```

### Problem: No Output Checklist

**Fix**: Add quality gate:

```markdown
## Output Checklist

Before delivering, verify ALL items:

### Functional
- [ ] Core feature works
- [ ] Error states handled
- [ ] Loading states present

### Quality
- [ ] Follows naming conventions
- [ ] No hardcoded values
- [ ] Comments where non-obvious

### Standards
- [ ] Passes domain requirements (above)
- [ ] Tested against criteria
```

---

## Technical Issues

### Problem: No Error Handling Guidance

**Fix**: Add error handling section:

```markdown
## Error Handling

| Scenario | Action |
|----------|--------|
| Invalid input | Return validation error with specifics |
| Network failure | Retry 3x with backoff, then fallback |
| Unknown error | Log context, return safe default |

### Error Response Format
```typescript
return {
  isError: true,
  content: [{ type: 'text', text: 'User-friendly message' }],
  _meta: { errorCode: 'VALIDATION_FAILED', details: {...} }
};
```
```

### Problem: No Security Guidance

**Fix**: Add security section (when relevant):

```markdown
## Security Considerations

- **Never hardcode**: Secrets, API keys, tokens
- **Always validate**: User input, file paths, URLs
- **Escape output**: Prevent XSS in generated HTML
- **Use parameterized**: Queries to prevent injection
```

### Problem: Dependencies Not Listed

**Fix**: Add dependencies section:

```markdown
## Dependencies

### Required
- Node.js 18+
- TypeScript 5.0+

### Optional
- Redis (for caching)

### External APIs
- OpenAI Apps SDK (via window.openai)
- No rate limits apply to widget
```

---

## Maintainability Issues

### Problem: Monolithic SKILL.md

**Fix**: Modularize into references:

1. Identify 3-5 independent topics
2. Create `references/[topic].md` for each
3. Keep SKILL.md as entry point with "when to read" table

### Problem: No Update Guidance

**Fix**: Add versioning section:

```markdown
## Keeping Current

- Official docs: [URL]
- Changelog: [URL]
- Last verified: 2024-12

When official docs update:
1. Check for breaking changes
2. Update affected references
3. Test against validation criteria
```

### Problem: Hardcoded Values

**Before**:
```markdown
Set timeout to 5000ms.
Use port 3000.
```

**After**:
```markdown
Set timeout (default: 5000ms, adjust for your use case).
Use configured port (default: 3000).
```

---

## Quick Improvement Checklist

When improving a skill, address in this order:

1. **Critical** (blocks usage):
   - [ ] SKILL.md exists and <500 lines
   - [ ] Frontmatter has name + description
   - [ ] Core workflow documented

2. **High Priority** (major quality):
   - [ ] Clarification questions (for builder skills)
   - [ ] Official documentation links
   - [ ] Output specification

3. **Medium Priority** (polish):
   - [ ] Progressive disclosure to references
   - [ ] Error handling guidance
   - [ ] Good/bad examples

4. **Low Priority** (excellence):
   - [ ] Update path documented
   - [ ] All edge cases covered
   - [ ] Templates in assets/
