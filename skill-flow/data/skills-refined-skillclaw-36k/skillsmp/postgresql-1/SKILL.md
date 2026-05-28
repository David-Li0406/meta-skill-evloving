---
name: postgresql
description: >
  PostgreSQL expert skill - Advanced SQL, extensions, data types, indexing, performance tuning, and PostgreSQL-specific features.
  Trigger: When writing SQL queries, designing schemas, optimizing performance, using PostgreSQL extensions, or working with advanced data types.
license: MIT
metadata:
  author: aurora
  version: "1.0"
  auto_invoke: "SQL queries, database design, PostgreSQL extensions, performance optimization, JSONB, arrays, full-text search"
allowed-tools: Read, Edit, Write, Glob, Grep, Bash, WebFetch, WebSearch
---

## When to Use

Use this skill when:
- Writing raw SQL queries for PostgreSQL
- Designing database schemas and tables
- Creating or optimizing indexes
- Working with JSONB, arrays, or composite types
- Implementing full-text search (tsvector/tsquery)
- Using PostgreSQL extensions (pg_trgm, uuid-ossp, etc.)
- Performance tuning and query optimization
- Writing stored procedures/functions
- Working with CTEs, window functions, or recursive queries
- Implementing constraints, triggers, or rules

## PostgreSQL Data Types

### Numeric Types

```sql
-- Exact numeric
SMALLINT          -- 2 bytes, -32768 to +32767
INTEGER           -- 4 bytes, -2147483648 to +2147483647
BIGINT            -- 8 bytes, -9223372036854775808 to +9223372036854775807
DECIMAL(p,s)      -- Variable, exact precision (alias: NUMERIC)
SERIAL            -- Auto-increment INTEGER
BIGSERIAL         -- Auto-increment BIGINT

-- Approximate numeric
REAL              -- 4 bytes, 6 decimal digits precision
DOUBLE PRECISION  -- 8 bytes, 15 decimal digits precision

-- Best practices
NUMERIC(10,2)     -- For money/financial (exact)
BIGINT            -- For IDs in high-volume tables
INTEGER           -- Default for counts/quantities
```

### Text Types

```sql
CHAR(n)           -- Fixed length, padded
VARCHAR(n)        -- Variable length, max n chars
TEXT              -- Unlimited variable length (preferred)
CITEXT            -- Case-insensitive text (extension)

-- Best practice: Use TEXT for most cases
-- VARCHAR(n) only when you need constraint
```

### Date/Time Types

```sql
DATE              -- Date only (4 bytes)
TIME              -- Time only (8 bytes)
TIMESTAMP         -- Date + time without timezone (8 bytes)
TIMESTAMPTZ       -- Date + time WITH timezone (8 bytes) - PREFERRED
INTERVAL          -- Time span

-- Examples
TIMESTAMP WITH TIME ZONE DEFAULT NOW()
TIMESTAMP WITHOUT TIME ZONE
INTERVAL '1 day 2 hours 30 minutes'

-- Best practice: ALWAYS use TIMESTAMPTZ
```

### Boolean

```sql
BOOLEAN           -- true, false, NULL
-- Accepts: TRUE, 't', 'true', 'y', 'yes', 'on', '1'
-- Accepts: FALSE, 'f', 'false', 'n', 'no', 'off', '0'
```

### UUID

```sql
UUID              -- 128-bit UUID

-- Generate UUID (requires extension)
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
uuid_generate_v4()           -- Random UUID
uuid_generate_v1()           -- Time-based UUID

-- Or use built-in (PostgreSQL 13+)
gen_random_uuid()

-- Best practice: Use UUID as primary key for distributed systems
```

### Binary

```sql
BYTEA             -- Variable length binary string
-- Use for: files, images, encrypted data
```

### Network Types

```sql
INET              -- IPv4 or IPv6 host address
CIDR              -- IPv4 or IPv6 network
MACADDR           -- MAC address
MACADDR8          -- MAC address (EUI-64 format)
```

### Geometric Types

```sql
POINT             -- (x, y)
LINE              -- Infinite line
LSEG              -- Line segment
BOX               -- Rectangular box
PATH              -- Geometric path
POLYGON           -- Polygon
CIRCLE            -- Circle
```

## PostgreSQL-Specific Data Types

### JSONB (Recommended over JSON)

