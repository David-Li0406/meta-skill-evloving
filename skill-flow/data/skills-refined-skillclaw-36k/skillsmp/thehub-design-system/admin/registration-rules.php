<?php
/**
 * Admin: Registration Rules - Simplified
 *
 * Select which event class (National/Sportmotion/Motion) applies to a series.
 * All license rules are managed in the License-Class Matrix.
 */

require_once __DIR__ . '/../config.php';
require_admin();

$db = getDB();
$pdo = $db->getPdo();

// Initialize message variables
$message = '';
$messageType = 'info';

// Event classes (matches license-class-matrix.php)
$eventClasses = [
    'national' => [
        'name' => 'Nationellt',
        'desc' => 'Nationella tävlingar med full rankingpoäng och strikta licensregler',
        'icon' => 'trophy',
        'color' => 'warning'
    ],
    'sportmotion' => [
        'name' => 'Sportmotion',
        'desc' => 'Sportmotion-event med 50% rankingpoäng',
        'icon' => 'bike',
        'color' => 'info'
    ],
    'motion' => [
        'name' => 'Motion',
        'desc' => 'Motion-event utan rankingpoäng, öppet för alla',
        'icon' => 'heart',
        'color' => 'success'
    ]
];

// Handle form submission
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    checkCsrf();

    $seriesId = filter_input(INPUT_POST, 'series_id', FILTER_VALIDATE_INT);
    $eventClass = $_POST['event_class'] ?? '';

    if ($seriesId && array_key_exists($eventClass, $eventClasses)) {
        try {
            $db->update('series', [
                'event_license_class' => $eventClass
            ], 'id = ?', [$seriesId]);

            $message = "Eventklass ändrad till '{$eventClasses[$eventClass]['name']}'";
            $messageType = 'success';
        } catch (Exception $e) {
            $message = 'Fel: ' . $e->getMessage();
            $messageType = 'error';
        }
    }
}

// Get series ID
$selectedSeriesId = filter_input(INPUT_GET, 'series_id', FILTER_VALIDATE_INT);

