<?php
/**
 * Admin tool to add bonus points for stage performance (PS/SS)
 * Award extra points based on stage times
 * Supports: single event, multiple events, or entire series
 */
require_once __DIR__ . '/../config/database.php';
require_once __DIR__ . '/../includes/auth.php';
require_admin();

$db = getDB();
$message = '';
$messageType = 'info';

// Check for message from redirect
if (isset($_SESSION['stage_bonus_message'])) {
    $message = $_SESSION['stage_bonus_message'];
    $messageType = $_SESSION['stage_bonus_message_type'] ?? 'info';
    unset($_SESSION['stage_bonus_message'], $_SESSION['stage_bonus_message_type']);
}

// Default point scales
$defaultScales = [
    'top3' => ['name' => 'Topp 3', 'points' => [25, 20, 16]],
    'top5' => ['name' => 'Topp 5', 'points' => [25, 20, 16, 13, 11]],
    'top10' => ['name' => 'Topp 10', 'points' => [25, 20, 16, 13, 11, 10, 9, 8, 7, 6]],
    'top3_small' => ['name' => 'Topp 3 (liten)', 'points' => [10, 7, 5]],
    'top5_small' => ['name' => 'Topp 5 (liten)', 'points' => [10, 7, 5, 3, 2]],
];

// Check if series is preselected from URL
$preselectedSeriesId = isset($_GET['series']) ? (int)$_GET['series'] : null;
$defaultSelectionMode = $preselectedSeriesId ? 'series' : 'single';

