---
name: neon-database
description: Use when working with Neon serverless PostgreSQL database. Covers database setup, CLI commands, Drizzle ORM integration, schema migrations, connection pooling, and user data storage patterns for authentication and chat history.
---

# Neon Database Skill

## Quick Start Workflow

When working with Neon PostgreSQL:

1. **Check if database exists**
   - Look in `.env` or `.env.local` for `DATABASE_URL`
   - Verify connection with `neon connection-string`

2. **For schema changes**
   - Always use Drizzle migrations (never manual SQL)
   - Check `drizzle.config.ts` is configured
   - Generate migration: `drizzle-kit generate`
   - Apply migration: `drizzle-kit push`

3. **For user data storage**
   - Use `users` table for authentication
   - Use `sessions` table for session management
   - Use `chat_history` table for conversations
   - Always include `user_id` foreign key

4. **For queries**
   - Use Drizzle ORM for type safety
   - Implement proper error handling
   - Use transactions for multi-table operations

### Standard Patterns

#### Environment Variables
```env
DATABASE_URL="postgresql://user:pass@ep-xxx.us-east-2.aws.neon.tech/neondb?sslmode=require"
```

#### Connection Setup
```typescript
import { drizzle } from 'drizzle-orm/neon-http';
import { neon } from '@neondatabase/serverless';

const sql = neon(process.env.DATABASE_URL!);
export const db = drizzle(sql);
```

### Database Design Principles

For this Physical AI RAG chatbot:
- **Users table**: Store authentication data (email, password_hash, email_verified)
- **Sessions table**: Manage user sessions (connect to users via user_id)
- **Chat history table**: Store Q&A pairs with user attribution
- **All timestamps**: Use `timestamp('created_at').defaultNow()`
- **All IDs**: Use `text('id').primaryKey()` with `crypto.randomUUID()`

## Knowledge Base

For detailed information, check these references:
- **CLI Commands** → `references/neon-cli.md`
- **Drizzle ORM Setup** → `references/drizzle-orm.md`
- **Schema Patterns** → `references/database-schemas.md`
- **Query Examples** → `references/query-patterns.md`
- **Migrations Guide** → `references/migrations.md`
