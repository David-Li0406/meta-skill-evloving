---
name: mysql-best-practices
description: MySQL database development standards. Triggers when working with MySQL databases, queries, schema design, or optimization.
trigger_patterns:
  - mysql
  - SELECT
  - INSERT
  - UPDATE
  - CREATE TABLE
  - ALTER TABLE
  - INDEX
auto_load_with: []
---

# MySQL Best Practices

Comprehensive coding standards for MySQL database development, optimized for AI agents and LLMs.

## Overview

This skill provides 24 rules organized across 8 categories:

1. **Query Optimization (query-)** - EXPLAIN, N+1 prevention, pagination [CRITICAL]
2. **Security (security-)** - Prepared statements, least privilege, encryption [CRITICAL]
3. **Schema Design (schema-)** - Data types, normalization, constraints [HIGH]
4. **Indexing Strategy (index-)** - Composite indexes, covering indexes [HIGH]
5. **Transaction Management (txn-)** - ACID, isolation levels, deadlocks [MEDIUM-HIGH]
6. **Connection Management (conn-)** - Pooling, timeouts [MEDIUM]
7. **Backup & Recovery (backup-)** - Strategies, point-in-time recovery [MEDIUM]
8. **Replication (repl-)** - Master-slave, read replicas [LOW-MEDIUM]

## Usage

Reference this skill when:
- Designing database schemas
- Writing or optimizing SQL queries
- Implementing indexes
- Managing transactions
- Configuring connections

## Build

```bash
pnpm build    # Compile rules to AGENTS.md
pnpm validate # Validate rule files
```
