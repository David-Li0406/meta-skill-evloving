---
name: mariadb-best-practices
description: MariaDB database development standards. Triggers when working with MariaDB databases, Galera cluster, or MariaDB-specific features.
trigger_patterns:
  - mariadb
  - galera
  - aria
  - columnstore
  - system versioning
auto_load_with:
  - mysql-best-practices
---

# MariaDB Best Practices

Comprehensive coding standards for MariaDB database development, optimized for AI agents and LLMs.

## Overview

This skill provides 22 rules organized across 8 categories:

1. **Query Optimization (query-)** - MariaDB optimizer hints, statistics [CRITICAL]
2. **Security (security-)** - Authentication plugins, encryption at rest [CRITICAL]
3. **Schema Design (schema-)** - System versioning, sequences [HIGH]
4. **Storage Engines (engine-)** - InnoDB, Aria, ColumnStore selection [HIGH]
5. **Galera Cluster (galera-)** - Multi-master, SST methods [MEDIUM-HIGH]
6. **Performance Tuning (perf-)** - Thread pool, buffer pool [MEDIUM]
7. **JSON Features (json-)** - JSON functions, dynamic columns [MEDIUM]
8. **Compatibility (compat-)** - MySQL compatibility, migration [LOW-MEDIUM]

## Usage

Reference this skill when:
- Working with MariaDB-specific features
- Setting up Galera cluster
- Using system versioned tables
- Optimizing MariaDB performance
- Migrating from MySQL to MariaDB

## Build

```bash
pnpm build    # Compile rules to AGENTS.md
pnpm validate # Validate rule files
```
