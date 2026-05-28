<?php
/**
 * Admin Point Templates - V3 Design System
 * Qualification point templates for series
 */
require_once __DIR__ . '/../config.php';
require_admin();

$db = getDB();
$current_admin = get_current_admin();

$message = '';
$messageType = 'info';

// Handle form submissions
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    checkCsrf();

    $action = $_POST['action'] ?? '';

    if ($action === 'create' || $action === 'update') {
        $name = trim($_POST['name'] ?? '');
        $description = trim($_POST['description'] ?? '');
        $pointsData = $_POST['points'] ?? [];

        if (empty($name)) {
            $message = 'Namn är obligatoriskt';
            $messageType = 'error';
        } else {
            // Convert points array to JSON
            // Format: position => points
            $points = [];
            foreach ($pointsData as $position => $pointValue) {
                if (!empty($pointValue) && is_numeric($pointValue)) {
                    $points[$position] = (int)$pointValue;
                }
            }

            $templateData = [
                'name' => $name,
                'description' => $description,
                'points' => json_encode($points),
                'active' => 1
            ];

            try {
                if ($action === 'create') {
                    $db->insert('qualification_point_templates', $templateData);
                    set_flash('success', 'Kvalpoängmall skapad!');
                    redirect('/admin/point-templates.php');
                } else {
                    $id = intval($_POST['id']);
                    $db->update('qualification_point_templates', $templateData, 'id = ?', [$id]);
                    set_flash('success', 'Kvalpoängmall uppdaterad!');
                    redirect('/admin/point-templates.php');
                }
            } catch (Exception $e) {
                $message = 'Ett fel uppstod: ' . $e->getMessage();
                $messageType = 'error';
            }
        }
    } elseif ($action === 'delete') {
        $id = intval($_POST['id']);
        try {
            $db->delete('qualification_point_templates', 'id = ?', [$id]);
            set_flash('success', 'Kvalpoängmall borttagen!');
            redirect('/admin/point-templates.php');
        } catch (Exception $e) {
            $message = 'Ett fel uppstod: ' . $e->getMessage();
            $messageType = 'error';
        }
    } elseif ($action === 'import') {
        $importData = trim($_POST['import_data'] ?? '');

        if (empty($importData)) {
            $message = "Ingen data att importera.";
            $messageType = 'error';
        } else {
            try {
                // Remove UTF-8 BOM if present
                $importData = preg_replace('/^\xEF\xBB\xBF/', '', $importData);

                // Try to parse as JSON first
                $imported = json_decode($importData, true);

                if (json_last_error() !== JSON_ERROR_NONE) {
                    // Try CSV format: position,points (one per line)
                    $lines = explode("\n", $importData);
                    $imported = ['points' => []];

                    foreach ($lines as $line) {
                        $line = trim($line);
                        if (empty($line) || strpos($line, '#') === 0) continue; // Skip empty and comments

                        // Try comma first, then semicolon (Swedish Excel uses semicolon)
                        $delimiter = strpos($line, ';') !== false ? ';' : ',';
                        $parts = array_map('trim', explode($delimiter, $line));

                        if (count($parts) >= 2 && is_numeric($parts[0]) && is_numeric($parts[1])) {
                            $imported['points'][(int)$parts[0]] = (int)$parts[1];
                        }
                    }
                }

                if (!empty($imported['points'])) {
                    $templateData = [
                        'name' => $imported['name'] ?? 'Importerad mall ' . date('Y-m-d H:i'),
                        'description' => $imported['description'] ?? 'Importerad poängmall',
                        'points' => json_encode($imported['points']),
                        'active' => 1
                    ];

                    $db->insert('qualification_point_templates', $templateData);
                    set_flash('success', 'Kvalpoängmall importerad! (' . count($imported['points']) . ' positioner)');
                    redirect('/admin/point-templates.php');
                } else {
                    $message = "Kunde inte tolka importerad data. Kontrollera formatet (position,poäng eller position;poäng per rad).";
                    $messageType = 'error';
                }
            } catch (Exception $e) {
                $message = 'Import misslyckades: ' . $e->getMessage();
                $messageType = 'error';
            }
        }
    }
}

