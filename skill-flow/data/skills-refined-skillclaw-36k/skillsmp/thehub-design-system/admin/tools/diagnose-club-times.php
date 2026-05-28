<?php
/**
 * Diagnose Club Times Issue
 * Finds events where club names look like stage times (column offset problem)
 */
require_once __DIR__ . '/../../config.php';
require_admin();

$db = getDB();

$pageTitle = 'Diagnostik: Klubbar som ser ut som tider';
include __DIR__ . '/../components/unified-layout.php';

// Find events where club names look like times (e.g., "1:23.45" or "02:15.33")
$timePattern = "^[0-9]{1,2}:[0-9]{2}";

// Get riders with club names that look like times
$affectedRiders = $db->getAll("
    SELECT
        r.id as result_id,
        r.event_id,
        r.position,
        e.name as event_name,
        e.date as event_date,
        rd.id as rider_id,
        rd.firstname,
        rd.lastname,
        c.id as club_id,
        c.name as club_name,
        cl.display_name as class_name,
        r.finish_time
    FROM results r
    JOIN events e ON r.event_id = e.id
    JOIN riders rd ON r.cyclist_id = rd.id
    LEFT JOIN clubs c ON rd.club_id = c.id
    LEFT JOIN classes cl ON r.class_id = cl.id
    WHERE c.name REGEXP ?
    ORDER BY e.date DESC, e.name, cl.sort_order, r.position
    LIMIT 500
", [$timePattern]);

// Group by event
$eventGroups = [];
foreach ($affectedRiders as $row) {
    $eventKey = $row['event_id'];
    if (!isset($eventGroups[$eventKey])) {
        $eventGroups[$eventKey] = [
            'event_id' => $row['event_id'],
            'event_name' => $row['event_name'],
            'event_date' => $row['event_date'],
            'riders' => []
        ];
    }
    $eventGroups[$eventKey]['riders'][] = $row;
}

// Also find clubs with time-like names
$timeClubs = $db->getAll("
    SELECT
        c.id,
        c.name,
        COUNT(DISTINCT rd.id) as rider_count
    FROM clubs c
    LEFT JOIN riders rd ON rd.club_id = c.id
    WHERE c.name REGEXP ?
    GROUP BY c.id
    ORDER BY rider_count DESC
", [$timePattern]);
?>

<div class="card mb-lg">
    <div class="card-header">
        <h2 class="text-primary">
            <i data-lucide="search"></i>
            Klubbar som ser ut som tider
        </h2>
    </div>
    <div class="card-body">
        <p class="text-secondary mb-md">
            Detta verktyg hittar klubbar vars namn ser ut som tidvärden (t.ex. "1:23.45", "02:15.33").
            Detta indikerar vanligtvis ett kolumnförskjutningsproblem i importfilen.
        </p>

        <?php if (empty($timeClubs)): ?>
        <div class="alert alert-success">
            <i data-lucide="check-circle"></i>
            Inga klubbar med tidsliknande namn hittades!
        </div>
        <?php else: ?>
        <div class="alert alert-warning mb-lg">
            <i data-lucide="alert-triangle"></i>
            <strong><?= count($timeClubs) ?> klubbar</strong> med tidsliknande namn hittades.
        </div>

        <h3 class="mb-md">Klubbar med tidsliknande namn</h3>
        <div class="table-responsive mb-lg">
            <table class="table">
                <thead>
                    <tr>
                        <th>Klubb-ID</th>
                        <th>Namn</th>
                        <th>Antal åkare</th>
                        <th>Åtgärd</th>
                    </tr>
                </thead>
                <tbody>
                    <?php foreach ($timeClubs as $club): ?>
                    <tr>
                        <td><?= $club['id'] ?></td>
                        <td><code><?= h($club['name']) ?></code></td>
                        <td><?= $club['rider_count'] ?></td>
                        <td>
                            <a href="/admin/club-edit.php?id=<?= $club['id'] ?>" class="btn btn--sm btn--secondary">
                                <i data-lucide="pencil"></i>
                                Redigera
                            </a>
                        </td>
                    </tr>
                    <?php endforeach; ?>
                </tbody>
            </table>
        </div>
        <?php endif; ?>
    </div>
</div>

<?php if (!empty($eventGroups)): ?>
<div class="card">
    <div class="card-header">
        <h2 class="text-warning">
            <i data-lucide="calendar"></i>
            Påverkade event (<?= count($eventGroups) ?>)
        </h2>
    </div>
    <div class="card-body">
        <?php foreach ($eventGroups as $eventData): ?>
        <div class="mb-lg" style="border: 1px solid var(--color-border); border-radius: var(--radius-md); padding: var(--space-md);">
            <h4 class="mb-sm">
                <a href="/event/<?= $eventData['event_id'] ?>?tab=resultat" target="_blank">
                    <?= h($eventData['event_name']) ?>
                </a>
                <span class="text-secondary text-sm">(<?= date('Y-m-d', strtotime($eventData['event_date'])) ?>)</span>
            </h4>

            <div class="table-responsive">
                <table class="table table-sm">
                    <thead>
                        <tr>
                            <th>Plac</th>
                            <th>Namn</th>
                            <th>Klass</th>
                            <th>Klubb (fel)</th>
                            <th>Tid</th>
                            <th>Åtgärd</th>
                        </tr>
                    </thead>
                    <tbody>
                        <?php foreach (array_slice($eventData['riders'], 0, 20) as $rider): ?>
                        <tr>
                            <td><?= $rider['position'] ?></td>
                            <td>
                                <a href="/rider/<?= $rider['rider_id'] ?>">
                                    <?= h($rider['firstname'] . ' ' . $rider['lastname']) ?>
                                </a>
                            </td>
                            <td><?= h($rider['class_name'] ?? '-') ?></td>
                            <td><code class="text-warning"><?= h($rider['club_name']) ?></code></td>
                            <td><?= h($rider['finish_time'] ?? '-') ?></td>
                            <td>
                                <a href="/admin/rider-edit.php?id=<?= $rider['rider_id'] ?>" class="btn btn--sm btn--ghost">
                                    <i data-lucide="pencil"></i>
                                </a>
                            </td>
                        </tr>
                        <?php endforeach; ?>
                        <?php if (count($eventData['riders']) > 20): ?>
                        <tr>
                            <td colspan="6" class="text-center text-secondary">
                                ... och <?= count($eventData['riders']) - 20 ?> till
                            </td>
                        </tr>
                        <?php endif; ?>
                    </tbody>
                </table>
            </div>

            <div class="mt-md">
                <a href="/admin/edit-results.php?event_id=<?= $eventData['event_id'] ?>" class="btn btn--sm btn--secondary">
                    <i data-lucide="pencil"></i>
                    Redigera resultat
                </a>
                <a href="/admin/import-results.php" class="btn btn--sm btn--warning">
                    <i data-lucide="upload"></i>
                    Importera om
                </a>
            </div>
        </div>
        <?php endforeach; ?>
    </div>
</div>
<?php endif; ?>

<div class="card mt-lg">
    <div class="card-header">
        <h3 class="text-primary">
            <i data-lucide="info"></i>
            Så fixar du problemet
        </h3>
    </div>
    <div class="card-body">
        <ol style="margin-left: 20px;">
            <li class="mb-sm">
                <strong>Kontrollera importfilen:</strong> Se till att kolumnerna är i rätt ordning:
                <br><code>Category, PlaceByCategory, Bib, FirstName, LastName, Club, UCI-ID, NetTime, Status, SS1, SS2...</code>
            </li>
            <li class="mb-sm">
                <strong>Leta efter tomma kolumner:</strong> En tom kolumn kan förskjuta alla efterföljande värden.
            </li>
            <li class="mb-sm">
                <strong>Importera om:</strong> Korrigera CSV-filen och importera om eventet.
            </li>
            <li class="mb-sm">
                <strong>Rensa felaktiga klubbar:</strong> Ta bort klubbar med tidsliknande namn och uppdatera åkarnas klubbtillhörighet.
            </li>
        </ol>
    </div>
</div>

<?php include __DIR__ . '/../components/unified-layout-footer.php'; ?>
