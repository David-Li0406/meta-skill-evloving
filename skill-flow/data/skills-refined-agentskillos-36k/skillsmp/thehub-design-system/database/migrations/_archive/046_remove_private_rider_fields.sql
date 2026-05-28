-- Migration 046: Remove private rider fields (GDPR data minimization)
-- Date: 2025-12-05
-- Description: Removes personal contact and address fields from riders table
--              to comply with data minimization principles.
--              District field is retained for regional statistics.

-- Remove indexes first
ALTER TABLE riders DROP INDEX IF EXISTS idx_postal_code;

-- Remove columns
ALTER TABLE riders
    DROP COLUMN IF EXISTS phone,
    DROP COLUMN IF EXISTS emergency_contact,
    DROP COLUMN IF EXISTS city,
    DROP COLUMN IF EXISTS address,
    DROP COLUMN IF EXISTS postal_code;

-- Update table comment
ALTER TABLE riders COMMENT = 'Rider profiles. District field used for regional statistics.';
