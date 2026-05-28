<?php
/**
 * Migration: Add 'lift' segment type
 *
 * Adds 'lift' to segment_type ENUM for ski lifts/gondolas.
 * Lift segments are excluded from elevation calculations.
 */
require_once __DIR__ . '/../../config.php';
require_admin();

$db = getDB();

echo "<h1>Migration: Lägg till Lift-sträcktyp</h1>";
echo "<pre>";

try {
    // Check current ENUM values
    $result = $db->query("SHOW COLUMNS FROM event_track_segments WHERE Field = 'segment_type'");
    $column = $result->fetch(PDO::FETCH_ASSOC);

    echo "Nuvarande segment_type definition:\n";
    echo htmlspecialchars($column['Type']) . "\n\n";

    // Check if lift already exists
    if (strpos($column['Type'], 'lift') !== false) {
        echo "INFO: 'lift' finns redan i ENUM\n";
    } else {
        // Alter the ENUM to add 'lift'
        $db->query("ALTER TABLE event_track_segments MODIFY COLUMN segment_type ENUM('stage', 'liaison', 'lift') NOT NULL DEFAULT 'stage'");
        echo "OK: Lade till 'lift' i segment_type ENUM\n";
    }

    // Verify the change
    $result = $db->query("SHOW COLUMNS FROM event_track_segments WHERE Field = 'segment_type'");
    $column = $result->fetch(PDO::FETCH_ASSOC);
    echo "\nNy segment_type definition:\n";
    echo htmlspecialchars($column['Type']) . "\n";

    echo "\n=== Migrering slutförd! ===\n";
    echo "Sträcktyper:\n";
    echo "  stage   = Tävlingssträcka (räknas i höjd)\n";
    echo "  liaison = Transport (räknas i höjd)\n";
    echo "  lift    = Lift/gondol (exkluderas från höjdberäkning)\n";

} catch (Exception $e) {
    echo "FEL: " . htmlspecialchars($e->getMessage()) . "\n";
}

echo "</pre>";
echo '<p><a href="/admin/events">← Tillbaka till Events</a></p>';
