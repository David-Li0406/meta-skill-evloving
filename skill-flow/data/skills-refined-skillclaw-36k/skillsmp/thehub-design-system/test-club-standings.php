<?php
/**
 * FRISTÅENDE TEST-SIDA FÖR KLUBBMÄSTERSKAP
 * Ladda upp denna fil direkt via FTP till /thehub/
 * Öppna: https://thehub.gravityseries.se/test-club-standings.php
 */

error_reporting(E_ALL);
ini_set('display_errors', 1);

// Inkludera hub-config för databasanslutning
require_once __DIR__ . '/hub-config.php';

$db = hub_db();

// Hämta alla serier
$seriesStmt = $db->query("
    SELECT id, name, year
    FROM series
    WHERE active = 1
    ORDER BY year DESC, name ASC
");
$allSeries = $seriesStmt->fetchAll(PDO::FETCH_ASSOC);

// Välj serie (default: första)
$selectedSeriesId = isset($_GET['series_id']) ? (int)$_GET['series_id'] : ($allSeries[0]['id'] ?? 0);

// Hämta vald serie
$selectedSeries = null;
foreach ($allSeries as $s) {
    if ($s['id'] == $selectedSeriesId) {
        $selectedSeries = $s;
        break;
    }
}

// Hämta events för serien
$eventsStmt = $db->prepare("
    SELECT e.id, e.name, e.date
    FROM series_events se
    JOIN events e ON se.event_id = e.id
    WHERE se.series_id = ?
    ORDER BY e.date ASC
");
$eventsStmt->execute([$selectedSeriesId]);
$seriesEvents = $eventsStmt->fetchAll(PDO::FETCH_ASSOC);

// Om inga series_events, försök med events.series_id
if (empty($seriesEvents)) {
    $eventsStmt = $db->prepare("
        SELECT id, name, date
        FROM events
        WHERE series_id = ?
        ORDER BY date ASC
    ");
    $eventsStmt->execute([$selectedSeriesId]);
    $seriesEvents = $eventsStmt->fetchAll(PDO::FETCH_ASSOC);
}

// Kolla om series_results finns
$useSeriesResults = false;
try {
    $stmt = $db->prepare("SELECT COUNT(*) FROM series_results WHERE series_id = ?");
    $stmt->execute([$selectedSeriesId]);
    $useSeriesResults = ($stmt->fetchColumn() > 0);
} catch (Exception $e) {
    $useSeriesResults = false;
}

// Beräkna klubbställning
$clubStandings = [];
$clubRiderContributions = [];

foreach ($seriesEvents as $event) {
    $eventId = $event['id'];

    if ($useSeriesResults) {
        $stmt = $db->prepare("
            SELECT
                sr.cyclist_id,
                sr.class_id,
                sr.points,
                rd.firstname,
                rd.lastname,
                c.id as club_id,
                c.name as club_name,
                cls.name as class_name,
                cls.display_name as class_display_name
            FROM series_results sr
            JOIN riders rd ON sr.cyclist_id = rd.id
            LEFT JOIN clubs c ON rd.club_id = c.id
            LEFT JOIN classes cls ON sr.class_id = cls.id
            WHERE sr.series_id = ? AND sr.event_id = ?
            AND c.id IS NOT NULL
            AND sr.points > 0
            ORDER BY c.id, sr.class_id, sr.points DESC
        ");
        $stmt->execute([$selectedSeriesId, $eventId]);
    } else {
        $stmt = $db->prepare("
            SELECT
                r.cyclist_id,
                r.class_id,
                r.points,
                rd.firstname,
                rd.lastname,
                c.id as club_id,
                c.name as club_name,
                cls.name as class_name,
                cls.display_name as class_display_name
            FROM results r
            JOIN riders rd ON r.cyclist_id = rd.id
            LEFT JOIN clubs c ON rd.club_id = c.id
            LEFT JOIN classes cls ON r.class_id = cls.id
            WHERE r.event_id = ?
            AND r.status = 'finished'
            AND c.id IS NOT NULL
            AND r.points > 0
            ORDER BY c.id, r.class_id, r.points DESC
        ");
        $stmt->execute([$eventId]);
    }
    $eventResults = $stmt->fetchAll(PDO::FETCH_ASSOC);

    // Gruppera per klubb och klass
    $clubClassResults = [];
    foreach ($eventResults as $result) {
        $key = $result['club_id'] . '_' . $result['class_id'];
        if (!isset($clubClassResults[$key])) {
            $clubClassResults[$key] = [];
        }
        $clubClassResults[$key][] = $result;
    }

    // Applicera 100%/50% regel
    foreach ($clubClassResults as $riders) {
        $rank = 1;
        foreach ($riders as $rider) {
            $clubId = $rider['club_id'];
            $clubName = $rider['club_name'];
            $originalPoints = (float)$rider['points'];
            $clubPoints = 0;

            if ($rank === 1) {
                $clubPoints = $originalPoints;
            } elseif ($rank === 2) {
                $clubPoints = round($originalPoints * 0.5, 0);
            }

            if (!isset($clubStandings[$clubId])) {
                $clubStandings[$clubId] = [
                    'club_id' => $clubId,
                    'club_name' => $clubName,
                    'total_points' => 0,
                    'event_points' => [],
                    'rider_count' => 0
                ];
                foreach ($seriesEvents as $e) {
                    $clubStandings[$clubId]['event_points'][$e['id']] = 0;
                }
            }

            $clubStandings[$clubId]['event_points'][$eventId] += $clubPoints;
            $clubStandings[$clubId]['total_points'] += $clubPoints;

            // Spåra åkare
            $riderId = $rider['cyclist_id'];
            $riderKey = $clubId . '_' . $riderId;
            if (!isset($clubRiderContributions[$riderKey])) {
                $clubRiderContributions[$riderKey] = [
                    'rider_id' => $riderId,
                    'club_id' => $clubId,
                    'name' => $rider['firstname'] . ' ' . $rider['lastname'],
                    'class_name' => $rider['class_display_name'] ?? $rider['class_name'],
                    'total_club_points' => 0
                ];
            }
            $clubRiderContributions[$riderKey]['total_club_points'] += $clubPoints;

            $rank++;
        }
    }
}

// Lägg till åkare till klubbar
foreach ($clubRiderContributions as $riderData) {
    $clubId = $riderData['club_id'];
    if (isset($clubStandings[$clubId])) {
        $clubStandings[$clubId]['riders'][] = $riderData;
        $clubStandings[$clubId]['rider_count']++;
    }
}

// Sortera klubbar efter poäng
uasort($clubStandings, function($a, $b) {
    return $b['total_points'] - $a['total_points'];
});

// Sortera åkare inom varje klubb
foreach ($clubStandings as &$club) {
    if (isset($club['riders'])) {
        usort($club['riders'], function($a, $b) {
            return $b['total_club_points'] - $a['total_club_points'];
        });
    }
}
unset($club);

// Debug-info
$debugInfo = [
    'series_id' => $selectedSeriesId,
    'series_name' => $selectedSeries['name'] ?? 'N/A',
    'events_count' => count($seriesEvents),
    'use_series_results' => $useSeriesResults ? 'JA' : 'NEJ',
    'clubs_found' => count($clubStandings),
];

// Test-query för rådata
$rawDataStmt = $db->prepare("
    SELECT COUNT(*) as total_results,
           COUNT(DISTINCT rd.club_id) as unique_clubs,
           COUNT(DISTINCT r.cyclist_id) as unique_riders
    FROM results r
    JOIN riders rd ON r.cyclist_id = rd.id
    JOIN events e ON r.event_id = e.id
    WHERE e.series_id = ? AND r.points > 0 AND rd.club_id IS NOT NULL
");
$rawDataStmt->execute([$selectedSeriesId]);
$rawData = $rawDataStmt->fetch(PDO::FETCH_ASSOC);
?>
<!DOCTYPE html>
<html lang="sv">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Test Klubbmästerskap</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; padding: 20px; background: #f5f5f5; }
        h1, h2, h3 { margin-bottom: 15px; }
        .container { max-width: 1200px; margin: 0 auto; }
        .card { background: white; border-radius: 8px; padding: 20px; margin-bottom: 20px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        .debug { background: #fff3cd; border: 1px solid #ffc107; padding: 15px; border-radius: 8px; margin-bottom: 20px; }
        .debug h3 { color: #856404; }
        .debug pre { background: #f8f9fa; padding: 10px; border-radius: 4px; overflow-x: auto; }
        select { padding: 10px; font-size: 16px; border-radius: 4px; border: 1px solid #ddd; margin-bottom: 20px; }
        table { width: 100%; border-collapse: collapse; }
        th, td { padding: 10px; text-align: left; border-bottom: 1px solid #eee; }
        th { background: #f8f9fa; font-weight: 600; }
        tr:hover { background: #f8f9fa; }
        .place-1 { color: #ffd700; font-weight: bold; }
        .place-2 { color: #c0c0c0; font-weight: bold; }
        .place-3 { color: #cd7f32; font-weight: bold; }
        .total { font-weight: bold; background: #e8f5e9; }
        .riders-list { font-size: 12px; color: #666; margin-top: 5px; }
        .success { color: #28a745; }
        .warning { color: #ffc107; }
        .danger { color: #dc3545; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Test Klubbmästerskap</h1>
        <p style="margin-bottom: 20px; color: #666;">Fristående test-sida för att debugga klubbställningar</p>

        <div class="card">
            <h3>Välj serie:</h3>
            <form method="get">
                <select name="series_id" onchange="this.form.submit()">
                    <?php foreach ($allSeries as $s): ?>
                    <option value="<?= $s['id'] ?>" <?= $s['id'] == $selectedSeriesId ? 'selected' : '' ?>>
                        <?= htmlspecialchars($s['name']) ?> (<?= $s['year'] ?>)
                    </option>
                    <?php endforeach; ?>
                </select>
            </form>
        </div>

        <div class="debug">
            <h3>Debug-information:</h3>
            <pre><?= json_encode($debugInfo, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE) ?></pre>
            <h4 style="margin-top: 15px;">Rådata från databasen:</h4>
            <pre><?= json_encode($rawData, JSON_PRETTY_PRINT) ?></pre>
            <p style="margin-top: 10px;">
                <strong>Status:</strong>
                <?php if (count($clubStandings) > 0): ?>
                    <span class="success">✓ <?= count($clubStandings) ?> klubbar hittades!</span>
                <?php elseif ($rawData['unique_clubs'] > 0): ?>
                    <span class="warning">⚠ Data finns (<?= $rawData['unique_clubs'] ?> klubbar) men beräkningen returnerar tomt</span>
                <?php else: ?>
                    <span class="danger">✗ Ingen data hittades för denna serie</span>
                <?php endif; ?>
            </p>
        </div>

        <div class="card">
            <h2>Klubbmästerskap: <?= htmlspecialchars($selectedSeries['name'] ?? 'N/A') ?></h2>

            <?php if (empty($clubStandings)): ?>
                <p style="color: #666; padding: 20px; text-align: center;">Inga klubbresultat hittades.</p>
            <?php else: ?>
                <table>
                    <thead>
                        <tr>
                            <th>#</th>
                            <th>Klubb</th>
                            <th>Åkare</th>
                            <?php foreach ($seriesEvents as $event): ?>
                            <th title="<?= htmlspecialchars($event['name']) ?>"><?= date('j/n', strtotime($event['date'])) ?></th>
                            <?php endforeach; ?>
                            <th>Totalt</th>
                        </tr>
                    </thead>
                    <tbody>
                        <?php $pos = 0; foreach ($clubStandings as $club): $pos++; ?>
                        <tr>
                            <td class="<?= $pos <= 3 ? 'place-' . $pos : '' ?>"><?= $pos ?></td>
                            <td>
                                <strong><?= htmlspecialchars($club['club_name']) ?></strong>
                                <?php if (!empty($club['riders'])): ?>
                                <div class="riders-list">
                                    <?php foreach (array_slice($club['riders'], 0, 3) as $rider): ?>
                                        <?= htmlspecialchars($rider['name']) ?> (<?= $rider['total_club_points'] ?>p)
                                    <?php endforeach; ?>
                                    <?php if (count($club['riders']) > 3): ?>
                                        +<?= count($club['riders']) - 3 ?> fler
                                    <?php endif; ?>
                                </div>
                                <?php endif; ?>
                            </td>
                            <td><?= $club['rider_count'] ?></td>
                            <?php foreach ($seriesEvents as $event): ?>
                            <td><?= $club['event_points'][$event['id']] ?? 0 ?></td>
                            <?php endforeach; ?>
                            <td class="total"><?= $club['total_points'] ?></td>
                        </tr>
                        <?php endforeach; ?>
                    </tbody>
                </table>
            <?php endif; ?>
        </div>

        <div class="card">
            <h3>Events i serien (<?= count($seriesEvents) ?> st):</h3>
            <ul>
                <?php foreach ($seriesEvents as $event): ?>
                <li><?= htmlspecialchars($event['name']) ?> - <?= $event['date'] ?></li>
                <?php endforeach; ?>
            </ul>
        </div>
    </div>
</body>
</html>
