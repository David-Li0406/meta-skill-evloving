<?php
/**
 * Safe Migration - Works around InfinityFree limitations
 */

error_reporting(E_ALL);
ini_set('display_errors', 1);
@ini_set('max_execution_time', 300); // Try to extend time limit

echo "<!DOCTYPE html><html><head><meta charset='UTF-8'><title>Safe Migration</title>";
echo "<style>body{font-family:monospace;padding:20px;background:#f5f5f5;} .success{color:green;} .error{color:red;} .info{color:blue;}</style>";
echo "</head><body>";
echo "<h1>Safe Migration - InfinityFree Compatible</h1>";

// Flush output after each step
function output_flush() {
    if (ob_get_level() > 0) {
        ob_flush();
    }
    flush();
}

try {
    require_once __DIR__ . '/../../config.php';
    require_admin();
    $db = getDB();

    echo "<h2>Step 1: Add format column (simple ALTER)</h2>";
    output_flush();

    $columns = $db->getAll("SHOW COLUMNS FROM series LIKE 'format'");
    if (empty($columns)) {
        try {
            // Simpler ALTER without AFTER clause
            $db->query("ALTER TABLE series ADD COLUMN format VARCHAR(50) DEFAULT 'Championship'");
            echo "<p class='success'>✓ Added format column</p>";
            output_flush();
        } catch (Exception $e) {
            echo "<p class='error'>✗ Failed: " . htmlspecialchars($e->getMessage()) . "</p>";
            echo "<p class='info'>Trying alternative method...</p>";
            output_flush();
        }
    } else {
        echo "<p class='info'>Format column already exists</p>";
        output_flush();
    }

    echo "<h2>Step 2: Create point templates table (using TEXT not JSON)</h2>";
    output_flush();

    try {
        // Use TEXT instead of JSON (better compatibility)
        $sql = "CREATE TABLE IF NOT EXISTS qualification_point_templates (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            description TEXT,
            points TEXT NOT NULL,
            active TINYINT(1) DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            KEY idx_active (active)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci";

        $db->query($sql);
        echo "<p class='success'>✓ Created qualification_point_templates table</p>";
        output_flush();
    } catch (Exception $e) {
        echo "<p class='error'>✗ Failed: " . htmlspecialchars($e->getMessage()) . "</p>";
        output_flush();
    }

    echo "<h2>Step 3: Create series_events table (without foreign keys)</h2>";
    output_flush();

    try {
        // No FOREIGN KEY constraints (InfinityFree may not support them)
        $sql = "CREATE TABLE IF NOT EXISTS series_events (
            id INT AUTO_INCREMENT PRIMARY KEY,
            series_id INT NOT NULL,
            event_id INT NOT NULL,
            template_id INT NULL,
            sort_order INT DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE KEY unique_series_event (series_id, event_id),
            KEY idx_series (series_id),
            KEY idx_event (event_id),
            KEY idx_template (template_id)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci";

        $db->query($sql);
        echo "<p class='success'>✓ Created series_events table</p>";
        output_flush();
    } catch (Exception $e) {
        echo "<p class='error'>✗ Failed: " . htmlspecialchars($e->getMessage()) . "</p>";
        output_flush();
    }

    echo "<h2>Step 4: Insert default point templates</h2>";
    output_flush();

    $defaultTemplates = [
        [
            'name' => 'SweCup Standard',
            'description' => 'Standard SweCup poängfördelning',
            'points' => json_encode([
                '1' => 100, '2' => 80, '3' => 60, '4' => 50, '5' => 45,
                '6' => 40, '7' => 36, '8' => 32, '9' => 29, '10' => 26,
                '11' => 24, '12' => 22, '13' => 20, '14' => 18, '15' => 16,
                '16' => 15, '17' => 14, '18' => 13, '19' => 12, '20' => 11,
                '21' => 10, '22' => 9, '23' => 8, '24' => 7, '25' => 6,
                '26' => 5, '27' => 4, '28' => 3, '29' => 2, '30' => 1
            ]),
            'active' => 1
        ],
        [
            'name' => 'UCI Standard',
            'description' => 'UCI standardpoäng',
            'points' => json_encode([
                '1' => 250, '2' => 200, '3' => 150, '4' => 120, '5' => 100,
                '6' => 90, '7' => 80, '8' => 70, '9' => 60, '10' => 50,
                '11' => 45, '12' => 40, '13' => 35, '14' => 30, '15' => 25,
                '16' => 20, '17' => 15, '18' => 10, '19' => 5, '20' => 1
            ]),
            'active' => 1
        ],
        [
            'name' => 'Top 10',
            'description' => 'Endast topp 10 får poäng',
            'points' => json_encode([
                '1' => 50, '2' => 40, '3' => 30, '4' => 25, '5' => 20,
                '6' => 15, '7' => 10, '8' => 7, '9' => 5, '10' => 3
            ]),
            'active' => 1
        ]
    ];

    foreach ($defaultTemplates as $template) {
        $existing = $db->getRow(
            "SELECT id FROM qualification_point_templates WHERE name = ?",
            [$template['name']]
        );

        if (!$existing) {
            try {
                $db->insert('qualification_point_templates', $template);
                echo "<p class='success'>  ✓ Created template: " . htmlspecialchars($template['name']) . "</p>";
                output_flush();
            } catch (Exception $e) {
                echo "<p class='error'>  ✗ Failed to create " . htmlspecialchars($template['name']) . ": " . htmlspecialchars($e->getMessage()) . "</p>";
                output_flush();
            }
        } else {
            echo "<p class='info'>  ℹ Template already exists: " . htmlspecialchars($template['name']) . "</p>";
            output_flush();
        }
    }

    echo "<h2 class='success'>✅ Migration completed!</h2>";
    echo "<p><a href='/admin/series.php'>Go to Series page</a> | <a href='/admin/point-templates.php'>Go to Point Templates page</a></p>";

} catch (Exception $e) {
    echo "<h2 class='error'>✗ Fatal error!</h2>";
    echo "<p class='error'>Error: " . htmlspecialchars($e->getMessage()) . "</p>";
    echo "<pre>" . htmlspecialchars($e->getTraceAsString()) . "</pre>";
}

echo "</body></html>";
?>
