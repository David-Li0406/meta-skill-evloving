-- ============================================================================
-- TheHUB Performance Indexes - Event System Tables
-- Run this AFTER performance-indexes-safe.sql
-- ============================================================================

USE u994733455_thehub;

-- ============================================================================
-- EVENT_TICKETS TABLE - Ticketing System (if exists)
-- ============================================================================

CREATE INDEX IF NOT EXISTS idx_event_tickets_rider_id ON event_tickets(rider_id);
CREATE INDEX IF NOT EXISTS idx_event_tickets_event_id ON event_tickets(event_id);
CREATE INDEX IF NOT EXISTS idx_event_tickets_status ON event_tickets(status);
CREATE INDEX IF NOT EXISTS idx_event_tickets_number ON event_tickets(ticket_number);

-- ============================================================================
-- EVENT_REGISTRATIONS TABLE - Registration System (if exists)
-- ============================================================================

CREATE INDEX IF NOT EXISTS idx_event_registrations_event_id ON event_registrations(event_id);
CREATE INDEX IF NOT EXISTS idx_event_registrations_rider_id ON event_registrations(rider_id);
CREATE INDEX IF NOT EXISTS idx_event_registrations_status ON event_registrations(status);
CREATE INDEX IF NOT EXISTS idx_event_registrations_payment ON event_registrations(payment_status);
CREATE INDEX IF NOT EXISTS idx_event_registrations_unique_check ON event_registrations(event_id, rider_id, status);

-- ============================================================================
-- SERIES_EVENTS TABLE - Series-Event Relationships (if exists)
-- ============================================================================

CREATE INDEX IF NOT EXISTS idx_series_events_series_id ON series_events(series_id);
CREATE INDEX IF NOT EXISTS idx_series_events_event_id ON series_events(event_id);

-- ============================================================================
-- CLUB_RIDER_POINTS TABLE - Club Points System (if exists)
-- ============================================================================

CREATE INDEX IF NOT EXISTS idx_club_rider_points_rider_id ON club_rider_points(rider_id);
CREATE INDEX IF NOT EXISTS idx_club_rider_points_club_id ON club_rider_points(club_id);
CREATE INDEX IF NOT EXISTS idx_club_rider_points_series_id ON club_rider_points(series_id);
CREATE INDEX IF NOT EXISTS idx_club_rider_points_event_id ON club_rider_points(event_id);

-- ============================================================================
-- Verify
-- ============================================================================

SELECT
    TABLE_NAME,
    INDEX_NAME,
    GROUP_CONCAT(COLUMN_NAME ORDER BY SEQ_IN_INDEX) as COLUMNS
FROM INFORMATION_SCHEMA.STATISTICS
WHERE TABLE_SCHEMA = DATABASE()
  AND TABLE_NAME IN ('event_tickets', 'event_registrations', 'series_events', 'club_rider_points')
GROUP BY TABLE_NAME, INDEX_NAME
ORDER BY TABLE_NAME, INDEX_NAME;
