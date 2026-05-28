<?php
/**
 * SCF License Sync Cron Job
 *
 * Synchronizes rider licenses with Svenska Cykelförbundet's License Portal.
 * Run via cron for automated daily/weekly updates.
 *
 * Usage:
 *   php sync_scf_licenses.php [options]
 *
 * Options:
 *   --year=YYYY        License year (default: current year)
 *   --limit=N          Max riders to process (default: 5000)
 *   --batch-size=N     Riders per batch (default: 25, max 25)
 *   --all              Sync all riders, not just unverified
 *   --history-years=Y  Also sync these years (comma-separated)
 *   --debug            Enable verbose output
 *   --dry-run          Don't update database, just show what would happen
 *
 * Cron example (daily at 03:00):
 *   0 3 * * * cd /path/to/TheHUB/cron && php sync_scf_licenses.php --year=2026 >> /var/log/scf-sync.log 2>&1
 *
 * @package TheHUB
 * @version 1.0
 */

// CLI only
if (php_sapi_name() !== 'cli') {
    die("This script must be run from the command line.\n");
}

// Parse command line options
$options = getopt('', [
    'year:',
    'limit:',
    'batch-size:',
    'all',
    'history-years:',
    'debug',
    'dry-run'
]);

// Set working directory
chdir(__DIR__ . '/..');

// Load dependencies
require_once __DIR__ . '/../config.php';
require_once __DIR__ . '/../includes/SCFLicenseService.php';

// Configuration
$year = isset($options['year']) ? (int)$options['year'] : (int)date('Y');
$limit = isset($options['limit']) ? (int)$options['limit'] : 5000;
$batchSize = min(25, isset($options['batch-size']) ? (int)$options['batch-size'] : 25);
$onlyUnverified = !isset($options['all']);
$historyYears = isset($options['history-years']) ? explode(',', $options['history-years']) : [];
$debug = isset($options['debug']);
$dryRun = isset($options['dry-run']);

// Get API key
$apiKey = env('SCF_API_KEY', '');
if (empty($apiKey)) {
    echo "[ERROR] SCF_API_KEY not configured in .env file.\n";
    exit(1);
}

// Initialize
$db = getDB();
$scfService = new SCFLicenseService($apiKey, $db);
$scfService->setDebug($debug);

// Start logging
$startTime = microtime(true);
$logDate = date('Y-m-d H:i:s');

echo "========================================\n";
echo " SCF License Sync\n";
echo " $logDate\n";
echo "========================================\n\n";

echo "[CONFIG]\n";
echo "  Year: $year\n";
echo "  Limit: $limit\n";
echo "  Batch size: $batchSize\n";
echo "  Only unverified: " . ($onlyUnverified ? 'Yes' : 'No') . "\n";
echo "  History years: " . (empty($historyYears) ? 'None' : implode(', ', $historyYears)) . "\n";
echo "  Debug: " . ($debug ? 'Yes' : 'No') . "\n";
echo "  Dry run: " . ($dryRun ? 'Yes' : 'No') . "\n";
echo "\n";

// Get rider count
$totalToSync = $scfService->countRidersToSync($year, $onlyUnverified);
$actualLimit = min($totalToSync, $limit);

echo "[INFO] Found $totalToSync riders to sync (processing up to $actualLimit)\n\n";

if ($totalToSync === 0) {
    echo "[INFO] No riders need syncing. Exiting.\n";
    exit(0);
}

if ($dryRun) {
    echo "[DRY RUN] Would sync $actualLimit riders. No changes made.\n";
    exit(0);
}

// Start sync
$syncId = $scfService->startSync('full', $year, $actualLimit, [
    'limit' => $limit,
    'batch_size' => $batchSize,
    'only_unverified' => $onlyUnverified
]);

$totalStats = [
    'processed' => 0,
    'found' => 0,
    'updated' => 0,
    'errors' => 0
];

try {
    $offset = 0;

    while ($offset < $actualLimit) {
        // Get batch of riders
        $riders = $scfService->getRidersToSync($year, $batchSize, $offset, $onlyUnverified);

        if (empty($riders)) {
            break;
        }

        echo "[BATCH] Processing " . count($riders) . " riders (offset: $offset)...\n";

        // Process batch
        $stats = $scfService->syncRiderBatch($riders, $year);

        // Accumulate stats
        $totalStats['processed'] += $stats['processed'];
        $totalStats['found'] += $stats['found'];
        $totalStats['updated'] += $stats['updated'];
        $totalStats['errors'] += $stats['errors'];

        // Update progress
        $scfService->updateSyncProgress(
            $totalStats['processed'],
            $totalStats['found'],
            $totalStats['updated'],
            $totalStats['errors']
        );

        // Progress output
        $progress = round(($totalStats['processed'] / $actualLimit) * 100, 1);
        echo "  Progress: $progress% ({$totalStats['processed']}/$actualLimit)\n";
        echo "  Found: {$totalStats['found']}, Updated: {$totalStats['updated']}, Errors: {$totalStats['errors']}\n";

        $offset += $batchSize;

        // Rate limiting between batches
        $scfService->rateLimit();
    }

    // Sync history years if specified
    foreach ($historyYears as $histYear) {
        $histYear = trim($histYear);
        if (!$histYear || $histYear == $year) continue;

        echo "\n[HISTORY] Syncing year $histYear...\n";

        $histOffset = 0;
        while ($histOffset < $actualLimit) {
            $riders = $scfService->getRidersToSync((int)$histYear, $batchSize, $histOffset, true);
            if (empty($riders)) break;

            $stats = $scfService->syncRiderBatch($riders, (int)$histYear);
            echo "  Processed: {$stats['processed']}, Found: {$stats['found']}\n";

            $histOffset += $batchSize;
            $scfService->rateLimit();
        }
    }

    // Complete sync
    $scfService->completeSync('completed');

    // Calculate duration
    $duration = round(microtime(true) - $startTime, 2);

    echo "\n========================================\n";
    echo " SYNC COMPLETED\n";
    echo "========================================\n";
    echo "  Total processed: {$totalStats['processed']}\n";
    echo "  Found in SCF: {$totalStats['found']}\n";
    echo "  Updated: {$totalStats['updated']}\n";
    echo "  Errors: {$totalStats['errors']}\n";
    echo "  Duration: {$duration}s\n";
    echo "========================================\n";

    exit(0);

} catch (Exception $e) {
    $scfService->completeSync('failed', $e->getMessage());

    echo "\n[ERROR] Sync failed: " . $e->getMessage() . "\n";
    echo "[STACK] " . $e->getTraceAsString() . "\n";

    exit(1);
}
