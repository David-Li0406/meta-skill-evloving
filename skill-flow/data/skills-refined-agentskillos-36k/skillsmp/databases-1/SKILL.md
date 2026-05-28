---
name: databases
description: Work with MongoDB (document database, BSON documents, aggregation pipelines, Atlas cloud) and PostgreSQL (relational database, SQL queries, psql CLI, pgAdmin). Use when designing database schemas, writing queries and aggregations, optimizing indexes for performance, performing database migrations, configuring replication and sharding, implementing backup and restore strategies, managing database users and permissions, analyzing query performance, or administering production databases.
license: MIT
---

# Databases Skill

Unified guide for working with MongoDB (document-oriented) and PostgreSQL (relational) databases. Choose the right database for your use case and master both systems.

<triggers>
<trigger>Designing database schemas and data models</trigger>
<trigger>Writing queries (SQL or MongoDB query language)</trigger>
<trigger>Building aggregation pipelines or complex joins</trigger>
<trigger>Optimizing indexes and query performance</trigger>
<trigger>Implementing database migrations</trigger>
<trigger>Setting up replication, sharding, or clustering</trigger>
<trigger>Configuring backups and disaster recovery</trigger>
<trigger>Managing database users and permissions</trigger>
<trigger>Analyzing slow queries and performance issues</trigger>
<trigger>Administering production database deployments</trigger>
</triggers>

## Database Selection Guide

### Choose MongoDB When:
- Schema flexibility: frequent structure changes, heterogeneous data
- Document-centric: natural JSON/BSON data model
- Horizontal scaling: need to shard across multiple servers
- High write throughput: IoT, logging, real-time analytics
- Nested/hierarchical data: embedded documents preferred
- Rapid prototyping: schema evolution without migrations

**Best for:** Content management, catalogs, IoT time series, real-time analytics, mobile apps, user profiles

### Choose PostgreSQL When:
- Strong consistency: ACID transactions critical
- Complex relationships: many-to-many joins, referential integrity
- SQL requirement: team expertise, reporting tools, BI systems
- Data integrity: strict schema validation, constraints
- Mature ecosystem: extensive tooling, extensions
- Complex queries: window functions, CTEs, analytical workloads

**Best for:** Financial systems, e-commerce transactions, ERP, CRM, data warehousing, analytics

### Both Support:
- JSON/JSONB storage and querying
- Full-text search capabilities
- Geospatial queries and indexing
- Replication and high availability
- ACID transactions (MongoDB 4.0+)
- Strong security features

## Quick Start

### MongoDB Setup

<example type="usage">
<code language="bash">
# Atlas (Cloud) - Recommended
# 1. Sign up at mongodb.com/atlas
# 2. Create M0 free cluster
# 3. Get connection string

# Connection
mongodb+srv://user:pass@cluster.mongodb.net/db

# Shell
mongosh "mongodb+srv://cluster.mongodb.net/mydb"

# Basic operations
db.users.insertOne({ name: "Alice", age: 30 })
db.users.find({ age: { $gte: 18 } })
db.users.updateOne({ name: "Alice" }, { $set: { age: 31 } })
db.users.deleteOne({ name: "Alice" })
</code>
</example>

### PostgreSQL Setup

<example type="usage">
<code language="bash">
# Ubuntu/Debian
sudo apt-get install postgresql postgresql-contrib

# Start service
sudo systemctl start postgresql

# Connect
psql -U postgres -d mydb

# Basic operations
CREATE TABLE users (id SERIAL PRIMARY KEY, name TEXT, age INT);
INSERT INTO users (name, age) VALUES ('Alice', 30);
SELECT * FROM users WHERE age >= 18;
UPDATE users SET age = 31 WHERE name = 'Alice';
DELETE FROM users WHERE name = 'Alice';
</code>
</example>

## Common Operations

### Create/Insert

<example type="usage">
<code language="javascript">
// MongoDB
db.users.insertOne({ name: "Bob", email: "bob@example.com" })
db.users.insertMany([{ name: "Alice" }, { name: "Charlie" }])
</code>
</example>

<example type="usage">
<code language="sql">
-- PostgreSQL
INSERT INTO users (name, email) VALUES ('Bob', 'bob@example.com');
INSERT INTO users (name, email) VALUES ('Alice', NULL), ('Charlie', NULL);
</code>
</example>

### Read/Query

<example type="usage">
<code language="javascript">
// MongoDB
db.users.find({ age: { $gte: 18 } })
db.users.findOne({ email: "bob@example.com" })
</code>
</example>

<example type="usage">
<code language="sql">
-- PostgreSQL
SELECT * FROM users WHERE age >= 18;
SELECT * FROM users WHERE email = 'bob@example.com' LIMIT 1;
</code>
</example>

### Update

