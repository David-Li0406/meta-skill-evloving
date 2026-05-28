-- ============================================================================
-- TheHUB Performance Indexes
-- Add these indexes BEFORE launch for optimal performance
-- ============================================================================

-- Check existing indexes first:
-- SELECT TABLE_NAME, INDEX_NAME, GROUP_CONCAT(COLUMN_NAME) as COLUMNS
-- FROM INFORMATION_SCHEMA.STATISTICS
-- WHERE TABLE_SCHEMA = DATABASE()
-- GROUP BY TABLE_NAME, INDEX_NAME;

USE u994733455_thehub;

-- ============================================================================
-- RIDERS TABLE - Authentication and Lookup
-- ============================================================================

-- Email lookup (login, registration, password reset)
CREATE INDEX IF NOT EXISTS idx_riders_email ON riders(email);

-- Active riders filter
CREATE INDEX IF NOT EXISTS idx_riders_active ON riders(active);

-- Club membership queries
CREATE INDEX IF NOT EXISTS idx_riders_club_id ON riders(club_id);

-- Password reset token lookup (critical for security)
CREATE INDEX IF NOT EXISTS idx_riders_reset_token ON riders(password_reset_token);

-- Password reset expiry check
CREATE INDEX IF NOT EXISTS idx_riders_reset_expires ON riders(password_reset_expires);

-- Last login tracking
CREATE INDEX IF NOT EXISTS idx_riders_last_login ON riders(last_login);

-- ============================================================================
-- RESULTS TABLE - Performance Critical
-- ============================================================================

-- Rider results lookup (rider-profile.php)
CREATE INDEX IF NOT EXISTS idx_results_cyclist_id ON results(cyclist_id);

-- Event results lookup
CREATE INDEX IF NOT EXISTS idx_results_event_id ON results(event_id);

-- Status filtering (finished, dnf, dns)
CREATE INDEX IF NOT EXISTS idx_results_status ON results(status);

-- Series standings calculations
CREATE INDEX IF NOT EXISTS idx_results_series_lookup ON results(cyclist_id, status, points);

-- Category/class filtering
CREATE INDEX IF NOT EXISTS idx_results_category_id ON results(category_id);

-- ============================================================================
-- EVENT_TICKETS TABLE - Ticketing System
-- ============================================================================

-- Rider tickets lookup (my-tickets.php)
CREATE INDEX IF NOT EXISTS idx_event_tickets_rider_id ON event_tickets(rider_id);

-- Event tickets lookup
CREATE INDEX IF NOT EXISTS idx_event_tickets_event_id ON event_tickets(event_id);

-- Status filtering (sold, refunded, etc)
CREATE INDEX IF NOT EXISTS idx_event_tickets_status ON event_tickets(status);

-- Ticket number lookup
CREATE INDEX IF NOT EXISTS idx_event_tickets_number ON event_tickets(ticket_number);

-- ============================================================================
-- EVENT_REFUND_REQUESTS TABLE - Refund Management
-- ============================================================================

-- Ticket refund lookup
CREATE INDEX IF NOT EXISTS idx_refund_requests_ticket_id ON event_refund_requests(ticket_id);

-- Rider refund requests
CREATE INDEX IF NOT EXISTS idx_refund_requests_rider_id ON event_refund_requests(rider_id);

-- Status filtering (pending, approved, rejected)
CREATE INDEX IF NOT EXISTS idx_refund_requests_status ON event_refund_requests(status);

-- ============================================================================
-- EVENT_REGISTRATIONS TABLE - Registration System
-- ============================================================================

-- Event registrations lookup
CREATE INDEX IF NOT EXISTS idx_event_registrations_event_id ON event_registrations(event_id);

-- Rider registrations lookup
CREATE INDEX IF NOT EXISTS idx_event_registrations_rider_id ON event_registrations(rider_id);

-- Status filtering (pending, confirmed, cancelled)
CREATE INDEX IF NOT EXISTS idx_event_registrations_status ON event_registrations(status);

-- Payment status tracking
CREATE INDEX IF NOT EXISTS idx_event_registrations_payment ON event_registrations(payment_status);

