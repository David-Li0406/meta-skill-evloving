-- Migration 100: Global Sponsors & Race Reports System
-- Date: 2026-01-10
-- Description: Adds global sponsor placements and race reports/blog functionality
--
-- NOTE: This migration only creates tables. For column additions to the
-- sponsors table, run the PHP migration instead:
-- /admin/migrations/100_global_sponsors_race_reports.php

-- ============================================================================
-- 1. SPONSOR PLACEMENTS TABLE
-- ============================================================================

CREATE TABLE IF NOT EXISTS sponsor_placements (
    id INT AUTO_INCREMENT PRIMARY KEY,
    sponsor_id INT NOT NULL,
    page_type ENUM('home', 'results', 'series_list', 'series_single', 'database', 'ranking', 'calendar', 'blog', 'blog_single', 'all') NOT NULL,
    position ENUM('header_banner', 'sidebar_top', 'sidebar_mid', 'content_top', 'content_mid', 'content_bottom', 'footer') NOT NULL,
    display_order INT DEFAULT 0,
    is_active TINYINT(1) DEFAULT 1,
    start_date DATE NULL,
    end_date DATE NULL,
    impressions_target INT NULL,
    impressions_current INT DEFAULT 0,
    clicks INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_placement_page (page_type, position),
    INDEX idx_placement_active (is_active, start_date, end_date),
    INDEX idx_sponsor (sponsor_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================================
-- 2. SPONSOR TIER BENEFITS TABLE
-- ============================================================================

CREATE TABLE IF NOT EXISTS sponsor_tier_benefits (
    id INT AUTO_INCREMENT PRIMARY KEY,
    tier VARCHAR(50) NOT NULL,
    benefit_key VARCHAR(100) NOT NULL,
    benefit_value TEXT NOT NULL,
    display_order INT DEFAULT 0,
    UNIQUE KEY unique_tier_benefit (tier, benefit_key)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================================
-- 3. SPONSOR ANALYTICS TABLE
-- ============================================================================

CREATE TABLE IF NOT EXISTS sponsor_analytics (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    sponsor_id INT NOT NULL,
    placement_id INT NULL,
    page_type VARCHAR(50) NOT NULL,
    page_id INT NULL,
    action_type ENUM('impression', 'click', 'conversion') NOT NULL,
    user_id INT NULL,
    ip_hash VARCHAR(64) NOT NULL,
    user_agent VARCHAR(500),
    referer VARCHAR(255),
    session_id VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_analytics_sponsor (sponsor_id, created_at),
    INDEX idx_analytics_placement (placement_id, created_at),
    INDEX idx_analytics_date (created_at),
    INDEX idx_analytics_action (action_type, created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================================
-- 4. SPONSOR SETTINGS TABLE
-- ============================================================================

CREATE TABLE IF NOT EXISTS sponsor_settings (
    setting_key VARCHAR(100) PRIMARY KEY,
    setting_value TEXT NOT NULL,
    description TEXT,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================================
-- 5. RACE REPORTS TABLE
-- ============================================================================

CREATE TABLE IF NOT EXISTS race_reports (
    id INT AUTO_INCREMENT PRIMARY KEY,
    rider_id INT NOT NULL,
    event_id INT NULL,
    title VARCHAR(255) NOT NULL,
    slug VARCHAR(255) NOT NULL UNIQUE,
    content LONGTEXT NOT NULL,
    excerpt TEXT,
    featured_image VARCHAR(255),
    status ENUM('draft', 'published', 'archived') DEFAULT 'draft',
    instagram_url VARCHAR(255),
    instagram_embed_code TEXT,
    is_from_instagram TINYINT(1) DEFAULT 0,
    is_featured TINYINT(1) DEFAULT 0,
    views INT DEFAULT 0,
    likes INT DEFAULT 0,
    reading_time_minutes INT DEFAULT 1,
    allow_comments TINYINT(1) DEFAULT 1,
    published_at DATETIME NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_reports_status (status, published_at),
    INDEX idx_reports_rider (rider_id),
    INDEX idx_reports_event (event_id),
    INDEX idx_reports_featured (is_featured, published_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================================
-- 6. RACE REPORT TAGS TABLE
-- ============================================================================

CREATE TABLE IF NOT EXISTS race_report_tags (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    slug VARCHAR(100) NOT NULL UNIQUE,
    usage_count INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================================
-- 7. RACE REPORT TAG RELATIONS TABLE
-- ============================================================================

CREATE TABLE IF NOT EXISTS race_report_tag_relations (
    report_id INT NOT NULL,
    tag_id INT NOT NULL,
    PRIMARY KEY (report_id, tag_id),
    INDEX idx_tag (tag_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================================
-- 8. RACE REPORT COMMENTS TABLE
-- ============================================================================

CREATE TABLE IF NOT EXISTS race_report_comments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    report_id INT NOT NULL,
    rider_id INT NULL,
    parent_comment_id INT NULL,
    comment_text TEXT NOT NULL,
    is_approved TINYINT(1) DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_comments_report (report_id, is_approved),
    INDEX idx_comments_parent (parent_comment_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================================
-- 9. RACE REPORT LIKES TABLE
-- ============================================================================

CREATE TABLE IF NOT EXISTS race_report_likes (
    report_id INT NOT NULL,
    rider_id INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (report_id, rider_id),
    INDEX idx_rider (rider_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================================
-- 10. INSERT DEFAULT DATA (uses INSERT IGNORE to avoid duplicates)
-- ============================================================================

INSERT IGNORE INTO sponsor_settings (setting_key, setting_value, description) VALUES
('max_sponsors_per_page', '5', 'Max antal sponsorer per sida'),
('banner_rotation_seconds', '10', 'Rotation banner (sekunder)'),
('enable_analytics', '1', 'Aktivera sponsorstatistik'),
('require_approval_race_reports', '0', 'Krav godkannande for race reports'),
('featured_reports_count', '3', 'Antal featured reports pa startsida'),
('instagram_auto_import', '0', 'Auto-importera fran Instagram'),
('public_enabled', '0', 'Visa globala sponsorer for besokare (0=endast admin, 1=alla)'),
('race_reports_public', '0', 'Visa race reports for besokare (0=endast admin, 1=alla)');

INSERT IGNORE INTO sponsor_tier_benefits (tier, benefit_key, benefit_value, display_order) VALUES
('title_gravityseries', 'branding', 'Varumarke i GravitySeries logotyp', 1),
('title_gravityseries', 'placement', 'Exklusiv startsidesplacering (header banner)', 2),
('title_gravityseries', 'all_pages', 'Header-placering pa alla sidor', 3),
('title_gravityseries', 'max_placements', 'Max 10 sponsorplatser', 4),
('title_gravityseries', 'analytics', 'Dedikerad analytics-dashboard', 5),
('title_series', 'branding', 'Varumarke i serienamnet', 1),
('title_series', 'placement', 'Banner pa seriesidor', 2),
('title_series', 'events', 'Branding pa seriens evenemang', 3),
('title_series', 'max_placements', 'Max 5 sponsorplatser', 4),
('gold', 'sidebar', 'Sidebar startsida', 1),
('gold', 'results', 'Alla resultsidor', 2),
('gold', 'ranking', 'Ranking sidebar', 3),
('gold', 'max_placements', 'Max 3 sponsorplatser', 4),
('silver', 'selected', 'Valda sidor', 1),
('silver', 'content', 'Content bottom', 2),
('silver', 'max_placements', 'Max 2 sponsorplatser', 3),
('branch', 'database', 'Databas sidebar (relevant for cykelbutiker)', 1),
('branch', 'footer', 'Footer rotation', 2),
('branch', 'max_placements', 'Max 2 sponsorplatser', 3);

INSERT IGNORE INTO race_report_tags (name, slug) VALUES
('Enduro', 'enduro'),
('Downhill', 'downhill'),
('XC', 'xc'),
('Gravel', 'gravel'),
('Traning', 'traning'),
('Tavling', 'tavling'),
('Teknik', 'teknik'),
('Utrustning', 'utrustning');
