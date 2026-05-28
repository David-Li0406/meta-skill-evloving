-- Migration 076: Add historical_data_verified column to series
-- Allows marking series as verified after manual data cleanup

ALTER TABLE series
    ADD COLUMN IF NOT EXISTS historical_data_verified TINYINT(1) DEFAULT 0;

-- All 2025 series are considered verified by default
UPDATE series SET historical_data_verified = 1 WHERE year >= 2025;
