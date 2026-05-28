-- Migration: Add publish date/time field for PM tab
-- This allows admins to prepare PM content before making it visible

-- PM publish date/time
ALTER TABLE events ADD COLUMN IF NOT EXISTS pm_publish_at DATETIME NULL AFTER pm_use_global;

-- Index for efficient queries
CREATE INDEX IF NOT EXISTS idx_events_pm_publish ON events(pm_publish_at);
