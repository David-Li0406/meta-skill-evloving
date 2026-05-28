-- ============================================================================
-- Migration 011: Brand Dimension for Journey Analysis
-- Version: 3.1.2
-- Created: 2026-01-16
-- Fixed: 2026-01-16 - Simplified for PHP compatibility (no dynamic SQL)
--
-- PURPOSE:
-- Adds brand filtering capability to First Season Journey and Longitudinal
-- Journey analysis. Enables comparison across up to 12 brands.
--
-- IMPORTANT: Run migrations 009 and 010 FIRST!
-- ============================================================================

-- ============================================================================
-- ALTER: rider_first_season - Add brand tracking
-- These will fail silently if columns already exist (run anyway)
-- ============================================================================
ALTER TABLE rider_first_season ADD COLUMN first_brand_id INT NULL;
ALTER TABLE rider_first_season ADD COLUMN first_series_id INT NULL;
ALTER TABLE rider_first_season ADD INDEX idx_first_brand (first_brand_id);
ALTER TABLE rider_first_season ADD INDEX idx_cohort_brand (cohort_year, first_brand_id);

-- ============================================================================
-- ALTER: rider_journey_years - Add brand tracking per year
-- ============================================================================
ALTER TABLE rider_journey_years ADD COLUMN primary_brand_id INT NULL;
ALTER TABLE rider_journey_years ADD COLUMN primary_series_id INT NULL;
ALTER TABLE rider_journey_years ADD INDEX idx_brand (primary_brand_id);
ALTER TABLE rider_journey_years ADD INDEX idx_cohort_offset_brand (cohort_year, year_offset, primary_brand_id);

-- ============================================================================
-- ALTER: rider_journey_summary - Add first brand reference
-- ============================================================================
ALTER TABLE rider_journey_summary ADD COLUMN fs_first_brand_id INT NULL;

-- ============================================================================
-- TABLE: brand_journey_aggregates
-- Pre-calculated brand-level aggregates for fast reporting
-- ============================================================================
CREATE TABLE IF NOT EXISTS brand_journey_aggregates (
    id INT AUTO_INCREMENT PRIMARY KEY,

    brand_id INT NOT NULL,
    cohort_year YEAR NOT NULL,
    year_offset TINYINT NOT NULL,

    total_riders INT NOT NULL,
    active_riders INT NOT NULL,
    retention_rate DECIMAL(5,4) DEFAULT NULL,

    avg_starts DECIMAL(6,2) DEFAULT NULL,
    avg_events DECIMAL(6,2) DEFAULT NULL,
    avg_dnf_rate DECIMAL(5,4) DEFAULT NULL,

    avg_percentile DECIMAL(5,2) DEFAULT NULL,
    pct_with_podium DECIMAL(5,4) DEFAULT NULL,

    pct_continuous_4yr DECIMAL(5,4) DEFAULT NULL,
    pct_one_and_done DECIMAL(5,4) DEFAULT NULL,
    pct_gap_returner DECIMAL(5,4) DEFAULT NULL,

    pct_multi_brand DECIMAL(5,4) DEFAULT NULL,

    calculated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    snapshot_id INT DEFAULT NULL,

    INDEX idx_brand_cohort (brand_id, cohort_year),
    INDEX idx_cohort_offset (cohort_year, year_offset),
    INDEX idx_snapshot (snapshot_id),

    UNIQUE KEY uk_brand_cohort_offset (brand_id, cohort_year, year_offset, snapshot_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================================
-- Migration complete marker
-- ============================================================================
INSERT INTO analytics_system_config (config_key, config_value, description)
VALUES
    ('journey_brand_dimension_version', '3.1.2', 'Journey brand dimension version'),
    ('journey_max_brand_comparison', '12', 'Maximum brands for comparison'),
    ('journey_brand_enabled', 'true', 'Enable brand filtering for journey analysis')
ON DUPLICATE KEY UPDATE config_value = VALUES(config_value);
