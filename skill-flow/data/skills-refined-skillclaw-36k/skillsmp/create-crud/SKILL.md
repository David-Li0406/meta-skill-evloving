---
name: create-crud
description: Generate complete CRUD operations for an entity using CQRS pattern
allowed-tools: [Read, Write, Edit, Bash, Glob, Grep]
---

# Create CRUD

When to use this skill:

- Creating standard CRUD operations for an entity
- Adding create, read, update, delete functionality
- Building database-backed resources

What this skill does:

1. Creates CQRS command handlers (create, update, delete)
2. Creates CQRS query handlers (get, list)
3. Generates repository with transaction support
4. Creates Zod validation schemas
5. Adds tRPC router
6. Writes unit tests with 80% coverage
7. Writes integration tests using Testcontainers

Usage:

```
"Create CRUD for Product with fields: name:string, price:number, description:text"
```
