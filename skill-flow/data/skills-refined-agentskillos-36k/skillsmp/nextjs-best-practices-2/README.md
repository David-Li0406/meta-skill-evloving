# Next.js Best Practices

Next.js App Router coding standards for AI-assisted development.

## Structure

```
rules/
├── _sections.md     # Section definitions
├── _template.md     # Template for new rules
├── app-*.md         # App Router rules (CRITICAL)
├── fetch-*.md       # Data fetching rules (CRITICAL)
├── actions-*.md     # Server Actions rules (HIGH)
├── render-*.md      # Rendering rules (HIGH)
├── middleware-*.md  # Middleware rules (MEDIUM-HIGH)
├── assets-*.md      # Asset optimization rules (MEDIUM)
├── routes-*.md      # Route handler rules (MEDIUM)
└── deploy-*.md      # Deployment rules (LOW-MEDIUM)
```

## Adding New Rules

1. Copy `rules/_template.md` to `rules/{section}-{name}.md`
2. Fill in YAML frontmatter (title, impact, impactDescription, tags)
3. Write rule explanation with Incorrect/Correct examples
4. Run `pnpm validate` to check format
5. Run `pnpm build` to regenerate AGENTS.md

## Rule Format

```markdown
---
title: Rule Title
impact: CRITICAL|HIGH|MEDIUM-HIGH|MEDIUM|LOW-MEDIUM|LOW
impactDescription: Brief impact description
tags: tag1, tag2, tag3
---

## Rule Title

Brief explanation.

**Incorrect (what's wrong):**

\`\`\`typescript
// Bad code
\`\`\`

**Correct (what's right):**

\`\`\`typescript
// Good code
\`\`\`
```

## Impact Levels

| Level | Description |
|-------|-------------|
| CRITICAL | Major performance/UX impact, always apply |
| HIGH | Significant improvements |
| MEDIUM-HIGH | Moderate-high gains |
| MEDIUM | Moderate improvements |
| LOW-MEDIUM | Low-medium gains |
| LOW | Incremental improvements |
