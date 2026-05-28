# Query Patterns for Neon with Drizzle

## Common Queries for RAG Chatbot

### User Management

#### Find User by Email
```typescript
import { eq } from 'drizzle-orm';
import { db } from './db';
import { users } from './db/schema';

async function getUserByEmail(email: string) {
  const [user] = await db
    .select()
    .from(users)
    .where(eq(users.email, email));
  
  return user;
}
```

#### Create New User
```typescript
async function createUser(email: string, passwordHash: string, name?: string) {
  const [user] = await db
    .insert(users)
    .values({
      id: crypto.randomUUID(),
      email,
      passwordHash,
      name,
    })
    .returning();
  
  return user;
}
```

### Session Management

#### Create Session
```typescript
async function createSession(userId: string, expiresIn: number = 7 * 24 * 60 * 60 * 1000) {
  const [session] = await db
    .insert(sessions)
    .values({
      id: crypto.randomUUID(),
      userId,
      expiresAt: new Date(Date.now() + expiresIn),
    })
    .returning();
  
  return session;
}
```

#### Validate Session
```typescript
import { and, gt } from 'drizzle-orm';

async function validateSession(sessionId: string) {
  const [session] = await db
    .select()
    .from(sessions)
    .where(
      and(
        eq(sessions.id, sessionId),
        gt(sessions.expiresAt, new Date())
      )
    );
  
  return session;
}
```

#### Delete Expired Sessions
```typescript
import { lt } from 'drizzle-orm';

async function deleteExpiredSessions() {
  await db
    .delete(sessions)
    .where(lt(sessions.expiresAt, new Date()));
}
```

### Chat History

#### Save Conversation
```typescript
async function saveConversation(
  userId: string,
  message: string,
  response: string,
  metadata?: any
) {
  const [chat] = await db
    .insert(chatHistory)
    .values({
      id: crypto.randomUUID(),
      userId,
      message,
      response,
      metadata,
    })
    .returning();
  
  return chat;
}
```

#### Get User Conversations
```typescript
import { desc } from 'drizzle-orm';

async function getUserConversations(userId: string, limit = 20) {
  return await db
    .select()
    .from(chatHistory)
    .where(eq(chatHistory.userId, userId))
    .orderBy(desc(chatHistory.createdAt))
    .limit(limit);
}
```

#### Search Conversations
```typescript
import { ilike } from 'drizzle-orm';

async function searchConversations(userId: string, query: string) {
  return await db
    .select()
    .from(chatHistory)
    .where(
      and(
        eq(chatHistory.userId, userId),
        or(
          ilike(chatHistory.message, `%${query}%`),
          ilike(chatHistory.response, `%${query}%`)
        )
      )
    )
    .orderBy(desc(chatHistory.createdAt));
}
```

### Complex Queries

#### Get Chat Stats
```typescript
import { count, sql } from 'drizzle-orm';

async function getChatStats(userId: string) {
  const [stats] = await db
    .select({
      totalChats: count(),
      avgResponseLength: sql<number>`AVG(LENGTH(${chatHistory.response}))`,
      firstChat: sql<Date>`MIN(${chatHistory.createdAt})`,
      lastChat: sql<Date>`MAX(${chatHistory.createdAt})`,
    })
    .from(chatHistory)
    .where(eq(chatHistory.userId, userId));
  
  return stats;
}
```

#### User with Sessions and Chats
```typescript
async function getUserWithRelations(userId: string) {
  const user = await db
    .select({
      user: users,
      sessions: sessions,
      chats: chatHistory,
    })
    .from(users)
    .leftJoin(sessions, eq(users.id, sessions.userId))
    .leftJoin(chatHistory, eq(users.id, chatHistory.userId))
    .where(eq(users.id, userId));
  
  return user;
}
```

## Performance Tips

1. **Use indexes** on frequently queried columns
2. **Limit results** to avoid large datasets
3. **Use `.returning()`** to get data without extra query
4. **Batch operations** when possible
5. **Use transactions** for consistency
