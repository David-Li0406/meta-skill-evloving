---
name: database-specialist
description: Expert database design, queries, and optimization for both SQL (Neon serverless PostgreSQL) and NoSQL (MongoDB) databases. Use when designing database schemas, writing queries, creating migrations, optimizing performance, adding indexes, integrating with ORMs (Prisma/SQLAlchemy/Mongoose), modeling data relationships, or any database-related tasks including CRUD operations, joins, aggregations, transactions, and connection management.
---

# Database Specialist

Expert guidance for SQL (Neon PostgreSQL) and NoSQL (MongoDB) database development.

## Quick Start Workflow

1. **Choose database** - SQL (Neon PostgreSQL) or NoSQL (MongoDB)
2. **Design schema** - Define tables/collections, relationships, indexes
3. **Setup connection** - Configure connection strings and pooling
4. **Create migrations** - Version control schema changes
5. **Implement queries** - CRUD operations, joins, aggregations
6. **Optimize performance** - Add indexes, analyze queries
7. **Integrate with ORM** - Prisma, SQLAlchemy, or Mongoose

## Decision Tree

**What database are you using?**

**Neon PostgreSQL (SQL)**
- Setup → See [neon-postgres-guide.md](references/neon-postgres-guide.md) - Setup and Connection
- Schema design → See [neon-postgres-guide.md](references/neon-postgres-guide.md) - Schema Design
- Queries → See [neon-postgres-guide.md](references/neon-postgres-guide.md) - CRUD Operations
- Performance → See [neon-postgres-guide.md](references/neon-postgres-guide.md) - Performance Optimization

**MongoDB (NoSQL)**
- Setup → Connection patterns below
- Schema design → Document modeling below
- Queries → CRUD and aggregation below
- Performance → Indexing strategies below

## Installation

### Neon PostgreSQL

```bash
# Node.js
npm install pg
npm install prisma @prisma/client  # If using Prisma

# Python
pip install psycopg2-binary
pip install sqlalchemy  # If using SQLAlchemy
```

### MongoDB

```bash
# Node.js
npm install mongodb
npm install mongoose  # If using Mongoose

# Python
pip install pymongo
pip install motor  # For async
```

## Basic Patterns

### Pattern 1: Neon PostgreSQL with Prisma

```prisma
// schema.prisma
datasource db {
  provider = "postgresql"
  url      = env("DATABASE_URL")
}

model User {
  id        Int      @id @default(autoincrement())
  email     String   @unique
  name      String?
  posts     Post[]
  createdAt DateTime @default(now())
}

model Post {
  id        Int      @id @default(autoincrement())
  title     String
  content   String?
  authorId  Int
  author    User     @relation(fields: [authorId], references: [id])
  createdAt DateTime @default(now())
}
```

```javascript
const { PrismaClient } = require('@prisma/client');
const prisma = new PrismaClient();

// Create
await prisma.user.create({
  data: { email: 'user@example.com', name: 'John' }
});

// Read
const users = await prisma.user.findMany({
  include: { posts: true }
});

// Update
await prisma.user.update({
  where: { id: 1 },
  data: { name: 'Jane' }
});

// Delete
await prisma.user.delete({ where: { id: 1 } });
```

### Pattern 2: Neon PostgreSQL Raw SQL

```javascript
const { Pool } = require('pg');

const pool = new Pool({
  connectionString: process.env.DATABASE_URL,
  ssl: { rejectUnauthorized: false }
});

// Create
await pool.query(
  'INSERT INTO users (email, name) VALUES ($1, $2) RETURNING *',
  ['user@example.com', 'John']
);

// Read
const result = await pool.query('SELECT * FROM users WHERE email = $1', ['user@example.com']);

// Update
await pool.query('UPDATE users SET name = $1 WHERE id = $2', ['Jane', 1]);

// Delete
await pool.query('DELETE FROM users WHERE id = $1', [1]);
```

### Pattern 3: MongoDB with Mongoose

```javascript
const mongoose = require('mongoose');

await mongoose.connect(process.env.MONGODB_URI);

const userSchema = new mongoose.Schema({
  email: { type: String, required: true, unique: true },
  name: String,
  posts: [{ type: mongoose.Schema.Types.ObjectId, ref: 'Post' }],
  createdAt: { type: Date, default: Date.now }
});

const User = mongoose.model('User', userSchema);

// Create
const user = await User.create({
  email: 'user@example.com',
  name: 'John'
});

// Read
const users = await User.find().populate('posts');

// Update
await User.findByIdAndUpdate(userId, { name: 'Jane' });

// Delete
await User.findByIdAndDelete(userId);
```

