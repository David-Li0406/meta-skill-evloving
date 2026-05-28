<?php
/**
 * Migration: Add Downhill-specific columns to results table
 *
 * Adds support for:
 * - Two run times (run_1, run_2) for DH format
 * - Separate points from each run
 * - class_id for proper class-based results
 */

// Enable error reporting
error_reporting(E_ALL);
ini_set('display_errors', 1);

require_once __DIR__ . '/../../config.php';
require_admin();

$db = getDB();

echo "<!DOCTYPE html><html><head><meta charset='UTF-8'><title>Migration: Add DH Support</title>";
echo "<style>body{font-family:monospace;padding:20px;background:#f5f5f5;} .success{color:green;} .error{color:red;} .info{color:blue;}</style>";
echo "</head><body>";
echo "<h1>Migration: Add Downhill Support to Results Table</h1>";

try {
    // Add run_1_time column
    echo "<p>Adding run_1_time column...</p>";
    $columns = $db->getAll("SHOW COLUMNS FROM results LIKE 'run_1_time'");
    if (empty($columns)) {
        $db->query("ALTER TABLE results ADD COLUMN run_1_time TIME NULL AFTER finish_time");
        echo "<p class='success'>✓ Added run_1_time column</p>";
    } else {
        echo "<p class='info'>ℹ run_1_time column already exists</p>";
    }

    // Add run_2_time column
    echo "<p>Adding run_2_time column...</p>";
    $columns = $db->getAll("SHOW COLUMNS FROM results LIKE 'run_2_time'");
    if (empty($columns)) {
        $db->query("ALTER TABLE results ADD COLUMN run_2_time TIME NULL AFTER run_1_time");
        echo "<p class='success'>✓ Added run_2_time column</p>";
    } else {
        echo "<p class='info'>ℹ run_2_time column already exists</p>";
    }

    // Add run_1_points column
    echo "<p>Adding run_1_points column...</p>";
    $columns = $db->getAll("SHOW COLUMNS FROM results LIKE 'run_1_points'");
    if (empty($columns)) {
        $db->query("ALTER TABLE results ADD COLUMN run_1_points INT DEFAULT 0 AFTER points");
        echo "<p class='success'>✓ Added run_1_points column</p>";
    } else {
        echo "<p class='info'>ℹ run_1_points column already exists</p>";
    }

    // Add run_2_points column
    echo "<p>Adding run_2_points column...</p>";
    $columns = $db->getAll("SHOW COLUMNS FROM results LIKE 'run_2_points'");
    if (empty($columns)) {
        $db->query("ALTER TABLE results ADD COLUMN run_2_points INT DEFAULT 0 AFTER run_1_points");
        echo "<p class='success'>✓ Added run_2_points column</p>";
    } else {
        echo "<p class='info'>ℹ run_2_points column already exists</p>";
    }

    // Add class_id column (for proper class-based organization)
    echo "<p>Adding class_id column...</p>";
    $columns = $db->getAll("SHOW COLUMNS FROM results LIKE 'class_id'");
    if (empty($columns)) {
        $db->query("ALTER TABLE results ADD COLUMN class_id INT NULL AFTER category_id");
        echo "<p class='success'>✓ Added class_id column</p>";

        // Add foreign key
        echo "<p>Adding foreign key for class_id...</p>";
        try {
            $db->query("ALTER TABLE results ADD FOREIGN KEY (class_id) REFERENCES classes(id) ON DELETE SET NULL");
            echo "<p class='success'>✓ Added foreign key for class_id</p>";
        } catch (Exception $e) {
            echo "<p class='info'>ℹ Foreign key already exists or skipped: " . htmlspecialchars($e->getMessage()) . "</p>";
        }

        // Add index
        echo "<p>Adding index for class_id...</p>";
        try {
            $db->query("ALTER TABLE results ADD INDEX idx_class (class_id)");
            echo "<p class='success'>✓ Added index for class_id</p>";
        } catch (Exception $e) {
            echo "<p class='info'>ℹ Index already exists or skipped: " . htmlspecialchars($e->getMessage()) . "</p>";
        }
    } else {
        echo "<p class='info'>ℹ class_id column already exists</p>";
    }

    // Add ss1-ss15 columns for Enduro special stages
    echo "<h2>Adding Special Stage columns for Enduro...</h2>";
    for ($i = 1; $i <= 15; $i++) {
        $colName = "ss" . $i;
        $columns = $db->getAll("SHOW COLUMNS FROM results LIKE '$colName'");
        if (empty($columns)) {
            $db->query("ALTER TABLE results ADD COLUMN $colName TIME NULL");
            echo "<p class='success'>✓ Added $colName column</p>";
        }
    }
    echo "<p class='success'>✓ All special stage columns verified/added</p>";

    echo "<h2 class='success'>✅ Migration completed successfully!</h2>";
    echo "<div style='background:lightblue;padding:15px;margin-top:20px;border-left:4px solid #004a98;'>";
    echo "<p><strong>Database now supports:</strong></p>";
    echo "<ul>";
    echo "<li>✅ Downhill: run_1_time, run_2_time</li>";
    echo "<li>✅ DH Points: run_1_points, run_2_points</li>";
    echo "<li>✅ Class-based results: class_id</li>";
    echo "<li>✅ Enduro: ss1-ss15 special stages</li>";
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
