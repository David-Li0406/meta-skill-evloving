<?php
/**
 * Admin Point Scale Edit - V3 Design System
 */
require_once __DIR__ . '/../config.php';
require_admin();

$db = getDB();
$message = '';
$messageType = 'info';

// Get scale ID
$scaleId = isset($_GET['id']) ? intval($_GET['id']) : 0;

if (!$scaleId) {
    redirect('/admin/point-scales.php');
}

// Handle form submissions
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    checkCsrf();

    $action = $_POST['action'] ?? '';

    if ($action === 'update_scale') {
        $name = trim($_POST['name'] ?? '');
        $description = trim($_POST['description'] ?? '');
        $discipline = $_POST['discipline'] ?? 'ALL';
        $active = isset($_POST['active']) ? 1 : 0;
        $isDHScale = isset($_POST['is_dh_scale']) && $_POST['is_dh_scale'] == '1';

        if (empty($name)) {
            $message = 'Namn är obligatoriskt';
            $messageType = 'error';
        } else {
            try {
                // Update scale
                $db->update('point_scales', [
                    'name' => $name,
                    'description' => $description,
                    'discipline' => $discipline,
                    'active' => $active
                ], 'id = ?', [$scaleId]);

                // Delete existing values
                $db->delete('point_scale_values', 'scale_id = ?', [$scaleId]);

                // Insert new point values
                $positions = $_POST['positions'] ?? [];
                $points = $_POST['points'] ?? [];
                $run1Points = $_POST['run_1_points'] ?? [];
                $run2Points = $_POST['run_2_points'] ?? [];

                error_log("🔍 POINT SCALE SAVE: isDHScale={$isDHScale}, scaleId={$scaleId}");
                error_log("🔍 POST data: positions=" . count($positions) . ", points=" . count($points) . ", run1=" . count($run1Points) . ", run2=" . count($run2Points));

                $insertedCount = 0;
                foreach ($positions as $idx => $position) {
                    if (!empty($position)) {
                        $pointValue = !empty($points[$idx]) ? floatval($points[$idx]) : 0;
                        // Always save run_1/run_2 points if they have values, regardless of checkbox
                        $run1Value = !empty($run1Points[$idx]) ? floatval($run1Points[$idx]) : 0;
                        $run2Value = !empty($run2Points[$idx]) ? floatval($run2Points[$idx]) : 0;

                        // Only insert if at least one value is non-zero
                        if ($pointValue > 0 || $run1Value > 0 || $run2Value > 0) {
                            $db->insert('point_scale_values', [
                                'scale_id' => $scaleId,
                                'position' => intval($position),
                                'points' => $pointValue,
                                'run_1_points' => $run1Value,
                                'run_2_points' => $run2Value
                            ]);
                            $insertedCount++;
                            if ($insertedCount <= 5) {
                                error_log("🔍 Inserted pos={$position}: points={$pointValue}, run1={$run1Value}, run2={$run2Value}");
                            }
                        }
                    }
                }
                error_log("🔍 Total inserted: {$insertedCount} rows");

                set_flash('success', 'Poängmall uppdaterad!');
                redirect('/admin/point-scale-edit.php?id=' . $scaleId);
            } catch (Exception $e) {
                $message = 'Ett fel uppstod: ' . $e->getMessage();
                $messageType = 'error';
            }
        }
    }
}

// Get scale data
$scale = $db->getRow("SELECT * FROM point_scales WHERE id = ?", [$scaleId]);

if (!$scale) {
    redirect('/admin/point-scales.php');
}

