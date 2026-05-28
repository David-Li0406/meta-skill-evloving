<?php
/**
 * Fix Time Format Tool
 * Removes leading "0:" from times that were imported incorrectly
 * e.g., "0:04:17.45" -> "4:17.45"
 */
require_once __DIR__ . '/../config.php';
require_admin();

$db = getDB();
$message = '';
$messageType = 'info';

// Get events with potentially bad times
$eventsWithBadTimes = $db->getAll("
    SELECT DISTINCT e.id, e.name, e.date, COUNT(*) as bad_count
    FROM results r
    JOIN events e ON r.event_id = e.id
    WHERE r.finish_time LIKE '0:%'
    GROUP BY e.id
    ORDER BY e.date DESC
");

// Handle fix request
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    checkCsrf();

    if (isset($_POST['fix_event'])) {
        $eventId = intval($_POST['fix_event']);

        $count = $db->getRow("SELECT COUNT(*) as cnt FROM results WHERE event_id = ? AND finish_time LIKE '0:%'", [$eventId]);
        $countBefore = $count['cnt'] ?? 0;

        if ($countBefore > 0) {
            $db->query("
                UPDATE results
                SET finish_time = SUBSTRING(finish_time, 3)
                WHERE event_id = ?
                AND finish_time LIKE '0:%'
            ", [$eventId]);

            $message = "Fixade {$countBefore} tider för event #{$eventId}";
            $messageType = 'success';

            // Refresh the list
            $eventsWithBadTimes = $db->getAll("
                SELECT DISTINCT e.id, e.name, e.date, COUNT(*) as bad_count
                FROM results r
                JOIN events e ON r.event_id = e.id
                WHERE r.finish_time LIKE '0:%'
                GROUP BY e.id
                ORDER BY e.date DESC
            ");
        } else {
            $message = "Inga tider att fixa för event #{$eventId}";
            $messageType = 'info';
        }
    }

    if (isset($_POST['fix_all'])) {
        $count = $db->getRow("SELECT COUNT(*) as cnt FROM results WHERE finish_time LIKE '0:%'");
        $totalBefore = $count['cnt'] ?? 0;

        $db->query("
            UPDATE results
            SET finish_time = SUBSTRING(finish_time, 3)
            WHERE finish_time LIKE '0:%'
        ");

        $message = "Fixade {$totalBefore} tider totalt";
        $messageType = 'success';

        $eventsWithBadTimes = [];
    }
}

// Page config for unified layout
$page_title = 'Fixa tidsformat';
$breadcrumbs = [
    ['label' => 'Verktyg', 'url' => '/admin/tools'],
    ['label' => 'Fixa tidsformat']
];
include __DIR__ . '/components/unified-layout.php';
?>

<h1 class="text-primary mb-lg">
    <i data-lucide="clock"></i>
    Fixa tidsformat
</h1>

<?php if ($message): ?>
<div class="alert alert-<?= $messageType ?> mb-lg">
    <i data-lucide="<?= $messageType === 'success' ? 'check-circle' : 'info' ?>"></i>
    <?= h($message) ?>
</div>
<?php endif; ?>

<!-- Info Card -->
<div class="card mb-lg">
    <div class="card-header">
        <h2 class="text-primary">
            <i data-lucide="info"></i>
            Om detta verktyg
        </h2>
    </div>
    <div class="card-body">
        <p class="mb-sm">Vissa importerade tider har felaktigt format:</p>
        <div class="grid grid-cols-2 gap-md mb-md" style="max-width: 300px;">
            <div>
                <span class="text-secondary">Fel:</span>
                <code class="text-danger">0:04:17.45</code>
            </div>
            <div>
                <span class="text-secondary">Rätt:</span>
                <code class="text-success">4:17.45</code>
            </div>
        </div>
        <p class="text-secondary">Detta verktyg tar bort den ledande <code>0:</code> från alla drabbade tider.</p>
    </div>
</div>

<?php if (empty($eventsWithBadTimes)): ?>
<div class="card">
    <div class="card-body text-center py-xl">
        <i data-lucide="check-circle" class="text-success" style="width: 48px; height: 48px;"></i>
        <h3 class="mt-md mb-sm">Allt ser bra ut!</h3>
        <p class="text-secondary">Inga event med felaktiga tidsformat hittades.</p>
    </div>
</div>
<?php else: ?>

<div class="card">
    <div class="card-header">
        <h2 class="text-primary">
            <i data-lucide="alert-triangle"></i>
            Event med felaktiga tider (<?= count($eventsWithBadTimes) ?>)
        </h2>
    </div>
    <div class="card-body gs-padding-0">
        <div class="table-responsive">
            <table class="table">
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Event</th>
                        <th>Datum</th>
                        <th>Felaktiga</th>
                        <th>Åtgärd</th>
                    </tr>
                </thead>
                <tbody>
                    <?php foreach ($eventsWithBadTimes as $event): ?>
                    <tr>
                        <td><?= $event['id'] ?></td>
                        <td><strong><?= h($event['name']) ?></strong></td>
                        <td><?= date('Y-m-d', strtotime($event['date'])) ?></td>
                        <td><span class="badge badge-warning"><?= $event['bad_count'] ?></span></td>
                        <td>
                            <form method="post" style="display: inline;">
                                <?= csrf_field() ?>
                                <input type="hidden" name="fix_event" value="<?= $event['id'] ?>">
                                <button type="submit" class="btn btn-sm btn-primary">
                                    <i data-lucide="wrench"></i>
                                    Fixa
                                </button>
                            </form>
                            <a href="/admin/edit-results.php?event_id=<?= $event['id'] ?>" class="btn btn-sm btn--secondary">
                                <i data-lucide="eye"></i>
                                Visa
                            </a>
                        </td>
                    </tr>
                    <?php endforeach; ?>
                </tbody>
            </table>
        </div>

        <div class="card-body border-top">
            <form method="post" onsubmit="return confirm('Fixa ALLA felaktiga tider?\n\nDetta kommer uppdatera alla drabbade resultat.');">
                <?= csrf_field() ?>
                <input type="hidden" name="fix_all" value="1">
                <button type="submit" class="btn btn-warning">
                    <i data-lucide="zap"></i>
                    Fixa alla <?= array_sum(array_column($eventsWithBadTimes, 'bad_count')) ?> tider
                </button>
            </form>
        </div>
    </div>
</div>
<?php endif; ?>

<div class="mt-lg">
    <a href="/admin/import-results.php" class="btn btn--secondary">
        <i data-lucide="arrow-left"></i>
        Tillbaka till resultat-import
    </a>
</div>

<?php include __DIR__ . '/components/unified-layout-footer.php'; ?>