### Pattern 4: MongoDB Raw Driver

```javascript
const { MongoClient } = require('mongodb');

const client = new MongoClient(process.env.MONGODB_URI);
await client.connect();
const db = client.db('mydb');
const users = db.collection('users');

// Create
const result = await users.insertOne({
  email: 'user@example.com',
  name: 'John',
  createdAt: new Date()
});

// Read
const user = await users.findOne({ email: 'user@example.com' });

// Update
await users.updateOne(
  { _id: userId },
  { $set: { name: 'Jane' } }
);

// Delete
await users.deleteOne({ _id: userId });
```

## Schema Design

### SQL (Neon PostgreSQL)

```sql
-- Users table
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Posts table (one-to-many relationship)
CREATE TABLE posts (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    title VARCHAR(255) NOT NULL,
    content TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes
CREATE INDEX idx_posts_user_id ON posts(user_id);
CREATE INDEX idx_users_email ON users(email);
```

### MongoDB

```javascript
// Users collection schema
{
  _id: ObjectId,
  email: String,  // indexed
  name: String,
  posts: [ObjectId],  // references to posts
  createdAt: Date
}

// Posts collection schema
{
  _id: ObjectId,
  userId: ObjectId,  // indexed
  title: String,
  content: String,
  createdAt: Date
}

// Create indexes
db.users.createIndex({ email: 1 }, { unique: true });
db.posts.createIndex({ userId: 1 });
```

## Common Queries

### Neon PostgreSQL

```sql
-- Join with aggregation
SELECT u.name, COUNT(p.id) as post_count
FROM users u
LEFT JOIN posts p ON u.id = p.user_id
GROUP BY u.id, u.name
HAVING COUNT(p.id) > 0;

-- Pagination
SELECT * FROM posts
ORDER BY created_at DESC
LIMIT 10 OFFSET 20;

-- Search
SELECT * FROM posts
WHERE title ILIKE '%search%' OR content ILIKE '%search%';

-- Transaction
BEGIN;
INSERT INTO users (email, name) VALUES ('user@example.com', 'John');
INSERT INTO posts (user_id, title) VALUES (1, 'My Post');
COMMIT;
```

### MongoDB

```javascript
// Aggregation pipeline
await db.collection('posts').aggregate([
  { $match: { userId: new ObjectId(userId) } },
  { $group: { _id: '$userId', count: { $sum: 1 } } },
  { $lookup: {
      from: 'users',
      localField: '_id',
      foreignField: '_id',
      as: 'user'
    }
  }
]);

// Pagination
await posts.find()
  .sort({ createdAt: -1 })
  .skip(20)
  .limit(10)
  .toArray();

// Search
await posts.find({
  $or: [
    { title: { $regex: 'search', $options: 'i' } },
    { content: { $regex: 'search', $options: 'i' } }
  ]
});

// Transaction
const session = client.startSession();
session.startTransaction();
try {
  await users.insertOne({ email: 'user@example.com' }, { session });
  await posts.insertOne({ userId, title: 'Post' }, { session });
  await session.commitTransaction();
} catch (error) {
  await session.abortTransaction();
  throw error;
} finally {
  session.endSession();
}
```

## Performance Optimization

### Indexing (SQL)

```sql
-- Single column index
CREATE INDEX idx_users_email ON users(email);

-- Multi-column index
CREATE INDEX idx_posts_user_date ON posts(user_id, created_at);

-- Partial index
CREATE INDEX idx_active_posts ON posts(user_id) WHERE published = true;

-- Analyze query
EXPLAIN ANALYZE SELECT * FROM posts WHERE user_id = 1;
```

### Indexing (MongoDB)

```javascript
// Single field index
db.users.createIndex({ email: 1 }, { unique: true });

// Compound index
db.posts.createIndex({ userId: 1, createdAt: -1 });

// Text index for search
db.posts.createIndex({ title: 'text', content: 'text' });

// Analyze query
db.posts.find({ userId: ObjectId(id) }).explain('executionStats');
```

### Connection Pooling

```javascript
// PostgreSQL pool
const pool = new Pool({
  connectionString: process.env.DATABASE_URL,
  max: 20,
  idleTimeoutMillis: 30000,
  connectionTimeoutMillis: 2000,
});

// MongoDB connection pool (automatic)
const client = new MongoClient(uri, {
  maxPoolSize: 50,
  minPoolSize: 10,
  maxIdleTimeMS: 30000
});
```

## Migrations

### Prisma Migrations

```bash
# Create migration
npx prisma migrate dev --name add_posts_table

# Apply migrations
npx prisma migrate deploy

# Reset database
npx prisma migrate reset
```