<example type="usage">
<code language="javascript">
// MongoDB
db.users.updateOne({ name: "Bob" }, { $set: { age: 25 } })
db.users.updateMany({ status: "pending" }, { $set: { status: "active" } })
</code>
</example>

<example type="usage">
<code language="sql">
-- PostgreSQL
UPDATE users SET age = 25 WHERE name = 'Bob';
UPDATE users SET status = 'active' WHERE status = 'pending';
</code>
</example>

### Delete

<example type="usage">
<code language="javascript">
// MongoDB
db.users.deleteOne({ name: "Bob" })
db.users.deleteMany({ status: "deleted" })
</code>
</example>

<example type="usage">
<code language="sql">
-- PostgreSQL
DELETE FROM users WHERE name = 'Bob';
DELETE FROM users WHERE status = 'deleted';
</code>
</example>

### Indexing

<example type="usage">
<code language="javascript">
// MongoDB
db.users.createIndex({ email: 1 })
db.users.createIndex({ status: 1, createdAt: -1 })
</code>
</example>

<example type="usage">
<code language="sql">
-- PostgreSQL
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_status_created ON users(status, created_at DESC);
</code>
</example>

## Reference Navigation

### MongoDB References
- **[mongodb-crud.md](references/mongodb-crud.md)** - CRUD operations, query operators, atomic updates
- **[mongodb-aggregation.md](references/mongodb-aggregation.md)** - Aggregation pipeline, stages, operators, patterns
- **[mongodb-indexing.md](references/mongodb-indexing.md)** - Index types, compound indexes, performance optimization
- **[mongodb-atlas.md](references/mongodb-atlas.md)** - Atlas cloud setup, clusters, monitoring, search

### PostgreSQL References
- **[postgresql-queries.md](references/postgresql-queries.md)** - SELECT, JOINs, subqueries, CTEs, window functions
- **[postgresql-psql-cli.md](references/postgresql-psql-cli.md)** - psql commands, meta-commands, scripting
- **[postgresql-performance.md](references/postgresql-performance.md)** - EXPLAIN, query optimization, vacuum, indexes
- **[postgresql-administration.md](references/postgresql-administration.md)** - User management, backups, replication, maintenance

## Python Utilities

Database utility scripts in `scripts/`:
- **db_migrate.py** - Generate and apply migrations for both databases
- **db_backup.py** - Backup and restore MongoDB and PostgreSQL
- **db_performance_check.py** - Analyze slow queries and recommend indexes

<example type="usage">
<code language="bash">
# Generate migration
python scripts/db_migrate.py --db mongodb --generate "add_user_index"

# Run backup
python scripts/db_backup.py --db postgres --output /backups/

# Check performance
python scripts/db_performance_check.py --db mongodb --threshold 100ms
</code>
</example>

## Key Differences Summary

| Feature | MongoDB | PostgreSQL |
|---------|---------|------------|
| Data Model | Document (JSON/BSON) | Relational (Tables/Rows) |
| Schema | Flexible, dynamic | Strict, predefined |
| Query Language | MongoDB Query Language | SQL |
| Joins | $lookup (limited) | Native, optimized |
| Transactions | Multi-document (4.0+) | Native ACID |
| Scaling | Horizontal (sharding) | Vertical (primary), Horizontal (extensions) |
| Indexes | Single, compound, text, geo, etc | B-tree, hash, GiST, GIN, etc |

## Best Practices

**MongoDB:**
- Use embedded documents for 1-to-few relationships
- Reference documents for 1-to-many or many-to-many
- Index frequently queried fields
- Use aggregation pipeline for complex transformations
- Enable authentication and TLS in production
- Use Atlas for managed hosting

**PostgreSQL:**
- Normalize schema to 3NF, denormalize for performance
- Use foreign keys for referential integrity
- Index foreign keys and frequently filtered columns
- Use EXPLAIN ANALYZE to optimize queries
- Regular VACUUM and ANALYZE maintenance
- Connection pooling (pgBouncer) for web apps

<constraints>
<constraint severity="critical">Always enable authentication in production databases</constraint>
<constraint severity="critical">Never expose database ports directly to the internet</constraint>
<constraint severity="high">Always use TLS/SSL for database connections in production</constraint>
<constraint severity="high">Implement automated backups with tested restore procedures</constraint>
<constraint severity="medium">Index foreign keys in PostgreSQL to prevent full table scans on joins</constraint>
<constraint severity="medium">MongoDB $lookup has performance limitations - consider denormalization for frequent joins</constraint>
</constraints>

## Resources

- MongoDB: https://www.mongodb.com/docs/
- PostgreSQL: https://www.postgresql.org/docs/
- MongoDB University: https://learn.mongodb.com/
- PostgreSQL Tutorial: https://www.postgresqltutorial.com/
