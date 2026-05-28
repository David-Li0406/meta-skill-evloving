-- =====================================================
-- MULTI-TRACK SUPPORT - Migration
-- Created: 2025-12-10
-- Description: Adds support for multiple GPX tracks per event
-- =====================================================

-- Add route classification to event_tracks
ALTER TABLE event_tracks
ADD COLUMN route_type VARCHAR(50) NULL AFTER name,
ADD COLUMN route_label VARCHAR(100) NULL AFTER route_type,
ADD COLUMN is_primary TINYINT(1) DEFAULT 0 AFTER route_label,
ADD COLUMN display_order INT DEFAULT 0 AFTER is_primary,
ADD COLUMN color VARCHAR(7) DEFAULT '#3B82F6' AFTER display_order;

-- Index for fetching tracks by event
ALTER TABLE event_tracks
ADD INDEX idx_event_tracks_order (event_id, display_order);

-- Update existing tracks to be primary
UPDATE event_tracks SET is_primary = 1 WHERE is_primary = 0;
