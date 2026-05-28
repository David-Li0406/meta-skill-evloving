-- Ranking Snapshots System
-- Creates tables for 24-month rolling ranking with snapshots

-- Settings table for ranking configuration
CREATE TABLE IF NOT EXISTS ranking_settings (
    id INT AUTO_INCREMENT PRIMARY KEY,
    setting_key VARCHAR(100) NOT NULL UNIQUE,
    setting_value TEXT,
    description VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Rider ranking snapshots (daily snapshots per discipline)
CREATE TABLE IF NOT EXISTS ranking_snapshots (
    id INT AUTO_INCREMENT PRIMARY KEY,
    rider_id INT NOT NULL,
    discipline ENUM('ENDURO', 'DH', 'GRAVITY') NOT NULL,
    snapshot_date DATE NOT NULL,
    total_ranking_points DECIMAL(12,2) DEFAULT 0,
    points_last_12_months DECIMAL(12,2) DEFAULT 0,
    points_months_13_24 DECIMAL(12,2) DEFAULT 0,
    events_count INT DEFAULT 0,
    ranking_position INT DEFAULT 0,
    previous_position INT DEFAULT NULL,
    position_change INT DEFAULT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (rider_id) REFERENCES riders(id) ON DELETE CASCADE,
    UNIQUE KEY unique_rider_discipline_date (rider_id, discipline, snapshot_date),
    INDEX idx_discipline_date (discipline, snapshot_date),
    INDEX idx_ranking_position (discipline, snapshot_date, ranking_position)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Club ranking snapshots
CREATE TABLE IF NOT EXISTS club_ranking_snapshots (
    id INT AUTO_INCREMENT PRIMARY KEY,
    club_id INT NOT NULL,
    discipline ENUM('ENDURO', 'DH', 'GRAVITY') NOT NULL,
    snapshot_date DATE NOT NULL,
    total_ranking_points DECIMAL(12,2) DEFAULT 0,
    points_last_12_months DECIMAL(12,2) DEFAULT 0,
    points_months_13_24 DECIMAL(12,2) DEFAULT 0,
    riders_count INT DEFAULT 0,
    events_count INT DEFAULT 0,
    ranking_position INT DEFAULT 0,
    previous_position INT DEFAULT NULL,
    position_change INT DEFAULT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (club_id) REFERENCES clubs(id) ON DELETE CASCADE,
    UNIQUE KEY unique_club_discipline_date (club_id, discipline, snapshot_date),
    INDEX idx_discipline_date (discipline, snapshot_date),
    INDEX idx_ranking_position (discipline, snapshot_date, ranking_position)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Insert default settings
INSERT IGNORE INTO ranking_settings (setting_key, setting_value, description) VALUES
('field_multipliers', '{"1":0.75,"2":0.77,"3":0.79,"4":0.81,"5":0.83,"6":0.85,"7":0.86,"8":0.87,"9":0.88,"10":0.89,"11":0.90,"12":0.91,"13":0.92,"14":0.93,"15":1.00}', 'Fältstorlek-multiplikatorer'),
('time_decay', '{"months_1_12":1.00,"months_13_24":0.50,"months_25_plus":0.00}', 'Tidsviktning'),
('event_level_multipliers', '{"national":1.00,"sportmotion":0.50}', 'Eventtyp-multiplikatorer');
