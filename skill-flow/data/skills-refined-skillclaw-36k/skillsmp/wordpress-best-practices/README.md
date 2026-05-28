# WordPress Best Practices

WordPress development coding standards for AI-assisted development.

## Structure

```
rules/
├── _sections.md      # Section definitions
├── _template.md      # Template for new rules
├── security-*.md     # Security hardening rules (CRITICAL)
├── database-*.md     # Database optimization rules (HIGH)
├── perf-*.md         # Performance rules (HIGH)
├── plugin-*.md       # Plugin development rules (MEDIUM-HIGH)
├── theme-*.md        # Theme development rules (MEDIUM)
├── api-*.md          # REST API rules (MEDIUM)
├── multisite-*.md    # Multisite rules (LOW-MEDIUM)
└── blocks-*.md       # Gutenberg/Blocks rules (LOW-MEDIUM)
```

## Adding New Rules

1. Copy `rules/_template.md` to `rules/{section}-{name}.md`
2. Fill in YAML frontmatter (title, impact, impactDescription, tags)
3. Write rule explanation with Incorrect/Correct examples
4. Run `pnpm validate` to check format
5. Run `pnpm build` to regenerate AGENTS.md

## Impact Levels

| Level | Description |
|-------|-------------|
| CRITICAL | Security vulnerabilities or major performance issues |
| HIGH | Significant improvements |
| MEDIUM-HIGH | Moderate-high gains |
| MEDIUM | Moderate improvements |
| LOW-MEDIUM | Low-medium gains |
| LOW | Incremental improvements |
