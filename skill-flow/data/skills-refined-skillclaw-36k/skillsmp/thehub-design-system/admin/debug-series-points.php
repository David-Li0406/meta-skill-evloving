<?php
/**
 * Debug Series Points - Diagnose calculation issues
 */
require_once __DIR__ . '/../config.php';
require_once __DIR__ . '/../includes/series-points.php';
require_admin();

$db = getDB();
$seriesId = isset($_GET['series_id']) ? intval($_GET['series_id']) : 5;

// Handle recalculate action with detailed logging
$recalcLog = [];
if (isset($_GET['recalculate']) && $_GET['recalculate'] == '1') {
    // Custom recalculation with detailed logging
    $seriesEvents = $db->getAll("SELECT event_id, template_id FROM series_events WHERE series_id = ?", [$seriesId]);

    foreach ($seriesEvents as $se) {
        $eventId = $se['event_id'];
        $templateId = $se['template_id'];

        $eventInfo = $db->getRow("SELECT name, event_level FROM events WHERE id = ?", [$eventId]);
        $eventLog = [
            'event_id' => $eventId,
            'event_name' => $eventInfo['name'] ?? 'Unknown',
            'event_level' => $eventInfo['event_level'] ?? 'NULL',
            'template_id' => $templateId,
            'results_found' => 0,
            'points_calculated' => []
        ];

        // Get results for this event - join with series_results to compare
        $results = $db->getAll("
            SELECT r.id, r.cyclist_id, r.class_id, r.position, r.status, r.points as results_points,
                   ri.firstname, ri.lastname,
                   cl.name as class_name, cl.awards_points, cl.series_eligible,
                   sr.points as series_results_points
            FROM results r
            LEFT JOIN riders ri ON r.cyclist_id = ri.id
            LEFT JOIN classes cl ON r.class_id = cl.id
            LEFT JOIN series_results sr ON sr.cyclist_id = r.cyclist_id
                AND sr.event_id = r.event_id
                AND sr.series_id = ?
            WHERE r.event_id = ?
            ORDER BY r.position, r.points DESC
            LIMIT 30
        ", [$seriesId, $eventId]);

        $eventLog['results_found'] = count($results);

        foreach ($results as $r) {
            // Calculate what points would be using the new detailed function
            $pointsData = ['total' => 0, 'run_1' => 0, 'run_2' => 0];
            if ($templateId) {
                $pointsData = calculateSeriesPointsDetailed($db, $templateId, $r['position'], $r['status']);
            }

            $eventLog['points_calculated'][] = [
                'rider' => $r['firstname'] . ' ' . $r['lastname'],
                'position' => $r['position'],
                'class' => $r['class_name'],
                'awards_points' => $r['awards_points'],
                'series_eligible' => $r['series_eligible'],
                'calculated_points' => $pointsData['total'],
                'calc_run1' => $pointsData['run_1'],
                'calc_run2' => $pointsData['run_2'],
                'results_points' => $r['results_points'],
                'series_results_points' => $r['series_results_points'],
                'status' => $r['status']
            ];
        }

        $recalcLog[] = $eventLog;
    }
}

echo "<!DOCTYPE html><html><head><meta charset='UTF-8'><title>Debug Series Points</title>";
echo "<style>
body { font-family: monospace; padding: 20px; background: #1a1a1a; color: #e0e0e0; max-width: 1400px; margin: 0 auto; }
.success { color: #4caf50; }
.error { color: #f44336; }
.warning { color: #ff9800; }
.info { color: #2196f3; }
h1, h2, h3 { color: #fff; }
table { border-collapse: collapse; width: 100%; margin: 10px 0; background: #2a2a2a; }
th, td { border: 1px solid #444; padding: 8px; text-align: left; }
th { background: #333; }
tr:hover { background: #363636; }
.card { background: #2a2a2a; padding: 15px; margin: 15px 0; border-radius: 8px; border-left: 4px solid #2196f3; }
.btn { display: inline-block; padding: 10px 20px; background: #4caf50; color: white; text-decoration: none; border-radius: 4px; margin: 5px; }
.btn:hover { background: #45a049; }
.btn-warning { background: #ff9800; }
</style></head><body>";

echo "<h1>Debug Series Points - Serie #{$seriesId}</h1>";

// Navigation
echo "<div style='margin-bottom: 20px;'>";
echo "<a href='?series_id={$seriesId}' class='btn'>Uppdatera</a>";
echo "<a href='?series_id={$seriesId}&recalculate=1' class='btn btn-warning'>Test Beräkning (visa detaljer)</a>";
echo "<a href='/admin/series-events.php?series_id={$seriesId}' class='btn'>Hantera Events</a>";
echo "<a href='/series/{$seriesId}' class='btn'>Visa Serie</a>";
echo "</div>";

// 1. Check series exists
$series = $db->getRow("SELECT * FROM series WHERE id = ?", [$seriesId]);
if (!$series) {
    echo "<p class='error'>Serie {$seriesId} finns inte!</p></body></html>";
    exit;
}
echo "<p class='success'>Serie: <strong>{$series['name']}</strong> ({$series['year']})</p>";

// Show recalculation log if available
if (!empty($recalcLog)) {
    echo "<div class='card' style='border-color: #ff9800;'><h2>Testberäkning Resultat</h2>";
    foreach ($recalcLog as $eventLog) {
        echo "<h3>{$eventLog['event_name']} (Event #{$eventLog['event_id']})</h3>";
        $levelClass = $eventLog['event_level'] === 'sportmotion' ? 'warning' : 'success';
        echo "<p>Template ID: <strong>{$eventLog['template_id']}</strong> | ";
        echo "event_level: <span class='{$levelClass}'><strong>{$eventLog['event_level']}</strong></span> | ";
        echo "Resultat hittade: <strong>{$eventLog['results_found']}</strong></p>";

        if ($eventLog['event_level'] === 'sportmotion') {
            echo "<p class='warning'>⚠️ event_level = 'sportmotion' → 50% multiplikator appliceras!</p>";
        }

        if (empty($eventLog['points_calculated'])) {
            echo "<p class='warning'>Inga resultat att beräkna!</p>";
        } else {
            echo "<table><tr><th>Åkare</th><th>Pos</th><th>Klass</th><th>awards</th><th>elig</th><th>results.pts</th><th>series_res</th><th>Kval</th><th>Final</th><th>Total</th></tr>";
            foreach ($eventLog['points_calculated'] as $pc) {
                $calcClass = $pc['calculated_points'] > 0 ? 'success' : 'error';
                $apClass = $pc['awards_points'] == 1 ? 'success' : 'error';
                $seClass = $pc['series_eligible'] == 1 ? 'success' : 'error';
                $rpClass = $pc['results_points'] > 0 ? 'info' : '';
                $srpClass = $pc['series_results_points'] > 0 ? 'success' : 'warning';
                $r1Class = ($pc['calc_run1'] ?? 0) > 0 ? 'info' : '';
                $r2Class = ($pc['calc_run2'] ?? 0) > 0 ? 'info' : '';
                echo "<tr>
                    <td>{$pc['rider']}</td>
                    <td>{$pc['position']}</td>
                    <td>{$pc['class']}</td>
                    <td class='{$apClass}'>{$pc['awards_points']}</td>
                    <td class='{$seClass}'>{$pc['series_eligible']}</td>
                    <td class='{$rpClass}'>{$pc['results_points']}</td>
                    <td class='{$srpClass}'>" . ($pc['series_results_points'] ?? 'NULL') . "</td>
                    <td class='{$r1Class}'>" . ($pc['calc_run1'] ?? 0) . "</td>
                    <td class='{$r2Class}'>" . ($pc['calc_run2'] ?? 0) . "</td>
                    <td class='{$calcClass}'><strong>{$pc['calculated_points']}</strong></td>
                </tr>";
            }
            echo "</table>";
        }
    }
    echo "</div>";
}

// 2. Check series_events
echo "<div class='card'><h2>1. Series Events</h2>";
$seriesEvents = $db->getAll("
    SELECT se.*, e.name as event_name, e.date as event_date, ps.name as scale_name
    FROM series_events se
    JOIN events e ON se.event_id = e.id
    LEFT JOIN point_scales ps ON se.template_id = ps.id
    WHERE se.series_id = ?
    ORDER BY se.sort_order
", [$seriesId]);

echo "<table><tr><th>Event</th><th>Datum</th><th>template_id</th><th>Point Scale Name</th><th>Har values?</th></tr>";
foreach ($seriesEvents as $se) {
    $scaleStatus = $se['scale_name'] ? "<span class='success'>{$se['scale_name']}</span>" : "<span class='error'>EJ HITTAT!</span>";

    // Check if scale has values
    $valueCount = 0;
    if ($se['template_id']) {
        $vc = $db->getRow("SELECT COUNT(*) as cnt FROM point_scale_values WHERE scale_id = ?", [$se['template_id']]);
        $valueCount = $vc['cnt'] ?? 0;
    }
    $vcClass = $valueCount > 0 ? 'success' : 'error';

    echo "<tr><td>{$se['event_name']}</td><td>{$se['event_date']}</td><td>{$se['template_id']}</td><td>{$scaleStatus}</td><td class='{$vcClass}'>{$valueCount} värden</td></tr>";
}
echo "</table></div>";

// 3. Check point_scales and their values
echo "<div class='card'><h2>2. Tillgängliga Point Scales</h2>";
$scales = $db->getAll("SELECT * FROM point_scales ORDER BY name");
echo "<table><tr><th>ID</th><th>Namn</th><th>Active</th><th>Typ</th><th>Antal pos</th><th>Topp 5 poäng</th></tr>";
foreach ($scales as $scale) {
    $values = $db->getAll("SELECT position, points, run_1_points, run_2_points FROM point_scale_values WHERE scale_id = ? ORDER BY position LIMIT 5", [$scale['id']]);
    $valueCount = $db->getRow("SELECT COUNT(*) as cnt FROM point_scale_values WHERE scale_id = ?", [$scale['id']]);
    $countClass = $valueCount['cnt'] > 0 ? 'success' : 'error';
    $activeClass = $scale['active'] ? 'success' : 'warning';

    // Check if it's a DH scale (has run_1/run_2 values)
    $isDH = false;
    $top5 = [];
    foreach ($values as $v) {
        $run1 = (float)($v['run_1_points'] ?? 0);
        $run2 = (float)($v['run_2_points'] ?? 0);
        if ($run1 > 0 || $run2 > 0) {
            $isDH = true;
            $total = $run1 + $run2;
            $top5[] = "#{$v['position']}=K{$run1}+F{$run2}={$total}";
        } else {
            $top5[] = "#{$v['position']}={$v['points']}";
        }
    }

    $typeLabel = $isDH ? "<span class='info'>DH (Kval+Final)</span>" : "Standard";

    echo "<tr>
        <td>{$scale['id']}</td>
        <td>{$scale['name']}</td>
        <td class='{$activeClass}'>" . ($scale['active'] ? 'Ja' : 'Nej') . "</td>
        <td>{$typeLabel}</td>
        <td class='{$countClass}'>{$valueCount['cnt']}</td>
        <td>" . (empty($top5) ? "<span class='error'>TOM!</span>" : implode(', ', $top5)) . "</td>
    </tr>";
}
echo "</table></div>";

// 4. Check series_results
echo "<div class='card'><h2>3. Series Results</h2>";
$resultsCount = $db->getRow("SELECT COUNT(*) as cnt FROM series_results WHERE series_id = ?", [$seriesId]);
echo "<p>Antal poster i series_results: <strong>{$resultsCount['cnt']}</strong></p>";

if ($resultsCount['cnt'] > 0) {
    $sampleResults = $db->getAll("
        SELECT sr.*, r.firstname, r.lastname, e.name as event_name
        FROM series_results sr
        JOIN riders r ON sr.cyclist_id = r.id
        JOIN events e ON sr.event_id = e.id
        WHERE sr.series_id = ?
        ORDER BY sr.points DESC
        LIMIT 15
    ", [$seriesId]);
    echo "<table><tr><th>Åkare</th><th>Event</th><th>Position</th><th>Poäng</th><th>template_id</th></tr>";
    foreach ($sampleResults as $sr) {
        $pointsClass = $sr['points'] > 0 ? 'success' : 'warning';
        echo "<tr><td>{$sr['firstname']} {$sr['lastname']}</td><td>{$sr['event_name']}</td><td>{$sr['position']}</td><td class='{$pointsClass}'>{$sr['points']}</td><td>{$sr['template_id']}</td></tr>";
    }
    echo "</table>";
} else {
    echo "<p class='warning'>Inga series_results finns! Systemet faller tillbaka på results.points</p>";
}
echo "</div>";

// 5. Check results table for events
echo "<div class='card'><h2>4. Results per Event</h2>";
foreach ($seriesEvents as $se) {
    $resultCount = $db->getRow("SELECT COUNT(*) as cnt FROM results WHERE event_id = ?", [$se['event_id']]);
    $countClass = $resultCount['cnt'] > 0 ? 'success' : 'error';
    echo "<p>{$se['event_name']}: <span class='{$countClass}'>{$resultCount['cnt']} resultat</span></p>";
}
echo "</div>";

// Recommendation
echo "<div class='card' style='border-color: #ff9800;'><h2>Diagnostik</h2>";
echo "<p>Om poängen inte beräknas korrekt:</p>";
echo "<ol>";
echo "<li><strong>Kolla att mallarna har värden</strong> - 'Antal positioner' ska vara > 0 och 'Topp 5 poäng' ska visa värden</li>";
echo "<li><strong>Kolla template_id</strong> - Varje event måste ha en template_id som finns i point_scales</li>";
echo "<li><strong>Kolla klasser</strong> - awards_points och series_eligible måste vara 1 för att ge poäng</li>";
echo "<li><strong>Kolla resultat</strong> - Events måste ha resultat i results-tabellen</li>";
echo "</ol>";
echo "<p><a href='/admin/point-scales.php' class='btn'>Hantera Poängmallar</a></p>";
echo "</div>";

echo "</body></html>";

