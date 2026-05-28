<?php
/**
 * Fix Series Points - Diagnostisera och fixa seriesammanställning
 */
require_once __DIR__ . '/../config.php';
require_once __DIR__ . '/../includes/series-points.php';
require_admin();

$db = getDB();
$pdo = $db->getPdo();

$message = '';
$messageType = 'info';

// Handle actions
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    checkCsrf();
    $action = $_POST['action'] ?? '';

    if ($action === 'assign_template') {
        // Assign template to all events in a series that don't have one
        $seriesId = (int)$_POST['series_id'];
        $templateId = (int)$_POST['template_id'];

        $updated = $pdo->prepare("
            UPDATE series_events
            SET template_id = ?
            WHERE series_id = ? AND (template_id IS NULL OR template_id = 0)
        ");
        $updated->execute([$templateId, $seriesId]);
        $count = $updated->rowCount();

        // Recalculate all series points
        $stats = recalculateAllSeriesPoints($db, $seriesId);

        $message = "Uppdaterade {$count} events med poängmall. Beräknade {$stats['inserted']} nya och uppdaterade {$stats['updated']} serieresultat.";
        $messageType = 'success';
    }
    elseif ($action === 'recalculate') {
        $seriesId = (int)$_POST['series_id'];
        $stats = recalculateAllSeriesPoints($db, $seriesId);
        $message = "Omberäknade serie #{$seriesId}: {$stats['inserted']} nya, {$stats['updated']} uppdaterade, {$stats['deleted']} raderade.";
        $messageType = 'success';
    }
    elseif ($action === 'recalculate_all') {
        // Recalculate ALL series
        $allSeries = $db->getAll("SELECT id, name FROM series");
        $totalStats = ['series' => 0, 'inserted' => 0, 'updated' => 0];

        foreach ($allSeries as $s) {
            $stats = recalculateAllSeriesPoints($db, $s['id']);
            $totalStats['series']++;
            $totalStats['inserted'] += $stats['inserted'];
            $totalStats['updated'] += $stats['updated'];
        }

        $message = "Omberäknade alla {$totalStats['series']} serier: {$totalStats['inserted']} nya, {$totalStats['updated']} uppdaterade.";
        $messageType = 'success';
    }
}

