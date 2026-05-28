<?php
/**
 * Event Class Manager - Fix wrong classes per event
 * Filter by event, see classes with counts, save all changes at once
 */
require_once __DIR__ . '/../config.php';
require_admin();

$db = getDB();

// Handle form submit
if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['save_changes'])) {
    checkCsrf();

    $eventId = (int)$_POST['event_id'];
    $changes = $_POST['changes'] ?? [];
    $changedCount = 0;

    foreach ($changes as $fromClassId => $toClassId) {
        $fromClassId = (int)$fromClassId;
        $toClassId = (int)$toClassId;

        if ($toClassId > 0 && $fromClassId !== $toClassId) {
            $db->update('results',
                ['class_id' => $toClassId],
                'event_id = ? AND class_id = ?',
                [$eventId, $fromClassId]
            );
            $changedCount++;
        }
    }

    if ($changedCount > 0) {
        $_SESSION['flash_message'] = "$changedCount klassbyten sparade!";
        $_SESSION['flash_type'] = 'success';
    }

    header("Location: ?event_id=$eventId");
    exit;
}

// Get selected event
$selectedEventId = isset($_GET['event_id']) ? (int)$_GET['event_id'] : 0;

// Get all events for dropdown
$allEvents = $db->getAll("
    SELECT e.id, e.name, e.date, COUNT(r.id) as result_count
    FROM events e
    LEFT JOIN results r ON e.id = r.event_id
    GROUP BY e.id
    HAVING result_count > 0
    ORDER BY e.date DESC
");

// Get classes for selected event
if ($selectedEventId > 0) {
    $classesQuery = "
        SELECT
            c.id as class_id,
            c.display_name as class_name,
            c.name as class_code,
            c.sort_order,
            COUNT(r.id) as result_count
        FROM results r
        JOIN classes c ON r.class_id = c.id
        WHERE r.event_id = ?
        GROUP BY c.id
        ORDER BY c.sort_order, c.display_name
    ";
    $eventClasses = $db->getAll($classesQuery, [$selectedEventId]);
    $selectedEvent = $db->getRow("SELECT id, name, date FROM events WHERE id = ?", [$selectedEventId]);
} else {
    $eventClasses = [];
    $selectedEvent = null;
}

// Get ALL classes for dropdown
$allClasses = $db->getAll("
    SELECT id, display_name, sort_order
    FROM classes
    WHERE active = 1
    ORDER BY sort_order, display_name
");

$page_title = 'Fixa Klasser per Event';
$breadcrumbs = [
    ['label' => 'Import', 'url' => '/admin/import.php'],
    ['label' => 'Fixa Klasser']
];

include __DIR__ . '/components/unified-layout.php';
?>

<style>
.event-filter {
    display: flex;
    gap: var(--space-md);
    align-items: center;
    margin-bottom: var(--space-lg);
    flex-wrap: wrap;
}
.event-filter select {
    min-width: 300px;
}
.class-table {
    width: 100%;
}
.class-table th,
.class-table td {
    padding: var(--space-sm) var(--space-md);
    text-align: left;
    border-bottom: 1px solid var(--color-border);
}
.class-table th {
    background: var(--color-surface);
    font-weight: 600;
}
.class-table tr:hover {
    background: var(--color-surface-hover);
}
.class-table .count {
    font-weight: 600;
    min-width: 60px;
}
.class-table select {
    min-width: 200px;
}
.class-name.suspicious {
    color: var(--color-warning);
    font-weight: 600;
}
.event-summary {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
    gap: var(--space-md);
}
.event-summary-card {
    display: block;
    background: var(--color-surface);
    border: 1px solid var(--color-border);
    border-radius: var(--radius-sm);
    padding: var(--space-md);
    text-decoration: none;
    color: inherit;
}
.event-summary-card:hover {
    border-color: var(--color-accent);
}
.event-summary-card h4 {
    margin: 0 0 var(--space-sm) 0;
}
.event-summary-card .meta {
    color: var(--color-text);
    font-size: 0.875rem;
}
.save-bar {
    position: sticky;
    bottom: 0;
    background: var(--color-background);
    padding: var(--space-md);
    border-top: 2px solid var(--color-accent);
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin: var(--space-lg) calc(-1 * var(--space-md)) 0;
}
.changed-row {
    background: rgba(97, 206, 112, 0.1) !important;
}
</style>

<?php if (isset($_SESSION['flash_message'])): ?>
<div class="alert alert-<?= $_SESSION['flash_type'] ?? 'info' ?> mb-lg">
    <?= h($_SESSION['flash_message']) ?>
</div>
<?php unset($_SESSION['flash_message'], $_SESSION['flash_type']); endif; ?>

<div class="card">
    <div class="card-header">
        <h2>
            <i data-lucide="layers"></i>
            Fixa Klasser per Event
        </h2>
    </div>
    <div class="card-body">
        <!-- Event Filter -->
        <div class="event-filter">
            <label class="label" style="margin:0;">Välj Event:</label>
            <select id="eventSelect" class="input" onchange="filterByEvent(this.value)">
                <option value="0">-- Välj ett event --</option>
                <?php foreach ($allEvents as $e): ?>
                <option value="<?= $e['id'] ?>" <?= $selectedEventId == $e['id'] ? 'selected' : '' ?>>
                    <?= h($e['name']) ?> (<?= date('Y-m-d', strtotime($e['date'])) ?>) - <?= $e['result_count'] ?> resultat
                </option>
                <?php endforeach; ?>
            </select>
            <?php if ($selectedEventId > 0): ?>
            <a href="?event_id=0" class="btn btn--secondary btn--sm">
                <i data-lucide="x"></i> Rensa
            </a>
            <?php endif; ?>
        </div>

        <?php if ($selectedEventId > 0 && $selectedEvent): ?>
        <!-- Selected Event Classes -->
        <form method="POST" id="classForm">
            <?= csrf_field() ?>
            <input type="hidden" name="event_id" value="<?= $selectedEventId ?>">
            <input type="hidden" name="save_changes" value="1">

            <div class="mb-md">
                <h3><?= h($selectedEvent['name']) ?></h3>
                <p class="text-secondary"><?= date('Y-m-d', strtotime($selectedEvent['date'])) ?> · <?= count($eventClasses) ?> klasser</p>
            </div>

            <?php if (!empty($eventClasses)): ?>
            <table class="class-table">
                <thead>
                    <tr>
                        <th>Nuvarande klass</th>
                        <th>Antal</th>
                        <th>Byt till</th>
                    </tr>
                </thead>
                <tbody>
                    <?php foreach ($eventClasses as $class): ?>
                    <?php $isSuspicious = $class['sort_order'] >= 900; ?>
                    <tr data-class-id="<?= $class['class_id'] ?>">
                        <td class="class-name <?= $isSuspicious ? 'suspicious' : '' ?>">
                            <?= h($class['class_name']) ?>
                            <?php if ($isSuspicious): ?>
                            <i data-lucide="alert-circle" style="width:14px;height:14px;color:var(--color-warning);vertical-align:middle;"></i>
                            <?php endif; ?>
                        </td>
                        <td class="count"><?= $class['result_count'] ?></td>
                        <td>
                            <select name="changes[<?= $class['class_id'] ?>]" class="input input-sm class-select">
                                <option value="">-- Behåll --</option>
                                <?php foreach ($allClasses as $ac): ?>
                                <?php if ($ac['id'] != $class['class_id']): ?>
                                <option value="<?= $ac['id'] ?>"><?= h($ac['display_name']) ?></option>
                                <?php endif; ?>
                                <?php endforeach; ?>
                            </select>
                        </td>
                    </tr>
                    <?php endforeach; ?>
                </tbody>
            </table>

            <div class="save-bar">
                <span id="changeCount" class="text-secondary">Inga ändringar</span>
                <button type="submit" class="btn btn--primary btn-lg" id="saveBtn" disabled>
                    <i data-lucide="save"></i>
                    Spara alla ändringar
                </button>
            </div>
            <?php else: ?>
            <p class="text-secondary">Inga klasser hittades för detta event.</p>
            <?php endif; ?>
        </form>

        <?php else: ?>
        <!-- No event selected - show summary -->
        <p class="text-secondary mb-lg">Välj ett event i listan ovan för att se och ändra dess klasser.</p>

        <h3 class="mb-md">Senaste events med resultat</h3>
        <div class="event-summary">
            <?php foreach (array_slice($allEvents, 0, 12) as $e): ?>
            <a href="?event_id=<?= $e['id'] ?>" class="event-summary-card">
                <h4><?= h($e['name']) ?></h4>
                <div class="meta">
                    <span><?= date('Y-m-d', strtotime($e['date'])) ?></span>
                    <span> · <?= $e['result_count'] ?> resultat</span>
                </div>
            </a>
            <?php endforeach; ?>
        </div>
        <?php endif; ?>
    </div>
</div>

<script>
function filterByEvent(eventId) {
    window.location.href = '?event_id=' + eventId;
}

// Track changes
document.querySelectorAll('.class-select').forEach(select => {
    select.addEventListener('change', function() {
        const row = this.closest('tr');
        if (this.value) {
            row.classList.add('changed-row');
        } else {
            row.classList.remove('changed-row');
        }
        updateChangeCount();
    });
});

function updateChangeCount() {
    const changed = document.querySelectorAll('.class-select').length > 0
        ? [...document.querySelectorAll('.class-select')].filter(s => s.value).length
        : 0;
    const countEl = document.getElementById('changeCount');
    const saveBtn = document.getElementById('saveBtn');

    if (changed > 0) {
        countEl.textContent = changed + ' ändring' + (changed > 1 ? 'ar' : '') + ' att spara';
        countEl.style.color = 'var(--color-accent)';
        countEl.style.fontWeight = '600';
        saveBtn.disabled = false;
    } else {
        countEl.textContent = 'Inga ändringar';
        countEl.style.color = '';
        countEl.style.fontWeight = '';
        saveBtn.disabled = true;
    }
}

if (typeof lucide !== 'undefined') lucide.createIcons();
</script>

<?php include __DIR__ . '/components/unified-layout-footer.php'; ?>
