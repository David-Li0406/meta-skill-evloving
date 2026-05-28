-- Migration 053: Payment Recipient for Events
-- Date: 2025-12-09
-- Description: Adds payment recipient choice on events (organizer vs series)
--              and links events to organizer clubs for payment routing

-- ============================================================================
-- 1. ADD PAYMENT RECIPIENT FIELD TO EVENTS
-- ============================================================================
-- Determines who receives payment for this event:
-- - 'series': Use series payment config (series.swish_number)
-- - 'organizer': Use organizer club's payment config
-- - 'custom': Use event-specific payment config (existing behavior)

ALTER TABLE events
    ADD COLUMN payment_recipient ENUM('series', 'organizer', 'custom') DEFAULT 'series' AFTER entry_fee;

-- ============================================================================
-- 2. ADD ORGANIZER CLUB LINK TO EVENTS
-- ============================================================================
-- Links event to the club that organizes it (for payment purposes)

ALTER TABLE events
    ADD COLUMN organizer_club_id INT NULL AFTER organizer,
    ADD FOREIGN KEY fk_events_organizer_club (organizer_club_id) REFERENCES clubs(id) ON DELETE SET NULL,
    ADD INDEX idx_organizer_club (organizer_club_id);

-- ============================================================================
-- 3. ADD PAYMENT FIELDS TO CLUBS
-- ============================================================================
-- Clubs (arranging clubs) can have their own Swish payment details

ALTER TABLE clubs
    ADD COLUMN swish_number VARCHAR(20) NULL,
    ADD COLUMN swish_name VARCHAR(255) NULL,
    ADD COLUMN payment_enabled TINYINT(1) DEFAULT 0;

-- ============================================================================
-- 4. ADD PAYMENT FIELDS TO SERIES (if not exists)
-- ============================================================================

-- Check and add swish_number to series if not exists
SET @col_exists = (SELECT COUNT(*) FROM information_schema.columns
    WHERE table_schema = DATABASE() AND table_name = 'series' AND column_name = 'swish_number');
SET @sql = IF(@col_exists = 0,
    'ALTER TABLE series ADD COLUMN swish_number VARCHAR(20) NULL',
    'SELECT "swish_number already exists on series"');
PREPARE stmt FROM @sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

-- Check and add swish_name to series if not exists
SET @col_exists = (SELECT COUNT(*) FROM information_schema.columns
    WHERE table_schema = DATABASE() AND table_name = 'series' AND column_name = 'swish_name');
SET @sql = IF(@col_exists = 0,
    'ALTER TABLE series ADD COLUMN swish_name VARCHAR(255) NULL',
    'SELECT "swish_name already exists on series"');
PREPARE stmt FROM @sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;
