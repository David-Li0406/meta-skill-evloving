<?php
/**
 * Migration: Add event_format column to events table
 *
 * Allows selection of event format:
 * - ENDURO: Standard enduro with finish_time
 * - DH_STANDARD: Downhill (two runs, fastest counts)
 * - DH_SWECUP: SweCUP Downhill (two runs, both award points)
 * - DUAL_SLALOM: Dual slalom format
 */

require_once __DIR__ . '/../../config.php';
require_admin();

$db = getDB();

try {
    echo "Checking if event_format column exists...\n";

    // Check if column already exists
    $columns = $db->getAll("SHOW COLUMNS FROM events LIKE 'event_format'");

    if (empty($columns)) {
        echo "Adding event_format column to events table...\n";

        // Add event_format column with ENUM type
        $db->query("
            ALTER TABLE events
            ADD COLUMN event_format VARCHAR(20) DEFAULT 'ENDURO'
            AFTER discipline
        ");

        echo "✅ Added event_format column\n";

        // Create index for faster queries
        $db->query("
            CREATE INDEX idx_event_format ON events(event_format)
        ");

        echo "✅ Created index on event_format\n";

    } else {
        echo "⚠️  Column event_format already exists, skipping\n";
    }

    echo "\n✅ Migration completed successfully!\n";

} catch (Exception $e) {
    echo "\n❌ Migration failed: " . $e->getMessage() . "\n";
    exit(1);
}
