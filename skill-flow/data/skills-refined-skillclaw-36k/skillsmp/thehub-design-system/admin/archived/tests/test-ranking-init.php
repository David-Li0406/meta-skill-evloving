<?php
// Minimal test to find where the error occurs
error_reporting(E_ALL);
ini_set('display_errors', 1);
ini_set('display_startup_errors', 1);

echo "1. Starting test...<br>\n";
flush();

try {
    echo "2. Loading config...<br>\n";
    flush();
    require_once __DIR__ . '/../config.php';
    echo "3. Config loaded OK<br>\n";
    flush();

    echo "4. Getting DB connection...<br>\n";
    flush();
    $db = getDB();
    echo "5. DB connected OK<br>\n";
    flush();

    echo "6. Loading ranking_functions.php...<br>\n";
    flush();
    require_once __DIR__ . '/../includes/ranking_functions.php';
    echo "7. Functions loaded OK<br>\n";
    flush();

    echo "8. Checking admin...<br>\n";
    flush();
    require_admin();
    echo "9. Admin check passed<br>\n";
    flush();

    echo "10. Getting current admin...<br>\n";
    flush();
    $current_admin = get_current_admin();
    echo "11. Current admin: " . ($current_admin ? $current_admin['username'] : 'none') . "<br>\n";
    flush();

    echo "12. Checking if ranking tables exist...<br>\n";
    flush();
    $exists = rankingTablesExist($db);
    echo "13. Ranking tables exist: " . ($exists ? 'YES' : 'NO') . "<br>\n";
    flush();

    echo "14. Getting field multipliers...<br>\n";
    flush();
    $multipliers = getRankingFieldMultipliers($db);
    echo "15. Got " . count($multipliers) . " multipliers<br>\n";
    flush();

    echo "16. Getting time decay...<br>\n";
    flush();
    $timeDecay = getRankingTimeDecay($db);
    echo "17. Got time decay settings<br>\n";
    flush();

    echo "18. Getting event level multipliers...<br>\n";
    flush();
    $eventLevelMultipliers = getEventLevelMultipliers($db);
    echo "19. Got event level multipliers<br>\n";
    flush();

    echo "20. Getting last calculation...<br>\n";
    flush();
    $lastCalc = getLastRankingCalculation($db);
    echo "21. Last calc: " . ($lastCalc['date'] ?? 'never') . "<br>\n";
    flush();

    echo "22. Getting ranking stats...<br>\n";
    flush();
    $disciplineStats = getRankingStats($db);
    echo "23. Got stats for " . count($disciplineStats) . " disciplines<br>\n";
    flush();

    echo "24. Getting last snapshot...<br>\n";
    flush();
    $latestSnapshot = $db->getRow("SELECT MAX(snapshot_date) as snapshot_date FROM ranking_snapshots");
    echo "25. Last snapshot: " . ($latestSnapshot['snapshot_date'] ?? 'never') . "<br>\n";
    flush();

    echo "<br><strong>✅ ALL TESTS PASSED!</strong><br>\n";
    echo "<a href='/admin/ranking.php'>Try ranking.php again</a>";

} catch (Exception $e) {
    echo "<br><strong>❌ ERROR CAUGHT:</strong><br>\n";
    echo "<pre>";
    echo "Message: " . htmlspecialchars($e->getMessage()) . "\n\n";
    echo "File: " . htmlspecialchars($e->getFile()) . "\n";
    echo "Line: " . $e->getLine() . "\n\n";
    echo "Stack trace:\n" . htmlspecialchars($e->getTraceAsString());
    echo "</pre>";
} catch (Error $e) {
    echo "<br><strong>❌ FATAL ERROR CAUGHT:</strong><br>\n";
    echo "<pre>";
    echo "Message: " . htmlspecialchars($e->getMessage()) . "\n\n";
    echo "File: " . htmlspecialchars($e->getFile()) . "\n";
    echo "Line: " . $e->getLine() . "\n\n";
    echo "Stack trace:\n" . htmlspecialchars($e->getTraceAsString());
    echo "</pre>";
}
?>
