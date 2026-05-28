<?php
/**
 * Migration: Add E-BIKE support to results table
 *
 * Adds is_ebike column to mark E-BIKE participants
 * E-BIKE participants:
 * - Are included in results sorted by time
 * - Have no numeric position
 * - Receive 0 points
 * - Are excluded from series standings
 */

// Enable error reporting
error_reporting(E_ALL);
ini_set('display_errors', 1);

require_once __DIR__ . '/../../config.php';
require_admin();

$db = getDB();

echo "<!DOCTYPE html><html><head><meta charset='UTF-8'><title>Migration: Add E-BIKE Support</title>";
echo "<style>body{font-family:monospace;padding:20px;background:#f5f5f5;} .success{color:green;} .error{color:red;} .info{color:blue;}</style>";
echo "</head><body>";
echo "<h1>Migration: Add E-BIKE Support to Results Table</h1>";

try {
    // Add is_ebike column
    echo "<p>Adding is_ebike column...</p>";
    $columns = $db->getAll("SHOW COLUMNS FROM results LIKE 'is_ebike'");
    if (empty($columns)) {
        $db->query("ALTER TABLE results ADD COLUMN is_ebike TINYINT(1) DEFAULT 0 AFTER status");
        echo "<p class='success'>✓ Added is_ebike column</p>";

        // Add index for better query performance
        echo "<p>Adding index for is_ebike...</p>";
        try {
            $db->query("ALTER TABLE results ADD INDEX idx_is_ebike (is_ebike)");
            echo "<p class='success'>✓ Added index for is_ebike</p>";
        } catch (Exception $e) {
            echo "<p class='info'>ℹ Index already exists or skipped: " . htmlspecialchars($e->getMessage()) . "</p>";
        }
    } else {
        echo "<p class='info'>ℹ is_ebike column already exists</p>";
    }

    echo "<h2 class='success'>✅ Migration completed successfully!</h2>";
    echo "<div style='background:lightblue;padding:15px;margin-top:20px;border-left:4px solid #004a98;'>";
    echo "<p><strong>Database now supports E-BIKE participants:</strong></p>";
    echo "<ul>";
    echo "<li>✅ is_ebike flag to mark E-BIKE participants</li>";
    echo "<li>✅ E-BIKE participants will be sorted by time but receive no position or points</li>";
    echo "<li>✅ E-BIKE status is preserved during result recalculation</li>";
    echo "</ul>";
    echo "</div>";
    echo "<p><a href='/admin/results.php'>Go to Results page</a></p>";

} catch (Exception $e) {
    echo "<h2 class='error'>✗ Migration failed!</h2>";
    echo "<p class='error'>Error: " . htmlspecialchars($e->getMessage()) . "</p>";
    echo "<pre>" . htmlspecialchars($e->getTraceAsString()) . "</pre>";
    exit(1);
}

echo "</body></html>";