// Get all series
$series = $db->getAll("
    SELECT s.id, s.name, s.year, COUNT(DISTINCT e.id) as event_count
    FROM series s
    LEFT JOIN events e ON e.series_id = s.id
    GROUP BY s.id
    HAVING event_count > 0
    ORDER BY s.year DESC, s.name
");

// Get all events with results and stage times
$events = $db->getAll("
    SELECT e.id, e.name, e.date, e.series_id, e.stage_names,
           s.name as series_name,
           COUNT(DISTINCT r.id) as result_count
    FROM events e
    LEFT JOIN series s ON e.series_id = s.id
    INNER JOIN results r ON e.id = r.event_id
    GROUP BY e.id
    HAVING result_count > 0
    ORDER BY e.date DESC
    LIMIT 200
");

// Get all classes (for multi-select)
$allClasses = $db->getAll("
    SELECT DISTINCT c.id, c.display_name, c.sort_order
    FROM classes c
    INNER JOIN results r ON c.id = r.class_id
    ORDER BY c.sort_order
");

// Handle apply action
if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['apply_bonus'])) {
    $selectionMode = $_POST['selection_mode'] ?? 'single';
    $eventIds = [];

    if ($selectionMode === 'series') {
        $seriesId = (int)$_POST['series_id'];
        if ($seriesId) {
            $seriesEvents = $db->getAll("SELECT id FROM events WHERE series_id = ?", [$seriesId]);
            $eventIds = array_column($seriesEvents, 'id');
        }
    } elseif ($selectionMode === 'multiple') {
        $eventIds = array_map('intval', $_POST['event_ids'] ?? []);
    } else {
        $eventId = (int)$_POST['event_id'];
        if ($eventId) $eventIds = [$eventId];
    }

    $classIds = array_map('intval', $_POST['class_ids'] ?? []);
    $stage = $_POST['stage'] ?? 'ss1';
    $scale = $_POST['point_scale'] ?? 'top3';

    if (!empty($eventIds) && $stage) {
        try {
            $db->pdo->beginTransaction();

            $stageColumn = preg_replace('/[^a-z0-9_]/', '', $stage);
            $pointValues = $defaultScales[$scale]['points'] ?? [25, 20, 16];

            $totalUpdated = 0;
            $eventsProcessed = 0;

            foreach ($eventIds as $eventId) {
                // Build query for this event
                $sql = "
                    SELECT r.id as result_id, r.class_id, r.{$stageColumn} as stage_time
                    FROM results r
                    WHERE r.event_id = ?
                      AND r.{$stageColumn} IS NOT NULL
                      AND r.{$stageColumn} != ''
                      AND r.{$stageColumn} != '0'
                ";
                $params = [$eventId];

                if (!empty($classIds)) {
                    $placeholders = implode(',', array_fill(0, count($classIds), '?'));
                    $sql .= " AND r.class_id IN ({$placeholders})";
                    $params = array_merge($params, $classIds);
                }

                $sql .= " ORDER BY r.class_id, r.{$stageColumn} ASC";

                $results = $db->getAll($sql, $params);

                if (empty($results)) continue;

                // Group by class
                $byClass = [];
                foreach ($results as $result) {
                    $cId = $result['class_id'] ?? 0;
                    if (!isset($byClass[$cId])) {
                        $byClass[$cId] = [];
                    }
                    $byClass[$cId][] = $result;
                }

                // Apply bonus points per class
                foreach ($byClass as $cId => $classResults) {
                    $rank = 1;
                    foreach ($classResults as $result) {
                        if ($rank <= count($pointValues)) {
                            $bonusPoints = $pointValues[$rank - 1];
                            $db->query(
                                "UPDATE results SET points = COALESCE(points, 0) + ? WHERE id = ?",
                                [$bonusPoints, $result['result_id']]
                            );
                            $totalUpdated++;
                        }
                        $rank++;
                    }
                }
                $eventsProcessed++;
            }

            $db->pdo->commit();

            $stageName = strtoupper($stage);
            $scaleName = $defaultScales[$scale]['name'] ?? $scale;
            $_SESSION['stage_bonus_message'] = "Lade till bonuspoäng för {$stageName} ({$scaleName}) i {$eventsProcessed} event - {$totalUpdated} deltagare uppdaterade";
            $_SESSION['stage_bonus_message_type'] = 'success';

        } catch (Exception $e) {
            if ($db->pdo->inTransaction()) {
                $db->pdo->rollBack();
            }
            $_SESSION['stage_bonus_message'] = "Fel: " . $e->getMessage();
            $_SESSION['stage_bonus_message_type'] = 'error';
        }

        header('Location: /admin/stage-bonus-points.php');
        exit;
    }
}

// Handle preview action
$previewResults = [];
$previewEventIds = [];
$previewClassIds = [];
$previewStage = null;
$previewScale = null;
$selectionMode = $_POST['selection_mode'] ?? $defaultSelectionMode;

if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['preview_bonus'])) {
    $selectionMode = $_POST['selection_mode'] ?? 'single';

    if ($selectionMode === 'series') {
        $seriesId = (int)$_POST['series_id'];
        if ($seriesId) {
            $seriesEvents = $db->getAll("SELECT id FROM events WHERE series_id = ?", [$seriesId]);
            $previewEventIds = array_column($seriesEvents, 'id');
        }
    } elseif ($selectionMode === 'multiple') {
        $previewEventIds = array_map('intval', $_POST['event_ids'] ?? []);
    } else {
        $eventId = (int)$_POST['event_id'];
        if ($eventId) $previewEventIds = [$eventId];
    }

    $previewClassIds = array_map('intval', $_POST['class_ids'] ?? []);
    $previewStage = $_POST['stage'] ?? 'ss1';
    $previewScale = $_POST['point_scale'] ?? 'top3';

    if (!empty($previewEventIds) && $previewStage) {
        $stageColumn = preg_replace('/[^a-z0-9_]/', '', $previewStage);
        $pointValues = $defaultScales[$previewScale]['points'] ?? [25, 20, 16];

        foreach ($previewEventIds as $eventId) {
            $sql = "
                SELECT r.id as result_id, r.cyclist_id, r.class_id, r.points as current_points,
                       r.{$stageColumn} as stage_time, r.event_id,
                       rd.firstname, rd.lastname,
                       cls.display_name as class_name,
                       e.name as event_name, e.date as event_date
                FROM results r
                INNER JOIN riders rd ON r.cyclist_id = rd.id
                LEFT JOIN classes cls ON r.class_id = cls.id
                LEFT JOIN events e ON r.event_id = e.id
                WHERE r.event_id = ?
                  AND r.{$stageColumn} IS NOT NULL
                  AND r.{$stageColumn} != ''
                  AND r.{$stageColumn} != '0'
            ";
            $params = [$eventId];

            if (!empty($previewClassIds)) {
                $placeholders = implode(',', array_fill(0, count($previewClassIds), '?'));
                $sql .= " AND r.class_id IN ({$placeholders})";
                $params = array_merge($params, $previewClassIds);
            }

            $sql .= " ORDER BY cls.sort_order, r.{$stageColumn} ASC";

            $results = $db->getAll($sql, $params);

            if (empty($results)) continue;

            // Group by event then class
            $eventName = $results[0]['event_name'] ?? 'Event';
            $eventDate = $results[0]['event_date'] ?? '';

            if (!isset($previewResults[$eventId])) {
                $previewResults[$eventId] = [
                    'event_name' => $eventName,
                    'event_date' => $eventDate,
                    'classes' => []
                ];
            }

            // Group by class
            $byClass = [];
            foreach ($results as $result) {
                $classKey = $result['class_id'] ?? 0;
                if (!isset($byClass[$classKey])) {
                    $byClass[$classKey] = [
                        'class_name' => $result['class_name'] ?? 'Okänd klass',
                        'riders' => []
                    ];
                }
                $byClass[$classKey]['riders'][] = $result;
            }

            // Calculate bonus points
            foreach ($byClass as $classId => &$classData) {
                $rank = 1;
                foreach ($classData['riders'] as &$rider) {
                    $bonusPoints = 0;
                    if ($rank <= count($pointValues)) {
                        $bonusPoints = $pointValues[$rank - 1];
                    }
                    $rider['rank'] = $rank;
                    $rider['bonus_points'] = $bonusPoints;
                    $rider['new_total'] = ($rider['current_points'] ?? 0) + $bonusPoints;
                    $rank++;
                }
            }
            unset($classData);

            $previewResults[$eventId]['classes'] = $byClass;
        }
    }
}

