---
name: database
description: Design PostgreSQL schemas with migrations, seeding, and documentation. Use when creating tables, writing migrations, or setting up database structure.
allowed-tools: Read, Write, Edit, Glob, Grep
---

# Database Skill

Design and manage PostgreSQL databases following project conventions for schema design, migrations, seeding, and documentation.

---

## When to Use

- Creating database tables and schemas
- Writing migration files
- Designing indexes and constraints
- Setting up foreign key relationships
- Creating seed data for development
- Documenting database structure

---

## Project Structure

```
src/db/
├── client.js           # Database connection pool
├── migrations/         # Timestamped migration files
│   ├── 001_create_users.js
│   ├── 002_create_products.js
│   └── 003_add_user_roles.js
├── seeds/              # Development seed data
│   ├── 001_users.js
│   └── 002_products.js
├── queries/            # SQL query files
│   ├── users.js
│   └── products.js
└── schema.sql          # Full schema documentation
```

---

## Migration File Format

### Standard Migration

```javascript
// src/db/migrations/001_create_users.js

/**
 * Migration: Create users table
 * @param {import('pg').Pool} db - Database pool
 */
export async function up(db) {
  await db.query(`
    CREATE TABLE users (
      id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
      email VARCHAR(255) NOT NULL UNIQUE,
      name VARCHAR(255) NOT NULL,
      password_hash VARCHAR(255) NOT NULL,
      role VARCHAR(50) NOT NULL DEFAULT 'user',
      email_verified BOOLEAN NOT NULL DEFAULT FALSE,
      created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
      updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
    );

    CREATE INDEX idx_users_email ON users(email);
    CREATE INDEX idx_users_role ON users(role);

    COMMENT ON TABLE users IS 'Application users';
    COMMENT ON COLUMN users.role IS 'User role: user, admin, moderator';
  `);
}

/**
 * Rollback migration
 * @param {import('pg').Pool} db - Database pool
 */
export async function down(db) {
  await db.query(`DROP TABLE IF EXISTS users CASCADE`);
}

export const description = 'Create users table with auth fields';
```

### Migration with Foreign Keys

```javascript
// src/db/migrations/002_create_tasks.js

export async function up(db) {
  await db.query(`
    CREATE TABLE tasks (
      id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
      user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
      title VARCHAR(255) NOT NULL,
      description TEXT,
      status VARCHAR(50) NOT NULL DEFAULT 'pending',
      priority INTEGER NOT NULL DEFAULT 2,
      due_date DATE,
      created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
      updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

      CONSTRAINT chk_status CHECK (status IN ('pending', 'in_progress', 'completed', 'cancelled')),
      CONSTRAINT chk_priority CHECK (priority BETWEEN 0 AND 4)
    );

    CREATE INDEX idx_tasks_user_id ON tasks(user_id);
    CREATE INDEX idx_tasks_status ON tasks(status);
    CREATE INDEX idx_tasks_due_date ON tasks(due_date) WHERE due_date IS NOT NULL;

    COMMENT ON TABLE tasks IS 'User tasks and todos';
    COMMENT ON COLUMN tasks.priority IS '0=critical, 1=high, 2=medium, 3=low, 4=backlog';
  `);
}

export async function down(db) {
  await db.query(`DROP TABLE IF EXISTS tasks CASCADE`);
}

export const description = 'Create tasks table with user relationship';
```

---

## Migration Runner

```javascript
// src/db/migrate.js
import { db } from './client.js';
import { readdir } from 'fs/promises';
import { join } from 'path';

/**
 * Run pending migrations
 */
export async function migrate() {
  // Ensure migrations table exists
  await db.query(`
    CREATE TABLE IF NOT EXISTS migrations (
      id SERIAL PRIMARY KEY,
      name VARCHAR(255) NOT NULL UNIQUE,
      executed_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
    )
  `);

  // Get executed migrations
  const { rows: executed } = await db.query(
    'SELECT name FROM migrations ORDER BY id'
  );
  const executedNames = new Set(executed.map(r => r.name));

  // Get migration files
  const migrationsDir = new URL('./migrations', import.meta.url).pathname;
  const files = await readdir(migrationsDir);
  const migrations = files
    .filter(f => f.endsWith('.js'))
    .sort();

  // Run pending migrations
  for (const file of migrations) {
    if (executedNames.has(file)) continue;

    console.log(`Running migration: ${file}`);
    const migration = await import(join(migrationsDir, file));

    await db.query('BEGIN');
    try {
      await migration.up(db);
      await db.query(
        'INSERT INTO migrations (name) VALUES ($1)',
        [file]
      );
      await db.query('COMMIT');
      console.log(`  Completed: ${migration.description || file}`);
    } catch (error) {
      await db.query('ROLLBACK');
      console.error(`  Failed: ${error.message}`);
      throw error;
    }
  }

  console.log('All migrations complete');
}

/**
 * Rollback last migration
 */
export async function rollback() {
  const { rows } = await db.query(
    'SELECT name FROM migrations ORDER BY id DESC LIMIT 1'
  );

  if (rows.length === 0) {
    console.log('No migrations to rollback');
    return;
  }

  const file = rows[0].name;
  console.log(`Rolling back: ${file}`);

  const migrationsDir = new URL('./migrations', import.meta.url).pathname;
  const migration = await import(join(migrationsDir, file));

  await db.query('BEGIN');
  try {
    await migration.down(db);
    await db.query('DELETE FROM migrations WHERE name = $1', [file]);
    await db.query('COMMIT');
    console.log('Rollback complete');
  } catch (error) {
    await db.query('ROLLBACK');
    console.error(`Rollback failed: ${error.message}`);
    throw error;
  }
}
```

