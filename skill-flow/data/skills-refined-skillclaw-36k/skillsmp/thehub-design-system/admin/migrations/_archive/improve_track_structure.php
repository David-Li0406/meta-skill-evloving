<?php
/**
 * Migration: Improve Track Structure
 *
 * Adds raw_coordinates to event_tracks so the full GPX track
 * is stored independently from segments.
 *
 * This allows:
 * - Full track always visible as "base" (liaison/transport)
 * - Segments are overlays that can be added/removed without losing track
 * - Delete segment = remove marking, not the track itself
 */

require_once __DIR__ . '/../../config.php';
require_admin();

// Use global $pdo directly (not getDB() wrapper) for ALTER TABLE
global $pdo;

echo "<h1>Migration: Improve Track Structure</h1>";
echo "<pre>";

try {
    // Check if column already exists
    $stmt = $pdo->query("SHOW COLUMNS FROM event_tracks LIKE 'raw_coordinates'");
    if ($stmt->fetch()) {
        echo "Column 'raw_coordinates' already exists. Skipping.\n";
    } else {
        // Add raw_coordinates column (LONGTEXT for large GPX files)
        $pdo->exec("
            ALTER TABLE event_tracks
            ADD COLUMN raw_coordinates LONGTEXT NULL AFTER gpx_file,
            ADD COLUMN raw_elevation_data LONGTEXT NULL AFTER raw_coordinates
        ");
        echo "Added 'raw_coordinates' and 'raw_elevation_data' columns.\n";
    }

    // Migrate existing data: Extract coordinates from first segment into track
    echo "\nMigrating existing track data...\n";

    $tracks = $pdo->query("
        SELECT t.id, t.name,
               (SELECT coordinates FROM event_track_segments WHERE track_id = t.id ORDER BY sequence_number LIMIT 1) as first_coords,
               (SELECT elevation_data FROM event_track_segments WHERE track_id = t.id ORDER BY sequence_number LIMIT 1) as first_ele
        FROM event_tracks t
        WHERE t.raw_coordinates IS NULL
    ")->fetchAll(PDO::FETCH_ASSOC);

    foreach ($tracks as $track) {
        // Get ALL coordinates from ALL segments for this track
        $segments = $pdo->prepare("
            SELECT coordinates, elevation_data
            FROM event_track_segments
            WHERE track_id = ?
            ORDER BY sequence_number
        ");
        $segments->execute([$track['id']]);
        $allSegments = $segments->fetchAll(PDO::FETCH_ASSOC);

        $allCoords = [];
        $allElevations = [];

        foreach ($allSegments as $seg) {
            $coords = json_decode($seg['coordinates'], true) ?: [];
            $eles = json_decode($seg['elevation_data'], true) ?: [];

            foreach ($coords as $i => $coord) {
                $allCoords[] = $coord;
                if (isset($eles[$i])) {
                    $allElevations[] = $eles[$i];
                }
            }
        }

        if (!empty($allCoords)) {
            $stmt = $pdo->prepare("
                UPDATE event_tracks
                SET raw_coordinates = ?, raw_elevation_data = ?
                WHERE id = ?
            ");
            $stmt->execute([
                json_encode($allCoords),
                json_encode($allElevations),
                $track['id']
            ]);
            echo "  Migrated track '{$track['name']}' with " . count($allCoords) . " waypoints\n";
        }
    }

    echo "\n✓ Migration completed successfully!\n";
    echo "\nNew workflow:\n";
    echo "1. Upload GPX → All waypoints stored in 'raw_coordinates'\n";
    echo "2. Full track shown as transport/liaison (gray)\n";
    echo "3. Mark sections as SS/Lift → Creates colored overlays\n";
    echo "4. Delete segment → Only removes marking, track remains\n";

} catch (Exception $e) {
    echo "ERROR: " . $e->getMessage() . "\n";
}

echo "</pre>";
echo '<p><a href="/admin/events">← Back to Events</a></p>';
