<?php
/**
 * Yearly Import Review
 * Go through imports year by year, verify data, and lock club affiliations
 */
require_once __DIR__ . '/../../config.php';
require_admin();

$db = getDB();
$message = '';
$messageType = 'info';

// Get selected year (default to current year)
$selectedYear = isset($_GET['year']) ? (int)$_GET['year'] : (int)date('Y');

// Handle actions
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    checkCsrf();
    $action = $_POST['action'] ?? '';

    if ($action === 'lock_year') {
        $year = (int)$_POST['year'];

        // Lock all rider_club_seasons for this year
        $locked = $db->query("UPDATE rider_club_seasons SET locked = 1 WHERE season_year = ?", [$year]);

        $message = "Säsong $year låst - klubbtillhörigheter kan inte längre ändras";
        $messageType = 'success';
    }

    if ($action === 'rebuild_club_seasons') {
        $year = (int)$_POST['year'];

        // Rebuild rider_club_seasons from results for this year
        // First, get all unique rider+club combinations from results this year
        $db->query("
            INSERT INTO rider_club_seasons (rider_id, club_id, season_year, locked)
            SELECT DISTINCT
                r.cyclist_id,
                r.club_id,
                ?,
                0
            FROM results r
            JOIN events e ON r.event_id = e.id
            WHERE YEAR(e.date) = ?
            AND r.club_id IS NOT NULL
            ON DUPLICATE KEY UPDATE club_id = VALUES(club_id)
        ", [$year, $year]);

        $message = "Klubbtillhörigheter för $year ombyggda från resultat";
        $messageType = 'success';
    }

    if ($action === 'mark_event_reviewed') {
        $eventId = (int)$_POST['event_id'];
        // Add a note or flag - for now just reload
        $message = "Event markerat som granskat";
        $messageType = 'success';
    }
}

$pageTitle = "Import-granskning $selectedYear";
include __DIR__ . '/../components/unified-layout.php';