```sql
-- Create column
metadata JSONB NOT NULL DEFAULT '{}'::jsonb

-- Insert
INSERT INTO products (metadata) VALUES ('{"color": "red", "size": "L"}'::jsonb);

-- Query operators
-- -> returns JSON, ->> returns TEXT
SELECT metadata->'color' FROM products;           -- Returns "red" (JSON)
SELECT metadata->>'color' FROM products;          -- Returns red (TEXT)
SELECT metadata->'nested'->'key' FROM products;   -- Nested access

-- Containment operators
SELECT * FROM products WHERE metadata @> '{"color": "red"}';    -- Contains
SELECT * FROM products WHERE metadata <@ '{"color": "red"}';    -- Is contained by
SELECT * FROM products WHERE metadata ? 'color';                -- Key exists
SELECT * FROM products WHERE metadata ?| array['color','size']; -- Any key exists
SELECT * FROM products WHERE metadata ?& array['color','size']; -- All keys exist

-- Path operators (PostgreSQL 12+)
SELECT metadata @? '$.color' FROM products;       -- Path exists
SELECT metadata @@ '$.price > 100' FROM products; -- Path predicate

-- JSONB functions
jsonb_set(target, path, new_value)       -- Set value at path
jsonb_insert(target, path, new_value)    -- Insert value at path
jsonb_strip_nulls(jsonb)                 -- Remove null values
jsonb_pretty(jsonb)                      -- Pretty print
jsonb_typeof(jsonb)                      -- Get type as text
jsonb_array_elements(jsonb)              -- Expand array to rows
jsonb_each(jsonb)                        -- Expand object to rows
jsonb_object_keys(jsonb)                 -- Get keys as set

-- Aggregation
jsonb_agg(expression)                    -- Aggregate to JSON array
jsonb_object_agg(key, value)             -- Aggregate to JSON object
```

### Arrays

```sql
-- Create column
tags TEXT[] NOT NULL DEFAULT '{}'
numbers INTEGER[]
matrix INTEGER[][]

-- Insert
INSERT INTO products (tags) VALUES (ARRAY['sale', 'new']);
INSERT INTO products (tags) VALUES ('{"sale", "new"}');

-- Query operators
SELECT * FROM products WHERE tags @> ARRAY['sale'];           -- Contains
SELECT * FROM products WHERE tags <@ ARRAY['sale', 'new'];    -- Is contained
SELECT * FROM products WHERE tags && ARRAY['sale', 'promo'];  -- Overlap (any match)
SELECT * FROM products WHERE 'sale' = ANY(tags);              -- Element exists
SELECT * FROM products WHERE 'sale' = ALL(tags);              -- All elements match

-- Array functions
array_length(array, dimension)           -- Get length
array_dims(array)                        -- Get dimensions
array_upper(array, dimension)            -- Upper bound
array_lower(array, dimension)            -- Lower bound
array_append(array, element)             -- Append element
array_prepend(element, array)            -- Prepend element
array_cat(array1, array2)                -- Concatenate arrays
array_remove(array, element)             -- Remove all occurrences
array_replace(array, from, to)           -- Replace elements
array_position(array, element)           -- Find position (1-indexed)
array_positions(array, element)          -- Find all positions
unnest(array)                            -- Expand to rows
array_agg(expression)                    -- Aggregate to array

-- Slicing
tags[1]                                  -- First element (1-indexed!)
tags[1:3]                                -- Slice from 1 to 3
tags[:3]                                 -- First 3 elements
tags[3:]                                 -- From 3 to end
```

### ENUM Types

```sql
-- Create enum
CREATE TYPE status_type AS ENUM ('pending', 'active', 'completed', 'cancelled');

-- Use in table
CREATE TABLE orders (
    id UUID PRIMARY KEY,
    status status_type NOT NULL DEFAULT 'pending'
);

-- Query
SELECT * FROM orders WHERE status = 'active';
SELECT * FROM orders WHERE status > 'pending';  -- Enums are ordered!

-- Alter enum (PostgreSQL 9.1+)
ALTER TYPE status_type ADD VALUE 'on_hold' AFTER 'active';
ALTER TYPE status_type RENAME VALUE 'cancelled' TO 'canceled';

-- List enum values
SELECT unnest(enum_range(NULL::status_type));
```

### Composite Types

```sql
-- Create composite type
CREATE TYPE address AS (
    street TEXT,
    city TEXT,
    country TEXT,
    postal_code VARCHAR(20)
);

-- Use in table
CREATE TABLE customers (
    id UUID PRIMARY KEY,
    name TEXT,
    shipping_address address,
    billing_address address
);

-- Insert
INSERT INTO customers (id, name, shipping_address)
VALUES (
    gen_random_uuid(),
    'John Doe',
    ROW('123 Main St', 'New York', 'USA', '10001')::address
);

-- Query composite fields
SELECT (shipping_address).city FROM customers;
SELECT * FROM customers WHERE (shipping_address).country = 'USA';
```

### Range Types