---

## Schema Design Patterns

### Primary Keys

```sql
-- UUID (recommended for distributed systems)
id UUID PRIMARY KEY DEFAULT gen_random_uuid()

-- Serial (simpler, sequential)
id SERIAL PRIMARY KEY

-- Composite key
PRIMARY KEY (user_id, product_id)
```

### Timestamps

```sql
-- Standard timestamps
created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()

-- With trigger for updated_at
CREATE OR REPLACE FUNCTION update_updated_at()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = NOW();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER set_updated_at
  BEFORE UPDATE ON users
  FOR EACH ROW
  EXECUTE FUNCTION update_updated_at();
```

### Soft Deletes

```sql
-- Soft delete column
deleted_at TIMESTAMPTZ DEFAULT NULL

-- Index for active records
CREATE INDEX idx_users_active ON users(id) WHERE deleted_at IS NULL;

-- Query pattern
SELECT * FROM users WHERE deleted_at IS NULL;
```

### JSON Columns

```sql
-- JSONB for structured data
metadata JSONB NOT NULL DEFAULT '{}',
settings JSONB NOT NULL DEFAULT '{}'

-- Index for JSON queries
CREATE INDEX idx_users_metadata ON users USING GIN (metadata);

-- Query JSON
SELECT * FROM users WHERE metadata->>'plan' = 'premium';
```

### Enums vs Check Constraints

```sql
-- Check constraint (preferred - easier to modify)
status VARCHAR(50) NOT NULL DEFAULT 'pending',
CONSTRAINT chk_status CHECK (status IN ('pending', 'active', 'completed'))

-- PostgreSQL enum (harder to modify, but type-safe)
CREATE TYPE task_status AS ENUM ('pending', 'active', 'completed');
status task_status NOT NULL DEFAULT 'pending'
```

---

## Indexes

### When to Create Indexes

```sql
-- Foreign keys (always index)
CREATE INDEX idx_tasks_user_id ON tasks(user_id);

-- Frequently queried columns
CREATE INDEX idx_users_email ON users(email);

-- Columns used in WHERE clauses
CREATE INDEX idx_tasks_status ON tasks(status);

-- Columns used in ORDER BY
CREATE INDEX idx_tasks_created_at ON tasks(created_at DESC);

-- Partial indexes (for filtered queries)
CREATE INDEX idx_tasks_pending ON tasks(due_date)
  WHERE status = 'pending';

-- Composite indexes (for multi-column queries)
CREATE INDEX idx_tasks_user_status ON tasks(user_id, status);
```

### Index Types

```sql
-- B-tree (default, most common)
CREATE INDEX idx_users_email ON users(email);

-- GIN (for JSONB, arrays, full-text)
CREATE INDEX idx_users_metadata ON users USING GIN (metadata);

-- GiST (for geometric, full-text)
CREATE INDEX idx_locations_coords ON locations USING GIST (coordinates);

-- Hash (for equality only, rarely used)
CREATE INDEX idx_sessions_token ON sessions USING HASH (token);
```

---

## Seed Data

### Seed File Format

```javascript
// src/db/seeds/001_users.js
import { faker } from '@faker-js/faker';

/**
 * Seed users table
 * @param {import('pg').Pool} db - Database pool
 */
export async function seed(db) {
  // Admin user (consistent for testing)
  await db.query(`
    INSERT INTO users (id, email, name, password_hash, role, email_verified)
    VALUES (
      '00000000-0000-0000-0000-000000000001',
      'admin@example.com',
      'Admin User',
      '$argon2id$v=19$m=65536,t=3,p=4$...',  -- 'password123'
      'admin',
      TRUE
    )
    ON CONFLICT (email) DO NOTHING
  `);

  // Generate fake users
  const users = Array.from({ length: 50 }, () => ({
    email: faker.internet.email(),
    name: faker.person.fullName(),
    password_hash: '$argon2id$v=19$m=65536,t=3,p=4$...',
    role: faker.helpers.arrayElement(['user', 'user', 'user', 'moderator']),
    email_verified: faker.datatype.boolean()
  }));

  for (const user of users) {
    await db.query(`
      INSERT INTO users (email, name, password_hash, role, email_verified)
      VALUES ($1, $2, $3, $4, $5)
      ON CONFLICT (email) DO NOTHING
    `, [user.email, user.name, user.password_hash, user.role, user.email_verified]);
  }

  console.log('Seeded 51 users');
}

export const description = 'Seed users with admin and fake data';
```

