<?php
/**
 * Fix SWE-ID Format Tool
 * Converts old SWE-ID formats (SWE-03.235) to new format (SWE25xxxxx)
 */
require_once __DIR__ . '/../config.php';
require_admin();

$db = getDB();
$message = '';
$messageType = '';

/**
 * Parse old SWE-ID format and extract year/number
 * Handles: SWE-03.235, SWE03235, SWE-2003-235, etc.
 */
function parseOldSweId($sweId) {
    // Remove whitespace
    $sweId = trim($sweId);

    // Pattern 1: SWE-YY.NNN or SWE-YY.NNNN (e.g., SWE-03.235)
    if (preg_match('/^SWE-(\d{2})\.(\d+)$/i', $sweId, $m)) {
        return ['year' => $m[1], 'number' => $m[2]];
    }

    // Pattern 2: SWE-YYYY-NNNNN (e.g., SWE-2003-00235)
    if (preg_match('/^SWE-(\d{4})-(\d+)$/i', $sweId, $m)) {
        return ['year' => substr($m[1], -2), 'number' => $m[2]];
    }

    // Pattern 3: SWEYYNNN without separators (e.g., SWE03235)
    if (preg_match('/^SWE(\d{2})(\d{3,5})$/i', $sweId, $m)) {
        // Already in new format - check if it needs padding
        return ['year' => $m[1], 'number' => $m[2]];
    }

    return null;
}

/**
 * Convert to new SWE-ID format: SWEYYnnnnn (e.g., SWE2500001)
 */
function convertToNewSweFormat($sweId) {
    $parsed = parseOldSweId($sweId);
    if (!$parsed) {
        return $sweId; // Return unchanged if can't parse
    }

    $year = $parsed['year'];
    $number = ltrim($parsed['number'], '0') ?: '1'; // Remove leading zeros, default to 1

    return sprintf('SWE%s%05d', $year, (int)$number);
}

/**
 * Check if SWE-ID needs conversion
 */
function needsSweConversion($licenseNumber) {
    if (empty($licenseNumber)) return false;

    // Must start with SWE
    if (stripos($licenseNumber, 'SWE') !== 0) return false;

    // Already in correct format: SWEYYnnnnn (10 chars, SWE + 2 digit year + 5 digit number)
    if (preg_match('/^SWE\d{7}$/i', $licenseNumber)) {
        return false;
    }

    // Check for old formats
    // SWE-YY.NNN
    if (preg_match('/^SWE-\d{2}\.\d+$/i', $licenseNumber)) return true;
    // SWE-YYYY-NNNNN
    if (preg_match('/^SWE-\d{4}-\d+$/i', $licenseNumber)) return true;
    // SWEYYnnn (too short, needs padding)
    if (preg_match('/^SWE\d{2}\d{1,4}$/i', $licenseNumber)) return true;

    return false;
}

