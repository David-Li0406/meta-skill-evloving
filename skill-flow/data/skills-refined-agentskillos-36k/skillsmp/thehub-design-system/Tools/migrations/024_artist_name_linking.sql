-- ============================================================================
-- Migration 024: Artist Name Linking System
-- Enables linking anonymous/artist name accounts to real rider profiles
-- ============================================================================

-- Add is_anonymous flag to riders table
-- This identifies riders imported with only artist names (no real identity data)
ALTER TABLE riders
ADD COLUMN is_anonymous TINYINT(1) DEFAULT 0 AFTER active,
ADD COLUMN anonymous_source VARCHAR(100) NULL COMMENT 'Where the anonymous data came from' AFTER is_anonymous,
ADD COLUMN merged_into_rider_id INT NULL COMMENT 'If merged, points to the target rider' AFTER anonymous_source;

-- Add index for finding anonymous riders
ALTER TABLE riders
ADD INDEX idx_anonymous (is_anonymous, merged_into_rider_id);

-- Artist name claims table (extends rider_claims concept)
CREATE TABLE IF NOT EXISTS artist_name_claims (
    id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,

    -- The anonymous rider being claimed
    anonymous_rider_id INT NOT NULL,

    -- The user/rider claiming ownership
    claiming_user_id INT NULL COMMENT 'users table ID if logged in',
    claiming_rider_id INT NULL COMMENT 'riders table ID they want to merge into',

    -- Claim details
    evidence TEXT NULL COMMENT 'User explanation of why they own this artist name',
    admin_notes TEXT NULL,

    -- Status workflow
    status ENUM('pending', 'approved', 'rejected', 'merged') DEFAULT 'pending',

    -- Timestamps
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    reviewed_at DATETIME NULL,
    reviewed_by INT NULL COMMENT 'admin_users ID',
    merged_at DATETIME NULL,

    INDEX idx_anonymous (anonymous_rider_id),
    INDEX idx_claiming (claiming_rider_id),
    INDEX idx_status (status),
    INDEX idx_created (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Auto-detect and mark existing anonymous riders
-- Criteria: has firstname but no lastname, no birth_year, no club
UPDATE riders
SET is_anonymous = 1
WHERE lastname IS NULL OR lastname = ''
  AND (birth_year IS NULL OR birth_year = 0)
  AND club_id IS NULL
  AND firstname IS NOT NULL AND firstname != '';
