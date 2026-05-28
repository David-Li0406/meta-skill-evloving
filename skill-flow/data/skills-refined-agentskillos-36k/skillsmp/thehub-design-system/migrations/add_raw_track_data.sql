-- =====================================================
-- RAW TRACK DATA & SEGMENT INDEXES - Migration
-- Created: 2025-12-10
-- Description: Adds raw coordinate storage and segment position indexes
-- =====================================================

-- Add raw coordinates and elevation data to event_tracks
-- This allows the section-based segment editor to work
ALTER TABLE event_tracks
ADD COLUMN raw_coordinates JSON NULL AFTER gpx_file,
ADD COLUMN raw_elevation_data JSON NULL AFTER raw_coordinates;

-- Modify segment_type to include 'lift' option
ALTER TABLE event_track_segments
MODIFY COLUMN segment_type ENUM('stage', 'liaison', 'lift') NOT NULL DEFAULT 'stage';

-- Add start/end index columns for referencing positions in raw_coordinates
ALTER TABLE event_track_segments
ADD COLUMN start_index INT NULL AFTER elevation_data,
ADD COLUMN end_index INT NULL AFTER start_index;
