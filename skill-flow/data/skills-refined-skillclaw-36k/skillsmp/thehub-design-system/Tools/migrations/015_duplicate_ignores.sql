-- Migration: 015_duplicate_ignores
-- Table for tracking rider pairs marked as "not duplicates"

CREATE TABLE IF NOT EXISTS rider_duplicate_ignores (
    id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    rider1_id INT UNSIGNED NOT NULL,
    rider2_id INT UNSIGNED NOT NULL,
    ignored_by INT UNSIGNED NULL COMMENT 'Admin user who marked as not duplicate',
    ignored_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    reason VARCHAR(255) NULL COMMENT 'Optional reason for ignoring',

    -- Prevent duplicate entries (rider1_id should always be < rider2_id by convention)
    UNIQUE KEY uq_rider_pair (rider1_id, rider2_id),

    -- Indexes for lookup
    INDEX idx_rider1 (rider1_id),
    INDEX idx_rider2 (rider2_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Also ensure rider_merge_map exists (for tracking merged riders)
CREATE TABLE IF NOT EXISTS rider_merge_map (
    id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    canonical_rider_id INT UNSIGNED NOT NULL COMMENT 'The rider that was kept',
    merged_rider_id INT UNSIGNED NOT NULL COMMENT 'The rider that was removed',
    reason VARCHAR(50) DEFAULT 'manual' COMMENT 'How merge was detected: manual, duplicate_service, import',
    confidence TINYINT UNSIGNED DEFAULT 100 COMMENT '0-100 confidence score',
    status ENUM('pending', 'approved', 'rejected') DEFAULT 'approved',
    merged_by INT UNSIGNED NULL COMMENT 'Admin who performed merge',
    merged_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    UNIQUE KEY uq_merged_rider (merged_rider_id),
    INDEX idx_canonical (canonical_rider_id),
    INDEX idx_status (status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