```sql
-- Built-in range types
INT4RANGE         -- Range of integer
INT8RANGE         -- Range of bigint
NUMRANGE          -- Range of numeric
TSRANGE           -- Range of timestamp without time zone
TSTZRANGE         -- Range of timestamp with time zone
DATERANGE         -- Range of date

-- Create range
'[1,10]'::int4range           -- Inclusive both ends
'[1,10)'::int4range           -- Inclusive start, exclusive end
'(1,10]'::int4range           -- Exclusive start, inclusive end
'(1,10)'::int4range           -- Exclusive both ends
'[,10]'::int4range            -- Unbounded start
'[1,]'::int4range             -- Unbounded end

-- Range operators
@>   -- Contains element or range
<@   -- Is contained by
&&   -- Overlaps
<<   -- Strictly left of
>>   -- Strictly right of
&<   -- Does not extend to the right of
&>   -- Does not extend to the left of
-|-  -- Adjacent to

-- Example: booking availability
CREATE TABLE bookings (
    id UUID PRIMARY KEY,
    room_id UUID NOT NULL,
    during TSTZRANGE NOT NULL,
    EXCLUDE USING gist (room_id WITH =, during WITH &&)  -- No overlaps!
);

INSERT INTO bookings (id, room_id, during) VALUES (
    gen_random_uuid(),
    'room-uuid',
    tstzrange('2024-01-15 14:00', '2024-01-15 16:00')
);
```

## Indexing Strategies

### B-Tree Index (Default)

```sql
-- Standard index
CREATE INDEX idx_users_email ON users(email);

-- Unique index
CREATE UNIQUE INDEX idx_users_email_unique ON users(email);

-- Partial index (conditional)
CREATE INDEX idx_orders_active ON orders(created_at)
WHERE status = 'active';

-- Multi-column index
CREATE INDEX idx_orders_user_status ON orders(user_id, status);
-- Useful for: WHERE user_id = ? AND status = ?
-- Also for: WHERE user_id = ? (leftmost prefix)
-- NOT useful for: WHERE status = ? (need separate index)

-- Expression index
CREATE INDEX idx_users_email_lower ON users(LOWER(email));
-- Query must match: WHERE LOWER(email) = 'test@example.com'

-- Index with INCLUDE (PostgreSQL 11+)
CREATE INDEX idx_orders_user ON orders(user_id) INCLUDE (status, total);
-- Enables index-only scans including status and total
```

### GIN Index (Generalized Inverted Index)

```sql
-- For JSONB
CREATE INDEX idx_products_metadata ON products USING GIN (metadata);
CREATE INDEX idx_products_metadata_path ON products USING GIN (metadata jsonb_path_ops);
-- jsonb_path_ops: faster @> queries, smaller index, but only supports @>

-- For Arrays
CREATE INDEX idx_products_tags ON products USING GIN (tags);

-- For Full-Text Search
CREATE INDEX idx_articles_fts ON articles USING GIN (to_tsvector('english', title || ' ' || body));

-- For Trigram (similarity search)
CREATE EXTENSION pg_trgm;
CREATE INDEX idx_products_name_trgm ON products USING GIN (name gin_trgm_ops);
```

### GiST Index (Generalized Search Tree)

```sql
-- For geometric types
CREATE INDEX idx_locations_point ON locations USING GiST (coordinates);

-- For range types (exclusion constraints)
CREATE INDEX idx_bookings_during ON bookings USING GiST (during);

-- For full-text search (smaller than GIN, but slower)
CREATE INDEX idx_articles_fts ON articles USING GiST (to_tsvector('english', body));
```

### BRIN Index (Block Range Index)

```sql
-- For naturally ordered data (time-series, append-only)
CREATE INDEX idx_logs_created ON logs USING BRIN (created_at);
-- Very small index size, good for large tables with correlated data
```

### Hash Index

```sql
-- For equality-only comparisons (PostgreSQL 10+)
CREATE INDEX idx_users_id ON users USING HASH (id);
-- Smaller than B-tree for equality, but no range queries
```

## Full-Text Search

### Basic Setup

```sql
-- Create tsvector column
ALTER TABLE articles ADD COLUMN search_vector tsvector;

-- Populate tsvector
UPDATE articles SET search_vector =
    setweight(to_tsvector('english', COALESCE(title, '')), 'A') ||
    setweight(to_tsvector('english', COALESCE(body, '')), 'B');

-- Create GIN index
CREATE INDEX idx_articles_search ON articles USING GIN (search_vector);

-- Keep updated with trigger
CREATE FUNCTION articles_search_trigger() RETURNS trigger AS $$
BEGIN
    NEW.search_vector :=
        setweight(to_tsvector('english', COALESCE(NEW.title, '')), 'A') ||
        setweight(to_tsvector('english', COALESCE(NEW.body, '')), 'B');
    RETURN NEW;
END
$$ LANGUAGE plpgsql;

CREATE TRIGGER tsvector_update BEFORE INSERT OR UPDATE
ON articles FOR EACH ROW EXECUTE FUNCTION articles_search_trigger();
```