// Get all series with diagnostics
$series = $db->getAll("
    SELECT s.id, s.name, s.year,
           (SELECT COUNT(*) FROM series_events WHERE series_id = s.id) as total_events,
           (SELECT COUNT(*) FROM series_events WHERE series_id = s.id AND template_id IS NOT NULL AND template_id > 0) as events_with_template,
           (SELECT COUNT(*) FROM series_results WHERE series_id = s.id) as series_results_count,
           (SELECT COUNT(*) FROM series_results WHERE series_id = s.id AND points > 0) as results_with_points
    FROM series s
    ORDER BY s.year DESC, s.name
");

// Get available templates
$templates = $db->getAll("
    SELECT ps.id, ps.name, COUNT(psv.id) as value_count
    FROM point_scales ps
    LEFT JOIN point_scale_values psv ON ps.id = psv.scale_id
    WHERE ps.active = 1
    GROUP BY ps.id
    ORDER BY ps.name
");

$page_title = 'Fixa seriepoäng';
$breadcrumbs = [
    ['label' => 'Verktyg', 'url' => '/admin/tools'],
    ['label' => 'Fixa seriepoäng']
];
include __DIR__ . '/components/unified-layout.php';
?>

<h1 class="text-primary mb-lg">
    <i data-lucide="calculator"></i> Fixa seriesammanställning
</h1>

<?php if ($message): ?>
<div class="alert alert-<?= $messageType ?> mb-lg">
    <?= h($message) ?>
</div>
<?php endif; ?>

<div class="alert alert-info mb-lg">
    <i data-lucide="info"></i>
    <strong>Varför visas ingen sammanställning?</strong><br>
    1. Events måste vara kopplade till serien (series_events)<br>
    2. Varje event måste ha en poängmall (template_id)<br>
    3. Poängmallen måste ha poängvärden (point_scale_values)<br>
    4. Seriepoängen måste beräknas (series_results)
</div>

<!-- Quick Actions -->
<div class="card mb-lg">
    <div class="card-header">
        <h3><i data-lucide="zap"></i> Snabbåtgärder</h3>
    </div>
    <div class="card-body">
        <form method="POST" class="inline">
            <?= csrf_field() ?>
            <input type="hidden" name="action" value="recalculate_all">
            <button type="submit" class="btn btn-primary"
                    onclick="return confirm('Beräkna om ALLA serier? Detta kan ta ett tag.')">
                <i data-lucide="refresh-cw"></i>
                Beräkna om ALLA serier
            </button>
        </form>
    </div>
</div>

<!-- Available Templates -->
<div class="card mb-lg">
    <div class="card-header">
        <h3><i data-lucide="file-text"></i> Tillgängliga poängmallar</h3>
    </div>
    <div class="card-body gs-padding-0">
        <?php if (empty($templates)): ?>
        <div class="alert alert-error m-md">
            <i data-lucide="alert-triangle"></i>
            <strong>Inga aktiva poängmallar!</strong>
            <a href="/admin/point-scales" class="btn btn-sm btn-primary ml-md">Skapa poängmall</a>
        </div>
        <?php else: ?>
        <table class="table table-sm">
            <thead>
                <tr>
                    <th>ID</th>
                    <th>Namn</th>
                    <th>Antal poängvärden</th>
                    <th>Status</th>
                </tr>
            </thead>
            <tbody>
                <?php foreach ($templates as $t): ?>
                <tr>
                    <td><?= $t['id'] ?></td>
                    <td><strong><?= h($t['name']) ?></strong></td>
                    <td><?= $t['value_count'] ?></td>
                    <td>
                        <?php if ($t['value_count'] > 0): ?>
                        <span class="badge badge-success">OK</span>
                        <?php else: ?>
                        <span class="badge badge-danger">TOM!</span>
                        <?php endif; ?>
                    </td>
                </tr>
                <?php endforeach; ?>
            </tbody>
        </table>
        <?php endif; ?>
    </div>
</div>

<!-- Series Diagnostics -->
<div class="card">
    <div class="card-header">
        <h3><i data-lucide="list"></i> Serier - Diagnostik</h3>
    </div>
    <div class="card-body gs-padding-0">
        <div class="table-responsive">
            <table class="table">
                <thead>
                    <tr>
                        <th>Serie</th>
                        <th>År</th>
                        <th>Events</th>
                        <th>Med mall</th>
                        <th>Utan mall</th>
                        <th>Series Results</th>
                        <th>Med poäng</th>
                        <th>Status</th>
                        <th>Åtgärd</th>
                    </tr>
                </thead>
                <tbody>
                    <?php foreach ($series as $s):
                        $eventsWithoutTemplate = $s['total_events'] - $s['events_with_template'];
                        $hasIssue = ($eventsWithoutTemplate > 0 && $s['total_events'] > 0) || ($s['total_events'] > 0 && $s['series_results_count'] == 0);
                    ?>
                    <tr class="<?= $hasIssue ? 'table-row-warning' : '' ?>">
                        <td>
                            <a href="/admin/series-events?series_id=<?= $s['id'] ?>">
                                <strong><?= h($s['name']) ?></strong>
                            </a>
                        </td>
                        <td><?= $s['year'] ?></td>
                        <td><?= $s['total_events'] ?></td>
                        <td class="<?= $s['events_with_template'] > 0 ? 'text-success' : '' ?>">
                            <?= $s['events_with_template'] ?>
                        </td>
                        <td class="<?= $eventsWithoutTemplate > 0 ? 'text-danger' : '' ?>">
                            <strong><?= $eventsWithoutTemplate ?></strong>
                        </td>
                        <td><?= $s['series_results_count'] ?></td>
                        <td class="<?= $s['results_with_points'] > 0 ? 'text-success' : 'text-warning' ?>">
                            <?= $s['results_with_points'] ?>
                        </td>
                        <td>
                            <?php if ($s['total_events'] == 0): ?>
                            <span class="badge badge-secondary">Inga events</span>
                            <?php elseif ($eventsWithoutTemplate > 0): ?>
                            <span class="badge badge-danger">Saknar mall</span>
                            <?php elseif ($s['series_results_count'] == 0): ?>
                            <span class="badge badge-warning">Ej beräknad</span>
                            <?php elseif ($s['results_with_points'] == 0): ?>
                            <span class="badge badge-warning">0 poäng</span>
                            <?php else: ?>
                            <span class="badge badge-success">OK</span>
                            <?php endif; ?>
                        </td>
                        <td>
                            <?php if ($s['total_events'] > 0): ?>
                            <div class="flex gap-sm">
                                <?php if ($eventsWithoutTemplate > 0 && !empty($templates)): ?>
                                <form method="POST" class="inline flex gap-xs">
                                    <?= csrf_field() ?>
                                    <input type="hidden" name="action" value="assign_template">
                                    <input type="hidden" name="series_id" value="<?= $s['id'] ?>">
                                    <select name="template_id" class="form-select form-select-sm" style="width: 120px;">
                                        <?php foreach ($templates as $t): ?>
                                        <option value="<?= $t['id'] ?>"><?= h($t['name']) ?></option>
                                        <?php endforeach; ?>
                                    </select>
                                    <button type="submit" class="btn btn-sm btn-primary" title="Tilldela mall till events utan">
                                        <i data-lucide="check"></i>
                                    </button>
                                </form>
                                <?php else: ?>
                                <form method="POST" class="inline">
                                    <?= csrf_field() ?>
                                    <input type="hidden" name="action" value="recalculate">
                                    <input type="hidden" name="series_id" value="<?= $s['id'] ?>">
                                    <button type="submit" class="btn btn-sm btn-secondary">
                                        <i data-lucide="refresh-cw"></i>
                                        Beräkna om
                                    </button>
                                </form>
                                <?php endif; ?>
                            </div>
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
