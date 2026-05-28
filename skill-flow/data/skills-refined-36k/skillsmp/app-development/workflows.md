# Workflows

Development workflows and step-by-step guides for common tasks.

## When to Use

Read these guides when you need:
- Step-by-step instructions for a specific task
- Code templates for common patterns
- Debugging help

## Available Workflows

### Daily Workflow
@.claude/skills/app-development/workflows/daily-workflow.md
- Git workflow (branch, commit, push)
- Commit message conventions
- Pre-commit checklist

### Implementation Guide
@.claude/skills/app-development/workflows/implementation-guide.md
- 6-phase feature implementation checklist
- Schema templates (Zod + Mongoose)
- Server action templates
- React Query hook templates

### Common Tasks
@.claude/skills/app-development/workflows/common-tasks.md
- Database operations (mongosh)
- Schema migrations
- Breaking changes guide
- Adding new pages
- Adding server actions

### Hook Patterns
@.claude/skills/app-development/workflows/hook-patterns.md
- Data fetching hooks (React Query)
- Form validation hooks
- LocalStorage hooks
- Utility hooks (toggle, debounce)

### Dev Utilities
@.claude/skills/app-development/workflows/dev-utilities.md
- Essential commands (npm, git, mongosh)
- Debugging tools and techniques
- Common debug scenarios
- Performance tips
- Code quality checklist

## Quick Reference

| Task | Read This |
|------|-----------|
| Start new feature | Implementation Guide |
| Fix a bug | Common Tasks |
| Create custom hook | Hook Patterns |
| Debug issue | Dev Utilities |
| Daily git workflow | Daily Workflow |
| Database migration | Common Tasks |

## Best Practices

1. **Type Safety** - Use proper TypeScript types, avoid `any`
2. **Validation** - Use Zod for all external data
3. **Server First** - Prefer server components and actions
4. **React Query** - Use for server state management
5. **Component Hierarchy** - Follow core → composed → domain → features
