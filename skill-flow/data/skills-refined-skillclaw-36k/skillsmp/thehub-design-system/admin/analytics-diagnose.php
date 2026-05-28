<?php
/**
 * Analytics Diagnostik
 *
 * Jamfor faktisk data i results/events med rider_yearly_stats
 * for att identifiera diskrepanser.
 *
 * @package TheHUB Analytics
 */
require_once __DIR__ . '/../config.php';
require_once __DIR__ . '/../includes/auth.php';
require_admin();

global $pdo;

// Satt query timeout
$pdo->setAttribute(PDO::ATTR_TIMEOUT, 10);

$diagnostics = [];
$errors = [];

// Hjalpfunktion for att kolla om tabell finns
function tableExists($pdo, $name) {
    try {
        $result = $pdo->query("SHOW TABLES LIKE '$name'")->fetch();
        return (bool)$result;
    } catch (Exception $e) {
        return false;
    }
}

// 1. Kolla om nodvandiga tabeller/views finns
$requiredObjects = [
    'rider_yearly_stats',
    'series_participation',
    'v_canonical_riders',
    'rider_merge_map',
    'analytics_cron_runs'
];

foreach ($requiredObjects as $name) {
    $diagnostics['objects'][$name] = tableExists($pdo, $name) ? 'EXISTS' : 'MISSING';
}

$hasCanonicalView = $diagnostics['objects']['v_canonical_riders'] === 'EXISTS';
$hasYearlyStats = $diagnostics['objects']['rider_yearly_stats'] === 'EXISTS';

