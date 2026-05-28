<?php
/**
 * Clear Event Results - Rensa resultat per event eller serie
 */
require_once __DIR__ . '/../config.php';
require_admin();

$db = getDB();
$pdo = $db->getPdo();

$message = '';
$messageType = 'info';

// Hämta alla serier
$allSeries = $db->getAll("SELECT id, name, year FROM series ORDER BY year DESC, name");

// Välj serie eller event
$selectedSeriesId = isset($_GET['series_id']) ? (int)$_GET['series_id'] : null;
$selectedEventId = isset($_GET['event_id']) ? (int)$_GET['event_id'] : null;

// Hantera radering
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    checkCsrf();
    $action = $_POST['action'] ?? '';

    if ($action === 'delete_event_results') {
        $eventId = (int)$_POST['event_id'];
        try {
            $pdo->beginTransaction();

            // Radera series_results först
            $stmt = $pdo->prepare("DELETE FROM series_results WHERE event_id = ?");
            $stmt->execute([$eventId]);
            $seriesDeleted = $stmt->rowCount();

            // Radera results
            $stmt = $pdo->prepare("DELETE FROM results WHERE event_id = ?");
            $stmt->execute([$eventId]);
            $resultsDeleted = $stmt->rowCount();

            $pdo->commit();
            $message = "Raderade {$resultsDeleted} resultat och {$seriesDeleted} serieresultat";
            $messageType = 'success';
        } catch (Exception $e) {
            $pdo->rollBack();
            $message = "Fel: " . $e->getMessage();
            $messageType = 'error';
        }
    }

    if ($action === 'delete_series_results') {
        $seriesId = (int)$_POST['series_id'];
        try {
            $pdo->beginTransaction();

            $eventIds = $db->getAll("SELECT event_id FROM series_events WHERE series_id = ?", [$seriesId]);
            $totalResults = 0;
            $totalSeriesResults = 0;

            foreach ($eventIds as $e) {
                $stmt = $pdo->prepare("DELETE FROM series_results WHERE event_id = ? AND series_id = ?");
                $stmt->execute([$e['event_id'], $seriesId]);
                $totalSeriesResults += $stmt->rowCount();

                $stmt = $pdo->prepare("DELETE FROM results WHERE event_id = ?");
                $stmt->execute([$e['event_id']]);
                $totalResults += $stmt->rowCount();
            }

            $pdo->commit();
            $message = "Raderade {$totalResults} resultat och {$totalSeriesResults} serieresultat för hela serien";
            $messageType = 'success';
        } catch (Exception $e) {
            $pdo->rollBack();
            $message = "Fel: " . $e->getMessage();
            $messageType = 'error';
        }
    }

    if ($action === 'cleanup_orphans') {
        try {
            $stmt = $pdo->query("
                DELETE FROM riders
                WHERE id NOT IN (SELECT DISTINCT cyclist_id FROM results WHERE cyclist_id IS NOT NULL)
            ");
            $deleted = $stmt->rowCount();
            $message = "Raderade {$deleted} åkare utan resultat";
            $messageType = 'success';
        } catch (Exception $e) {
            $message = "Fel: " . $e->getMessage();
            $messageType = 'error';
        }
    }
}

