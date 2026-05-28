<?php
require_once __DIR__ . '/../config.php';

global $pdo;

echo "=== RANKING SYSTEM STATUS ===\n\n";

// Check tables
$tables = ['ranking_settings', 'ranking_snapshots', 'ranking_history', 'club_ranking_snapshots'];
echo "1. DATABASE TABLES:\n";
foreach ($tables as $table) {
    $stmt = $pdo->query("SHOW TABLES LIKE '$table'");
    $exists = $stmt->rowCount() > 0;
    echo "   $table: " . ($exists ? "✓ EXISTS" : "✗ MISSING") . "\n";
}

// Check event_level column
echo "\n2. EVENTS TABLE:\n";
$stmt = $pdo->query("SHOW COLUMNS FROM events LIKE 'event_level'");
$hasEventLevel = $stmt->rowCount() > 0;
echo "   event_level column: " . ($hasEventLevel ? "✓ EXISTS" : "✗ MISSING") . "\n";

if ($hasEventLevel) {
    $stmt = $pdo->query("SELECT event_level, COUNT(*) as cnt FROM events GROUP BY event_level");
    $levels = $stmt->fetchAll(PDO::FETCH_ASSOC);
    echo "   Distribution:\n";
    foreach ($levels as $l) {
        echo "   - " . ($l['event_level'] ?: 'NULL') . ": " . $l['cnt'] . " events\n";
    }
}

// Check results with points
echo "\n3. RESULTS WITH POINTS (last 24 months):\n";
$cutoff = date('Y-m-d', strtotime('-24 months'));
$stmt = $pdo->prepare("
    SELECT COUNT(*) as total,
           COUNT(CASE WHEN r.points > 0 THEN 1 END) as with_points,
           COUNT(DISTINCT r.cyclist_id) as unique_riders
    FROM results r
    JOIN events e ON r.event_id = e.id
    WHERE e.date >= ? AND r.status = 'finished'
");
$stmt->execute([$cutoff]);
$stats = $stmt->fetch(PDO::FETCH_ASSOC);
echo "   Total finished results: " . $stats['total'] . "\n";
echo "   Results with points > 0: " . $stats['with_points'] . "\n";
echo "   Unique riders: " . $stats['unique_riders'] . "\n";

// Check ranking settings
echo "\n4. RANKING SETTINGS:\n";
try {
    $stmt = $pdo->query("SELECT setting_key, LEFT(setting_value, 50) as val FROM ranking_settings");
    $settings = $stmt->fetchAll(PDO::FETCH_ASSOC);
    if (empty($settings)) {
        echo "   ✗ NO SETTINGS FOUND - Run calculation to create defaults\n";
    } else {
        foreach ($settings as $s) {
            echo "   " . $s['setting_key'] . ": " . $s['val'] . "...\n";
        }
    }
} catch (Exception $e) {
    echo "   ✗ ERROR: " . $e->getMessage() . "\n";
}

echo "\n=== END STATUS ===\n";