// Get series list
$currentYear = date('Y');
$series = $db->getAll("
    SELECT id, name, year, event_license_class
    FROM series
    WHERE year >= ?
    ORDER BY year DESC, name ASC
", [$currentYear - 1]);

// Get selected series
$selectedSeries = null;
if ($selectedSeriesId) {
    $selectedSeries = $db->getRow("SELECT * FROM series WHERE id = ?", [$selectedSeriesId]);
}

// Page setup
$page_title = 'Eventklass för serie';
$page_group = 'config';
include __DIR__ . '/components/unified-layout.php';
?>

<div class="flex justify-between items-center mb-lg">
    <p class="text-secondary">
        Välj vilken eventklass som gäller för serien. Detta styr vilka licenstyper som får anmäla sig.
    </p>
</div>

<?php if ($message): ?>
<div class="alert alert-<?= $messageType ?> mb-lg">
    <i data-lucide="<?= $messageType === 'success' ? 'check-circle' : 'alert-circle' ?>"></i>
    <?= h($message) ?>
</div>
<?php endif; ?>

<!-- Series Selector -->
<div class="admin-card mb-lg">
    <div class="admin-card-header">
        <h2><i data-lucide="calendar"></i> Välj serie</h2>
    </div>
    <div class="admin-card-body">
        <form method="GET" class="flex gap-md items-end">
            <div class="admin-form-group" style="flex: 1; max-width: 400px;">
                <label class="admin-form-label">Serie</label>
                <select name="series_id" class="admin-form-select" onchange="this.form.submit()">
                    <option value="">-- Välj serie --</option>
                    <?php foreach ($series as $s): ?>
                    <option value="<?= $s['id'] ?>" <?= $selectedSeriesId == $s['id'] ? 'selected' : '' ?>>
                        <?= h($s['name']) ?> (<?= $s['year'] ?>)
                        <?php if ($s['event_license_class']): ?>
                            - <?= h($eventClasses[$s['event_license_class']]['name'] ?? $s['event_license_class']) ?>
                        <?php endif; ?>
                    </option>
                    <?php endforeach; ?>
                </select>
            </div>
        </form>
    </div>
</div>

<?php if ($selectedSeries): ?>

<?php
// Fetch events in this series
$seriesEvents = $db->getAll("
    SELECT e.id, e.name, e.date, e.location, e.active,
           e.registration_opens, e.registration_deadline
    FROM events e
    WHERE e.series_id = ?
    ORDER BY e.date ASC
", [$selectedSeriesId]);

// DEBUG: Kolla om events finns med raw PDO
$debugStmt = $pdo->prepare("SELECT COUNT(*) as cnt FROM events WHERE series_id = ?");
$debugStmt->execute([$selectedSeriesId]);
$debugCount = $debugStmt->fetch(PDO::FETCH_ASSOC);
error_log("REGISTRATION-RULES DEBUG: series_id={$selectedSeriesId}, events found via getAll=" . count($seriesEvents) . ", raw count=" . ($debugCount['cnt'] ?? 'error'));
?>

<!-- DEBUG INFO -->
<div class="alert alert-info mb-md" style="font-size: 0.8rem;">
    <strong>Debug:</strong> series_id=<?= $selectedSeriesId ?>,
    events via getAll=<?= count($seriesEvents) ?>,
    raw SQL count=<?= $debugCount['cnt'] ?? 'error' ?>
</div>

<!-- Events in Series -->
<div class="admin-card mb-lg">
    <div class="admin-card-header">
        <h2><i data-lucide="calendar-days"></i> Events i serien (<?= count($seriesEvents) ?>)</h2>
    </div>
    <div class="admin-card-body">
        <?php if (empty($seriesEvents)): ?>
            <p class="text-secondary">Inga events kopplade till denna serie.</p>
        <?php else: ?>
            <div class="admin-table-container">
                <table class="admin-table">
                    <thead>
                        <tr>
                            <th>Event</th>
                            <th>Datum</th>
                            <th>Plats</th>
                            <th>Status</th>
                            <th></th>
                        </tr>
                    </thead>
                    <tbody>
                        <?php foreach ($seriesEvents as $evt): ?>
                        <tr>
                            <td>
                                <strong><?= h($evt['name']) ?></strong>
                            </td>
                            <td><?= date('Y-m-d', strtotime($evt['date'])) ?></td>
                            <td><?= h($evt['location'] ?? '-') ?></td>
                            <td>
                                <?php if ($evt['active']): ?>
                                    <span class="badge badge-success">Aktiv</span>
                                <?php else: ?>
                                    <span class="badge badge-warning">Inaktiv</span>
                                <?php endif; ?>
                            </td>
                            <td>
                                <a href="/admin/event-edit.php?id=<?= $evt['id'] ?>" class="btn-admin btn-admin-sm btn-admin-secondary">
                                    <i data-lucide="pencil"></i>
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

<!-- Event Class Selection -->
<div class="admin-card mb-lg">
    <div class="admin-card-header">
        <h2><i data-lucide="shield"></i> Eventklass: <?= h($selectedSeries['name']) ?></h2>
    </div>
    <div class="admin-card-body">
        <form method="POST">
            <?= csrf_field() ?>
            <input type="hidden" name="series_id" value="<?= $selectedSeriesId ?>">

            <div class="grid gap-md" style="grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));">
                <?php foreach ($eventClasses as $key => $info):
                    $isSelected = ($selectedSeries['event_license_class'] ?? '') === $key;
                ?>
                <label class="admin-card" style="cursor: pointer; border: 2px solid <?= $isSelected ? 'var(--color-accent)' : 'var(--color-border)' ?>; background: <?= $isSelected ? 'var(--color-accent-light)' : 'var(--color-bg-surface)' ?>;">
                    <div class="admin-card-body">
                        <div class="flex gap-md items-start">
                            <input type="radio" name="event_class" value="<?= $key ?>"
                                <?= $isSelected ? 'checked' : '' ?>
                                style="margin-top: 4px;">
                            <div>
                                <div class="flex items-center gap-sm mb-xs">
                                    <i data-lucide="<?= $info['icon'] ?>" style="width: 20px; height: 20px;"></i>
                                    <strong style="font-size: 1.1rem;"><?= h($info['name']) ?></strong>
                                </div>
                                <p class="text-secondary text-sm" style="margin: 0;">
                                    <?= h($info['desc']) ?>
                                </p>
                            </div>
                        </div>
                    </div>
                </label>
                <?php endforeach; ?>
            </div>

            <div class="mt-lg">
                <button type="submit" class="btn-admin btn-admin-primary">
                    <i data-lucide="save"></i>
                    Spara eventklass
                </button>
            </div>
        </form>
    </div>
</div>

<!-- Link to License Matrix -->
<div class="admin-card">
    <div class="admin-card-header">
        <h2><i data-lucide="grid-3x3"></i> Licensregler</h2>
    </div>
    <div class="admin-card-body">
        <p class="text-secondary mb-lg">
            Licensreglerna (vilka licenstyper som får anmäla sig till vilka klasser) hanteras i
            <strong>Licens-Klass Matrisen</strong>. Samma regler gäller för alla serier med samma eventklass.
        </p>

        <?php
        $currentClass = $selectedSeries['event_license_class'] ?? 'sportmotion';
        ?>
        <a href="/admin/license-class-matrix.php?tab=<?= h($currentClass) ?>" class="btn-admin btn-admin-secondary">
            <i data-lucide="external-link"></i>
            Öppna Licens-Klass Matris (<?= h($eventClasses[$currentClass]['name'] ?? 'Sportmotion') ?>)
        </a>
    </div>
</div>
<?php endif; ?>

<?php include __DIR__ . '/components/unified-layout-footer.php'; ?>
