<?php
/**
 * Quick Edit Results - Fix mismatched riders and classes
 * Bulk fix tool for imported results
 */
require_once __DIR__ . '/../config.php';
require_admin();

$db = getDB();

// Handle AJAX
if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['ajax'])) {
    header('Content-Type: application/json');
    checkCsrf();

    $action = $_POST['action'] ?? '';

    try {
        switch ($action) {
            case 'change_rider':
                $resultId = (int)$_POST['result_id'];
                $newRiderId = (int)$_POST['new_rider_id'];

                $db->update('results', ['cyclist_id' => $newRiderId], 'id = ?', [$resultId]);
                echo json_encode(['success' => true]);
                exit;

            case 'change_class':
                $resultId = (int)$_POST['result_id'];
                $newClassId = (int)$_POST['new_class_id'];

                $db->update('results', ['class_id' => $newClassId], 'id = ?', [$resultId]);
                echo json_encode(['success' => true]);
                exit;

            case 'merge_riders':
                $sourceId = (int)$_POST['source_id'];
                $targetId = (int)$_POST['target_id'];

                // Move all results to target
                $db->execute("UPDATE results SET cyclist_id = ? WHERE cyclist_id = ?", [$targetId, $sourceId]);
                // Delete source rider
                $db->delete('riders', 'id = ?', [$sourceId]);

                echo json_encode(['success' => true]);
                exit;

            case 'bulk_change_class':
                $resultIds = $_POST['result_ids'] ?? [];
                $newClassId = (int)$_POST['new_class_id'];

                if (!empty($resultIds)) {
                    $placeholders = implode(',', array_fill(0, count($resultIds), '?'));
                    $db->execute(
                        "UPDATE results SET class_id = ? WHERE id IN ($placeholders)",
                        array_merge([$newClassId], $resultIds)
                    );
                }
                echo json_encode(['success' => true, 'count' => count($resultIds)]);
                exit;

            case 'search_riders':
                $query = trim($_POST['query'] ?? '');
                if (strlen($query) < 2) {
                    echo json_encode(['riders' => []]);
                    exit;
                }

                $riders = $db->getAll(
                    "SELECT r.id, r.firstname, r.lastname, r.license_number, c.name as club_name
                     FROM riders r
                     LEFT JOIN clubs c ON r.club_id = c.id
                     WHERE r.firstname LIKE ? OR r.lastname LIKE ? OR CONCAT(r.firstname, ' ', r.lastname) LIKE ?
                     ORDER BY r.lastname, r.firstname
                     LIMIT 20",
                    ["%$query%", "%$query%", "%$query%"]
                );
                echo json_encode(['riders' => $riders]);
                exit;

            default:
                echo json_encode(['success' => false, 'error' => 'Unknown action']);
                exit;
        }
    } catch (Exception $e) {
        echo json_encode(['success' => false, 'error' => $e->getMessage()]);
        exit;
    }
}

// Get filter params
$eventId = $_GET['event_id'] ?? '';
$classFilter = $_GET['class'] ?? '';
$search = $_GET['search'] ?? '';

