---
name: Supabase Database & Auth
description: Database operations, authentication, and real-time subscriptions via Supabase MCP
---

# Supabase MCP Integration

Manage PostgreSQL database, authentication, storage, and real-time features.

## Configuration ✅

**Status**: Configured with all keys

| Key | Status |
|-----|--------|
| `SUPABASE_URL` | ✅ Set |
| `SUPABASE_ANON_KEY` | ✅ Set |
| `SUPABASE_SERVICE_ROLE_KEY` | ✅ Set |
| `SUPABASE_JWT_SECRET` | ✅ Set |

## Capabilities

| Feature | Use Case |
|---------|----------|
| **Database** | CRUD, migrations, queries |
| **Auth** | User management, JWT validation |
| **Storage** | File uploads, signed URLs |
| **Real-time** | Live subscriptions |
| **Edge Functions** | Serverless TypeScript |

## Database Operations

### Run SQL Query
```sql
SELECT * FROM trades WHERE symbol = 'AAPL' ORDER BY created_at DESC LIMIT 10;
```

### Create Table
```sql
CREATE TABLE signals (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    symbol TEXT NOT NULL,
    direction TEXT NOT NULL,
    strength NUMERIC,
    created_at TIMESTAMPTZ DEFAULT NOW()
);
```

## Auth Integration

Use JWT validation for API endpoints:
```typescript
const { data: { user } } = await supabase.auth.getUser(token);
```

## Real-time for Trading

Enable live signal updates:
```typescript
supabase
  .channel('signals')
  .on('postgres_changes', { event: 'INSERT', schema: 'public', table: 'signals' }, 
      payload => handleNewSignal(payload))
  .subscribe();
```

## Trading Platform Tables

| Table | Purpose |
|-------|---------|
| `users` | User accounts |
| `trades` | Trade history |
| `signals` | Generated signals |
| `positions` | Open positions |
| `watchlists` | User watchlists |