### Search Queries

```sql
-- Basic search
SELECT * FROM articles
WHERE search_vector @@ to_tsquery('english', 'postgresql & database');

-- Phrase search
SELECT * FROM articles
WHERE search_vector @@ phraseto_tsquery('english', 'full text search');

-- Websearch syntax (PostgreSQL 11+)
SELECT * FROM articles
WHERE search_vector @@ websearch_to_tsquery('english', 'postgres -oracle "full text"');

-- Ranking results
SELECT title, ts_rank(search_vector, query) AS rank
FROM articles, to_tsquery('english', 'postgresql') AS query
WHERE search_vector @@ query
ORDER BY rank DESC;

-- Highlighting matches
SELECT ts_headline('english', body, to_tsquery('english', 'postgresql'),
    'StartSel=<mark>, StopSel=</mark>, MaxWords=35, MinWords=15')
FROM articles WHERE search_vector @@ to_tsquery('english', 'postgresql');
```

### tsquery Operators

```sql
'postgresql & database'    -- AND
'postgresql | mysql'       -- OR
'!oracle'                  -- NOT
'postgresql <-> database'  -- FOLLOWED BY (adjacent)
'postgresql <2> database'  -- FOLLOWED BY within 2 words
```

## Common Table Expressions (CTEs)

### Basic CTE

```sql
WITH active_users AS (
    SELECT id, name, email
    FROM users
    WHERE is_active = true
)
SELECT * FROM active_users WHERE email LIKE '%@company.com';
```

### Multiple CTEs

```sql
WITH
    active_users AS (
        SELECT id, name FROM users WHERE is_active = true
    ),
    user_orders AS (
        SELECT user_id, COUNT(*) as order_count
        FROM orders
        GROUP BY user_id
    )
SELECT u.name, COALESCE(o.order_count, 0) as orders
FROM active_users u
LEFT JOIN user_orders o ON u.id = o.user_id;
```

### Recursive CTE

```sql
-- Hierarchical data (org chart, categories, etc.)
WITH RECURSIVE category_tree AS (
    -- Anchor member (root categories)
    SELECT id, name, parent_id, 1 AS level, ARRAY[id] AS path
    FROM categories
    WHERE parent_id IS NULL

    UNION ALL

    -- Recursive member
    SELECT c.id, c.name, c.parent_id, ct.level + 1, ct.path || c.id
    FROM categories c
    INNER JOIN category_tree ct ON c.parent_id = ct.id
    WHERE NOT c.id = ANY(ct.path)  -- Prevent cycles
)
SELECT * FROM category_tree ORDER BY path;

-- Generate series example
WITH RECURSIVE numbers AS (
    SELECT 1 AS n
    UNION ALL
    SELECT n + 1 FROM numbers WHERE n < 10
)
SELECT * FROM numbers;
```

### Materialized CTE (PostgreSQL 12+)

```sql
-- Force CTE to be materialized (computed once)
WITH active_users AS MATERIALIZED (
    SELECT * FROM users WHERE is_active = true
)
SELECT * FROM active_users;

-- Force CTE to be inlined (merged into main query)
WITH active_users AS NOT MATERIALIZED (
    SELECT * FROM users WHERE is_active = true
)
SELECT * FROM active_users;
```

## Window Functions

### Basic Syntax

```sql
function_name(args) OVER (
    [PARTITION BY partition_columns]
    [ORDER BY sort_columns]
    [frame_clause]
)
```

### Ranking Functions

```sql
-- ROW_NUMBER: unique sequential number
SELECT name, department, salary,
    ROW_NUMBER() OVER (PARTITION BY department ORDER BY salary DESC) as row_num
FROM employees;

-- RANK: same rank for ties, gaps after
SELECT name, department, salary,
    RANK() OVER (PARTITION BY department ORDER BY salary DESC) as rank
FROM employees;
-- Result: 1, 2, 2, 4 (gap at 3)

-- DENSE_RANK: same rank for ties, no gaps
SELECT name, department, salary,
    DENSE_RANK() OVER (PARTITION BY department ORDER BY salary DESC) as dense_rank
FROM employees;
-- Result: 1, 2, 2, 3 (no gap)

-- NTILE: divide into n buckets
SELECT name, salary,
    NTILE(4) OVER (ORDER BY salary) as quartile
FROM employees;
```

### Aggregate Window Functions

