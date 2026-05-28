-- Migration 070: Add columns for onsite registration tracking
-- Adds registration_source and registered_by_user_id to event_registrations

-- Add registration_source column to track where registration came from
ALTER TABLE event_registrations
ADD COLUMN IF NOT EXISTS registration_source ENUM('online', 'onsite') DEFAULT 'online'
AFTER registration_date;

-- Add registered_by_user_id to track which organizer registered the participant
ALTER TABLE event_registrations
ADD COLUMN IF NOT EXISTS registered_by_user_id INT NULL
AFTER registration_source;

-- Add foreign key constraint (optional, depends on your setup)
-- ALTER TABLE event_registrations
-- ADD CONSTRAINT fk_registered_by_user
-- FOREIGN KEY (registered_by_user_id) REFERENCES admin_users(id) ON DELETE SET NULL;

-- Add index for filtering by source
CREATE INDEX IF NOT EXISTS idx_registration_source ON event_registrations(registration_source);
