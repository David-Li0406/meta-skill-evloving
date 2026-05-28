<?php
/**
 * Backfill Historical Ranking Snapshots
 *
 * Generates ranking snapshots from 2016 onwards.
 * For each event date, calculates ranking based on 24 months prior to that date.
 * This provides complete ranking history.
 */
require_once __DIR__ . '/../config.php';
require_once __DIR__ . '/../includes/ranking_functions.php';
require_admin();

if (!hasRole('super_admin')) {
    header('Location: /admin?error=access_denied');
    exit;
}

$db = getDB();
$message = '';
$messageType = 'info';
$stats = [];
$progress = null;

// Handle backfill request
if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['start_backfill'])) {
    checkCsrf();

    $startYear = (int)($_POST['start_year'] ?? 2016);
    $endYear = (int)($_POST['end_year'] ?? date('Y'));
    $includeClubs = isset($_POST['include_clubs']);

    try {
        set_time_limit(600); // 10 minutes

        // Get all unique event dates from startYear onwards
        $eventDates = $db->getAll("
            SELECT DISTINCT DATE(e.date) as event_date
            FROM events e
            JOIN results r ON r.event_id = e.id
            WHERE YEAR(e.date) >= ?
              AND YEAR(e.date) <= ?
              AND e.discipline IN ('ENDURO', 'DH')
              AND r.status = 'finished'
            ORDER BY e.date ASC
        ", [$startYear, $endYear]);

        $totalDates = count($eventDates);
        $riderSnapshots = 0;
        $clubSnapshots = 0;
        $processed = 0;

        foreach ($eventDates as $row) {
            $eventDate = $row['event_date'];

            // Calculate rider ranking as of this date
            $riderData = calculateRankingDataAsOf($db, 'GRAVITY', $eventDate);

            // Delete existing snapshots for this date (if re-running)
            $db->query("DELETE FROM ranking_snapshots WHERE discipline = 'GRAVITY' AND snapshot_date = ?", [$eventDate]);

            // Get previous snapshot for position changes
            $previousSnapshot = $db->getAll("
                SELECT rider_id, ranking_position FROM ranking_snapshots
                WHERE discipline = 'GRAVITY' AND snapshot_date = (
                    SELECT MAX(snapshot_date) FROM ranking_snapshots
                    WHERE discipline = 'GRAVITY' AND snapshot_date < ?
                )
            ", [$eventDate]);

            $previousPositions = [];
            foreach ($previousSnapshot as $prev) {
                $previousPositions[$prev['rider_id']] = $prev['ranking_position'];
            }

            // Insert rider snapshots
            foreach ($riderData as $rider) {
                $prevPos = $previousPositions[$rider['rider_id']] ?? null;
                $posChange = $prevPos !== null ? ($prevPos - $rider['ranking_position']) : null;

                $db->query("INSERT INTO ranking_snapshots
                    (rider_id, discipline, snapshot_date, total_ranking_points,
                     points_last_12_months, points_months_13_24, events_count,
                     ranking_position, previous_position, position_change)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", [
                    $rider['rider_id'],
                    'GRAVITY',
                    $eventDate,
                    $rider['total_ranking_points'],
                    $rider['points_12'],
                    $rider['points_13_24'],
                    $rider['events_count'],
                    $rider['ranking_position'],
                    $prevPos,
                    $posChange
                ]);
                $riderSnapshots++;
            }

            // Calculate club ranking if requested
            if ($includeClubs) {
                $clubData = calculateClubRankingDataAsOf($db, 'GRAVITY', $eventDate);

                $db->query("DELETE FROM club_ranking_snapshots WHERE discipline = 'GRAVITY' AND snapshot_date = ?", [$eventDate]);

                // Get previous club snapshot
                $previousClubSnapshot = $db->getAll("
                    SELECT club_id, ranking_position FROM club_ranking_snapshots
                    WHERE discipline = 'GRAVITY' AND snapshot_date = (
                        SELECT MAX(snapshot_date) FROM club_ranking_snapshots
                        WHERE discipline = 'GRAVITY' AND snapshot_date < ?
                    )
                ", [$eventDate]);

                $previousClubPositions = [];
                foreach ($previousClubSnapshot as $prev) {
                    $previousClubPositions[$prev['club_id']] = $prev['ranking_position'];
                }

                foreach ($clubData as $club) {
                    $prevPos = $previousClubPositions[$club['club_id']] ?? null;
                    $posChange = $prevPos !== null ? ($prevPos - $club['ranking_position']) : null;

                    $db->query("INSERT INTO club_ranking_snapshots
                        (club_id, discipline, snapshot_date, total_ranking_points,
                         points_last_12_months, points_months_13_24, riders_count, events_count,
                         ranking_position, previous_position, position_change)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", [
                        $club['club_id'],
                        'GRAVITY',
                        $eventDate,
                        $club['total_ranking_points'],
                        $club['points_12'],
                        $club['points_13_24'],
                        $club['riders_count'],
                        $club['events_count'],
                        $club['ranking_position'],
                        $prevPos,
                        $posChange
                    ]);
                    $clubSnapshots++;
                }
            }

            $processed++;
        }

        $stats = [
            'dates_processed' => $processed,
            'total_dates' => $totalDates,
            'rider_snapshots' => $riderSnapshots,
            'club_snapshots' => $clubSnapshots,
            'start_year' => $startYear,
            'end_year' => $endYear
        ];

        $message = "Historisk ranking genererad! {$processed} datum bearbetade, {$riderSnapshots} ryttare-snapshots, {$clubSnapshots} klubb-snapshots.";
        $messageType = 'success';

    } catch (Exception $e) {
        $message = 'Fel: ' . $e->getMessage();
        $messageType = 'error';
    }
}

// Get current snapshot stats
$snapshotStats = $db->getRow("
    SELECT
        MIN(snapshot_date) as first_date,
        MAX(snapshot_date) as last_date,
        COUNT(DISTINCT snapshot_date) as unique_dates,
        COUNT(*) as total_snapshots
    FROM ranking_snapshots
    WHERE discipline = 'GRAVITY'
");

$clubSnapshotStats = $db->getRow("
    SELECT COUNT(*) as total FROM club_ranking_snapshots WHERE discipline = 'GRAVITY'
");

// Get available year range from events
$yearRange = $db->getRow("
    SELECT MIN(YEAR(date)) as min_year, MAX(YEAR(date)) as max_year
    FROM events
    WHERE discipline IN ('ENDURO', 'DH')
");

$page_title = 'Historisk Ranking Backfill';
$breadcrumbs = [
    ['label' => 'Ranking', 'url' => '/admin/ranking.php'],
    ['label' => 'Historisk Backfill']
];
include __DIR__ . '/components/unified-layout.php';
?>

<?php if ($message): ?>
<div class="alert alert-<?= $messageType === 'success' ? 'success' : 'danger' ?> mb-lg">
    <i data-lucide="<?= $messageType === 'success' ? 'check-circle' : 'alert-circle' ?>"></i>
    <?= h($message) ?>
</div>
<?php endif; ?>

<div class="card">
    <div class="card-header">
        <h2 class="text-primary">
            <i data-lucide="history"></i>
            Generera Historisk Ranking
        </h2>
    </div>
    <div class="card-body">
        <p class="mb-lg">
            Detta verktyg genererar ranking-snapshots för varje event-datum i vald period.
            <strong>För varje datum beräknas ranking baserat på de 24 föregående månadernas resultat</strong>,
            precis som den rullande rankingen fungerar.
        </p>

        <div class="alert alert-info mb-lg">
            <i data-lucide="info"></i>
            <div>
                <strong>Hur det fungerar:</strong>
                <ul class="mt-sm mb-0">
                    <li>Event 2018-06-15: Ranking beräknas på resultat 2016-06-15 till 2018-06-15</li>
                    <li>Event 2020-03-01: Ranking beräknas på resultat 2018-03-01 till 2020-03-01</li>
                    <li>Poäng viktade: 0-12 mån = 100%, 13-24 mån = 50%</li>
                </ul>
            </div>
        </div>

        <h3 class="mb-md">Nuvarande snapshots</h3>
        <div class="admin-stats-grid mb-lg">
            <div class="admin-stat-card">
                <div class="admin-stat-content">
                    <div class="admin-stat-value"><?= number_format($snapshotStats['unique_dates'] ?? 0) ?></div>
                    <div class="admin-stat-label">Unika datum</div>
                </div>
            </div>
            <div class="admin-stat-card">
                <div class="admin-stat-content">
                    <div class="admin-stat-value"><?= number_format($snapshotStats['total_snapshots'] ?? 0) ?></div>
                    <div class="admin-stat-label">Ryttare-snapshots</div>
                </div>
            </div>
            <div class="admin-stat-card">
                <div class="admin-stat-content">
                    <div class="admin-stat-value"><?= number_format($clubSnapshotStats['total'] ?? 0) ?></div>
                    <div class="admin-stat-label">Klubb-snapshots</div>
                </div>
            </div>
            <div class="admin-stat-card">
                <div class="admin-stat-content">
                    <div class="admin-stat-value"><?= $snapshotStats['first_date'] ?? '-' ?></div>
                    <div class="admin-stat-label">Första datum</div>
                </div>
            </div>
        </div>

        <form method="POST">
            <?= csrf_field() ?>

            <div class="grid grid-cols-2 gap-md mb-lg" style="max-width: 400px;">
                <div class="form-group">
                    <label class="label">Från år</label>
                    <select name="start_year" class="input">
                        <?php for ($y = ($yearRange['min_year'] ?? 2016); $y <= date('Y'); $y++): ?>
                            <option value="<?= $y ?>" <?= $y == 2016 ? 'selected' : '' ?>><?= $y ?></option>
                        <?php endfor; ?>
                    </select>
                </div>
                <div class="form-group">
                    <label class="label">Till år</label>
                    <select name="end_year" class="input">
                        <?php for ($y = ($yearRange['min_year'] ?? 2016); $y <= date('Y'); $y++): ?>
                            <option value="<?= $y ?>" <?= $y == date('Y') ? 'selected' : '' ?>><?= $y ?></option>
                        <?php endfor; ?>
                    </select>
                </div>
            </div>

            <div class="form-group mb-lg">
                <label class="flex items-center gap-sm">
                    <input type="checkbox" name="include_clubs" value="1" checked>
                    <span>Inkludera klubb-ranking</span>
                </label>
            </div>

            <div class="alert alert-warning mb-lg">
                <i data-lucide="alert-triangle"></i>
                <strong>OBS:</strong> Detta kan ta flera minuter beroende på datamängd.
                Befintliga snapshots för valda datum kommer att ersättas.
            </div>

            <button type="submit" name="start_backfill" class="btn btn--primary btn-lg">
                <i data-lucide="play"></i>
                Starta Historisk Backfill
            </button>
        </form>
    </div>
</div>

<?php if (!empty($stats)): ?>
<div class="card mt-lg">
    <div class="card-header">
        <h3>
            <i data-lucide="check-circle"></i>
            Resultat
        </h3>
    </div>
    <div class="card-body">
        <table class="table">
            <tr>
                <td>Period</td>
                <td><strong><?= $stats['start_year'] ?> - <?= $stats['end_year'] ?></strong></td>
            </tr>
            <tr>
                <td>Event-datum bearbetade</td>
                <td><strong><?= number_format($stats['dates_processed']) ?></strong></td>
            </tr>
            <tr>
                <td>Ryttare-snapshots skapade</td>
                <td><strong class="text-success"><?= number_format($stats['rider_snapshots']) ?></strong></td>
            </tr>
            <tr>
                <td>Klubb-snapshots skapade</td>
                <td><strong class="text-success"><?= number_format($stats['club_snapshots']) ?></strong></td>
            </tr>
        </table>
    </div>
</div>
<?php endif; ?>

<?php include __DIR__ . '/components/unified-layout-footer.php'; ?>
