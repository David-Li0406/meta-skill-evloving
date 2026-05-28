# Schema Design Patterns

Detailed patterns for database schema design, normalization, indexes, and relationships.

## Normalization Levels

### First Normal Form (1NF)

**Rule:** No repeating groups, atomic values only.

```sql
-- BAD: Repeating groups
CREATE TABLE orders (
  id INT PRIMARY KEY,
  items TEXT  -- "item1,item2,item3"
);

-- GOOD: Separate table
CREATE TABLE orders (
  id INT PRIMARY KEY,
  created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE order_items (
  id INT PRIMARY KEY,
  order_id INT REFERENCES orders(id),
  item_name TEXT NOT NULL,
  quantity INT NOT NULL
);
```

### Second Normal Form (2NF)

**Rule:** All non-key columns depend on the entire primary key.

```sql
-- BAD: Partial dependency on composite key
CREATE TABLE order_items (
  order_id INT,
  product_id INT,
  product_name TEXT,  -- depends only on product_id
  quantity INT,
  PRIMARY KEY (order_id, product_id)
);

-- GOOD: Separate product details
CREATE TABLE products (
  id INT PRIMARY KEY,
  name TEXT NOT NULL
);

CREATE TABLE order_items (
  order_id INT REFERENCES orders(id),
  product_id INT REFERENCES products(id),
  quantity INT NOT NULL,
  PRIMARY KEY (order_id, product_id)
);
```

### Third Normal Form (3NF)

**Rule:** No transitive dependencies.

```sql
-- BAD: Transitive dependency
CREATE TABLE employees (
  id INT PRIMARY KEY,
  name TEXT,
  department_id INT,
  department_name TEXT  -- depends on department_id, not employee
);

-- GOOD: Separate department table
CREATE TABLE departments (
  id INT PRIMARY KEY,
  name TEXT NOT NULL
);

CREATE TABLE employees (
  id INT PRIMARY KEY,
  name TEXT NOT NULL,
  department_id INT REFERENCES departments(id)
);
```

## Naming Conventions

### Tables

| Convention | Example | Notes |
|------------|---------|-------|
| Singular | `user`, `order` | Preferred |
| Plural | `users`, `orders` | Common in Rails |
| snake_case | `order_item` | Standard SQL |

### Columns

| Type | Convention | Example |
|------|------------|---------|
| Primary key | `id` | `id` |
| Foreign key | `{table}_id` | `user_id` |
| Boolean | `is_` or `has_` prefix | `is_active`, `has_verified` |
| Timestamps | `{verb}_at` | `created_at`, `deleted_at` |
| Counts | `{noun}_count` | `comment_count` |

### Indexes

```sql
-- Pattern: idx_{table}_{columns}
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_orders_user_id_created_at ON orders(user_id, created_at);

-- Unique indexes: uq_{table}_{columns}
CREATE UNIQUE INDEX uq_users_email ON users(email);
```

## Primary Key Strategies

### Auto-increment Integer

```sql
-- PostgreSQL
CREATE TABLE users (
  id SERIAL PRIMARY KEY
);

-- MySQL
CREATE TABLE users (
  id INT AUTO_INCREMENT PRIMARY KEY
);
```

**Pros:** Simple, compact, fast joins
**Cons:** Exposes record count, predictable, problematic for distributed systems

### UUID

```sql
-- PostgreSQL
CREATE TABLE users (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid()
);

-- With index optimization (UUID v7 for sortability)
CREATE EXTENSION IF NOT EXISTS pgcrypto;
```

**Pros:** Globally unique, no central coordination, non-predictable
**Cons:** Larger (16 bytes), random inserts cause index fragmentation

### ULID / UUID v7

```sql
-- Sortable, timestamp-prefixed
-- Use application-generated ULIDs for better index performance
CREATE TABLE users (
  id CHAR(26) PRIMARY KEY  -- ULID
);
```

**Pros:** Sortable by creation time, globally unique
**Cons:** Application must generate, 26 characters

## Relationship Patterns

### One-to-Many

