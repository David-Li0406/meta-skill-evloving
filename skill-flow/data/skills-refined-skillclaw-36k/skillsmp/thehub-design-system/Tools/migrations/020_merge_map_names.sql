-- ============================================================================
-- Add merged rider name columns to rider_merge_map
-- This allows import to detect if a name belongs to a previously merged rider
-- ============================================================================

-- Add columns to store the merged rider's name
ALTER TABLE rider_merge_map
ADD COLUMN IF NOT EXISTS merged_firstname VARCHAR(100) NULL COMMENT 'Fornamn pa den borttagna dubbletten',
ADD COLUMN IF NOT EXISTS merged_lastname VARCHAR(100) NULL COMMENT 'Efternamn pa den borttagna dubbletten',
ADD COLUMN IF NOT EXISTS merged_license_number VARCHAR(50) NULL COMMENT 'License/UCI ID pa den borttagna dubbletten';

-- Add index for name lookups
ALTER TABLE rider_merge_map
ADD INDEX IF NOT EXISTS idx_merged_name (merged_firstname, merged_lastname);
