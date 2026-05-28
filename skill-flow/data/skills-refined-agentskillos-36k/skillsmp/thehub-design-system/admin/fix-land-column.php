<?php
/**
 * Fix LAND Column - Remove incorrectly imported LAND column from results
 *
 * This tool fixes the issue where "LAND" column was imported as a split time
 * instead of being mapped to rider nationality.
 */
require_once __DIR__ . '/../config.php';
require_admin();

$db = getDB();
$message = '';
$messageType = 'info';

// Find events with LAND in stage_names
$eventsWithLand = $db->getAll("
    SELECT id, name, date, stage_names
    FROM events
    WHERE stage_names LIKE '%LAND%' OR stage_names LIKE '%Land%' OR stage_names LIKE '%land%'
    ORDER BY date DESC
");

// Handle fix request
if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['fix_events'])) {
    checkCsrf();

    $eventIds = $_POST['event_ids'] ?? [];
    $fixedCount = 0;
    $errors = [];

    foreach ($eventIds as $eventId) {
        $eventId = (int)$eventId;

        // Get current stage_names
        $event = $db->getRow("SELECT id, stage_names FROM events WHERE id = ?", [$eventId]);
        if (!$event) continue;

        $stageNames = json_decode($event['stage_names'], true) ?: [];

        // Find which index has LAND
        $landIndex = null;
        foreach ($stageNames as $idx => $name) {
            if (stripos($name, 'land') !== false) {
                $landIndex = $idx;
                break;
            }
        }

        if ($landIndex !== null) {
            // Remove LAND from stage_names
            unset($stageNames[$landIndex]);

            // Re-index array to fix gaps
            $newStageNames = [];
            $newIdx = 1;
            foreach ($stageNames as $idx => $name) {
                if ($idx < $landIndex) {
                    $newStageNames[$idx] = $name;
                } else {
                    // Shift everything after LAND down by 1
                    $newStageNames[$idx - 1] = $name;
                }
            }

            // Clear the SS column that had LAND data
            $ssColumn = 'ss' . $landIndex;

            // Update event stage_names
            $db->update('events', [
                'stage_names' => json_encode(array_filter($newStageNames))
            ], 'id = ?', [$eventId]);

            // Clear the LAND data from results (it contains "SWE" etc.)
            $db->query("UPDATE results SET {$ssColumn} = NULL WHERE event_id = ?", [$eventId]);

            // Shift all SS columns after LAND down by one
            // This moves SS6 data to SS5, SS7 to SS6, etc.
            for ($i = $landIndex; $i <= 14; $i++) {
                $currentCol = 'ss' . $i;
                $nextCol = 'ss' . ($i + 1);
                $db->query("UPDATE results SET {$currentCol} = {$nextCol} WHERE event_id = ?", [$eventId]);
            }

            // Clear the last SS column (now duplicate)
            $db->query("UPDATE results SET ss15 = NULL WHERE event_id = ?", [$eventId]);

            $fixedCount++;
        }
    }

    if ($fixedCount > 0) {
        $message = "Fixade {$fixedCount} event. LAND-kolumnen har tagits bort och sträcktiderna har flyttats.";
        $messageType = 'success';

        // Refresh the list
        $eventsWithLand = $db->getAll("
            SELECT id, name, date, stage_names
            FROM events
            WHERE stage_names LIKE '%LAND%' OR stage_names LIKE '%Land%' OR stage_names LIKE '%land%'
            ORDER BY date DESC
        ");
    } else {
        $message = "Inga event att fixa.";
        $messageType = 'warning';
    }
}

$page_title = 'Fixa LAND-kolumn';
$breadcrumbs = [
    ['label' => 'Import', 'url' => '/admin/import'],
    ['label' => 'Fixa LAND-kolumn']
];

include __DIR__ . '/components/unified-layout.php';
?>

<?php if ($message): ?>
<div class="alert alert-<?= $messageType ?> mb-lg">
    <i data-lucide="<?= $messageType === 'success' ? 'check-circle' : ($messageType === 'error' ? 'alert-circle' : 'info') ?>"></i>
    <?= h($message) ?>
</div>
<?php endif; ?>

<div class="card">
    <div class="card-header">
        <h2 class="text-primary">
            <i data-lucide="wrench"></i>
            Fixa LAND-kolumn i resultat
        </h2>
    </div>
    <div class="card-body">
        <div class="alert alert--info mb-lg">
            <i data-lucide="info"></i>
            <div>
                <strong>Vad gör detta verktyg?</strong>
                <p class="mt-sm mb-0">
                    Om du importerade resultat med en "LAND"-kolumn så tolkades den felaktigt som en sträcktid.
                    Detta verktyg tar bort LAND-data från resultaten och flyttar de riktiga sträcktiderna till rätt plats.
                </p>
            </div>
        </div>

        <?php if (empty($eventsWithLand)): ?>
            <div class="alert alert--success">
                <i data-lucide="check-circle"></i>
                Inga event hittades med LAND i stage_names. Allt ser bra ut!
            </div>
        <?php else: ?>
            <form method="POST">
                <?= csrf_field() ?>

                <p class="mb-md">
                    <strong><?= count($eventsWithLand) ?> event</strong> hittades med LAND-kolumn:
                </p>

                <div class="table-responsive mb-lg">
                    <table class="table table--striped">
                        <thead>
                            <tr>
                                <th style="width: 40px;">
                                    <input type="checkbox" id="selectAll" onclick="toggleAll(this)">
                                </th>
                                <th>Event</th>
                                <th>Datum</th>
                                <th>Stage Names (JSON)</th>
                            </tr>
                        </thead>
                        <tbody>
                            <?php foreach ($eventsWithLand as $event): ?>
                            <tr>
                                <td>
                                    <input type="checkbox" name="event_ids[]" value="<?= $event['id'] ?>" class="event-checkbox" checked>
                                </td>
                                <td>
                                    <a href="/event/<?= $event['id'] ?>" target="_blank">
                                        <?= h($event['name']) ?>
                                    </a>
                                </td>
                                <td><?= date('Y-m-d', strtotime($event['date'])) ?></td>
                                <td>
                                    <code class="text-xs"><?= h($event['stage_names']) ?></code>
                                </td>
                            </tr>
                            <?php endforeach; ?>
                        </tbody>
                    </table>
                </div>

                <div class="alert alert--warning mb-lg">
                    <i data-lucide="alert-triangle"></i>
                    <div>
                        <strong>Varning!</strong>
                        <p class="mt-sm mb-0">
                            Detta kommer att:
                            <ul class="mt-sm mb-0">
                                <li>Ta bort LAND från stage_names</li>
                                <li>Nollställa SS-kolumnen som innehöll "SWE" etc.</li>
                                <li>Flytta alla efterföljande sträcktider ett steg åt vänster</li>
                            </ul>
                        </p>
                    </div>
                </div>

                <button type="submit" name="fix_events" class="btn btn--primary btn-lg">
                    <i data-lucide="check"></i>
                    Fixa valda event
                </button>
            </form>
        <?php endif; ?>
    </div>
</div>

<script>
function toggleAll(checkbox) {
    document.querySelectorAll('.event-checkbox').forEach(cb => {
        cb.checked = checkbox.checked;
    });
}
</script>

<?php include __DIR__ . '/components/unified-layout-footer.php'; ?>
