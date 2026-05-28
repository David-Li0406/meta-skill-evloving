-- ============================================================================
-- Migration 007: Brands Tables
-- Creates missing brands and brand_series_map tables
-- ============================================================================

-- BRANDS TABLE
CREATE TABLE IF NOT EXISTS brands (
    id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    short_code VARCHAR(10) NOT NULL COMMENT 'GS, SCF, etc',
    description TEXT NULL,
    logo_url VARCHAR(255) NULL,
    website_url VARCHAR(255) NULL,
    color_primary VARCHAR(7) DEFAULT '#37d4d6' COMMENT 'Hex color',
    color_secondary VARCHAR(7) NULL,
    active TINYINT(1) DEFAULT 1,
    display_order INT DEFAULT 0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    UNIQUE INDEX idx_brand_name (name),
    UNIQUE INDEX idx_brand_code (short_code),
    INDEX idx_brand_active (active, display_order)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- BRAND-SERIES MAPPING
CREATE TABLE IF NOT EXISTS brand_series_map (
    id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    brand_id INT UNSIGNED NOT NULL,
    series_id INT UNSIGNED NOT NULL,
    relationship_type ENUM('owner', 'partner', 'sponsor') DEFAULT 'owner',
    valid_from DATE NULL,
    valid_until DATE NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,

    UNIQUE INDEX idx_brand_series (brand_id, series_id),
    INDEX idx_series_brand (series_id),
    INDEX idx_brand_active (brand_id, valid_from, valid_until)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Seed default brands
INSERT INTO brands (name, short_code, description, color_primary, active, display_order)
VALUES
    ('GravitySeries', 'GS', 'Sveriges storsta gravity MTB-serie', '#37d4d6', 1, 1),
    ('Svenska Cykelforbundet', 'SCF', 'Svenska Cykelforbundet - nationella masterskapsavlingar', '#0066cc', 1, 2)
ON DUPLICATE KEY UPDATE updated_at = CURRENT_TIMESTAMP;
