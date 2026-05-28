# Database Schema Patterns for RAG Chatbot

## Core Tables

### Users Table
Stores user authentication and profile data.

```typescript
import { pgTable, text, timestamp, boolean } from 'drizzle-orm/pg-core';

export const users = pgTable('users', {
  id: text('id').primaryKey(), // UUID from crypto.randomUUID()
  email: text('email').notNull().unique(),
  name: text('name'),
  passwordHash: text('password_hash'),
  emailVerified: boolean('email_verified').default(false),
  createdAt: timestamp('created_at').defaultNow(),
  updatedAt: timestamp('updated_at').defaultNow(),
});
```

**Indexes**:
```sql
CREATE INDEX idx_users_email ON users(email);
```

### Sessions Table
Manages user sessions for authentication.

```typescript
export const sessions = pgTable('sessions', {
  id: text('id').primaryKey(),
  userId: text('user_id').references(() => users.id, { onDelete: 'cascade' }).notNull(),
  expiresAt: timestamp('expires_at').notNull(),
  createdAt: timestamp('created_at').defaultNow(),
});
```

**Indexes**:
```sql
CREATE INDEX idx_sessions_user_id ON sessions(user_id);
CREATE INDEX idx_sessions_expires_at ON sessions(expires_at);
```

### Chat History Table
Stores conversation history between users and AI.

```typescript
export const chatHistory = pgTable('chat_history', {
  id: text('id').primaryKey(),
  userId: text('user_id').references(() => users.id, { onDelete: 'cascade' }).notNull(),
  message: text('message').notNull(),
  response: text('response').notNull(),
  metadata: jsonb('metadata'), // Store sources, scores, etc.
  createdAt: timestamp('created_at').defaultNow(),
});
```

**Indexes**:
```sql
CREATE INDEX idx_chat_history_user_id ON chat_history(user_id);
CREATE INDEX idx_chat_history_created_at ON chat_history(created_at DESC);
```

**Metadata JSONB Structure**:
```json
{
  "sources": [
    { "chapter": "Chapter 2", "section": "ROS 2 Architecture", "score": 0.89 }
  ],
  "model": "gpt-4",
  "tokens": 450
}
```

## Optional Tables

### User Preferences
Store user-specific settings.

```typescript
export const userPreferences = pgTable('user_preferences', {
  userId: text('user_id').references(() => users.id, { onDelete: 'cascade' }).primaryKey(),
  theme: text('theme').default('light'),
  emailNotifications: boolean('email_notifications').default(true),
  updatedAt: timestamp('updated_at').defaultNow(),
});
```

### Feedback Table
Capture user feedback on AI responses.

```typescript
export const feedback = pgTable('feedback', {
  id: text('id').primaryKey(),
  chatHistoryId: text('chat_history_id').references(() => chatHistory.id),
  rating: integer('rating'), // 1-5 stars
  comment: text('comment'),
  createdAt: timestamp('created_at').defaultNow(),
});
```

## Schema Evolution Best Practices

1. **Always use migrations** for schema changes
2. **Never drop columns** in production without backups
3. **Add new columns as nullable** first, then fill data, then make `notNull()`
4. **Use foreign keys** with `onDelete: 'cascade'` for referential integrity
5. **Add indexes** on frequently queried columns (user_id, email, created_at)
6. **Use JSONB** for flexible, evolving data structures (metadata)

## Example Migration

```typescript
// drizzle/0001_add_user_preferences.ts
import { sql } from 'drizzle-orm';

export async function up(db: Database) {
  await db.execute(sql`
    CREATE TABLE user_preferences (
      user_id TEXT PRIMARY KEY REFERENCES users(id) ON DELETE CASCADE,
      theme TEXT DEFAULT 'light',
      email_notifications BOOLEAN DEFAULT true,
      updated_at TIMESTAMP DEFAULT NOW()
    );
  `);
}

export async function down(db: Database) {
  await db.execute(sql`DROP TABLE IF EXISTS user_preferences;`);
}
```