// Get scale values
$values = $db->getAll("
    SELECT position, points, run_1_points, run_2_points
    FROM point_scale_values
    WHERE scale_id = ?
    ORDER BY position ASC
", [$scaleId]);

// Check if this is a DH scale
$isDHScale = false;
foreach ($values as $value) {
    if ($value['run_1_points'] > 0 || $value['run_2_points'] > 0) {
        $isDHScale = true;
        break;
    }
}

// Create indexed array for easier access
$valuesByPosition = [];
$maxPosition = 50; // Default
foreach ($values as $value) {
    $valuesByPosition[$value['position']] = $value;
    if ($value['position'] > $maxPosition) {
        $maxPosition = $value['position'];
    }
}
// Show at least 10 more empty rows than highest position
$maxPosition = max($maxPosition + 10, 60);

$pageTitle = 'Redigera Poängmall - ' . $scale['name'];
$pageType = 'admin';
include __DIR__ . '/components/unified-layout.php';
?>

<div class="container">
    <!-- Header -->
    <div class="flex items-center justify-between mb-lg">
        <div>
            <h1>
                <i data-lucide="edit-3"></i>
                Redigera Poängmall
            </h1>
            <p class="text-secondary"><?= h($scale['name']) ?></p>
        </div>
        <a href="/admin/point-scales.php" class="btn btn--secondary">
            <i data-lucide="arrow-left"></i>
            Tillbaka
        </a>
    </div>

    <?php if ($message): ?>
    <div class="alert alert-<?= $messageType ?> mb-lg">
        <i data-lucide="<?= $messageType === 'success' ? 'check-circle' : 'alert-circle' ?>"></i>
        <?= h($message) ?>
    </div>
    <?php endif; ?>

    <form method="POST" action="">
        <?= csrf_field() ?>
        <input type="hidden" name="action" value="update_scale">

        <!-- Settings Card -->
        <div class="card mb-lg">
            <div class="card-header">
                <h2><i data-lucide="settings"></i> Inställningar</h2>
            </div>
            <div class="card-body">
                <div class="grid grid-cols-1 lg-grid-cols-2 gap-md mb-md">
                    <div class="form-group">
                        <label class="label">Namn <span class="text-error">*</span></label>
                        <input type="text" name="name" class="input" value="<?= h($scale['name']) ?>" required>
                    </div>

                    <div class="form-group">
                        <label class="label">Disciplin</label>
                        <select name="discipline" class="input">
                            <option value="ALL" <?= $scale['discipline'] === 'ALL' ? 'selected' : '' ?>>Alla</option>
                            <option value="ENDURO" <?= $scale['discipline'] === 'ENDURO' ? 'selected' : '' ?>>Enduro</option>
                            <option value="DH" <?= $scale['discipline'] === 'DH' ? 'selected' : '' ?>>Downhill</option>
                            <option value="XCO" <?= $scale['discipline'] === 'XCO' ? 'selected' : '' ?>>XCO</option>
                            <option value="CX" <?= $scale['discipline'] === 'CX' ? 'selected' : '' ?>>Cyclocross</option>
                        </select>
                    </div>
                </div>

                <div class="form-group mb-md">
                    <label class="label">Beskrivning</label>
                    <textarea name="description" class="input" rows="2"><?= h($scale['description']) ?></textarea>
                </div>

                <div class="flex gap-lg">
                    <label class="checkbox">
                        <input type="checkbox" name="active" value="1" <?= $scale['active'] ? 'checked' : '' ?>>
                        <span>Aktiv</span>
                    </label>

                    <label class="checkbox">
                        <input type="checkbox" name="is_dh_scale" value="1" id="isDHScale" <?= $isDHScale ? 'checked' : '' ?>>
                        <span>DH-mall (Kval + Final)</span>
                    </label>
                </div>
            </div>
        </div>

        <!-- Points Card -->
        <div class="card mb-lg">
            <div class="card-header">
                <h2><i data-lucide="trophy"></i> Poängvärden</h2>
                <p class="text-secondary text-sm">Ange poäng per placering. Tomma fält sparas inte.</p>
            </div>
            <div class="card-body">
                <div class="table-wrapper">
                    <table class="table table--striped" id="pointsTable">
                        <thead>
                            <tr>
                                <th style="width: 80px;">Pos</th>
                                <th class="standard-col">Poäng</th>
                                <th class="dh-col hidden">Kval</th>
                                <th class="dh-col hidden">Final</th>
                            </tr>
                        </thead>
                        <tbody>
                            <?php for ($i = 1; $i <= $maxPosition; $i++): ?>
                            <?php
                            $posValue = $valuesByPosition[$i] ?? ['points' => '', 'run_1_points' => '', 'run_2_points' => ''];
                            $hasValue = !empty($posValue['points']) || !empty($posValue['run_1_points']) || !empty($posValue['run_2_points']);
                            ?>
                            <tr class="<?= $hasValue ? 'has-value' : '' ?>">
                                <td>
                                    <input type="hidden" name="positions[]" value="<?= $i ?>">
                                    <span class="badge <?= $i <= 3 ? 'badge--primary' : 'badge--secondary' ?>"><?= $i ?></span>
                                </td>
                                <td class="standard-col">
                                    <input type="number" name="points[]" step="0.01" class="input input--sm"
                                           value="<?= $posValue['points'] ? h($posValue['points']) : '' ?>"
                                           placeholder="0">
                                </td>
                                <td class="dh-col hidden">
                                    <input type="number" name="run_1_points[]" step="0.01" class="input input--sm"
                                           value="<?= $posValue['run_1_points'] ? h($posValue['run_1_points']) : '' ?>"
                                           placeholder="0">
                                </td>
                                <td class="dh-col hidden">
                                    <input type="number" name="run_2_points[]" step="0.01" class="input input--sm"
                                           value="<?= $posValue['run_2_points'] ? h($posValue['run_2_points']) : '' ?>"
                                           placeholder="0">
                                </td>
                            </tr>
                            <?php endfor; ?>
                        </tbody>
                    </table>
                </div>
            </div>
        </div>

        <!-- Footer Actions -->
        <div class="card">
            <div class="card-body flex justify-between items-center">
                <a href="/admin/point-scales.php" class="btn btn--secondary">
                    <i data-lucide="x"></i>
                    Avbryt
                </a>
                <button type="submit" class="btn btn--primary">
                    <i data-lucide="save"></i>
                    Spara Ändringar
                </button>
            </div>
        </div>
    </form>
</div>

<style>
/* Point Scale Edit Styles */
.has-value {
    background: var(--color-bg-success-subtle, rgba(97, 206, 112, 0.1)) !important;
}

.has-value td {
    border-color: var(--color-success, #61CE70) !important;
}

#pointsTable .input--sm {
    width: 100%;
    max-width: 120px;
    padding: var(--space-xs) var(--space-sm);
    font-size: var(--text-sm);
}

#pointsTable td {
    padding: var(--space-xs) var(--space-sm);
    vertical-align: middle;
}

