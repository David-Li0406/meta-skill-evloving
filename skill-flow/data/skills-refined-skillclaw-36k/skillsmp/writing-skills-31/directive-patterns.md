# Directive Writing Patterns

## Core Principle

Claude is smart. Only write what it doesn't already know.

## Framing

### Positive Framing (Preferred)
Tell Claude what TO do, not what to avoid.

| Instead of | Write |
|------------|-------|
| Don't create duplicate files | Update existing files in place |
| Don't use deprecated APIs | Use the v2 API endpoints |
| Avoid hardcoding values | Extract configuration to environment variables |
| Don't make assumptions | Ask clarifying questions when requirements are ambiguous |

### Motivation Over Commands

Explain WHY; Claude generalizes from understanding motivation.

**Weak:**
```
Always use TypeScript strict mode.
```

**Strong:**
```
Use TypeScript strict mode because it catches null reference errors
at compile time, which are the #1 source of production bugs in this codebase.
```

## Compliance Hierarchy

### 1. Context (Most Effective)
Supply context explaining why rules exist. Claude internalizes and applies broadly.

```markdown
## Database Migrations
Migrations must be reversible because we deploy with blue-green strategy.
A non-reversible migration blocks rollback during incidents.
```

### 2. Structural Enforcement
Make compliance the path of least resistance through workflows.

```markdown
## PR Checklist
Before marking ready for review:
1. [ ] All tests pass locally
2. [ ] No TypeScript errors (`npm run typecheck`)
3. [ ] Changes documented in CHANGELOG
4. [ ] Reviewer assigned

Do not proceed until all boxes are checked.
```

### 3. Imperatives (Use Sparingly)
Reserve strong language for true boundaries.

```markdown
NEVER commit secrets to version control.
NEVER run migrations on production without a backup.
```

**Warning:** Overuse of imperatives causes overtriggering in Claude 4.x. Save them for genuine safety boundaries.

## Structural Patterns

### Numbered Workflows
```markdown
## Feature Implementation Workflow
1. Create branch from main
2. Write failing test for the requirement
3. Implement minimum code to pass test
4. Refactor while tests stay green
5. Open PR with test coverage summary
```

### Verification Gates
```markdown
## Before Deployment
STOP. Verify each item before proceeding:
- [ ] Staging tests passed
- [ ] Performance benchmarks within threshold
- [ ] Security scan clean
- [ ] Rollback plan documented

If any item is unchecked, do not deploy.
```

### Decision Trees
```markdown
## Error Handling Decision
Is this a user-facing error?
├── Yes: Return friendly message, log details internally
└── No: Is this recoverable?
    ├── Yes: Retry with exponential backoff
    └── No: Fail fast, alert on-call
```

## Description Optimization

The description field controls skill discoverability.

### Structure
```
Use when [trigger]. [Purpose in one sentence].
```

### Keywords to Include
- Error messages the skill addresses
- Symptoms users might describe
- Technical terms for the domain
- Action verbs (creating, debugging, optimizing)

### Examples

**Good:**
```yaml
description: Use when writing database migrations. Covers reversibility requirements, testing strategies, and rollback procedures.
```

**Bad:**
```yaml
description: This skill helps with database stuff.
```

## Token Efficiency

### Word Limits
- Frequently-loaded skills: <200 words
- Total loaded directives: ~150 instruction limit before degradation
- Description field: <200 characters

### Progressive Disclosure
```markdown
## Quick Start
[50 words covering 80% of use cases]

See [detailed-reference.md](./detailed-reference.md) for edge cases.
```

### Cross-Referencing
Instead of duplicating content:
```markdown
For testing methodology, see the testing-skills skill.
```

## Format Considerations

### XML for Preservation
XML structures survive long prompts better than markdown or JSON.

```xml
<rule name="no-any-types">
  <trigger>TypeScript code review</trigger>
  <guidance>Replace `any` with specific types or `unknown`</guidance>
  <rationale>Type safety is the point of TypeScript</rationale>
</rule>
```

### Output Matching
Match prompt formatting to desired output formatting. If you want bulleted lists, write prompts with bulleted structure.

## Anti-Patterns

| Pattern | Problem | Fix |
|---------|---------|-----|
| Wall of imperatives | Cognitive overload, ignored | Prioritize, use context |
| Vague triggers | Never discovered | Specific "Use when..." |
| Duplicated content | Drift, bloat | Cross-reference |
| Hypothetical requirements | Complexity without value | Write for observed needs |
| Missing rationale | Brittle compliance | Explain why |
