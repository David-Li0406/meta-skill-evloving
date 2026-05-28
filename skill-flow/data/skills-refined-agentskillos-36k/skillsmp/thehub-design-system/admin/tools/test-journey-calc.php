<?php
/**
 * Test Journey Calculation
 * Visar exakt vad som händer vid Journey-beräkning
 */
require_once __DIR__ . '/../../config.php';
require_admin();

header('Content-Type: text/plain; charset=utf-8');

$year = isset($_GET['year']) ? (int)$_GET['year'] : 2025;

echo "=== TEST JOURNEY CALCULATION FOR {$year} ===\n\n";

global $pdo;

// 1. Check how many riders started in this year (rookies)
echo "1. ROOKIES FÖR {$year}:\n";
echo str_repeat("-", 50) . "\n";

$sql = "
    SELECT COUNT(DISTINCT v.canonical_rider_id) as rookies
    FROM results res
    JOIN events e ON res.event_id = e.id
    JOIN v_canonical_riders v ON res.cyclist_id = v.original_rider_id
    WHERE YEAR(e.date) = ?
    AND v.canonical_rider_id NOT IN (
        SELECT DISTINCT v2.canonical_rider_id
        FROM results res2
        JOIN events e2 ON res2.event_id = e2.id
        JOIN v_canonical_riders v2 ON res2.cyclist_id = v2.original_rider_id
        WHERE YEAR(e2.date) < ?
    )
";

try {
    $stmt = $pdo->prepare($sql);
    $stmt->execute([$year, $year]);
    $count = $stmt->fetchColumn();
    echo "   Rookies (nya {$year}): {$count}\n";
} catch (Exception $e) {
    echo "   FEL: " . $e->getMessage() . "\n";
}

// 2. Check rider_first_season table
echo "\n2. RIDER_FIRST_SEASON TABELL:\n";
echo str_repeat("-", 50) . "\n";

try {
    $stmt = $pdo->prepare("SELECT COUNT(*) FROM rider_first_season WHERE cohort_year = ?");
    $stmt->execute([$year]);
    $count = $stmt->fetchColumn();
    echo "   Antal i tabellen för {$year}: {$count}\n";

    // Show sample
    if ($count > 0) {
        $stmt = $pdo->prepare("SELECT * FROM rider_first_season WHERE cohort_year = ? LIMIT 3");
        $stmt->execute([$year]);
        echo "   Sample:\n";
        while ($row = $stmt->fetch(PDO::FETCH_ASSOC)) {
            echo "   - Rider {$row['rider_id']}: {$row['total_starts']} starter, retained_y1={$row['retained_year_1']}\n";
        }
    }
} catch (Exception $e) {
    echo "   FEL: " . $e->getMessage() . "\n";
}

// 3. Try to run the calculation
echo "\n3. TESTAR BERÄKNING:\n";
echo str_repeat("-", 50) . "\n";

try {
    require_once __DIR__ . '/../../analytics/includes/AnalyticsEngine.php';

    $engine = new AnalyticsEngine($pdo);
    $engine->setForceRerun(true);

    echo "   Kör calculateFirstSeasonJourney({$year})...\n";

    $start = microtime(true);
    $result = $engine->calculateFirstSeasonJourney($year);
    $elapsed = round(microtime(true) - $start, 2);

    echo "   Resultat: {$result} rader på {$elapsed}s\n";

} catch (Exception $e) {
    echo "   FEL: " . $e->getMessage() . "\n";
    echo "   Stack: " . $e->getTraceAsString() . "\n";
} catch (Throwable $t) {
    echo "   FATAL: " . $t->getMessage() . "\n";
    echo "   Stack: " . $t->getTraceAsString() . "\n";
}

// 4. Check result after calculation
echo "\n4. RESULTAT EFTER BERÄKNING:\n";
echo str_repeat("-", 50) . "\n";

try {
    $stmt = $pdo->prepare("SELECT COUNT(*) FROM rider_first_season WHERE cohort_year = ?");
    $stmt->execute([$year]);
    $count = $stmt->fetchColumn();
    echo "   Antal i tabellen för {$year}: {$count}\n";
} catch (Exception $e) {
    echo "   FEL: " . $e->getMessage() . "\n";
}

// 5. Check v_canonical_riders view
echo "\n5. V_CANONICAL_RIDERS VIEW:\n";
echo str_repeat("-", 50) . "\n";

try {
    $count = $pdo->query("SELECT COUNT(*) FROM v_canonical_riders")->fetchColumn();
    echo "   Totalt i view: {$count}\n";

    // Check for riders in this year
    $stmt = $pdo->prepare("
        SELECT COUNT(DISTINCT v.canonical_rider_id)
        FROM v_canonical_riders v
        JOIN results r ON r.cyclist_id = v.original_rider_id
        JOIN events e ON e.id = r.event_id
        WHERE YEAR(e.date) = ?
    ");
    $stmt->execute([$year]);
    $yearCount = $stmt->fetchColumn();
    echo "   Riders med resultat {$year}: {$yearCount}\n";

} catch (Exception $e) {
    echo "   FEL: " . $e->getMessage() . "\n";
}

echo "\n=== SLUT ===\n";
