-- Migration: XXX - Add foreign key from [child_table] to [parent_table]
-- Description: [Why this relationship is needed]
-- Date: [YYYY-MM-DD]

-- Ensure parent records exist (optional, for safety)
DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM parent_table WHERE id = 0) THEN
        INSERT INTO parent_table (id, name) VALUES (0, 'Unknown');
    END IF;
END $$;

-- Set default value for existing NULL foreign keys (optional)
UPDATE child_table
    SET parent_id = 0
    WHERE parent_id IS NULL;

-- Create index on foreign key (ALWAYS do this before adding constraint)
CREATE INDEX IF NOT EXISTS idx_child_parent
    ON child_table(parent_id);

-- Add foreign key constraint
ALTER TABLE child_table
    ADD CONSTRAINT fk_child_parent
    FOREIGN KEY (parent_id)
    REFERENCES parent_table(id)
    ON DELETE SET NULL;  -- Options: CASCADE, SET NULL, RESTRICT, NO ACTION

-- Add comment
COMMENT ON COLUMN child_table.parent_id IS 'Foreign key to parent_table';
