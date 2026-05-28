<?php
/**
 * Debug Journey Analysis
 * Diagnostiserar varför journey-analysen hänger
 */
require_once __DIR__ . '/../config.php';
require_admin();

global $pdo;

header('Content-Type: text/plain; charset=utf-8');

echo "=== JOURNEY ANALYSIS DIAGNOSTIK ===\n\n";

// 1. Kolla analytics_jobs status
echo "1. ANALYTICS JOBS STATUS:\n";
echo str_repeat("-", 60) . "\n";
try {
    $stmt = $pdo->query("
        SELECT job_type, job_key, status, started_at, completed_at, last_heartbeat,
               TIMESTAMPDIFF(MINUTE, started_at, NOW()) as running_minutes
        FROM analytics_jobs
        WHERE status = 'running'
        ORDER BY started_at DESC
        LIMIT 10
    ");
    $running = $stmt->fetchAll(PDO::FETCH_ASSOC);

    if (empty($running)) {
        echo "   Inga jobb kör just nu.\n";
    } else {
        foreach ($running as $job) {
            echo "   KÖRANDE: {$job['job_type']} / {$job['job_key']}\n";
            echo "   Startad: {$job['started_at']} ({$job['running_minutes']} min sedan)\n";
            echo "   Heartbeat: {$job['last_heartbeat']}\n\n";
        }
    }
} catch (Exception $e) {
    echo "   FEL: " . $e->getMessage() . "\n";
}

// 2. Kolla senaste jobb
echo "\n2. SENASTE ANALYTICS JOBS:\n";
echo str_repeat("-", 60) . "\n";
try {
    $stmt = $pdo->query("
        SELECT job_type, job_key, status, started_at, completed_at, rows_affected, error_message
        FROM analytics_jobs
        ORDER BY started_at DESC
        LIMIT 10
    ");
    $recent = $stmt->fetchAll(PDO::FETCH_ASSOC);

    foreach ($recent as $job) {
        $status = strtoupper($job['status']);
        echo "   [{$status}] {$job['job_type']} / {$job['job_key']}\n";
        echo "   Started: {$job['started_at']} | Completed: " . ($job['completed_at'] ?? 'N/A') . "\n";
        if ($job['error_message']) {
            echo "   ERROR: {$job['error_message']}\n";
        }
        echo "\n";
    }
} catch (Exception $e) {
    echo "   FEL: " . $e->getMessage() . "\n";
}

// 3. Kolla rider_first_season data
echo "\n3. RIDER_FIRST_SEASON STATUS:\n";
echo str_repeat("-", 60) . "\n";
try {
    $stmt = $pdo->query("
        SELECT cohort_year, COUNT(*) as cnt
        FROM rider_first_season
        GROUP BY cohort_year
        ORDER BY cohort_year DESC
    ");
    $data = $stmt->fetchAll(PDO::FETCH_ASSOC);

    if (empty($data)) {
        echo "   TOMT! Ingen data i rider_first_season.\n";
    } else {
        foreach ($data as $row) {
            echo "   Kohort {$row['cohort_year']}: {$row['cnt']} riders\n";
        }
    }
} catch (Exception $e) {
    echo "   FEL: " . $e->getMessage() . "\n";
}

// 4. Rensa hängande jobb?
echo "\n4. RENSA HÄNGANDE JOBB:\n";
echo str_repeat("-", 60) . "\n";
try {
    // Jobb som kört mer än 10 minuter utan heartbeat är troligen döda
    $stmt = $pdo->prepare("
        UPDATE analytics_jobs
        SET status = 'failed', error_message = 'Timeout - inget heartbeat på 10 min'
        WHERE status = 'running'
        AND (last_heartbeat IS NULL OR TIMESTAMPDIFF(MINUTE, last_heartbeat, NOW()) > 10)
    ");
    $stmt->execute();
    $cleaned = $stmt->rowCount();

    echo "   Rensade {$cleaned} hängande jobb.\n";
} catch (Exception $e) {
    echo "   FEL: " . $e->getMessage() . "\n";
}

// 5. Test: Räkna rookies för ett år
echo "\n5. TEST: RÄKNA ROOKIES 2024:\n";
echo str_repeat("-", 60) . "\n";
try {
    $stmt = $pdo->prepare("
        SELECT COUNT(DISTINCT v.canonical_rider_id) as rookies
        FROM results res
        JOIN events e ON res.event_id = e.id
        JOIN v_canonical_riders v ON res.cyclist_id = v.original_rider_id
        GROUP BY v.canonical_rider_id
        HAVING MIN(YEAR(e.date)) = 2024
    ");
    $stmt->execute();
    $count = $stmt->rowCount();

    echo "   Antal rookies 2024: {$count}\n";
} catch (Exception $e) {
    echo "   FEL: " . $e->getMessage() . "\n";
}

// 6. Test: Kör en mini-beräkning
echo "\n6. TEST: MINI-BERÄKNING (1 kohort):\n";
echo str_repeat("-", 60) . "\n";
try {
    require_once __DIR__ . '/../analytics/includes/AnalyticsEngine.php';

    $engine = new AnalyticsEngine($pdo);
    $engine->setForceRerun(true);

    echo "   Startar beräkning för 2024...\n";
    $start = microtime(true);

    $result = $engine->calculateFirstSeasonJourney(2024);

    $elapsed = round(microtime(true) - $start, 2);
    echo "   Resultat: {$result} riders processade på {$elapsed}s\n";

} catch (Exception $e) {
    echo "   FEL: " . $e->getMessage() . "\n";
    echo "   Stack: " . $e->getTraceAsString() . "\n";
} catch (Throwable $t) {
    echo "   FATAL: " . $t->getMessage() . "\n";
    echo "   Stack: " . $t->getTraceAsString() . "\n";
}

echo "\n=== SLUT ===\n";