// Get events for filter
$events = $db->getAll("
    SELECT e.id, e.name, e.date, COUNT(r.id) as result_count
    FROM events e
    LEFT JOIN results r ON e.id = r.event_id
    GROUP BY e.id
    ORDER BY e.date DESC
    LIMIT 200
");

// Get classes for filter
$classes = $db->getAll("SELECT id, display_name FROM classes ORDER BY sort_order, display_name");

// Build results query
$where = [];
$params = [];

if ($eventId) {
    $where[] = "r.event_id = ?";
    $params[] = $eventId;
}
if ($classFilter) {
    $where[] = "r.class_id = ?";
    $params[] = $classFilter;
}
if ($search) {
    $where[] = "(rd.firstname LIKE ? OR rd.lastname LIKE ? OR CONCAT(rd.firstname, ' ', rd.lastname) LIKE ?)";
    $params[] = "%$search%";
    $params[] = "%$search%";
    $params[] = "%$search%";
}

$whereClause = $where ? 'WHERE ' . implode(' AND ', $where) : '';

// Get results with full info
$results = [];
if ($eventId || $classFilter || $search) {
    $results = $db->getAll("
        SELECT
            r.id as result_id,
            r.event_id,
            r.cyclist_id,
            r.class_id,
            r.position,
            r.finish_time,
            r.bib_number,
            rd.firstname,
            rd.lastname,
            rd.license_number,
            cl.name as club_name,
            cls.display_name as class_name,
            e.name as event_name,
            e.date as event_date
        FROM results r
        JOIN riders rd ON r.cyclist_id = rd.id
        LEFT JOIN clubs cl ON rd.club_id = cl.id
        LEFT JOIN classes cls ON r.class_id = cls.id
        JOIN events e ON r.event_id = e.id
        $whereClause
        ORDER BY r.position ASC, rd.lastname ASC
        LIMIT 500
    ", $params);
}

// Page config
$page_title = 'Snabbredigera Resultat';
$breadcrumbs = [
    ['label' => 'Resultat', 'url' => '/admin/results.php'],
    ['label' => 'Snabbredigera']
];

include __DIR__ . '/components/unified-layout.php';
?>

<style>
.result-row {
    display: grid;
    grid-template-columns: 50px 60px 1fr 200px 200px 120px;
    gap: var(--space-sm);
    padding: var(--space-sm);
    border-bottom: 1px solid var(--color-border);
    align-items: center;
}
.result-row:hover {
    background: var(--color-surface-hover);
}
.result-row.selected {
    background: rgba(97, 206, 112, 0.1);
}
.result-header {
    font-weight: 600;
    background: var(--color-surface);
    position: sticky;
    top: 0;
}
.rider-cell {
    display: flex;
    flex-direction: column;
}
.rider-name {
    font-weight: 500;
}
.rider-meta {
    font-size: 12px;
    color: var(--color-text-secondary);
}
.inline-select {
    padding: 4px 8px;
    font-size: 13px;
    border: 1px solid var(--color-border);
    border-radius: var(--radius-sm);
    background: var(--color-surface);
    cursor: pointer;
}
.inline-select:hover {
    border-color: var(--color-accent);
}
.action-panel {
    position: fixed;
    bottom: 0;
    left: 0;
    right: 0;
    background: var(--color-surface);
    border-top: 2px solid var(--color-accent);
    padding: var(--space-md);
    padding-bottom: calc(var(--space-md) + env(safe-area-inset-bottom, 0px));
    display: none;
    z-index: 100;
    box-shadow: 0 -4px 20px rgba(0,0,0,0.15);
}
.action-panel.active {
    display: block;
}
/* Mobile: Position above mobile nav */
@media (max-width: 899px) and (orientation: portrait) {
    .action-panel {
        bottom: calc(var(--mobile-nav-height, 64px) + env(safe-area-inset-bottom, 0px));
        padding-bottom: var(--space-md);
    }
    .action-panel .flex {
        flex-direction: column;
        gap: var(--space-md);
    }
}
.search-rider-input {
    position: relative;
}
.search-rider-results {
    position: absolute;
    top: 100%;
    left: 0;
    right: 0;
    background: var(--color-surface);
    border: 1px solid var(--color-border);
    border-radius: var(--radius-sm);
    max-height: 200px;
    overflow-y: auto;
    z-index: 10;
    display: none;
}
.search-rider-results.active {
    display: block;
}
.search-rider-item {
    padding: var(--space-sm);
    cursor: pointer;
}
.search-rider-item:hover {
    background: var(--color-surface-hover);
}
</style>

<!-- Filters -->
<div class="card mb-lg">
    <div class="card-body">
        <form method="GET" class="flex flex-wrap gap-md items-end">
            <div>
                <label class="label">Event</label>
                <select name="event_id" class="input" style="width: 300px;">
                    <option value="">-- Välj event --</option>
                    <?php foreach ($events as $e): ?>
                    <option value="<?= $e['id'] ?>" <?= $eventId == $e['id'] ? 'selected' : '' ?>>
                        <?= h($e['name']) ?> (<?= date('Y-m-d', strtotime($e['date'])) ?>) - <?= $e['result_count'] ?> res
                    </option>
                    <?php endforeach; ?>
                </select>
            </div>
            <div>
                <label class="label">Klass</label>
                <select name="class" class="input" style="width: 200px;">
                    <option value="">Alla klasser</option>
                    <?php foreach ($classes as $c): ?>
                    <option value="<?= $c['id'] ?>" <?= $classFilter == $c['id'] ? 'selected' : '' ?>>
                        <?= h($c['display_name']) ?>
                    </option>
                    <?php endforeach; ?>
                </select>
            </div>
            <div>
                <label class="label">Sök deltagare</label>
                <input type="text" name="search" class="input" value="<?= h($search) ?>" placeholder="Namn..." style="width: 200px;">
            </div>
            <button type="submit" class="btn btn--primary">
                <i data-lucide="search"></i> Sök
            </button>
        </form>
    </div>
</div>

<?php if (empty($results) && ($eventId || $classFilter || $search)): ?>
<div class="card">
    <div class="card-body text-center py-xl">
        <i data-lucide="search-x" style="width:48px;height:48px;color:var(--color-text-secondary);"></i>
        <p class="text-secondary mt-md">Inga resultat hittades</p>
    </div>
</div>
<?php elseif (!empty($results)): ?>

<!-- Results Table -->
<div class="card">
    <div class="card-header flex justify-between items-center">
        <h2><?= count($results) ?> resultat</h2>
        <div class="flex gap-sm">
            <button type="button" class="btn btn--secondary btn--sm" onclick="selectAll()">Välj alla</button>
            <button type="button" class="btn btn--secondary btn--sm" onclick="deselectAll()">Avmarkera</button>
        </div>
    </div>
    <div class="card-body p-0">
        <div class="result-header result-row">
            <div><input type="checkbox" id="select-all-cb"></div>
            <div>Plats</div>
            <div>Deltagare</div>
            <div>Klass</div>
            <div>Byt till rider</div>
            <div></div>
        </div>

        <?php foreach ($results as $r): ?>
        <div class="result-row" data-result-id="<?= $r['result_id'] ?>" data-rider-id="<?= $r['cyclist_id'] ?>">
            <div>
                <input type="checkbox" class="result-cb" value="<?= $r['result_id'] ?>">
            </div>
            <div class="text-center">
                <strong><?= $r['position'] ?: '-' ?></strong>
            </div>
            <div class="rider-cell">
                <span class="rider-name"><?= h($r['firstname']) ?> <?= h($r['lastname']) ?></span>
                <span class="rider-meta">
                    <?= $r['license_number'] ? h($r['license_number']) : '<em>Ingen UCI</em>' ?>
                    <?php if ($r['club_name']): ?> · <?= h($r['club_name']) ?><?php endif; ?>
                </span>
            </div>
            <div>
                <select class="inline-select class-select" data-result-id="<?= $r['result_id'] ?>">
                    <?php foreach ($classes as $c): ?>
                    <option value="<?= $c['id'] ?>" <?= $r['class_id'] == $c['id'] ? 'selected' : '' ?>>
                        <?= h($c['display_name']) ?>
                    </option>
                    <?php endforeach; ?>
                </select>
            </div>
            <div class="search-rider-input">
                <input type="text"
                       class="input input-sm rider-search"
                       data-result-id="<?= $r['result_id'] ?>"
                       placeholder="Sök rider...">
                <div class="search-rider-results"></div>
            </div>
            <div>
                <button type="button" class="btn btn--ghost btn--xs" onclick="showMergeModal(<?= $r['cyclist_id'] ?>, '<?= h($r['firstname']) ?> <?= h($r['lastname']) ?>')">
                    <i data-lucide="git-merge"></i>
                </button>
            </div>
        </div>
        <?php endforeach; ?>
    </div>
</div>

<!-- Bulk Action Panel -->
<div class="action-panel" id="action-panel">
    <div class="flex items-center justify-between">
        <div>
            <strong><span id="selected-count">0</span> resultat valda</strong>
        </div>
        <div class="flex gap-sm items-center">
            <span>Byt klass till:</span>
            <select id="bulk-class" class="input" style="width: 200px;">
                <?php foreach ($classes as $c): ?>
                <option value="<?= $c['id'] ?>"><?= h($c['display_name']) ?></option>
                <?php endforeach; ?>
            </select>
            <button type="button" class="btn btn--primary" onclick="bulkChangeClass()">
                Byt klass
            </button>
        </div>
    </div>
</div>

<!-- Merge Modal -->
<div id="merge-modal" class="admin-modal" style="display:none; position:fixed; inset:0; background:rgba(0,0,0,0.5); z-index:200; padding:var(--space-md);">
    <div class="admin-modal-content" style="position:relative; margin:auto; background:var(--color-surface); padding:var(--space-lg); border-radius:var(--radius-md); width:100%; max-width:400px; max-height:90vh; overflow-y:auto;">
        <div class="admin-modal-header" style="display:flex; justify-content:space-between; align-items:center; margin-bottom:var(--space-md);">
            <h3>Slå ihop rider</h3>
            <button type="button" class="btn btn--ghost btn--sm admin-modal-close" onclick="closeMergeModal()" style="min-width:44px; min-height:44px;">
                <i data-lucide="x"></i>
            </button>
        </div>
        <div class="admin-modal-body">
            <p class="text-sm text-secondary mb-md">
                Slå ihop "<span id="merge-source-name"></span>" med en annan rider.
                Alla resultat flyttas till målridern.
            </p>
            <input type="hidden" id="merge-source-id">
            <div class="form-group mb-md">
                <label class="label">Sök målrider:</label>
                <input type="text" id="merge-target-search" class="input" placeholder="Sök namn...">
                <div id="merge-target-results" style="max-height:150px; overflow-y:auto; border:1px solid var(--color-border); border-radius:var(--radius-sm); margin-top:var(--space-xs); display:none;"></div>
            </div>
            <input type="hidden" id="merge-target-id">
        </div>
        <div class="admin-modal-footer" style="display:flex; gap:var(--space-sm); justify-content:flex-end; padding-top:var(--space-md); border-top:1px solid var(--color-border); margin-top:var(--space-md);">
            <button type="button" class="btn btn--secondary" onclick="closeMergeModal()">Avbryt</button>
            <button type="button" class="btn btn--danger" onclick="confirmMerge()">Slå ihop</button>
        </div>
    </div>
</div>

<script>
const csrfToken = '<?= csrf_token() ?>';

// Selection handling
document.getElementById('select-all-cb').addEventListener('change', function() {
    document.querySelectorAll('.result-cb').forEach(cb => cb.checked = this.checked);
    updateSelection();
});

document.querySelectorAll('.result-cb').forEach(cb => {
    cb.addEventListener('change', updateSelection);
});

function selectAll() {
    document.querySelectorAll('.result-cb').forEach(cb => cb.checked = true);
    document.getElementById('select-all-cb').checked = true;
    updateSelection();
}

function deselectAll() {
    document.querySelectorAll('.result-cb').forEach(cb => cb.checked = false);
    document.getElementById('select-all-cb').checked = false;
    updateSelection();
}

function updateSelection() {
    const count = document.querySelectorAll('.result-cb:checked').length;
    document.getElementById('selected-count').textContent = count;
    document.getElementById('action-panel').classList.toggle('active', count > 0);

    document.querySelectorAll('.result-row').forEach(row => {
        const cb = row.querySelector('.result-cb');
        if (cb) row.classList.toggle('selected', cb.checked);
    });
}

// Class change (single)
document.querySelectorAll('.class-select').forEach(select => {
    select.addEventListener('change', async function() {
        const resultId = this.dataset.resultId;
        const newClassId = this.value;

        const formData = new FormData();
        formData.append('ajax', '1');
        formData.append('action', 'change_class');
        formData.append('csrf_token', csrfToken);
        formData.append('result_id', resultId);
        formData.append('new_class_id', newClassId);

        const response = await fetch(location.href, { method: 'POST', body: formData });
        const result = await response.json();

        if (result.success) {
            this.style.borderColor = 'var(--color-success)';
            setTimeout(() => this.style.borderColor = '', 1000);
        }
    });
});

// Bulk class change
async function bulkChangeClass() {
    const resultIds = Array.from(document.querySelectorAll('.result-cb:checked')).map(cb => cb.value);
    const newClassId = document.getElementById('bulk-class').value;

    if (resultIds.length === 0) return;

    const formData = new FormData();
    formData.append('ajax', '1');
    formData.append('action', 'bulk_change_class');
    formData.append('csrf_token', csrfToken);
    formData.append('new_class_id', newClassId);
    resultIds.forEach(id => formData.append('result_ids[]', id));

    const response = await fetch(location.href, { method: 'POST', body: formData });
    const result = await response.json();

    if (result.success) {
        location.reload();
    }
}

// Rider search
let searchTimeout;
document.querySelectorAll('.rider-search').forEach(input => {
    const resultsDiv = input.nextElementSibling;

    input.addEventListener('input', function() {
        clearTimeout(searchTimeout);
        const query = this.value.trim();

        if (query.length < 2) {
            resultsDiv.classList.remove('active');
            return;
        }

        searchTimeout = setTimeout(async () => {
            const formData = new FormData();
            formData.append('ajax', '1');
            formData.append('action', 'search_riders');
            formData.append('csrf_token', csrfToken);
            formData.append('query', query);

            const response = await fetch(location.href, { method: 'POST', body: formData });
            const result = await response.json();

            resultsDiv.innerHTML = result.riders.map(r => `
                <div class="search-rider-item" data-rider-id="${r.id}">
                    <strong>${r.firstname} ${r.lastname}</strong>
                    <br><small>${r.license_number || 'Ingen UCI'} ${r.club_name ? '· ' + r.club_name : ''}</small>
                </div>
            `).join('');

            resultsDiv.classList.add('active');

            resultsDiv.querySelectorAll('.search-rider-item').forEach(item => {
                item.addEventListener('click', async () => {
                    const resultId = input.dataset.resultId;
                    const newRiderId = item.dataset.riderId;

                    const formData = new FormData();
                    formData.append('ajax', '1');
                    formData.append('action', 'change_rider');
                    formData.append('csrf_token', csrfToken);
                    formData.append('result_id', resultId);
                    formData.append('new_rider_id', newRiderId);

                    const response = await fetch(location.href, { method: 'POST', body: formData });
                    const res = await response.json();

                    if (res.success) {
                        location.reload();
                    }
                });
            });
        }, 300);
    });

    input.addEventListener('blur', () => {
        setTimeout(() => resultsDiv.classList.remove('active'), 200);
    });
});

// Merge modal
function showMergeModal(riderId, riderName) {
    document.getElementById('merge-source-id').value = riderId;
    document.getElementById('merge-source-name').textContent = riderName;
    document.getElementById('merge-modal').style.display = 'block';
}

function closeMergeModal() {
    document.getElementById('merge-modal').style.display = 'none';
    document.getElementById('merge-target-search').value = '';
    document.getElementById('merge-target-results').style.display = 'none';
    document.getElementById('merge-target-id').value = '';
}

document.getElementById('merge-target-search').addEventListener('input', async function() {
    const query = this.value.trim();
    const resultsDiv = document.getElementById('merge-target-results');

    if (query.length < 2) {
        resultsDiv.style.display = 'none';
        return;
    }

    const formData = new FormData();
    formData.append('ajax', '1');
    formData.append('action', 'search_riders');
    formData.append('csrf_token', csrfToken);
    formData.append('query', query);

    const response = await fetch(location.href, { method: 'POST', body: formData });
    const result = await response.json();

    resultsDiv.innerHTML = result.riders.map(r => `
        <div class="search-rider-item" data-rider-id="${r.id}" style="padding:8px; cursor:pointer;">
            <strong>${r.firstname} ${r.lastname}</strong>
            <br><small>${r.license_number || 'Ingen UCI'}</small>
        </div>
    `).join('');

    resultsDiv.style.display = 'block';

    resultsDiv.querySelectorAll('.search-rider-item').forEach(item => {
        item.addEventListener('click', function() {
            document.getElementById('merge-target-id').value = this.dataset.riderId;
            document.getElementById('merge-target-search').value = this.querySelector('strong').textContent;
            resultsDiv.style.display = 'none';
        });
    });
});

async function confirmMerge() {
    const sourceId = document.getElementById('merge-source-id').value;
    const targetId = document.getElementById('merge-target-id').value;

    if (!targetId) {
        alert('Välj en målrider först');
        return;
    }

    if (!confirm('Slå ihop dessa riders? Alla resultat flyttas till målridern och källridern raderas.')) {
        return;
    }

    const formData = new FormData();
    formData.append('ajax', '1');
    formData.append('action', 'merge_riders');
    formData.append('csrf_token', csrfToken);
    formData.append('source_id', sourceId);
    formData.append('target_id', targetId);

    const response = await fetch(location.href, { method: 'POST', body: formData });
    const result = await response.json();

    if (result.success) {
        closeMergeModal();
        location.reload();
    } else {
        alert('Fel: ' + result.error);
    }
}

if (typeof lucide !== 'undefined') lucide.createIcons();
</script>

<?php elseif (!$eventId && !$classFilter && !$search): ?>
<div class="card">
    <div class="card-body text-center py-xl">
        <i data-lucide="mouse-pointer-click" style="width:48px;height:48px;color:var(--color-text-secondary);"></i>
        <p class="text-secondary mt-md">Välj ett event eller sök för att visa resultat</p>
    </div>
</div>
<?php endif; ?>

<?php include __DIR__ . '/components/unified-layout-footer.php'; ?>
