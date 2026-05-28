# Server Actions

Server Actions orchestrate data mutations and cache invalidation.

## Basic Pattern

```typescript
// features/agents/actions/delete-agent-action.ts
"use server";

import { updateTag } from "next/cache";
import { deleteAgent } from "@/features/agents/data/delete-agent";

export async function deleteAgentAction(agentId: number, userId: string) {
  await deleteAgent(agentId);

  // Invalidate all affected caches
  updateTag(`agent-${agentId}`);
  updateTag(`messages-${agentId}`);
  updateTag(`recent-agents-${userId}`);
  updateTag(`agents-${userId}`);
}
```

---

## With Authentication

```typescript
// features/agents/actions/create-agent-action.ts
"use server";

import { headers } from "next/headers";
import { auth } from "@/features/auth/lib/auth-server";
import { updateTag } from "next/cache";
import { createAgent } from "@/features/agents/data/create-agent";

export async function createAgentAction(data: AgentInput) {
  const session = await auth.api.getSession({ headers: await headers() });

  if (!session?.user) {
    return { success: false, error: "Authentication required" };
  }

  const agent = await createAgent({ 
    userId: session.user.id,
    ...data 
  });

  updateTag(`recent-agents-${session.user.id}`);
  updateTag(`agents-${session.user.id}`);

  return { success: true, data: agent };
}
```

---

## With Validation

```typescript
// features/agents/actions/update-agent-action.ts
"use server";

import { updateTag } from "next/cache";
import { agentSchema } from "@/features/agents/schemas/agent-schema";
import { updateAgent } from "@/features/agents/data/update-agent";

export async function updateAgentAction(id: number, formData: FormData) {
  const parsed = agentSchema.safeParse(Object.fromEntries(formData));
  
  if (!parsed.success) {
    return { success: false, error: parsed.error.flatten() };
  }

  const agent = await updateAgent(id, parsed.data);

  updateTag(`agent-${id}`);

  return { success: true, data: agent };
}
```

---

## Return Type Convention

```typescript
// features/shared/types/action-response.ts
export type ActionResponse<T> = {
  success: boolean
  data?: T
  error?: string
}
```

### Usage
```typescript
export async function myAction(): Promise<ActionResponse<Agent>> {
  // ...
  return { success: true, data: agent };
  // or
  return { success: false, error: "Something went wrong" };
}
```

---

## Cache Invalidation

### Functions
- `updateTag(tag)` - Invalidates cache entries with this tag
- `revalidateTag(tag)` - Alias for updateTag

### Invalidation Rules

When modifying an entity, invalidate:

1. **The entity itself**: `updateTag(\`agent-${id}\`)`
2. **Related entities**: `updateTag(\`messages-${agentId}\`)`
3. **List queries**: `updateTag(\`agents-${userId}\`)`
4. **Subset queries**: `updateTag(\`recent-agents-${userId}\`)`

### Example: Delete Agent
```typescript
export async function deleteAgentAction(agentId: number, userId: string) {
  await deleteAgent(agentId);

  // Invalidate everything affected
  updateTag(`agent-${agentId}`);          // The agent itself
  updateTag(`messages-${agentId}`);       // Its messages
  updateTag(`agents-${userId}`);          // User's agent list
  updateTag(`recent-agents-${userId}`);   // User's recent agents
}
```

---

## Rules

1. `"use server"` directive at top of file
2. Call data layer functions (never query DB directly)
3. Call `updateTag()` for ALL affected cache tags
4. Return `{ success: boolean; data?: T; error?: string }`
5. File naming: `{verb}-{entity}-action.ts`