// Check if editing a template
$editTemplate = null;
if (isset($_GET['edit']) && is_numeric($_GET['edit'])) {
    $editTemplate = $db->getRow("SELECT * FROM qualification_point_templates WHERE id = ?", [intval($_GET['edit'])]);
    if ($editTemplate) {
        $editTemplate['points'] = json_decode($editTemplate['points'], true);
    }
}

// Get all templates
$templates = $db->getAll("SELECT * FROM qualification_point_templates ORDER BY name");

// Page config for V3 admin layout
$page_title = 'Kvalpoängmallar';
$breadcrumbs = [
    ['label' => 'Serier', 'url' => '/admin/series'],
    ['label' => 'Poängmallar', 'url' => '/admin/point-scales.php'],
    ['label' => 'Kvalpoängmallar']
];

include __DIR__ . '/components/unified-layout.php';
?>

<style>
.template-card {
    background: var(--color-bg-sunken);
    border-radius: var(--radius-md);
    padding: var(--space-md);
    margin-bottom: var(--space-md);
}

.template-card:last-child {
    margin-bottom: 0;
}

.template-header {
    display: flex;
    align-items: flex-start;
    justify-content: space-between;
    margin-bottom: var(--space-sm);
}

.template-points {
    display: flex;
    flex-wrap: wrap;
    gap: var(--space-xs);
    margin-top: var(--space-sm);
}

.point-badge {
    background: var(--color-bg-surface);
    padding: 2px 8px;
    border-radius: var(--radius-sm);
    font-size: var(--text-xs);
    font-family: monospace;
}

/* Modal styles */
.modal-overlay {
    display: none;
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(0, 0, 0, 0.5);
    z-index: 1000;
    align-items: center;
    justify-content: center;
    padding: var(--space-lg);
}

.modal-overlay.active {
    display: flex;
}

.modal-content {
    background: var(--color-bg-surface);
    border-radius: var(--radius-lg);
    max-width: 600px;
    width: 100%;
    max-height: 90vh;
    overflow: hidden;
    display: flex;
    flex-direction: column;
}

.modal-header {
    padding: var(--space-lg);
    border-bottom: 1px solid var(--color-border);
    display: flex;
    align-items: center;
    justify-content: space-between;
}

.modal-header h3 {
    margin: 0;
    display: flex;
    align-items: center;
    gap: var(--space-sm);
}

.modal-body {
    padding: var(--space-lg);
    overflow-y: auto;
    flex: 1;
}

.modal-footer {
    padding: var(--space-lg);
    border-top: 1px solid var(--color-border);
    display: flex;
    justify-content: flex-end;
    gap: var(--space-sm);
}

.points-container {
    max-height: 400px;
    overflow-y: auto;
    padding-right: var(--space-sm);
}

.point-row {
    display: flex;
    align-items: center;
    gap: var(--space-sm);
    margin-bottom: var(--space-xs);
}

.point-row label {
    width: 80px;
    font-size: var(--text-sm);
    color: var(--color-text-secondary);
}

.point-row input {
    flex: 1;
}
</style>

<?php if ($message): ?>
<div class="alert alert-<?= $messageType === 'success' ? 'success' : ($messageType === 'error' ? 'danger' : 'info') ?> mb-lg">
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <?php if ($messageType === 'success'): ?>
            <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/>
        <?php elseif ($messageType === 'error'): ?>
            <circle cx="12" cy="12" r="10"/><line x1="15" y1="9" x2="9" y2="15"/><line x1="9" y1="9" x2="15" y2="15"/>
        <?php else: ?>
            <circle cx="12" cy="12" r="10"/><line x1="12" x2="12" y1="8" y2="12"/><line x1="12" x2="12.01" y1="16" y2="16"/>
        <?php endif; ?>
    </svg>
    <?= htmlspecialchars($message) ?>
</div>
<?php endif; ?>

