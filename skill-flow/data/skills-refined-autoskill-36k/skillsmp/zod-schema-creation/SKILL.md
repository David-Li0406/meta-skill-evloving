---
name: zod-schema-creation
description: Guide through creating Zod validation schemas with i18n integration for API request validation. Use when creating API endpoints that need validation.
---

# Zod Validation Schema Creation Skill

Guides through creating Zod validation schemas with i18n integration for API request validation.

## Purpose

USE this skill when:
- Creating new API endpoints that accept request bodies
- Adding validation for POST, PUT, or PATCH requests
- Implementing form validation schemas

## Critical Rules

⚠️ **Factory pattern REQUIRED** - Schemas must accept translation function `t: (key: string) => string`
⚠️ **i18n keys in errors** - All error messages use translation keys, not hardcoded text
⚠️ **File organization** - All schemas in `shared/utils/schemas/` directory
⚠️ **Type export** - Always export TypeScript type using `z.infer<ReturnType<...>>`

## Workflow Steps

### Step 1: Identify Validation Requirements
- What fields are required/optional?
- What validation rules apply?
- Creating (create schema) or updating (update schema)?

### Step 2: Create Schema File
Location: `shared/utils/schemas/{resource}.ts`

### Step 3: Implement Factory Function Pattern

```typescript
import { z } from "zod"

export function createSpeakerSchema(t: (key: string) => string) {
  return z.object({
    firstName: z
      .string()
      .min(1, t("validation.firstNameRequired"))
      .max(100, t("validation.firstNameTooLong")),
    
    lastName: z
      .string()
      .min(1, t("validation.lastNameRequired"))
      .max(100),
    
    email: z
      .string()
      .email(t("validation.emailInvalid"))
      .optional(),
  })
}
```

### Step 4: Export TypeScript Type

```typescript
export type CreateSpeakerInput = z.infer<ReturnType<typeof createSpeakerSchema>>
```

### Step 5: Create Update Schema (If Needed)

```typescript
export function updateSpeakerSchema(t: (key: string) => string) {
  return createSpeakerSchema(t).partial()
}

export type UpdateSpeakerInput = z.infer<ReturnType<typeof updateSpeakerSchema>>
```

### Step 6: Update Barrel File
Add to `shared/utils/schemas/index.ts`:
```typescript
export * from "./speaker"
```

### Step 7: Add Translation Keys
Use `i18n-key-validation` skill to ensure keys exist in both pl.json and en.json

### Step 8: Implement in API Route

```typescript
import { createSpeakerSchema } from "#shared/utils/schemas"

export default defineEventHandler(async (event) => {
  const body = await validateBody(event, createSpeakerSchema)
  
  // body is now typed and validated
  const db = useDrizzle()
  const [speaker] = await db.insert(tables.speakers)
    .values({
      id: crypto.randomUUID(),
      ...body,
      createdAt: new Date(),
      updatedAt: new Date(),
    })
    .returning()
  
  return speaker
})
```

## Common Validation Patterns

```typescript
// String with length
field: z.string().min(1, t("validation.required")).max(200)

// Email
email: z.string().email(t("validation.emailInvalid")).optional()

// Number
age: z.number().min(0).max(150)

// Enum
status: z.enum(["active", "archived"])

// Array
tags: z.array(z.string()).max(10)
```

## Anti-Patterns

❌ Hardcoded error messages
❌ No factory pattern
❌ Wrong file location
❌ Missing type export

## References
- Backend guidelines: `server/AGENTS.md`
- i18n patterns: `.agents/i18n-patterns.md`
