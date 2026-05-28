-- Migration 109: Add event_license_class to series
-- Stores which license class rules apply (national/sportmotion/motion)

ALTER TABLE series ADD COLUMN IF NOT EXISTS event_license_class VARCHAR(20) DEFAULT 'sportmotion';

-- Set default based on series name
UPDATE series SET event_license_class = 'national' WHERE name LIKE '%SM %' OR name LIKE '%Swedish Championship%';
UPDATE series SET event_license_class = 'sportmotion' WHERE event_license_class IS NULL OR event_license_class = '';
