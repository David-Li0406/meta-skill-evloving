<?php
/**
 * Migration V2: Add format column to series table
 * More robust with better error handling
 */

// Enable error reporting
error_reporting(E_ALL);
ini_set('display_errors', 1);
set_time_limit(60);

require_once __DIR__ . '/../../config.php';
require_admin();

$db = getDB();

echo "<!DOCTYPE html><html><head><meta charset='UTF-8'><title>Migration V2: Add Series Format</title>";
echo "<style>body{font-family:monospace;padding:20px;background:#f5f5f5;} .success{color:green;} .error{color:red;} .info{color:blue;} pre{background:#fff;padding:10px;border:1px solid #ccc;}</style>";
echo "</head><body>";
echo "<h1>Migration V2: Add Format Column to Series Table</h1>";

try {
    echo "<p class='info'>Step 1: Testing database connection...</p>";
    flush();

    // Test connection
    $testQuery = $db->getRow("SELECT 1 as test");
    if ($testQuery && $testQuery['test'] == 1) {
        echo "<p class='success'>✓ Database connection OK</p>";
    } else {
        throw new Exception("Database connection test failed");
    }
    flush();

    echo "<p class='info'>Step 2: Checking if 'format' column exists...</p>";
    flush();

    // Check if column already exists
    $columns = $db->getAll("SHOW COLUMNS FROM series LIKE 'format'");

    if (empty($columns)) {
        echo "<p class='info'>✓ Column does not exist. Ready to add it.</p>";
        flush();

        echo "<p class='info'>Step 3: Adding 'format' column to series table...</p>";
        flush();

        // Get PDO connection directly for better error handling
        $pdo = $db->getConnection();

        if (!$pdo) {
            throw new Exception("Could not get PDO connection");
        }

        // Execute ALTER TABLE with direct PDO
        $sql = "ALTER TABLE series ADD COLUMN format VARCHAR(50) DEFAULT 'Championship' AFTER type";
        echo "<pre>SQL: " . htmlspecialchars($sql) . "</pre>";
        flush();

        $result = $pdo->exec($sql);

        if ($result === false) {
            $errorInfo = $pdo->errorInfo();
            throw new Exception("ALTER TABLE failed: " . $errorInfo[2]);
        }

        echo "<p class='success'>✓ Successfully executed ALTER TABLE</p>";
        flush();

        // Verify column was added
        echo "<p class='info'>Step 4: Verifying column was added...</p>";
        flush();

        $verifyColumns = $db->getAll("SHOW COLUMNS FROM series LIKE 'format'");

        if (empty($verifyColumns)) {
            throw new Exception("Column was not added successfully!");
        }

        echo "<p class='success'>✓ Column 'format' verified in series table</p>";

    } else {
        echo "<p class='info'>ℹ Column 'format' already exists in series table</p>";
    }

    echo "<hr>";
    echo "<h2 class='success'>✅ Migration completed successfully!</h2>";
    echo "<p><a href='/admin/series.php' style='color: green; font-weight: bold;'>→ Go to Series page</a></p>";
    echo "<p><a href='/admin/check-series-format.php' style='color: blue;'>→ Verify with diagnostic tool</a></p>";

} catch (Exception $e) {
    echo "<hr>";
    echo "<h2 class='error'>✗ Migration failed!</h2>";
    echo "<p class='error'><strong>Error:</strong> " . htmlspecialchars($e->getMessage()) . "</p>";
    echo "<h3>Stack Trace:</h3>";
    echo "<pre>" . htmlspecialchars($e->getTraceAsString()) . "</pre>";

    echo "<h3>Debug Info:</h3>";
    echo "<pre>";
    echo "PHP Version: " . PHP_VERSION . "\n";
    echo "DB Host: " . DB_HOST . "\n";
    echo "DB Name: " . DB_NAME . "\n";
    echo "</pre>";
}

echo "</body></html>";
