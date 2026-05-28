---
name: sql
description: Read when writing raw SQL queries
---

# SQL Rules


## Tech Stack
- Database: PostgreSQL running on RDS

## Naming Conventions
- Use uppercase for SQL reserved words
- Tables are named with "TitleCase", need quotes
- Columns are named with "camelCase"
- CTEs and table aliases use very short names, usually 1 or 2 characters (the initials)
- Tables are singular, e.g. "User" not "Users"
- Tables are aliased to a single character

### By type
- Boolean: Start with `is`, `can`, `are` (e.g., `isActive`)
- Date: End with `At` (e.g., `createdAt`)
- Array: Use plural form (e.g., `users`)
- Enums: Use TitleCase (e.g., `OrganizationKind`)

## Do's
- Use CTEs if they make the code more readable

## Don'ts
- Write ugly code

## Misc
- Before providing a block of code, reason about what is requested and the context provided first
- When the query is shorter keep it on just a few lines. As it gets larger start adding newlines for readability
