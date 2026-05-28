---
name: postgres-best-practices
description: Postgres performance optimization and best practices from Supabase, adapted to EquipQR's Supabase (Postgres + RLS) workflow. Use when editing SQL, migrations, indexes, or RLS policies.
license: MIT
metadata:
  author: supabase
  version: "1.0.0"
  source_repo: supabase/agent-skills
  source_ref: main
  adapted_for: EquipQR
---

# Postgres Best Practices (Supabase, adapted for EquipQR)

Comprehensive performance optimization guide for Postgres, maintained by Supabase. Contains rules across 8 categories, prioritized by impact to guide automated query optimization and schema design.

## EquipQR applicability notes (important)

EquipQR uses **Supabase Postgres**. When applying these rules in this repo:

- **Migrations live in**: `supabase/migrations/*.sql` (follow our migration standards: timestamped filenames, enable RLS by default, avoid overly complex RLS joins, etc.).
- **RLS is mandatory**: Never add permissive “always true” policies without explicit, documented justification.
- **Service role usage**: Edge Functions (including Google Workspace integrations) must rely on RLS by default. Use `service_role` only in narrowly scoped, backend-only functions where you (1) validate the JWT, (2) enforce `organization_id` scoping on every query, and (3) perform explicit permission checks at least as strict as equivalent RLS policies. Never use `service_role` as a shortcut to bypass RLS.
- **App code boundaries**: UI components should not issue raw SQL; changes here typically translate into migrations, RPCs, or changes to query patterns in services.

## When to Apply

Reference these guidelines when:
- Writing SQL queries or designing schemas
- Implementing indexes or query optimization
- Reviewing database performance issues
- Configuring connection pooling or scaling
- Optimizing for Postgres-specific features
- Working with Row-Level Security (RLS)

## Rule Categories by Priority

| Priority | Category | Impact | Prefix |
|----------|----------|--------|--------|
| 1 | Query Performance | CRITICAL | `query-` |
| 2 | Connection Management | CRITICAL | `conn-` |
| 3 | Security & RLS | CRITICAL | `security-` |
| 4 | Schema Design | HIGH | `schema-` |
| 5 | Concurrency & Locking | MEDIUM-HIGH | `lock-` |
| 6 | Data Access Patterns | MEDIUM | `data-` |
| 7 | Monitoring & Diagnostics | LOW-MEDIUM | `monitor-` |
| 8 | Advanced Features | LOW | `advanced-` |

## How to Use

Read individual rule files for detailed explanations and SQL examples:

```
rules/query-missing-indexes.md
rules/schema-partial-indexes.md
rules/_sections.md
```

Each rule file contains:
- Brief explanation of why it matters
- Incorrect SQL example with explanation
- Correct SQL example with explanation
- Optional EXPLAIN output or metrics
- Additional context and references
- Supabase-specific notes (when applicable)

## Full Compiled Document

For the complete guide with all rules expanded: `AGENTS.md`
