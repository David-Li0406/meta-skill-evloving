# Neon Serverless PostgreSQL Guide

Complete guide to working with Neon serverless PostgreSQL database.

## Setup and Connection

### Getting Started

1. Create account at https://neon.tech
2. Create a new project
3. Get connection string from dashboard

### Connection String Format

```
postgresql://[user]:[password]@[endpoint]/[database]?sslmode=require
```

### Environment Variables

```env
DATABASE_URL="postgresql://user:password@ep-xxx.us-east-2.aws.neon.tech/neondb?sslmode=require"
```

## Connection Patterns

### Node.js with pg

```javascript
const { Pool } = require('pg');

const pool = new Pool({
  connectionString: process.env.DATABASE_URL,
  ssl: { rejectUnauthorized: false }
});

// Query
async function getUsers() {
  const result = await pool.query('SELECT * FROM users');
  return result.rows;
}
```

### Node.js with Prisma

```prisma
// schema.prisma
datasource db {
  provider = "postgresql"
  url      = env("DATABASE_URL")
}

generator client {
  provider = "prisma-client-js"
}

model User {
  id    Int     @id @default(autoincrement())
  email String  @unique
  name  String?
}
```

```javascript
const { PrismaClient } = require('@prisma/client');
const prisma = new PrismaClient();

async function getUsers() {
  return await prisma.user.findMany();
}
```

### Python with psycopg2

```python
import psycopg2
import os

conn = psycopg2.connect(os.environ['DATABASE_URL'])
cur = conn.cursor()

cur.execute('SELECT * FROM users')
users = cur.fetchall()
```

### Python with SQLAlchemy

```python
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

engine = create_engine(os.environ['DATABASE_URL'])
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True)
    name = Column(String)

Base.metadata.create_all(engine)
```

## Schema Design

### Basic Table Creation

```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_users_email ON users(email);
```

### Relationships

```sql
-- One-to-Many
CREATE TABLE posts (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    title VARCHAR(255) NOT NULL,
    content TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_posts_user_id ON posts(user_id);

-- Many-to-Many
CREATE TABLE tags (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL
);

CREATE TABLE post_tags (
    post_id INTEGER REFERENCES posts(id) ON DELETE CASCADE,
    tag_id INTEGER REFERENCES tags(id) ON DELETE CASCADE,
    PRIMARY KEY (post_id, tag_id)
);
```

## CRUD Operations

### INSERT

```sql
-- Single insert
INSERT INTO users (email, name) VALUES ('user@example.com', 'John Doe');

-- Multiple inserts
INSERT INTO users (email, name) VALUES
    ('user1@example.com', 'User 1'),
    ('user2@example.com', 'User 2'),
    ('user3@example.com', 'User 3');

-- Insert and return
INSERT INTO users (email, name)
VALUES ('user@example.com', 'John Doe')
RETURNING id, email, created_at;
```

### SELECT

```sql
-- Basic select
SELECT * FROM users;

-- Select specific columns
SELECT id, email FROM users;

-- With WHERE clause
SELECT * FROM users WHERE email = 'user@example.com';

-- With LIKE
SELECT * FROM users WHERE name LIKE '%John%';

-- With ORDER BY
SELECT * FROM users ORDER BY created_at DESC;

-- With LIMIT and OFFSET (pagination)
SELECT * FROM users ORDER BY id LIMIT 10 OFFSET 20;

-- Joins
SELECT u.name, p.title
FROM users u
JOIN posts p ON u.id = p.user_id
WHERE u.email = 'user@example.com';
```

### UPDATE

```sql
-- Update single field
UPDATE users SET name = 'Jane Doe' WHERE id = 1;

-- Update multiple fields
UPDATE users
SET name = 'Jane Doe', updated_at = NOW()
WHERE id = 1;

-- Update with RETURNING
UPDATE users SET name = 'Jane Doe'
WHERE id = 1
RETURNING *;
```

### DELETE

```sql
-- Delete specific record
DELETE FROM users WHERE id = 1;

-- Delete with condition
DELETE FROM users WHERE created_at < NOW() - INTERVAL '1 year';

-- Delete with RETURNING
DELETE FROM users WHERE id = 1 RETURNING *;
```

## Advanced Queries

### Aggregations

```sql
-- Count
SELECT COUNT(*) FROM users;

-- Group by
SELECT user_id, COUNT(*) as post_count
FROM posts
GROUP BY user_id;

-- Having clause
SELECT user_id, COUNT(*) as post_count
FROM posts
GROUP BY user_id
HAVING COUNT(*) > 5;

-- Multiple aggregations
SELECT
    user_id,
    COUNT(*) as post_count,
    MAX(created_at) as latest_post,
    MIN(created_at) as first_post
FROM posts
GROUP BY user_id;
```

### Joins

```sql
-- INNER JOIN
SELECT u.name, p.title
FROM users u
INNER JOIN posts p ON u.id = p.user_id;

-- LEFT JOIN
SELECT u.name, COUNT(p.id) as post_count
FROM users u
LEFT JOIN posts p ON u.id = p.user_id
GROUP BY u.id, u.name;

-- Multiple joins
SELECT u.name, p.title, t.name as tag
FROM users u
JOIN posts p ON u.id = p.user_id
JOIN post_tags pt ON p.id = pt.post_id
JOIN tags t ON pt.tag_id = t.id;
```

