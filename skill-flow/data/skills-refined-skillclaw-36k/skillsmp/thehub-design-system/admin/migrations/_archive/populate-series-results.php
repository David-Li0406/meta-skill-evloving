<?php
/**
 * Migration: Populate series_results table
 *
 * This script populates the new series_results table using:
 * - series_events.template_id -> qualification_point_templates
 * - Results from the results table
 *
 * Run this AFTER running 037_series_results_table.sql
 *
 * IMPORTANT: This creates series-specific points that are SEPARATE from ranking points!
 */

error_reporting(E_ALL);
ini_set('display_errors', 1);
ini_set('max_execution_time', 300); // 5 minutes
set_time_limit(300);

// Disable output buffering for real-time progress
if (ob_get_level()) ob_end_flush();
ob_implicit_flush(true);

require_once __DIR__ . '/../../config.php';
require_once __DIR__ . '/../../includes/series-points.php';
require_admin();

$db = getDB();

echo "<!DOCTYPE html><html><head><meta charset='UTF-8'><title>Populate Series Results</title>";
echo "<style>
body { font-family: monospace; padding: 20px; background: #f5f5f5; max-width: 1200px; margin: 0 auto; }
.success { color: green; }
.error { color: red; }
.info { color: blue; }
.warning { color: orange; }
h1 { border-bottom: 2px solid #333; padding-bottom: 10px; }
h2 { margin-top: 30px; border-bottom: 1px solid #999; padding-bottom: 5px; }
.stats { background: #e8f5e9; padding: 15px; border-radius: 5px; margin: 20px 0; }
.series-block { background: white; padding: 15px; margin: 10px 0; border-radius: 5px; border-left: 4px solid #2196F3; }
</style>";
echo "</head><body>";
echo "<h1>Migration: Populate Series Results Table</h1>";

// Check if series_results table exists
try {
    $db->getRow("SELECT 1 FROM series_results LIMIT 1");
    echo "<p class='success'>✓ series_results table exists</p>";
} catch (Exception $e) {
    echo "<p class='error'>✗ series_results table does not exist!</p>";
    echo "<p>Please run the SQL migration first:</p>";
    echo "<pre>mysql -u root -p thehub < database/migrations/037_series_results_table.sql</pre>";
    echo "</body></html>";
    exit(1);
}

// Check if qualification_point_templates exists
try {
    $templates = $db->getAll("SELECT id, name, points FROM qualification_point_templates WHERE active = 1");
    echo "<p class='success'>✓ Found " . count($templates) . " active point templates</p>";

    if (count($templates) === 0) {
        echo "<p class='warning'>⚠ No active templates found! Series points will be 0.</p>";
    }
} catch (Exception $e) {
    echo "<p class='error'>✗ qualification_point_templates table error: " . htmlspecialchars($e->getMessage()) . "</p>";
    echo "</body></html>";
    exit(1);
}

// Get all series with events
$seriesList = $db->getAll("
    SELECT DISTINCT s.id, s.name, s.year,
           COUNT(DISTINCT se.event_id) as event_count
    FROM series s
    JOIN series_events se ON s.id = se.series_id
    GROUP BY s.id
    ORDER BY s.year DESC, s.name
");

echo "<h2>Found " . count($seriesList) . " series with events</h2>";

$totalStats = [
    'series' => 0,
    'events' => 0,
    'inserted' => 0,
    'updated' => 0,
    'deleted' => 0
];

foreach ($seriesList as $series) {
    echo "<div class='series-block'>";
    echo "<h3>{$series['name']} ({$series['year']}) - {$series['event_count']} events</h3>";
    flush();

    try {
        // Recalculate all series points
        echo "<p class='info'>Beräknar poäng...</p>";
        flush();

        $stats = recalculateAllSeriesPoints($db, $series['id']);

        echo "<p class='success'>";
        echo "Events: {$stats['events']}, ";
        echo "Inserted: {$stats['inserted']}, ";
        echo "Updated: {$stats['updated']}, ";
        echo "Deleted: {$stats['deleted']}";
        echo "</p>";

        // Update totals
        $totalStats['series']++;
        $totalStats['events'] += $stats['events'];
        $totalStats['inserted'] += $stats['inserted'];
        $totalStats['updated'] += $stats['updated'];
        $totalStats['deleted'] += $stats['deleted'];
    } catch (Exception $e) {
        echo "<p class='error'>FEL: " . htmlspecialchars($e->getMessage()) . "</p>";
        echo "<pre>" . htmlspecialchars($e->getTraceAsString()) . "</pre>";
    }

    echo "</div>";
    flush();
}

echo "<div class='stats'>";
echo "<h2>Total Migration Stats</h2>";
echo "<ul>";
echo "<li><strong>Series processed:</strong> {$totalStats['series']}</li>";
echo "<li><strong>Events processed:</strong> {$totalStats['events']}</li>";
echo "<li><strong>Results inserted:</strong> {$totalStats['inserted']}</li>";
echo "<li><strong>Results updated:</strong> {$totalStats['updated']}</li>";
echo "<li><strong>Results deleted:</strong> {$totalStats['deleted']}</li>";
echo "</ul>";
echo "</div>";

// Verify data
$totalSeriesResults = $db->getRow("SELECT COUNT(*) as cnt FROM series_results");
echo "<p class='success'>✓ Total rows in series_results: <strong>{$totalSeriesResults['cnt']}</strong></p>";

echo "<h2 class='success'>✅ Migration completed!</h2>";
echo "<p><a href='/admin/series.php'>Go to Series Admin</a></p>";
echo "<p><a href='/series.php'>Go to Public Series Page</a></p>";

echo "</body></html>";
