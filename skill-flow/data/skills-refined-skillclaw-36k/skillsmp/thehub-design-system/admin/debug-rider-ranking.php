<?php
/**
 * Debug script for checking rider ranking issues
 * Usage: /admin/debug-rider-ranking.php?id=20002
 */
require_once __DIR__ . '/../config.php';
require_once __DIR__ . '/../includes/ranking_functions.php';
require_admin();

$db = getDB();
$riderId = (int)($_GET['id'] ?? 0);

if (!$riderId) {
    die('Usage: ?id=RIDER_ID');
}

// Get rider info
$rider = $db->getRow("SELECT * FROM riders WHERE id = ?", [$riderId]);
if (!$rider) {
    die("Rider $riderId not found");
}

echo "<h1>Ranking Debug: " . h($rider['firstname'] . ' ' . $rider['lastname']) . " (ID: $riderId)</h1>";

// 1. Check ranking snapshots
echo "<h2>1. Ranking Snapshots</h2>";
$snapshots = $db->getAll("
    SELECT * FROM ranking_snapshots
    WHERE rider_id = ?
    ORDER BY snapshot_date DESC
    LIMIT 5
", [$riderId]);

if (empty($snapshots)) {
    echo "<p style='color:red'>NO RANKING SNAPSHOTS found for this rider!</p>";
} else {
    echo "<table border='1' cellpadding='5'>";
    echo "<tr><th>Date</th><th>Discipline</th><th>Position</th><th>Points</th></tr>";
    foreach ($snapshots as $s) {
        echo "<tr><td>{$s['snapshot_date']}</td><td>{$s['discipline']}</td><td>#{$s['ranking_position']}</td><td>" . number_format($s['total_ranking_points'], 1) . "</td></tr>";
    }
    echo "</table>";
}

// 2. Check latest snapshot date
echo "<h2>2. Latest Snapshot Dates</h2>";
$latestDates = $db->getAll("
    SELECT discipline, MAX(snapshot_date) as latest
    FROM ranking_snapshots
    GROUP BY discipline
");
if (empty($latestDates)) {
    echo "<p style='color:red'>NO SNAPSHOTS in ranking_snapshots table at all!</p>";
} else {
    foreach ($latestDates as $ld) {
        echo "<p>{$ld['discipline']}: {$ld['latest']}</p>";
    }
}

// 3. Check rider's GRAVITY results
echo "<h2>3. Rider's DH/ENDURO Results (Last 24 Months)</h2>";
$cutoff = date('Y-m-d', strtotime('-24 months'));
$results = $db->getAll("
    SELECT
        r.id,
        r.event_id,
        r.class_id,
        r.position,
        r.points,
        r.run_1_points,
        r.run_2_points,
        r.status,
        e.name as event_name,
        e.date,
        e.discipline,
        cl.name as class_name,
        cl.series_eligible,
        cl.awards_points
    FROM results r
    JOIN events e ON r.event_id = e.id
    JOIN classes cl ON r.class_id = cl.id
    WHERE r.cyclist_id = ?
    AND e.discipline IN ('ENDURO', 'DH')
    AND e.date >= ?
    ORDER BY e.date DESC
", [$riderId, $cutoff]);

if (empty($results)) {
    echo "<p style='color:red'>No DH/ENDURO results in the last 24 months</p>";
} else {
    echo "<p>Found " . count($results) . " results:</p>";
    echo "<table border='1' cellpadding='5'>";
    echo "<tr><th>Date</th><th>Event</th><th>Class</th><th>Pos</th><th>Points</th><th>Run1</th><th>Run2</th><th>Status</th><th>Eligible?</th><th>Awards?</th></tr>";

    $eligibleCount = 0;
    $pointsCount = 0;

    foreach ($results as $r) {
        $eligible = (($r['series_eligible'] ?? 1) == 1);
        $awards = (($r['awards_points'] ?? 1) == 1);
        $hasPoints = ($r['points'] > 0 || ($r['run_1_points'] ?? 0) > 0 || ($r['run_2_points'] ?? 0) > 0);
        $statusOk = ($r['status'] === 'finished');

        if ($eligible && $awards && $hasPoints && $statusOk) {
            $eligibleCount++;
        }
        if ($hasPoints) {
            $pointsCount++;
        }

        $style = '';
        if (!$eligible || !$awards) $style = 'background:#fef3c7;';
        if (!$hasPoints) $style = 'background:#fee2e2;';
        if (!$statusOk) $style = 'background:#fecaca;';

        echo "<tr style='$style'>";
        echo "<td>{$r['date']}</td>";
        echo "<td>" . h($r['event_name']) . "</td>";
        echo "<td>" . h($r['class_name']) . "</td>";
        echo "<td>{$r['position']}</td>";
        echo "<td>{$r['points']}</td>";
        echo "<td>" . ($r['run_1_points'] ?? '-') . "</td>";
        echo "<td>" . ($r['run_2_points'] ?? '-') . "</td>";
        echo "<td>{$r['status']}</td>";
        echo "<td>" . ($eligible ? 'YES' : 'NO') . "</td>";
        echo "<td>" . ($awards ? 'YES' : 'NO') . "</td>";
        echo "</tr>";
    }
    echo "</table>";

    echo "<p><strong>Results with points: $pointsCount</strong></p>";
    echo "<p><strong>Eligible for ranking: $eligibleCount</strong></p>";
}

// 4. Calculate what ranking SHOULD be
echo "<h2>4. Calculated Ranking (Live)</h2>";
if (function_exists('calculateSingleRiderRanking')) {
    $calcRanking = calculateSingleRiderRanking($db, $riderId, 'GRAVITY');
    if ($calcRanking) {
        echo "<p><strong>Position:</strong> #{$calcRanking['ranking_position']}</p>";
        echo "<p><strong>Points:</strong> " . number_format($calcRanking['total_ranking_points'], 1) . "</p>";
        echo "<p><strong>Events:</strong> {$calcRanking['events_count']}</p>";
    } else {
        echo "<p style='color:red'>Could not calculate ranking - rider may not have eligible results</p>";
    }
}

// 5. Check if ALL GRAVITY results are missing from ranking
echo "<h2>5. Total GRAVITY Ranking Check</h2>";
$totalInRanking = $db->getRow("
    SELECT COUNT(*) as cnt FROM ranking_snapshots
    WHERE discipline = 'GRAVITY'
    AND snapshot_date = (SELECT MAX(snapshot_date) FROM ranking_snapshots WHERE discipline = 'GRAVITY')
");
echo "<p>Total riders in GRAVITY ranking: " . ($totalInRanking['cnt'] ?? 0) . "</p>";

// 6. Recommendations
echo "<h2>6. Diagnosis</h2>";
$issues = [];

if (empty($snapshots)) {
    $issues[] = "Rider not in ranking_snapshots - need to run ranking calculation";
}

if (empty($results)) {
    $issues[] = "No DH/ENDURO results in last 24 months";
}

$resultsWithPoints = 0;
$eligibleResults = 0;
foreach ($results ?? [] as $r) {
    $hasPoints = ($r['points'] > 0 || ($r['run_1_points'] ?? 0) > 0 || ($r['run_2_points'] ?? 0) > 0);
    $eligible = (($r['series_eligible'] ?? 1) == 1) && (($r['awards_points'] ?? 1) == 1);
    $statusOk = ($r['status'] === 'finished');
    if ($hasPoints) $resultsWithPoints++;
    if ($hasPoints && $eligible && $statusOk) $eligibleResults++;
}

if ($resultsWithPoints == 0 && !empty($results)) {
    $issues[] = "Results exist but have NO POINTS assigned - need to recalculate event points";
}

if ($eligibleResults == 0 && $resultsWithPoints > 0) {
    $issues[] = "Results have points but classes are not series_eligible or awards_points - check class settings";
}

if (($totalInRanking['cnt'] ?? 0) == 0) {
    $issues[] = "GRAVITY ranking is empty - need to run full ranking calculation";
}

if (empty($issues)) {
    echo "<p style='color:green'>No obvious issues found. Try running ranking calculation from /admin/ranking</p>";
} else {
    echo "<ul>";
    foreach ($issues as $issue) {
        echo "<li style='color:red'><strong>$issue</strong></li>";
    }
    echo "</ul>";
}

echo "<h2>Actions</h2>";
echo "<p><a href='/admin/ranking'>Go to Admin Ranking</a> - Click 'Kör beräkning' to update rankings</p>";
?>