### Subqueries

```sql
-- Subquery in WHERE
SELECT * FROM users
WHERE id IN (SELECT user_id FROM posts WHERE title LIKE '%important%');

-- Subquery in SELECT
SELECT
    u.name,
    (SELECT COUNT(*) FROM posts WHERE user_id = u.id) as post_count
FROM users u;
```

### CTEs (Common Table Expressions)

```sql
WITH active_users AS (
    SELECT user_id, COUNT(*) as post_count
    FROM posts
    WHERE created_at > NOW() - INTERVAL '30 days'
    GROUP BY user_id
)
SELECT u.name, au.post_count
FROM users u
JOIN active_users au ON u.id = au.user_id
ORDER BY au.post_count DESC;
```

## Transactions

```sql
BEGIN;

INSERT INTO users (email, name) VALUES ('user@example.com', 'John');
INSERT INTO posts (user_id, title) VALUES (1, 'My Post');

COMMIT;

-- With rollback
BEGIN;

INSERT INTO users (email, name) VALUES ('user@example.com', 'John');
-- Error occurs
ROLLBACK;
```

## Indexing

### Create Indexes

```sql
-- Single column index
CREATE INDEX idx_users_email ON users(email);

-- Unique index
CREATE UNIQUE INDEX idx_users_email_unique ON users(email);

-- Multi-column index
CREATE INDEX idx_posts_user_date ON posts(user_id, created_at);

-- Partial index
CREATE INDEX idx_active_users ON users(email) WHERE active = true;

-- Full-text search index
CREATE INDEX idx_posts_content_fts ON posts USING GIN(to_tsvector('english', content));
```

### Drop Indexes

```sql
DROP INDEX idx_users_email;
```

## Performance Optimization

### Query Analysis

```sql
-- Explain query plan
EXPLAIN SELECT * FROM users WHERE email = 'user@example.com';

-- Explain analyze (actually runs the query)
EXPLAIN ANALYZE SELECT * FROM users WHERE email = 'user@example.com';
```

### Connection Pooling

```javascript
// Node.js pg pool
const { Pool } = require('pg');

const pool = new Pool({
  connectionString: process.env.DATABASE_URL,
  max: 20, // max connections
  idleTimeoutMillis: 30000,
  connectionTimeoutMillis: 2000,
});
```

### Prepared Statements

```javascript
// Node.js
const result = await pool.query(
  'SELECT * FROM users WHERE email = $1',
  ['user@example.com']
);
```

```python
# Python psycopg2
cur.execute('SELECT * FROM users WHERE email = %s', ('user@example.com',))
```

## Neon-Specific Features

### Branching

Create database branches for development:

```bash
# Using Neon CLI
neon branches create --name dev --parent main
```

### Auto-Suspend

Neon automatically suspends inactive databases to save costs. No configuration needed.

### Serverless Benefits

- No connection limits
- Automatic scaling
- Pay only for storage and compute used
- Instant database provisioning

## Migrations

### Using Prisma Migrate

```bash
# Create migration
npx prisma migrate dev --name init

# Apply migrations
npx prisma migrate deploy
```

### Using raw SQL migrations

```sql
-- migrations/001_create_users.sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- migrations/002_add_posts.sql
CREATE TABLE posts (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    title VARCHAR(255) NOT NULL,
    content TEXT
);
```

## Best Practices

1. **Use connection pooling** - Don't create new connections per request
2. **Add indexes** - Index foreign keys and frequently queried columns
3. **Use prepared statements** - Prevent SQL injection and improve performance
4. **Limit result sets** - Use LIMIT and OFFSET for pagination
5. **Use transactions** - For operations that must succeed or fail together
6. **Monitor queries** - Use EXPLAIN ANALYZE to identify slow queries
7. **Normalize data** - Follow normalization rules for data integrity
8. **Use CASCADE** - For foreign key constraints to maintain referential integrity
9. **Set appropriate types** - Use correct data types (INTEGER vs BIGINT, VARCHAR vs TEXT)
10. **Backup regularly** - Neon provides automatic backups, but export important data

## Common Patterns

### Pagination

```sql
SELECT * FROM posts
ORDER BY created_at DESC
LIMIT 10 OFFSET 0;  -- Page 1

SELECT * FROM posts
ORDER BY created_at DESC
LIMIT 10 OFFSET 10; -- Page 2
```

### Search

```sql
-- Simple search
SELECT * FROM posts
WHERE title ILIKE '%search term%'
   OR content ILIKE '%search term%';

-- Full-text search
SELECT * FROM posts
WHERE to_tsvector('english', title || ' ' || content)
@@ to_tsquery('english', 'search & term');
```

### Soft Delete

```sql
ALTER TABLE users ADD COLUMN deleted_at TIMESTAMP;

-- Soft delete
UPDATE users SET deleted_at = NOW() WHERE id = 1;

-- Query active records
SELECT * FROM users WHERE deleted_at IS NULL;
```

### Audit Trail

```sql
CREATE TABLE audit_log (
    id SERIAL PRIMARY KEY,
    table_name VARCHAR(100),
    record_id INTEGER,
    action VARCHAR(50),
    old_data JSONB,
    new_data JSONB,
    user_id INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```