### Seed Runner

```javascript
// src/db/seed.js
import { db } from './client.js';
import { readdir } from 'fs/promises';
import { join } from 'path';

/**
 * Run all seed files
 */
export async function seed() {
  const seedsDir = new URL('./seeds', import.meta.url).pathname;
  const files = await readdir(seedsDir);
  const seeds = files
    .filter(f => f.endsWith('.js'))
    .sort();

  for (const file of seeds) {
    console.log(`Seeding: ${file}`);
    const seedModule = await import(join(seedsDir, file));
    await seedModule.seed(db);
  }

  console.log('All seeds complete');
}
```

---

## Schema Documentation (schema.sql)

```sql
-- schema.sql
-- Generated documentation of database structure
-- Do not run directly - use migrations

-- ============================================
-- USERS
-- ============================================
-- Application users with authentication data

CREATE TABLE users (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  email VARCHAR(255) NOT NULL UNIQUE,
  name VARCHAR(255) NOT NULL,
  password_hash VARCHAR(255) NOT NULL,
  role VARCHAR(50) NOT NULL DEFAULT 'user',  -- user, admin, moderator
  email_verified BOOLEAN NOT NULL DEFAULT FALSE,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Indexes
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_role ON users(role);

-- ============================================
-- TASKS
-- ============================================
-- User tasks with status tracking

CREATE TABLE tasks (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  title VARCHAR(255) NOT NULL,
  description TEXT,
  status VARCHAR(50) NOT NULL DEFAULT 'pending',
  priority INTEGER NOT NULL DEFAULT 2,  -- 0-4
  due_date DATE,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Constraints
ALTER TABLE tasks ADD CONSTRAINT chk_status
  CHECK (status IN ('pending', 'in_progress', 'completed', 'cancelled'));
ALTER TABLE tasks ADD CONSTRAINT chk_priority
  CHECK (priority BETWEEN 0 AND 4);

-- Indexes
CREATE INDEX idx_tasks_user_id ON tasks(user_id);
CREATE INDEX idx_tasks_status ON tasks(status);
CREATE INDEX idx_tasks_due_date ON tasks(due_date) WHERE due_date IS NOT NULL;
```

---

## Common Queries Pattern

```javascript
// src/db/queries/users.js

export const userQueries = {
  findById: `
    SELECT id, email, name, role, email_verified, created_at, updated_at
    FROM users
    WHERE id = $1 AND deleted_at IS NULL
  `,

  findByEmail: `
    SELECT id, email, name, role, password_hash, email_verified
    FROM users
    WHERE email = $1 AND deleted_at IS NULL
  `,

  create: `
    INSERT INTO users (email, name, password_hash)
    VALUES ($1, $2, $3)
    RETURNING id, email, name, role, created_at
  `,

  update: `
    UPDATE users
    SET name = COALESCE($2, name),
        email = COALESCE($3, email),
        updated_at = NOW()
    WHERE id = $1 AND deleted_at IS NULL
    RETURNING id, email, name, role, updated_at
  `,

  softDelete: `
    UPDATE users
    SET deleted_at = NOW()
    WHERE id = $1 AND deleted_at IS NULL
    RETURNING id
  `,

  list: `
    SELECT id, email, name, role, created_at
    FROM users
    WHERE deleted_at IS NULL
    ORDER BY created_at DESC
    LIMIT $1 OFFSET $2
  `,

  count: `
    SELECT COUNT(*) as total
    FROM users
    WHERE deleted_at IS NULL
  `
};
```

---

## Checklist

When designing databases:

- [ ] Use UUID or SERIAL for primary keys consistently
- [ ] Add created_at and updated_at timestamps
- [ ] Index all foreign key columns
- [ ] Index columns used in WHERE and ORDER BY
- [ ] Use check constraints for enums (easier than PostgreSQL ENUMs)
- [ ] Add comments to tables and important columns
- [ ] Write reversible migrations with up/down
- [ ] Include description in migration files
- [ ] Create seeds for admin/test users
- [ ] Use faker.js for realistic seed data
- [ ] Document schema in schema.sql
- [ ] Use TIMESTAMPTZ (not TIMESTAMP) for times
- [ ] Consider soft deletes for important data
- [ ] Use parameterized queries (prevent SQL injection)

## Related Skills

- **nodejs-backend** - Build Node.js backend services with Express/Fastify, Post...
- **rest-api** - Write REST API endpoints with HTTP methods, status codes,...
- **authentication** - Implement secure authentication with JWT, sessions, OAuth...
- **security** - Write secure web pages and applications
