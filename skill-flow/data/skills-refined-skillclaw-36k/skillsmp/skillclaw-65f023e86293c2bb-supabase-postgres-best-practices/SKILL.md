---
name: supabase-postgres-best-practices
description: Use this skill when writing, reviewing, or optimizing Postgres queries, schema designs, or database configurations, particularly in a Supabase environment.
---

# Postgres Best Practices

**Version 1.0.0**  
Supabase  
January 2026

## Abstract

This document serves as a comprehensive performance optimization guide for developers using Supabase and Postgres. It contains performance rules across multiple categories, prioritized by impact, to guide automated optimization and code generation.

## When to Apply

Reference these guidelines when:
- Writing SQL queries or designing schemas
- Implementing indexes or query optimization
- Reviewing database performance issues
- Configuring connection pooling or scaling
- Optimizing for Postgres-specific features
- Working with Row-Level Security (RLS)

## Rule Categories by Priority

| Priority | Category                | Impact       | Prefix   |
|----------|-------------------------|--------------|----------|
| 1        | Query Performance       | CRITICAL     | `query-` |
| 2        | Connection Management    | CRITICAL     | `conn-`  |
| 3        | Security & RLS         | CRITICAL     | `security-` |
| 4        | Schema Design           | HIGH         | `schema-` |
| 5        | Concurrency & Locking   | MEDIUM-HIGH  | `lock-`  |
| 6        | Data Access Patterns     | MEDIUM       | `data-`  |
| 7        | Monitoring & Diagnostics | LOW-MEDIUM   | `monitor-` |
| 8        | Advanced Features       | LOW          | `advanced-` |

## How to Use

Read individual rule files for detailed explanations and SQL examples. Each rule file contains:
- A brief explanation of why it matters
- Incorrect SQL example with explanation
- Correct SQL example with explanation
- Optional EXPLAIN output or metrics
- Additional context and references
- Supabase-specific notes (when applicable)

## Full Compiled Document

For the complete guide with all rules expanded, refer to the compiled document: `AGENTS.md`.

## Key Performance Rules

1. **Query Performance**
   - Add indexes on WHERE and JOIN columns.
   - Choose the right index type for your data.
   - Create composite indexes for multi-column queries.
   - Use covering indexes to avoid table lookups.
   - Use partial indexes for filtered queries.

2. **Connection Management**
   - Configure idle connection timeouts.
   - Set appropriate connection limits.
   - Use connection pooling for all applications.
   - Use prepared statements correctly with pooling.

3. **Security & RLS**
   - Apply the principle of least privilege.
   - Enable Row Level Security for multi-tenant data.
   - Optimize RLS policies for performance.

4. **Schema Design**
   - Choose appropriate data types.
   - Index foreign key columns.
   - Follow best practices for migrations and RLS policies.

This skill is designed to help developers optimize their Postgres databases effectively, ensuring high performance and security in their applications.