// 2. Hamta faktiska deltagare fran results/events (ALLTID)
try {
    $stmt = $pdo->query("
        SELECT
            YEAR(e.date) as year,
            COUNT(DISTINCT r.cyclist_id) as actual_unique_riders,
            COUNT(*) as total_result_rows
        FROM results r
        JOIN events e ON r.event_id = e.id
        WHERE e.date IS NOT NULL
        GROUP BY YEAR(e.date)
        ORDER BY year DESC
    ");
    $diagnostics['actual_data'] = $stmt->fetchAll(PDO::FETCH_ASSOC);
} catch (Exception $e) {
    $errors[] = "Kunde inte hamta faktisk data: " . $e->getMessage();
    $diagnostics['actual_data'] = [];
}

// 3. Hamta rider_yearly_stats per ar (om tabellen finns)
if ($hasYearlyStats) {
    try {
        $stmt = $pdo->query("
            SELECT season_year as year, COUNT(*) as analytics_riders
            FROM rider_yearly_stats
            GROUP BY season_year
            ORDER BY season_year DESC
        ");
        $diagnostics['analytics_data'] = $stmt->fetchAll(PDO::FETCH_KEY_PAIR);
    } catch (Exception $e) {
        $errors[] = "Kunde inte hamta analytics data: " . $e->getMessage();
        $diagnostics['analytics_data'] = [];
    }
} else {
    $diagnostics['analytics_data'] = [];
    $errors[] = "Tabellen rider_yearly_stats saknas - kor setup-tables.php";
}

// 4. Kolla v_canonical_riders (om VIEW finns)
if ($hasCanonicalView) {
    try {
        $stmt = $pdo->query("SELECT COUNT(*) FROM v_canonical_riders");
        $diagnostics['canonical_riders_count'] = $stmt->fetchColumn();
    } catch (Exception $e) {
        $errors[] = "v_canonical_riders VIEW ar trasig: " . $e->getMessage();
        $diagnostics['canonical_riders_count'] = 'ERROR';
    }
} else {
    $diagnostics['canonical_riders_count'] = 'MISSING';
}

// 5. Total riders
try {
    $stmt = $pdo->query("SELECT COUNT(*) FROM riders");
    $diagnostics['total_riders'] = $stmt->fetchColumn();
} catch (Exception $e) {
    $diagnostics['total_riders'] = 'ERROR';
}

// 6. Storsta event per ar (enkel query utan v_canonical_riders)
try {
    $stmt = $pdo->query("
        SELECT
            YEAR(e.date) as year,
            e.name as event_name,
            e.date,
            COUNT(r.id) as participants
        FROM results r
        JOIN events e ON r.event_id = e.id
        WHERE e.date IS NOT NULL
        GROUP BY e.id
        HAVING participants > 50
        ORDER BY year DESC, participants DESC
        LIMIT 50
    ");
    $allEvents = $stmt->fetchAll(PDO::FETCH_ASSOC);

    $maxPerYear = [];
    foreach ($allEvents as $ev) {
        $y = $ev['year'];
        if (!isset($maxPerYear[$y]) || $ev['participants'] > $maxPerYear[$y]['participants']) {
            $maxPerYear[$y] = $ev;
        }
    }
    $diagnostics['largest_events'] = $maxPerYear;
} catch (Exception $e) {
    $errors[] = "Kunde inte hamta event-data: " . $e->getMessage();
    $diagnostics['largest_events'] = [];
}

// 7. Cron-runs (om tabellen finns)
if (tableExists($pdo, 'analytics_cron_runs')) {
    try {
        $stmt = $pdo->query("
            SELECT job_name, run_key, status, started_at, finished_at, rows_affected
            FROM analytics_cron_runs
            ORDER BY started_at DESC
            LIMIT 15
        ");
        $diagnostics['cron_runs'] = $stmt->fetchAll(PDO::FETCH_ASSOC);
    } catch (Exception $e) {
        $diagnostics['cron_runs'] = [];
    }
} else {
    $diagnostics['cron_runs'] = [];
}

$page_title = 'Analytics Diagnostik';
$breadcrumbs = [
    ['label' => 'Tools', 'url' => '/admin/tools.php'],
    ['label' => 'Analytics Diagnostik']
];
include __DIR__ . '/components/unified-layout.php';
?>

<style>
.diag-card {
    background: var(--color-bg-card);
    border: 1px solid var(--color-border);
    border-radius: var(--radius-md);
    padding: var(--space-lg);
    margin-bottom: var(--space-lg);
}
.diag-card h3 {
    margin: 0 0 var(--space-md);
    font-size: var(--text-lg);
    color: var(--color-text-primary);
}
.status-ok { color: var(--color-success); font-weight: 600; }
.status-error { color: var(--color-error); font-weight: 600; }
.status-warning { color: var(--color-warning); font-weight: 600; }
.compare-table th { text-align: left; padding: var(--space-sm); }
.compare-table td { padding: var(--space-sm); }
.compare-table tr:nth-child(even) { background: var(--color-bg-hover); }
.discrepancy { background: rgba(239, 68, 68, 0.15) !important; }
.big-number {
    font-size: var(--text-2xl);
    font-weight: 700;
    color: var(--color-accent);
}
.info-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
    gap: var(--space-md);
}
.info-box {
    background: var(--color-bg-surface);
    padding: var(--space-md);
    border-radius: var(--radius-sm);
    text-align: center;
}
.info-box .label {
    font-size: var(--text-sm);
    color: var(--color-text-muted);
    word-break: break-all;
}
</style>

<?php if (!empty($errors)): ?>
<div class="alert alert-danger">
    <i data-lucide="alert-circle"></i>
    <div>
        <strong>Problem upptackta:</strong>
        <ul style="margin: var(--space-sm) 0 0; padding-left: var(--space-lg);">
            <?php foreach ($errors as $err): ?>
                <li><?= htmlspecialchars($err) ?></li>
            <?php endforeach; ?>
        </ul>
    </div>
</div>
<?php endif; ?>

<!-- DATABAS-OBJEKT -->
<div class="diag-card">
    <h3>1. Databas-objekt</h3>
    <div class="info-grid">
        <?php foreach ($diagnostics['objects'] as $name => $status): ?>
        <div class="info-box">
            <div class="label"><?= htmlspecialchars($name) ?></div>
            <div class="<?= $status === 'EXISTS' ? 'status-ok' : 'status-error' ?>">
                <?= $status === 'EXISTS' ? 'OK' : 'SAKNAS' ?>
            </div>
        </div>
        <?php endforeach; ?>
    </div>

    <div style="margin-top: var(--space-md);">
        <strong>riders-tabell:</strong> <?= is_numeric($diagnostics['total_riders']) ? number_format($diagnostics['total_riders']) : $diagnostics['total_riders'] ?> rader
        <?php if ($hasCanonicalView && is_numeric($diagnostics['canonical_riders_count'])): ?>
        | <strong>v_canonical_riders:</strong> <?= number_format($diagnostics['canonical_riders_count']) ?> rader
        <?php endif; ?>
    </div>
</div>

<!-- JAMFORELSE -->
<div class="diag-card">
    <h3>2. Jamforelse: Faktiska deltagare vs Analytics</h3>

    <?php if (!$hasYearlyStats): ?>
    <div class="alert alert-warning">
        <i data-lucide="alert-triangle"></i>
        rider_yearly_stats-tabellen saknas. Kor setup forst.
    </div>
    <?php else: ?>

    <div class="admin-table-container">
        <table class="admin-table compare-table">
            <thead>
                <tr>
                    <th>Ar</th>
                    <th>Faktiska</th>
                    <th>Analytics</th>
                    <th>Differens</th>
                    <th>Storsta event</th>
                </tr>
            </thead>
            <tbody>
                <?php foreach ($diagnostics['actual_data'] ?? [] as $row):
                    $year = $row['year'];
                    $actual = (int)$row['actual_unique_riders'];
                    $analytics = (int)($diagnostics['analytics_data'][$year] ?? 0);
                    $diff = $analytics - $actual;
                    $pct = $actual > 0 ? round($analytics / $actual * 100, 1) : 0;
                    $isDiscrepancy = $pct < 50 || ($actual > 0 && $analytics === 0);

                    $largestEvent = $diagnostics['largest_events'][$year] ?? null;
                ?>
                <tr class="<?= $isDiscrepancy ? 'discrepancy' : '' ?>">
                    <td><strong><?= $year ?></strong></td>
                    <td><?= number_format($actual) ?></td>
                    <td>
                        <?= number_format($analytics) ?>
                        <?php if ($analytics === 0 && $actual > 0): ?>
                            <span class="status-error">(SAKNAS!)</span>
                        <?php endif; ?>
                    </td>
                    <td>
                        <?php if ($actual > 0): ?>
                            <span class="<?= $pct >= 90 ? 'status-ok' : ($pct >= 50 ? 'status-warning' : 'status-error') ?>">
                                <?= $pct ?>%
                            </span>
                        <?php else: ?>
                            -
                        <?php endif; ?>
                    </td>
                    <td>
                        <?php if ($largestEvent): ?>
                            <?= htmlspecialchars($largestEvent['event_name']) ?>
                            (<?= number_format($largestEvent['participants']) ?>)
                        <?php else: ?>
                            -
                        <?php endif; ?>
                    </td>
                </tr>
                <?php endforeach; ?>
            </tbody>
        </table>
    </div>

    <?php endif; ?>
</div>

<!-- CRON-KORNINGAR -->
<?php if (!empty($diagnostics['cron_runs'])): ?>
<div class="diag-card">
    <h3>3. Senaste Analytics-korningar</h3>
    <div class="admin-table-container">
        <table class="admin-table">
            <thead>
                <tr>
                    <th>Jobb</th>
                    <th>Ar</th>
                    <th>Status</th>
                    <th>Rader</th>
                    <th>Tid</th>
                </tr>
            </thead>
            <tbody>
                <?php foreach ($diagnostics['cron_runs'] as $run): ?>
                <tr>
                    <td><?= htmlspecialchars($run['job_name']) ?></td>
                    <td><?= htmlspecialchars($run['run_key']) ?></td>
                    <td>
                        <span class="<?= $run['status'] === 'success' ? 'status-ok' : ($run['status'] === 'started' ? 'status-warning' : 'status-error') ?>">
                            <?= htmlspecialchars($run['status']) ?>
                        </span>
                    </td>
                    <td><?= number_format($run['rows_affected'] ?? 0) ?></td>
                    <td><?= $run['started_at'] ?></td>
                </tr>
                <?php endforeach; ?>
            </tbody>
        </table>
    </div>
</div>
<?php endif; ?>

<!-- ATGARDER -->
<div class="diag-card">
    <h3>4. Atgarder</h3>

    <?php
    $missingObjects = array_filter($diagnostics['objects'], fn($s) => $s !== 'EXISTS');
    $hasDataIssue = false;
    foreach ($diagnostics['actual_data'] ?? [] as $row) {
        $year = $row['year'];
        $actual = (int)$row['actual_unique_riders'];
        $analytics = (int)($diagnostics['analytics_data'][$year] ?? 0);
        if ($actual > 100 && $analytics < $actual * 0.5) {
            $hasDataIssue = true;
            break;
        }
    }
    ?>

    <?php if (!empty($missingObjects)): ?>
    <div class="alert alert-danger" style="margin-bottom: var(--space-md);">
        <i data-lucide="database"></i>
        <div>
            <strong>1. Skapa saknade tabeller/views</strong><br>
            Kor dessa kommandon (SSH eller via migrations):<br>
            <code style="display: block; margin-top: var(--space-xs);">php analytics/setup-governance.php</code>
            <code style="display: block;">php analytics/setup-tables.php</code>
        </div>
    </div>
    <?php endif; ?>

    <?php if ($hasDataIssue || (!empty($diagnostics['analytics_data']) && empty(array_filter($diagnostics['analytics_data'])))): ?>
    <div class="alert alert-warning" style="margin-bottom: var(--space-md);">
        <i data-lucide="refresh-cw"></i>
        <div>
            <strong><?= !empty($missingObjects) ? '2' : '1' ?>. Regenerera analytics-data</strong><br>
            <a href="/analytics/populate-historical.php?force=1" class="btn-admin btn-admin-warning" style="margin-top: var(--space-sm);">
                Kor populate-historical (Force)
            </a>
        </div>
    </div>
    <?php endif; ?>

    <?php if (empty($missingObjects) && !$hasDataIssue): ?>
    <div class="alert alert-success">
        <i data-lucide="check-circle"></i>
        <div>
            <strong>Allt ser bra ut!</strong><br>
            Tabeller finns och data matchar.
        </div>
    </div>
    <?php endif; ?>
</div>

<?php include __DIR__ . '/components/unified-layout-footer.php'; ?>
