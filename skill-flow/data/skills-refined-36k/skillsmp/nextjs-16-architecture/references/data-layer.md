# Data Layer

All database queries live in `data/` folder.

## Cacheable Queries (SELECT)

```typescript
// features/agents/data/get-agent.ts
import { cacheLife, cacheTag } from "next/cache";
import { db } from "@/db/client";
import { agents } from "@/db/schemas/agents";
import { eq } from "drizzle-orm";
import type { Agent } from "@/db/schemas/agents";

export async function getAgent(agentId: number): Promise<Agent | null> {
  "use cache";
  cacheTag(`agent-${agentId}`);
  cacheLife("hours");

  const [agent] = await db
    .select()
    .from(agents)
    .where(eq(agents.id, agentId))
    .limit(1);

  return agent ?? null;
}
```

### Cache Directives
- `"use cache"` - Marks function as cacheable
- `cacheTag(tag)` - Names this cache entry for invalidation
- `cacheLife(duration)` - Sets cache duration: `"seconds"`, `"minutes"`, `"hours"`, `"days"`, `"weeks"`, `"max"`

---

## Multiple Results Query

```typescript
// features/agents/data/get-recent-agents.ts
export async function getRecentAgents(userId: string): Promise<Agent[]> {
  "use cache";
  cacheTag(`recent-agents-${userId}`);
  cacheLife("hours");

  return await db
    .select()
    .from(agents)
    .where(eq(agents.userId, userId))
    .orderBy(desc(agents.updatedAt))
    .limit(10);
}
```

---

## Non-Cacheable Queries (Session Data)

**Session/auth data must NEVER be cached.**

```typescript
// features/auth/data/get-current-user.ts
// NO CACHE - Sessions must never be cached
export async function getCurrentUser() {
  const session = await auth.api.getSession({ headers: await headers() })
  return session?.user ?? null
}
```

---

## Mutations (CREATE/UPDATE/DELETE)

Mutations don't use cache directives.

```typescript
// features/agents/data/create-agent.ts
export async function createAgent(data: AgentInsert): Promise<Agent> {
  const [agent] = await db.insert(agents).values(data).returning();
  return agent;
}

// features/agents/data/update-agent.ts
export async function updateAgent(id: number, data: Partial<AgentInsert>): Promise<Agent> {
  const [agent] = await db
    .update(agents)
    .set(data)
    .where(eq(agents.id, id))
    .returning();
  return agent;
}

// features/agents/data/delete-agent.ts
export async function deleteAgent(agentId: number): Promise<void> {
  await db.delete(agents).where(eq(agents.id, agentId));
}
```

---

## Return Types

| Query Type | Return Type |
|------------|-------------|
| Single entity | `Promise<Entity \| null>` |
| Multiple entities | `Promise<Entity[]>` |
| Create | `Promise<Entity>` |
| Update | `Promise<Entity>` |
| Delete | `Promise<void>` |

---

## Cache Tag Naming

Format: `{resource}-{identifier}` in kebab-case.

| Tag | Description |
|-----|-------------|
| `agent-123` | Single agent by ID |
| `agents-user456` | All agents for a user |
| `recent-agents-user456` | Recent agents subset |
| `messages-agent123` | Messages for an agent |

### Invalidation Strategy

When modifying data, invalidate:
1. **Direct entity**: `agent-${id}`
2. **Related entities**: `messages-${agentId}`
3. **User aggregations**: `agents-${userId}`, `recent-agents-${userId}`

---

## Summary

| Operation | Cache | Tag | Life |
|-----------|-------|-----|------|
| SELECT single | ✅ | `entity-${id}` | hours |
| SELECT multiple | ✅ | `entities-${userId}` | hours |
| Session/Auth | ❌ | - | - |
| INSERT | ❌ | - | - |
| UPDATE | ❌ | - | - |
| DELETE | ❌ | - | - |
