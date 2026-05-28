-- =====================================================
-- EVENT MAP & POI SYSTEM - Migration
-- Created: 2025-12-09
-- Description: Adds tables for GPX tracks, segments, POIs
-- =====================================================

-- =====================================================
-- EVENT TRACKS - Huvudtabell for GPX-filer
-- =====================================================
CREATE TABLE IF NOT EXISTS event_tracks (
    id INT AUTO_INCREMENT PRIMARY KEY,
    event_id INT NOT NULL,
    name VARCHAR(255) NOT NULL,
    gpx_file VARCHAR(255) NOT NULL,
    total_distance_km DECIMAL(10,2) DEFAULT 0,
    total_elevation_m INT DEFAULT 0,
    bounds_north DECIMAL(10,7) NULL,
    bounds_south DECIMAL(10,7) NULL,
    bounds_east DECIMAL(10,7) NULL,
    bounds_west DECIMAL(10,7) NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (event_id) REFERENCES events(id) ON DELETE CASCADE,
    INDEX idx_event_tracks_event (event_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =====================================================
-- TRACK SEGMENTS - Stage/Liaison-klassificering
-- =====================================================
CREATE TABLE IF NOT EXISTS event_track_segments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    track_id INT NOT NULL,
    segment_type ENUM('stage', 'liaison') NOT NULL DEFAULT 'stage',
    segment_name VARCHAR(255) NULL,
    sequence_number INT NOT NULL DEFAULT 1,
    timing_id VARCHAR(100) NULL,
    distance_km DECIMAL(10,2) DEFAULT 0,
    elevation_gain_m INT DEFAULT 0,
    elevation_loss_m INT DEFAULT 0,
    start_lat DECIMAL(10,7) NOT NULL,
    start_lng DECIMAL(10,7) NOT NULL,
    end_lat DECIMAL(10,7) NOT NULL,
    end_lng DECIMAL(10,7) NOT NULL,
    coordinates JSON NOT NULL,
    elevation_data JSON NULL,
    color VARCHAR(7) DEFAULT '#FF0000',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (track_id) REFERENCES event_tracks(id) ON DELETE CASCADE,
    INDEX idx_track_segments_track (track_id),
    INDEX idx_track_segments_sequence (track_id, sequence_number),
    INDEX idx_track_segments_timing (timing_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =====================================================
-- POI MARKERS - Intressepunkter
-- =====================================================
CREATE TABLE IF NOT EXISTS event_pois (
    id INT AUTO_INCREMENT PRIMARY KEY,
    event_id INT NOT NULL,
    poi_type ENUM(
        'water',
        'depot',
        'spectator',
        'food',
        'bike_wash',
        'tech_zone',
        'feed_zone',
        'parking',
        'aid_station',
        'information',
        'start',
        'finish'
    ) NOT NULL,
    label VARCHAR(255) NULL,
    description TEXT NULL,
    lat DECIMAL(10,7) NOT NULL,
    lng DECIMAL(10,7) NOT NULL,
    sequence_number INT NULL,
    is_visible TINYINT(1) DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (event_id) REFERENCES events(id) ON DELETE CASCADE,
    INDEX idx_event_pois_event (event_id),
    INDEX idx_event_pois_type (poi_type),
    INDEX idx_event_pois_visible (event_id, is_visible)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =====================================================
-- WAYPOINTS - Numrerade vagpunkter fran GPX
-- =====================================================
CREATE TABLE IF NOT EXISTS event_waypoints (
    id INT AUTO_INCREMENT PRIMARY KEY,
    segment_id INT NOT NULL,
    waypoint_number INT NOT NULL,
    lat DECIMAL(10,7) NOT NULL,
    lng DECIMAL(10,7) NOT NULL,
    elevation_m INT NULL,
    distance_from_start_km DECIMAL(10,3) NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (segment_id) REFERENCES event_track_segments(id) ON DELETE CASCADE,
    INDEX idx_event_waypoints_segment (segment_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
