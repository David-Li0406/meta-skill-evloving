<?php
/**
 * Migration: Add name_locked and federation columns to clubs
 *
 * Allows locking club names and tracking which federation (SCF, NCF, DCU) they belong to
 */

$migrationName = 'Add name_locked and federation columns to clubs';
$migrationDescription = 'Adds name_locked flag and federation tracking';

function migrate_113_add_name_locked($db) {
    $results = [];

    try {
        // Check if name_locked column exists
        $stmt = $db->query("SHOW COLUMNS FROM clubs LIKE 'name_locked'");
        if ($stmt->rowCount() === 0) {
            $db->exec("ALTER TABLE clubs ADD COLUMN name_locked TINYINT(1) DEFAULT 0 AFTER name");
            $results[] = ['status' => 'success', 'message' => 'Added name_locked column to clubs table'];
        } else {
            $results[] = ['status' => 'info', 'message' => 'Column name_locked already exists'];
        }

        // Check if federation column exists (SCF, NCF, DCU)
        $stmt = $db->query("SHOW COLUMNS FROM clubs LIKE 'federation'");
        if ($stmt->rowCount() === 0) {
            $db->exec("ALTER TABLE clubs ADD COLUMN federation VARCHAR(10) DEFAULT NULL AFTER scf_district");
            $results[] = ['status' => 'success', 'message' => 'Added federation column to clubs table'];

            // Update existing clubs based on scf_district
            $db->exec("UPDATE clubs SET federation = 'SCF' WHERE rf_registered = 1 AND scf_district IS NOT NULL AND scf_district != ''");
            $results[] = ['status' => 'info', 'message' => 'Set federation=SCF for existing RF-registered clubs with scf_district'];
        } else {
            $results[] = ['status' => 'info', 'message' => 'Column federation already exists'];
        }
    } catch (Exception $e) {
        $results[] = ['status' => 'error', 'message' => 'Failed: ' . $e->getMessage()];
    }

    return $results;
}

// Auto-run if accessed directly
if (basename($_SERVER['SCRIPT_FILENAME']) === basename(__FILE__)) {
    require_once __DIR__ . '/../../config.php';
    require_once __DIR__ . '/../../includes/auth.php';
    requireLogin();

    global $pdo;

    $results = migrate_113_add_name_locked($pdo);

    header('Content-Type: application/json');
    echo json_encode(['migration' => $migrationName, 'results' => $results], JSON_PRETTY_PRINT);
}
