<?php
/**
 * Fix Birth Years Tool
 * Fixes riders with impossible birth years (parsed incorrectly from personnummer)
 */
require_once __DIR__ . '/../config.php';
require_admin();

$db = getDB();
$message = '';
$messageType = '';

/**
 * Try to extract correct birth year from a value that looks like personnummer
 */
function extractBirthYearFromPersonnummer($value) {
    if (empty($value)) return null;

    // Remove non-digits except dash
    $clean = preg_replace('/[^\d\-]/', '', trim($value));

    // 12 digits with dash: YYYYMMDD-XXXX
    if (preg_match('/^(\d{4})\d{4}-?\d{4}$/', $clean, $m)) {
        $year = (int)$m[1];
        if ($year >= 1900 && $year <= date('Y')) {
            return $year;
        }
    }

    // 10 digits: YYMMDD-XXXX or YYMMDDXXXX
    if (preg_match('/^(\d{2})\d{4}-?\d{4}$/', $clean, $m)) {
        $yy = (int)$m[1];
        $currentYear = (int)date('Y');
        $currentCentury = (int)floor($currentYear / 100) * 100;

        if ($yy > ($currentYear % 100)) {
            return $currentCentury - 100 + $yy;
        } else {
            return $currentCentury + $yy;
        }
    }

    return null;
}