$page_title = 'Sträckbonus';
$breadcrumbs = [
    ['label' => 'Verktyg', 'url' => '/admin/tools.php'],
    ['label' => 'Sträckbonus']
];
include __DIR__ . '/components/unified-layout.php';
?>

<?php if ($message): ?>
    <div class="alert alert-<?= $messageType ?> mb-lg">
        <i data-lucide="<?= $messageType === 'success' ? 'check-circle' : 'alert-circle' ?>"></i>
        <?= htmlspecialchars($message) ?>
    </div>
<?php endif; ?>

<!-- Info Box -->
<div class="alert alert-info mb-lg">
    <i data-lucide="info"></i>
    <div>
        <strong>Sträckbonus:</strong> Ge extra poäng till de snabbaste på en specifik sträcka (PS/SS).
        Poängen läggs till befintliga poäng. Du kan välja enstaka event, flera event, eller en hel serie.
    </div>
</div>

<!-- Selection Form -->
<div class="card mb-lg">
    <div class="card-header">
        <h2><i data-lucide="trophy"></i> Välj event och sträcka</h2>
    </div>
    <div class="card-body">
        <form method="POST" id="bonus-form">

            <!-- Selection Mode Tabs -->
            <div class="selection-tabs mb-md">
                <button type="button" class="selection-tab active" data-mode="single" onclick="setSelectionMode('single')">
                    <i data-lucide="calendar"></i> Enstaka event
                </button>
                <button type="button" class="selection-tab" data-mode="series" onclick="setSelectionMode('series')">
                    <i data-lucide="layers"></i> Hel serie
                </button>
                <button type="button" class="selection-tab" data-mode="multiple" onclick="setSelectionMode('multiple')">
                    <i data-lucide="check-square"></i> Flera event
                </button>
            </div>
            <input type="hidden" name="selection_mode" id="selection_mode" value="<?= htmlspecialchars($selectionMode) ?>">

            <!-- Single Event Selection -->
            <div id="single-mode" class="selection-mode">
                <div class="form-group mb-md">
                    <label class="form-label">Event *</label>
                    <select name="event_id" id="event_id" class="form-select">
                        <option value="">Välj event...</option>
                        <?php foreach ($events as $event): ?>
                            <option value="<?= $event['id'] ?>">
                                <?= htmlspecialchars($event['name']) ?> (<?= date('Y-m-d', strtotime($event['date'])) ?>)
                                <?= $event['series_name'] ? ' - ' . htmlspecialchars($event['series_name']) : '' ?>
                            </option>
                        <?php endforeach; ?>
                    </select>
                </div>
            </div>

            <!-- Series Selection -->
            <div id="series-mode" class="selection-mode" style="display: none;">
                <div class="form-group mb-md">
                    <label class="form-label">Serie *</label>
                    <select name="series_id" id="series_id" class="form-select">
                        <option value="">Välj serie...</option>
                        <?php foreach ($series as $s): ?>
                            <option value="<?= $s['id'] ?>" <?= $preselectedSeriesId == $s['id'] ? 'selected' : '' ?>>
                                <?= htmlspecialchars($s['name']) ?> (<?= $s['year'] ?>) - <?= $s['event_count'] ?> event
                            </option>
                        <?php endforeach; ?>
                    </select>
                </div>
            </div>

            <!-- Multiple Events Selection -->
            <div id="multiple-mode" class="selection-mode" style="display: none;">
                <div class="form-group mb-md">
                    <label class="form-label">Välj event (flera)</label>
                    <div class="checkbox-grid">
                        <?php foreach ($events as $event): ?>
                            <label class="checkbox-item">
                                <input type="checkbox" name="event_ids[]" value="<?= $event['id'] ?>">
                                <span><?= htmlspecialchars($event['name']) ?> (<?= date('Y-m-d', strtotime($event['date'])) ?>)</span>
                            </label>
                        <?php endforeach; ?>
                    </div>
                </div>
            </div>

            <hr class="my-md">

            <!-- Class Selection (Multi-select) -->
            <div class="form-group mb-md">
                <label class="form-label">Klasser (lämna tomt för alla)</label>
                <div class="checkbox-grid checkbox-grid--classes">
                    <?php foreach ($allClasses as $class): ?>
                        <label class="checkbox-item">
                            <input type="checkbox" name="class_ids[]" value="<?= $class['id'] ?>"
                                   <?= in_array($class['id'], $previewClassIds) ? 'checked' : '' ?>>
                            <span><?= htmlspecialchars($class['display_name']) ?></span>
                        </label>
                    <?php endforeach; ?>
                </div>
                <div class="mt-sm">
                    <button type="button" class="btn btn-sm btn-ghost" onclick="selectAllClasses()">Välj alla</button>
                    <button type="button" class="btn btn-sm btn-ghost" onclick="deselectAllClasses()">Avmarkera alla</button>
                </div>
            </div>

            <hr class="my-md">

            <!-- Stage and Point Scale -->
            <div class="form-row">
                <div class="form-group">
                    <label class="form-label">Sträcka *</label>
                    <select name="stage" id="stage" class="form-select" required>
                        <option value="ss1" <?= $previewStage == 'ss1' ? 'selected' : '' ?>>SS1 / PS1</option>
                        <option value="ss2" <?= $previewStage == 'ss2' ? 'selected' : '' ?>>SS2 / PS2</option>
                        <option value="ss3" <?= $previewStage == 'ss3' ? 'selected' : '' ?>>SS3 / PS3</option>
                        <option value="ss4" <?= $previewStage == 'ss4' ? 'selected' : '' ?>>SS4 / PS4</option>
                        <option value="ss5" <?= $previewStage == 'ss5' ? 'selected' : '' ?>>SS5 / PS5</option>
                        <option value="ss6" <?= $previewStage == 'ss6' ? 'selected' : '' ?>>SS6 / PS6</option>
                        <option value="ss7" <?= $previewStage == 'ss7' ? 'selected' : '' ?>>SS7 / PS7</option>
                        <option value="ss8" <?= $previewStage == 'ss8' ? 'selected' : '' ?>>SS8 / PS8</option>
                    </select>
                </div>

                <div class="form-group">
                    <label class="form-label">Poängskala *</label>
                    <select name="point_scale" id="point_scale" class="form-select" required>
                        <?php foreach ($defaultScales as $key => $scale): ?>
                            <option value="<?= $key ?>" <?= $previewScale == $key ? 'selected' : '' ?>>
                                <?= htmlspecialchars($scale['name']) ?> (<?= implode(', ', $scale['points']) ?>)
                            </option>
                        <?php endforeach; ?>
                    </select>
                </div>
            </div>

            <div class="btn-group mt-lg">
                <button type="submit" name="preview_bonus" class="btn btn-secondary">
                    <i data-lucide="eye"></i>
                    Förhandsgranska
                </button>
                <?php if (!empty($previewResults)): ?>
                <button type="submit" name="apply_bonus" class="btn btn-primary"
                        onclick="return confirm('Lägga till bonuspoäng för <?= count($previewResults) ?> event? Poängen adderas till befintliga poäng.');">
                    <i data-lucide="plus-circle"></i>
                    Lägg till bonuspoäng (<?= count($previewResults) ?> event)
                </button>
                <?php endif; ?>
            </div>
        </form>
    </div>
