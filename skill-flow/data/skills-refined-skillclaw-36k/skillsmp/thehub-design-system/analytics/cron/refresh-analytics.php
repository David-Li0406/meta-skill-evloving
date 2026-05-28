<?php
/**
 * Analytics Cron Job - Uppdatera analytics-data
 *
 * Kor dagligen via cron:
 * 0 3 * * * php /path/to/analytics/cron/refresh-analytics.php
 *
 * Vad den gor:
 * 1. Uppdaterar rider_yearly_stats for aktuellt ar
 * 2. Uppdaterar series_participation
 * 3. Uppdaterar series_crossover
 * 4. Uppdaterar club_yearly_stats
 * 5. Uppdaterar venue_yearly_stats
 * 6. Skapar daglig snapshot
 * 7. Loggar korstatus
 *
 * @package TheHUB Analytics
 * @version 1.0
 */

// Kor bara fran CLI
if (php_sapi_name() !== 'cli') {
    http_response_code(403);
    die('CLI only');
}

require_once __DIR__ . '/../../config.php';
require_once __DIR__ . '/../includes/AnalyticsEngine.php';

// Tid och loggning
$startTime = microtime(true);
$currentYear = (int)date('Y');
$runId = null;

/**
 * Logga till analytics_cron_runs
 */
function logCronRun(PDO $pdo, string $jobName, string $status, ?int $processed = null, ?string $error = null, ?float $duration = null): int {
    $stmt = $pdo->prepare("
        INSERT INTO analytics_cron_runs (job_name, status, records_processed, error_message, duration_seconds)
        VALUES (?, ?, ?, ?, ?)
    ");
    $stmt->execute([$jobName, $status, $processed, $error, $duration]);
    return (int)$pdo->lastInsertId();
}

/**
 * Uppdatera cron run status
 */
function updateCronRun(PDO $pdo, int $runId, string $status, ?int $processed = null, ?string $error = null, ?float $duration = null): void {
    $stmt = $pdo->prepare("
        UPDATE analytics_cron_runs
        SET status = ?, records_processed = ?, error_message = ?, duration_seconds = ?, completed_at = NOW()
        WHERE id = ?
    ");
    $stmt->execute([$status, $processed, $error, $duration, $runId]);
}

// Output header
echo "========================================\n";
echo " TheHUB Analytics - Daily Refresh\n";
echo " " . date('Y-m-d H:i:s') . "\n";
echo "========================================\n\n";

try {
    global $pdo;

    // Logga start
    $runId = logCronRun($pdo, 'daily_refresh', 'running');

    echo "[INFO] Starting analytics refresh for {$currentYear}...\n";

    // Initiera engine
    $engine = new AnalyticsEngine($pdo);

    // Kör alla uppdateringar
    $results = $engine->refreshAllStats($currentYear);

    // Summera
    $totalProcessed = array_sum($results);
    $duration = microtime(true) - $startTime;

    // Uppdatera run status
    updateCronRun($pdo, $runId, 'completed', $totalProcessed, null, $duration);

    // Output resultat
    echo "\n[RESULTS]\n";
    foreach ($results as $table => $count) {
        echo "  - {$table}: {$count} records\n";
    }

    echo "\n[SUMMARY]\n";
    echo "  Total records: " . number_format($totalProcessed) . "\n";
    echo "  Duration: " . round($duration, 2) . " seconds\n";
    echo "  Status: COMPLETED\n";

    // Skapa daglig snapshot
    echo "\n[INFO] Creating daily snapshot...\n";

    $snapshotData = [
        'total_riders' => $results['rider_yearly_stats'] ?? 0,
        'series_participations' => $results['series_participation'] ?? 0,
        'club_stats' => $results['club_yearly_stats'] ?? 0,
        'venue_stats' => $results['venue_yearly_stats'] ?? 0,
        'crossover_entries' => $results['series_crossover'] ?? 0,
        'refresh_duration' => round($duration, 2)
    ];

    $stmt = $pdo->prepare("
        INSERT INTO analytics_snapshots (snapshot_type, snapshot_date, metrics_data, calculation_version)
        VALUES ('daily_stats', CURDATE(), ?, 1)
        ON DUPLICATE KEY UPDATE
            metrics_data = VALUES(metrics_data),
            created_at = NOW()
    ");
    $stmt->execute([json_encode($snapshotData)]);

    echo "  Snapshot saved.\n";

    echo "\n========================================\n";
    echo " ANALYTICS REFRESH COMPLETED\n";
    echo "========================================\n";

    exit(0);

} catch (Exception $e) {
    $duration = microtime(true) - $startTime;

    // Logga fel
    if ($runId) {
        updateCronRun($pdo, $runId, 'failed', null, $e->getMessage(), $duration);
    }

    echo "\n[ERROR] " . $e->getMessage() . "\n";
    echo "  Duration: " . round($duration, 2) . " seconds\n";
    echo "  Status: FAILED\n";

    // Skicka alert (om konfigurerat)
    // mail('admin@example.com', 'Analytics Cron Failed', $e->getMessage());

    exit(1);
}
