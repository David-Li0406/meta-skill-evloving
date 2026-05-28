<?php
/**
 * Check table structure and locks
 */
error_reporting(E_ALL);
ini_set('display_errors', 1);

echo "<h1>Table Structure Check</h1>";
echo "<pre>";

try {
    require_once __DIR__ . '/../config.php';
    $db = getDB();

    echo "1. Checking SHOW CREATE TABLE...\n";
    $create = $db->getRow("SHOW CREATE TABLE ranking_points");
    echo $create['Create Table'] . "\n\n";

    echo "2. Checking for locks...\n";
    $locks = $db->getAll("SHOW OPEN TABLES WHERE In_use > 0 AND `Table` = 'ranking_points'");
    if (empty($locks)) {
        echo "   No locks found\n\n";
    } else {
        echo "   ⚠️ Locks found:\n";
        print_r($locks);
        echo "\n";
    }

    echo "3. Checking SHOW PROCESSLIST...\n";
    $processes = $db->getAll("SHOW PROCESSLIST");
    echo "   Active queries:\n";
    foreach ($processes as $p) {
        if (!empty($p['Info']) && $p['Info'] !== 'SHOW PROCESSLIST') {
            echo "   - ID: {$p['Id']}, Time: {$p['Time']}s, State: {$p['State']}\n";
            echo "     Query: " . substr($p['Info'], 0, 100) . "\n";
        }
    }
    echo "\n";

    echo "4. Trying simple SELECT...\n";
    $start = microtime(true);
    $count = $db->getRow("SELECT COUNT(*) as cnt FROM ranking_points");
    $duration = round((microtime(true) - $start) * 1000, 2);
    echo "   ✅ SELECT works: {$count['cnt']} rows in {$duration}ms\n\n";

    echo "5. Trying DELETE with LIMIT (safer)...\n";
    $start = microtime(true);
    $cutoffDate = date('Y-m-d', strtotime('-24 months'));
    $db->query("DELETE FROM ranking_points WHERE event_date >= ? LIMIT 1000", [$cutoffDate]);
    $duration = round((microtime(true) - $start) * 1000, 2);
    echo "   ✅ DELETE with LIMIT works in {$duration}ms\n\n";

    echo "6. Checking if table needs optimization...\n";
    $status = $db->getRow("SHOW TABLE STATUS LIKE 'ranking_points'");
    echo "   Rows: {$status['Rows']}\n";
    echo "   Data_length: {$status['Data_length']}\n";
    echo "   Index_length: {$status['Index_length']}\n";
    echo "   Data_free: {$status['Data_free']}\n\n";

} catch (Exception $e) {
    echo "\n❌ ERROR:\n";
    echo "Message: " . $e->getMessage() . "\n";
    echo "File: " . $e->getFile() . "\n";
    echo "Line: " . $e->getLine() . "\n";
}

echo "</pre>";
?>