```sql
SELECT name, department, salary,
    SUM(salary) OVER (PARTITION BY department) as dept_total,
    AVG(salary) OVER (PARTITION BY department) as dept_avg,
    COUNT(*) OVER (PARTITION BY department) as dept_count,
    salary::numeric / SUM(salary) OVER (PARTITION BY department) * 100 as pct_of_dept
FROM employees;
```

### Navigation Functions

```sql
-- LAG: previous row value
SELECT date, revenue,
    LAG(revenue, 1, 0) OVER (ORDER BY date) as prev_revenue,
    revenue - LAG(revenue, 1, 0) OVER (ORDER BY date) as revenue_change
FROM daily_sales;

-- LEAD: next row value
SELECT date, revenue,
    LEAD(revenue, 1) OVER (ORDER BY date) as next_revenue
FROM daily_sales;

-- FIRST_VALUE / LAST_VALUE
SELECT name, department, salary,
    FIRST_VALUE(name) OVER (PARTITION BY department ORDER BY salary DESC) as top_earner,
    LAST_VALUE(name) OVER (
        PARTITION BY department ORDER BY salary DESC
        ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
    ) as lowest_earner
FROM employees;

-- NTH_VALUE
SELECT name, salary,
    NTH_VALUE(name, 2) OVER (ORDER BY salary DESC) as second_highest
FROM employees;
```

### Frame Clauses

```sql
-- Running total
SELECT date, amount,
    SUM(amount) OVER (ORDER BY date ROWS UNBOUNDED PRECEDING) as running_total
FROM transactions;

-- Moving average (last 7 days)
SELECT date, amount,
    AVG(amount) OVER (
        ORDER BY date
        ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
    ) as moving_avg_7d
FROM daily_sales;

-- Frame specifications
ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW     -- Default
ROWS BETWEEN 3 PRECEDING AND 3 FOLLOWING             -- 7-row window
ROWS BETWEEN CURRENT ROW AND UNBOUNDED FOLLOWING     -- Current to end
RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW    -- By value, not position
GROUPS BETWEEN 1 PRECEDING AND 1 FOLLOWING           -- By peer groups
```

## Advanced Queries

### UPSERT (INSERT ... ON CONFLICT)

```sql
-- Update on conflict
INSERT INTO products (id, name, price)
VALUES ('uuid', 'Widget', 19.99)
ON CONFLICT (id) DO UPDATE SET
    name = EXCLUDED.name,
    price = EXCLUDED.price,
    updated_at = NOW();

-- Do nothing on conflict
INSERT INTO products (id, name, price)
VALUES ('uuid', 'Widget', 19.99)
ON CONFLICT (id) DO NOTHING;

-- Conflict on constraint
INSERT INTO products (id, sku, name)
VALUES ('uuid', 'SKU001', 'Widget')
ON CONFLICT ON CONSTRAINT products_sku_key DO UPDATE SET
    name = EXCLUDED.name;

-- Conditional update
INSERT INTO products (id, name, price)
VALUES ('uuid', 'Widget', 19.99)
ON CONFLICT (id) DO UPDATE SET
    price = EXCLUDED.price
WHERE products.price < EXCLUDED.price;  -- Only update if new price is higher
```

### RETURNING Clause

```sql
-- Return inserted row
INSERT INTO users (name, email)
VALUES ('John', 'john@example.com')
RETURNING id, created_at;

-- Return updated rows
UPDATE products
SET price = price * 1.1
WHERE category = 'electronics'
RETURNING id, name, price;

-- Return deleted rows
DELETE FROM sessions
WHERE expires_at < NOW()
RETURNING user_id, session_id;
```

### LATERAL Joins

```sql
-- Correlated subquery as join
SELECT u.name, recent_orders.*
FROM users u
CROSS JOIN LATERAL (
    SELECT id, total, created_at
    FROM orders
    WHERE orders.user_id = u.id
    ORDER BY created_at DESC
    LIMIT 3
) AS recent_orders;

-- With aggregation
SELECT c.name, stats.*
FROM categories c
CROSS JOIN LATERAL (
    SELECT
        COUNT(*) as product_count,
        AVG(price) as avg_price,
        MAX(price) as max_price
    FROM products
    WHERE products.category_id = c.id
) AS stats;
```

### GROUPING SETS, ROLLUP, CUBE

