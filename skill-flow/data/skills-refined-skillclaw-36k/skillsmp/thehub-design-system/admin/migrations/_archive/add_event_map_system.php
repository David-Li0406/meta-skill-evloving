<?php
/**
 * Migration: Add Event Map & POI System
 *
 * Creates tables for:
 * - event_tracks: GPX track files
 * - event_track_segments: Stage/liaison segments
 * - event_pois: Points of interest (12 types)
 * - event_waypoints: Numbered waypoints
 *
 * @since 2025-12-09
 */

error_reporting(E_ALL);
ini_set('display_errors', 1);

require_once __DIR__ . '/../../config.php';
require_admin();

$db = getDB();

echo "<!DOCTYPE html><html><head><meta charset='UTF-8'><title>Migration: Event Map & POI System</title>";
echo "<style>
    body { font-family: system-ui, sans-serif; padding: 20px; background: #f5f5f5; max-width: 800px; margin: 0 auto; }
    .success { color: #059669; }
    .error { color: #dc2626; }
    .info { color: #0284c7; }
    .box { background: white; padding: 20px; border-radius: 8px; margin: 15px 0; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }
    h1 { color: #171717; }
    pre { background: #1a1a1a; color: #e5e5e5; padding: 15px; border-radius: 6px; overflow-x: auto; }
</style>";
echo "</head><body>";
echo "<h1>Migration: Event Map & POI System</h1>";

$tablesCreated = 0;
$errors = [];

try {
    // =========================================
    // TABLE 1: event_tracks
    // =========================================
    echo "<div class='box'>";
    echo "<h3>1. event_tracks</h3>";

    $exists = $db->getAll("SHOW TABLES LIKE 'event_tracks'");
    if (empty($exists)) {
        $db->query("
            CREATE TABLE event_tracks (
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
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        ");
        echo "<p class='success'>✓ Skapade tabell event_tracks</p>";
        $tablesCreated++;
    } else {
        echo "<p class='info'>ℹ Tabell event_tracks finns redan</p>";
    }
    echo "</div>";

    // =========================================
    // TABLE 2: event_track_segments
    // =========================================
    echo "<div class='box'>";
    echo "<h3>2. event_track_segments</h3>";

    $exists = $db->getAll("SHOW TABLES LIKE 'event_track_segments'");
    if (empty($exists)) {
        $db->query("
            CREATE TABLE event_track_segments (
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
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        ");
        echo "<p class='success'>✓ Skapade tabell event_track_segments</p>";
        $tablesCreated++;
    } else {
        echo "<p class='info'>ℹ Tabell event_track_segments finns redan</p>";
    }
    echo "</div>";

    // =========================================
    // TABLE 3: event_pois
    // =========================================
    echo "<div class='box'>";
    echo "<h3>3. event_pois</h3>";

    $exists = $db->getAll("SHOW TABLES LIKE 'event_pois'");
    if (empty($exists)) {
        $db->query("
            CREATE TABLE event_pois (
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
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        ");
        echo "<p class='success'>✓ Skapade tabell event_pois</p>";
        $tablesCreated++;
    } else {
        echo "<p class='info'>ℹ Tabell event_pois finns redan</p>";
    }
    echo "</div>";

    // =========================================
    // TABLE 4: event_waypoints
    // =========================================
    echo "<div class='box'>";
    echo "<h3>4. event_waypoints</h3>";

    $exists = $db->getAll("SHOW TABLES LIKE 'event_waypoints'");
    if (empty($exists)) {
        $db->query("
            CREATE TABLE event_waypoints (
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
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        ");
        echo "<p class='success'>✓ Skapade tabell event_waypoints</p>";
        $tablesCreated++;
    } else {
        echo "<p class='info'>ℹ Tabell event_waypoints finns redan</p>";
    }
    echo "</div>";

    // =========================================
    // SUMMARY
    // =========================================
    echo "<div class='box' style='background: #d1fae5; border-left: 4px solid #059669;'>";
    echo "<h2 class='success'>✅ Migration klar!</h2>";

    if ($tablesCreated > 0) {
        echo "<p><strong>{$tablesCreated} tabeller skapades.</strong></p>";
    } else {
        echo "<p>Alla tabeller fanns redan.</p>";
    }

    echo "<h4>POI-typer som stöds:</h4>";
    echo "<ul style='column-count: 3;'>";
    echo "<li>🏁 Start</li>";
    echo "<li>🏆 Mål</li>";
    echo "<li>💧 Vatten</li>";
    echo "<li>🔧 Depå</li>";
    echo "<li>👥 Publikplats</li>";
    echo "<li>🍔 Mat</li>";
    echo "<li>🚿 Cykeltvätt</li>";
    echo "<li>⚙️ Teknisk zon</li>";
    echo "<li>🍌 Langning</li>";
    echo "<li>🅿️ Parkering</li>";
    echo "<li>➕ Hjälpstation</li>";
    echo "<li>ℹ️ Information</li>";
    echo "</ul>";
    echo "</div>";

    echo "<p style='margin-top: 20px;'>";
    echo "<a href='/admin/migrations/migration-browser.php' style='color: #004a98;'>← Tillbaka till Migration Browser</a>";
    echo "</p>";

} catch (Exception $e) {
    echo "<div class='box' style='background: #fee2e2; border-left: 4px solid #dc2626;'>";
    echo "<h2 class='error'>✗ Migration misslyckades!</h2>";
    echo "<p class='error'>Fel: " . htmlspecialchars($e->getMessage()) . "</p>";
    echo "<pre>" . htmlspecialchars($e->getTraceAsString()) . "</pre>";
    echo "</div>";
}

echo "</body></html>";