<!-- Actions -->
<div class="mb-lg" style="display: flex; justify-content: space-between; align-items: center;">
    <a href="/admin/point-scales.php" class="btn-admin btn-admin-secondary">
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="icon-sm"><path d="m12 19-7-7 7-7"/><path d="M19 12H5"/></svg>
        Tillbaka till Poängmallar
    </a>
    <div class="flex gap-sm">
        <button type="button" class="btn-admin btn-admin-secondary" onclick="openImportModal()">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="icon-sm"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="17 8 12 3 7 8"/><line x1="12" x2="12" y1="3" y2="15"/></svg>
            Importera
        </button>
        <button type="button" class="btn-admin btn-admin-primary" onclick="openTemplateModal()">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="icon-sm"><line x1="12" x2="12" y1="5" y2="19"/><line x1="5" x2="19" y1="12" y2="12"/></svg>
            Ny Mall
        </button>
    </div>
</div>

<!-- Templates List -->
<div class="admin-card">
    <div class="admin-card-header">
        <h2>Kvalpoängmallar för Serier</h2>
        <span class="text-secondary text-sm"><?= count($templates) ?> mallar</span>
    </div>
    <div class="admin-card-body">
        <?php if (empty($templates)): ?>
            <div class="text-secondary" style="text-align: center; padding: var(--space-xl);">
                <p>Inga kvalpoängmallar hittades.</p>
                <button type="button" class="btn-admin btn-admin-primary mt-lg" onclick="openTemplateModal()">
                    Skapa första kvalpoängmallen
                </button>
            </div>
        <?php else: ?>
            <?php foreach ($templates as $template): ?>
                <?php $points = json_decode($template['points'], true); ?>
                <div class="template-card">
                    <div class="template-header">
                        <div>
                            <h3 style="margin: 0 0 var(--space-xs) 0;"><?= htmlspecialchars($template['name']) ?></h3>
                            <?php if (!empty($template['description'])): ?>
                                <p class="text-secondary text-sm" class="m-0"><?= htmlspecialchars($template['description']) ?></p>
                            <?php endif; ?>
                        </div>
                        <div style="display: flex; gap: var(--space-xs);">
                            <button type="button" class="btn-admin btn-admin-sm btn-admin-secondary" onclick="exportTemplate(<?= $template['id'] ?>)" title="Exportera">
                                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="icon-xs"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" x2="12" y1="15" y2="3"/></svg>
                            </button>
                            <a href="?edit=<?= $template['id'] ?>" class="btn-admin btn-admin-sm btn-admin-secondary" title="Redigera">
                                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="icon-xs"><path d="M17 3a2.85 2.83 0 1 1 4 4L7.5 20.5 2 22l1.5-5.5Z"/></svg>
                            </a>
                            <form method="POST" style="display: inline;" onsubmit="return confirm('Är du säker på att du vill ta bort \'<?= htmlspecialchars($template['name']) ?>\'?');">
                                <?= csrf_field() ?>
                                <input type="hidden" name="action" value="delete">
                                <input type="hidden" name="id" value="<?= $template['id'] ?>">
                                <button type="submit" class="btn-admin btn-admin-sm btn-admin-danger" title="Ta bort">
                                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="icon-xs"><path d="M3 6h18"/><path d="M19 6v14c0 1-1 2-2 2H7c-1 0-2-1-2-2V6"/><path d="M8 6V4c0-1 1-2 2-2h4c1 0 2 1 2 2v2"/></svg>
                                </button>
                            </form>
                        </div>
                    </div>

                    <?php if (!empty($points)): ?>
                        <div class="template-points">
                            <?php foreach ($points as $position => $pointValue): ?>
                                <span class="point-badge">#<?= $position ?>: <?= $pointValue ?>p</span>
                            <?php endforeach; ?>
                        </div>
                    <?php else: ?>
                        <p class="text-secondary text-sm" class="m-0">Ingen poängfördelning angiven</p>
                    <?php endif; ?>
                </div>
            <?php endforeach; ?>
        <?php endif; ?>
    </div>
</div>

