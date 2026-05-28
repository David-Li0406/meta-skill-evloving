---
name: zenstack-relation-naming-discovery
description: |
  Discover actual ZenStack/Prisma relation field names when type errors occur.
  Use when: (1) TypeScript errors like "Property 'verificationRecord' does not exist"
  on model instances, (2) Runtime errors accessing relations, (3) Implementing new
  features that query related data. Solves the problem of mismatched assumptions
  about relation names vs actual schema-generated names.
author: Claude Code
version: 1.0.0
date: 2026-01-22
---

# ZenStack Relation Naming Discovery

## Problem

When working with ZenStack (enhanced Prisma), the actual relation field names on model
instances don't always match what you expect from reading the schema. This causes
TypeScript errors and runtime failures when accessing related data.

**Common scenario**: Schema defines `verificationRecord VerificationRecord?` but the
actual field name is `verification`, not `verificationRecord`.

## Context / Trigger Conditions

Use this pattern when you encounter:

1. **TypeScript errors** like:
   ```
   Property 'verificationRecord' does not exist on type 'User'
   Property 'documentsOwned' does not exist on type 'User'
   ```

2. **Runtime errors** when accessing relations:
   ```
   Cannot read property 'status' of undefined
   ```

3. **Implementing new queries** that need to include related data and you're unsure
   of the exact field names

## Solution

### Step 1: Check the Schema Definition

Look at the schema in `packages/database/zenstack/schema.zmodel` (or `.prisma` file):

```zmodel
model User {
  id String @id
  verification VerificationRecord?  // ← Note the field name here
  documents Document[]               // ← And here
}

model VerificationRecord {
  id String @id
  userId String @unique
  user User @relation(fields: [userId], references: [id])
}
```

**Key insight**: The relation field name is determined by:
- **Explicit name in schema**: `verification VerificationRecord?` → field name is `verification`
- **Not the type name**: The type `VerificationRecord` doesn't determine the field name

### Step 2: Verify with Generated Types

Check the generated TypeScript types in `packages/database/zenstack/models.ts`:

```typescript
// Search for your model
export type User = {
  id: string;
  verification?: VerificationRecord | null;  // ← Actual field name
  documents: Document[];                     // ← Actual field name
}
```

This shows the **exact** field names available on instances.

### Step 3: Test with a Database Query (if still unsure)

Write a simple query to see what's actually available:

```typescript
const user = await db.user.findUnique({
  where: { id: 'some-id' },
  include: {
    verification: true,  // Try the suspected name
    documents: true
  }
});

console.log(Object.keys(user)); // See all available fields
```

### Step 4: Update Your Code

Use the **actual** field names from the schema/types:

```typescript
// ❌ WRONG (assumed names)
const status = instructor.verificationRecord?.status;
const docs = instructor.documentsOwned;

// ✅ CORRECT (actual schema names)
const status = instructor.verification?.status;
const docs = instructor.documents;
```

## Verification

After using the correct field names:
- ✅ TypeScript errors disappear
- ✅ Queries execute without runtime errors
- ✅ Related data is properly accessed

## Example

**Scenario**: Implementing admin verification UI, need to access instructor's verification
record and documents.

**Initial attempt** (based on assumptions):
```typescript
const instructor = await baseDB.user.findUnique({
  where: { id: instructorId },
  include: {
    verificationRecord: true,  // ❌ Doesn't exist
    documentsOwned: true,       // ❌ Doesn't exist
  },
});
```

**After schema discovery**:
```typescript
const instructor = await baseDB.user.findUnique({
  where: { id: instructorId },
  include: {
    verification: true,  // ✅ Correct name from schema
    documents: true,     // ✅ Correct name from schema
  },
});
```

## Common Patterns

### One-to-One Relations
```zmodel
model User {
  profile Profile?  // ← Field name: "profile"
}

// Access: user.profile (not user.userProfile)
```

### One-to-Many Relations
```zmodel
model User {
  vehicles Vehicle[]  // ← Field name: "vehicles"
}

// Access: user.vehicles (not user.vehiclesOwned)
```

### Many-to-Many Relations
```zmodel
model User {
  languages UserLanguage[]  // ← Field name: "languages"
}

// Access: user.languages (not user.userLanguages)
```

### Relations with Type Tables
```zmodel
model Profile {
  type ProfileType @relation(fields: [typeId], references: [id])
}

// Access: profile.type (not profile.profileType)
```

## Notes

- **Schema is source of truth**: The field name in the schema definition is the actual
  field name on instances
- **Type name ≠ Field name**: `verification VerificationRecord?` creates a field called
  `verification`, not `verificationRecord`
- **Prisma conventions**: Prisma (and ZenStack) follow these naming rules consistently
- **Generated types are reliable**: Always check `models.ts` when in doubt
- **Include syntax matches**: The `include` object uses the same field names as schema

## References

- [Prisma Relations Documentation](https://www.prisma.io/docs/orm/prisma-schema/data-model/relations)
- [ZenStack ZModel Language Reference](https://zenstack.dev/docs/reference/zmodel-language)
- [Prisma Naming Conventions Discussion](https://github.com/prisma/prisma/discussions/10395)
- [Custom Model and Field Names | Prisma](https://www.prisma.io/docs/orm/prisma-client/setup-and-configuration/custom-model-and-field-names)
