<?php
/**
 * Admin Point Scales - V3 Design System
 */
require_once __DIR__ . '/../config.php';
require_admin();

$db = getDB();
$message = '';
$messageType = 'info';

// Handle form submissions
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    checkCsrf();

    $action = $_POST['action'] ?? '';

    if ($action === 'create_scale') {
        $name = trim($_POST['name'] ?? '');
        $description = trim($_POST['description'] ?? '');
        $discipline = $_POST['discipline'] ?? 'ALL';
        $isDHScale = isset($_POST['is_dh_scale']) && $_POST['is_dh_scale'] == '1';

        if (empty($name)) {
            $message = 'Namn är obligatoriskt';
            $messageType = 'error';
        } else {
            try {
                // Insert scale
                $db->insert('point_scales', [
                    'name' => $name,
                    'description' => $description,
                    'discipline' => $discipline,
                    'active' => 1,
                    'is_default' => 0
                ]);

                $scaleId = $db->lastInsertId();

                // Insert point values
                $positions = $_POST['positions'] ?? [];
                $points = $_POST['points'] ?? [];
                $run1Points = $_POST['run_1_points'] ?? [];
                $run2Points = $_POST['run_2_points'] ?? [];

                foreach ($positions as $idx => $position) {
                    if (!empty($position)) {
                        $pointValue = !empty($points[$idx]) ? floatval($points[$idx]) : 0;
                        $run1Value = $isDHScale && !empty($run1Points[$idx]) ? floatval($run1Points[$idx]) : 0;
                        $run2Value = $isDHScale && !empty($run2Points[$idx]) ? floatval($run2Points[$idx]) : 0;

                        $db->insert('point_scale_values', [
                            'scale_id' => $scaleId,
                            'position' => intval($position),
                            'points' => $pointValue,
                            'run_1_points' => $run1Value,
                            'run_2_points' => $run2Value
                        ]);
                    }
                }

                set_flash('success', 'Poängmall skapad!');
                redirect('/admin/point-scales.php');
            } catch (Exception $e) {
                $message = 'Ett fel uppstod: ' . $e->getMessage();
                $messageType = 'error';
            }
        }
    }

    // Import from CSV
    if ($action === 'import_scale') {
        $name = trim($_POST['import_name'] ?? '');
        $discipline = $_POST['import_discipline'] ?? 'ALL';
        $isDHScale = isset($_POST['import_is_dh']) && $_POST['import_is_dh'] == '1';

        if (empty($name)) {
            $message = 'Namn är obligatoriskt';
            $messageType = 'error';
        } elseif (!isset($_FILES['import_file']) || $_FILES['import_file']['error'] !== UPLOAD_ERR_OK) {
            $message = 'Ingen fil uppladdad';
            $messageType = 'error';
        } else {
            try {
                $file = $_FILES['import_file']['tmp_name'];
                $handle = fopen($file, 'r');

                if (!$handle) {
                    throw new Exception('Kunde inte öppna filen');
                }

                // Auto-detect delimiter by reading first line
                $firstLine = fgets($handle);
                rewind($handle);
                $delimiter = (substr_count($firstLine, ';') > substr_count($firstLine, ',')) ? ';' : ',';

                // Read header row
                $header = fgetcsv($handle, 0, $delimiter);
                if (!$header) {
                    $header = [];
                }

                // Normalize header names
                $headerMap = [];
                foreach ($header as $idx => $col) {
                    $col = strtolower(trim($col));
                    $col = str_replace(['å', 'ä', 'ö'], ['a', 'a', 'o'], $col);
                    if (in_array($col, ['position', 'plac', 'placering', 'pos'])) {
                        $headerMap['position'] = $idx;
                    } elseif (in_array($col, ['poang', 'points', 'p'])) {
                        $headerMap['points'] = $idx;
                    } elseif (in_array($col, ['kval', 'run1', 'run_1', 'kval-poang', 'kvalpoang'])) {
                        $headerMap['run_1'] = $idx;
                    } elseif (in_array($col, ['final', 'run2', 'run_2', 'final-poang', 'finalpoang'])) {
                        $headerMap['run_2'] = $idx;
                    }
                }

                // Create scale
                $scaleId = $db->insert('point_scales', [
                    'name' => $name,
                    'description' => 'Importerad från CSV',
                    'discipline' => $discipline,
                    'active' => 1,
                    'is_default' => 0
                ]);

                // Read data rows
                $rowCount = 0;
                $rowNum = 1;
                while (($row = fgetcsv($handle, 0, $delimiter)) !== false) {
                    $rowNum++;

                    // Get position (required)
                    $position = isset($headerMap['position']) ? intval($row[$headerMap['position']] ?? 0) : $rowNum - 1;

                    if ($position <= 0) {
                        continue;
                    }

                    // Get points
                    $points = isset($headerMap['points']) ? floatval(str_replace(',', '.', $row[$headerMap['points']] ?? 0)) : 0;
                    $run1 = isset($headerMap['run_1']) ? floatval(str_replace(',', '.', $row[$headerMap['run_1']] ?? 0)) : 0;
                    $run2 = isset($headerMap['run_2']) ? floatval(str_replace(',', '.', $row[$headerMap['run_2']] ?? 0)) : 0;

                    // Skip empty rows
                    if ($points == 0 && $run1 == 0 && $run2 == 0) {
                        continue;
                    }

                    $db->insert('point_scale_values', [
                        'scale_id' => $scaleId,
                        'position' => $position,
                        'points' => $isDHScale ? 0 : $points,
                        'run_1_points' => $isDHScale ? $run1 : 0,
                        'run_2_points' => $isDHScale ? $run2 : 0
                    ]);
                    $rowCount++;
                }

                fclose($handle);

                set_flash('success', "Importerade poängmall '$name' med $rowCount positioner");
                redirect('/admin/point-scales.php');

            } catch (Exception $e) {
                $message = 'Importfel: ' . $e->getMessage();
                $messageType = 'error';
            }
        }
    }

    // Delete scale
    if ($action === 'delete_scale') {
        $scaleId = (int)($_POST['scale_id'] ?? 0);

        if ($scaleId) {
            try {
                // Check if scale is in use by any events
                $inUse = $db->getRow(
                    "SELECT COUNT(*) as cnt FROM events WHERE point_scale_id = ?",
                    [$scaleId]
                );

                if ($inUse && $inUse['cnt'] > 0) {
                    $message = "Kan inte ta bort poängmallen - den används av {$inUse['cnt']} event";
                    $messageType = 'error';
                } else {
                    // Delete scale values first
                    $db->delete('point_scale_values', 'scale_id = ?', [$scaleId]);
                    // Then delete the scale
                    $db->delete('point_scales', 'id = ?', [$scaleId]);

                    set_flash('success', 'Poängmall borttagen');
                    redirect('/admin/point-scales.php');
                }
            } catch (Exception $e) {
                $message = 'Fel vid borttagning: ' . $e->getMessage();
                $messageType = 'error';
            }
        }
    }

    // Set scale as default
    if ($action === 'set_default') {
        $scaleId = (int)($_POST['scale_id'] ?? 0);

        if ($scaleId) {
            try {
                // Remove default from all scales
                $db->update('point_scales', ['is_default' => 0], '1 = 1', []);
                // Set new default
                $db->update('point_scales', ['is_default' => 1], 'id = ?', [$scaleId]);

                set_flash('success', 'Standard poängmall uppdaterad');
                redirect('/admin/point-scales.php');
            } catch (Exception $e) {
                $message = 'Fel vid uppdatering: ' . $e->getMessage();
                $messageType = 'error';
            }
        }
    }
}

