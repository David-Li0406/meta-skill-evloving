# Database Patterns

## Schema Design

### Standard Columns

```sql
CREATE TABLE users (
  id            SERIAL PRIMARY KEY,          -- Internal ID
  public_id     UUID DEFAULT gen_random_uuid(), -- Public API ID
  email         VARCHAR(255) NOT NULL UNIQUE,
  name          VARCHAR(100) NOT NULL,
  created_at    TIMESTAMPTZ DEFAULT NOW(),
  updated_at    TIMESTAMPTZ DEFAULT NOW(),
  deleted_at    TIMESTAMPTZ                  -- Soft delete
);

CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_public_id ON users(public_id);
```

### Naming Conventions

```
Tables: plural, snake_case (users, order_items)
Columns: snake_case (created_at, user_id)
Foreign keys: singular_table_id (user_id, order_id)
Indexes: idx_table_column (idx_users_email)
```

### Relationships

```sql
-- One-to-Many
CREATE TABLE posts (
  id SERIAL PRIMARY KEY,
  user_id INTEGER REFERENCES users(id) ON DELETE CASCADE
);

-- Many-to-Many
CREATE TABLE user_roles (
  user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
  role_id INTEGER REFERENCES roles(id) ON DELETE CASCADE,
  PRIMARY KEY (user_id, role_id)
);
```

## Migrations

```
migrations/
├── 001_create_users.sql
├── 002_add_users_avatar.sql
├── 003_create_posts.sql
└── ...

Rules:
├─ Never edit applied migrations
├─ One logical change per migration
├─ Include both UP and DOWN
├─ Test rollback locally
└─ Run in transaction when possible
```

### Migration Template

```sql
-- 003_create_posts.sql

-- UP
CREATE TABLE posts (
  id SERIAL PRIMARY KEY,
  user_id INTEGER NOT NULL REFERENCES users(id),
  title VARCHAR(255) NOT NULL,
  body TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_posts_user_id ON posts(user_id);

-- DOWN
DROP TABLE posts;
```

## Query Optimization

### Indexes

```sql
-- Add indexes for:
WHERE clauses:     CREATE INDEX idx_orders_status ON orders(status);
JOIN columns:      CREATE INDEX idx_posts_user_id ON posts(user_id);
ORDER BY:          CREATE INDEX idx_posts_created ON posts(created_at DESC);
Composite:         CREATE INDEX idx_orders_user_status ON orders(user_id, status);
```

### N+1 Prevention

```python
# BAD: N+1 queries
users = User.all()
for user in users:
    print(user.posts)  # Query per user!

# GOOD: Eager load
users = User.all().prefetch_related('posts')
```

### Pagination

```sql
-- Offset (simple, slow for large offsets)
SELECT * FROM posts ORDER BY id LIMIT 20 OFFSET 100;

-- Cursor (faster, stable)
SELECT * FROM posts
WHERE id > :last_id
ORDER BY id
LIMIT 20;
```

## Connection Pooling

```
Pool settings:
├─ min_connections: 2-5
├─ max_connections: 10-20 (per process)
├─ idle_timeout: 300s
└─ max_lifetime: 1800s

Formula: max_connections = (core_count * 2) + effective_spindle_count
```

## Transactions

```python
# Python (SQLAlchemy)
with session.begin():
    user = User(name="John")
    session.add(user)
    # Auto-commit on exit, rollback on exception

# Explicit
try:
    session.begin()
    # ... operations
    session.commit()
except:
    session.rollback()
    raise
```

### Isolation Levels

| Level | Dirty Read | Non-repeatable | Phantom |
|-------|------------|----------------|---------|
| Read Uncommitted | Yes | Yes | Yes |
| Read Committed | No | Yes | Yes |
| Repeatable Read | No | No | Yes |
| Serializable | No | No | No |

Default: Read Committed (PostgreSQL) or Repeatable Read (MySQL)

## Backup & Recovery

```
Strategy:
├─ Full backup: daily
├─ WAL/binlog: continuous (point-in-time recovery)
├─ Test restore: monthly
└─ Offsite copy: always
```
