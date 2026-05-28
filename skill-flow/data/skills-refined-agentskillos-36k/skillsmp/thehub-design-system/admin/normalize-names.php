<?php
/**
 * Normalize Names Tool - Convert names to proper title case
 * TheHUB V3
 *
 * Finds riders with ALL CAPS or all lowercase names and normalizes them
 */
require_once __DIR__ . '/../config.php';
require_admin();

$db = getDB();
$message = '';
$messageType = '';

/**
 * Convert a name to proper Swedish title case
 * Handles special cases like "von", "af", "de", "van" etc.
 */
function properNameCase($name) {
    if (empty($name)) return $name;

    // First, convert to lowercase
    $name = mb_strtolower($name, 'UTF-8');

    // Split on spaces and hyphens but preserve the delimiters
    $parts = preg_split('/(\s+|-)/u', $name, -1, PREG_SPLIT_DELIM_CAPTURE);

    // Words that should stay lowercase (noble prefixes, etc.)
    $lowercaseWords = ['von', 'af', 'de', 'van', 'der', 'den', 'la', 'le', 'du', 'da', 'dos', 'das', 'di', 'del'];

    $result = [];
    $isFirst = true;

    foreach ($parts as $part) {
        // Skip empty parts and delimiters
        if (preg_match('/^(\s+|-)$/u', $part)) {
            $result[] = $part;
            continue;
        }

        if (empty(trim($part))) {
            $result[] = $part;
            continue;
        }

        // Check if it's a lowercase word (but capitalize if it's the first word)
        if (!$isFirst && in_array(mb_strtolower($part, 'UTF-8'), $lowercaseWords)) {
            $result[] = mb_strtolower($part, 'UTF-8');
        } else {
            // Capitalize first letter
            $result[] = mb_strtoupper(mb_substr($part, 0, 1, 'UTF-8'), 'UTF-8') . mb_substr($part, 1, null, 'UTF-8');
        }

        $isFirst = false;
    }

    return implode('', $result);
}

/**
 * Check if a name needs normalization
 * - All caps: "ANDERSSON"
 * - All lowercase: "andersson"
 * - Mixed with caps words: "Anna ANDERSSON" or "ANDERSSON BERG"
 */
function needsNormalization($name) {
    if (empty($name) || strlen($name) < 2) return false;

    // Remove spaces and hyphens for full-name check
    $cleanName = preg_replace('/[\s-]/u', '', $name);
    if (empty($cleanName)) return false;

    // Check if entire name is all uppercase or all lowercase
    $upper = mb_strtoupper($cleanName, 'UTF-8');
    $lower = mb_strtolower($cleanName, 'UTF-8');

    if ($cleanName === $upper || $cleanName === $lower) {
        return true;
    }

    // Also check individual words - catch "Anna ANDERSSON" or "ANDERSSON BERG"
    $words = preg_split('/[\s-]+/u', $name);
    foreach ($words as $word) {
        if (mb_strlen($word, 'UTF-8') >= 2) {
            $wordUpper = mb_strtoupper($word, 'UTF-8');
            $wordLower = mb_strtolower($word, 'UTF-8');
            // If any word is all caps (and not a known acronym), needs normalization
            if ($word === $wordUpper && preg_match('/[A-ZÄÖÅÜ]/u', $word)) {
                return true;
            }
        }
    }

    return false;
}