```sql
-- Multiple groupings in one query
SELECT department, job_title, SUM(salary)
FROM employees
GROUP BY GROUPING SETS (
    (department, job_title),  -- Group by both
    (department),              -- Group by department only
    (job_title),               -- Group by job_title only
    ()                         -- Grand total
);

-- ROLLUP: hierarchical grouping
SELECT year, quarter, month, SUM(revenue)
FROM sales
GROUP BY ROLLUP (year, quarter, month);
-- Produces: (year, quarter, month), (year, quarter), (year), ()

-- CUBE: all possible combinations
SELECT department, job_title, SUM(salary)
FROM employees
GROUP BY CUBE (department, job_title);
-- Produces all 4 combinations
```

### FILTER Clause

```sql
-- Conditional aggregation
SELECT
    COUNT(*) as total_orders,
    COUNT(*) FILTER (WHERE status = 'completed') as completed_orders,
    COUNT(*) FILTER (WHERE status = 'pending') as pending_orders,
    SUM(total) FILTER (WHERE status = 'completed') as completed_revenue
FROM orders;

-- Equivalent to CASE WHEN but cleaner
-- Old way:
-- SUM(CASE WHEN status = 'completed' THEN total ELSE 0 END)
```

## PostgreSQL Extensions

### Essential Extensions

```sql
-- UUID generation
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
SELECT uuid_generate_v4();

-- Crypto functions
CREATE EXTENSION IF NOT EXISTS pgcrypto;
SELECT crypt('password', gen_salt('bf'));
SELECT encode(digest('data', 'sha256'), 'hex');

-- Fuzzy string matching
CREATE EXTENSION IF NOT EXISTS pg_trgm;
SELECT similarity('postgresql', 'postgres');
SELECT 'postgresql' % 'postgres';  -- Similarity operator
CREATE INDEX idx_name_trgm ON products USING GIN (name gin_trgm_ops);

-- Case-insensitive text
CREATE EXTENSION IF NOT EXISTS citext;
-- Then use CITEXT type instead of TEXT

-- Table statistics
CREATE EXTENSION IF NOT EXISTS pg_stat_statements;
SELECT * FROM pg_stat_statements ORDER BY total_exec_time DESC LIMIT 10;

-- Foreign data wrappers
CREATE EXTENSION IF NOT EXISTS postgres_fdw;
-- Connect to other PostgreSQL databases

-- Tablefunc (crosstab/pivot)
CREATE EXTENSION IF NOT EXISTS tablefunc;
```

### Useful Functions from Extensions

```sql
-- pg_trgm: fuzzy search
SELECT * FROM products
WHERE name % 'widgett'  -- Finds 'widget' despite typo
ORDER BY similarity(name, 'widgett') DESC;

-- pgcrypto: password hashing
-- Hash password
INSERT INTO users (email, password_hash)
VALUES ('user@example.com', crypt('password123', gen_salt('bf', 12)));

-- Verify password
SELECT * FROM users
WHERE email = 'user@example.com'
AND password_hash = crypt('password123', password_hash);

-- pgcrypto: encryption
-- Encrypt
SELECT pgp_sym_encrypt('secret data', 'encryption_key');

-- Decrypt
SELECT pgp_sym_decrypt(encrypted_column, 'encryption_key') FROM secrets;
```

## Performance Optimization

### EXPLAIN ANALYZE

```sql
-- Basic explain
EXPLAIN SELECT * FROM users WHERE email = 'test@example.com';

-- With actual execution
EXPLAIN ANALYZE SELECT * FROM users WHERE email = 'test@example.com';

-- Full analysis
EXPLAIN (ANALYZE, BUFFERS, FORMAT TEXT)
SELECT * FROM users WHERE email = 'test@example.com';

-- JSON format for tools
EXPLAIN (ANALYZE, BUFFERS, FORMAT JSON)
SELECT * FROM users WHERE email = 'test@example.com';
```

### Understanding EXPLAIN Output

```
Seq Scan         -- Full table scan (usually bad for large tables)
Index Scan       -- Using index (good)
Index Only Scan  -- Covering index (best)
Bitmap Index     -- Multiple index conditions
Nested Loop      -- O(n*m), good for small result sets
Hash Join        -- Good for larger joins
Merge Join       -- Good for pre-sorted data

-- Key metrics
cost=0.00..123.45    -- Start cost..total cost (arbitrary units)
rows=1000            -- Estimated row count
width=100            -- Estimated row width in bytes
actual time=0.1..50  -- Actual start..total time in ms
loops=1              -- Number of executions
```

### Index Optimization

```sql
-- Check index usage
SELECT
    schemaname, tablename, indexname, idx_scan, idx_tup_read, idx_tup_fetch
FROM pg_stat_user_indexes
ORDER BY idx_scan DESC;

-- Find unused indexes
SELECT
    schemaname || '.' || relname AS table,
    indexrelname AS index,
    pg_size_pretty(pg_relation_size(i.indexrelid)) AS size,
    idx_scan as scans
FROM pg_stat_user_indexes ui
JOIN pg_index i ON ui.indexrelid = i.indexrelid
WHERE NOT i.indisunique
AND idx_scan < 50
ORDER BY pg_relation_size(i.indexrelid) DESC;

-- Check if index would help
SELECT * FROM pg_stat_user_tables
WHERE seq_scan > idx_scan
ORDER BY seq_tup_read DESC;
```

