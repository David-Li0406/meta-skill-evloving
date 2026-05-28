<?php
/**
 * Check License Numbers Tool
 * Find and fix invalid license numbers, convert to SWE ID format
 */
require_once __DIR__ . '/../config.php';
require_admin();

$db = getDB();
$message = '';
$messageType = '';

// Handle fix actions
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    checkCsrf();

    $action = $_POST['action'] ?? '';

    if ($action === 'fix_single') {
        $riderId = intval($_POST['rider_id']);
        $newLicense = trim($_POST['new_license'] ?? '');

        if ($newLicense) {
            try {
                $db->update('riders', ['license_number' => $newLicense], 'id = ?', [$riderId]);
                $message = 'Licensnummer uppdaterat!';
                $messageType = 'success';
            } catch (Exception $e) {
                $message = 'Fel: ' . $e->getMessage();
                $messageType = 'error';
            }
        }
    } elseif ($action === 'convert_to_swe') {
        $riderId = intval($_POST['rider_id']);
        $currentLicense = trim($_POST['current_license'] ?? '');

        // Generate SWE ID from license number
        $numbers = preg_replace('/[^0-9]/', '', $currentLicense);
        if (strlen($numbers) >= 8) {
            $sweId = 'SWE' . substr($numbers, 0, 11);
            try {
                $db->update('riders', ['license_number' => $sweId], 'id = ?', [$riderId]);
                $message = "Konverterat till: $sweId";
                $messageType = 'success';
            } catch (Exception $e) {
                $message = 'Fel: ' . $e->getMessage();
                $messageType = 'error';
            }
        } else {
            $message = 'Kunde inte konvertera - för få siffror';
            $messageType = 'error';
        }
    } elseif ($action === 'clear_license') {
        $riderId = intval($_POST['rider_id']);
        try {
            $db->update('riders', ['license_number' => null], 'id = ?', [$riderId]);
            $message = 'Licensnummer borttaget!';
            $messageType = 'success';
        } catch (Exception $e) {
            $message = 'Fel: ' . $e->getMessage();
            $messageType = 'error';
        }
    }
}

// Find riders with problematic license numbers
$filter = $_GET['filter'] ?? 'invalid';

// UCI license format: XXX XXX XXX XX (11 digits with spaces) e.g. "101 180 688 85"
// Also valid without spaces: 11 digits
$filterQueries = [
    'invalid' => "license_number IS NOT NULL AND license_number != ''
                  AND license_number NOT LIKE 'SWE%'
                  AND license_number NOT REGEXP '^[0-9]{11}$'
                  AND license_number NOT REGEXP '^[0-9]{3} [0-9]{3} [0-9]{3} [0-9]{2}$'",
    'numeric_only' => "license_number REGEXP '^[0-9]+$' AND LENGTH(license_number) >= 8 AND license_number NOT LIKE 'SWE%'",
    'short' => "license_number IS NOT NULL AND LENGTH(license_number) > 0 AND LENGTH(license_number) < 8",
    'has_spaces' => "license_number LIKE '% %' AND license_number NOT REGEXP '^[0-9]{3} [0-9]{3} [0-9]{3} [0-9]{2}$'",
    'uci_format' => "license_number REGEXP '^[0-9]{3} [0-9]{3} [0-9]{3} [0-9]{2}$'",
    'all' => "license_number IS NOT NULL AND license_number != ''"
];

$condition = $filterQueries[$filter] ?? $filterQueries['invalid'];