// Handle form submission
if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['action'])) {
    if ($_POST['action'] === 'normalize_selected' && isset($_POST['rider_ids']) && is_array($_POST['rider_ids'])) {
        $normalized = 0;
        $errors = 0;

        foreach ($_POST['rider_ids'] as $riderId) {
            $riderId = (int)$riderId;
            $rider = $db->getRow("SELECT id, firstname, lastname FROM riders WHERE id = ?", [$riderId]);

            if ($rider) {
                $newFirstName = properNameCase($rider['firstname']);
                $newLastName = properNameCase($rider['lastname']);

                try {
                    $db->query(
                        "UPDATE riders SET firstname = ?, lastname = ?, updated_at = NOW() WHERE id = ?",
                        [$newFirstName, $newLastName, $riderId]
                    );
                    $normalized++;
                } catch (Exception $e) {
                    $errors++;
                    error_log("Error normalizing rider $riderId: " . $e->getMessage());
                }
            }
        }

        if ($normalized > 0) {
            $message = "Normaliserade $normalized namn" . ($errors > 0 ? " ($errors fel)" : "");
            $messageType = 'success';
        } else {
            $message = "Inga namn kunde normaliseras" . ($errors > 0 ? " ($errors fel)" : "");
            $messageType = 'warning';
        }
    }

    if ($_POST['action'] === 'normalize_all') {
        $normalized = 0;
        $errors = 0;

        // Get all riders that need normalization
        $riders = $db->getAll("SELECT id, firstname, lastname FROM riders");

        foreach ($riders as $rider) {
            if (needsNormalization($rider['firstname']) || needsNormalization($rider['lastname'])) {
                $newFirstName = properNameCase($rider['firstname']);
                $newLastName = properNameCase($rider['lastname']);

                // Only update if something changed
                if ($newFirstName !== $rider['firstname'] || $newLastName !== $rider['lastname']) {
                    try {
                        $db->query(
                            "UPDATE riders SET firstname = ?, lastname = ?, updated_at = NOW() WHERE id = ?",
                            [$newFirstName, $newLastName, $rider['id']]
                        );
                        $normalized++;
                    } catch (Exception $e) {
                        $errors++;
                        error_log("Error normalizing rider {$rider['id']}: " . $e->getMessage());
                    }
                }
            }
        }

        if ($normalized > 0) {
            $message = "Normaliserade $normalized namn" . ($errors > 0 ? " ($errors fel)" : "");
            $messageType = 'success';
        } else {
            $message = "Alla namn är redan korrekt formaterade";
            $messageType = 'info';
        }
    }
}