</div>

<!-- Preview Results -->
<?php if (!empty($previewResults)): ?>
<div class="card">
    <div class="card-header">
        <h2><i data-lucide="list"></i> Förhandsgranskning - <?= strtoupper($previewStage) ?> bonus (<?= count($previewResults) ?> event)</h2>
    </div>
    <div class="card-body">
        <?php foreach ($previewResults as $eventId => $eventData): ?>
        <div class="event-preview mb-xl">
            <h3 class="event-preview-title">
                <i data-lucide="calendar"></i>
                <?= htmlspecialchars($eventData['event_name']) ?>
                <span class="text-muted">(<?= date('Y-m-d', strtotime($eventData['event_date'])) ?>)</span>
            </h3>

            <?php foreach ($eventData['classes'] as $classId => $classData): ?>
            <div class="mb-lg">
                <h4 class="text-accent mb-sm"><?= htmlspecialchars($classData['class_name']) ?></h4>
                <div class="table-responsive">
                    <table class="table table--sm">
                        <thead>
                            <tr>
                                <th style="width: 50px;">Rank</th>
                                <th>Namn</th>
                                <th>Sträcktid</th>
                                <th class="text-right">Nu</th>
                                <th class="text-right">Bonus</th>
                                <th class="text-right">Nytt</th>
                            </tr>
                        </thead>
                        <tbody>
                            <?php foreach (array_slice($classData['riders'], 0, 10) as $rider): ?>
                            <tr class="<?= $rider['bonus_points'] > 0 ? 'highlight-row' : '' ?>">
                                <td>
                                    <?php if ($rider['rank'] <= 3 && $rider['bonus_points'] > 0): ?>
                                        <span class="badge badge-<?= $rider['rank'] == 1 ? 'warning' : 'secondary' ?>"><?= $rider['rank'] ?></span>
                                    <?php else: ?>
                                        <?= $rider['rank'] ?>
                                    <?php endif; ?>
                                </td>
                                <td><strong><?= htmlspecialchars($rider['firstname'] . ' ' . $rider['lastname']) ?></strong></td>
                                <td><?= htmlspecialchars($rider['stage_time']) ?></td>
                                <td class="text-right"><?= $rider['current_points'] ?? 0 ?></td>
                                <td class="text-right">
                                    <?php if ($rider['bonus_points'] > 0): ?>
                                        <span class="text-success">+<?= $rider['bonus_points'] ?></span>
                                    <?php else: ?>
                                        <span class="text-muted">-</span>
                                    <?php endif; ?>
                                </td>
                                <td class="text-right"><strong><?= $rider['new_total'] ?></strong></td>
                            </tr>
                            <?php endforeach; ?>
                            <?php if (count($classData['riders']) > 10): ?>
                            <tr>
                                <td colspan="6" class="text-muted text-center">
                                    ... och <?= count($classData['riders']) - 10 ?> till
                                </td>
                            </tr>
                            <?php endif; ?>
                        </tbody>
                    </table>
                </div>
            </div>
            <?php endforeach; ?>
        </div>
        <?php endforeach; ?>
    </div>