#pointsTable .badge {
    min-width: 32px;
    text-align: center;
}

/* Responsive table wrapper */
.table-wrapper {
    max-height: 600px;
    overflow-y: auto;
    border: 1px solid var(--color-border);
    border-radius: var(--radius-md);
}

.table-wrapper thead {
    position: sticky;
    top: 0;
    background: var(--color-bg-surface);
    z-index: 10;
}

/* Hide/show columns based on DH mode */
.dh-mode .standard-col {
    display: none !important;
}

.dh-mode .dh-col {
    display: table-cell !important;
}
</style>

<script>
document.addEventListener('DOMContentLoaded', function() {
    const isDHCheckbox = document.getElementById('isDHScale');
    const table = document.getElementById('pointsTable');

    function toggleDHMode() {
        if (isDHCheckbox.checked) {
            table.classList.add('dh-mode');
        } else {
            table.classList.remove('dh-mode');
        }
    }

    // Initial state
    <?php if ($isDHScale): ?>
    table.classList.add('dh-mode');
    <?php endif; ?>

    isDHCheckbox.addEventListener('change', toggleDHMode);

    // Highlight rows with values on input
    document.querySelectorAll('#pointsTable input[type="number"]').forEach(input => {
        input.addEventListener('input', function() {
            const row = this.closest('tr');
            const inputs = row.querySelectorAll('input[type="number"]');
            let hasValue = false;
            inputs.forEach(inp => {
                if (inp.value && parseFloat(inp.value) > 0) hasValue = true;
            });
            row.classList.toggle('has-value', hasValue);
        });
    });
});
</script>

<?php include __DIR__ . '/components/unified-layout-footer.php'; ?>
