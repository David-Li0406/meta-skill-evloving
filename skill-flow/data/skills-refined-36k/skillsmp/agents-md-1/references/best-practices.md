# Best Practices for Agent Documentation

## Length Guidelines

| Metric | Limit | Reason |
|--------|-------|--------|
| Total lines | < 300 (ideal < 100) | LLMs can follow ~150-200 instructions consistently |
| Instructions | < 100-150 | System prompt already uses ~50 instructions |

## Writing Principles

### Be Specific, Not Generic

❌ Bad:
```markdown
- Format code properly
- Write good tests
```

✅ Good:
```markdown
- Use 2-space indentation
- Prefer integration tests over unit tests for API endpoints
```

### Use Pointers, Not Copies

❌ Bad:
```markdown
Here's how the User model looks:
class User {
  id: string
  name: string
  ...
}
```

✅ Good:
```markdown
See `src/models/User.ts:10-25` for the User model definition.
```

Code snippets become outdated quickly. Reference file:line instead.

### Let Linters Handle Style

Do NOT include in agent docs:
- Indentation rules
- Semicolon preferences
- Quote style
- Import ordering

These belong in `.eslintrc`, `.prettierrc`, `biome.json`, etc.

## Progressive Disclosure

Keep the main document lean. Link to detailed docs:

```markdown
## Additional Resources
- `docs/DATABASE.md`: Database schema and relationships
- `docs/API.md`: API endpoints and authentication
```

### When to Split

Split content into separate files when:
- A section exceeds 50 lines
- Content is only relevant to specific tasks
- Information changes frequently

## Anti-Patterns

### Avoid `/init` Over-Reliance

`/init` generates a starting point, not a finished product. Always:
1. Review generated content
2. Remove generic/obvious information
3. Add project-specific nuances

### Avoid Duplication

If the same instruction exists in multiple places (CLAUDE.md, README, etc.), keep it in ONE place and reference it.

### Avoid Vague Instructions

❌ "Follow best practices"
❌ "Write clean code"
❌ "Be careful with..."

✅ Specific, actionable instructions

## Structure Tips

### Use Clear Headings

```markdown
## Development Commands     ← Clear category
- `npm test` - Run tests   ← Command + description
```

### Group Related Items

```markdown
## Development Commands

### Building
- `npm run build` - Production build
- `npm run build:dev` - Development build

### Testing
- `npm test` - Run all tests
- `npm test:watch` - Watch mode
```

## Maintenance

Review and update agent docs when:
- Adding new features or packages
- Changing build/test commands
- Modifying project structure
- Onboarding reveals missing information
