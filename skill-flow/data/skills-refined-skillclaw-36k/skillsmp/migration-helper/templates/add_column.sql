-- Migration: XXX - Add [column_name] to [table_name]
-- Description: [Why this column is needed]
-- Date: [YYYY-MM-DD]

-- Add column (nullable first for safety)
ALTER TABLE table_name
    ADD COLUMN IF NOT EXISTS column_name VARCHAR(255);

-- Populate with default value for existing rows (if needed)
UPDATE table_name
    SET column_name = 'default_value'
    WHERE column_name IS NULL;

-- Add NOT NULL constraint (optional, only if required)
-- ALTER TABLE table_name
--     ALTER COLUMN column_name SET NOT NULL;

-- Add default value constraint (optional)
-- ALTER TABLE table_name
--     ALTER COLUMN column_name SET DEFAULT 'value';

-- Create index (if column will be queried)
CREATE INDEX IF NOT EXISTS idx_table_column
    ON table_name(column_name);

-- Add comment
COMMENT ON COLUMN table_name.column_name IS '[Column description]';
