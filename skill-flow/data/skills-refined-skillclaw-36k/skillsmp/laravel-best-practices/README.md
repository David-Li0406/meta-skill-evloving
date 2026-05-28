# Laravel Best Practices

Laravel coding standards for AI-assisted development.

## Structure

```
rules/
├── _sections.md      # Section definitions
├── _template.md      # Template for new rules
├── security-*.md     # Security rules (CRITICAL)
├── eloquent-*.md     # Eloquent optimization rules (CRITICAL)
├── perf-*.md         # Performance rules (HIGH)
├── arch-*.md         # Architecture rules (HIGH)
├── api-*.md          # API development rules (MEDIUM-HIGH)
├── test-*.md         # Testing rules (MEDIUM)
├── queue-*.md        # Queue & jobs rules (MEDIUM)
└── livewire-*.md     # Livewire rules (LOW-MEDIUM)
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

\`\`\`php
// Bad code
\`\`\`

**Correct (what's right):**

\`\`\`php
// Good code
\`\`\`
```

## Impact Levels

| Level | Description |
|-------|-------------|
| CRITICAL | Security vulnerabilities or major performance issues |
| HIGH | Significant improvements |
| MEDIUM-HIGH | Moderate-high gains |
| MEDIUM | Moderate improvements |
| LOW-MEDIUM | Low-medium gains |
| LOW | Incremental improvements |
