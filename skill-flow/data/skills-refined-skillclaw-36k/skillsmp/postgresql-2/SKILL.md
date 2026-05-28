---
name: postgresql
description: Performance and design guidelines for PostgreSQL database in RSSVibe, including connection pooling, JSONB columns, and query optimization. Use this skill when optimizing database performance.
---

# PostgreSQL Database

## Performance & Design

- MUST use connection pooling for efficient connection management
- MUST use JSONB columns for semi-structured data (avoid creating many tables for flexible schemas)
- MUST create indexes on frequently queried columns to improve read performance

---

## Query Optimization

- SHOULD monitor query plans for expensive operations
- SHOULD use partial indexes when filtering on specific conditions
- SHOULD consider materialized views for complex aggregations