```sql
-- Parent table
CREATE TABLE authors (
  id SERIAL PRIMARY KEY,
  name TEXT NOT NULL
);

-- Child table with foreign key
CREATE TABLE books (
  id SERIAL PRIMARY KEY,
  title TEXT NOT NULL,
  author_id INT NOT NULL REFERENCES authors(id)
);

-- Always index foreign keys
CREATE INDEX idx_books_author_id ON books(author_id);
```

### Many-to-Many

```sql
-- Junction table
CREATE TABLE book_categories (
  book_id INT REFERENCES books(id) ON DELETE CASCADE,
  category_id INT REFERENCES categories(id) ON DELETE CASCADE,
  PRIMARY KEY (book_id, category_id)
);

-- Index both directions
CREATE INDEX idx_book_categories_category_id ON book_categories(category_id);
```

### Self-Referential

```sql
-- Hierarchical data (adjacency list)
CREATE TABLE categories (
  id SERIAL PRIMARY KEY,
  name TEXT NOT NULL,
  parent_id INT REFERENCES categories(id)
);

CREATE INDEX idx_categories_parent_id ON categories(parent_id);

-- Query children
SELECT * FROM categories WHERE parent_id = 1;

-- Query with recursion (PostgreSQL)
WITH RECURSIVE tree AS (
  SELECT id, name, parent_id, 0 AS depth
  FROM categories WHERE parent_id IS NULL
  UNION ALL
  SELECT c.id, c.name, c.parent_id, t.depth + 1
  FROM categories c JOIN tree t ON c.parent_id = t.id
)
SELECT * FROM tree;
```

### Polymorphic Associations

```sql
-- Option 1: Separate tables (preferred)
CREATE TABLE post_comments (
  id SERIAL PRIMARY KEY,
  post_id INT REFERENCES posts(id),
  content TEXT NOT NULL
);

CREATE TABLE image_comments (
  id SERIAL PRIMARY KEY,
  image_id INT REFERENCES images(id),
  content TEXT NOT NULL
);

-- Option 2: Polymorphic (when necessary)
CREATE TABLE comments (
  id SERIAL PRIMARY KEY,
  commentable_type TEXT NOT NULL,  -- 'post' or 'image'
  commentable_id INT NOT NULL,
  content TEXT NOT NULL
);

CREATE INDEX idx_comments_poly ON comments(commentable_type, commentable_id);
```

## Soft Deletes

```sql
CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  email TEXT NOT NULL,
  deleted_at TIMESTAMP NULL,
  created_at TIMESTAMP DEFAULT NOW()
);

-- Partial index for active records
CREATE UNIQUE INDEX uq_users_email_active
ON users(email) WHERE deleted_at IS NULL;

-- Query active users
SELECT * FROM users WHERE deleted_at IS NULL;
```

## Audit Columns

### Standard Timestamps

```sql
CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  email TEXT NOT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);

-- PostgreSQL: Auto-update trigger
CREATE OR REPLACE FUNCTION update_updated_at()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = NOW();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER users_updated_at
BEFORE UPDATE ON users
FOR EACH ROW EXECUTE FUNCTION update_updated_at();
```

### Full Audit Trail

```sql
-- Separate audit table
CREATE TABLE audit_log (
  id SERIAL PRIMARY KEY,
  table_name TEXT NOT NULL,
  record_id INT NOT NULL,
  action TEXT NOT NULL,  -- INSERT, UPDATE, DELETE
  old_data JSONB,
  new_data JSONB,
  changed_by INT REFERENCES users(id),
  changed_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_audit_log_record ON audit_log(table_name, record_id);
```

## Index Design

### B-tree Indexes (Default)

```sql
-- Single column
CREATE INDEX idx_users_email ON users(email);

-- Composite (order matters!)
CREATE INDEX idx_orders_user_date ON orders(user_id, created_at);

-- Partial index
CREATE INDEX idx_orders_pending ON orders(created_at)
WHERE status = 'pending';

-- Covering index (includes columns for index-only scans)
CREATE INDEX idx_users_email_name ON users(email) INCLUDE (name);
```

