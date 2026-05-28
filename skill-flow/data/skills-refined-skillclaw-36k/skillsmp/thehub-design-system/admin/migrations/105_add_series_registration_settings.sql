-- Migration 105: Add registration settings to series table
-- Enables series-level registration configuration

-- Registration enable/disable
ALTER TABLE series ADD COLUMN IF NOT EXISTS registration_enabled TINYINT(1) DEFAULT 0;

-- When registration opens (date + time)
ALTER TABLE series ADD COLUMN IF NOT EXISTS registration_opens DATE NULL;
ALTER TABLE series ADD COLUMN IF NOT EXISTS registration_opens_time TIME NULL;

-- When registration closes (date + time) - deadline
ALTER TABLE series ADD COLUMN IF NOT EXISTS registration_closes DATE NULL;
ALTER TABLE series ADD COLUMN IF NOT EXISTS registration_closes_time TIME NULL;

-- Default pricing template for series events
ALTER TABLE series ADD COLUMN IF NOT EXISTS pricing_template_id INT NULL;

-- Index for pricing template lookups
ALTER TABLE series ADD INDEX IF NOT EXISTS idx_series_pricing_template (pricing_template_id);
