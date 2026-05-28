-- Migration 059: Add missing columns to event_tracks table
-- These columns are required by the map_functions.php code

-- Add route metadata columns
ALTER TABLE event_tracks ADD COLUMN route_type VARCHAR(50) NULL AFTER gpx_file;
ALTER TABLE event_tracks ADD COLUMN route_label VARCHAR(255) NULL AFTER route_type;
ALTER TABLE event_tracks ADD COLUMN color VARCHAR(7) DEFAULT '#3B82F6' AFTER route_label;

-- Add display control columns
ALTER TABLE event_tracks ADD COLUMN is_primary TINYINT(1) DEFAULT 0 AFTER color;
ALTER TABLE event_tracks ADD COLUMN display_order INT DEFAULT 0 AFTER is_primary;

-- Add raw coordinate storage for new workflow
ALTER TABLE event_tracks ADD COLUMN raw_coordinates LONGTEXT NULL AFTER bounds_west;
ALTER TABLE event_tracks ADD COLUMN raw_elevation_data LONGTEXT NULL AFTER raw_coordinates;

-- Add index columns to segments for waypoint-based segment definition
ALTER TABLE event_track_segments ADD COLUMN start_index INT NULL;
ALTER TABLE event_track_segments ADD COLUMN end_index INT NULL;

-- Add lift type to segment_type enum (if not already present)
-- Note: This may fail if 'lift' already exists, which is OK
ALTER TABLE event_track_segments MODIFY COLUMN segment_type ENUM('stage', 'liaison', 'lift') NOT NULL DEFAULT 'stage';