// Handle form submission
if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['action'])) {
    checkCsrf();

    if ($_POST['action'] === 'convert_selected' && isset($_POST['rider_ids']) && is_array($_POST['rider_ids'])) {
        $converted = 0;
        $errors = 0;

        foreach ($_POST['rider_ids'] as $riderId) {
            $riderId = (int)$riderId;
            $rider = $db->getRow("SELECT id, license_number FROM riders WHERE id = ?", [$riderId]);

            if ($rider && !empty($rider['license_number'])) {
                $newLicense = convertToNewSweFormat($rider['license_number']);

                if ($newLicense !== $rider['license_number']) {
                    try {
                        $db->query(
                            "UPDATE riders SET license_number = ?, updated_at = NOW() WHERE id = ?",
                            [$newLicense, $riderId]
                        );
                        $converted++;
                    } catch (Exception $e) {
                        $errors++;
                    }
                }
            }
        }

        if ($converted > 0) {
            $message = "Konverterade $converted SWE-ID" . ($errors > 0 ? " ($errors fel)" : "");
            $messageType = 'success';
        } else {
            $message = "Inga SWE-ID kunde konverteras" . ($errors > 0 ? " ($errors fel)" : "");
            $messageType = 'warning';
        }
    }

    if ($_POST['action'] === 'convert_all') {
        $converted = 0;
        $errors = 0;

        $riders = $db->getAll("
            SELECT id, license_number
            FROM riders
            WHERE license_number LIKE 'SWE%'
        ");

        foreach ($riders as $rider) {
            if (needsSweConversion($rider['license_number'])) {
                $newLicense = convertToNewSweFormat($rider['license_number']);

                if ($newLicense !== $rider['license_number']) {
                    try {
                        $db->query(
                            "UPDATE riders SET license_number = ?, updated_at = NOW() WHERE id = ?",
                            [$newLicense, $rider['id']]
                        );
                        $converted++;
                    } catch (Exception $e) {
                        $errors++;
                    }
                }
            }
        }

        if ($converted > 0) {
            $message = "Konverterade $converted SWE-ID" . ($errors > 0 ? " ($errors fel)" : "");
            $messageType = 'success';
        } else {
            $message = "Alla SWE-ID är redan i korrekt format";
            $messageType = 'info';
        }
    }
}

// Find riders with old SWE-ID format
$problematicRiders = [];
$allSweRiders = $db->getAll("
    SELECT id, firstname, lastname, license_number, club_id
    FROM riders
    WHERE license_number LIKE 'SWE%'
    ORDER BY lastname, firstname
");

foreach ($allSweRiders as $rider) {
    if (needsSweConversion($rider['license_number'])) {
        $rider['new_license'] = convertToNewSweFormat($rider['license_number']);
        $problematicRiders[] = $rider;
    }
}

// Get total SWE-ID count
$totalSweIds = $db->getRow("
    SELECT COUNT(*) as cnt FROM riders
    WHERE license_number LIKE 'SWE%'
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
$page_title = 'Konvertera SWE-ID Format';
$breadcrumbs = [
    ['label' => 'Verktyg', 'url' => '/admin/tools'],
    ['label' => 'Konvertera SWE-ID']
];

include __DIR__ . '/components/unified-layout.php';
?>

<style>
.swe-preview {
    display: flex;
    align-items: center;
    gap: var(--space-sm);
}

.swe-old {
    font-family: var(--font-mono);
    color: var(--color-text-secondary);
    text-decoration: line-through;
}

.swe-new {
    font-family: var(--font-mono);
    color: var(--color-success);
    font-weight: 600;
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

.swe-table {
    width: 100%;
    border-collapse: collapse;
}

.swe-table th,
.swe-table td {
    padding: var(--space-sm) var(--space-md);
    text-align: left;
    border-bottom: 1px solid var(--color-border);
}

.swe-table th {
    background: var(--color-bg-muted);
    font-weight: 600;
    font-size: var(--text-sm);
}

.swe-table tr:hover {
    background: var(--color-bg-hover);
}

.swe-table td.checkbox-cell {
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

.btn-convert-all {
    background: var(--color-warning);
    color: white;
}

.btn-convert-all:hover {
    background: #d97706;
}

.format-examples {
    background: var(--color-bg-sunken);
    padding: var(--space-md);
    border-radius: var(--radius-md);
    margin-bottom: var(--space-lg);
    font-size: var(--text-sm);
}

.format-examples code {
    background: var(--color-bg-surface);
    padding: 2px 6px;
    border-radius: 4px;
    font-family: var(--font-mono);
}

.format-arrow {
    color: var(--color-success);
    margin: 0 var(--space-sm);
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
            <i data-lucide="replace"></i>
            Konvertera SWE-ID till nytt format
        </h2>
    </div>
    <div class="card-body">
        <p style="margin-bottom: var(--space-md); color: var(--color-text-secondary);">
            Detta verktyg konverterar gamla SWE-ID format till det nya standardformatet <code>SWEYYnnnnn</code>.
        </p>

        <div class="format-examples">
            <strong>Formatkonvertering:</strong><br>
            <code>SWE-03.235</code> <span class="format-arrow">&rarr;</span> <code>SWE0300235</code><br>
            <code>SWE-2024-00123</code> <span class="format-arrow">&rarr;</span> <code>SWE2400123</code><br>
            <code>SWE2512</code> <span class="format-arrow">&rarr;</span> <code>SWE2500012</code>
        </div>

        <div class="stats-row">
            <div class="stat-item">
                <div class="stat-value <?= count($problematicRiders) > 0 ? 'warning' : '' ?>">
                    <?= count($problematicRiders) ?>
                </div>
                <div class="stat-label">Behöver konverteras</div>
            </div>
            <div class="stat-item">
                <div class="stat-value"><?= number_format($totalSweIds) ?></div>
                <div class="stat-label">Totalt SWE-ID</div>
            </div>
        </div>

        <?php if (empty($problematicRiders)): ?>
        <div class="empty-state">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/>
                <polyline points="22 4 12 14.01 9 11.01"/>
            </svg>
            <h3>Alla SWE-ID är i korrekt format!</h3>
            <p>Det finns inga SWE-ID som behöver konverteras till det nya formatet.</p>
        </div>
        <?php else: ?>

        <form method="POST" id="convert-form">
            <?= csrf_field() ?>
            <input type="hidden" name="action" value="convert_selected" id="form-action">

            <div class="action-bar">
                <div class="action-bar-left">
                    <label class="select-all-label">
                        <input type="checkbox" id="select-all">
                        <span>Markera alla</span>
                    </label>
                    <span class="badge-count" id="selected-count">0 valda</span>
                </div>
                <div style="display: flex; gap: var(--space-sm);">
                    <button type="submit" class="btn-admin btn-admin-primary" id="convert-selected-btn" disabled>
                        <i data-lucide="check"></i>
                        Konvertera valda
                    </button>
                    <button type="button" class="btn-admin btn-convert-all" onclick="convertAll()">
                        <i data-lucide="refresh-cw"></i>
                        Konvertera alla (<?= count($problematicRiders) ?>)
                    </button>
                </div>
            </div>

            <div class="table-responsive">
                <table class="swe-table">
                    <thead>
                        <tr>
                            <th class="checkbox-cell"></th>
                            <th>Deltagare</th>
                            <th>Nuvarande SWE-ID</th>
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
                                <span class="swe-old"><?= htmlspecialchars($rider['license_number']) ?></span>
                            </td>
                            <td>
                                <span class="swe-new"><?= htmlspecialchars($rider['new_license']) ?></span>
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
    const convertBtn = document.getElementById('convert-selected-btn');

    function updateCount() {
        const checked = document.querySelectorAll('.rider-checkbox:checked').length;
        selectedCount.textContent = checked + ' valda';
        if (convertBtn) convertBtn.disabled = checked === 0;
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

function convertAll() {
    if (confirm('Är du säker på att du vill konvertera alla <?= count($problematicRiders) ?> SWE-ID?')) {
        document.getElementById('form-action').value = 'convert_all';
        document.getElementById('convert-form').submit();
    }
}
</script>

<?php include __DIR__ . '/components/unified-layout-footer.php'; ?>
