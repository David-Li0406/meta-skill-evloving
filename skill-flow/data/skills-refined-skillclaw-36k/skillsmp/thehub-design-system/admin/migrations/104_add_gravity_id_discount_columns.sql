-- Migration 104: Add gravity_id_discount columns to series and events tables
-- This allows configuring Gravity ID discount per series or event

-- Add to series table (if not exists)
ALTER TABLE series ADD COLUMN IF NOT EXISTS gravity_id_discount DECIMAL(10,2) DEFAULT 0;

-- Add to events table (if not exists)
ALTER TABLE events ADD COLUMN IF NOT EXISTS gravity_id_discount DECIMAL(10,2) DEFAULT 0;

-- Add index for quick lookups
-- ALTER TABLE series ADD INDEX IF NOT EXISTS idx_gravity_id_discount (gravity_id_discount);
-- ALTER TABLE events ADD INDEX IF NOT EXISTS idx_gravity_id_discount (gravity_id_discount);
