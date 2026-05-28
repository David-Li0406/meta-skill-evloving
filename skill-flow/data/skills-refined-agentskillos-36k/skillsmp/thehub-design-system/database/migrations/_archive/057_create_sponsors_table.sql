-- Migration 057: Create sponsors table if not exists
-- This table may have been missed during initial setup

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

-- Junction table for event-sponsor relationships
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
    INDEX idx_sponsor (sponsor_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Junction table for series-sponsor relationships
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
    INDEX idx_sponsor (sponsor_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
