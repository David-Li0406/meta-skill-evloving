<?php
/**
 * Migration: Add format column to series table
 *
 * This adds a 'format' column to determine how qualification points are calculated
 * - Championship: Individual results
 * - Team: Team results
 */

// Enable error reporting
error_reporting(E_ALL);
ini_set('display_errors', 1);

require_once __DIR__ . '/../../config.php';
require_admin();

$db = getDB();

echo "<!DOCTYPE html><html><head><meta charset='UTF-8'><title>Migration: Add Series Format</title>";
echo "<style>body{font-family:monospace;padding:20px;background:#f5f5f5;} .success{color:green;} .error{color:red;} .info{color:blue;}</style>";
echo "</head><body>";
echo "<h1>Migration: Add Format Column to Series Table</h1>";

try {
    echo "<p>Checking if 'format' column exists...</p>";

    // Check if column already exists
    $columns = $db->getAll("SHOW COLUMNS FROM series LIKE 'format'");

    if (empty($columns)) {
        echo "<p class='info'>Column does not exist. Adding it now...</p>";
        // Add the column
        $db->query("ALTER TABLE series ADD COLUMN format VARCHAR(50) DEFAULT 'Championship' AFTER type");
        echo "<p class='success'>✓ Successfully added 'format' column to series table</p>";
    } else {
        echo "<p class='info'>ℹ Column 'format' already exists in series table</p>";
    }

    echo "<h2 class='success'>✅ Migration completed successfully!</h2>";
    echo "<p><a href='/admin/series.php'>Go to Series page</a></p>";

} catch (Exception $e) {
    echo "<h2 class='error'>✗ Migration failed!</h2>";
    echo "<p class='error'>Error: " . htmlspecialchars($e->getMessage()) . "</p>";
    echo "<pre>" . htmlspecialchars($e->getTraceAsString()) . "</pre>";
    exit(1);
}

echo "</body></html>";
