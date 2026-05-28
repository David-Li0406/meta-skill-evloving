-- Migration 058: Create event map tables
-- Creates tables for GPX tracks, segments, and POIs if they don't exist

-- Event tracks - main table for GPX files
CREATE TABLE IF NOT EXISTS event_tracks (
    id INT AUTO_INCREMENT PRIMARY KEY,
    event_id INT NOT NULL,
    name VARCHAR(255) NOT NULL,
    gpx_file VARCHAR(255) NULL,
    route_type VARCHAR(50) NULL,
    route_label VARCHAR(255) NULL,
    color VARCHAR(7) DEFAULT '#3B82F6',
    is_primary TINYINT(1) DEFAULT 0,
    display_order INT DEFAULT 0,
    total_distance_km DECIMAL(10,2) DEFAULT 0,
    total_elevation_m INT DEFAULT 0,
    bounds_north DECIMAL(10,7) NULL,
    bounds_south DECIMAL(10,7) NULL,
    bounds_east DECIMAL(10,7) NULL,
    bounds_west DECIMAL(10,7) NULL,
    raw_coordinates LONGTEXT NULL,
    raw_elevation_data LONGTEXT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_event_tracks_event (event_id)
);

-- Track segments - stage/liaison classification
CREATE TABLE IF NOT EXISTS event_track_segments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    track_id INT NOT NULL,
    segment_type ENUM('stage', 'liaison', 'lift') NOT NULL DEFAULT 'stage',
    segment_name VARCHAR(255) NULL,
    sequence_number INT NOT NULL DEFAULT 1,
    timing_id VARCHAR(100) NULL,
    sponsor_id INT NULL,
    distance_km DECIMAL(10,2) DEFAULT 0,
    elevation_gain_m INT DEFAULT 0,
    elevation_loss_m INT DEFAULT 0,
    start_lat DECIMAL(10,7) NULL,
    start_lng DECIMAL(10,7) NULL,
    end_lat DECIMAL(10,7) NULL,
    end_lng DECIMAL(10,7) NULL,
    start_index INT NULL,
    end_index INT NULL,
    coordinates JSON NULL,
    elevation_data JSON NULL,
    color VARCHAR(7) DEFAULT '#EF4444',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_track_segments_track (track_id),
    INDEX idx_track_segments_sequence (track_id, sequence_number)
);

-- POI markers - points of interest
CREATE TABLE IF NOT EXISTS event_pois (
    id INT AUTO_INCREMENT PRIMARY KEY,
    event_id INT NOT NULL,
    poi_type VARCHAR(50) NOT NULL,
    label VARCHAR(255) NULL,
    description TEXT NULL,
    lat DECIMAL(10,7) NOT NULL,
    lng DECIMAL(10,7) NOT NULL,
    sequence_number INT NULL,
    is_visible TINYINT(1) DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_event_pois_event (event_id),
    INDEX idx_event_pois_type (poi_type)
);
