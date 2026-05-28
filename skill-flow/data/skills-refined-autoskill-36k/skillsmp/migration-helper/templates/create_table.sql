-- Migration: XXX - Create [table_name] table
-- Description: [Purpose of this table]
-- Author: [Your name or system]
-- Date: [YYYY-MM-DD]

-- Create main table
CREATE TABLE IF NOT EXISTS table_name (
    -- Primary key
    id SERIAL PRIMARY KEY,

    -- Required fields
    name VARCHAR(255) NOT NULL,
    status VARCHAR(50) NOT NULL DEFAULT 'active',

    -- Optional fields
    description TEXT,
    metadata JSONB,

    -- Foreign keys (if any)
    parent_id INTEGER,

    -- Timestamps
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes
CREATE INDEX IF NOT EXISTS idx_table_name_name
    ON table_name(name);

CREATE INDEX IF NOT EXISTS idx_table_name_status
    ON table_name(status);

CREATE INDEX IF NOT EXISTS idx_table_name_created
    ON table_name(created_at DESC);

-- Foreign key indexes
CREATE INDEX IF NOT EXISTS idx_table_name_parent
    ON table_name(parent_id);

-- Add foreign key constraints
ALTER TABLE table_name
    ADD CONSTRAINT fk_table_parent
    FOREIGN KEY (parent_id)
    REFERENCES parent_table(id)
    ON DELETE SET NULL;  -- or CASCADE, RESTRICT

-- Add comments
COMMENT ON TABLE table_name IS '[Table description]';
COMMENT ON COLUMN table_name.name IS '[Column description]';
COMMENT ON COLUMN table_name.status IS '[Status values: active, inactive, etc.]';
COMMENT ON COLUMN table_name.metadata IS '[Metadata in JSON format]';
