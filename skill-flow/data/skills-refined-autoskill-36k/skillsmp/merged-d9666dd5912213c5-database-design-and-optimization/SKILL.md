---
name: database-design-and-optimization
description: Use this skill for designing and optimizing database schemas for both SQL and NoSQL databases, including migrations and indexing strategies.
---

# Database Design and Optimization

## Overview

This skill provides comprehensive guidance for designing robust, scalable, and maintainable database schemas for both relational (SQL) and NoSQL databases, from conceptual modeling to physical implementation.

## When to Use This Skill

- **New Projects**: Designing a database schema for a new application.
- **Schema Refactoring**: Redesigning existing schemas for performance or scalability.
- **Relationship Definition**: Implementing 1:1, 1:N, and N:M relationships between tables.
- **Migrations**: Safely applying schema changes.
- **Performance Issues**: Optimizing queries and indexing strategies.

## Input Format

### Required Information
- **Database Type**: PostgreSQL, MySQL, MongoDB, etc.
- **Domain Description**: What data will be stored (e.g., e-commerce, blog).
- **Key Entities**: Core data objects (e.g., User, Product, Order).

### Optional Information
- **Expected Data Volume**: Small (<10K rows), Medium (10K-1M), Large (>1M).
- **Read/Write Ratio**: Read-heavy, Write-heavy, Balanced.
- **Transaction Requirements**: ACID compliance.
- **Sharding/Partitioning**: Need for distributed data.

## Design Workflow

1. **Entity and Attribute Definition**
   - Identify core data objects and their attributes.
   - Determine data types and primary keys.

2. **Relationship Design and Normalization**
   - Define relationships between tables and apply normalization (up to 3NF for OLTP systems).

3. **Index Strategy Development**
   - Design indexes for frequently queried columns and foreign keys.

4. **Constraints and Triggers Setup**
   - Add constraints for data integrity and triggers for automatic updates.

5. **Migration Script Creation**
   - Write migration scripts for applying schema changes safely.

## Core Principles

- **Normalization**: Start normalized, denormalize only when necessary for performance.
- **Indexing**: Index strategically based on actual query patterns.
- **Data Integrity**: Use constraints to enforce data integrity at the database level.
- **Documentation**: Document design decisions and their rationale.

## Example Schema Design

### Basic E-commerce Schema

```sql
-- Users table
CREATE TABLE users (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  email VARCHAR(255) UNIQUE NOT NULL,
  password_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);

-- Products table
CREATE TABLE products (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name VARCHAR(255) NOT NULL,
  description TEXT,
  price DECIMAL(10,2) NOT NULL CHECK (price >= 0),
  stock_quantity INTEGER DEFAULT 0,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);

-- Orders table
CREATE TABLE orders (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  total_amount DECIMAL(10,2) NOT NULL,
  status VARCHAR(50) DEFAULT 'pending',
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);
```

## Indexing Strategies

### Common Index Patterns

```sql
-- Single-column index
CREATE INDEX idx_users_email ON users(email);

-- Composite index
CREATE INDEX idx_orders_user_status ON orders(user_id, status);

-- Partial index
CREATE INDEX idx_active_users ON users(email) WHERE deleted_at IS NULL;
```

## Migration Patterns

### Safe Migration Template

```sql
BEGIN;

ALTER TABLE users ADD COLUMN status VARCHAR(20) DEFAULT 'active';
CREATE INDEX CONCURRENTLY idx_users_status ON users(status);

COMMIT;
```

## Best Practices

1. **Consistent Naming Conventions**: Use snake_case for table and column names.
2. **Soft Deletes**: Implement soft deletes using a `deleted_at` timestamp.
3. **Timestamps**: Include `created_at` and `updated_at` in most tables.
4. **Transaction Management**: Use transactions for schema changes to prevent data loss.

## Common Issues

### N+1 Query Problem

**Symptoms**: Multiple database calls instead of a single query.

**Solution**: Use JOINs to fetch related data in one query.

### Slow JOINs Due to Missing Indexes

**Symptoms**: JOIN queries are slow.

**Solution**: Ensure foreign key columns are indexed.

## References

- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [MySQL Documentation](https://dev.mysql.com/doc/)
- [MongoDB Schema Design Best Practices](https://www.mongodb.com/docs/manual/core/data-modeling-introduction/)

## Metadata

### Version
- **Current Version**: 1.0.0
- **Last Updated**: 2025-01-01

### Tags
`#database` `#schema` `#SQL` `#NoSQL` `#PostgreSQL` `#MySQL` `#MongoDB` `#migration`