// Hämta events
$events = [];
if ($selectedSeriesId) {
    $events = $db->getAll("
        SELECT e.id, e.name, e.date, e.location,
               (SELECT COUNT(*) FROM results WHERE event_id = e.id) as result_count,
               (SELECT COUNT(*) FROM series_results WHERE event_id = e.id AND series_id = ?) as series_result_count
        FROM events e
        JOIN series_events se ON e.id = se.event_id
        WHERE se.series_id = ?
        ORDER BY e.date
    ", [$selectedSeriesId, $selectedSeriesId]);
} else {
    $events = $db->getAll("
        SELECT e.id, e.name, e.date, e.location,
               (SELECT COUNT(*) FROM results WHERE event_id = e.id) as result_count,
               0 as series_result_count
        FROM events e
        ORDER BY e.date DESC
        LIMIT 50
    ");
}

// Räkna orphans
$orphanCount = $db->getRow("
    SELECT COUNT(*) as cnt FROM riders
    WHERE id NOT IN (SELECT DISTINCT cyclist_id FROM results WHERE cyclist_id IS NOT NULL)
")['cnt'] ?? 0;

// Page config
$page_title = 'Rensa resultat';
$breadcrumbs = [
    ['label' => 'Verktyg', 'url' => '/admin/tools'],
    ['label' => 'Rensa resultat']
];
include __DIR__ . '/components/unified-layout.php';
?>

<h1 class="text-primary mb-lg">
    <i data-lucide="trash-2"></i> Rensa resultat
</h1>

<?php if ($message): ?>
<div class="alert alert-<?= $messageType ?> mb-lg">
    <?= h($message) ?>
</div>
<?php endif; ?>

<div class="alert alert--warning mb-lg">
    <i data-lucide="alert-triangle"></i>
    <strong>Varning!</strong> Radering kan inte ångras. Gör en backup först.
</div>

<div class="grid grid-cols-1 md-grid-cols-2 gap-lg mb-lg">
    <!-- Serie-väljare -->
    <div class="card">
        <div class="card-header">
            <h3><i data-lucide="trophy"></i> Välj serie</h3>
        </div>
        <div class="card-body">
            <form method="GET">
                <div class="form-group mb-md">
                    <select name="series_id" class="form-select" onchange="this.form.submit()">
                        <option value="">-- Alla events (senaste 50) --</option>
                        <?php foreach ($allSeries as $s): ?>
                        <option value="<?= $s['id'] ?>" <?= $selectedSeriesId == $s['id'] ? 'selected' : '' ?>>
                            <?= h($s['name']) ?> (<?= $s['year'] ?>)
                        </option>
                        <?php endforeach; ?>
                    </select>
                </div>
            </form>

            <?php if ($selectedSeriesId): ?>
            <form method="POST" onsubmit="return confirm('VARNING! Radera ALLA resultat för hela serien?')">
                <?= csrf_field() ?>
                <input type="hidden" name="action" value="delete_series_results">
                <input type="hidden" name="series_id" value="<?= $selectedSeriesId ?>">
                <button type="submit" class="btn btn-danger w-full">
                    <i data-lucide="alert-triangle"></i>
                    Radera ALLA resultat i serien
                </button>
            </form>
            <?php endif; ?>
        </div>
    </div>

    <!-- Orphan cleanup -->
    <div class="card">
        <div class="card-header">
            <h3><i data-lucide="user-x"></i> Rensa åkare utan resultat</h3>
        </div>
        <div class="card-body">
            <div class="stat-card mb-md">
                <div class="stat-number"><?= number_format($orphanCount) ?></div>
                <div class="stat-label">Åkare utan resultat</div>
            </div>

            <?php if ($orphanCount > 0): ?>
            <form method="POST" onsubmit="return confirm('Radera <?= $orphanCount ?> åkare utan resultat?')">
                <?= csrf_field() ?>
                <input type="hidden" name="action" value="cleanup_orphans">
                <button type="submit" class="btn btn-warning w-full">
                    <i data-lucide="user-x"></i>
                    Rensa <?= number_format($orphanCount) ?> åkare
                </button>
            </form>
            <?php else: ?>
            <div class="alert alert-success">Inga åkare att rensa</div>
            <?php endif; ?>
        </div>
    </div>
</div>

<!-- Events-lista -->
<div class="card">
    <div class="card-header">
        <h3><i data-lucide="calendar"></i> Events (<?= count($events) ?>)</h3>
    </div>
    <div class="card-body gs-padding-0">
        <div class="table-responsive">
            <table class="table">
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Event</th>
                        <th>Datum</th>
                        <th>Resultat</th>
                        <th>Serieresultat</th>
                        <th>Åtgärd</th>
                    </tr>
                </thead>
                <tbody>
                    <?php foreach ($events as $event): ?>
                    <tr>
                        <td><?= $event['id'] ?></td>
                        <td><strong><?= h($event['name']) ?></strong></td>
                        <td><?= $event['date'] ?></td>
                        <td>
                            <span class="badge badge-<?= $event['result_count'] > 0 ? 'primary' : 'secondary' ?>">
                                <?= $event['result_count'] ?>
                            </span>
                        </td>
                        <td>
                            <span class="badge badge-<?= $event['series_result_count'] > 0 ? 'warning' : 'secondary' ?>">
                                <?= $event['series_result_count'] ?>
                            </span>
                        </td>
                        <td>
                            <?php if ($event['result_count'] > 0): ?>
                            <form method="POST" style="display:inline" onsubmit="return confirm('Radera <?= $event['result_count'] ?> resultat för <?= h($event['name']) ?>?')">
                                <?= csrf_field() ?>
                                <input type="hidden" name="action" value="delete_event_results">
                                <input type="hidden" name="event_id" value="<?= $event['id'] ?>">
                                <button type="submit" class="btn btn-danger btn-sm">
                                    <i data-lucide="trash-2"></i> Radera
                                </button>
                            </form>
                            <?php else: ?>
                            <span class="text-muted">Inga resultat</span>
                            <?php endif; ?>
                        </td>
                    </tr>
                    <?php endforeach; ?>
                </tbody>
            </table>
        </div>
    </div>
</div>

</div>
<?php include __DIR__ . '/components/unified-layout-footer.php'; ?>
