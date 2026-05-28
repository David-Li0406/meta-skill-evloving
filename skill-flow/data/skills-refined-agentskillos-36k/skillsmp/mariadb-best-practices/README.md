# MariaDB Best Practices

MariaDB database coding standards for AI-assisted development.

## Structure

```
rules/
├── _sections.md      # Section definitions
├── _template.md      # Template for new rules
├── query-*.md        # Query optimization rules (CRITICAL)
├── security-*.md     # Security rules (CRITICAL)
├── schema-*.md       # Schema design rules (HIGH)
├── engine-*.md       # Storage engine rules (HIGH)
├── galera-*.md       # Galera cluster rules (MEDIUM-HIGH)
├── perf-*.md         # Performance tuning rules (MEDIUM)
├── json-*.md         # JSON feature rules (MEDIUM)
└── compat-*.md       # Compatibility rules (LOW-MEDIUM)
```

## Adding New Rules

1. Copy `rules/_template.md` to `rules/{section}-{name}.md`
2. Fill in YAML frontmatter (title, impact, impactDescription, tags)
3. Write rule explanation with Incorrect/Correct examples
4. Run `pnpm validate` to check format
5. Run `pnpm build` to regenerate AGENTS.md

## MariaDB vs MySQL

MariaDB is a fork of MySQL with additional features:
- Galera Cluster for multi-master replication
- System versioned tables for temporal data
- ColumnStore for analytics workloads
- Additional storage engines (Aria, Spider, etc.)

Many MySQL rules apply to MariaDB. This skill covers MariaDB-specific features.
