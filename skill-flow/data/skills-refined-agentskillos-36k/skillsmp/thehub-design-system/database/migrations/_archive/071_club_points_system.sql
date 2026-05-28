-- Club Points System Tables
-- Stores calculated club points for series with team/club rankings

-- Individual rider points per event/club
CREATE TABLE IF NOT EXISTS club_rider_points (
    id INT AUTO_INCREMENT PRIMARY KEY,
    club_id INT NOT NULL,
    event_id INT NOT NULL,
    series_id INT NOT NULL,
    rider_id INT NOT NULL,
    class_id INT,
    original_points DECIMAL(10,2) DEFAULT 0,
    club_points DECIMAL(10,2) DEFAULT 0,
    rider_rank_in_club INT DEFAULT 0,
    percentage_applied INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (club_id) REFERENCES clubs(id) ON DELETE CASCADE,
    FOREIGN KEY (event_id) REFERENCES events(id) ON DELETE CASCADE,
    FOREIGN KEY (series_id) REFERENCES series(id) ON DELETE CASCADE,
    FOREIGN KEY (rider_id) REFERENCES riders(id) ON DELETE CASCADE,
    UNIQUE KEY unique_rider_event_series_class (rider_id, event_id, series_id, class_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Club total points per event
CREATE TABLE IF NOT EXISTS club_event_points (
    id INT AUTO_INCREMENT PRIMARY KEY,
    club_id INT NOT NULL,
    event_id INT NOT NULL,
    series_id INT NOT NULL,
    total_points DECIMAL(10,2) DEFAULT 0,
    participants_count INT DEFAULT 0,
    scoring_riders INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (club_id) REFERENCES clubs(id) ON DELETE CASCADE,
    FOREIGN KEY (event_id) REFERENCES events(id) ON DELETE CASCADE,
    FOREIGN KEY (series_id) REFERENCES series(id) ON DELETE CASCADE,
    UNIQUE KEY unique_club_event_series (club_id, event_id, series_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Cached club standings per series
CREATE TABLE IF NOT EXISTS club_standings_cache (
    id INT AUTO_INCREMENT PRIMARY KEY,
    club_id INT NOT NULL,
    series_id INT NOT NULL,
    total_points DECIMAL(10,2) DEFAULT 0,
    total_participants INT DEFAULT 0,
    events_count INT DEFAULT 0,
    best_event_points DECIMAL(10,2) DEFAULT 0,
    ranking INT DEFAULT 0,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (club_id) REFERENCES clubs(id) ON DELETE CASCADE,
    FOREIGN KEY (series_id) REFERENCES series(id) ON DELETE CASCADE,
    UNIQUE KEY unique_club_series (club_id, series_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Add indexes for performance
CREATE INDEX idx_crp_club_series ON club_rider_points(club_id, series_id);
CREATE INDEX idx_crp_event_series ON club_rider_points(event_id, series_id);
CREATE INDEX idx_cep_series ON club_event_points(series_id);
CREATE INDEX idx_csc_series ON club_standings_cache(series_id);
CREATE INDEX idx_csc_ranking ON club_standings_cache(series_id, ranking);
