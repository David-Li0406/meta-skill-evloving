<?php
/**
 * Debug Migration - Test database operations step by step
 */

error_reporting(E_ALL);
ini_set('display_errors', 1);

echo "<!DOCTYPE html><html><head><meta charset='UTF-8'><title>Debug Migration</title>";
echo "<style>body{font-family:monospace;padding:20px;background:#f5f5f5;} .success{color:green;} .error{color:red;} .info{color:blue;}</style>";
echo "</head><body>";
echo "<h1>Debug Migration - Step by Step</h1>";

try {
    echo "<h2>Step 1: Loading config...</h2>";
    require_once __DIR__ . '/../../config.php';
    echo "<p class='success'>✓ Config loaded</p>";

    echo "<h2>Step 2: Checking admin...</h2>";
    require_admin();
    echo "<p class='success'>✓ Admin authenticated</p>";

    echo "<h2>Step 3: Getting database connection...</h2>";
    $db = getDB();
    echo "<p class='success'>✓ Database connected</p>";

    echo "<h2>Step 4: Testing simple query...</h2>";
    $test = $db->getRow("SELECT 1 as test");
    echo "<p class='success'>✓ Simple query works: " . $test['test'] . "</p>";

    echo "<h2>Step 5: Checking if format column exists...</h2>";
    $columns = $db->getAll("SHOW COLUMNS FROM series LIKE 'format'");
    if (empty($columns)) {
        echo "<p class='info'>Column does NOT exist</p>";

        echo "<h2>Step 6: Attempting to add format column...</h2>";
        try {
            $db->query("ALTER TABLE series ADD COLUMN format VARCHAR(50) DEFAULT 'Championship' AFTER type");
            echo "<p class='success'>✓ ALTER TABLE succeeded!</p>";
        } catch (Exception $e) {
            echo "<p class='error'>✗ ALTER TABLE failed: " . htmlspecialchars($e->getMessage()) . "</p>";
            echo "<pre>" . htmlspecialchars($e->getTraceAsString()) . "</pre>";
        }
    } else {
        echo "<p class='info'>Column already exists</p>";
    }

    echo "<h2>Step 7: Checking if qualification_point_templates table exists...</h2>";
    $tables = $db->getAll("SHOW TABLES LIKE 'qualification_point_templates'");
    if (empty($tables)) {
        echo "<p class='info'>Table does NOT exist</p>";

        echo "<h2>Step 8: Attempting to create qualification_point_templates table...</h2>";
        try {
            $sql = "CREATE TABLE IF NOT EXISTS qualification_point_templates (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                description TEXT,
                points JSON NOT NULL,
                active BOOLEAN DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                INDEX idx_active (active)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci";

            $db->query($sql);
            echo "<p class='success'>✓ CREATE TABLE qualification_point_templates succeeded!</p>";
        } catch (Exception $e) {
            echo "<p class='error'>✗ CREATE TABLE failed: " . htmlspecialchars($e->getMessage()) . "</p>";
            echo "<pre>" . htmlspecialchars($e->getTraceAsString()) . "</pre>";
        }
    } else {
        echo "<p class='info'>Table already exists</p>";
    }

    echo "<h2>Step 9: Checking if series_events table exists...</h2>";
    $tables = $db->getAll("SHOW TABLES LIKE 'series_events'");
    if (empty($tables)) {
        echo "<p class='info'>Table does NOT exist</p>";

        echo "<h2>Step 10: Attempting to create series_events table (WITHOUT foreign keys)...</h2>";
        try {
            // Try without foreign keys first
            $sql = "CREATE TABLE IF NOT EXISTS series_events (
                id INT AUTO_INCREMENT PRIMARY KEY,
                series_id INT NOT NULL,
                event_id INT NOT NULL,
                template_id INT NULL,
                sort_order INT DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE KEY unique_series_event (series_id, event_id),
                INDEX idx_series (series_id),
                INDEX idx_event (event_id),
                INDEX idx_template (template_id)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci";

            $db->query($sql);
            echo "<p class='success'>✓ CREATE TABLE series_events succeeded (without foreign keys)!</p>";

            echo "<p class='info'>Note: Foreign key constraints were skipped. Add them manually later if needed.</p>";
        } catch (Exception $e) {
            echo "<p class='error'>✗ CREATE TABLE failed: " . htmlspecialchars($e->getMessage()) . "</p>";
            echo "<pre>" . htmlspecialchars($e->getTraceAsString()) . "</pre>";
        }
    } else {
        echo "<p class='info'>Table already exists</p>";
    }

    echo "<h2 class='success'>✅ Debug migration completed!</h2>";
    echo "<p>If all steps above show green checkmarks, you can run the regular migrations.</p>";
    echo "<p><a href='/admin/series.php'>Go to Series page</a></p>";

} catch (Exception $e) {
    echo "<h2 class='error'>✗ Fatal error!</h2>";
    echo "<p class='error'>Error: " . htmlspecialchars($e->getMessage()) . "</p>";
    echo "<pre>" . htmlspecialchars($e->getTraceAsString()) . "</pre>";
}

echo "</body></html>";
?>
