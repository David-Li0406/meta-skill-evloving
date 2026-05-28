---
name: nextjs-server-actions
description: Use this skill when you need to create, modify, or debug Next.js Server Actions with TypeScript, ensuring best practices for validation, error handling, and form handling.
---

# Next.js Server Actions Skill

This skill provides a comprehensive guide for implementing Next.js Server Actions, focusing on type safety, error handling, and optimal user experience patterns.

## ⚠️ PRAGMATIC PATTERN SELECTION

> **Not every operation needs full DDD architecture. Choose the right pattern for the job.**

### Quick Decision Guide

| Operation Type                   | Pattern                       | Example                |
| -------------------------------- | ----------------------------- | ---------------------- |
| **Read-only public data**        | Simple Repository             | `findAllCharacters()`  |
| **Simple mutation, no rules**    | Basic Server Action           | `incrementViewCount()` |
| **Mutation with business rules** | Server Action + UseCase       | `trackEpisode()`       |
| **User-owned data**              | Server Action + UseCase + RLS | `createDiaryEntry()`   |

### Step-by-Step Instructions

1. **Analyze Requirements**
   - Gather information about:
     - What data does the action handle?
     - Does it return data or redirect?
     - What validation is needed?
     - What authentication/authorization is required?
     - What errors need to be handled?
     - What cache paths need revalidation?

2. **Choose Response Type**
   - Determine the appropriate response based on the action's requirements.

3. **Implement Server Actions**
   - Use the following patterns based on the operation type:

#### 🟢 Simple Pattern (Read + Basic Mutations)

```typescript
// For operations WITHOUT business rules
// app/_lib/repositories.ts
export async function findAllCharacters(limit = 50) {
  return prisma.character.findMany({ take: limit });
}

// Page uses directly
const characters = await findAllCharacters();
```

#### 🟡 Standard Server Action (Light Mutations)

```typescript
// For mutations with Zod validation but no complex business logic
"use server";
import { z } from "zod";

const Schema = z.object({ name: z.string().min(1) });

export async function updateName(name: string) {
  const validated = Schema.parse({ name });
  await prisma.item.update({ data: { name: validated.name } });
  revalidatePath("/items");
  return { success: true };
}
```

#### 🔴 Full DDD Pattern (Complex Mutations)

```typescript
// For mutations WITH business rules, user ownership, RLS
"use server";
import { withAuthenticatedRLS } from "@/app/_lib/prisma-rls";
import { UseCaseFactory } from "@/infrastructure/factories";

export async function createDiaryEntry(...) {
  return withAuthenticatedRLS(prisma, async (tx, user) => {
    const useCase = UseCaseFactory.createCreateDiaryEntryUseCase();
    // UseCase implementation here
  });
}
```

### Additional Resources
- **Validation**: Use Zod for schema validation.
- **Error Handling**: Implement robust error handling strategies.
- **Form Handling**: Integrate with React Hook Form for managing form state.

This skill is designed to streamline the development of server actions in Next.js, ensuring adherence to best practices and efficient handling of server-side operations.