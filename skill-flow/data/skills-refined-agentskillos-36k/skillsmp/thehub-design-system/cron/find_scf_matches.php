<?php
/**
 * SCF License Match Finder Cron Job
 *
 * Searches for potential UCI ID matches for riders without a UCI ID
 * by querying the SCF License Portal API with name-based lookups.
 *
 * Usage:
 *   php find_scf_matches.php [options]
 *
 * Options:
 *   --year=YYYY       License year to search (default: current year)
 *   --limit=N         Max riders to process (default: 500)
 *   --min-score=N     Minimum match score to save (default: 60)
 *   --auto-confirm=N  Auto-confirm matches with score >= N (default: 0/disabled)
 *   --debug           Enable verbose output
 *   --dry-run         Don't update database, just show results
 *
 * Cron example (weekly on Sunday at 04:00):
 *   0 4 * * 0 cd /path/to/TheHUB/cron && php find_scf_matches.php --limit=500 >> /var/log/scf-match.log 2>&1
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
    'min-score:',
    'auto-confirm:',
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
$limit = isset($options['limit']) ? (int)$options['limit'] : 500;
$minScore = isset($options['min-score']) ? (float)$options['min-score'] : 60;
$autoConfirmThreshold = isset($options['auto-confirm']) ? (float)$options['auto-confirm'] : 0;
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
echo " SCF License Match Finder\n";
echo " $logDate\n";
echo "========================================\n\n";

echo "[CONFIG]\n";
echo "  Year: $year\n";
echo "  Limit: $limit\n";
echo "  Min score: $minScore%\n";
echo "  Auto-confirm threshold: " . ($autoConfirmThreshold > 0 ? "{$autoConfirmThreshold}%" : 'Disabled') . "\n";
echo "  Debug: " . ($debug ? 'Yes' : 'No') . "\n";
echo "  Dry run: " . ($dryRun ? 'Yes' : 'No') . "\n";
echo "\n";

// Get riders without UCI ID
$riders = $scfService->getRidersWithoutUciId($limit, 0);
$totalRiders = count($riders);

echo "[INFO] Found $totalRiders riders without UCI ID to process\n\n";

if ($totalRiders === 0) {
    echo "[INFO] No riders need matching. Exiting.\n";
    exit(0);
}

if ($dryRun) {
    echo "[DRY RUN] Would search for $totalRiders riders. No changes made.\n";
    exit(0);
}

// Start sync log
$syncId = $scfService->startSync('match_search', $year, $totalRiders, [
    'limit' => $limit,
    'min_score' => $minScore,
    'auto_confirm' => $autoConfirmThreshold
]);

$stats = [
    'processed' => 0,
    'matches_found' => 0,
    'matches_saved' => 0,
    'auto_confirmed' => 0,
    'errors' => 0
];

try {
    foreach ($riders as $index => $rider) {
        $stats['processed']++;

        $name = $rider['firstname'] . ' ' . $rider['lastname'];
        echo "[" . ($index + 1) . "/$totalRiders] Searching: $name... ";

        try {
            // Search for matches
            $matches = $scfService->findPotentialMatches($rider, $year);

            if (empty($matches)) {
                echo "No matches\n";
            } else {
                $bestMatch = $matches[0];
                $score = $bestMatch['score'];

                echo "Found " . count($matches) . " match(es), best: {$score}%\n";

                if ($score >= $minScore) {
                    // Save match candidate
                    if ($scfService->saveMatchCandidate($rider['id'], $rider, $bestMatch)) {
                        $stats['matches_found']++;
                        $stats['matches_saved']++;

                        // Auto-confirm if score is high enough
                        if ($autoConfirmThreshold > 0 && $score >= $autoConfirmThreshold) {
                            // Get the match ID
                            $matchRecord = $db->getRow(
                                "SELECT id FROM scf_match_candidates WHERE rider_id = ? AND status = 'pending' ORDER BY id DESC LIMIT 1",
                                [$rider['id']]
                            );
                            if ($matchRecord && $scfService->confirmMatch($matchRecord['id'], 0)) {
                                $stats['auto_confirmed']++;
                                echo "  -> Auto-confirmed (UCI: {$bestMatch['license']['uci_id']})\n";
                            }
                        } else {
                            echo "  -> Saved for review (UCI: {$bestMatch['license']['uci_id']})\n";
                        }
                    }
                } else {
                    echo "  -> Score too low ({$score}% < {$minScore}%)\n";
                }
            }

        } catch (Exception $e) {
            $stats['errors']++;
            echo "ERROR: " . $e->getMessage() . "\n";
        }

        // Update progress
        $scfService->updateSyncProgress(
            $stats['processed'],
            $stats['matches_found'],
            $stats['matches_saved'],
            $stats['errors']
        );

        // Rate limiting
        $scfService->rateLimit();

        // Progress every 50 riders
        if ($stats['processed'] % 50 === 0) {
            $progress = round(($stats['processed'] / $totalRiders) * 100, 1);
            echo "\n[PROGRESS] $progress% complete ({$stats['processed']}/$totalRiders)\n";
            echo "  Matches found: {$stats['matches_found']}, Saved: {$stats['matches_saved']}, Auto-confirmed: {$stats['auto_confirmed']}\n\n";
        }
    }

    // Complete sync
    $scfService->completeSync('completed');

    // Calculate duration
    $duration = round(microtime(true) - $startTime, 2);
    $avgTime = $stats['processed'] > 0 ? round($duration / $stats['processed'], 2) : 0;

    echo "\n========================================\n";
    echo " MATCH SEARCH COMPLETED\n";
    echo "========================================\n";
    echo "  Riders processed: {$stats['processed']}\n";
    echo "  Matches found: {$stats['matches_found']}\n";
    echo "  Matches saved: {$stats['matches_saved']}\n";
    echo "  Auto-confirmed: {$stats['auto_confirmed']}\n";
    echo "  Errors: {$stats['errors']}\n";
    echo "  Duration: {$duration}s ({$avgTime}s per rider)\n";
    echo "========================================\n";

    if ($stats['matches_saved'] > 0 && $stats['auto_confirmed'] < $stats['matches_saved']) {
        $toReview = $stats['matches_saved'] - $stats['auto_confirmed'];
        echo "\n[ACTION] $toReview match(es) pending review.\n";
        echo "         Visit: /admin/scf-match-review.php\n";
    }

    exit(0);

} catch (Exception $e) {
    $scfService->completeSync('failed', $e->getMessage());

    echo "\n[ERROR] Match search failed: " . $e->getMessage() . "\n";
    echo "[STACK] " . $e->getTraceAsString() . "\n";

    exit(1);
}
