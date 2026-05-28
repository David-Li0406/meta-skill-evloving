-- Migration 050: Add series brands (parent series)
-- Date: 2025-12-08
-- Description: Creates series_brands table for grouping yearly series under a main brand.
--              Example: "Swecup 2023" and "Swecup 2024" both belong to brand "Swecup"

-- ============================================================================
-- SERIES BRANDS TABLE
-- ============================================================================
CREATE TABLE IF NOT EXISTS series_brands (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    slug VARCHAR(100) UNIQUE,
    description TEXT,
    logo VARCHAR(255),
    website VARCHAR(255),

    -- Badge styling (inherited by series if not overridden)
    gradient_start VARCHAR(7) DEFAULT '#004A98',
    gradient_end VARCHAR(7) DEFAULT '#002a5c',
    accent_color VARCHAR(7) DEFAULT '#61CE70',

    active BOOLEAN DEFAULT 1,
    display_order INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    INDEX idx_slug (slug),
    INDEX idx_active (active),
    INDEX idx_display_order (display_order)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================================
-- ADD BRAND_ID TO SERIES TABLE
-- ============================================================================
ALTER TABLE series
    ADD COLUMN brand_id INT NULL AFTER id,
    ADD INDEX idx_brand (brand_id),
    ADD CONSTRAINT fk_series_brand FOREIGN KEY (brand_id) REFERENCES series_brands(id) ON DELETE SET NULL;

-- ============================================================================
-- POPULATE INITIAL BRANDS FROM EXISTING SERIES
-- ============================================================================
-- This creates brands based on unique series names (without year suffix)
-- You may need to manually clean up / merge these afterwards

INSERT INTO series_brands (name, slug, logo, gradient_start, gradient_end, accent_color, active)
SELECT DISTINCT
    TRIM(REGEXP_REPLACE(s.name, ' ?[0-9]{4}$', '')) as name,
    LOWER(REPLACE(TRIM(REGEXP_REPLACE(s.name, ' ?[0-9]{4}$', '')), ' ', '-')) as slug,
    s.logo,
    s.gradient_start,
    s.gradient_end,
    s.accent_color,
    1
FROM series s
WHERE s.name IS NOT NULL AND s.name != ''
ON DUPLICATE KEY UPDATE name = VALUES(name);

-- Update series to link to their brands
UPDATE series s
JOIN series_brands sb ON TRIM(REGEXP_REPLACE(s.name, ' ?[0-9]{4}$', '')) = sb.name
SET s.brand_id = sb.id;
