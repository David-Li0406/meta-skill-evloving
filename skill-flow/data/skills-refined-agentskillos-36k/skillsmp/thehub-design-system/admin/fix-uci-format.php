<?php
/**
 * Fix UCI-ID Format Tool
 * Converts UCI IDs to standard format: XXX XXX XXX XX
 * Based on normalize-names.php structure
 *
 * Note: normalizeUciId() is defined in includes/helpers.php
 */
require_once __DIR__ . '/../config.php';
require_admin();

$db = getDB();
$message = '';
$messageType = '';

/**
 * Check if UCI-ID needs normalization (not in XXX XXX XXX XX format)
 */
function needsNormalization($uciId) {
    if (empty($uciId)) return false;

    // Skip SWE licenses
    if (stripos($uciId, 'SWE') === 0) return false;

    // Check if already in correct format
    if (preg_match('/^[0-9]{3} [0-9]{3} [0-9]{3} [0-9]{2}$/', $uciId)) {
        return false;
    }

    // Check if it looks like a UCI-ID (10-11 digits)
    $digits = preg_replace('/[^0-9]/', '', $uciId);
    return strlen($digits) >= 10 && strlen($digits) <= 11;
}

// Handle form submission
if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['action'])) {
    checkCsrf();

    if ($_POST['action'] === 'normalize_selected' && isset($_POST['rider_ids']) && is_array($_POST['rider_ids'])) {
        $normalized = 0;
        $errors = 0;

        foreach ($_POST['rider_ids'] as $riderId) {
            $riderId = (int)$riderId;
            $rider = $db->getRow("SELECT id, license_number FROM riders WHERE id = ?", [$riderId]);

            if ($rider && !empty($rider['license_number'])) {
                $newLicense = normalizeUciId($rider['license_number']);

                if ($newLicense !== $rider['license_number']) {
                    try {
                        $db->query(
                            "UPDATE riders SET license_number = ?, updated_at = NOW() WHERE id = ?",
                            [$newLicense, $riderId]
                        );
                        $normalized++;
                    } catch (Exception $e) {
                        $errors++;
                    }
                }
            }
        }

        if ($normalized > 0) {
            $message = "Normaliserade $normalized UCI-ID" . ($errors > 0 ? " ($errors fel)" : "");
            $messageType = 'success';
        } else {
            $message = "Inga UCI-ID kunde normaliseras" . ($errors > 0 ? " ($errors fel)" : "");
            $messageType = 'warning';
        }
    }

    if ($_POST['action'] === 'normalize_all') {
        $normalized = 0;
        $errors = 0;

        // Get all riders that need normalization
        $riders = $db->getAll("
            SELECT id, license_number
            FROM riders
            WHERE license_number IS NOT NULL
              AND license_number != ''
              AND license_number NOT LIKE 'SWE%'
        ");

        foreach ($riders as $rider) {
            if (needsNormalization($rider['license_number'])) {
                $newLicense = normalizeUciId($rider['license_number']);

                if ($newLicense !== $rider['license_number']) {
                    try {
                        $db->query(
                            "UPDATE riders SET license_number = ?, updated_at = NOW() WHERE id = ?",
                            [$newLicense, $rider['id']]
                        );
                        $normalized++;
                    } catch (Exception $e) {
                        $errors++;
                    }
                }
            }
        }

        if ($normalized > 0) {
            $message = "Normaliserade $normalized UCI-ID" . ($errors > 0 ? " ($errors fel)" : "");
            $messageType = 'success';
        } else {
            $message = "Alla UCI-ID är redan korrekt formaterade";
            $messageType = 'info';
        }
    }
}

// Find riders with UCI-IDs that need normalization
$problematicRiders = $db->getAll("
    SELECT id, firstname, lastname, license_number, club_id
    FROM riders
    WHERE license_number IS NOT NULL
      AND license_number != ''
      AND license_number NOT LIKE 'SWE%'
      AND license_number NOT REGEXP '^[0-9]{3} [0-9]{3} [0-9]{3} [0-9]{2}$'
    ORDER BY lastname, firstname
    LIMIT 500
");

// Add preview data and filter to only UCI-like IDs
$filteredRiders = [];
foreach ($problematicRiders as $rider) {
    $digits = preg_replace('/[^0-9]/', '', $rider['license_number']);
    if (strlen($digits) >= 10 && strlen($digits) <= 11) {
        $rider['new_license'] = normalizeUciId($rider['license_number']);
        $rider['is_valid'] = strlen(preg_replace('/[^0-9]/', '', $rider['new_license'])) === 11;
        $filteredRiders[] = $rider;
    }
}
$problematicRiders = $filteredRiders;

// Get total count
$totalUciIds = $db->getRow("
    SELECT COUNT(*) as cnt FROM riders
    WHERE license_number IS NOT NULL
      AND license_number != ''
      AND license_number NOT LIKE 'SWE%'
")['cnt'] ?? 0;

// Get club names
$clubIds = array_unique(array_filter(array_column($problematicRiders, 'club_id')));
$clubs = [];
if (!empty($clubIds)) {
    $placeholders = implode(',', array_fill(0, count($clubIds), '?'));
    $clubRows = $db->getAll("SELECT id, name FROM clubs WHERE id IN ($placeholders)", $clubIds);
    foreach ($clubRows as $club) {
        $clubs[$club['id']] = $club['name'];
    }
}

// Page config
$page_title = 'Fixa UCI-ID Format';
$breadcrumbs = [
    ['label' => 'Verktyg', 'url' => '/admin/tools'],
    ['label' => 'Fixa UCI-ID Format']
];

include __DIR__ . '/components/unified-layout.php';
?>

<style>
.uci-preview {
    display: flex;
    align-items: center;
    gap: var(--space-sm);
}

.uci-old {
    font-family: var(--font-mono);
    color: var(--color-text-secondary);
    text-decoration: line-through;
}

.uci-new {
    font-family: var(--font-mono);
    color: var(--color-success);
    font-weight: 600;
    letter-spacing: 0.5px;
}

.uci-invalid {
    color: var(--color-warning);
}

.stats-row {
    display: flex;
    gap: var(--space-lg);
    margin-bottom: var(--space-lg);
    padding: var(--space-md);
    background: var(--color-bg-muted);
    border-radius: var(--radius-md);
}

.stat-item {
    text-align: center;
}

.stat-value {
    font-size: var(--text-2xl);
    font-weight: 700;
    color: var(--color-text-primary);
}

.stat-value.warning {
    color: var(--color-warning);
}

.stat-label {
    font-size: var(--text-sm);
    color: var(--color-text-secondary);
}

.action-bar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: var(--space-md);
    padding: var(--space-md);
    background: var(--color-bg-surface);
    border: 1px solid var(--color-border);
    border-radius: var(--radius-md);
}

.action-bar-left {
    display: flex;
    align-items: center;
    gap: var(--space-md);
}

.select-all-label {
    display: flex;
    align-items: center;
    gap: var(--space-sm);
    cursor: pointer;
}

.badge-count {
    background: var(--color-accent);
    color: white;
    padding: 2px 8px;
    border-radius: var(--radius-full);
    font-size: var(--text-xs);
    font-weight: 600;
}

.uci-table {
    width: 100%;
    border-collapse: collapse;
}

.uci-table th,
.uci-table td {
    padding: var(--space-sm) var(--space-md);
    text-align: left;
    border-bottom: 1px solid var(--color-border);
}

.uci-table th {
    background: var(--color-bg-muted);
    font-weight: 600;
    font-size: var(--text-sm);
}

.uci-table tr:hover {
    background: var(--color-bg-hover);
}

.uci-table td.checkbox-cell {
    width: 40px;
}

.club-name {
    font-size: var(--text-sm);
    color: var(--color-text-secondary);
}

.empty-state {
    text-align: center;
    padding: var(--space-2xl);
    color: var(--color-text-secondary);
}

.empty-state svg {
    width: 64px;
    height: 64px;
    margin-bottom: var(--space-md);
    color: var(--color-success);
}

.btn-normalize-all {
    background: var(--color-warning);
    color: white;
}

.btn-normalize-all:hover {
    background: #d97706;
}
</style>

<?php if ($message): ?>
<div class="alert alert-<?= $messageType ?>">
    <?= htmlspecialchars($message) ?>
</div>
<?php endif; ?>

<div class="card">
    <div class="card-header">
        <h2>
            <i data-lucide="hash"></i>
            Normalisera UCI-ID format
        </h2>
    </div>
    <div class="card-body">
        <p style="margin-bottom: var(--space-md); color: var(--color-text-secondary);">
            Detta verktyg hittar UCI-ID som inte är korrekt formaterade och konverterar dem till standardformat
            <code style="background: var(--color-bg-sunken); padding: 2px 6px; border-radius: 4px;">XXX XXX XXX XX</code>
            (t.ex. "10011107086" blir "100 111 070 86").
        </p>

        <div class="stats-row">
            <div class="stat-item">
                <div class="stat-value <?= count($problematicRiders) > 0 ? 'warning' : '' ?>">
                    <?= count($problematicRiders) ?>
                </div>
                <div class="stat-label">Behöver normaliseras</div>
            </div>
            <div class="stat-item">
                <div class="stat-value"><?= number_format($totalUciIds) ?></div>
                <div class="stat-label">Totalt UCI-ID</div>
            </div>
        </div>

        <?php if (empty($problematicRiders)): ?>
        <div class="empty-state">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/>
                <polyline points="22 4 12 14.01 9 11.01"/>
            </svg>
            <h3>Alla UCI-ID är korrekt formaterade!</h3>
            <p>Det finns inga UCI-ID som behöver normaliseras till format XXX XXX XXX XX.</p>
        </div>
        <?php else: ?>

        <form method="POST" id="normalize-form">
            <?= csrf_field() ?>
            <input type="hidden" name="action" value="normalize_selected" id="form-action">

            <div class="action-bar">
                <div class="action-bar-left">
                    <label class="select-all-label">
                        <input type="checkbox" id="select-all">
                        <span>Markera alla</span>
                    </label>
                    <span class="badge-count" id="selected-count">0 valda</span>
                </div>
                <div style="display: flex; gap: var(--space-sm);">
                    <button type="submit" class="btn-admin btn-admin-primary" id="normalize-selected-btn" disabled>
                        <i data-lucide="check"></i>
                        Normalisera valda
                    </button>
                    <button type="button" class="btn-admin btn-normalize-all" onclick="normalizeAll()">
                        <i data-lucide="refresh-cw"></i>
                        Normalisera alla (<?= count($problematicRiders) ?>)
                    </button>
                </div>
            </div>

            <div class="table-responsive">
                <table class="uci-table">
                    <thead>
                        <tr>
                            <th class="checkbox-cell"></th>
                            <th>Deltagare</th>
                            <th>Nuvarande UCI-ID</th>
                            <th>Nytt format</th>
                            <th>Klubb</th>
                        </tr>
                    </thead>
                    <tbody>
                        <?php foreach ($problematicRiders as $rider): ?>
                        <tr>
                            <td class="checkbox-cell">
                                <input type="checkbox" name="rider_ids[]" value="<?= $rider['id'] ?>" class="rider-checkbox">
                            </td>
                            <td>
                                <a href="/admin/riders/edit/<?= $rider['id'] ?>">
                                    <?= htmlspecialchars($rider['firstname'] . ' ' . $rider['lastname']) ?>
                                </a>
                            </td>
                            <td>
                                <span class="uci-old"><?= htmlspecialchars($rider['license_number']) ?></span>
                            </td>
                            <td>
                                <span class="uci-new <?= !$rider['is_valid'] ? 'uci-invalid' : '' ?>">
                                    <?= htmlspecialchars($rider['new_license']) ?>
                                </span>
                                <?php if (!$rider['is_valid']): ?>
                                <span style="color: var(--color-warning); font-size: var(--text-xs);">(ogiltigt)</span>
                                <?php endif; ?>
                            </td>
                            <td>
                                <span class="club-name">
                                    <?= htmlspecialchars($clubs[$rider['club_id']] ?? '-') ?>
                                </span>
                            </td>
                        </tr>
                        <?php endforeach; ?>
                    </tbody>
                </table>
            </div>
        </form>

        <?php endif; ?>
    </div>
</div>

<script>
document.addEventListener('DOMContentLoaded', function() {
    const selectAll = document.getElementById('select-all');
    const checkboxes = document.querySelectorAll('.rider-checkbox');
    const selectedCount = document.getElementById('selected-count');
    const normalizeBtn = document.getElementById('normalize-selected-btn');

    function updateCount() {
        const checked = document.querySelectorAll('.rider-checkbox:checked').length;
        selectedCount.textContent = checked + ' valda';
        if (normalizeBtn) normalizeBtn.disabled = checked === 0;
    }

    if (selectAll) {
        selectAll.addEventListener('change', function() {
            checkboxes.forEach(cb => cb.checked = this.checked);
            updateCount();
        });
    }

    checkboxes.forEach(cb => {
        cb.addEventListener('change', function() {
            if (selectAll) {
                selectAll.checked = document.querySelectorAll('.rider-checkbox:checked').length === checkboxes.length;
            }
            updateCount();
        });
    });

    // Initialize Lucide icons
    if (typeof lucide !== 'undefined') {
        lucide.createIcons();
    }
});

function normalizeAll() {
    if (confirm('Är du säker på att du vill normalisera alla <?= count($problematicRiders) ?> UCI-ID?')) {
        document.getElementById('form-action').value = 'normalize_all';
        document.getElementById('normalize-form').submit();
    }
}
</script>

<?php include __DIR__ . '/components/unified-layout-footer.php'; ?>