// PERFORMANCE FIX: Only fetch riders that actually need normalization
// Using SQL pattern matching instead of loading all riders into PHP memory
// This query finds names that are ALL CAPS, all lowercase, OR contain words in all caps
// NOTE: Must use BINARY for case-sensitive comparison since MySQL default collation is case-insensitive
$problematicRiders = $db->getAll("
    SELECT id, firstname, lastname, club_id
    FROM riders
    WHERE (
        -- All uppercase (case-sensitive comparison with BINARY)
        (LENGTH(firstname) >= 2 AND BINARY firstname = BINARY UPPER(firstname) AND firstname REGEXP BINARY '[A-ZÄÖÅÜ]')
        OR (LENGTH(lastname) >= 2 AND BINARY lastname = BINARY UPPER(lastname) AND lastname REGEXP BINARY '[A-ZÄÖÅÜ]')
        -- All lowercase (case-sensitive comparison with BINARY)
        OR (LENGTH(firstname) >= 2 AND BINARY firstname = BINARY LOWER(firstname) AND firstname REGEXP BINARY '[a-zäöåü]')
        OR (LENGTH(lastname) >= 2 AND BINARY lastname = BINARY LOWER(lastname) AND lastname REGEXP BINARY '[a-zäöåü]')
        -- Contains words in all caps (double last names like 'ANDERSSON BERG' or 'Anna ANDERSSON')
        OR (lastname REGEXP BINARY '[A-ZÄÖÅ]{2,}' AND lastname REGEXP BINARY ' ')
        OR (firstname REGEXP BINARY '[A-ZÄÖÅ]{2,}' AND firstname != BINARY UPPER(firstname))
        OR (lastname REGEXP BINARY '[A-ZÄÖÅ]{2,}' AND lastname != BINARY UPPER(lastname))
    )
    ORDER BY lastname, firstname
    LIMIT 500
");

// Filter in PHP to ensure accurate detection (SQL regex is limited)
$problematicRiders = array_filter($problematicRiders, function($rider) {
    return needsNormalization($rider['firstname']) || needsNormalization($rider['lastname']);
});
$problematicRiders = array_values($problematicRiders); // Re-index array

// Add preview data
foreach ($problematicRiders as &$rider) {
    $rider['new_firstname'] = properNameCase($rider['firstname']);
    $rider['new_lastname'] = properNameCase($rider['lastname']);
    $rider['first_needs_norm'] = needsNormalization($rider['firstname']);
    $rider['last_needs_norm'] = needsNormalization($rider['lastname']);
}
unset($rider);

// Get total count for stats (separate lightweight query)
$totalRiders = $db->getRow("SELECT COUNT(*) as cnt FROM riders")['cnt'] ?? 0;

// Get club names for display
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
$page_title = 'Normalisera namn';
$breadcrumbs = [
    ['label' => 'Verktyg', 'url' => '/admin/tools'],
    ['label' => 'Normalisera namn']
];

include __DIR__ . '/components/unified-layout.php';
?>

<style>
.name-preview {
    display: flex;
    align-items: center;
    gap: var(--space-sm);
}

.name-old {
    color: var(--color-text-secondary);
    text-decoration: line-through;
}

.name-new {
    color: var(--color-success);
    font-weight: 600;
}

.name-arrow {
    color: var(--color-text-muted);
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

.name-table {
    width: 100%;
    border-collapse: collapse;
}

.name-table th,
.name-table td {
    padding: var(--space-sm) var(--space-md);
    text-align: left;
    border-bottom: 1px solid var(--color-border);
}

.name-table th {
    background: var(--color-bg-muted);
    font-weight: 600;
    font-size: var(--text-sm);
}

.name-table tr:hover {
    background: var(--color-bg-hover);
}

.name-table td.checkbox-cell {
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
            <i data-lucide="type"></i>
            Normalisera deltagarnamn
        </h2>
    </div>
    <div class="card-body">
        <p style="margin-bottom: var(--space-md); color: var(--color-text-secondary);">
            Detta verktyg hittar deltagare med namn som är skrivna med STORA BOKSTÄVER eller små bokstäver
            och konverterar dem till normal versalgemen form (t.ex. "ANNA ANDERSSON" → "Anna Andersson").
        </p>

        <div class="stats-row">
            <div class="stat-item">
                <div class="stat-value <?= count($problematicRiders) > 0 ? 'warning' : '' ?>">
                    <?= count($problematicRiders) ?>
                </div>
                <div class="stat-label">Behöver normaliseras</div>
            </div>
            <div class="stat-item">
                <div class="stat-value"><?= number_format($totalRiders) ?></div>
                <div class="stat-label">Totalt deltagare</div>
            </div>
        </div>

        <?php if (empty($problematicRiders)): ?>
        <div class="empty-state">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/>
                <polyline points="22 4 12 14.01 9 11.01"/>
            </svg>
            <h3>Alla namn är korrekt formaterade!</h3>
            <p>Det finns inga deltagare med namn som behöver normaliseras.</p>
        </div>
        <?php else: ?>

        <form method="POST" id="normalize-form">
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
                        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="width: 16px; height: 16px;">
                            <polyline points="20 6 9 17 4 12"/>
                        </svg>
                        Normalisera valda
                    </button>
                    <button type="button" class="btn-admin btn-normalize-all" onclick="normalizeAll()">
                        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="width: 16px; height: 16px;">
                            <path d="M21.5 2v6h-6M2.5 22v-6h6M2 11.5a10 10 0 0 1 18.8-4.3M22 12.5a10 10 0 0 1-18.8 4.2"/>
                        </svg>
                        Normalisera alla (<?= count($problematicRiders) ?>)
                    </button>
                </div>
            </div>

            <div class="table-responsive">
                <table class="name-table">
                    <thead>
                        <tr>
                            <th class="checkbox-cell"></th>
                            <th>Nuvarande namn</th>
                            <th>Nytt namn</th>
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
                                <span class="name-old">
                                    <?= htmlspecialchars($rider['firstname'] . ' ' . $rider['lastname']) ?>
                                </span>
                            </td>
                            <td>
                                <span class="name-new">
                                    <?= htmlspecialchars($rider['new_firstname'] . ' ' . $rider['new_lastname']) ?>
                                </span>
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
        normalizeBtn.disabled = checked === 0;
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
});

function normalizeAll() {
    if (confirm('Är du säker på att du vill normalisera alla <?= count($problematicRiders) ?> namn?')) {
        document.getElementById('form-action').value = 'normalize_all';
        document.getElementById('normalize-form').submit();
    }
}
</script>

<?php include __DIR__ . '/components/unified-layout-footer.php'; ?>