-- Composite index for duplicate check (api/registration.php:201)
CREATE INDEX IF NOT EXISTS idx_event_registrations_unique_check
  ON event_registrations(event_id, rider_id, status);

-- ============================================================================
-- EVENTS TABLE - Event Queries
-- ============================================================================

-- Date-based queries (upcoming/past events)
CREATE INDEX IF NOT EXISTS idx_events_date ON events(date);

-- Series events lookup
CREATE INDEX IF NOT EXISTS idx_events_series_id ON events(series_id);

-- Active events filter
CREATE INDEX IF NOT EXISTS idx_events_active ON events(active);

-- ============================================================================
-- SERIES TABLE - Series Standings
-- ============================================================================

-- Year-based queries
CREATE INDEX IF NOT EXISTS idx_series_year ON series(year);

-- Active series filter
CREATE INDEX IF NOT EXISTS idx_series_active ON series(active);

-- ============================================================================
-- SERIES_EVENTS TABLE - Series-Event Relationships
-- ============================================================================

-- Series events lookup
CREATE INDEX IF NOT EXISTS idx_series_events_series_id ON series_events(series_id);

-- Event's series lookup
CREATE INDEX IF NOT EXISTS idx_series_events_event_id ON series_events(event_id);

-- ============================================================================
-- CLUB_RIDER_POINTS TABLE - Club Points System
-- ============================================================================

-- Rider club points
CREATE INDEX IF NOT EXISTS idx_club_rider_points_rider_id ON club_rider_points(rider_id);

-- Club standings
CREATE INDEX IF NOT EXISTS idx_club_rider_points_club_id ON club_rider_points(club_id);

-- Series club standings
CREATE INDEX IF NOT EXISTS idx_club_rider_points_series_id ON club_rider_points(series_id);

-- Event club points
CREATE INDEX IF NOT EXISTS idx_club_rider_points_event_id ON club_rider_points(event_id);

-- ============================================================================
-- CLUBS TABLE - Club Queries
-- ============================================================================

-- Active clubs filter
CREATE INDEX IF NOT EXISTS idx_clubs_active ON clubs(active);

-- ============================================================================
-- ADMIN_USERS TABLE - Admin Authentication
-- ============================================================================

-- Username lookup (login)
CREATE INDEX IF NOT EXISTS idx_admin_users_username ON admin_users(username);

-- Active admin filter
CREATE INDEX IF NOT EXISTS idx_admin_users_active ON admin_users(active);

-- Role-based queries
CREATE INDEX IF NOT EXISTS idx_admin_users_role ON admin_users(role);

-- ============================================================================
-- Verify indexes were created
-- ============================================================================

SELECT
    TABLE_NAME,
    INDEX_NAME,
    CARDINALITY,
    GROUP_CONCAT(COLUMN_NAME ORDER BY SEQ_IN_INDEX) as COLUMNS
FROM INFORMATION_SCHEMA.STATISTICS
WHERE TABLE_SCHEMA = DATABASE()
  AND TABLE_NAME IN (
    'riders', 'results', 'event_tickets', 'event_refund_requests',
    'event_registrations', 'events', 'series', 'series_events',
    'club_rider_points', 'clubs', 'admin_users'
  )
GROUP BY TABLE_NAME, INDEX_NAME
ORDER BY TABLE_NAME, INDEX_NAME;

-- ============================================================================
-- Performance Check Queries
-- ============================================================================

-- Check table sizes
SELECT
    TABLE_NAME,
    TABLE_ROWS as 'Rows',
    ROUND(DATA_LENGTH / 1024 / 1024, 2) as 'Data (MB)',
    ROUND(INDEX_LENGTH / 1024 / 1024, 2) as 'Index (MB)',
    ROUND((DATA_LENGTH + INDEX_LENGTH) / 1024 / 1024, 2) as 'Total (MB)'
FROM INFORMATION_SCHEMA.TABLES
WHERE TABLE_SCHEMA = DATABASE()
  AND TABLE_TYPE = 'BASE TABLE'
ORDER BY (DATA_LENGTH + INDEX_LENGTH) DESC;

-- ============================================================================
-- Done!
-- ============================================================================
