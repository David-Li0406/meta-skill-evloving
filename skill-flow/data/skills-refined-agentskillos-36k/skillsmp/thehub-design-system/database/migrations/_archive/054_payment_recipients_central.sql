-- Migration 054: Central Payment Recipients
-- Date: 2025-12-11
-- Description: Creates a central table for payment recipients (Swish accounts)
--              that can be reused across series and events.

-- ============================================================================
-- 1. CREATE PAYMENT_RECIPIENTS TABLE
-- ============================================================================
-- Central table for all Swish payment accounts

CREATE TABLE IF NOT EXISTS payment_recipients (
    id INT AUTO_INCREMENT PRIMARY KEY,

    -- Display info
    name VARCHAR(100) NOT NULL,              -- "GravitySeries", "Järvsö IF"
    description VARCHAR(255) NULL,           -- "Centralt konto för GS-serier"

    -- Swish details
    swish_number VARCHAR(20) NOT NULL,       -- "070-1234567" or "123-456 78 90"
    swish_name VARCHAR(100) NOT NULL,        -- Name shown in Swish app

    -- Settings
    active TINYINT(1) DEFAULT 1,

    -- Metadata
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    -- Indexes
    INDEX idx_active (active),
    INDEX idx_swish_number (swish_number)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================================
-- 2. ADD PAYMENT_RECIPIENT_ID TO SERIES
-- ============================================================================

ALTER TABLE series
    ADD COLUMN payment_recipient_id INT NULL AFTER swish_name,
    ADD FOREIGN KEY fk_series_payment_recipient (payment_recipient_id)
        REFERENCES payment_recipients(id) ON DELETE SET NULL,
    ADD INDEX idx_series_payment_recipient (payment_recipient_id);

-- ============================================================================
-- 3. ADD PAYMENT_RECIPIENT_ID TO EVENTS
-- ============================================================================

ALTER TABLE events
    ADD COLUMN payment_recipient_id INT NULL AFTER payment_recipient,
    ADD FOREIGN KEY fk_events_payment_recipient (payment_recipient_id)
        REFERENCES payment_recipients(id) ON DELETE SET NULL,
    ADD INDEX idx_events_payment_recipient (payment_recipient_id);

-- ============================================================================
-- 4. MIGRATE EXISTING DATA
-- ============================================================================
-- Create payment recipients from existing series with Swish info

INSERT INTO payment_recipients (name, swish_number, swish_name, description)
SELECT DISTINCT
    s.name,
    s.swish_number,
    COALESCE(s.swish_name, s.name),
    CONCAT('Migrerat från serie: ', s.name)
FROM series s
WHERE s.swish_number IS NOT NULL AND s.swish_number != ''
ON DUPLICATE KEY UPDATE name = name;

-- Link series back to their created payment recipients
UPDATE series s
JOIN payment_recipients pr ON s.swish_number = pr.swish_number
SET s.payment_recipient_id = pr.id
WHERE s.swish_number IS NOT NULL AND s.swish_number != '';

-- Create payment recipients from clubs with Swish info
INSERT INTO payment_recipients (name, swish_number, swish_name, description)
SELECT DISTINCT
    c.name,
    c.swish_number,
    COALESCE(c.swish_name, c.name),
    CONCAT('Klubbkonto: ', c.name)
FROM clubs c
WHERE c.swish_number IS NOT NULL AND c.swish_number != ''
AND c.swish_number NOT IN (SELECT swish_number FROM payment_recipients)
ON DUPLICATE KEY UPDATE name = name;

-- ============================================================================
-- 5. UPDATE PAYMENT_RECIPIENT ENUM ON EVENTS
-- ============================================================================
-- Change 'custom' to 'event' and add 'none' option

ALTER TABLE events
    MODIFY COLUMN payment_recipient ENUM('series', 'organizer', 'event', 'none') DEFAULT 'series';
