---
name: payload-cms
description: Use this skill when developing with Payload CMS, including tasks related to collections, fields, hooks, access control, and debugging.
---

# Payload CMS Development

Payload is a Next.js native CMS with a TypeScript-first architecture. This skill provides expert guidance for building collections, hooks, access control, and executing database queries effectively.

## Mental Model

Think of Payload as **three interconnected layers**:

1. **Config Layer** → Collections, globals, fields define your schema.
2. **Hook Layer** → Lifecycle events transform and validate data.
3. **Access Layer** → Functions control who can do what.

Every operation flows through: `Config → Access Check → Hook Chain → Database → Response Hooks`.

## Quick Reference

| Task                     | Solution                                  | Details                                                                                                                          |
|--------------------------|-------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------|
| Auto-generate slugs      | `slugField()`                             | [FIELDS.md#slug-field-helper](reference/FIELDS.md#slug-field-helper)                                                             |
| Restrict content by user | Access control with query                 | [ACCESS-CONTROL.md#row-level-security-with-complex-queries](reference/ACCESS-CONTROL.md#row-level-security-with-complex-queries) |
| Local API user ops       | `user` + `overrideAccess: false`          | [QUERIES.md#access-control-in-local-api](reference/QUERIES.md#access-control-in-local-api)                                       |
| Draft/publish workflow   | `versions: { drafts: true }`              | [COLLECTIONS.md#versioning--drafts](reference/COLLECTIONS.md#versioning--drafts)                                                 |
| Computed fields          | `virtual: true` with afterRead            | [FIELDS.md#virtual-fields](reference/FIELDS.md#virtual-fields)                                                                   |
| Conditional fields       | `admin.condition`                          | [FIELDS.md#conditional-fields](reference/FIELDS.md#conditional-fields)                                                           |
| Filter relationships      | `filterOptions` on field                  | [FIELDS.md#relationship](reference/FIELDS.md#relationship)                                                                       |
| Prevent hook loops       | `req.context` flag                        | [HOOKS.md#context](reference/HOOKS.md#context)                                                                                 |
| Transactions             | Pass `req` to all operations              | [HOOKS.md#transactions](reference/HOOKS.md#transactions)                                                                         |
| Background jobs          | Jobs queue with tasks                     | [ADVANCED.md#jobs](reference/ADVANCED.md#jobs)                                                                                   |

## Quick Start

```bash
npx create-payload-app@latest my-app
cd my-app
pnpm dev
```

### Minimal Config

```ts
import { buildConfig } from 'payload'
import { mongooseAdapter } from '@payloadcms/db-mongodb'
import { lexicalEditor } from '@payloadcms/richtext-lexical'

export default buildConfig({
  admin: { user: 'users' },
  collections: [Users, Media, Posts],
  editor: lexicalEditor(),
  secret: process.env.PAYLOAD_SECRET,
  typescript: true,
})
```