// Get available years
$years = $db->getAll("
    SELECT DISTINCT YEAR(date) as year, COUNT(*) as event_count
    FROM events
    GROUP BY YEAR(date)
    ORDER BY year DESC
");

// Get events for selected year with stats
$events = $db->getAll("
    SELECT
        e.id,
        e.name,
        e.date,
        e.location,
        e.discipline,
        COUNT(DISTINCT r.id) as result_count,
        COUNT(DISTINCT r.cyclist_id) as rider_count,
        COUNT(DISTINCT CASE WHEN r.club_id IS NOT NULL THEN r.id END) as results_with_club,
        COUNT(DISTINCT CASE WHEN c.name REGEXP '^[0-9]{1,2}:[0-9]{2}' THEN r.id END) as bad_club_results,
        GROUP_CONCAT(DISTINCT s.name SEPARATOR ', ') as series_names
    FROM events e
    LEFT JOIN results r ON r.event_id = e.id
    LEFT JOIN clubs c ON r.club_id = c.id
    LEFT JOIN series_events se ON e.id = se.event_id
    LEFT JOIN series s ON se.series_id = s.id
    WHERE YEAR(e.date) = ?
    GROUP BY e.id
    ORDER BY e.date ASC
", [$selectedYear]);

// Get year stats
$yearStats = $db->getRow("
    SELECT
        COUNT(DISTINCT e.id) as total_events,
        COUNT(DISTINCT r.id) as total_results,
        COUNT(DISTINCT r.cyclist_id) as total_riders,
        COUNT(DISTINCT CASE WHEN rcs.locked = 1 THEN rcs.id END) as locked_affiliations,
        COUNT(DISTINCT rcs.id) as total_affiliations
    FROM events e
    LEFT JOIN results r ON r.event_id = e.id
    LEFT JOIN rider_club_seasons rcs ON rcs.rider_id = r.cyclist_id AND rcs.season_year = ?
    WHERE YEAR(e.date) = ?
", [$selectedYear, $selectedYear]);

// Get clubs with time-like names for this year
$badClubs = $db->getAll("
    SELECT DISTINCT c.id, c.name, COUNT(DISTINCT r.id) as result_count
    FROM clubs c
    JOIN results r ON r.club_id = c.id
    JOIN events e ON r.event_id = e.id
    WHERE c.name REGEXP '^[0-9]{1,2}:[0-9]{2}'
    AND YEAR(e.date) = ?
    GROUP BY c.id
    ORDER BY result_count DESC
", [$selectedYear]);
?>

<?php if ($message): ?>
<div class="alert alert-<?= $messageType ?> mb-lg">
    <?= $message ?>
</div>
<?php endif; ?>

<!-- Year Selector -->
<div class="card mb-lg">
    <div class="card-body">
        <div class="flex items-center gap-lg flex-wrap">
            <div class="flex items-center gap-md">
                <label class="text-secondary">Välj säsong:</label>
                <div class="flex gap-sm">
                    <?php foreach ($years as $y): ?>
                    <a href="?year=<?= $y['year'] ?>"
                       class="btn <?= $y['year'] == $selectedYear ? 'btn--primary' : 'btn--secondary' ?> btn--sm">
                        <?= $y['year'] ?> (<?= $y['event_count'] ?>)
                    </a>
                    <?php endforeach; ?>
                </div>
            </div>
        </div>
    </div>
</div>

<!-- Year Stats -->
<div class="grid grid-cols-2 md-grid-cols-4 gap-md mb-lg">
    <div class="stat-card">
        <div class="stat-number"><?= $yearStats['total_events'] ?? 0 ?></div>
        <div class="stat-label">Event</div>
    </div>
    <div class="stat-card">
        <div class="stat-number"><?= $yearStats['total_results'] ?? 0 ?></div>
        <div class="stat-label">Resultat</div>
    </div>
    <div class="stat-card">
        <div class="stat-number"><?= $yearStats['total_riders'] ?? 0 ?></div>
        <div class="stat-label">Unika åkare</div>
    </div>
    <div class="stat-card">
        <div class="stat-number">
            <?= $yearStats['locked_affiliations'] ?? 0 ?>/<?= $yearStats['total_affiliations'] ?? 0 ?>
        </div>
        <div class="stat-label">Låsta klubbtillh.</div>
    </div>
</div>

<!-- Bad Clubs Warning -->
<?php if (!empty($badClubs)): ?>
<div class="alert alert-warning mb-lg">
    <i data-lucide="alert-triangle"></i>
    <strong><?= count($badClubs) ?> klubbar med tidsliknande namn</strong> hittades i <?= $selectedYear ?>:
    <?php foreach (array_slice($badClubs, 0, 5) as $bc): ?>
        <code class="ml-sm"><?= h($bc['name']) ?></code> (<?= $bc['result_count'] ?> resultat)
    <?php endforeach; ?>
    <?php if (count($badClubs) > 5): ?>
        <span class="ml-sm">... och <?= count($badClubs) - 5 ?> till</span>
    <?php endif; ?>
    <a href="/admin/tools/fix-club-times.php" class="btn btn--sm btn--warning ml-md">Fixa</a>
</div>
<?php endif; ?>

<!-- Events Table -->
<div class="card">
    <div class="card-header">
        <h2 class="text-primary">
            <i data-lucide="calendar"></i>
            Event <?= $selectedYear ?> (<?= count($events) ?>)
        </h2>
    </div>
    <div class="card-body gs-padding-0">
        <div class="table-responsive">
            <table class="table">
                <thead>
                    <tr>
                        <th>Datum</th>
                        <th>Event</th>
                        <th>Serie</th>
                        <th>Resultat</th>
                        <th>Klubb OK</th>
                        <th>Problem</th>
                        <th>Åtgärder</th>
                    </tr>
                </thead>
                <tbody>
                    <?php foreach ($events as $event): ?>
                    <?php
                    $hasProblems = $event['bad_club_results'] > 0;
                    $clubCoverage = $event['result_count'] > 0
                        ? round(($event['results_with_club'] / $event['result_count']) * 100)
                        : 0;
                    ?>
                    <tr class="<?= $hasProblems ? 'bg-warning-light' : '' ?>">
                        <td><?= date('m-d', strtotime($event['date'])) ?></td>
                        <td>
                            <a href="/event/<?= $event['id'] ?>?tab=resultat" target="_blank">
                                <?= h($event['name']) ?>
                            </a>
                            <?php if ($event['discipline']): ?>
                            <span class="badge badge-sm badge-secondary ml-sm"><?= h($event['discipline']) ?></span>
                            <?php endif; ?>
                        </td>
                        <td class="text-sm"><?= h($event['series_names'] ?? '-') ?></td>
                        <td>
                            <strong><?= $event['result_count'] ?></strong>
                            <span class="text-secondary text-sm">(<?= $event['rider_count'] ?> åkare)</span>
                        </td>
                        <td>
                            <?php if ($clubCoverage == 100): ?>
                            <span class="badge badge-success"><?= $clubCoverage ?>%</span>
                            <?php elseif ($clubCoverage >= 80): ?>
                            <span class="badge badge-warning"><?= $clubCoverage ?>%</span>
                            <?php else: ?>
                            <span class="badge badge-danger"><?= $clubCoverage ?>%</span>
                            <?php endif; ?>
                        </td>
                        <td>
                            <?php if ($event['bad_club_results'] > 0): ?>
                            <span class="badge badge-danger">
                                <i data-lucide="alert-circle" style="width:12px;height:12px;"></i>
                                <?= $event['bad_club_results'] ?> tidsklubbar
                            </span>
                            <?php else: ?>
                            <span class="text-success">-</span>
                            <?php endif; ?>
                        </td>
                        <td>
                            <div class="flex gap-sm">
                                <a href="/admin/edit-results.php?event_id=<?= $event['id'] ?>"
                                   class="btn btn--sm btn--ghost" title="Redigera resultat">
                                    <i data-lucide="pencil"></i>
                                </a>
                                <a href="/admin/import-results.php"
                                   class="btn btn--sm btn--ghost" title="Importera om">
                                    <i data-lucide="upload"></i>
                                </a>
                            </div>
                        </td>
                    </tr>
                    <?php endforeach; ?>
                </tbody>
            </table>
        </div>
    </div>
</div>

<!-- Year Actions -->
<div class="card mt-lg">
    <div class="card-header">
        <h3 class="text-primary">
            <i data-lucide="lock"></i>
            Säsongsåtgärder
        </h3>
    </div>
    <div class="card-body">
        <div class="flex gap-md flex-wrap">
            <form method="POST" style="display:inline;">
                <?= csrf_field() ?>
                <input type="hidden" name="action" value="rebuild_club_seasons">
                <input type="hidden" name="year" value="<?= $selectedYear ?>">
                <button type="submit" class="btn btn--secondary"
                        onclick="return confirm('Bygga om klubbtillhörigheter för <?= $selectedYear ?> från resultat?')">
                    <i data-lucide="refresh-cw"></i>
                    Bygg om klubbtillhörigheter
                </button>
            </form>

            <form method="POST" style="display:inline;">
                <?= csrf_field() ?>
                <input type="hidden" name="action" value="lock_year">
                <input type="hidden" name="year" value="<?= $selectedYear ?>">
                <button type="submit" class="btn btn--warning"
                        onclick="return confirm('Lås alla klubbtillhörigheter för <?= $selectedYear ?>? Detta kan inte ångras.')">
                    <i data-lucide="lock"></i>
                    Lås säsong <?= $selectedYear ?>
                </button>
            </form>
        </div>

        <p class="text-secondary text-sm mt-md">
            <strong>Bygg om:</strong> Skapar/uppdaterar rider_club_seasons från results.club_id<br>
            <strong>Lås:</strong> Markerar alla klubbtillhörigheter som låsta - kan inte ändras av nya importer
        </p>
    </div>
</div>

<?php include __DIR__ . '/../components/unified-layout-footer.php'; ?>
