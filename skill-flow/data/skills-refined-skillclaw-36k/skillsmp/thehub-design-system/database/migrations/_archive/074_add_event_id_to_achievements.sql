-- Add event_id column to rider_achievements for linking achievements to specific events
-- This allows showing detailed information when clicking on achievements like "Svensk mästare"

ALTER TABLE rider_achievements
    ADD COLUMN IF NOT EXISTS event_id INT DEFAULT NULL,
    ADD INDEX idx_rider_achievements_event (event_id);

-- Note: Foreign key not added because events might be deleted while achievements should remain
