# MySQL Best Practices

MySQL database coding standards for AI-assisted development.

## Structure

```
rules/
├── _sections.md      # Section definitions
├── _template.md      # Template for new rules
├── query-*.md        # Query optimization rules (CRITICAL)
├── security-*.md     # Security rules (CRITICAL)
├── schema-*.md       # Schema design rules (HIGH)
├── index-*.md        # Indexing rules (HIGH)
├── txn-*.md          # Transaction rules (MEDIUM-HIGH)
├── conn-*.md         # Connection rules (MEDIUM)
├── backup-*.md       # Backup rules (MEDIUM)
└── repl-*.md         # Replication rules (LOW-MEDIUM)
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