<!-- Create/Edit Template Modal -->
<div id="templateModal" class="modal-overlay">
    <div class="modal-content">
        <div class="modal-header">
            <h3>
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="icon-md"><circle cx="12" cy="8" r="6"/><path d="M15.477 12.89 17 22l-5-3-5 3 1.523-9.11"/></svg>
                <span id="modalTitleText">Ny Kvalpoängmall</span>
            </h3>
            <button type="button" onclick="closeTemplateModal()" class="btn-admin btn-admin-sm btn-admin-secondary">
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="icon-sm"><line x1="18" x2="6" y1="6" y2="18"/><line x1="6" x2="18" y1="6" y2="18"/></svg>
            </button>
        </div>
        <form method="POST" id="templateForm">
            <?= csrf_field() ?>
            <input type="hidden" name="action" id="formAction" value="create">
            <input type="hidden" name="id" id="templateId" value="">

            <div class="modal-body">
                <div class="admin-form-group">
                    <label class="admin-form-label">Namn <span class="text-error">*</span></label>
                    <input type="text" id="templateName" name="name" class="admin-form-input" required>
                </div>

                <div class="admin-form-group">
                    <label class="admin-form-label">Beskrivning</label>
                    <textarea id="templateDescription" name="description" class="admin-form-input" rows="2"></textarea>
                </div>

                <div class="admin-form-group">
                    <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: var(--space-sm);">
                        <label class="admin-form-label" class="m-0">Poängfördelning per placering</label>
                        <button type="button" class="btn-admin btn-admin-sm btn-admin-secondary" onclick="addPointRow()">
                            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="width: 12px; height: 12px;"><line x1="12" x2="12" y1="5" y2="19"/><line x1="5" x2="19" y1="12" y2="12"/></svg>
                            Lägg till rad
                        </button>
                    </div>
                    <div id="pointsContainer" class="points-container">
                        <!-- Rows will be added dynamically -->
                    </div>
                </div>
            </div>

            <div class="modal-footer">
                <button type="button" onclick="closeTemplateModal()" class="btn-admin btn-admin-secondary">
                    Avbryt
                </button>
                <button type="submit" class="btn-admin btn-admin-primary">
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="icon-sm"><polyline points="20 6 9 17 4 12"/></svg>
                    <span id="submitButtonText">Skapa</span>
                </button>
            </div>
        </form>
    </div>
</div>

<!-- Import Modal -->
<div id="importModal" class="modal-overlay">
    <div class="modal-content">
        <div class="modal-header">
            <h3>
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="icon-md"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="17 8 12 3 7 8"/><line x1="12" x2="12" y1="3" y2="15"/></svg>
                Importera Kvalpoängmall
            </h3>
            <button type="button" onclick="closeImportModal()" class="btn-admin btn-admin-sm btn-admin-secondary">
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="icon-sm"><line x1="18" x2="6" y1="6" y2="18"/><line x1="6" x2="18" y1="6" y2="18"/></svg>
            </button>
        </div>
        <form method="POST">
            <?= csrf_field() ?>
            <input type="hidden" name="action" value="import">

            <div class="modal-body">
                <div class="admin-form-group">
                    <label class="admin-form-label">Importera data (JSON eller CSV)</label>
                    <textarea name="import_data" class="admin-form-input" rows="12" placeholder='JSON format:
{
  "name": "Min mall",
  "description": "Beskrivning",
  "points": {
    "1": 100,
    "2": 80,
    "3": 60
  }
}

CSV format:
1,100
2,80
3,60'></textarea>
                </div>

                <div class="alert alert-info">
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <circle cx="12" cy="12" r="10"/><line x1="12" x2="12" y1="16" y2="12"/><line x1="12" x2="12.01" y1="8" y2="8"/>
                    </svg>
                    <div>
                        <p style="margin: 0 0 var(--space-xs) 0;"><strong>JSON format:</strong> Klistra in exporterad JSON-data</p>
                        <p class="m-0"><strong>CSV format:</strong> En rad per placering: placering,poäng</p>
                    </div>
                </div>
            </div>

            <div class="modal-footer">
                <button type="button" onclick="closeImportModal()" class="btn-admin btn-admin-secondary">
                    Avbryt
                </button>
                <button type="submit" class="btn-admin btn-admin-primary">
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="icon-sm"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="17 8 12 3 7 8"/><line x1="12" x2="12" y1="3" y2="15"/></svg>
                    Importera
                </button>
            </div>
        </form>
    </div>
