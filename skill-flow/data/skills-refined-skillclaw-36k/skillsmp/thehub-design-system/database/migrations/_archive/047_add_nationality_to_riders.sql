-- Migration 047: Add nationality field to riders
-- Date: 2025-12-05
-- Description: Adds nationality field with SWE as default for Swedish riders.
--              Can be set during result import for international riders.

-- Add nationality column
ALTER TABLE riders
    ADD COLUMN nationality VARCHAR(3) DEFAULT 'SWE' AFTER gender;

-- Add index for filtering by nationality
ALTER TABLE riders
    ADD INDEX idx_nationality (nationality);
