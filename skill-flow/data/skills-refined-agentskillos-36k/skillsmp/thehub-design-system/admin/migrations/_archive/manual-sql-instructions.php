<?php
/**
 * Manual SQL Instructions - For phpMyAdmin
 *
 * InfinityFree blocks CREATE TABLE from PHP scripts.
 * Use these SQL commands in phpMyAdmin instead.
 */

error_reporting(E_ALL);
ini_set('display_errors', 1);

require_once __DIR__ . '/../../config.php';
require_admin();

echo "<!DOCTYPE html><html><head><meta charset='UTF-8'><title>Manual SQL Instructions</title>";
echo "<style>
body{font-family:Arial,sans-serif;padding:20px;background:#f5f5f5;max-width:1200px;margin:0 auto;}
.sql-box{background:#2d2d2d;color:#f8f8f2;padding:20px;border-radius:8px;overflow-x:auto;margin:15px 0;}
.sql-box code{color:#f8f8f2;font-family:monospace;white-space:pre;}
.step{background:white;padding:20px;margin:20px 0;border-left:4px solid #004a98;border-radius:4px;}
.success{color:green;} .error{color:red;} .info{color:blue;} .warning{color:orange;}
h1{color:#004a98;} h2{color:#ef761f;margin-top:30px;} h3{color:#004a98;}
.button{background:#004a98;color:white;padding:10px 20px;text-decoration:none;border-radius:4px;display:inline-block;margin:10px 5px 10px 0;}
.button:hover{background:#003a78;}
</style>";
echo "</head><body>";

echo "<h1>📋 Manual Database Setup for TheHUB</h1>";

echo "<div style='background:lightyellow;padding:20px;margin-bottom:30px;border-left:4px solid orange;border-radius:4px;'>";
echo "<h3 class='warning'>⚠️ Why Manual Setup?</h3>";
echo "<p>InfinityFree's free hosting blocks CREATE TABLE and ALTER TABLE commands from PHP scripts for security reasons.</p>";
echo "<p><strong>Solution:</strong> Run these SQL commands directly in phpMyAdmin.</p>";
echo "</div>";

echo "<h2>📍 Step 1: Access phpMyAdmin</h2>";
echo "<div class='step'>";
echo "<ol>";
echo "<li>Log in to your InfinityFree control panel: <a href='https://infinityfree.com' target='_blank'>https://infinityfree.com</a></li>";
echo "<li>Click on <strong>\"MySQL Databases\"</strong></li>";
echo "<li>Click <strong>\"phpMyAdmin\"</strong> button for your database</li>";
echo "<li>Select your database from the left sidebar (looks like: <code>if0_40400950_THEHUB</code>)</li>";
echo "<li>Click the <strong>\"SQL\"</strong> tab at the top</li>";
echo "</ol>";
echo "</div>";

echo "<h2>📍 Step 2: Create qualification_point_templates Table</h2>";
echo "<div class='step'>";
echo "<p>Copy and paste this SQL into phpMyAdmin and click <strong>\"Go\"</strong>:</p>";
echo "<div class='sql-box'><code>";
echo htmlspecialchars("CREATE TABLE IF NOT EXISTS qualification_point_templates (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    points TEXT NOT NULL,
    active TINYINT(1) DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    KEY idx_active (active)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;");
echo "</code></div>";
echo "<p class='success'>✅ Expected result: \"1 table created\"</p>";
echo "</div>";

echo "<h2>📍 Step 3: Create series_events Table</h2>";
echo "<div class='step'>";
echo "<p>Copy and paste this SQL into phpMyAdmin and click <strong>\"Go\"</strong>:</p>";
echo "<div class='sql-box'><code>";
echo htmlspecialchars("CREATE TABLE IF NOT EXISTS series_events (
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;");
echo "</code></div>";
echo "<p class='success'>✅ Expected result: \"1 table created\"</p>";
echo "</div>";

echo "<h2>📍 Step 4: Insert Default Point Templates</h2>";
echo "<div class='step'>";
echo "<p>Copy and paste this SQL into phpMyAdmin and click <strong>\"Go\"</strong>:</p>";
echo "<div class='sql-box'><code>";
$swecup = json_encode(['1' => 100, '2' => 80, '3' => 60, '4' => 50, '5' => 45,
    '6' => 40, '7' => 36, '8' => 32, '9' => 29, '10' => 26,
    '11' => 24, '12' => 22, '13' => 20, '14' => 18, '15' => 16,
    '16' => 15, '17' => 14, '18' => 13, '19' => 12, '20' => 11,
    '21' => 10, '22' => 9, '23' => 8, '24' => 7, '25' => 6,
    '26' => 5, '27' => 4, '28' => 3, '29' => 2, '30' => 1]);
$uci = json_encode(['1' => 250, '2' => 200, '3' => 150, '4' => 120, '5' => 100,
    '6' => 90, '7' => 80, '8' => 70, '9' => 60, '10' => 50,
    '11' => 45, '12' => 40, '13' => 35, '14' => 30, '15' => 25,
    '16' => 20, '17' => 15, '18' => 10, '19' => 5, '20' => 1]);
$top10 = json_encode(['1' => 50, '2' => 40, '3' => 30, '4' => 25, '5' => 20,
    '6' => 15, '7' => 10, '8' => 7, '9' => 5, '10' => 3]);

echo htmlspecialchars("INSERT INTO qualification_point_templates (name, description, points, active) VALUES
('SweCup Standard', 'Standard SweCup poängfördelning', '" . $swecup . "', 1),
('UCI Standard', 'UCI standardpoäng', '" . $uci . "', 1),
('Top 10', 'Endast topp 10 får poäng', '" . $top10 . "', 1);");
echo "</code></div>";
echo "<p class='success'>✅ Expected result: \"3 rows inserted\"</p>";
echo "</div>";

echo "<h2>📍 Step 5 (Optional): Add format Column to series Table</h2>";
echo "<div class='step'>";
echo "<p>This is optional. The site works fine without it. If you want to add it:</p>";
echo "<div class='sql-box'><code>";
echo htmlspecialchars("ALTER TABLE series ADD COLUMN format VARCHAR(50) DEFAULT 'Championship';");
echo "</code></div>";
echo "<p class='info'>ℹ️ If this fails, don't worry - the site will work fine without it.</p>";
echo "</div>";

echo "<h2>📍 Step 6: Verify Installation</h2>";
echo "<div class='step'>";
echo "<p>After running the SQL commands, verify the tables exist:</p>";
echo "<ol>";
echo "<li>In phpMyAdmin, look at the left sidebar</li>";
echo "<li>You should see tables: <code>qualification_point_templates</code> and <code>series_events</code></li>";
echo "<li>Click on <code>qualification_point_templates</code> and verify it has 3 rows</li>";
echo "</ol>";
echo "</div>";

echo "<h2>✅ After Setup Complete</h2>";
echo "<div class='step'>";
echo "<p>Once you've run all the SQL commands successfully, you can use these pages:</p>";
echo "<p>";
echo "<a href='/admin/series.php' class='button'>Go to Series Page</a>";
echo "<a href='/admin/point-templates.php' class='button'>Go to Point Templates</a>";
echo "<a href='/admin/import-results.php' class='button'>Import Results</a>";
echo "</p>";
echo "</div>";

echo "<h2>❓ Troubleshooting</h2>";
echo "<div class='step'>";
echo "<p><strong>If tables already exist:</strong> You'll see \"Table already exists\" - that's OK!</p>";
echo "<p><strong>If you get errors:</strong> Make sure you're in the correct database (check the database name in the left sidebar)</p>";
echo "<p><strong>If INSERT fails:</strong> Tables might already have data. Check by clicking on the table name.</p>";
echo "</div>";

echo "</body></html>";
?>
