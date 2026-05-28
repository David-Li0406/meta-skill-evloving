---
name: Database Health & Optimization
description: Tools to validate schema, check for missing indexes, and audit Prisma patterns.
---

# 🗄️ Database Health & Optimization Skill

This skill operationalizes the knowledge of the **Database Specialist** agent. It ensures your Prisma schema is performant and your data integrity is maintained.

## 🎯 When to Use
- **Modifying Schema**: ALWAYS run audit before `prisma migrate`.
- **Debugging Slow Queries**: Check for missing indexes.
- **Data Modeling**: When adding new relations.

## 🛠️ Toolbelt

### 1. The Schema Auditor (Automated)
Checks `schema.prisma` for performance killers and missing indexes.

```bash
node .agent/skills/db-optimizer/scripts/audit-prisma-schema.js
```

### 2. The Migration Canary (Manual Guide)
**STOP.** Before you run a migration, verify against this table:

| Action | Risk Level | The Safe Way |
|:---:|:---:|:---:|
| **Renaming Column** | 🛑 **DATA LOSS** | Use `@map("old_name")` to keep DB column same, or write a manual SQL migration. |
| **Changing Type** | ⚠️ **LOCKS** | Be careful with large tables. Might need maintenance window. |
| **Adding Relation** | ⚠️ **PERF** | **MUST** add `@@index([foreignKeyId])` on the child side. |

## 🚀 Workflows

### Workflow A: The Safe Migration
Use this whenever you edit `schema.prisma`.

1. **Design**: Edit the schema.
2. **Audit**: Run `audit-prisma-schema.js`. Fix any missing indexes.
3. **Dry Run**: Run `npx prisma migrate dev --create-only`.
4. **Review**: Check the generated SQL file. Does it drop data?
5. **Apply**: Only then, apply the migration.

### Workflow B: The Performance Tune-up
Use this when users complain about slowness.

1. **Identify**: Which query is slow? Find the `where` or `orderBy` clause.
2. **Index**: Add a composite index `@@index([fieldA, fieldB])`.
3. **Verify**: Run `audit-prisma-schema.js` to ensure you didn't break rules.

## 🧠 Best Practices
- **Foreign Keys**: Prisma does NOT index FKs by default. You **MUST** do it manually.
- **Json Fields**: Avoid if possible. Relational tables are faster and safer.
- **IDs**: Use CUID (`cuid()`) or UUID (`uuid()`) for primary keys. Never auto-increment integers for public IDs.
