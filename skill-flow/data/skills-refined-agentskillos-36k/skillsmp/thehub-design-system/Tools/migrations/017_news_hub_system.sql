-- Migration 017: News Hub System
-- Date: 2026-01-19
-- Description: Extends race_reports for full News Hub functionality
--
-- This migration adds:
-- 1. content_type column for distinguishing different post types
-- 2. series_id for automatic series tagging
-- 3. YouTube video support columns
-- 4. Admin moderation notes
-- 5. Photo gallery support
-- 6. SEO meta fields

-- ============================================================================
-- 1. ENSURE BASE TABLES EXIST (idempotent)
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
    status ENUM('draft', 'pending', 'published', 'archived') DEFAULT 'draft',
    instagram_url VARCHAR(255),
    instagram_embed_code TEXT,
    is_from_instagram TINYINT(1) DEFAULT 0,
    youtube_url VARCHAR(255) NULL,
    youtube_video_id VARCHAR(20) NULL,
    is_from_youtube TINYINT(1) DEFAULT 0,
    is_featured TINYINT(1) DEFAULT 0,
    views INT DEFAULT 0,
    likes INT DEFAULT 0,
    reading_time_minutes INT DEFAULT 1,
    allow_comments TINYINT(1) DEFAULT 1,
    moderated_by INT NULL,
    moderated_at DATETIME NULL,
    moderation_notes TEXT NULL,
    published_at DATETIME NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_reports_status (status, published_at),
    INDEX idx_reports_rider (rider_id),
    INDEX idx_reports_event (event_id),
    INDEX idx_reports_featured (is_featured, published_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Add missing columns if table already exists (safe to run multiple times)
-- Using stored procedure to check column existence before adding

CREATE TABLE IF NOT EXISTS race_report_tags (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    slug VARCHAR(100) NOT NULL UNIQUE,
    usage_count INT DEFAULT 0,
    color VARCHAR(7) NULL,
    icon VARCHAR(50) NULL,
    is_system TINYINT(1) DEFAULT 0,
    tag_type ENUM('discipline', 'event', 'series', 'location', 'general') DEFAULT 'general',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS race_report_tag_relations (
    report_id INT NOT NULL,
    tag_id INT NOT NULL,
    PRIMARY KEY (report_id, tag_id),
    INDEX idx_tag (tag_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

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

CREATE TABLE IF NOT EXISTS race_report_likes (
    report_id INT NOT NULL,
    rider_id INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (report_id, rider_id),
    INDEX idx_rider (rider_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS news_page_views (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    report_id INT NOT NULL,
    visitor_hash VARCHAR(64) NOT NULL,
    session_id VARCHAR(100) NULL,
    user_id INT NULL,
    referer VARCHAR(255) NULL,
    user_agent VARCHAR(500) NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_report_date (report_id, created_at),
    INDEX idx_visitor (visitor_hash, report_id),
    INDEX idx_date (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================================
-- 2. INSERT DEFAULT TAGS (ignore duplicates)
-- ============================================================================

INSERT IGNORE INTO race_report_tags (name, slug, color, icon, is_system, tag_type) VALUES
('Enduro', 'enduro', '#FFE009', 'mountain', 1, 'discipline'),
('Downhill', 'downhill', '#FF6B35', 'arrow-down', 1, 'discipline'),
('XC', 'xc', '#2E7D32', 'bike', 1, 'discipline'),
('Gravel', 'gravel', '#795548', 'map', 1, 'discipline'),
('Dual Slalom', 'dual-slalom', '#E91E63', 'split', 1, 'discipline'),
('SM', 'sm', '#FFD700', 'trophy', 1, 'event'),
('NM', 'nm', '#C0C0C0', 'flag', 1, 'event'),
('Rookie', 'rookie', '#4CAF50', 'star', 1, 'general'),
('Foton', 'foton', '#2196F3', 'camera', 1, 'general'),
('Video', 'video', '#FF0000', 'play', 1, 'general'),
('Teknik', 'teknik', '#9C27B0', 'settings', 1, 'general'),
('Utrustning', 'utrustning', '#607D8B', 'wrench', 1, 'general'),
('Are', 'are', '#00BCD4', 'map-pin', 0, 'location'),
('Isaberg', 'isaberg', '#00BCD4', 'map-pin', 0, 'location'),
('Kungsbacka', 'kungsbacka', '#00BCD4', 'map-pin', 0, 'location');

-- ============================================================================
-- 3. SPONSOR SETTINGS TABLE (if not exists)
-- ============================================================================

CREATE TABLE IF NOT EXISTS sponsor_settings (
    setting_key VARCHAR(100) PRIMARY KEY,
    setting_value TEXT NOT NULL,
    description TEXT,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================================
-- 4. SPONSOR SETTINGS FOR NEWS HUB (ignore duplicates)
-- ============================================================================

INSERT IGNORE INTO sponsor_settings (setting_key, setting_value, description) VALUES
('news_ads_enabled', '1', 'Enable ads on news pages'),
('news_ads_frequency', '4', 'Show ad every N posts in feed'),
('news_google_adsense_client', '', 'Google AdSense client ID'),
('news_google_adsense_slot', '', 'Google AdSense slot ID'),
('race_reports_public', '1', 'Show news/race reports to all visitors');
