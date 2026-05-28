---
name: sql-database-expert
description: Use this skill when you need expert-level knowledge in SQL database design, querying, optimization, and administration across multiple database systems like PostgreSQL, MySQL, and SQL Server.
---

# SQL Database Expert

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

-- Comments table
CREATE TABLE comments (
    id SERIAL PRIMARY KEY,
    post_id INTEGER NOT NULL REFERENCES posts(id) ON DELETE CASCADE,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    content TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tags table
CREATE TABLE tags (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL,
    slug VARCHAR(50) UNIQUE NOT NULL
);

CREATE TABLE post_tags (
    post_id INTEGER NOT NULL REFERENCES posts(id) ON DELETE CASCADE,
    tag_id INTEGER NOT NULL REFERENCES tags(id) ON DELETE CASCADE,
    PRIMARY KEY (post_id, tag_id)
);
```

### Query Optimization

- Use `EXPLAIN` to analyze query performance.
- Implement proper indexing strategies based on query patterns.
- Optimize data types to minimize storage and improve performance.

### Advanced Data Types

**PostgreSQL JSONB Example:**
```sql
CREATE TABLE events (
    id SERIAL PRIMARY KEY,
    event_type VARCHAR(50),
    data JSONB NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert JSON data
INSERT INTO events (event_type, data) VALUES
    ('user_signup', '{"email": "alice@example.com", "referrer": "google"}');

-- Query JSON
SELECT * FROM events WHERE data->>'email' = 'alice@example.com';
```

**MySQL Best Practices:**
- Use InnoDB as the default storage engine.
- Optimize queries using EXPLAIN and proper indexing.
- Use appropriate data types to minimize storage and improve performance.

### Indexing Strategies

- Use B-tree indexes for equality and range queries.
- Use GIN indexes for JSONB and array types in PostgreSQL.
- Consider partitioning for large tables to improve performance.

### Security and Administration

- Implement connection pooling and query caching.
- Follow security best practices specific to each database system.
- Regularly back up databases and monitor performance metrics.

This skill encompasses best practices and advanced techniques for managing SQL databases effectively across different platforms.