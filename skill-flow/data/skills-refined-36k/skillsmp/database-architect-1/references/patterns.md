# Database Architect

## Patterns


---
  #### **Name**
Schema Design for Growth
  #### **Description**
Designing schemas that scale with business
  #### **When**
Starting new database design
  #### **Example**
    -- Multi-tenant SaaS schema pattern
    
    -- Tenant isolation with organization_id
    CREATE TABLE organizations (
        id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
        name TEXT NOT NULL,
        slug TEXT UNIQUE NOT NULL,
        created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
        settings JSONB NOT NULL DEFAULT '{}'
    );
    
    -- Users belong to organizations
    CREATE TABLE users (
        id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
        organization_id UUID NOT NULL REFERENCES organizations(id),
        email TEXT NOT NULL,
        password_hash TEXT NOT NULL,
        role TEXT NOT NULL DEFAULT 'member',
        created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    
        -- Unique email per organization (allows same email in different orgs)
        UNIQUE (organization_id, email)
    );
    
    -- Every table includes organization_id for isolation
    CREATE TABLE projects (
        id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
        organization_id UUID NOT NULL REFERENCES organizations(id),
        name TEXT NOT NULL,
        created_by UUID NOT NULL REFERENCES users(id),
        created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
    );
    
    -- Indexes designed for query patterns
    CREATE INDEX idx_users_org_email ON users(organization_id, email);
    CREATE INDEX idx_projects_org_created ON projects(organization_id, created_at DESC);
    
    -- Row-level security for tenant isolation
    ALTER TABLE projects ENABLE ROW LEVEL SECURITY;
    CREATE POLICY projects_org_isolation ON projects
        USING (organization_id = current_setting('app.organization_id')::UUID);
    

---
  #### **Name**
Query-Driven Index Design
  #### **Description**
Creating indexes based on access patterns
  #### **When**
Optimizing query performance
  #### **Example**
    -- Common query: Find user's recent orders
    -- SELECT * FROM orders WHERE user_id = ? ORDER BY created_at DESC LIMIT 20
    
    -- Covering index for this query
    CREATE INDEX idx_orders_user_recent
        ON orders(user_id, created_at DESC)
        INCLUDE (status, total);  -- Include columns to avoid table lookup
    
    -- Query: Search products by category and price range
    -- SELECT * FROM products WHERE category = ? AND price BETWEEN ? AND ?
    
    -- Composite index with range condition last
    CREATE INDEX idx_products_category_price
        ON products(category, price);
    
    -- Query: Full-text search on product names
    -- SELECT * FROM products WHERE name ILIKE '%search%'
    
    -- GIN index for text search (PostgreSQL)
    CREATE INDEX idx_products_name_search
        ON products USING GIN (to_tsvector('english', name));
    
    -- Partial index for common filter
    -- Only index active products (most common query)
    CREATE INDEX idx_products_active
        ON products(category, price)
        WHERE status = 'active';
    
    -- Monitor index usage
    SELECT schemaname, tablename, indexname, idx_scan, idx_tup_read
    FROM pg_stat_user_indexes
    ORDER BY idx_scan DESC;
    

---
  #### **Name**
Migration Strategies
  #### **Description**
Safe database migrations without downtime
  #### **When**
Evolving schema in production
  #### **Example**
    -- NEVER do this in production:
    -- ALTER TABLE users ADD COLUMN phone TEXT NOT NULL;
    -- (Locks table, rewrites all rows, fails on existing data)
    
    -- DO: Multi-step migration for adding NOT NULL column
    
    -- Step 1: Add nullable column (instant, no lock)
    ALTER TABLE users ADD COLUMN phone TEXT;
    
    -- Step 2: Backfill in batches (application code)
    -- UPDATE users SET phone = 'unknown'
    -- WHERE phone IS NULL AND id BETWEEN batch_start AND batch_end;
    
    -- Step 3: Add NOT NULL constraint
    -- (Only after all rows have values)
    ALTER TABLE users ALTER COLUMN phone SET NOT NULL;
    
    -- For renaming columns (zero downtime):
    
    -- Step 1: Add new column
    ALTER TABLE users ADD COLUMN full_name TEXT;
    
    -- Step 2: Deploy code that writes to BOTH columns
    -- UPDATE users SET full_name = name WHERE full_name IS NULL;
    
    -- Step 3: Deploy code that reads from new column
    
    -- Step 4: Drop old column
    ALTER TABLE users DROP COLUMN name;
    
    -- For large table changes, use pg_repack or similar
    -- to avoid locking
    

---
  #### **Name**
JSON vs Relational Trade-offs
  #### **Description**
When to use JSONB vs normalized columns
  #### **When**
Deciding data structure
  #### **Example**
    -- USE JSONB when:
    -- 1. Schema is truly dynamic/user-defined
    -- 2. Data is read as a whole, rarely queried by fields
    -- 3. Rapid prototyping (migrate to columns later)
    
    -- User preferences - rarely queried, read as whole
    CREATE TABLE users (
        id UUID PRIMARY KEY,
        email TEXT NOT NULL,
        preferences JSONB NOT NULL DEFAULT '{}'
    );
    
    -- Index specific JSONB paths if queried
    CREATE INDEX idx_users_theme
        ON users ((preferences->>'theme'));
    
    -- USE COLUMNS when:
    -- 1. Field is queried/filtered frequently
    -- 2. Field needs constraints or foreign keys
    -- 3. Field is used in joins
    -- 4. Type safety matters
    
    -- BAD: Important data in JSONB
    CREATE TABLE orders (
        id UUID PRIMARY KEY,
        data JSONB  -- contains user_id, total, status
    );
    
    -- GOOD: Query-able fields as columns
    CREATE TABLE orders (
        id UUID PRIMARY KEY,
        user_id UUID NOT NULL REFERENCES users(id),
        status TEXT NOT NULL CHECK (status IN ('pending', 'paid', 'shipped')),
        total NUMERIC(10,2) NOT NULL,
        metadata JSONB NOT NULL DEFAULT '{}'  -- Only truly flexible data
    );
    

## Anti-Patterns


---
  #### **Name**
Missing Indexes
  #### **Description**
Deploying tables without considering query patterns
  #### **Why**
Every query scans full table, performance degrades with data
  #### **Instead**
Design indexes from query patterns before deployment

---
  #### **Name**
Over-Indexing
  #### **Description**
Adding index on every column "just in case"
  #### **Why**
Indexes slow writes, use disk, need maintenance
  #### **Instead**
Monitor slow queries, add indexes for proven patterns

---
  #### **Name**
EAV (Entity-Attribute-Value)
  #### **Description**
Storing all data as key-value pairs
  #### **Why**
Impossible to query efficiently, no type safety, join hell
  #### **Instead**
Use proper schema with JSONB for truly dynamic parts

---
  #### **Name**
UUID Primary Keys Without Strategy
  #### **Description**
Random UUIDs causing index fragmentation
  #### **Why**
Random inserts scatter across B-tree, slow writes
  #### **Instead**
Use UUIDv7 (time-ordered) or bigserial for high-write tables

---
  #### **Name**
No Foreign Keys
  #### **Description**
Relying on application code for referential integrity
  #### **Why**
Bugs create orphan records, data becomes inconsistent
  #### **Instead**
Always use foreign keys, they're documentation that enforces