# Database Provider Detection Patterns

This reference documents how to detect database providers and their associated ORMs.

## Provider Detection

### Supabase (Priority - MCP Available)

**Detection:**
```bash
# In package.json dependencies
"@supabase/supabase-js"
"@supabase/ssr"
"@supabase/auth-helpers-nextjs"

# Environment variables
SUPABASE_URL or NEXT_PUBLIC_SUPABASE_URL
SUPABASE_ANON_KEY or NEXT_PUBLIC_SUPABASE_ANON_KEY

# Config files
supabase/config.toml
```

**MCP Integration:**
- Tool prefix: `mcp__supabase__*`
- Available operations: tables, columns, query, execute
- Enables real-time schema validation

**Schema Source:** `mcp` (direct query) or `supabase/migrations/`

---

### Firebase

**Detection:**
```bash
# In package.json dependencies
"firebase"
"firebase-admin"
"@firebase/firestore"

# Config files
firebase.json
.firebaserc
```

**Schema Source:** `manual` (Firestore is schemaless)

---

### Prisma

**Detection:**
```bash
# In package.json dependencies
"@prisma/client"
"prisma"

# Directory/file existence
prisma/
prisma/schema.prisma
```

**Schema Source:** `prisma/schema.prisma`

**Type Generation:** `npx prisma generate`

---

### Drizzle

**Detection:**
```bash
# In package.json dependencies
"drizzle-orm"
"drizzle-kit"

# Config files
drizzle.config.ts
drizzle.config.js

# Common schema locations
src/db/schema.ts
drizzle/schema.ts
```

**Schema Source:** TypeScript schema file (detect via config)

**Type Generation:** Built-in (TypeScript)

---

### PlanetScale

**Detection:**
```bash
# In package.json dependencies
"@planetscale/database"

# Config files
.pscale.yml
```

**Schema Source:** Usually paired with Prisma or Drizzle

---

### Neon

**Detection:**
```bash
# In package.json dependencies
"@neondatabase/serverless"
"@neondatabase/neon-http"

# Environment variables
DATABASE_URL containing "neon"
```

**Schema Source:** Usually paired with Prisma or Drizzle

---

### MongoDB

**Detection:**
```bash
# In package.json dependencies
"mongodb"
"mongoose"

# In pyproject.toml
"pymongo"
"motor"
"mongoengine"
```

**Schema Source:** `manual` (schemaless) or Mongoose schemas

---

### PostgreSQL (Direct)

**Detection:**
```bash
# In package.json dependencies
"pg"
"postgres"
"@vercel/postgres"

# In pyproject.toml
"psycopg2"
"asyncpg"
```

**Schema Source:** SQL migrations or ORM

---

### MySQL

**Detection:**
```bash
# In package.json dependencies
"mysql2"
"mysql"

# In pyproject.toml
"mysql-connector-python"
"aiomysql"
```

**Schema Source:** SQL migrations or ORM

---

### SQLite

**Detection:**
```bash
# In package.json dependencies
"better-sqlite3"
"sql.js"
"sqlite3"

# File existence
*.db
*.sqlite
*.sqlite3
```

**Schema Source:** Embedded, usually with ORM

---

## ORM Detection

| ORM | Detection | Language |
|-----|-----------|----------|
| Prisma | `@prisma/client` in deps | JS/TS |
| Drizzle | `drizzle-orm` in deps | JS/TS |
| TypeORM | `typeorm` in deps | JS/TS |
| Mongoose | `mongoose` in deps | JS/TS |
| Kysely | `kysely` in deps | JS/TS |
| SQLAlchemy | `sqlalchemy` in pyproject | Python |
| Django ORM | `django` in pyproject | Python |
| Tortoise | `tortoise-orm` in pyproject | Python |
| GORM | `gorm.io/gorm` in go.mod | Go |
| Diesel | `diesel` in Cargo.toml | Rust |
| SeaORM | `sea-orm` in Cargo.toml | Rust |

---

## MCP Availability Matrix

| Provider | MCP Available | Tool Prefix |
|----------|---------------|-------------|
| Supabase | ✅ Yes | `mcp__supabase__*` |
| Firebase | ❌ No | - |
| PlanetScale | ❌ No | - |
| Neon | ❌ No | - |
| MongoDB | ❌ No | - |
| PostgreSQL | ⚠️ Generic | `mcp__postgres__*` |

**Note:** MCP availability enables:
- Real-time schema queries
- Type mismatch detection
- RLS policy verification (Supabase)
- Migration status checking

---

## Profile Output Example

```yaml
database:
  provider: supabase
  orm: none  # Supabase client is not an ORM
  mcp_available: true
  schema_source: mcp
  config_path: .env.local
```

```yaml
database:
  provider: postgres
  orm: prisma
  mcp_available: false
  schema_source: prisma/schema.prisma
  config_path: .env
```

```yaml
database:
  provider: mongodb
  orm: mongoose
  mcp_available: false
  schema_source: manual
  config_path: .env
```