$riders = $db->getAll("
    SELECT r.*, c.name as club_name
    FROM riders r
    LEFT JOIN clubs c ON r.club_id = c.id
    WHERE $condition
    ORDER BY r.lastname, r.firstname
    LIMIT 100
");

// Stats
$stats = $db->getRow("
    SELECT
        COUNT(*) as total,
        SUM(CASE WHEN license_number LIKE 'SWE%' THEN 1 ELSE 0 END) as valid_swe,
        SUM(CASE WHEN license_number REGEXP '^[0-9]{11}$' THEN 1 ELSE 0 END) as valid_numeric,
        SUM(CASE WHEN license_number REGEXP '^[0-9]{3} [0-9]{3} [0-9]{3} [0-9]{2}$' THEN 1 ELSE 0 END) as valid_uci,
        SUM(CASE WHEN license_number IS NOT NULL AND license_number != ''
                 AND license_number NOT LIKE 'SWE%'
                 AND license_number NOT REGEXP '^[0-9]{11}$'
                 AND license_number NOT REGEXP '^[0-9]{3} [0-9]{3} [0-9]{3} [0-9]{2}$'
            THEN 1 ELSE 0 END) as invalid
    FROM riders
");

// Page config
$page_title = 'Kontrollera Licensnummer';
$breadcrumbs = [
    ['label' => 'Verktyg', 'url' => '/admin/tools.php'],
    ['label' => 'Kontrollera Licensnummer']
];

include __DIR__ . '/components/unified-layout.php';
?>

        <?php if ($message): ?>
        <div class="alert alert--<?= h($messageType) ?> mb-lg">
            <i data-lucide="<?= $messageType === 'success' ? 'check-circle' : 'alert-circle' ?>"></i>
            <?= h($message) ?>
        </div>
        <?php endif; ?>

        <!-- Stats -->
        <div class="grid grid-cols-5 gap-md mb-lg">
            <div class="card">
                <div class="card-body text-center">
                    <div class="text-2xl text-primary"><?= $stats['total'] ?? 0 ?></div>
                    <div class="text-sm text-secondary">Totalt deltagare</div>
                </div>
            </div>
            <div class="card">
                <div class="card-body text-center">
                    <div class="text-2xl text-success"><?= $stats['valid_swe'] ?? 0 ?></div>
                    <div class="text-sm text-secondary">Giltiga SWE ID</div>
                </div>
            </div>
            <div class="card">
                <div class="card-body text-center">
                    <div class="text-2xl text-success"><?= $stats['valid_uci'] ?? 0 ?></div>
                    <div class="text-sm text-secondary">Giltiga UCI</div>
                </div>
            </div>
            <div class="card">
                <div class="card-body text-center">
                    <div class="text-2xl text-success"><?= $stats['valid_numeric'] ?? 0 ?></div>
                    <div class="text-sm text-secondary">Giltiga numeriska</div>
                </div>
            </div>
            <div class="card">
                <div class="card-body text-center">
                    <div class="text-2xl text-error"><?= $stats['invalid'] ?? 0 ?></div>
                    <div class="text-sm text-secondary">Ogiltiga</div>
                </div>
            </div>
        </div>

        <!-- Info -->
        <div class="alert alert--info mb-lg">
            <i data-lucide="info"></i>
            <div>
                <strong>Giltiga format:</strong>
                <ul class="mt-sm" style="margin-left: 1.5rem; list-style: disc;">
                    <li><strong>SWE ID:</strong> SWE + 11 siffror (t.ex. SWE19850315001)</li>
                    <li><strong>UCI:</strong> 11 siffror med mellanslag (t.ex. 101 180 688 85)</li>
                    <li><strong>Numeriskt:</strong> Exakt 11 siffror (personnummer utan bindestreck)</li>
                </ul>
            </div>
        </div>

        <!-- Filter -->
        <div class="card mb-lg">
            <div class="card-body">
                <form method="GET" class="flex gap-md items-end">
                    <div>
                        <label class="label">
                            <i data-lucide="filter"></i>
                            Visa licensnummer som
                        </label>
                        <select name="filter" class="input" style="max-width: 300px;">
                            <option value="invalid" <?= $filter === 'invalid' ? 'selected' : '' ?>>Ogiltigt format</option>
                            <option value="numeric_only" <?= $filter === 'numeric_only' ? 'selected' : '' ?>>Numeriska (kan konverteras)</option>
                            <option value="short" <?= $filter === 'short' ? 'selected' : '' ?>>För korta (&lt; 8 tecken)</option>
                            <option value="has_spaces" <?= $filter === 'has_spaces' ? 'selected' : '' ?>>Mellanslag (ej UCI-format)</option>
                            <option value="uci_format" <?= $filter === 'uci_format' ? 'selected' : '' ?>>UCI-format</option>
                            <option value="all" <?= $filter === 'all' ? 'selected' : '' ?>>Alla med licensnummer</option>
                        </select>
                    </div>
                    <button type="submit" class="btn btn--primary">
                        <i data-lucide="filter"></i>
                        Filtrera
                    </button>
                </form>
            </div>
        </div>

        <!-- Results -->
        <div class="card">
            <div class="card-header">
                <h2>
                    <i data-lucide="list"></i>
                    Licensnummer att granska (<?= count($riders) ?>)
                </h2>
            </div>
            <div class="card-body">
                <?php if (empty($riders)): ?>
                <div class="text-center py-xl">
                    <i data-lucide="check-circle" style="width: 48px; height: 48px; color: var(--color-success);"></i>
                    <p class="text-secondary mt-md">Inga problematiska licensnummer hittades!</p>
                </div>
                <?php else: ?>
                <div class="table-responsive">
                    <table class="table">
                        <thead>
                            <tr>
                                <th>Namn</th>
                                <th>Nuvarande licensnummer</th>
                                <th>Klubb</th>
                                <th>Problem</th>
                                <th class="text-right">Åtgärder</th>
                            </tr>
                        </thead>
                        <tbody>
                            <?php foreach ($riders as $rider): ?>
                            <?php
                            $license = $rider['license_number'] ?? '';
                            $numbers = preg_replace('/[^0-9]/', '', $license);
                            $canConvert = strlen($numbers) >= 8;
                            $isSwe = strpos($license, 'SWE') === 0;
                            $isValidNumeric = preg_match('/^[0-9]{11}$/', $license);
                            $isValidUci = preg_match('/^[0-9]{3} [0-9]{3} [0-9]{3} [0-9]{2}$/', $license);
                            $isValid = $isSwe || $isValidNumeric || $isValidUci;

                            $problems = [];
                            if (strlen($license) < 8) $problems[] = 'För kort';
                            if (strpos($license, ' ') !== false && !$isValidUci) $problems[] = 'Mellanslag';
                            if (!$isValid && strlen($license) >= 8) $problems[] = 'Ogiltigt format';
                            ?>
                            <tr>
                                <td>
                                    <strong><?= h($rider['firstname'] . ' ' . $rider['lastname']) ?></strong>
                                    <br><small class="text-secondary">ID: <?= $rider['id'] ?></small>
                                </td>
                                <td>
                                    <code class="<?= $isValid ? 'text-success' : 'text-error' ?>"><?= h($license) ?></code>
                                </td>
                                <td>
                                    <?= h($rider['club_name'] ?? '-') ?>
                                </td>
                                <td>
                                    <?php foreach ($problems as $problem): ?>
                                    <span class="badge badge--warning"><?= h($problem) ?></span>
                                    <?php endforeach; ?>
                                    <?php if (empty($problems)): ?>
                                    <span class="badge badge--success">OK</span>
                                    <?php endif; ?>
                                </td>
                                <td class="text-right">
                                    <div class="flex gap-sm justify-end">
                                        <?php if ($canConvert && !$isSwe): ?>
                                        <form method="POST" style="display: inline;">
                                            <?= csrf_field() ?>
                                            <input type="hidden" name="action" value="convert_to_swe">
                                            <input type="hidden" name="rider_id" value="<?= $rider['id'] ?>">
                                            <input type="hidden" name="current_license" value="<?= h($license) ?>">
                                            <button type="submit" class="btn btn--success btn--sm" title="Konvertera till SWE<?= substr($numbers, 0, 11) ?>">
                                                <i data-lucide="refresh-cw"></i>
                                                SWE
                                            </button>
                                        </form>
                                        <?php endif; ?>
                                        <button type="button" class="btn btn--primary btn--sm" onclick="editLicense(<?= $rider['id'] ?>, '<?= addslashes(h($license)) ?>')">
                                            <i data-lucide="edit"></i>
                                        </button>
                                        <form method="POST" style="display: inline;" onsubmit="return confirm('Ta bort licensnummer?')">
                                            <?= csrf_field() ?>
                                            <input type="hidden" name="action" value="clear_license">
                                            <input type="hidden" name="rider_id" value="<?= $rider['id'] ?>">
                                            <button type="submit" class="btn btn--secondary btn--sm" title="Ta bort licensnummer">
                                                <i data-lucide="trash-2"></i>
                                            </button>
                                        </form>
                                    </div>
                                </td>
                            </tr>
                            <?php endforeach; ?>
                        </tbody>
                    </table>
                </div>
                <?php endif; ?>
            </div>
        </div>

<!-- Edit Modal -->
<div id="editModal" style="display: none; position: fixed; inset: 0; background: rgba(0,0,0,0.5); z-index: 1000; align-items: center; justify-content: center;">
    <div class="card" style="width: 100%; max-width: 400px; margin: 1rem;">
        <div class="card-header">
            <h3>Redigera licensnummer</h3>
        </div>
        <div class="card-body">
            <form id="editForm" method="POST">
                <?= csrf_field() ?>
                <input type="hidden" name="action" value="fix_single">
                <input type="hidden" name="rider_id" id="editRiderId">

                <div class="form-group mb-md">
                    <label class="label">Nytt licensnummer</label>
                    <input type="text" name="new_license" id="editLicense" class="input" placeholder="SWE19850315001">
                    <small class="text-secondary">Format: SWE + 11 siffror</small>
                </div>

                <div class="flex gap-md justify-end">
                    <button type="button" class="btn btn--secondary" onclick="closeModal()">Avbryt</button>
                    <button type="submit" class="btn btn--primary">Spara</button>
                </div>
            </form>
        </div>
    </div>
</div>

<script>
function editLicense(id, currentLicense) {
    document.getElementById('editRiderId').value = id;
    document.getElementById('editLicense').value = currentLicense;
    document.getElementById('editModal').style.display = 'flex';
}

function closeModal() {
    document.getElementById('editModal').style.display = 'none';
}

document.getElementById('editModal').addEventListener('click', function(e) {
    if (e.target === this) closeModal();
});
</script>

<?php include __DIR__ . '/components/unified-layout-footer.php'; ?>
