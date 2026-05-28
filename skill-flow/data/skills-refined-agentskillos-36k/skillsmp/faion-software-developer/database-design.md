---
id: database-design
name: "Database Design"
domain: DEV
skill: faion-software-developer
category: "development"
---

# Database Design

## Overview

Database design is the process of structuring data storage to ensure integrity, performance, and maintainability. It encompasses schema design, normalization, indexing strategies, and relationship modeling for both relational and non-relational databases.

## When to Use

- Starting a new project that requires persistent data storage
- Adding new features that require schema changes
- Migrating from one database system to another
- Performance optimization requiring schema refactoring
- Scaling applications that have outgrown initial design

## Key Principles

- **Normalize first, denormalize for performance**: Start with 3NF, then selectively denormalize based on query patterns
- **Design for queries**: Understand access patterns before finalizing schema
- **Enforce integrity at database level**: Use constraints, foreign keys, and triggers
- **Plan for growth**: Consider partitioning, sharding strategies from the start
- **Document everything**: Schema diagrams, relationships, and business rules

## Best Practices

### Entity-Relationship Modeling

```sql
-- Example: E-commerce schema with proper relationships
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE products (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    sku VARCHAR(50) NOT NULL UNIQUE,
    name VARCHAR(255) NOT NULL,
    price DECIMAL(10, 2) NOT NULL CHECK (price >= 0),
    stock_quantity INTEGER NOT NULL DEFAULT 0 CHECK (stock_quantity >= 0),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE orders (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE RESTRICT,
    status VARCHAR(20) NOT NULL DEFAULT 'pending'
        CHECK (status IN ('pending', 'processing', 'shipped', 'delivered', 'cancelled')),
    total_amount DECIMAL(12, 2) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE order_items (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    order_id UUID NOT NULL REFERENCES orders(id) ON DELETE CASCADE,
    product_id UUID NOT NULL REFERENCES products(id) ON DELETE RESTRICT,
    quantity INTEGER NOT NULL CHECK (quantity > 0),
    unit_price DECIMAL(10, 2) NOT NULL,
    UNIQUE(order_id, product_id)
);
```

### Indexing Strategy

```sql
-- Primary queries determine index strategy
-- Query: Find orders by user, sorted by date
CREATE INDEX idx_orders_user_created ON orders(user_id, created_at DESC);

-- Query: Search products by name
CREATE INDEX idx_products_name_trgm ON products
    USING gin(name gin_trgm_ops);

-- Query: Find pending orders for processing
CREATE INDEX idx_orders_status_pending ON orders(created_at)
    WHERE status = 'pending';

-- Composite index for common join pattern
CREATE INDEX idx_order_items_order_product ON order_items(order_id, product_id);
```

### Soft Deletes Pattern

```sql
-- Add soft delete capability
ALTER TABLE users ADD COLUMN deleted_at TIMESTAMP WITH TIME ZONE;

-- Create view for active users
CREATE VIEW active_users AS
SELECT * FROM users WHERE deleted_at IS NULL;

-- Partial index for queries on active records
CREATE INDEX idx_users_email_active ON users(email)
    WHERE deleted_at IS NULL;
```

### Audit Trail

```sql
-- Audit table for tracking changes
CREATE TABLE audit_log (
    id BIGSERIAL PRIMARY KEY,
    table_name VARCHAR(50) NOT NULL,
    record_id UUID NOT NULL,
    action VARCHAR(10) NOT NULL CHECK (action IN ('INSERT', 'UPDATE', 'DELETE')),
    old_data JSONB,
    new_data JSONB,
    changed_by UUID REFERENCES users(id),
    changed_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Trigger function for automatic auditing
CREATE OR REPLACE FUNCTION audit_trigger_func()
RETURNS TRIGGER AS $$
BEGIN
    IF TG_OP = 'INSERT' THEN
        INSERT INTO audit_log(table_name, record_id, action, new_data)
        VALUES (TG_TABLE_NAME, NEW.id, 'INSERT', to_jsonb(NEW));
    ELSIF TG_OP = 'UPDATE' THEN
        INSERT INTO audit_log(table_name, record_id, action, old_data, new_data)
        VALUES (TG_TABLE_NAME, NEW.id, 'UPDATE', to_jsonb(OLD), to_jsonb(NEW));
    ELSIF TG_OP = 'DELETE' THEN
        INSERT INTO audit_log(table_name, record_id, action, old_data)
        VALUES (TG_TABLE_NAME, OLD.id, 'DELETE', to_jsonb(OLD));
    END IF;
    RETURN COALESCE(NEW, OLD);
END;
$$ LANGUAGE plpgsql;
```

### Migration Strategy

```python
# Alembic migration example
"""Add user preferences table

Revision ID: a1b2c3d4e5f6
Revises: 9z8y7x6w5v4u
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

def upgrade():
    op.create_table(
        'user_preferences',
        sa.Column('id', postgresql.UUID(), primary_key=True),
        sa.Column('user_id', postgresql.UUID(), nullable=False),
        sa.Column('theme', sa.String(20), default='light'),
        sa.Column('notifications_enabled', sa.Boolean(), default=True),
        sa.Column('language', sa.String(5), default='en'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.UniqueConstraint('user_id')
    )
    op.create_index('idx_user_prefs_user', 'user_preferences', ['user_id'])

def downgrade():
    op.drop_table('user_preferences')
```

## Anti-patterns

- **God tables**: Single table with 50+ columns for everything
- **Missing foreign keys**: Relying on application logic for referential integrity
- **Over-indexing**: Index on every column regardless of query patterns
- **EAV abuse**: Entity-Attribute-Value for structured data
- **No constraints**: Missing CHECK, NOT NULL, UNIQUE constraints
- **Storing computed values**: That can become stale (store formulas instead)
- **VARCHAR(255) everywhere**: Without considering actual data requirements

## References

- [PostgreSQL Documentation](https://www.postgresql.org/docs/current/)
- [Database Normalization](https://en.wikipedia.org/wiki/Database_normalization)
- [Use The Index, Luke](https://use-the-index-luke.com/)
- [Alembic Tutorial](https://alembic.sqlalchemy.org/en/latest/tutorial.html)
