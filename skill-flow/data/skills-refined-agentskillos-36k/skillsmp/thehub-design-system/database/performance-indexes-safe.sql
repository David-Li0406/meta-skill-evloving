-- ============================================================================
-- TheHUB Performance Indexes (Safe Version)
-- Only indexes for core tables that definitely exist
-- ============================================================================

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
    'riders', 'results', 'events', 'series', 'clubs', 'admin_users'
  )
GROUP BY TABLE_NAME, INDEX_NAME
ORDER BY TABLE_NAME, INDEX_NAME;

-- ============================================================================
-- Performance Check
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
