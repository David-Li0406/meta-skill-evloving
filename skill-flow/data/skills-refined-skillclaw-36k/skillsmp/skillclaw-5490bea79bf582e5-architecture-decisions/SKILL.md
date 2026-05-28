---
name: architecture-decisions
description: Use this skill when you need guidance on selecting frameworks, runtimes, databases, nodes, and testing strategies for your Kailash application.
---

# Kailash Architecture Decisions

Decision guides for selecting the right frameworks, runtimes, databases, nodes, and testing strategies for your Kailash application.

## Overview

Comprehensive decision guides for:
- Framework selection (Core SDK, DataFlow, Nexus, Kaizen)
- Runtime selection (AsyncLocalRuntime vs LocalRuntime)
- Database selection (PostgreSQL vs SQLite)
- Node selection for specific tasks
- Test tier selection (Unit, Integration, E2E)

## Reference Documentation

### Framework Selection
- **[decide-framework](decide-framework.md)** - Choose the right framework
  - Core SDK: Custom workflows with full control
  - DataFlow: Database-first applications
  - Nexus: Multi-channel platforms
  - Kaizen: AI agent systems
  - When to use each
  - Combining frameworks

### Runtime Selection
- **[decide-runtime](decide-runtime.md)** - AsyncLocalRuntime vs LocalRuntime
  - Docker/FastAPI → AsyncLocalRuntime
  - CLI/Scripts → LocalRuntime
  - Performance implications
  - Threading considerations
  - Auto-detection with get_runtime()

### Database Selection
- **[decide-database-postgresql-sqlite](decide-database-postgresql-sqlite.md)** - PostgreSQL vs SQLite
  - Production → PostgreSQL
  - Development/Testing → SQLite
  - Feature comparison
  - Migration strategies
  - Multi-database support

### Node Selection
- **[decide-node-for-task](decide-node-for-task.md)** - Choose the right node
  - AI tasks → AI nodes
  - API calls → API nodes
  - Custom logic → PythonCodeNode
  - Database → Database nodes or DataFlow
  - File operations → File nodes
  - Conditional logic → SwitchNode

### Test Tier Selection
- **[decide-test-tier](decide-test-tier.md)** - Unit vs Integration vs E2E
  - Tier 1: Unit tests (fast, mocking allowed)
  - Tier 2: Integration tests (real infrastructure)
  - Tier 3: End-to-end tests (full system)
  - When to use each tier
  - Coverage targets

## Key Decision Frameworks

### Framework Selection