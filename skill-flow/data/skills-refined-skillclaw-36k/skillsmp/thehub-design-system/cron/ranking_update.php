<?php
/**
 * Ranking Update Cron Job
 *
 * Automatically updates the ranking system on the 1st of each month.
 * Run this script via cron:
 *
 * 0 2 1 * * /usr/bin/php /path/to/TheHUB/cron/ranking_update.php >> /var/log/ranking.log 2>&1
 *
 * This will run at 02:00 on the 1st of every month.
 */

// Only run from CLI
if (php_sapi_name() !== 'cli') {
    die("This script must be run from the command line.\n");
}

// Set working directory
chdir(__DIR__ . '/..');

// Load dependencies
require_once __DIR__ . '/../config.php';
require_once __DIR__ . '/../includes/ranking_functions.php';

// Start logging
$startTime = microtime(true);
$logDate = date('Y-m-d H:i:s');

echo "[$logDate] Ranking update started\n";

try {
    $db = getDB();

    // Check if tables exist
    if (!rankingTablesExist($db)) {
        echo "[$logDate] ERROR: Ranking tables do not exist. Run migration first.\n";
        exit(1);
    }

    // Run full ranking update (calculates all disciplines and creates snapshots)
    echo "[$logDate] Running full ranking update...\n";
    $stats = runFullRankingUpdate($db, false); // false = no debug output

    echo "[$logDate] Ranking update completed:\n";
    echo "  - Enduro: {$stats['enduro']['riders']} riders, {$stats['enduro']['clubs']} clubs\n";
    echo "  - Downhill: {$stats['dh']['riders']} riders, {$stats['dh']['clubs']} clubs\n";
    echo "  - Gravity: {$stats['gravity']['riders']} riders, {$stats['gravity']['clubs']} clubs\n";
    echo "  - Total time: {$stats['total_time']}s\n";

    // Calculate execution time
    $endTime = microtime(true);
    $duration = round($endTime - $startTime, 2);

    echo "[$logDate] Ranking update completed successfully in {$duration}s\n";

} catch (Exception $e) {
    echo "[$logDate] ERROR: " . $e->getMessage() . "\n";
    echo "[$logDate] Stack trace:\n" . $e->getTraceAsString() . "\n";
    exit(1);
}

exit(0);
