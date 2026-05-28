-- Migration 064: Add color columns to series table if missing
-- Date: 2025-12-13
-- Description: Ensures series table has gradient_start, gradient_end, accent_color columns

-- Add columns if they don't exist
ALTER TABLE series
    ADD COLUMN IF NOT EXISTS gradient_start VARCHAR(7) DEFAULT '#004A98',
    ADD COLUMN IF NOT EXISTS gradient_end VARCHAR(7) DEFAULT '#002a5c',
    ADD COLUMN IF NOT EXISTS accent_color VARCHAR(7) DEFAULT '#61CE70';

-- Set default values for existing rows that have NULL
UPDATE series SET gradient_start = '#004A98' WHERE gradient_start IS NULL;
UPDATE series SET gradient_end = '#002a5c' WHERE gradient_end IS NULL;
UPDATE series SET accent_color = '#61CE70' WHERE accent_color IS NULL;
