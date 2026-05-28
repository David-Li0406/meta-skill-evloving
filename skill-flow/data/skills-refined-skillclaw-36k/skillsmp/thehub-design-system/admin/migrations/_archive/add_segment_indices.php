<?php
/**
 * Migration: Add start_index and end_index to segments
 *
 * These indices reference positions in the track's raw_coordinates
 * allowing us to know which part of the track each segment covers.
 */
require_once __DIR__ . '/../../config.php';
require_admin();

// Use global $pdo directly (not getDB() wrapper) for ALTER TABLE
global $pdo;

echo "<h1>Migration: Add Segment Indices</h1>";
echo "<pre>";

try {
    // Check if columns already exist
    $stmt = $pdo->query("SHOW COLUMNS FROM event_track_segments LIKE 'start_index'");
    if ($stmt->fetch()) {
        echo "Columns already exist. Skipping.\n";
    } else {
        $pdo->exec("
            ALTER TABLE event_track_segments
            ADD COLUMN start_index INT NULL AFTER end_lng,
            ADD COLUMN end_index INT NULL AFTER start_index
        ");
        echo "Added 'start_index' and 'end_index' columns.\n";
    }

    echo "\n=== Migration completed! ===\n";
    echo "Segments now store their position in the raw track coordinates.\n";

} catch (Exception $e) {
    echo "ERROR: " . $e->getMessage() . "\n";
}

echo "</pre>";
echo '<p><a href="/admin/events">← Back to Events</a></p>';
