---
name: prisma
description: Read when modifying schema.prisma
---

# Prisma Rules


## Tech Stack
- Database: PostgreSQL running on RDS
- Prisma v2

## Naming Conventions
- Tables are named with TitleCase
- Columns are named with camelCase
- Tables are singular, e.g. "User" not "Users"
- **Never use GraphQL built-in type names as tables** (e.g., `Subscription`, `Query`, `Mutation`)

### By type
- Boolean: Start with `is`, `can`, `are` (e.g., `isActive`)
- Date: End with `At` (e.g., `createdAt`)
- Array: Use plural form (e.g., `users`)
- Enums: Use TitleCase (e.g., `OrganizationKind`)

## Standard Model Structure
- Every model has: `id`, `createdAt`, `updatedAt`
- User-owned entities have: `userId` and `user` relation
- Org-owned entities have: `orgId` and `org` relation

## Relations
- Foreign keys end with `Id` (e.g., `userId`, `stateId`)
- Relation fields omit the `Id` suffix (e.g., `user`, `state`)
- Use `@unique` where applicable
- Add `onDelete: Cascade` for dependent entities
- Do NOT use @relation `name` unless we have too, aka +1 relations to the same table

## Status Enums
- Status enums follow pattern: `EntityNameStatus` (e.g., `ProductStatus`, `ReceiptStatus`)
- Common status values: `Draft`, `Pending`, `Active`, `Archived`
- Use `@default()` for initial status

## Indexes
- Add indexes for: foreign keys, status fields, date fields, commonly filtered fields
- Don't create indexes for columns that are already `@unique` or `@id`

## Column order and grouping
Requires a new line after each group
1. id, createdAt, updatedAt, userId/user (if exists), orgId/org (if exists)
2. All non-relational columns
3. One group per relation: xId field first, then x relation field, blank line before next relation
4. All list relations (users[], payments[], etc.)
5. @@unique lines, then @@index lines come last