### Query Optimization Tips

```sql
-- 1. Use specific columns instead of SELECT *
SELECT id, name, email FROM users;  -- Good
SELECT * FROM users;                 -- Bad

-- 2. Use EXISTS instead of IN for subqueries
SELECT * FROM users u
WHERE EXISTS (SELECT 1 FROM orders o WHERE o.user_id = u.id);
-- Better than: WHERE u.id IN (SELECT user_id FROM orders)

-- 3. Use LIMIT for samples
SELECT * FROM large_table LIMIT 100;

-- 4. Batch operations
-- Instead of many single inserts:
INSERT INTO products (name, price) VALUES
    ('A', 10), ('B', 20), ('C', 30);  -- Single multi-row insert

-- 5. Use COPY for bulk loads
COPY products FROM '/path/to/file.csv' WITH (FORMAT csv, HEADER true);

-- 6. Avoid functions on indexed columns in WHERE
WHERE created_at >= '2024-01-01'              -- Good (uses index)
WHERE DATE(created_at) = '2024-01-01'         -- Bad (function prevents index)

-- 7. Use partial indexes for filtered queries
CREATE INDEX idx_active_users ON users(email) WHERE is_active = true;
```

### Connection and Resource Settings

```sql
-- Check current settings
SHOW work_mem;
SHOW shared_buffers;
SHOW effective_cache_size;

-- Set for session (for heavy queries)
SET work_mem = '256MB';
SET maintenance_work_mem = '1GB';

-- Reset
RESET work_mem;
```

## Schema Design Best Practices

### Primary Keys

```sql
-- UUID (recommended for distributed systems)
id UUID PRIMARY KEY DEFAULT gen_random_uuid()

-- BIGSERIAL (for high-volume single-database)
id BIGSERIAL PRIMARY KEY

-- Composite key
PRIMARY KEY (tenant_id, order_id)
```

### Foreign Keys

```sql
-- Basic foreign key
FOREIGN KEY (user_id) REFERENCES users(id)

-- With actions
FOREIGN KEY (user_id) REFERENCES users(id)
    ON DELETE CASCADE
    ON UPDATE CASCADE

-- Options: CASCADE, SET NULL, SET DEFAULT, RESTRICT, NO ACTION
```

### Constraints

```sql
-- Check constraint
CONSTRAINT positive_price CHECK (price > 0)
CONSTRAINT valid_email CHECK (email ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$')

-- Exclusion constraint (no overlapping ranges)
CONSTRAINT no_overlap EXCLUDE USING gist (
    room_id WITH =,
    during WITH &&
)

-- Unique constraint
CONSTRAINT unique_email UNIQUE (email)
CONSTRAINT unique_per_tenant UNIQUE (tenant_id, code)
```

### Partitioning (PostgreSQL 10+)

```sql
-- Range partitioning (by date)
CREATE TABLE orders (
    id UUID NOT NULL,
    created_at TIMESTAMPTZ NOT NULL,
    total NUMERIC(10,2)
) PARTITION BY RANGE (created_at);

CREATE TABLE orders_2024_01 PARTITION OF orders
    FOR VALUES FROM ('2024-01-01') TO ('2024-02-01');
CREATE TABLE orders_2024_02 PARTITION OF orders
    FOR VALUES FROM ('2024-02-01') TO ('2024-03-01');

-- List partitioning (by category)
CREATE TABLE products (
    id UUID NOT NULL,
    category TEXT NOT NULL
) PARTITION BY LIST (category);

CREATE TABLE products_electronics PARTITION OF products
    FOR VALUES IN ('electronics', 'computers');
CREATE TABLE products_clothing PARTITION OF products
    FOR VALUES IN ('clothing', 'shoes');

-- Hash partitioning (for even distribution)
CREATE TABLE logs (
    id UUID NOT NULL,
    data JSONB
) PARTITION BY HASH (id);

CREATE TABLE logs_0 PARTITION OF logs FOR VALUES WITH (MODULUS 4, REMAINDER 0);
CREATE TABLE logs_1 PARTITION OF logs FOR VALUES WITH (MODULUS 4, REMAINDER 1);
CREATE TABLE logs_2 PARTITION OF logs FOR VALUES WITH (MODULUS 4, REMAINDER 2);
CREATE TABLE logs_3 PARTITION OF logs FOR VALUES WITH (MODULUS 4, REMAINDER 3);
```

