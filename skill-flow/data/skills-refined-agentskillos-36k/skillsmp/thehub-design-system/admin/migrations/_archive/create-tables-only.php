<?php
/**
 * Create Tables Only - Skip ALTER TABLE (InfinityFree limitation)
 */

error_reporting(E_ALL);
ini_set('display_errors', 1);
@ini_set('max_execution_time', 300);

echo "<!DOCTYPE html><html><head><meta charset='UTF-8'><title>Create Tables</title>";
echo "<style>body{font-family:monospace;padding:20px;background:#f5f5f5;} .success{color:green;} .error{color:red;} .info{color:blue;} .warning{color:orange;}</style>";
echo "</head><body>";
echo "<h1>Create Tables Migration (InfinityFree Compatible)</h1>";

echo "<div style='background:lightyellow;padding:15px;margin-bottom:20px;border-left:4px solid orange;'>";
echo "<p class='warning'><strong>⚠️ Note:</strong> The 'format' column for the series table cannot be added automatically due to InfinityFree restrictions.</p>";
echo "<p class='info'>The series page will work fine without it - it defaults to 'Championship'.</p>";
echo "<p class='info'>If you want to add it later, use phpMyAdmin:</p>";
echo "<code>ALTER TABLE series ADD COLUMN format VARCHAR(50) DEFAULT 'Championship'</code>";
echo "</div>";

function flush_output() {
    if (ob_get_level() > 0) ob_flush();
    flush();
}

try {
    require_once __DIR__ . '/../../config.php';
    require_admin();
    $db = getDB();

    echo "<h2>Creating qualification_point_templates table...</h2>";
    flush_output();

    try {
        $sql = "CREATE TABLE IF NOT EXISTS qualification_point_templates (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            description TEXT,
            points TEXT NOT NULL,
            active TINYINT(1) DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            KEY idx_active (active)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4";

        $db->query($sql);
        echo "<p class='success'>✓ Created qualification_point_templates table</p>";
        flush_output();
    } catch (Exception $e) {
        echo "<p class='error'>✗ Error: " . htmlspecialchars($e->getMessage()) . "</p>";
        flush_output();
    }

    echo "<h2>Creating series_events table...</h2>";
    flush_output();

    try {
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
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4";

        $db->query($sql);
        echo "<p class='success'>✓ Created series_events table</p>";
        flush_output();
    } catch (Exception $e) {
        echo "<p class='error'>✗ Error: " . htmlspecialchars($e->getMessage()) . "</p>";
        flush_output();
    }

    echo "<h2>Inserting default point templates...</h2>";
    flush_output();

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

    $created = 0;
    $skipped = 0;

    foreach ($defaultTemplates as $template) {
        $existing = $db->getRow(
            "SELECT id FROM qualification_point_templates WHERE name = ?",
            [$template['name']]
        );

        if (!$existing) {
            try {
                $db->insert('qualification_point_templates', $template);
                echo "<p class='success'>  ✓ Created: " . htmlspecialchars($template['name']) . "</p>";
                $created++;
                flush_output();
            } catch (Exception $e) {
                echo "<p class='error'>  ✗ Failed: " . htmlspecialchars($template['name']) . " - " . htmlspecialchars($e->getMessage()) . "</p>";
                flush_output();
            }
        } else {
            echo "<p class='info'>  ℹ Already exists: " . htmlspecialchars($template['name']) . "</p>";
            $skipped++;
            flush_output();
        }
    }

    echo "<h2 class='success'>✅ Migration Completed!</h2>";
    echo "<p>Tables created: qualification_point_templates, series_events</p>";
    echo "<p>Point templates: $created created, $skipped already existed</p>";

    echo "<div style='background:lightgreen;padding:15px;margin-top:20px;border-left:4px solid green;'>";
    echo "<p><strong>✅ Success! You can now use:</strong></p>";
    echo "<ul>";
    echo "<li><a href='/admin/series.php'>Series page</a></li>";
    echo "<li><a href='/admin/point-templates.php'>Point Templates page</a></li>";
    echo "<li><a href='/admin/series-events.php'>Series Events management</a> (when you select a series)</li>";
    echo "</ul>";
    echo "</div>";

} catch (Exception $e) {
    echo "<h2 class='error'>✗ Fatal Error</h2>";
    echo "<p class='error'>Error: " . htmlspecialchars($e->getMessage()) . "</p>";
    echo "<pre>" . htmlspecialchars($e->getTraceAsString()) . "</pre>";
}

echo "</body></html>";
?>
