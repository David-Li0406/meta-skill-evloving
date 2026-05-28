<?php
/**
 * Quick Edit Classes - Bulk operations for class management
 * Merge, rename, and manage 1000+ classes efficiently
 */
require_once __DIR__ . '/../config.php';
require_admin();

$db = getDB();
$message = '';
$messageType = 'info';

// Handle AJAX requests
if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['ajax'])) {
    header('Content-Type: application/json');
    checkCsrf();

    $action = $_POST['action'] ?? '';

    try {
        switch ($action) {
            case 'rename':
                $id = (int)$_POST['id'];
                $newName = trim($_POST['new_name']);
                $newDisplayName = trim($_POST['new_display_name'] ?? $newName);

                if (empty($newName)) {
                    echo json_encode(['success' => false, 'error' => 'Namn krävs']);
                    exit;
                }

                $db->update('classes', [
                    'name' => $newName,
                    'display_name' => $newDisplayName
                ], 'id = ?', [$id]);

                echo json_encode(['success' => true, 'message' => 'Klass uppdaterad']);
                exit;

            case 'merge':
                $sourceIds = $_POST['source_ids'] ?? [];
                $targetId = (int)$_POST['target_id'];

                if (empty($sourceIds) || !$targetId) {
                    echo json_encode(['success' => false, 'error' => 'Välj käll- och målklass']);
                    exit;
                }

                $sourceIds = array_map('intval', $sourceIds);
                $sourceIds = array_filter($sourceIds, fn($id) => $id !== $targetId);

                if (empty($sourceIds)) {
                    echo json_encode(['success' => false, 'error' => 'Inga klasser att slå ihop']);
                    exit;
                }

                // Update all results to use target class
                $placeholders = implode(',', array_fill(0, count($sourceIds), '?'));
                $db->execute(
                    "UPDATE results SET class_id = ? WHERE class_id IN ($placeholders)",
                    array_merge([$targetId], $sourceIds)
                );

                // Delete source classes
                $db->execute("DELETE FROM classes WHERE id IN ($placeholders)", $sourceIds);

                $count = count($sourceIds);
                echo json_encode(['success' => true, 'message' => "$count klasser sammanslagna"]);
                exit;

            case 'bulk_update':
                $updates = $_POST['updates'] ?? [];
                $count = 0;

                foreach ($updates as $update) {
                    $id = (int)($update['id'] ?? 0);
                    if ($id <= 0) continue;

                    $data = [];
                    if (isset($update['display_name'])) $data['display_name'] = trim($update['display_name']);
                    if (isset($update['gender'])) $data['gender'] = $update['gender'];
                    if (isset($update['sort_order'])) $data['sort_order'] = (int)$update['sort_order'];
                    if (isset($update['active'])) $data['active'] = (int)$update['active'];

                    if (!empty($data)) {
                        $db->update('classes', $data, 'id = ?', [$id]);
                        $count++;
                    }
                }

                echo json_encode(['success' => true, 'message' => "$count klasser uppdaterade"]);
                exit;

            case 'delete':
                $id = (int)$_POST['id'];

                // Check if class has results
                $resultCount = $db->getRow("SELECT COUNT(*) as cnt FROM results WHERE class_id = ?", [$id]);
                if ($resultCount['cnt'] > 0) {
                    echo json_encode(['success' => false, 'error' => "Klassen har {$resultCount['cnt']} resultat. Flytta eller ta bort dessa först."]);
                    exit;
                }

                $db->delete('classes', 'id = ?', [$id]);
                echo json_encode(['success' => true, 'message' => 'Klass borttagen']);
                exit;

            case 'create_alias':
                $classId = (int)$_POST['class_id'];
                $alias = trim($_POST['alias']);

                if (empty($alias)) {
                    echo json_encode(['success' => false, 'error' => 'Alias krävs']);
                    exit;
                }

                // Check if alias table exists, create if not
                try {
                    $db->execute("
                        CREATE TABLE IF NOT EXISTS class_aliases (
                            id INT AUTO_INCREMENT PRIMARY KEY,
                            class_id INT NOT NULL,
                            alias VARCHAR(255) NOT NULL,
                            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                            UNIQUE KEY unique_alias (alias),
                            FOREIGN KEY (class_id) REFERENCES classes(id) ON DELETE CASCADE
                        )
                    ");
                } catch (Exception $e) {
                    // Table might already exist
                }

                $db->insert('class_aliases', [
                    'class_id' => $classId,
                    'alias' => $alias
                ]);

                echo json_encode(['success' => true, 'message' => 'Alias skapat']);
                exit;

            default:
                echo json_encode(['success' => false, 'error' => 'Okänd action']);
                exit;
        }
    } catch (Exception $e) {
        echo json_encode(['success' => false, 'error' => $e->getMessage()]);
        exit;
    }
}

// Get all classes with result counts
$classes = $db->getAll("
    SELECT
        c.*,
        COUNT(DISTINCT r.id) as result_count,
        COUNT(DISTINCT r.event_id) as event_count
    FROM classes c
    LEFT JOIN results r ON c.id = r.class_id
    GROUP BY c.id
    ORDER BY c.sort_order ASC, c.display_name ASC
");

// Get aliases if table exists
$aliases = [];
try {
    $aliasRows = $db->getAll("SELECT * FROM class_aliases");
    foreach ($aliasRows as $row) {
        $aliases[$row['class_id']][] = $row['alias'];
    }
} catch (Exception $e) {
    // Table doesn't exist yet
}

// Group classes by gender for easier viewing
$classesByGender = [
    'M' => [],
    'F' => [],
    '' => []
];
foreach ($classes as $class) {
    $gender = $class['gender'] ?? '';
    $classesByGender[$gender][] = $class;
}

// Page config
$page_title = 'Snabbredigera Klasser';
$breadcrumbs = [
    ['label' => 'Klasser', 'url' => '/admin/classes.php'],
    ['label' => 'Snabbredigera']
];

include __DIR__ . '/components/unified-layout.php';
?>

<style>
.class-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
    gap: var(--space-sm);
}
.class-card {
    background: var(--color-surface);
    border: 1px solid var(--color-border);
    border-radius: var(--radius-sm);
    padding: var(--space-sm);
    position: relative;
}
.class-card.selected {
    border-color: var(--color-accent);
    background: rgba(97, 206, 112, 0.05);
}
.class-card.inactive {
    opacity: 0.6;
}
.class-name {
    font-weight: 600;
    font-size: 14px;
}
.class-meta {
    font-size: 12px;
    color: var(--color-text-secondary);
    margin-top: 4px;
}
.class-actions {
    position: absolute;
    top: var(--space-xs);
    right: var(--space-xs);
    display: flex;
    gap: 4px;
}
.class-checkbox {
    position: absolute;
    top: var(--space-sm);
    left: var(--space-sm);
}
.inline-edit {
    display: none;
    margin-top: var(--space-sm);
}
.inline-edit.active {
    display: block;
}
.merge-panel {
    position: fixed;
    bottom: 0;
    left: 0;
    right: 0;
    background: var(--color-surface);
    border-top: 2px solid var(--color-accent);
    padding: var(--space-md);
    display: none;
    z-index: 100;
    box-shadow: 0 -4px 20px rgba(0,0,0,0.15);
}
.merge-panel.active {
    display: block;
}
.gender-section {
    margin-bottom: var(--space-lg);
}
.gender-header {
    display: flex;
    align-items: center;
    gap: var(--space-sm);
    margin-bottom: var(--space-md);
    padding-bottom: var(--space-sm);
    border-bottom: 2px solid var(--color-border);
}
</style>

<!-- Toolbar -->
<div class="card mb-lg">
    <div class="card-body">
        <div class="flex flex-wrap gap-md items-center justify-between">
            <div class="flex gap-sm items-center">
                <input type="text" id="search-input" class="input" placeholder="Sök klasser..." style="width: 250px;">
                <select id="filter-gender" class="input" style="width: 120px;">
                    <option value="">Alla kön</option>
                    <option value="M">Herrar</option>
                    <option value="F">Damer</option>
                    <option value="none">Inget kön</option>
                </select>
                <label class="flex items-center gap-xs">
                    <input type="checkbox" id="show-empty" checked>
                    <span class="text-sm">Visa tomma</span>
                </label>
            </div>
            <div class="flex gap-sm">
                <button type="button" class="btn btn--secondary btn--sm" onclick="selectAll()">
                    <i data-lucide="check-square"></i> Välj alla synliga
                </button>
                <button type="button" class="btn btn--secondary btn--sm" onclick="deselectAll()">
                    <i data-lucide="square"></i> Avmarkera
                </button>
            </div>
        </div>
    </div>
</div>

<!-- Stats -->
<div class="grid grid-cols-4 gap-md mb-lg">
    <div class="card">
        <div class="card-body text-center">
            <div class="text-2xl font-bold"><?= count($classes) ?></div>
            <div class="text-sm text-secondary">Totalt klasser</div>
        </div>
    </div>
    <div class="card">
        <div class="card-body text-center">
            <div class="text-2xl font-bold"><?= count($classesByGender['M']) ?></div>
            <div class="text-sm text-secondary">Herrklasser</div>
        </div>
    </div>
    <div class="card">
        <div class="card-body text-center">
            <div class="text-2xl font-bold"><?= count($classesByGender['F']) ?></div>
            <div class="text-sm text-secondary">Damklasser</div>
        </div>
    </div>
    <div class="card">
        <div class="card-body text-center">
            <div class="text-2xl font-bold"><?= count(array_filter($classes, fn($c) => $c['result_count'] == 0)) ?></div>
            <div class="text-sm text-secondary">Utan resultat</div>
        </div>
    </div>
</div>

<!-- Classes by Gender -->
<?php
$genderLabels = ['M' => 'Herrar', 'F' => 'Damer', '' => 'Utan kön'];
$genderIcons = ['M' => 'user', 'F' => 'user', '' => 'users'];
?>

<?php foreach (['M', 'F', ''] as $gender): ?>
<?php if (count($classesByGender[$gender]) > 0): ?>
<div class="gender-section" data-gender="<?= $gender ?>">
    <div class="gender-header">
        <i data-lucide="<?= $genderIcons[$gender] ?>"></i>
        <h2><?= $genderLabels[$gender] ?></h2>
        <span class="badge badge--secondary"><?= count($classesByGender[$gender]) ?></span>
    </div>

    <div class="class-grid">
        <?php foreach ($classesByGender[$gender] as $class): ?>
        <div class="class-card <?= $class['active'] ? '' : 'inactive' ?>"
             data-id="<?= $class['id'] ?>"
             data-name="<?= h($class['name']) ?>"
             data-display="<?= h($class['display_name']) ?>"
             data-gender="<?= $class['gender'] ?>"
             data-results="<?= $class['result_count'] ?>">

            <input type="checkbox" class="class-checkbox" value="<?= $class['id'] ?>">

            <div class="class-actions">
                <button type="button" class="btn btn--ghost btn--xs" onclick="editClass(<?= $class['id'] ?>)" title="Redigera">
                    <i data-lucide="pencil"></i>
                </button>
                <?php if ($class['result_count'] == 0): ?>
                <button type="button" class="btn btn--ghost btn--xs text-danger" onclick="deleteClass(<?= $class['id'] ?>)" title="Ta bort">
                    <i data-lucide="trash-2"></i>
                </button>
                <?php endif; ?>
            </div>

            <div class="class-name" style="padding-left: 24px;">
                <?= h($class['display_name']) ?>
            </div>
            <div class="class-meta" style="padding-left: 24px;">
                <?= $class['result_count'] ?> resultat · <?= $class['event_count'] ?> events
                <?php if (!$class['active']): ?>
                <span class="badge badge--warning badge--xs">Inaktiv</span>
                <?php endif; ?>
            </div>

            <?php if (isset($aliases[$class['id']])): ?>
            <div class="class-meta" style="padding-left: 24px;">
                <i data-lucide="corner-down-right" style="width:12px;height:12px;"></i>
                Alias: <?= h(implode(', ', $aliases[$class['id']])) ?>
            </div>
            <?php endif; ?>

            <!-- Inline Edit Form -->
            <div class="inline-edit" id="edit-<?= $class['id'] ?>">
                <div class="flex gap-sm mb-sm">
                    <input type="text" class="input input-sm flex-1" id="name-<?= $class['id'] ?>" value="<?= h($class['display_name']) ?>" placeholder="Visningsnamn">
                </div>
                <div class="flex gap-sm mb-sm">
                    <select class="input input-sm" id="gender-<?= $class['id'] ?>">
                        <option value="" <?= $class['gender'] === '' ? 'selected' : '' ?>>Inget kön</option>
                        <option value="M" <?= $class['gender'] === 'M' ? 'selected' : '' ?>>Herrar</option>
                        <option value="F" <?= $class['gender'] === 'F' ? 'selected' : '' ?>>Damer</option>
                    </select>
                    <input type="number" class="input input-sm" id="order-<?= $class['id'] ?>" value="<?= $class['sort_order'] ?>" placeholder="Sortering" style="width:80px;">
                </div>
                <div class="flex gap-sm">
                    <button type="button" class="btn btn--primary btn--sm" onclick="saveClass(<?= $class['id'] ?>)">Spara</button>
                    <button type="button" class="btn btn--secondary btn--sm" onclick="cancelEdit(<?= $class['id'] ?>)">Avbryt</button>
                    <button type="button" class="btn btn--ghost btn--sm" onclick="addAlias(<?= $class['id'] ?>)">+ Alias</button>
                </div>
            </div>
        </div>
        <?php endforeach; ?>
    </div>
</div>
<?php endif; ?>
<?php endforeach; ?>

<!-- Merge Panel (sticky bottom) -->
<div class="merge-panel" id="merge-panel">
    <div class="flex items-center justify-between">
        <div>
            <strong><span id="selected-count">0</span> klasser valda</strong>
            <span class="text-secondary ml-md" id="selected-names"></span>
        </div>
        <div class="flex gap-sm">
            <select id="merge-target" class="input" style="width: 250px;">
                <option value="">-- Välj målklass --</option>
                <?php foreach ($classes as $class): ?>
                <option value="<?= $class['id'] ?>"><?= h($class['display_name']) ?> (<?= $class['result_count'] ?> res)</option>
                <?php endforeach; ?>
            </select>
            <button type="button" class="btn btn--primary" onclick="mergeClasses()">
                <i data-lucide="git-merge"></i>
                Slå ihop till vald
            </button>
            <button type="button" class="btn btn--danger" onclick="deleteSelected()">
                <i data-lucide="trash-2"></i>
                Ta bort tomma
            </button>
        </div>
    </div>
</div>

<script>
const csrfToken = '<?= csrf_token() ?>';

// Search and filter
document.getElementById('search-input').addEventListener('input', filterClasses);
document.getElementById('filter-gender').addEventListener('change', filterClasses);
document.getElementById('show-empty').addEventListener('change', filterClasses);

function filterClasses() {
    const search = document.getElementById('search-input').value.toLowerCase();
    const gender = document.getElementById('filter-gender').value;
    const showEmpty = document.getElementById('show-empty').checked;

    document.querySelectorAll('.class-card').forEach(card => {
        const name = card.dataset.name.toLowerCase();
        const display = card.dataset.display.toLowerCase();
        const cardGender = card.dataset.gender;
        const results = parseInt(card.dataset.results);

        let show = true;

        // Search filter
        if (search && !name.includes(search) && !display.includes(search)) {
            show = false;
        }

        // Gender filter
        if (gender === 'none' && cardGender !== '') show = false;
        else if (gender && gender !== 'none' && cardGender !== gender) show = false;

        // Empty filter
        if (!showEmpty && results === 0) show = false;

        card.style.display = show ? '' : 'none';
    });
}

// Selection
document.querySelectorAll('.class-checkbox').forEach(cb => {
    cb.addEventListener('change', updateSelection);
});

function updateSelection() {
    const checked = document.querySelectorAll('.class-checkbox:checked');
    const count = checked.length;

    document.getElementById('selected-count').textContent = count;

    const names = Array.from(checked).slice(0, 5).map(cb => {
        return cb.closest('.class-card').dataset.display;
    });
    if (count > 5) names.push(`+${count - 5} fler`);
    document.getElementById('selected-names').textContent = names.join(', ');

    // Show/hide merge panel
    document.getElementById('merge-panel').classList.toggle('active', count > 0);

    // Update card styling
    document.querySelectorAll('.class-card').forEach(card => {
        const cb = card.querySelector('.class-checkbox');
        card.classList.toggle('selected', cb.checked);
    });
}

function selectAll() {
    document.querySelectorAll('.class-card:not([style*="display: none"]) .class-checkbox').forEach(cb => {
        cb.checked = true;
    });
    updateSelection();
}

function deselectAll() {
    document.querySelectorAll('.class-checkbox').forEach(cb => cb.checked = false);
    updateSelection();
}

// Edit functions
function editClass(id) {
    document.querySelectorAll('.inline-edit').forEach(el => el.classList.remove('active'));
    document.getElementById('edit-' + id).classList.add('active');
}

function cancelEdit(id) {
    document.getElementById('edit-' + id).classList.remove('active');
}

async function saveClass(id) {
    const name = document.getElementById('name-' + id).value;
    const gender = document.getElementById('gender-' + id).value;
    const order = document.getElementById('order-' + id).value;

    const formData = new FormData();
    formData.append('ajax', '1');
    formData.append('action', 'bulk_update');
    formData.append('csrf_token', csrfToken);
    formData.append('updates[0][id]', id);
    formData.append('updates[0][display_name]', name);
    formData.append('updates[0][gender]', gender);
    formData.append('updates[0][sort_order]', order);

    const response = await fetch('/admin/quick-edit-classes.php', {
        method: 'POST',
        body: formData
    });

    const result = await response.json();
    if (result.success) {
        location.reload();
    } else {
        alert('Fel: ' + result.error);
    }
}

async function deleteClass(id) {
    if (!confirm('Ta bort denna klass?')) return;

    const formData = new FormData();
    formData.append('ajax', '1');
    formData.append('action', 'delete');
    formData.append('csrf_token', csrfToken);
    formData.append('id', id);

    const response = await fetch('/admin/quick-edit-classes.php', {
        method: 'POST',
        body: formData
    });

    const result = await response.json();
    if (result.success) {
        document.querySelector(`.class-card[data-id="${id}"]`).remove();
    } else {
        alert('Fel: ' + result.error);
    }
}

function addAlias(id) {
    const alias = prompt('Ange alias för denna klass (t.ex. "Men Elite", "H Elite"):');
    if (!alias) return;

    const formData = new FormData();
    formData.append('ajax', '1');
    formData.append('action', 'create_alias');
    formData.append('csrf_token', csrfToken);
    formData.append('class_id', id);
    formData.append('alias', alias);

    fetch('/admin/quick-edit-classes.php', {
        method: 'POST',
        body: formData
    })
    .then(r => r.json())
    .then(result => {
        if (result.success) {
            location.reload();
        } else {
            alert('Fel: ' + result.error);
        }
    });
}

// Merge functions
async function mergeClasses() {
    const targetId = document.getElementById('merge-target').value;
    if (!targetId) {
        alert('Välj en målklass först');
        return;
    }

    const sourceIds = Array.from(document.querySelectorAll('.class-checkbox:checked'))
        .map(cb => cb.value)
        .filter(id => id !== targetId);

    if (sourceIds.length === 0) {
        alert('Välj minst en klass att slå ihop');
        return;
    }

    const targetName = document.querySelector('#merge-target option:checked').textContent;
    if (!confirm(`Slå ihop ${sourceIds.length} klasser till "${targetName}"?\n\nAlla resultat flyttas till målklassen och källklasserna tas bort.`)) {
        return;
    }

    const formData = new FormData();
    formData.append('ajax', '1');
    formData.append('action', 'merge');
    formData.append('csrf_token', csrfToken);
    formData.append('target_id', targetId);
    sourceIds.forEach(id => formData.append('source_ids[]', id));

    const response = await fetch('/admin/quick-edit-classes.php', {
        method: 'POST',
        body: formData
    });

    const result = await response.json();
    if (result.success) {
        alert(result.message);
        location.reload();
    } else {
        alert('Fel: ' + result.error);
    }
}

async function deleteSelected() {
    const checked = document.querySelectorAll('.class-checkbox:checked');
    const emptyClasses = Array.from(checked).filter(cb => {
        const card = cb.closest('.class-card');
        return parseInt(card.dataset.results) === 0;
    });

    if (emptyClasses.length === 0) {
        alert('Inga tomma klasser valda');
        return;
    }

    if (!confirm(`Ta bort ${emptyClasses.length} tomma klasser?`)) return;

    for (const cb of emptyClasses) {
        const formData = new FormData();
        formData.append('ajax', '1');
        formData.append('action', 'delete');
        formData.append('csrf_token', csrfToken);
        formData.append('id', cb.value);

        await fetch('/admin/quick-edit-classes.php', {
            method: 'POST',
            body: formData
        });
    }

    location.reload();
}

// Initialize Lucide icons
if (typeof lucide !== 'undefined') {
    lucide.createIcons();
}
</script>

<?php include __DIR__ . '/components/unified-layout-footer.php'; ?>