## Aurora/Sequelize Integration

### DataTypes Mapping

```typescript
// In Aurora/Sequelize models
import { DataTypes } from 'sequelize';

// UUID
type: DataTypes.UUID,
defaultValue: DataTypes.UUIDV4

// JSONB
type: DataTypes.JSONB,
defaultValue: {}

// Array
type: DataTypes.ARRAY(DataTypes.STRING(64))
type: DataTypes.ARRAY(DataTypes.UUID)
type: DataTypes.ARRAY(DataTypes.INTEGER)

// Enum
type: DataTypes.ENUM('PENDING', 'ACTIVE', 'COMPLETED')

// Numeric
type: DataTypes.DECIMAL(10, 2)
type: DataTypes.BIGINT
type: DataTypes.INTEGER

// Text
type: DataTypes.TEXT
type: DataTypes.STRING(255)

// Date/Time
type: DataTypes.DATE  // TIMESTAMP WITH TIME ZONE
type: DataTypes.DATEONLY  // DATE

// Boolean
type: DataTypes.BOOLEAN
```

### Index Definition in Models

```typescript
@Table({
    modelName: 'MyModel',
    indexes: [
        // Standard B-tree index
        { fields: ['email'], unique: true },

        // GIN index for arrays
        { fields: ['tags'], using: 'GIN' },

        // GIN index for JSONB
        { fields: ['metadata'], using: 'GIN' },

        // Partial index
        {
            fields: ['status'],
            where: { deletedAt: null }
        },

        // Multi-column index
        { fields: ['tenantId', 'code'], unique: true },

        // Expression index (requires raw SQL in migration)
    ],
})
```

## Decision Trees

### Choosing Data Types

```
Storing identifiers?
├─ Distributed system → UUID
├─ Single database, high volume → BIGSERIAL
└─ Single database, moderate → SERIAL/INTEGER

Storing text?
├─ Need case-insensitive → CITEXT (with extension)
├─ Fixed max length required → VARCHAR(n)
└─ Variable/unlimited → TEXT

Storing numbers?
├─ Money/financial → NUMERIC(precision, scale)
├─ Counts/IDs → INTEGER or BIGINT
└─ Scientific/approximate → DOUBLE PRECISION

Storing dates?
├─ Date only → DATE
├─ Time only → TIME
└─ Date + time → TIMESTAMPTZ (always with timezone!)

Storing structured data?
├─ Schema-less, queryable → JSONB
├─ List of values → ARRAY
├─ Fixed structure → Composite type or separate table
└─ Key-value pairs → JSONB or hstore
```

### Choosing Index Type

```
Query pattern?
├─ Equality (=) only → HASH (or B-tree)
├─ Range (<, >, BETWEEN) → B-tree
├─ Pattern matching (LIKE '%x%') → GIN with pg_trgm
├─ Full-text search → GIN (faster) or GiST (smaller)
├─ JSONB containment (@>) → GIN
├─ Array operations (@>, &&) → GIN
├─ Geometric/range → GiST
└─ Time-series (ordered inserts) → BRIN

Table size?
├─ Small (< 100K rows) → B-tree usually sufficient
├─ Medium (100K-10M) → Consider partial indexes
└─ Large (> 10M) → Consider partitioning + BRIN
```

## Commands Reference

```bash
# Connect to database
psql -h localhost -U postgres -d database_name

# Execute SQL file
psql -h localhost -U postgres -d database_name -f script.sql

# Dump database
pg_dump -h localhost -U postgres database_name > backup.sql
pg_dump -h localhost -U postgres -Fc database_name > backup.dump  # Custom format

# Restore database
psql -h localhost -U postgres -d database_name < backup.sql
pg_restore -h localhost -U postgres -d database_name backup.dump

# Check PostgreSQL version
psql -c "SELECT version();"

# List databases
psql -c "\l"

# List tables in database
psql -d database_name -c "\dt"

# Describe table
psql -d database_name -c "\d+ table_name"

# List indexes
psql -d database_name -c "\di"

# Show running queries
psql -c "SELECT pid, now() - pg_stat_activity.query_start AS duration, query FROM pg_stat_activity WHERE state = 'active';"

# Kill query
psql -c "SELECT pg_cancel_backend(pid);"      -- Graceful
psql -c "SELECT pg_terminate_backend(pid);"   -- Force
```

## Resources

- **Templates**: See [assets/](assets/) for SQL templates
- **Aurora Criteria**: See `aurora-criteria` skill for QueryStatement patterns
- **Aurora Models**: See `src/@app/*/infrastructure/sequelize/*.model.ts` for examples