### SQL Migrations

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
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    title VARCHAR(255) NOT NULL,
    content TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## Environment Variables

```env
# Neon PostgreSQL
DATABASE_URL="postgresql://user:password@ep-xxx.neon.tech/dbname?sslmode=require"

# MongoDB
MONGODB_URI="mongodb+srv://user:password@cluster.mongodb.net/dbname"
```

## Reference Files

- **[neon-postgres-guide.md](references/neon-postgres-guide.md)** - Complete Neon PostgreSQL guide with setup, queries, optimization, transactions, and best practices

## Best Practices

### General
1. **Use connection pooling** - Reuse connections
2. **Add indexes** - Index foreign keys and frequently queried fields
3. **Use prepared statements** - Prevent SQL injection
4. **Normalize data** - Avoid data duplication (SQL)
5. **Denormalize when needed** - For read performance (MongoDB)
6. **Use transactions** - For operations that must succeed/fail together
7. **Monitor queries** - Use EXPLAIN/explain() to find slow queries
8. **Backup regularly** - Automate database backups

### SQL-Specific
- Use foreign key constraints with CASCADE
- Create indexes on join columns
- Use appropriate data types (INTEGER vs BIGINT, VARCHAR vs TEXT)
- Avoid SELECT * in production
- Use LIMIT for large result sets

### MongoDB-Specific
- Embed related data for one-to-few relationships
- Reference for one-to-many or many-to-many
- Use projection to limit returned fields
- Create indexes before querying
- Use aggregation pipeline for complex queries

## Common Patterns

### Pagination (SQL)

```sql
-- Page 1 (skip 0, limit 10)
SELECT * FROM posts ORDER BY created_at DESC LIMIT 10 OFFSET 0;

-- Page 2 (skip 10, limit 10)
SELECT * FROM posts ORDER BY created_at DESC LIMIT 10 OFFSET 10;
```

### Pagination (MongoDB)

```javascript
const page = 1;
const limit = 10;
const skip = (page - 1) * limit;

const posts = await db.collection('posts')
  .find()
  .sort({ createdAt: -1 })
  .skip(skip)
  .limit(limit)
  .toArray();
```

### Search (SQL)

```sql
-- Case-insensitive search
SELECT * FROM posts
WHERE title ILIKE '%search%' OR content ILIKE '%search%';

-- Full-text search
SELECT * FROM posts
WHERE to_tsvector('english', title || ' ' || content)
@@ to_tsquery('english', 'search & term');
```

### Search (MongoDB)

```javascript
// Regex search
await posts.find({
  $or: [
    { title: { $regex: 'search', $options: 'i' } },
    { content: { $regex: 'search', $options: 'i' } }
  ]
});

// Text search (requires text index)
await posts.find({ $text: { $search: 'search term' } });
```

## Example Workflow

User request: "Design a database for a blog with users, posts, and comments"

### SQL (Neon PostgreSQL) Approach

1. **Design schema**
   ```sql
   CREATE TABLE users (
       id SERIAL PRIMARY KEY,
       email VARCHAR(255) UNIQUE NOT NULL,
       name VARCHAR(255),
       created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
   );

   CREATE TABLE posts (
       id SERIAL PRIMARY KEY,
       user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
       title VARCHAR(255) NOT NULL,
       content TEXT,
       created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
   );

   CREATE TABLE comments (
       id SERIAL PRIMARY KEY,
       post_id INTEGER REFERENCES posts(id) ON DELETE CASCADE,
       user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
       content TEXT NOT NULL,
       created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
   );
   ```

2. **Add indexes**
   ```sql
   CREATE INDEX idx_posts_user_id ON posts(user_id);
   CREATE INDEX idx_comments_post_id ON comments(post_id);
   CREATE INDEX idx_comments_user_id ON comments(user_id);
   ```

3. **Create with Prisma**
   ```bash
   npx prisma migrate dev --name init
   ```

### MongoDB Approach

1. **Design collections**
   ```javascript
   // users collection
   {
     _id: ObjectId,
     email: String,
     name: String,
     createdAt: Date
   }

   // posts collection (embedded comments for performance)
   {
     _id: ObjectId,
     userId: ObjectId,
     title: String,
     content: String,
     comments: [
       {
         userId: ObjectId,
         content: String,
         createdAt: Date
       }
     ],
     createdAt: Date
   }
   ```

2. **Create indexes**
   ```javascript
   db.users.createIndex({ email: 1 }, { unique: true });
   db.posts.createIndex({ userId: 1 });
   db.posts.createIndex({ createdAt: -1 });
   ```

Result: Fully designed database schema with relationships and indexes optimized for queries.