### Composite Index Column Order

The leftmost columns should be:
1. Columns with equality conditions (`=`)
2. Columns with range conditions (`<`, `>`, `BETWEEN`)
3. Columns in ORDER BY

```sql
-- Query pattern
SELECT * FROM orders
WHERE user_id = 1 AND status = 'pending'
ORDER BY created_at DESC;

-- Optimal index
CREATE INDEX idx_orders_user_status_created
ON orders(user_id, status, created_at DESC);
```

### Specialized Indexes

```sql
-- PostgreSQL: GIN for arrays and JSONB
CREATE INDEX idx_users_tags ON users USING GIN(tags);
CREATE INDEX idx_users_metadata ON users USING GIN(metadata);

-- PostgreSQL: GiST for geometric/full-text
CREATE INDEX idx_locations_point ON locations USING GIST(point);

-- PostgreSQL: BRIN for large sequential data
CREATE INDEX idx_events_timestamp ON events USING BRIN(timestamp);

-- Full-text search
CREATE INDEX idx_posts_search ON posts USING GIN(
  to_tsvector('english', title || ' ' || content)
);
```

## Data Types

### Choosing the Right Type

| Data | Type | Notes |
|------|------|-------|
| Boolean | `BOOLEAN` | Not `INT` or `CHAR(1)` |
| Small int (< 32K) | `SMALLINT` | 2 bytes |
| Integer | `INT` | 4 bytes |
| Large int | `BIGINT` | 8 bytes |
| Money | `DECIMAL(19,4)` | Never use `FLOAT` |
| Percentages | `DECIMAL(5,2)` | 0.00 to 100.00 |
| Email | `VARCHAR(255)` | With CHECK constraint |
| URL | `TEXT` | URLs can be long |
| IP address | `INET` (PostgreSQL) | Native type |
| UUID | `UUID` | Native type when available |
| Timestamp | `TIMESTAMPTZ` | Always store with timezone |
| Duration | `INTERVAL` | Or `INT` for seconds |

### JSON Columns

```sql
-- PostgreSQL: JSONB preferred over JSON
CREATE TABLE products (
  id SERIAL PRIMARY KEY,
  name TEXT NOT NULL,
  attributes JSONB DEFAULT '{}'
);

-- Query JSON
SELECT * FROM products
WHERE attributes->>'color' = 'red';

-- Index JSON paths
CREATE INDEX idx_products_color
ON products((attributes->>'color'));

-- Full JSONB index (for @>, ?, ?| operators)
CREATE INDEX idx_products_attrs ON products USING GIN(attributes);
```

## Constraints

### Check Constraints

```sql
CREATE TABLE products (
  id SERIAL PRIMARY KEY,
  name TEXT NOT NULL,
  price DECIMAL(10,2) NOT NULL CHECK (price >= 0),
  discount DECIMAL(5,2) CHECK (discount >= 0 AND discount <= 100),
  status TEXT CHECK (status IN ('draft', 'active', 'archived'))
);
```

### Exclusion Constraints (PostgreSQL)

```sql
-- Prevent overlapping date ranges
CREATE TABLE reservations (
  id SERIAL PRIMARY KEY,
  room_id INT NOT NULL,
  start_date DATE NOT NULL,
  end_date DATE NOT NULL,
  EXCLUDE USING GIST (
    room_id WITH =,
    daterange(start_date, end_date) WITH &&
  )
);
```

## Schema Validation Checklist

- [ ] Tables use singular names consistently
- [ ] All tables have `id` primary key
- [ ] Foreign keys follow `{table}_id` pattern
- [ ] Foreign keys have indexes
- [ ] Timestamps: `created_at`, `updated_at` on all tables
- [ ] Boolean columns use `is_` or `has_` prefix
- [ ] No nullable columns without explicit reason
- [ ] Appropriate data types (no VARCHAR for booleans)
- [ ] Check constraints for enums and valid ranges
- [ ] Composite indexes in correct column order
- [ ] No redundant indexes (composite covers single-column queries)
- [ ] Cascading rules appropriate for relationships
