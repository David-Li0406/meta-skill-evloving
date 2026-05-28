-- Migration 055: Segment Sponsors
-- Allows sponsors to be linked to map segments (stages)
-- Shows as "SS1 By Sponsor" on the map with optional banner
-- NOTE: Run migration 056 first to ensure sponsors table exists!

-- Add sponsor_id column to event_track_segments
-- (does NOT add foreign key - sponsors table might not exist yet)
ALTER TABLE event_track_segments
ADD COLUMN sponsor_id INT NULL AFTER segment_name;

-- Add index for faster lookups (foreign key added later if sponsors table exists)
CREATE INDEX idx_segments_sponsor ON event_track_segments(sponsor_id);
