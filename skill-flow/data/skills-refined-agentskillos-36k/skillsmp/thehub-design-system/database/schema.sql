-- TheHUB Database Schema
-- MySQL/MariaDB database for cycling competition platform
-- Updated: 2025-11-13 (Force deployment sync)

-- Set charset
SET NAMES utf8mb4;
SET CHARACTER SET utf8mb4;

-- ============================================================================
-- CLUBS TABLE
-- ============================================================================
CREATE TABLE IF NOT EXISTS clubs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    short_name VARCHAR(50),
    region VARCHAR(100),
    city VARCHAR(100),
    country VARCHAR(100) DEFAULT 'Sverige',
    website VARCHAR(255),
    active BOOLEAN DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_name (name),
    INDEX idx_city (city),
    INDEX idx_active (active)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================================
-- RIDERS TABLE (was CYCLISTS)
-- ============================================================================
-- PRIVACY NOTE: Fields marked with [PRIVATE] contain sensitive data and must
-- NEVER be exposed publicly. Only use for internal admin and autofill features.
CREATE TABLE IF NOT EXISTS riders (
    id INT AUTO_INCREMENT PRIMARY KEY,
    firstname VARCHAR(100) NOT NULL,
    lastname VARCHAR(100) NOT NULL,
    birth_year INT,
    gender ENUM('M', 'F', 'K', 'Other') DEFAULT 'M',
    nationality VARCHAR(3) DEFAULT 'SWE', -- ISO 3166-1 alpha-3 country code

    -- Club and Team
    club_id INT,
    team VARCHAR(255), -- Team name (separate from club)

    -- License Information
    license_number VARCHAR(50),
    license_type VARCHAR(50),
    license_category VARCHAR(100),
    discipline VARCHAR(100), -- Legacy single discipline
    disciplines JSON, -- Multiple disciplines (Road, Track, BMX, CX, Trial, Para, MTB, E-cycling, Gravel)
    license_valid_until DATE,
    license_year INT,

    -- Authentication
    email VARCHAR(255),
    password VARCHAR(255) DEFAULT NULL,
    password_reset_token VARCHAR(255) DEFAULT NULL,
    password_reset_expires DATETIME DEFAULT NULL,
    last_login DATETIME DEFAULT NULL,

    -- Regional Information (for statistics)
    country VARCHAR(100) DEFAULT 'Sverige',
    district VARCHAR(100), -- District/Region for regional statistics

    -- Status and Metadata
    active BOOLEAN DEFAULT 1,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    -- Foreign Keys
    FOREIGN KEY (club_id) REFERENCES clubs(id) ON DELETE SET NULL,

    -- Indexes
    INDEX idx_name (lastname, firstname),
    INDEX idx_club (club_id),
    INDEX idx_license (license_number),
    INDEX idx_active (active),
    INDEX idx_email (email),
    INDEX idx_reset_token (password_reset_token),
    INDEX idx_district (district),
    INDEX idx_nationality (nationality),
    UNIQUE KEY unique_license (license_number)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
COMMENT='Rider profiles. District field used for regional statistics.';

-- ============================================================================
-- CATEGORIES TABLE - DEPRECATED
-- ============================================================================
-- WARNING: This table is DEPRECATED as of 2025-11-19
-- Use the 'classes' table instead (see migration 008_classes_system.sql)
-- This table is kept for historical reference only
-- ============================================================================
CREATE TABLE IF NOT EXISTS categories (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    short_name VARCHAR(20),
    age_min INT,
    age_max INT,
    gender ENUM('M', 'F', 'All') DEFAULT 'All',
    description TEXT,
    active BOOLEAN DEFAULT 0,  -- Set to 0 to prevent new usage
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_active (active)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
COMMENT='DEPRECATED: Use classes table instead. Kept for historical reference only.';

-- ============================================================================
-- SERIES BRANDS TABLE (parent series / series families)
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
-- SERIES TABLE
-- ============================================================================
CREATE TABLE IF NOT EXISTS series (
    id INT AUTO_INCREMENT PRIMARY KEY,
    brand_id INT NULL,
    name VARCHAR(255) NOT NULL,
    slug VARCHAR(100),
    type VARCHAR(100),
    discipline VARCHAR(100),
    year INT,
    status ENUM('planning', 'active', 'completed', 'cancelled') DEFAULT 'planning',
    start_date DATE,
    end_date DATE,
    description TEXT,
    website VARCHAR(255),
    logo VARCHAR(255),
    organizer VARCHAR(255),

    -- Badge styling (for visual display)
    gradient_start VARCHAR(7) DEFAULT '#004A98',
    gradient_end VARCHAR(7) DEFAULT '#002a5c',
    accent_color VARCHAR(7) DEFAULT '#61CE70',
    logo_light VARCHAR(255),
    logo_dark VARCHAR(255),

    active BOOLEAN DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    UNIQUE KEY unique_slug (slug),
    INDEX idx_brand (brand_id),
    INDEX idx_status (status),
    INDEX idx_type (type),
    INDEX idx_discipline (discipline),
    INDEX idx_year (year),
    INDEX idx_active (active),
    INDEX idx_start_date (start_date),
    CONSTRAINT fk_series_brand FOREIGN KEY (brand_id) REFERENCES series_brands(id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================================
-- SPONSORS TABLE
-- ============================================================================
CREATE TABLE IF NOT EXISTS sponsors (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    slug VARCHAR(100),
    logo VARCHAR(255),
    logo_dark VARCHAR(255),
    website VARCHAR(255),
    tier ENUM('title', 'gold', 'silver', 'bronze') DEFAULT 'bronze',
    description TEXT,
    active TINYINT(1) DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    UNIQUE KEY unique_slug (slug),
    INDEX idx_tier (tier),
    INDEX idx_active (active)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================================
-- EVENT_SPONSORS - Junction table for event-sponsor relationships
-- ============================================================================
CREATE TABLE IF NOT EXISTS event_sponsors (
    id INT PRIMARY KEY AUTO_INCREMENT,
    event_id INT NOT NULL,
    sponsor_id INT NOT NULL,
    placement ENUM('header', 'sidebar', 'footer', 'content') DEFAULT 'sidebar',
    display_order INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (event_id) REFERENCES events(id) ON DELETE CASCADE,
    FOREIGN KEY (sponsor_id) REFERENCES sponsors(id) ON DELETE CASCADE,
    UNIQUE KEY unique_event_sponsor_placement (event_id, sponsor_id, placement),
    INDEX idx_event (event_id),
    INDEX idx_sponsor (sponsor_id),
    INDEX idx_placement (placement)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================================
-- SERIES_SPONSORS - Junction table for series-sponsor relationships
-- ============================================================================
CREATE TABLE IF NOT EXISTS series_sponsors (
    id INT PRIMARY KEY AUTO_INCREMENT,
    series_id INT NOT NULL,
    sponsor_id INT NOT NULL,
    placement ENUM('header', 'sidebar', 'footer', 'content') DEFAULT 'sidebar',
    display_order INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (series_id) REFERENCES series(id) ON DELETE CASCADE,
    FOREIGN KEY (sponsor_id) REFERENCES sponsors(id) ON DELETE CASCADE,
    UNIQUE KEY unique_series_sponsor_placement (series_id, sponsor_id, placement),
    INDEX idx_series (series_id),
    INDEX idx_sponsor (sponsor_id),
    INDEX idx_placement (placement)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================================
-- VENUES TABLE
-- ============================================================================
CREATE TABLE IF NOT EXISTS venues (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    city VARCHAR(100),
    region VARCHAR(100),
    country VARCHAR(100) DEFAULT 'Sverige',
    address TEXT,
    coordinates VARCHAR(100),
    description TEXT,
    website VARCHAR(255),
    active BOOLEAN DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_city (city),
    INDEX idx_active (active)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================================
-- EVENTS TABLE
-- ============================================================================
CREATE TABLE IF NOT EXISTS events (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    advent_id VARCHAR(50), -- External ID for result imports
    date DATE NOT NULL,
    location VARCHAR(255),
    venue_id INT,
    type VARCHAR(100),
    discipline VARCHAR(100),
    series_id INT,
    distance DECIMAL(6,2), -- in kilometers
    elevation_gain INT, -- in meters
    status ENUM('upcoming', 'ongoing', 'completed', 'cancelled') DEFAULT 'upcoming',
    description TEXT,
    organizer VARCHAR(255),
    website VARCHAR(255),
    registration_url VARCHAR(255),
    registration_deadline DATE,
    max_participants INT,
    entry_fee DECIMAL(10,2),
    active BOOLEAN DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (series_id) REFERENCES series(id) ON DELETE SET NULL,
    FOREIGN KEY (venue_id) REFERENCES venues(id) ON DELETE SET NULL,
    INDEX idx_date (date),
    INDEX idx_status (status),
    INDEX idx_type (type),
    INDEX idx_discipline (discipline),
    INDEX idx_series (series_id),
    INDEX idx_venue (venue_id),
    INDEX idx_active (active),
    INDEX idx_advent_id (advent_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================================
-- RESULTS TABLE
-- ============================================================================
CREATE TABLE IF NOT EXISTS results (
    id INT AUTO_INCREMENT PRIMARY KEY,
    event_id INT NOT NULL,
    cyclist_id INT NOT NULL,
    category_id INT,
    position INT,
    finish_time TIME,
    points INT DEFAULT 0,
    bib_number VARCHAR(20),
    status ENUM('finished', 'dnf', 'dns', 'dq') DEFAULT 'finished',
    is_ebike TINYINT(1) DEFAULT 0, -- E-BIKE participant (no points/position)
    time_behind TIME, -- time behind winner
    average_speed DECIMAL(5,2), -- km/h
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (event_id) REFERENCES events(id) ON DELETE CASCADE,
    FOREIGN KEY (cyclist_id) REFERENCES riders(id) ON DELETE CASCADE,
    FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE SET NULL,
    INDEX idx_event (event_id),
    INDEX idx_cyclist (cyclist_id),
    INDEX idx_category (category_id),
    INDEX idx_position (position),
    UNIQUE KEY unique_event_cyclist (event_id, cyclist_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================================
-- ADMIN USERS TABLE
-- ============================================================================
CREATE TABLE IF NOT EXISTS admin_users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    full_name VARCHAR(100),
    role ENUM('super_admin', 'admin', 'editor') DEFAULT 'editor',
    active BOOLEAN DEFAULT 1,
    last_login TIMESTAMP NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_username (username),
    INDEX idx_active (active)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================================
-- IMPORT LOGS TABLE (for tracking imports)
-- ============================================================================
CREATE TABLE IF NOT EXISTS import_logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    import_type ENUM('riders', 'results', 'events', 'clubs', 'cyclists') NOT NULL,
    filename VARCHAR(255),
    records_total INT DEFAULT 0,
    records_success INT DEFAULT 0,
    records_failed INT DEFAULT 0,
    errors TEXT,
    imported_by VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_type (import_type),
    INDEX idx_date (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================================
-- IMPORT HISTORY TABLE (for rollback functionality)
-- ============================================================================
CREATE TABLE IF NOT EXISTS import_history (
    id INT AUTO_INCREMENT PRIMARY KEY,
    import_type ENUM('riders', 'results', 'events', 'clubs', 'uci', 'other') NOT NULL,
    filename VARCHAR(255),
    file_size INT,
    status ENUM('pending', 'processing', 'completed', 'failed', 'rolled_back') DEFAULT 'pending',
    total_records INT DEFAULT 0,
    success_count INT DEFAULT 0,
    updated_count INT DEFAULT 0,
    failed_count INT DEFAULT 0,
    skipped_count INT DEFAULT 0,
    error_summary TEXT,
    notes TEXT,
    imported_by VARCHAR(100),
    rolled_back_at TIMESTAMP NULL DEFAULT NULL,
    rolled_back_by VARCHAR(100) NULL DEFAULT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_type (import_type),
    INDEX idx_status (status),
    INDEX idx_date (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================================
-- IMPORT RECORDS TABLE (for tracking individual created/updated records)
-- ============================================================================
CREATE TABLE IF NOT EXISTS import_records (
    id INT AUTO_INCREMENT PRIMARY KEY,
    import_id INT NOT NULL,
    record_type ENUM('rider', 'result', 'event', 'club', 'venue', 'other') NOT NULL,
    record_id INT NOT NULL,
    action ENUM('created', 'updated', 'deleted') NOT NULL,
    old_data JSON,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (import_id) REFERENCES import_history(id) ON DELETE CASCADE,
    INDEX idx_import (import_id),
    INDEX idx_record (record_type, record_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================================
-- DEFAULT DATA - Categories
-- ============================================================================
INSERT IGNORE INTO categories (name, short_name, age_min, age_max, gender) VALUES
('Herr Elite', 'HE', 19, 34, 'M'),
('Dam Elite', 'DE', 19, 34, 'F'),
('Herr Junior', 'HJ', 17, 18, 'M'),
('Dam Junior', 'DJ', 17, 18, 'F'),
('Herr Veteran 35-44', 'HV35', 35, 44, 'M'),
('Herr Veteran 45-54', 'HV45', 45, 54, 'M'),
('Herr Veteran 55+', 'HV55', 55, 99, 'M'),
('Dam Veteran 35+', 'DV35', 35, 99, 'F'),
('Herr Motion', 'HM', 19, 99, 'M'),
('Dam Motion', 'DM', 19, 99, 'F');

-- ============================================================================
-- DEFAULT ADMIN USER
-- ============================================================================
INSERT IGNORE INTO admin_users (username, password_hash, email, full_name, role) VALUES
('roger', '$2y$12$Chd19PIKV6soorPEpY9WAOnCW3HiIRb3KBZTw0Wf.mEPyThZcnvwe', 'Roger@ecab.bike', 'Roger', 'super_admin');

-- ============================================================================
-- VIEWS FOR COMMON QUERIES
-- ============================================================================

-- View for complete results with rider and event info
CREATE OR REPLACE VIEW results_complete AS
SELECT
    r.id,
    r.event_id,
    e.name AS event_name,
    e.date AS event_date,
    e.location,
    r.cyclist_id,
    CONCAT(c.firstname, ' ', c.lastname) AS cyclist_name,
    c.birth_year,
    c.gender,
    cl.name AS club_name,
    cls.name AS class_name,
    cls.display_name AS class_display_name,
    r.position,
    r.class_position,
    r.finish_time,
    r.points,
    r.class_points,
    r.bib_number,
    r.status,
    r.average_speed
FROM results r
JOIN riders c ON r.cyclist_id = c.id
JOIN events e ON r.event_id = e.id
LEFT JOIN clubs cl ON c.club_id = cl.id
LEFT JOIN classes cls ON r.class_id = cls.id;

-- View for rider statistics (using class-based results)
CREATE OR REPLACE VIEW cyclist_stats AS
SELECT
    c.id AS cyclist_id,
    CONCAT(c.firstname, ' ', c.lastname) AS cyclist_name,
    cl.name AS club_name,
    COUNT(r.id) AS total_races,
    COUNT(CASE WHEN r.class_position = 1 THEN 1 END) AS class_wins,
    COUNT(CASE WHEN r.class_position <= 3 THEN 1 END) AS class_podiums,
    COUNT(CASE WHEN r.class_position <= 10 THEN 1 END) AS class_top_10,
    SUM(r.class_points) AS total_class_points,
    MIN(r.class_position) AS best_class_position
FROM riders c
LEFT JOIN results r ON c.id = r.cyclist_id
LEFT JOIN clubs cl ON c.club_id = cl.id
GROUP BY c.id, cyclist_name, cl.name;
