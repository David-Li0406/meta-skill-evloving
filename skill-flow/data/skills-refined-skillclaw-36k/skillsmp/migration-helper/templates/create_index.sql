-- Migration: XXX - Create index on [table_name].[column_name]
-- Description: Improve query performance for [specific query pattern]
-- Date: [YYYY-MM-DD]

-- Single column index
CREATE INDEX IF NOT EXISTS idx_table_column
    ON table_name(column_name);

-- Multi-column index (for queries with multiple WHERE conditions)
CREATE INDEX IF NOT EXISTS idx_table_col1_col2
    ON table_name(column1, column2);

-- Descending index (for ORDER BY ... DESC queries)
CREATE INDEX IF NOT EXISTS idx_table_column_desc
    ON table_name(column_name DESC);

-- Partial index (for filtered queries, saves space)
CREATE INDEX IF NOT EXISTS idx_table_active
    ON table_name(column_name)
    WHERE status = 'active';

-- Unique index (enforce uniqueness)
CREATE UNIQUE INDEX IF NOT EXISTS idx_table_unique_column
    ON table_name(column_name);

-- Expression index (for computed values)
CREATE INDEX IF NOT EXISTS idx_table_lower_name
    ON table_name(LOWER(name));

-- GIN index (for JSONB, arrays, full-text search)
CREATE INDEX IF NOT EXISTS idx_table_jsonb
    ON table_name USING GIN (jsonb_column);

-- For large tables, use CONCURRENTLY to avoid locking
-- CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_table_column
--     ON table_name(column_name);
