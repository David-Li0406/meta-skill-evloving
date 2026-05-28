<?php
/**
 * Test just the DELETE query
 */
error_reporting(E_ALL);
ini_set('display_errors', 1);

echo "<h1>DELETE Query Test</h1>";
echo "<pre>";

try {
    require_once __DIR__ . '/../config.php';
    $db = getDB();

    $cutoffDate = date('Y-m-d', strtotime('-24 months'));
    echo "1. Cutoff date: {$cutoffDate}\n\n";

    echo "2. Checking current row count...\n";
    $before = $db->getRow("SELECT COUNT(*) as cnt FROM ranking_points");
    echo "   Current rows: {$before['cnt']}\n\n";

    echo "3. Running DELETE query...\n";
    $startTime = microtime(true);
    $db->query("DELETE FROM ranking_points WHERE event_date >= ?", [$cutoffDate]);
    $endTime = microtime(true);
    $duration = round(($endTime - $startTime) * 1000, 2);
    echo "   ✅ DELETE completed in {$duration}ms\n\n";

    echo "4. Checking row count after delete...\n";
    $after = $db->getRow("SELECT COUNT(*) as cnt FROM ranking_points");
    echo "   Rows after: {$after['cnt']}\n";
    echo "   Deleted: " . ($before['cnt'] - $after['cnt']) . " rows\n\n";

    echo "✅ DELETE query works fine!\n";

} catch (Exception $e) {
    echo "\n❌ ERROR:\n";
    echo "Message: " . $e->getMessage() . "\n";
    echo "File: " . $e->getFile() . "\n";
    echo "Line: " . $e->getLine() . "\n\n";
    echo "Stack trace:\n" . $e->getTraceAsString();
}

echo "</pre>";
?>
