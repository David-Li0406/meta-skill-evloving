-- ============================================
-- PostgreSQL Common Query Templates
-- ============================================

-- ============================================
-- 1. PAGINATION PATTERNS
-- ============================================

-- Offset pagination (simple but slow for large offsets)
SELECT id, name, created_at
FROM products
WHERE deleted_at IS NULL
ORDER BY created_at DESC
LIMIT 25 OFFSET 0;  -- Page 1

-- Keyset/Cursor pagination (faster for large datasets)
SELECT id, name, created_at
FROM products
WHERE deleted_at IS NULL
  AND (created_at, id) < ('2024-01-15 10:00:00+00', 'last-seen-uuid')
ORDER BY created_at DESC, id DESC
LIMIT 25;

-- Count with pagination
WITH filtered AS (
    SELECT id, name, created_at
    FROM products
    WHERE deleted_at IS NULL
      AND category = 'electronics'
)
SELECT
    (SELECT COUNT(*) FROM filtered) as total_count,
    f.*
FROM filtered f
ORDER BY f.created_at DESC
LIMIT 25 OFFSET 0;


-- ============================================
-- 2. SEARCH PATTERNS
-- ============================================

-- Multi-field search with ILIKE
SELECT * FROM products
WHERE deleted_at IS NULL
  AND (
    name ILIKE '%search_term%'
    OR sku ILIKE '%search_term%'
    OR description ILIKE '%search_term%'
  )
ORDER BY
    CASE WHEN name ILIKE 'search_term%' THEN 0 ELSE 1 END,  -- Prioritize prefix match
    name
LIMIT 25;

-- Fuzzy search with pg_trgm (requires extension)
SELECT *, similarity(name, 'search_term') as sim
FROM products
WHERE name % 'search_term'
ORDER BY sim DESC
LIMIT 25;

-- Full-text search
SELECT *,
    ts_rank(search_vector, query) as rank,
    ts_headline('english', description, query, 'MaxWords=35') as snippet
FROM products,
    websearch_to_tsquery('english', 'search term') as query
WHERE search_vector @@ query
ORDER BY rank DESC
LIMIT 25;


-- ============================================
-- 3. JSONB QUERIES
-- ============================================

-- Query nested JSONB
SELECT * FROM products
WHERE metadata->>'brand' = 'Samsung'
  AND (metadata->'specs'->>'ram')::int >= 8;

-- JSONB containment
SELECT * FROM products
WHERE metadata @> '{"category": "phone", "active": true}';

-- Update JSONB field
UPDATE products
SET metadata = jsonb_set(metadata, '{specs,ram}', '16')
WHERE id = 'uuid';

-- Add to JSONB object
UPDATE products
SET metadata = metadata || '{"new_field": "value"}'
WHERE id = 'uuid';

-- Remove from JSONB
UPDATE products
SET metadata = metadata - 'field_to_remove'
WHERE id = 'uuid';

-- Query array inside JSONB
SELECT * FROM products
WHERE metadata->'tags' ? 'sale';  -- Has 'sale' in tags array


-- ============================================
-- 4. ARRAY QUERIES
-- ============================================

-- Contains all elements
SELECT * FROM products WHERE tags @> ARRAY['new', 'featured'];

-- Contains any element
SELECT * FROM products WHERE tags && ARRAY['sale', 'clearance'];

-- Element exists
SELECT * FROM products WHERE 'electronics' = ANY(categories);

-- Array aggregation
SELECT category, array_agg(DISTINCT tag) as all_tags
FROM products, unnest(tags) as tag
GROUP BY category;

-- Add to array
UPDATE products
SET tags = array_append(tags, 'new_tag')
WHERE id = 'uuid' AND NOT 'new_tag' = ANY(tags);

-- Remove from array
UPDATE products
SET tags = array_remove(tags, 'old_tag')
WHERE id = 'uuid';


-- ============================================
-- 5. DATE/TIME QUERIES
-- ============================================

-- Today's records
SELECT * FROM orders
WHERE created_at >= CURRENT_DATE
  AND created_at < CURRENT_DATE + INTERVAL '1 day';

-- Last 30 days
SELECT * FROM orders
WHERE created_at >= NOW() - INTERVAL '30 days';

-- Date range
SELECT * FROM orders
WHERE created_at BETWEEN '2024-01-01' AND '2024-01-31 23:59:59';

-- Group by date
SELECT DATE(created_at) as date, COUNT(*), SUM(total)
FROM orders
GROUP BY DATE(created_at)
ORDER BY date DESC;

-- Group by week
SELECT DATE_TRUNC('week', created_at) as week, COUNT(*), SUM(total)
FROM orders
GROUP BY DATE_TRUNC('week', created_at)
ORDER BY week DESC;

-- Business days calculation (excluding weekends)
SELECT COUNT(*) as business_days
FROM generate_series('2024-01-01'::date, '2024-01-31'::date, '1 day') as d
WHERE EXTRACT(DOW FROM d) NOT IN (0, 6);


-- ============================================
-- 6. AGGREGATION PATTERNS
-- ============================================

-- Conditional aggregation
SELECT
    COUNT(*) as total_orders,
    COUNT(*) FILTER (WHERE status = 'completed') as completed,
    COUNT(*) FILTER (WHERE status = 'pending') as pending,
    COUNT(*) FILTER (WHERE status = 'cancelled') as cancelled,
    SUM(total) FILTER (WHERE status = 'completed') as revenue,
    AVG(total) FILTER (WHERE status = 'completed') as avg_order
