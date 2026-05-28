-- Migration: Add publish date/time fields for event tabs
-- This allows admins to prepare content before making it visible

-- Starttider publish date/time
ALTER TABLE events ADD COLUMN IF NOT EXISTS starttider_publish_at DATETIME NULL AFTER start_times_use_global;

-- Karta/Map publish date/time
ALTER TABLE events ADD COLUMN IF NOT EXISTS karta_publish_at DATETIME NULL AFTER map_use_global;

-- Registration deadline time (to complement the date)
ALTER TABLE events ADD COLUMN IF NOT EXISTS registration_deadline_time TIME NULL AFTER registration_deadline;

-- Index for efficient queries on publish dates
CREATE INDEX IF NOT EXISTS idx_events_starttider_publish ON events(starttider_publish_at);
CREATE INDEX IF NOT EXISTS idx_events_karta_publish ON events(karta_publish_at);
