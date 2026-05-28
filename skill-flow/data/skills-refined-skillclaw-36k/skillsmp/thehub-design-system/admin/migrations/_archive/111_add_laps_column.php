<?php
/**
 * Migration: Add laps column to results table
 * For XC/MTB races where number of completed laps is tracked
 */

$migrationName = 'Add laps column to results';
$migrationDescription = 'Adds laps column for XC/MTB race results';

function migrate_111_add_laps_column($db) {
    $results = [];

    // Check if column already exists
    $columnExists = $db->getValue("
        SELECT COUNT(*)
        FROM information_schema.COLUMNS
        WHERE TABLE_SCHEMA = DATABASE()
        AND TABLE_NAME = 'results'
        AND COLUMN_NAME = 'laps'
    ");

    if ($columnExists) {
        $results[] = ['status' => 'skipped', 'message' => 'Column laps already exists'];
        return $results;
    }

    // Add laps column
    try {
        $db->query("
            ALTER TABLE results
            ADD COLUMN laps TINYINT UNSIGNED NULL DEFAULT NULL
            COMMENT 'Number of laps completed (for XC/MTB)'
            AFTER status
        ");
        $results[] = ['status' => 'success', 'message' => 'Added laps column to results table'];
    } catch (Exception $e) {
        $results[] = ['status' => 'error', 'message' => 'Failed to add laps column: ' . $e->getMessage()];
    }

    return $results;
}

// Auto-run if accessed directly
if (basename($_SERVER['SCRIPT_FILENAME']) === basename(__FILE__)) {
    require_once __DIR__ . '/../../config.php';
    require_admin();

    $db = getDB();
    $results = migrate_111_add_laps_column($db);

    header('Content-Type: application/json');
    echo json_encode(['migration' => $migrationName, 'results' => $results], JSON_PRETTY_PRINT);
}