// Get all point scales with value counts
$scales = $db->getAll("
    SELECT
        ps.*,
        COUNT(psv.id) as value_count,
        MAX(psv.position) as max_position,
        SUM(CASE WHEN psv.run_1_points > 0 OR psv.run_2_points > 0 THEN 1 ELSE 0 END) as has_dh_points
    FROM point_scales ps
    LEFT JOIN point_scale_values psv ON ps.id = psv.scale_id
    GROUP BY ps.id
    ORDER BY ps.is_default DESC, ps.name ASC
");

// Page config for V3 admin layout
$page_title = 'Poängmallar';
$breadcrumbs = [
    ['label' => 'Serier', 'url' => '/admin/series'],
    ['label' => 'Poängmallar']
];

include __DIR__ . '/components/unified-layout.php';
?>

<style>
.scale-table {
    width: 100%;
    border-collapse: collapse;
}

.scale-table th,
.scale-table td {
    padding: var(--space-sm) var(--space-md);
    text-align: left;
    border-bottom: 1px solid var(--color-border);
}

.scale-table th {
    background: var(--color-bg-sunken);
    font-weight: 600;
    font-size: var(--text-xs);
    text-transform: uppercase;
    letter-spacing: 0.05em;
    color: var(--color-text-secondary);
}

.scale-table tbody tr:hover {
    background: var(--color-bg-hover);
}

.badge-default {
    background: var(--color-accent);
    color: white;
}

.badge-dh {
    background: #7C3AED;
    color: white;
}

.badge-active {
    background: var(--color-success);
    color: white;
}

.badge-inactive {
    background: var(--color-text-secondary);
    color: white;
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
    max-width: 800px;
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

.points-table-container {
    max-height: 400px;
    overflow-y: auto;
    border: 1px solid var(--color-border);
    border-radius: var(--radius-md);
}

.points-table {
    width: 100%;
    border-collapse: collapse;
}

.points-table th,
.points-table td {
    padding: var(--space-xs) var(--space-sm);
    border-bottom: 1px solid var(--color-border);
}

.points-table th {
    position: sticky;
    top: 0;
    background: var(--color-bg-sunken);
    font-weight: 600;
    font-size: var(--text-xs);
}

.hidden {
    display: none !important;
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

<!-- Info Box -->
<div class="alert alert-info mb-lg">
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <circle cx="12" cy="12" r="10"/><line x1="12" x2="12" y1="16" y2="12"/><line x1="12" x2="12.01" y1="8" y2="8"/>
    </svg>
    <strong>Tips:</strong> För SweCUP DH-format, markera "DH-mall med dubbla poäng" och fyll i både Kval och Final-poäng.
</div>

<!-- Actions -->
<div class="flex gap-sm justify-end mb-lg">
    <button type="button" class="btn-admin btn-admin-secondary" onclick="openImportModal()">
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="icon-sm"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="17 8 12 3 7 8"/><line x1="12" x2="12" y1="3" y2="15"/></svg>
        Importera CSV
    </button>
    <button type="button" class="btn-admin btn-admin-primary" onclick="openCreateModal()">
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="icon-sm"><line x1="12" x2="12" y1="5" y2="19"/><line x1="5" x2="19" y1="12" y2="12"/></svg>
        Ny Poängmall
    </button>
</div>

<!-- Point Scales Table -->
<div class="admin-card">
    <div class="admin-card-header">
        <h2>Poängmallar för Event</h2>
        <span class="text-secondary text-sm"><?= count($scales) ?> mallar</span>
    </div>
    <div class="admin-card-body p-0">
        <?php if (empty($scales)): ?>
            <div style="padding: var(--space-xl); text-align: center; color: var(--color-text-secondary);">
                <p>Inga poängmallar hittades.</p>
                <button type="button" class="btn-admin btn-admin-primary" onclick="openCreateModal()" class="mt-md">
                    Skapa första poängmallen
                </button>
            </div>
        <?php else: ?>
            <table class="scale-table">
                <thead>
                    <tr>
                        <th>Namn</th>
                        <th>Disciplin</th>
                        <th>Typ</th>
                        <th>Positioner</th>
                        <th>Status</th>
                        <th class="text-right">Åtgärder</th>
                    </tr>
                </thead>
                <tbody>
                    <?php foreach ($scales as $scale): ?>
                    <tr>
                        <td>
                            <strong><?= htmlspecialchars($scale['name']) ?></strong>
                            <?php if ($scale['is_default']): ?>
                                <span class="badge badge-default" style="margin-left: var(--space-xs);">Standard</span>
                            <?php endif; ?>
                            <?php if ($scale['description']): ?>
                                <br><small class="text-secondary"><?= htmlspecialchars($scale['description']) ?></small>
                            <?php endif; ?>
                        </td>
                        <td>
                            <span class="badge badge-secondary"><?= htmlspecialchars($scale['discipline']) ?></span>
                        </td>
                        <td>
                            <?php if ($scale['has_dh_points'] > 0): ?>
                                <span class="badge badge-dh">DH Dubbla Poäng</span>
                            <?php else: ?>
                                <span class="badge badge-secondary">Standard</span>
                            <?php endif; ?>
                        </td>
                        <td><?= $scale['value_count'] ?> (max P<?= $scale['max_position'] ?: 0 ?>)</td>
                        <td>
                            <?php if ($scale['active']): ?>
                                <span class="badge badge-active">Aktiv</span>
                            <?php else: ?>
                                <span class="badge badge-inactive">Inaktiv</span>
                            <?php endif; ?>
                        </td>
                        <td class="text-right">
                            <div class="flex gap-xs justify-end" style="flex-wrap: wrap;">
                                <a href="/admin/point-scale-edit.php?id=<?= $scale['id'] ?>" class="btn-admin btn-admin-sm btn-admin-secondary">
                                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="icon-xs"><path d="M17 3a2.85 2.83 0 1 1 4 4L7.5 20.5 2 22l1.5-5.5Z"/></svg>
                                    Redigera
                                </a>
                                <?php if (!$scale['is_default']): ?>
                                    <form method="POST" style="display: inline;">
                                        <?= csrf_field() ?>
                                        <input type="hidden" name="action" value="set_default">
                                        <input type="hidden" name="scale_id" value="<?= $scale['id'] ?>">
                                        <button type="submit" class="btn-admin btn-admin-sm btn-admin-secondary" title="Sätt som standard">
                                            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="icon-xs"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg>
                                        </button>
                                    </form>
                                <?php endif; ?>
                                <form method="POST" style="display: inline;" onsubmit="return confirm('Är du säker på att du vill ta bort poängmallen \'<?= htmlspecialchars($scale['name']) ?>\'?');">
                                    <?= csrf_field() ?>
                                    <input type="hidden" name="action" value="delete_scale">
                                    <input type="hidden" name="scale_id" value="<?= $scale['id'] ?>">
                                    <button type="submit" class="btn-admin btn-admin-sm btn-admin-danger">
                                        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="icon-xs"><path d="M3 6h18"/><path d="M19 6v14c0 1-1 2-2 2H7c-1 0-2-1-2-2V6"/><path d="M8 6V4c0-1 1-2 2-2h4c1 0 2 1 2 2v2"/></svg>
                                    </button>
                                </form>
                            </div>
                        </td>
                    </tr>
                    <?php endforeach; ?>
                </tbody>
            </table>
        <?php endif; ?>
    </div>
</div>

<!-- Link to Qualification Point Templates -->
<div class="admin-card mt-lg">
    <div class="admin-card-body">
        <div style="display: flex; align-items: center; justify-content: space-between;">
            <div>
                <h3 style="margin: 0 0 var(--space-xs) 0;">Kvalpoängmallar</h3>
                <p class="text-secondary text-sm" class="m-0">
                    Hantera poängmallar för seriekvalificering
                </p>
            </div>
            <a href="/admin/point-templates.php" class="btn-admin btn-admin-secondary">
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="icon-sm"><circle cx="12" cy="8" r="6"/><path d="M15.477 12.89 17 22l-5-3-5 3 1.523-9.11"/></svg>
                Hantera Kvalpoängmallar
            </a>
        </div>
    </div>
</div>

<!-- Create Scale Modal -->
<div id="createModal" class="modal-overlay">
    <div class="modal-content">
        <div class="modal-header">
            <h3>
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="icon-md"><line x1="12" x2="12" y1="5" y2="19"/><line x1="5" x2="19" y1="12" y2="12"/></svg>
                Skapa Ny Poängmall
            </h3>
            <button type="button" onclick="closeCreateModal()" class="btn-admin btn-admin-sm btn-admin-secondary">
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="icon-sm"><line x1="18" x2="6" y1="6" y2="18"/><line x1="6" x2="18" y1="6" y2="18"/></svg>
            </button>
        </div>

        <form method="POST" action="">
            <?= csrf_field() ?>
            <input type="hidden" name="action" value="create_scale">

            <div class="modal-body">
                <div class="grid-2-col mb-lg">
                    <div class="admin-form-group">
                        <label class="admin-form-label">Namn <span class="text-error">*</span></label>
                        <input type="text" name="name" class="admin-form-input" required>
                    </div>

                    <div class="admin-form-group">
                        <label class="admin-form-label">Disciplin</label>
                        <select name="discipline" class="admin-form-input">
                            <option value="ALL">Alla</option>
                            <option value="ENDURO">Enduro</option>
                            <option value="DH">Downhill</option>
                            <option value="XCO">XCO</option>
                            <option value="CX">Cyclocross</option>
                        </select>
                    </div>
                </div>

                <div class="admin-form-group mb-lg">
                    <label class="admin-form-label">Beskrivning</label>
                    <textarea name="description" class="admin-form-input" rows="2"></textarea>
                </div>

                <div class="admin-form-group mb-lg">
                    <label style="display: flex; align-items: center; gap: var(--space-sm); cursor: pointer;">
                        <input type="checkbox" name="is_dh_scale" value="1" id="isDHScale" onchange="toggleDHColumns()">
                        <span><strong>DH-mall med dubbla poäng</strong> (För SweCUP DH där både Kval och Final ger poäng)</span>
                    </label>
                </div>

                <div class="admin-form-group">
                    <label class="admin-form-label">Poängvärden</label>
                    <div class="points-table-container">
                        <table class="points-table">
                            <thead>
                                <tr>
                                    <th style="width: 80px;">Position</th>
                                    <th class="standard-points-col">Poäng</th>
                                    <th class="dh-points-col hidden">Kval-Poäng</th>
                                    <th class="dh-points-col hidden">Final-Poäng</th>
                                </tr>
                            </thead>
                            <tbody id="pointsTableBody">
                                <?php for ($i = 1; $i <= 50; $i++): ?>
                                <tr>
                                    <td>
                                        <input type="number" name="positions[]" value="<?= $i ?>" class="admin-form-input" readonly style="width: 60px; text-align: center;">
                                    </td>
                                    <td class="standard-points-col">
                                        <input type="number" name="points[]" step="0.01" class="admin-form-input" placeholder="0">
                                    </td>
                                    <td class="dh-points-col hidden">
                                        <input type="number" name="run_1_points[]" step="0.01" class="admin-form-input" placeholder="0">
                                    </td>
                                    <td class="dh-points-col hidden">
                                        <input type="number" name="run_2_points[]" step="0.01" class="admin-form-input" placeholder="0">
                                    </td>
                                </tr>
                                <?php endfor; ?>
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>

            <div class="modal-footer">
                <button type="button" onclick="closeCreateModal()" class="btn-admin btn-admin-secondary">
                    Avbryt
                </button>
                <button type="submit" class="btn-admin btn-admin-primary">
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="icon-sm"><path d="M19 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11l5 5v11a2 2 0 0 1-2 2z"/><polyline points="17 21 17 13 7 13 7 21"/><polyline points="7 3 7 8 15 8"/></svg>
                    Skapa Poängmall
                </button>
            </div>
        </form>
    </div>
</div>

<!-- Import Modal -->
<div id="importModal" class="modal-overlay">
    <div class="modal-content" style="max-width: 500px;">
        <div class="modal-header">
            <h3>
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="icon-md"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="17 8 12 3 7 8"/><line x1="12" x2="12" y1="3" y2="15"/></svg>
                Importera Poängmall från CSV
            </h3>
            <button type="button" onclick="closeImportModal()" class="btn-admin btn-admin-sm btn-admin-secondary">
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="icon-sm"><line x1="18" x2="6" y1="6" y2="18"/><line x1="6" x2="18" y1="6" y2="18"/></svg>
            </button>
        </div>
        <form method="POST" enctype="multipart/form-data">
            <?= csrf_field() ?>
            <input type="hidden" name="action" value="import_scale">

            <div class="modal-body">
                <div class="admin-form-group">
                    <label class="admin-form-label">Mallnamn *</label>
                    <input type="text" name="import_name" class="admin-form-input" required placeholder="Ex: SweCup Enduro 2025">
                </div>

                <div class="admin-form-group">
                    <label class="admin-form-label">Disciplin</label>
                    <select name="import_discipline" class="admin-form-input">
                        <option value="ALL">Alla</option>
                        <option value="ENDURO">Enduro</option>
                        <option value="DH">Downhill</option>
                        <option value="XCO">XCO</option>
                        <option value="CX">Cyclocross</option>
                    </select>
                </div>

                <div class="admin-form-group">
                    <label style="display: flex; align-items: center; gap: var(--space-sm); cursor: pointer;">
                        <input type="checkbox" name="import_is_dh" value="1">
                        <span><strong>DH-mall</strong> (använd Kval/Final kolumner)</span>
                    </label>
                </div>

                <div class="admin-form-group">
                    <label class="admin-form-label">CSV-fil *</label>
                    <input type="file" name="import_file" class="admin-form-input" accept=".csv,.txt" required>
                    <small style="color: var(--color-text-secondary); display: block; margin-top: var(--space-xs);">
                        Kolumner: Position;Poäng eller Position;Kval;Final (semikolon-separerad)
                    </small>
                </div>

                <div class="alert alert-info">
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <circle cx="12" cy="12" r="10"/><line x1="12" x2="12" y1="16" y2="12"/><line x1="12" x2="12.01" y1="8" y2="8"/>
                    </svg>
                    <div>
                        <strong>Exempelformat:</strong><br>
                        <code>Position;Poäng</code> eller <code>Position;Kval;Final</code>
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
function openCreateModal() {
    document.getElementById('createModal').classList.add('active');
}

function closeCreateModal() {
    document.getElementById('createModal').classList.remove('active');
}

function openImportModal() {
    document.getElementById('importModal').classList.add('active');
}

function closeImportModal() {
    document.getElementById('importModal').classList.remove('active');
}

function toggleDHColumns() {
    const isDH = document.getElementById('isDHScale').checked;
    const standardCols = document.querySelectorAll('.standard-points-col');
    const dhCols = document.querySelectorAll('.dh-points-col');

    standardCols.forEach(col => {
        if (isDH) {
            col.classList.add('hidden');
        } else {
            col.classList.remove('hidden');
        }
    });

    dhCols.forEach(col => {
        if (isDH) {
            col.classList.remove('hidden');
        } else {
            col.classList.add('hidden');
        }
    });
}

// Close modal on outside click
document.querySelectorAll('.modal-overlay').forEach(modal => {
    modal.addEventListener('click', function(e) {
        if (e.target === this) {
            this.classList.remove('active');
        }
    });
});

// Close modal on Escape key
document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape') {
        closeCreateModal();
        closeImportModal();
    }
});
</script>

<?php include __DIR__ . '/components/unified-layout-footer.php'; ?>
