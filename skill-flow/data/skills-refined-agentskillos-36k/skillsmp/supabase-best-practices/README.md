# Supabase Best Practices

Supabase development coding standards for AI-assisted development.

## Structure

```
rules/
├── _sections.md      # Section definitions
├── _template.md      # Template for new rules
├── rls-*.md          # Row Level Security rules (CRITICAL)
├── schema-*.md       # Database design rules (CRITICAL)
├── auth-*.md         # Authentication rules (HIGH)
├── realtime-*.md     # Real-time rules (HIGH)
├── edge-*.md         # Edge Functions rules (MEDIUM-HIGH)
├── storage-*.md      # Storage rules (MEDIUM)
├── perf-*.md         # Performance rules (MEDIUM)
└── client-*.md       # Client library rules (LOW-MEDIUM)
```

## Adding New Rules

1. Copy `rules/_template.md` to `rules/{section}-{name}.md`
2. Fill in YAML frontmatter (title, impact, impactDescription, tags)
3. Write rule explanation with Incorrect/Correct examples
4. Run `pnpm validate` to check format
5. Run `pnpm build` to regenerate AGENTS.md

## Key Concepts

- **Row Level Security (RLS)**: PostgreSQL policies that control data access
- **auth.uid()**: Function returning the current user's ID
- **Edge Functions**: Deno-based serverless functions
- **Realtime**: WebSocket-based subscriptions to database changes