</div>
<?php endif; ?>

<style>
.selection-tabs {
    display: flex;
    gap: var(--space-sm);
    flex-wrap: wrap;
}
.selection-tab {
    display: flex;
    align-items: center;
    gap: var(--space-xs);
    padding: var(--space-sm) var(--space-md);
    background: #ffffff;
    border: 1px solid var(--color-border);
    border-radius: var(--radius-sm);
    font-size: 0.875rem;
    font-weight: 500;
    color: #171717;
    cursor: pointer;
    transition: all 0.15s ease;
}
.selection-tab:hover {
    background: #f5f5f5;
}
.selection-tab.active {
    background: #171717;
    border-color: #171717;
    color: #ffffff;
}
.selection-tab i {
    width: 16px;
    height: 16px;
}
.checkbox-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
    gap: var(--space-xs);
    max-height: 300px;
    overflow-y: auto;
    padding: var(--space-sm);
    background: var(--color-bg-surface, #f8f9fa);
    border-radius: var(--radius-sm);
}
.checkbox-grid--classes {
    grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
}
.checkbox-item {
    display: flex;
    align-items: center;
    gap: var(--space-xs);
    padding: var(--space-xs) var(--space-sm);
    background: white;
    border-radius: var(--radius-sm);
    cursor: pointer;
    font-size: 0.875rem;
}
.checkbox-item:hover {
    background: #f0f0f0;
}
.checkbox-item input {
    margin: 0;
}
.form-row {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: var(--space-md);
}
.highlight-row {
    background: rgba(97, 206, 112, 0.1);
}
.text-success {
    color: var(--color-success);
    font-weight: 600;
}
.btn-group {
    display: flex;
    gap: var(--space-sm);
    flex-wrap: wrap;
}
.event-preview {
    padding-bottom: var(--space-lg);
    border-bottom: 2px solid var(--color-border);
}
.event-preview:last-child {
    border-bottom: none;
}
.event-preview-title {
    display: flex;
    align-items: center;
    gap: var(--space-sm);
    font-size: 1.1rem;
    margin-bottom: var(--space-md);
    color: var(--color-primary);
}
.event-preview-title i {
    width: 20px;
    height: 20px;
}
.my-md {
    margin-top: var(--space-md);
    margin-bottom: var(--space-md);
}
.mb-xl {
    margin-bottom: var(--space-xl);
}
.table--sm {
    font-size: 0.8rem;
}
.table--sm th, .table--sm td {
    padding: var(--space-xs) var(--space-sm);
}
hr {
    border: none;
    border-top: 1px solid var(--color-border);
}
.btn-sm {
    padding: var(--space-xs) var(--space-sm);
    font-size: 0.75rem;
}
.btn-ghost {
    background: transparent;
    border: 1px solid var(--color-border);
}
.btn-ghost:hover {
    background: #f5f5f5;
}
</style>

<script>
function setSelectionMode(mode) {
    // Update hidden input
    document.getElementById('selection_mode').value = mode;

    // Update tab buttons
    document.querySelectorAll('.selection-tab').forEach(tab => {
        tab.classList.toggle('active', tab.dataset.mode === mode);
    });

    // Show/hide mode sections
    document.querySelectorAll('.selection-mode').forEach(section => {
        section.style.display = 'none';
    });
    document.getElementById(mode + '-mode').style.display = 'block';

    // Re-init Lucide icons
    if (typeof lucide !== 'undefined') {
        lucide.createIcons();
    }
}

function selectAllClasses() {
    document.querySelectorAll('input[name="class_ids[]"]').forEach(cb => cb.checked = true);
}

function deselectAllClasses() {
    document.querySelectorAll('input[name="class_ids[]"]').forEach(cb => cb.checked = false);
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
    const mode = document.getElementById('selection_mode').value || 'single';
    setSelectionMode(mode);
});
</script>

<?php include __DIR__ . '/components/unified-layout-footer.php'; ?>
