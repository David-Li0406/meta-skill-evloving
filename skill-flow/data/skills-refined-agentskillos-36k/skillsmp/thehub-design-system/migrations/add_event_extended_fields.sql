-- Add extended event information fields
-- Run this migration to add fields for comprehensive event pages

ALTER TABLE events
ADD COLUMN IF NOT EXISTS schedule TEXT COMMENT 'Event schedule/timetable (JSON or formatted text)',
ADD COLUMN IF NOT EXISTS practical_info TEXT COMMENT 'Practical information (parking, food, facilities)',
ADD COLUMN IF NOT EXISTS safety_rules TEXT COMMENT 'Safety and competition rules',
ADD COLUMN IF NOT EXISTS course_description TEXT COMMENT 'Detailed course/track description',
ADD COLUMN IF NOT EXISTS course_map_url VARCHAR(500) COMMENT 'URL to course map image',
ADD COLUMN IF NOT EXISTS gpx_file_url VARCHAR(500) COMMENT 'URL to GPX file download',
ADD COLUMN IF NOT EXISTS contact_email VARCHAR(255) COMMENT 'Contact email for event',
ADD COLUMN IF NOT EXISTS contact_phone VARCHAR(50) COMMENT 'Contact phone number',
ADD COLUMN IF NOT EXISTS parking_info TEXT COMMENT 'Parking information and directions',
ADD COLUMN IF NOT EXISTS accommodation_info TEXT COMMENT 'Accommodation and lodging information',
ADD COLUMN IF NOT EXISTS food_info TEXT COMMENT 'Food and catering information',
ADD COLUMN IF NOT EXISTS prizes_info TEXT COMMENT 'Prize information',
ADD COLUMN IF NOT EXISTS sponsors TEXT COMMENT 'Sponsor information';

-- Add indices for commonly queried fields
CREATE INDEX IF NOT EXISTS idx_events_date ON events(date);
CREATE INDEX IF NOT EXISTS idx_events_series_id ON events(series_id);
CREATE INDEX IF NOT EXISTS idx_events_status ON events(status);