// Handle form submission
if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['action'])) {
    checkCsrf();

    if ($_POST['action'] === 'fix_selected' && isset($_POST['fixes']) && is_array($_POST['fixes'])) {
        $fixed = 0;
        $errors = 0;

        foreach ($_POST['fixes'] as $riderId => $newYear) {
            $riderId = (int)$riderId;
            $newYear = (int)$newYear;

            if ($newYear >= 1900 && $newYear <= date('Y')) {
                try {
                    $db->query(
                        "UPDATE riders SET birth_year = ?, updated_at = NOW() WHERE id = ?",
                        [$newYear, $riderId]
                    );
                    $fixed++;
                } catch (Exception $e) {
                    $errors++;
                }
            }
        }

        if ($fixed > 0) {
            $message = "Fixade födelseår för $fixed deltagare" . ($errors > 0 ? " ($errors fel)" : "");
            $messageType = 'success';
        } else {
            $message = "Inga födelseår kunde fixas" . ($errors > 0 ? " ($errors fel)" : "");
            $messageType = 'warning';
        }
    }

    if ($_POST['action'] === 'fix_all_auto') {
        $fixed = 0;
        $errors = 0;

        // Get all riders with bad birth years that have a suggested fix
        $riders = $db->getAll("
            SELECT id, birth_year, license_number
            FROM riders
            WHERE birth_year IS NOT NULL
              AND (birth_year < 1900 OR birth_year > ?)
        ", [date('Y')]);

        foreach ($riders as $rider) {
            // The bad birth_year might actually be the last 4 digits of personnummer
            // Try to figure out the correct year
            $suggestedYear = null;

            // If birth_year is 4 digits and looks like MMDD or control digits
            if ($rider['birth_year'] >= 1000 && $rider['birth_year'] <= 9999) {
                // This might be the last 4 digits of personnummer - we can't recover
                // But if license_number contains birth info, try that
                if (!empty($rider['license_number'])) {
                    $suggestedYear = extractBirthYearFromPersonnummer($rider['license_number']);
                }
            }

            if ($suggestedYear && $suggestedYear >= 1900 && $suggestedYear <= date('Y')) {
                try {
                    $db->query(
                        "UPDATE riders SET birth_year = ?, updated_at = NOW() WHERE id = ?",
                        [$suggestedYear, $rider['id']]
                    );
                    $fixed++;
                } catch (Exception $e) {
                    $errors++;
                }
            }
        }

        if ($fixed > 0) {
            $message = "Automatiskt fixade $fixed födelseår" . ($errors > 0 ? " ($errors fel)" : "");
            $messageType = 'success';
        } else {
            $message = "Kunde inte automatiskt fixa några födelseår. Manuell korrigering krävs.";
            $messageType = 'warning';
        }
    }
}

// Find riders with impossible birth years
$currentYear = (int)date('Y');
$problematicRiders = $db->getAll("
    SELECT r.id, r.firstname, r.lastname, r.birth_year, r.license_number, r.club_id, c.name as club_name
    FROM riders r
    LEFT JOIN clubs c ON r.club_id = c.id
    WHERE r.birth_year IS NOT NULL
      AND (r.birth_year < 1900 OR r.birth_year > ?)
    ORDER BY r.lastname, r.firstname
    LIMIT 500
", [$currentYear]);

// Add suggested corrections
foreach ($problematicRiders as &$rider) {
    $rider['suggested_year'] = null;

    // Try to extract from license_number if it looks like personnummer
    if (!empty($rider['license_number'])) {
        $rider['suggested_year'] = extractBirthYearFromPersonnummer($rider['license_number']);
    }
}
unset($rider);

// Count totals
$totalBad = $db->getRow("
    SELECT COUNT(*) as cnt FROM riders
    WHERE birth_year IS NOT NULL AND (birth_year < 1900 OR birth_year > ?)
", [$currentYear])['cnt'] ?? 0;

$totalRiders = $db->getRow("SELECT COUNT(*) as cnt FROM riders")['cnt'] ?? 0;

// Page config
$page_title = 'Fixa födelseår';
$breadcrumbs = [
    ['label' => 'Verktyg', 'url' => '/admin/tools'],
    ['label' => 'Fixa födelseår']
];

include __DIR__ . '/components/unified-layout.php';
?>

<style>
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

.stat-value.danger {
    color: var(--color-danger);
}

.stat-label {
    font-size: var(--text-sm);
    color: var(--color-text-secondary);
}

.action-bar {
    display: flex;
    justify-content: flex-end;
    gap: var(--space-sm);
    margin-bottom: var(--space-md);
    padding: var(--space-md);
    background: var(--color-bg-surface);
    border: 1px solid var(--color-border);
    border-radius: var(--radius-md);
}

.fix-table {
    width: 100%;
    border-collapse: collapse;
}

.fix-table th,
.fix-table td {
    padding: var(--space-sm) var(--space-md);
    text-align: left;
    border-bottom: 1px solid var(--color-border);
}

.fix-table th {
    background: var(--color-bg-muted);
    font-weight: 600;
    font-size: var(--text-sm);
}

.fix-table tr:hover {
    background: var(--color-bg-hover);
}

.bad-year {
    color: var(--color-danger);
    font-weight: 600;
    font-family: var(--font-mono);
}

.suggested-year {
    color: var(--color-success);
    font-weight: 600;
}

.year-input {
    width: 80px;
    padding: var(--space-xs) var(--space-sm);
    border: 1px solid var(--color-border);
    border-radius: var(--radius-sm);
    font-family: var(--font-mono);
    text-align: center;
}

.year-input:focus {
    border-color: var(--color-accent);
    outline: none;
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

.club-name {
    font-size: var(--text-sm);
    color: var(--color-text-secondary);
}

.license-info {
    font-size: var(--text-xs);
    color: var(--color-text-tertiary);
    font-family: var(--font-mono);
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
            <i data-lucide="calendar-x"></i>
            Fixa felaktiga födelseår
        </h2>
    </div>
    <div class="card-body">
        <p style="margin-bottom: var(--space-md); color: var(--color-text-secondary);">
            Deltagare med födelseår som är omöjliga (före 1900 eller efter <?= $currentYear ?>).
            Detta beror oftast på felaktig parsning av personnummer vid import.
        </p>

        <div class="stats-row">
            <div class="stat-item">
                <div class="stat-value <?= $totalBad > 0 ? 'danger' : '' ?>">
                    <?= number_format($totalBad) ?>
                </div>
                <div class="stat-label">Felaktiga födelseår</div>
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
            <h3>Alla födelseår är korrekta!</h3>
            <p>Det finns inga deltagare med omöjliga födelseår.</p>
        </div>
        <?php else: ?>

        <form method="POST" id="fix-form">
            <?= csrf_field() ?>
            <input type="hidden" name="action" value="fix_selected" id="form-action">

            <div class="action-bar">
                <button type="submit" class="btn-admin btn-admin-primary">
                    <i data-lucide="check"></i>
                    Spara ändringar
                </button>
            </div>

            <div class="table-responsive">
                <table class="fix-table">
                    <thead>
                        <tr>
                            <th>Deltagare</th>
                            <th>Klubb</th>
                            <th>Felaktigt år</th>
                            <th>Nytt födelseår</th>
                        </tr>
                    </thead>
                    <tbody>
                        <?php foreach ($problematicRiders as $rider): ?>
                        <tr>
                            <td>
                                <a href="/admin/riders/edit/<?= $rider['id'] ?>">
                                    <?= htmlspecialchars($rider['firstname'] . ' ' . $rider['lastname']) ?>
                                </a>
                                <?php if (!empty($rider['license_number'])): ?>
                                <div class="license-info"><?= htmlspecialchars($rider['license_number']) ?></div>
                                <?php endif; ?>
                            </td>
                            <td>
                                <span class="club-name"><?= htmlspecialchars($rider['club_name'] ?? '-') ?></span>
                            </td>
                            <td>
                                <span class="bad-year"><?= $rider['birth_year'] ?></span>
                            </td>
                            <td>
                                <input type="number"
                                       name="fixes[<?= $rider['id'] ?>]"
                                       class="year-input"
                                       value="<?= $rider['suggested_year'] ?? '' ?>"
                                       min="1900"
                                       max="<?= $currentYear ?>"
                                       placeholder="YYYY">
                                <?php if ($rider['suggested_year']): ?>
                                <span class="suggested-year" title="Föreslagen korrigering">?</span>
                                <?php endif; ?>
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
    // Initialize Lucide icons
    if (typeof lucide !== 'undefined') {
        lucide.createIcons();
    }
});
</script>

<?php include __DIR__ . '/components/unified-layout-footer.php'; ?>