FROM orders
WHERE created_at >= CURRENT_DATE - INTERVAL '30 days';

-- Running total
SELECT
    date,
    amount,
    SUM(amount) OVER (ORDER BY date) as running_total
FROM daily_sales;

-- Moving average
SELECT
    date,
    amount,
    AVG(amount) OVER (
        ORDER BY date
        ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
    ) as moving_avg_7d
FROM daily_sales;

-- Rank within groups
SELECT
    department,
    name,
    salary,
    RANK() OVER (PARTITION BY department ORDER BY salary DESC) as rank
FROM employees;


-- ============================================
-- 7. UPSERT PATTERNS
-- ============================================

-- Insert or update
INSERT INTO products (id, name, price, updated_at)
VALUES ('uuid', 'Widget', 19.99, NOW())
ON CONFLICT (id) DO UPDATE SET
    name = EXCLUDED.name,
    price = EXCLUDED.price,
    updated_at = EXCLUDED.updated_at;

-- Insert if not exists
INSERT INTO products (id, name, price)
VALUES ('uuid', 'Widget', 19.99)
ON CONFLICT (id) DO NOTHING;

-- Conditional upsert
INSERT INTO products (id, name, price)
VALUES ('uuid', 'Widget', 19.99)
ON CONFLICT (id) DO UPDATE SET
    price = EXCLUDED.price
WHERE products.price < EXCLUDED.price;  -- Only update if new price is higher


-- ============================================
-- 8. HIERARCHICAL QUERIES
-- ============================================

-- Recursive CTE for tree structure
WITH RECURSIVE category_tree AS (
    -- Anchor: root categories
    SELECT id, name, parent_id, 1 as level, ARRAY[id] as path, name as full_path
    FROM categories
    WHERE parent_id IS NULL

    UNION ALL

    -- Recursive: children
    SELECT c.id, c.name, c.parent_id, ct.level + 1,
           ct.path || c.id,
           ct.full_path || ' > ' || c.name
    FROM categories c
    JOIN category_tree ct ON c.parent_id = ct.id
    WHERE c.id <> ALL(ct.path)  -- Prevent cycles
)
SELECT * FROM category_tree
ORDER BY path;

-- Get all descendants
WITH RECURSIVE descendants AS (
    SELECT id, name, parent_id
    FROM categories WHERE id = 'root-category-uuid'

    UNION ALL

    SELECT c.id, c.name, c.parent_id
    FROM categories c
    JOIN descendants d ON c.parent_id = d.id
)
SELECT * FROM descendants;

-- Get all ancestors
WITH RECURSIVE ancestors AS (
    SELECT id, name, parent_id
    FROM categories WHERE id = 'leaf-category-uuid'

    UNION ALL

    SELECT c.id, c.name, c.parent_id
    FROM categories c
    JOIN ancestors a ON c.id = a.parent_id
)
SELECT * FROM ancestors;


-- ============================================
-- 9. PERFORMANCE QUERIES
-- ============================================

-- Find slow queries (requires pg_stat_statements)
SELECT
    query,
    calls,
    mean_exec_time,
    total_exec_time,
    rows
FROM pg_stat_statements
ORDER BY mean_exec_time DESC
LIMIT 20;

-- Table sizes
SELECT
    schemaname || '.' || relname as table_name,
    pg_size_pretty(pg_total_relation_size(relid)) as total_size,
    pg_size_pretty(pg_relation_size(relid)) as data_size,
    pg_size_pretty(pg_indexes_size(relid)) as index_size
FROM pg_catalog.pg_statio_user_tables
ORDER BY pg_total_relation_size(relid) DESC;

-- Unused indexes
SELECT
    schemaname || '.' || relname as table_name,
    indexrelname as index_name,
    pg_size_pretty(pg_relation_size(indexrelid)) as index_size,
    idx_scan as number_of_scans
FROM pg_stat_user_indexes
WHERE idx_scan < 50
ORDER BY pg_relation_size(indexrelid) DESC;

-- Missing indexes (tables with more seq scans than index scans)
SELECT
    schemaname || '.' || relname as table_name,
    seq_scan,
    idx_scan,
    seq_tup_read,
    idx_tup_fetch
FROM pg_stat_user_tables
WHERE seq_scan > idx_scan
ORDER BY seq_tup_read DESC;

-- Lock monitoring
SELECT
    pg_stat_activity.pid,
    pg_stat_activity.query,
    pg_locks.locktype,
    pg_locks.mode,
    pg_locks.granted
FROM pg_stat_activity
JOIN pg_locks ON pg_stat_activity.pid = pg_locks.pid
WHERE pg_stat_activity.query != '<IDLE>'
  AND pg_locks.granted = false;


-- ============================================
-- 10. MAINTENANCE QUERIES
-- ============================================

-- Vacuum analyze table
VACUUM ANALYZE products;

-- Reindex
REINDEX INDEX idx_products_name;
REINDEX TABLE products;

-- Kill long-running queries
SELECT pg_cancel_backend(pid)
FROM pg_stat_activity
WHERE state = 'active'
  AND query_start < NOW() - INTERVAL '5 minutes'
  AND query NOT ILIKE '%pg_stat_activity%';

-- Active connections
SELECT
    datname as database,
    usename as user,
    application_name,
    state,
    query_start,
    NOW() - query_start as duration
FROM pg_stat_activity
WHERE state = 'active'
ORDER BY query_start;
