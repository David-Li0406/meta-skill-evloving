# Best Practices for Creating Effective Rules

## Core Principles

### 1. Clarity Over Brevity

Rules should be immediately understandable. A slightly longer rule that's crystal clear is better than a short, ambiguous one.

**Example:**
- ❌ "No magic numbers"
- ✅ "Replace numeric literals with named constants. Exception: 0, 1, -1 for loops and basic math."

### 2. Positive Framing

Tell what TO DO, not just what NOT to do.

**Example:**
- ❌ "Don't use console.log in production"
- ✅ "Use the logger service for all logging. Remove or replace console.log with logger.debug before merging."

### 3. Scope Definition

Clearly define where and when the rule applies.

**Example:**
- ❌ "Always write tests"
- ✅ "Write unit tests for all functions in /app/services. UI components in /app/components require tests only for complex logic."

### 4. Escape Hatches

Provide exceptions when absolute rules would be counterproductive.

**Example:**
```
Use TypeScript strict mode for all new files.
Exception: Third-party type definitions that require 'any' are acceptable with a // @ts-expect-error comment explaining why.
```

---

## Rule Categories

### Project Rules vs Personal Rules

**Project Rules** (share with team):
- Coding standards
- Architecture decisions
- Security requirements
- Git workflows

**Personal Rules** (individual preferences):
- Response language
- Explanation style
- Tool preferences

---

## Rule Organization

### Grouping Rules

Group related rules together with clear headers:

```
## API Development
- All API routes must validate input using zod schemas
- Return consistent error response format: { error: string, code: number }
- Log all errors with request context

## Database
- Use transactions for multi-table operations
- Add created_at and updated_at to all tables
```

### Priority Rules

When rules might conflict, establish priority:

```
## Priority Order
1. Security rules (always take precedence)
2. Performance rules (when not conflicting with security)
3. Style rules (lowest priority)
```

---

## Common Mistakes to Avoid

### 1. Vague Language

❌ "Write clean code"
❌ "Use best practices"
❌ "Be careful with..."

### 2. Unrealistic Rules

❌ "100% test coverage for all code"
❌ "Never use any"
❌ "Document every line"

### 3. Outdated Rules

Review rules periodically. Remove or update rules that:
- Reference deprecated technologies
- No longer match current workflows
- Have been superseded by new practices

### 4. Conflicting Rules

Before adding a new rule, check it doesn't contradict existing rules:
- "Always use interfaces" vs "Prefer types over interfaces"
- "Keep functions short" vs "Avoid creating too many small functions"

---

## Rule Validation Checklist

Before finalizing a rule, verify:

- [ ] Is it clear and unambiguous?
- [ ] Does it apply to a specific context?
- [ ] Is it actionable?
- [ ] Does it include an example (if complex)?
- [ ] Are exceptions documented?
- [ ] Does it conflict with other rules?
- [ ] Is it enforceable/verifiable?

---

## Rule Maintenance

### Review Cycle

- **Weekly**: Quick scan for relevance
- **Monthly**: Detailed review and updates
- **Quarterly**: Major revision and cleanup

### Versioning

Consider adding version/date to rule sets:

```
## Coding Standards v2.1 (Updated: 2026-01-17)
```

### Feedback Loop

Document which rules cause confusion or are frequently violated. These need clarification or may be unrealistic.