</div>

<script>
let pointRowCounter = 0;
const templates = <?= json_encode($templates) ?>;

function openTemplateModal() {
    document.getElementById('templateModal').classList.add('active');
    document.getElementById('templateForm').reset();
    document.getElementById('formAction').value = 'create';
    document.getElementById('templateId').value = '';
    document.getElementById('modalTitleText').textContent = 'Ny Kvalpoängmall';
    document.getElementById('submitButtonText').textContent = 'Skapa';

    // Reset points container and add initial rows
    document.getElementById('pointsContainer').innerHTML = '';
    pointRowCounter = 0;
    for (let i = 1; i <= 10; i++) {
        addPointRow(i, '');
    }
}

function closeTemplateModal() {
    document.getElementById('templateModal').classList.remove('active');
}

function openImportModal() {
    document.getElementById('importModal').classList.add('active');
}

function closeImportModal() {
    document.getElementById('importModal').classList.remove('active');
}

function addPointRow(position = null, points = '') {
    const container = document.getElementById('pointsContainer');
    const nextPosition = position || (pointRowCounter + 1);
    pointRowCounter = Math.max(pointRowCounter, nextPosition);

    const row = document.createElement('div');
    row.className = 'point-row';
    row.innerHTML = `
        <label>Plats #${nextPosition}</label>
        <input type="number" name="points[${nextPosition}]" class="admin-form-input" value="${points}" min="0" placeholder="Poäng">
        <button type="button" class="btn-admin btn-admin-sm btn-admin-danger" onclick="this.parentElement.remove()">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="width: 12px; height: 12px;"><line x1="18" x2="6" y1="6" y2="18"/><line x1="6" x2="18" y1="6" y2="18"/></svg>
        </button>
    `;
    container.appendChild(row);
}

function exportTemplate(id) {
    const template = templates.find(t => t.id == id);
    if (!template) return;

    const exportData = {
        name: template.name,
        description: template.description || '',
        points: JSON.parse(template.points)
    };

    const dataStr = JSON.stringify(exportData, null, 2);
    const blob = new Blob([dataStr], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `kvalpoangmall_${template.name.replace(/[^a-z0-9]/gi, '_').toLowerCase()}.json`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
}

// Handle edit mode
<?php if ($editTemplate): ?>
document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('formAction').value = 'update';
    document.getElementById('templateId').value = '<?= $editTemplate['id'] ?>';
    document.getElementById('templateName').value = '<?= addslashes($editTemplate['name']) ?>';
    document.getElementById('templateDescription').value = '<?= addslashes($editTemplate['description'] ?? '') ?>';

    // Reset and populate points
    document.getElementById('pointsContainer').innerHTML = '';
    pointRowCounter = 0;

    const editPoints = <?= json_encode($editTemplate['points'] ?? []) ?>;
    const positions = Object.keys(editPoints).map(Number).sort((a, b) => a - b);

    positions.forEach(position => {
        addPointRow(position, editPoints[position]);
    });

    // Add a few empty rows
    for (let i = 0; i < 3; i++) {
        addPointRow();
    }

    document.getElementById('modalTitleText').textContent = 'Redigera Kvalpoängmall';
    document.getElementById('submitButtonText').textContent = 'Uppdatera';
    document.getElementById('templateModal').classList.add('active');
});
<?php endif; ?>

// Close modal on outside click
document.querySelectorAll('.modal-overlay').forEach(modal => {
    modal.addEventListener('click', function(e) {
        if (e.target === this) {
            this.classList.remove('active');
        }
    });
});

// Close modal with Escape key
document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape') {
        closeTemplateModal();
        closeImportModal();
    }
});
</script>

<?php include __DIR__ . '/components/unified-layout-footer.php'; ?>
