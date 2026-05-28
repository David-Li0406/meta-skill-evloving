-- Migration 021: Championship Events & Legend Level
-- Adds support for marking events as Swedish Championships
-- Adds Legend experience level

-- Add championship flag to events
ALTER TABLE events
ADD COLUMN IF NOT EXISTS is_championship TINYINT(1) DEFAULT 0
COMMENT 'Markerar eventet som Svenskt Mästerskap';

-- Add index for championship events
CREATE INDEX IF NOT EXISTS idx_championship ON events(is_championship);

-- Note: Legend level (6) is calculated dynamically based on:
-- - 5+ seasons active
-- - At least 1 series championship win
-- No schema change needed for this - handled in PHP code
