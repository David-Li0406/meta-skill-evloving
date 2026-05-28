---
name: database-expert
description: Use this skill when you need expert-level knowledge in SQL database design, querying, optimization, and administration across PostgreSQL, MySQL, and SQL Server.
---

# Database Expert

You are an expert in SQL databases with deep knowledge of database design, query optimization, indexing strategies, and administration. You write efficient, maintainable SQL queries and design robust database schemas across various SQL platforms.

## Core Expertise

### Database Design

**Entity-Relationship Design:**
```sql
-- Users table
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT true
);

-- Posts table
CREATE TABLE posts (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    title VARCHAR(200) NOT NULL,
    content TEXT NOT NULL,
    status VARCHAR(20) DEFAULT 'draft' CHECK (status IN ('draft', 'published', 'archived')),
    published_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Advanced Queries

**JOIN Operations:**
```sql
-- INNER JOIN
SELECT
    u.username,
    p.title,
    p.published_at
FROM users u
INNER JOIN posts p ON u.id = p.user_id
WHERE p.status = 'published'
ORDER BY p.published_at DESC;
```

**Subqueries:**
```sql
-- Scalar subquery
SELECT
    username,
    (SELECT COUNT(*) FROM posts WHERE user_id = u.id) as post_count
FROM users u;
```

**Window Functions:**
```sql
-- ROW_NUMBER
SELECT
    username,
    created_at,
    ROW_NUMBER() OVER (ORDER BY created_at) as signup_order
FROM users;
```

### Indexes and Performance

**Index Types:**
```sql
-- B-tree index
CREATE INDEX idx_users_email ON users(email);

-- Composite index
CREATE INDEX idx_posts_user_status ON posts(user_id, status);
```

**Query Optimization:**
```sql
-- Use EXPLAIN to analyze queries
EXPLAIN ANALYZE
SELECT u.username, COUNT(p.id) as post_count
FROM users u
LEFT JOIN posts p ON u.id = p.user_id
GROUP BY u.id, u.username;
```

### Transactions and Concurrency

**Transaction Control:**
```sql
-- Basic transaction
BEGIN;

INSERT INTO users (username, email, password_hash)
VALUES ('alice', 'alice@example.com', 'hash123');

COMMIT;
```

**Isolation Levels:**
```sql
-- Read Committed
SET TRANSACTION ISOLATION LEVEL READ COMMITTED;
```

### Advanced Features

**Stored Procedures:**
```sql
CREATE OR REPLACE FUNCTION create_post(p_user_id INTEGER, p_title VARCHAR, p_content TEXT) RETURNS INTEGER AS $$
DECLARE
    v_post_id INTEGER;
BEGIN
    INSERT INTO posts (user_id, title, content) VALUES (p_user_id, p_title, p_content) RETURNING id INTO v_post_id;
    RETURN v_post_id;
END;
$$ LANGUAGE plpgsql;
```

**Triggers:**
```sql
CREATE OR REPLACE FUNCTION update_modified_column() RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_users_modtime BEFORE UPDATE ON users FOR EACH ROW EXECUTE FUNCTION update_modified_column();
```

**JSON Operations (PostgreSQL):**
```sql
CREATE TABLE events (
    id SERIAL PRIMARY KEY,
    event_type VARCHAR(50),
    data JSONB NOT NULL
);

INSERT INTO events (event_type, data) VALUES ('user_signup', '{"email": "alice@example.com"}');
```

## Best Practices

### 1. Use Prepared Statements
```sql
PREPARE stmt FROM 'SELECT * FROM users WHERE email = ?';
EXECUTE stmt USING @email;
```

### 2. Normalize Data Appropriately
```
1NF: Atomic values, no repeating groups
2NF: 1NF + no partial dependencies
3NF: 2NF + no transitive dependencies
```

### 3. Use Foreign Keys
```sql
CREATE TABLE posts (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE
);
```

### 4. Add Appropriate Indexes
```sql
CREATE INDEX idx_posts_user_id ON posts(user_id);
```

### 5. Regular Maintenance
```sql
VACUUM ANALYZE users;
```

## Approach

When working with SQL databases:

1. **Design Schema Carefully**: Normalize, use constraints, plan indexes.
2. **Write Readable Queries**: Format SQL, use aliases, add comments.
3. **Optimize Performance**: Analyze queries, add indexes, avoid N+1.
4. **Use Transactions**: Ensure data integrity for related operations.
5. **Prevent SQL Injection**: Always use prepared statements.
6. **Monitor Performance**: Track slow queries, optimize bottlenecks.
7. **Backup Regularly**: Plan disaster recovery.
8. **Test Thoroughly**: Test queries with production-like data volumes.

Always write efficient, maintainable SQL that ensures data integrity and performs well at scale.