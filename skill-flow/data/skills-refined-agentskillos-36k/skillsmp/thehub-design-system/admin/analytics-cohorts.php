<?php
/**
 * Analytics - Cohort Analysis
 *
 * Foljer kohorter av nya riders over tid for att
 * forsta retention-monster och karriarutveckling.
 *
 * Behorighet: super_admin ELLER statistics-permission
 *
 * @package TheHUB Analytics
 * @version 2.0
 */
require_once __DIR__ . '/../config.php';
require_once __DIR__ . '/../includes/auth.php';
require_once __DIR__ . '/../analytics/includes/KPICalculator.php';
require_once __DIR__ . '/../analytics/includes/AnalyticsConfig.php';

// Kraver super_admin eller statistics-behorighet
requireAnalyticsAccess();

global $pdo;

// Arval
$currentYear = (int)date('Y');
$selectedCohort = isset($_GET['cohort']) && $_GET['cohort'] !== '' ? (int)$_GET['cohort'] : $currentYear - 3;
$selectedBrand = isset($_GET['brand']) && $_GET['brand'] !== '' ? (int)$_GET['brand'] : null;

// Compare kan komma som array (checkboxes) eller som kommaseparerad strang
$compareYears = [];
if (isset($_GET['compare'])) {
    if (is_array($_GET['compare'])) {
        $compareYears = array_map('intval', $_GET['compare']);
    } else {
        $compareYears = array_map('intval', explode(',', $_GET['compare']));
    }
    $compareYears = array_filter($compareYears); // Ta bort tomma/noll-varden
}

// Initiera KPI Calculator
$kpiCalc = new KPICalculator($pdo);

// Hamta alla varumarken for dropdown
$allBrands = [];
try {
    $allBrands = $kpiCalc->getAllBrands();
} catch (Exception $e) {
    // Tabellen kanske inte finns annu
}

// Hamta senaste sasong med data (anvands for att avgora aktiv/churn status)
// Viktigt: Vi anvander senaste avslutade sasong, inte kalenderaret,
// for att undvika att rakna pagaende sasong som "inaktiv"
$latestSeasonYear = $kpiCalc->getLatestSeasonYear();

// Hamta tillgangliga kohorter
$availableCohorts = [];
$cohortRetention = [];
$cohortStatus = [];
$cohortRiders = [];
$cohortComparison = [];
$avgLifespan = 0;
$feederBreakdown = null;

try {
    // Hamta kohorter - filtrerat pa varumarke om valt
    $availableCohorts = $kpiCalc->getAvailableCohortsByBrand($selectedBrand, AnalyticsConfig::COHORT_MIN_SIZE);

    if ($selectedCohort) {
        $cohortRetention = $kpiCalc->getCohortRetentionByBrand($selectedCohort, $selectedBrand, $latestSeasonYear);
        $cohortStatus = $kpiCalc->getCohortStatusBreakdownByBrand($selectedCohort, $selectedBrand, $latestSeasonYear);
        $avgLifespan = $kpiCalc->getCohortAverageLifespanByBrand($selectedCohort, $selectedBrand);

        // Hamta rider-lista (begransad for prestanda)
        $cohortRiders = $kpiCalc->getCohortRidersByBrand($selectedCohort, $selectedBrand, 'all', $latestSeasonYear);

        // Hamta feeder-breakdown om varumärke är valt
        if ($selectedBrand) {
            $feederBreakdown = $kpiCalc->getFeederSeriesBreakdown($selectedCohort, $selectedBrand);
        }
    }

    // Multi-cohort comparison (TODO: add brand filtering)
    if (!empty($compareYears)) {
        $cohortComparison = $kpiCalc->compareCohorts($compareYears, 5);
    }
} catch (Exception $e) {
    $error = $e->getMessage();
}

// Export
if (isset($_GET['export']) && $_GET['export'] === 'csv' && !isset($error)) {
    header('Content-Type: text/csv; charset=utf-8');
    header('Content-Disposition: attachment; filename="thehub-cohort-' . $selectedCohort . '.csv"');
    $output = fopen('php://output', 'w');
    fprintf($output, chr(0xEF).chr(0xBB).chr(0xBF)); // UTF-8 BOM

    fputcsv($output, ['Rider ID', 'Fornamn', 'Efternamn', 'Klubb', 'Forsta Disciplin', 'Sasonger', 'Sista Aktiv', 'Status', 'Profil']);
    foreach ($cohortRiders as $rider) {
        fputcsv($output, [
            $rider['rider_id'],
            $rider['firstname'],
            $rider['lastname'],
            $rider['club_name'] ?? '',
            $rider['first_discipline'] ?? '',
            $rider['total_seasons'],
            $rider['last_active_year'],
            $rider['current_status'],
            'https://thehub.se/rider/' . $rider['rider_id']
        ]);
    }
    fclose($output);

    // Logga export
    try {
        $stmt = $pdo->prepare("INSERT INTO analytics_exports (export_type, export_params, exported_by, row_count, ip_address) VALUES (?, ?, ?, ?, ?)");
        $stmt->execute(['cohort_riders', json_encode(['cohort' => $selectedCohort]), $_SESSION['user_id'] ?? null, count($cohortRiders), $_SERVER['REMOTE_ADDR'] ?? null]);
    } catch (Exception $e) { /* Ignore */ }

    exit;
}

// Page config
$page_title = 'Kohort-analys';
$breadcrumbs = [
    ['label' => 'Analytics', 'url' => '/admin/analytics-dashboard.php'],
    ['label' => 'Kohorter']
];

$page_actions = '
<div class="btn-group">
    <a href="/admin/analytics-dashboard.php" class="btn-admin btn-admin-secondary">
        <i data-lucide="arrow-left"></i> Dashboard
    </a>
</div>
';

// Include unified layout
include __DIR__ . '/components/unified-layout.php';
?>

<!-- Info Box - Forklaring -->
<div class="info-box">
    <div class="info-box-icon">
        <i data-lucide="info"></i>
    </div>
    <div class="info-box-content">
        <strong>Vad ar en kohort?</strong>
        <p>En kohort ar en grupp riders som borjade samma ar. T.ex. "Kohort 2023" ar alla som hade sin <em>forsta tavling</em> 2023. Har kan du folja hur manga som fortsatter aktiva over tid (retention) och hur manga som slutar (churn).</p>
        <p style="margin-top: var(--space-xs); font-size: var(--text-xs); color: var(--color-text-muted);">
            <i data-lucide="calendar" style="width: 12px; height: 12px; display: inline-block; vertical-align: middle;"></i>
            Data baseras pa sasong <strong><?= $latestSeasonYear ?></strong> (senaste avslutade sasong med data)
        </p>
    </div>
</div>

<!-- Cohort Selector -->
<div class="filter-bar">
    <form method="get" class="filter-form">
        <?php if (!empty($allBrands)): ?>
        <div class="filter-group">
            <label class="filter-label">Varumarke</label>
            <select name="brand" class="form-select" onchange="this.form.submit()">
                <option value="">Alla varumarken</option>
                <?php foreach ($allBrands as $brand): ?>
                    <option value="<?= $brand['id'] ?>" <?= $selectedBrand == $brand['id'] ? 'selected' : '' ?>
                        <?php if (!empty($brand['accent_color'])): ?>style="border-left: 3px solid <?= htmlspecialchars($brand['accent_color']) ?>"<?php endif; ?>>
                        <?= htmlspecialchars($brand['name']) ?>
                    </option>
                <?php endforeach; ?>
            </select>
        </div>
        <?php endif; ?>

        <div class="filter-group">
            <label class="filter-label">Valj Kohort (startår)</label>
            <select name="cohort" class="form-select" onchange="this.form.submit()">
                <option value="">-- Valj kohort --</option>
                <?php foreach ($availableCohorts as $c): ?>
                    <option value="<?= $c['cohort_year'] ?>" <?= $c['cohort_year'] == $selectedCohort ? 'selected' : '' ?>>
                        <?= $c['cohort_year'] ?> (<?= number_format($c['cohort_size']) ?> riders)
                    </option>
                <?php endforeach; ?>
            </select>
        </div>

        <?php if ($selectedCohort && !empty($cohortRiders)): ?>
        <div class="filter-group">
            <a href="?cohort=<?= $selectedCohort ?><?= $selectedBrand ? '&brand=' . $selectedBrand : '' ?>&export=csv" class="btn-admin btn-admin-secondary">
                <i data-lucide="download"></i> Exportera CSV
            </a>
        </div>
        <?php endif; ?>
    </form>
</div>

<?php if (isset($error)): ?>
<div class="alert alert-warning">
    <i data-lucide="alert-triangle"></i>
    <div>
        <strong>Fel vid inlasning av data</strong><br>
        <?= htmlspecialchars($error) ?>
    </div>
</div>
<?php elseif (empty($availableCohorts)): ?>
<div class="alert alert-info">
    <i data-lucide="info"></i>
    <div>
        <strong>Ingen data tillganglig</strong><br>
        Kor <a href="/admin/analytics-populate.php">Populate Historical</a> for att generera historisk data.
    </div>
</div>
<?php elseif ($selectedCohort && !empty($cohortRetention)): ?>

<!-- Selected Brand Indicator -->
<?php if ($selectedBrand): ?>
    <?php
    $brandName = '';
    foreach ($allBrands as $b) {
        if ($b['id'] == $selectedBrand) {
            $brandName = $b['name'];
            break;
        }
    }
    ?>
<div class="alert alert-info" style="margin-bottom: var(--space-lg);">
    <i data-lucide="filter"></i>
    <div>
        Visar endast riders som <strong>borjade i <?= htmlspecialchars($brandName) ?></strong>.
        <a href="?cohort=<?= $selectedCohort ?>">Visa alla varumarken</a>
    </div>
</div>
<?php endif; ?>

<!-- Cohort Overview -->
<div class="dashboard-metrics">
    <div class="metric-card metric-card--primary">
        <div class="metric-icon">
            <i data-lucide="users"></i>
        </div>
        <div class="metric-content">
            <div class="metric-value"><?= number_format($cohortStatus['total']) ?></div>
            <div class="metric-label">Kohort <?= $selectedCohort ?><?= $selectedBrand && isset($brandName) ? ' (' . $brandName . ')' : '' ?></div>
        </div>
    </div>

    <div class="metric-card metric-card--success">
        <div class="metric-icon">
            <i data-lucide="check-circle"></i>
        </div>
        <div class="metric-content">
            <div class="metric-value"><?= number_format($cohortStatus['active']) ?></div>
            <div class="metric-label">Fortfarande aktiva (<?= $cohortStatus['active_pct'] ?>%)</div>
        </div>
    </div>

    <div class="metric-card">
        <div class="metric-icon">
            <i data-lucide="calendar"></i>
        </div>
        <div class="metric-content">
            <div class="metric-value"><?= number_format($avgLifespan, 1) ?></div>
            <div class="metric-label">Snitt sasonger</div>
        </div>
    </div>

    <div class="metric-card metric-card--warning">
        <div class="metric-icon">
            <i data-lucide="user-x"></i>
        </div>
        <div class="metric-content">
            <div class="metric-value"><?= number_format($cohortStatus['hard_churn']) ?></div>
            <div class="metric-label">Hard churn (3+ ar)</div>
        </div>
    </div>
</div>

<!-- Feeder Series Breakdown (visas endast när varumärke är valt) -->
<?php if ($feederBreakdown && $feederBreakdown['total_new'] > 0): ?>
<div class="admin-card" style="margin-top: var(--space-lg);">
    <div class="admin-card-header">
        <h2><i data-lucide="git-merge" style="width:20px;height:20px;margin-right:var(--space-sm);"></i> Kohortens ursprung - Varifrån kom de?</h2>
    </div>
    <div class="admin-card-body">
        <div class="feeder-breakdown">
            <div class="feeder-summary" style="display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: var(--space-lg); margin-bottom: var(--space-lg);">
                <div class="feeder-stat" style="text-align: center; padding: var(--space-md); background: var(--color-bg-sunken); border-radius: var(--radius-md);">
                    <div style="font-size: var(--text-2xl); font-weight: var(--weight-bold); color: var(--color-success);"><?= number_format($feederBreakdown['true_rookies']) ?></div>
                    <div style="font-size: var(--text-sm); color: var(--color-text-secondary);">True Rookies</div>
                    <div style="font-size: var(--text-xs); color: var(--color-text-muted);">Helt nya - aldrig tävlat</div>
                </div>
                <div class="feeder-stat" style="text-align: center; padding: var(--space-md); background: var(--color-bg-sunken); border-radius: var(--radius-md);">
                    <div style="font-size: var(--text-2xl); font-weight: var(--weight-bold); color: var(--color-info);"><?= number_format($feederBreakdown['crossover']) ?></div>
                    <div style="font-size: var(--text-sm); color: var(--color-text-secondary);">Crossover</div>
                    <div style="font-size: var(--text-xs); color: var(--color-text-muted);">Från andra serier</div>
                </div>
                <div class="feeder-stat" style="text-align: center; padding: var(--space-md); background: var(--color-bg-sunken); border-radius: var(--radius-md);">
                    <?php $rookiePct = $feederBreakdown['total_new'] > 0 ? round($feederBreakdown['true_rookies'] / $feederBreakdown['total_new'] * 100) : 0; ?>
                    <div style="font-size: var(--text-2xl); font-weight: var(--weight-bold); color: var(--color-text-primary);"><?= $rookiePct ?>%</div>
                    <div style="font-size: var(--text-sm); color: var(--color-text-secondary);">True Rookie Rate</div>
                    <div style="font-size: var(--text-xs); color: var(--color-text-muted);">Helt nya av totalt</div>
                </div>
            </div>

            <?php if (!empty($feederBreakdown['feeder_series'])): ?>
            <h4 style="margin-bottom: var(--space-md);">Crossover-riders kom från:</h4>
            <div class="feeder-sources" style="display: flex; flex-wrap: wrap; gap: var(--space-sm);">
                <?php foreach ($feederBreakdown['feeder_series'] as $feeder): ?>
                <div class="feeder-badge" style="display: inline-flex; align-items: center; gap: var(--space-xs); padding: var(--space-xs) var(--space-sm); background: var(--color-accent-light); border-radius: var(--radius-sm); font-size: var(--text-sm);">
                    <span style="font-weight: var(--weight-semibold);"><?= htmlspecialchars($feeder['brand_name']) ?></span>
                    <span style="background: var(--color-accent); color: white; padding: 2px 6px; border-radius: var(--radius-full); font-size: var(--text-xs);"><?= number_format($feeder['rider_count']) ?></span>
                </div>
                <?php endforeach; ?>
            </div>
            <?php endif; ?>
        </div>
    </div>
</div>
<?php endif; ?>

<!-- Retention Chart -->
<div class="admin-card">
    <div class="admin-card-header">
        <h2>Retention over tid - Kohort <?= $selectedCohort ?><?= $selectedBrand && isset($brandName) ? ' (' . $brandName . ')' : '' ?></h2>
    </div>
    <div class="admin-card-body">
        <div style="max-width: 800px; margin: 0 auto;">
            <canvas id="retentionChart" height="300"></canvas>
        </div>
    </div>
</div>

<!-- Status Breakdown -->
<div class="grid grid-2 grid-gap-lg">
    <div class="admin-card">
        <div class="admin-card-header">
            <h2>Status-fordelning</h2>
        </div>
        <div class="admin-card-body">
            <canvas id="statusChart" height="250"></canvas>
        </div>
    </div>

    <div class="admin-card">
        <div class="admin-card-header">
            <h2>Retention per ar</h2>
        </div>
        <div class="admin-card-body" style="padding: 0;">
            <table class="admin-table">
                <thead>
                    <tr>
                        <th>Ar</th>
                        <th>Ar fran start</th>
                        <th>Aktiva</th>
                        <th>Retention</th>
                    </tr>
                </thead>
                <tbody>
                    <?php foreach ($cohortRetention as $row): ?>
                    <tr>
                        <td><?= $row['year'] ?></td>
                        <td>+<?= $row['years_from_start'] ?></td>
                        <td><?= number_format($row['active_count']) ?></td>
                        <td>
                            <div class="progress-cell">
                                <div class="progress-bar-mini">
                                    <div class="progress-fill" style="width: <?= $row['retention_rate'] ?>%;"></div>
                                </div>
                                <span><?= $row['retention_rate'] ?>%</span>
                            </div>
                        </td>
                    </tr>
                    <?php endforeach; ?>
                </tbody>
            </table>
        </div>
    </div>
</div>

<!-- Cohort Riders List -->
<?php if (!empty($cohortRiders)): ?>
<div class="admin-card">
    <div class="admin-card-header">
        <h2>Riders i kohort <?= $selectedCohort ?><?= $selectedBrand && isset($brandName) ? ' (' . $brandName . ')' : '' ?> (<?= number_format(count($cohortRiders)) ?> st)</h2>
        <div class="filter-inline">
            <label>Filter:</label>
            <select id="statusFilter" onchange="filterRiders(this.value)">
                <option value="all">Alla</option>
                <option value="active">Aktiva</option>
                <option value="soft_churn">Soft churn (1 ar)</option>
                <option value="medium_churn">Medium churn (2 ar)</option>
                <option value="hard_churn">Hard churn (3+ ar)</option>
            </select>
        </div>
    </div>
    <div class="admin-card-body" style="padding: 0;">
        <div class="admin-table-container" style="max-height: 500px; overflow-y: auto;">
            <table class="admin-table" id="ridersTable">
                <thead>
                    <tr>
                        <th>Namn</th>
                        <th>Klubb</th>
                        <th>Forsta Disciplin</th>
                        <th>Sasonger</th>
                        <th>Sista Aktiv</th>
                        <th>Status</th>
                        <th></th>
                    </tr>
                </thead>
                <tbody>
                    <?php foreach (array_slice($cohortRiders, 0, 200) as $rider): ?>
                    <tr data-status="<?= $rider['current_status'] ?>">
                        <td>
                            <a href="/rider/<?= $rider['rider_id'] ?>" class="text-link">
                                <?= htmlspecialchars($rider['firstname'] . ' ' . $rider['lastname']) ?>
                            </a>
                        </td>
                        <td><?= htmlspecialchars($rider['club_name'] ?? '-') ?></td>
                        <td><?= htmlspecialchars($rider['first_discipline'] ?? '-') ?></td>
                        <td><?= $rider['total_seasons'] ?></td>
                        <td><?= $rider['last_active_year'] ?></td>
                        <td>
                            <?php
                            $statusClass = match($rider['current_status']) {
                                'active' => 'badge-success',
                                'soft_churn' => 'badge-warning',
                                'medium_churn' => 'badge-secondary',
                                default => 'badge-danger'
                            };
                            $statusLabel = match($rider['current_status']) {
                                'active' => 'Aktiv',
                                'soft_churn' => '1 ar',
                                'medium_churn' => '2 ar',
                                default => '3+ ar'
                            };
                            ?>
                            <span class="badge <?= $statusClass ?>"><?= $statusLabel ?></span>
                        </td>
                        <td>
                            <a href="/rider/<?= $rider['rider_id'] ?>" class="btn-icon" title="Visa profil">
                                <i data-lucide="external-link"></i>
                            </a>
                        </td>
                    </tr>
                    <?php endforeach; ?>
                </tbody>
            </table>
        </div>
        <?php if (count($cohortRiders) > 200): ?>
        <div class="table-footer">
            <small>Visar 200 av <?= number_format(count($cohortRiders)) ?> riders. Exportera CSV for komplett lista.</small>
        </div>
        <?php endif; ?>
    </div>
</div>
<?php endif; ?>

<!-- Multi-Cohort Comparison -->
<div class="admin-card">
    <div class="admin-card-header">
        <h2>Jamfor kohorter</h2>
    </div>
    <div class="admin-card-body">
        <form method="get" class="compare-form">
            <input type="hidden" name="cohort" value="<?= $selectedCohort ?>">
            <?php if ($selectedBrand): ?>
            <input type="hidden" name="brand" value="<?= $selectedBrand ?>">
            <?php endif; ?>
            <div class="compare-checkboxes">
                <?php
                $recentCohorts = array_slice($availableCohorts, 0, 8);
                foreach ($recentCohorts as $c):
                    $isChecked = in_array($c['cohort_year'], $compareYears);
                ?>
                <label class="compare-checkbox <?= $isChecked ? 'checked' : '' ?>">
                    <input type="checkbox" name="compare[]" value="<?= $c['cohort_year'] ?>" <?= $isChecked ? 'checked' : '' ?>>
                    <?= $c['cohort_year'] ?> (<?= $c['cohort_size'] ?>)
                </label>
                <?php endforeach; ?>
            </div>
            <button type="submit" class="btn-admin btn-admin-primary">
                <i data-lucide="bar-chart-2"></i> Jamfor valda
            </button>
        </form>

        <?php if (!empty($cohortComparison)): ?>
        <div style="margin-top: var(--space-xl);">
            <canvas id="comparisonChart" height="300"></canvas>
        </div>
        <?php endif; ?>
    </div>
</div>

<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<script>
document.addEventListener('DOMContentLoaded', function() {
    // Retention Chart
    const retentionCtx = document.getElementById('retentionChart');
    if (retentionCtx) {
        new Chart(retentionCtx, {
            type: 'line',
            data: {
                labels: <?= json_encode(array_column($cohortRetention, 'year')) ?>,
                datasets: [{
                    label: 'Retention %',
                    data: <?= json_encode(array_column($cohortRetention, 'retention_rate')) ?>,
                    borderColor: 'rgb(55, 212, 214)',
                    backgroundColor: 'rgba(55, 212, 214, 0.1)',
                    fill: true,
                    tension: 0.3,
                    pointRadius: 6,
                    pointHoverRadius: 8
                }, {
                    label: 'Aktiva',
                    data: <?= json_encode(array_column($cohortRetention, 'active_count')) ?>,
                    borderColor: 'rgb(16, 185, 129)',
                    backgroundColor: 'rgba(16, 185, 129, 0.1)',
                    fill: false,
                    tension: 0.3,
                    yAxisID: 'y1'
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: { position: 'bottom' }
                },
                scales: {
                    y: {
                        min: 0,
                        max: 100,
                        title: { display: true, text: 'Retention %' }
                    },
                    y1: {
                        position: 'right',
                        min: 0,
                        title: { display: true, text: 'Antal aktiva' },
                        grid: { drawOnChartArea: false }
                    }
                }
            }
        });
    }

    // Status Donut Chart
    const statusCtx = document.getElementById('statusChart');
    if (statusCtx) {
        new Chart(statusCtx, {
            type: 'doughnut',
            data: {
                labels: ['Aktiva', 'Soft churn (1 ar)', 'Medium churn (2 ar)', 'Hard churn (3+ ar)'],
                datasets: [{
                    data: [
                        <?= $cohortStatus['active'] ?>,
                        <?= $cohortStatus['soft_churn'] ?>,
                        <?= $cohortStatus['medium_churn'] ?>,
                        <?= $cohortStatus['hard_churn'] ?>
                    ],
                    backgroundColor: [
                        'rgb(16, 185, 129)',
                        'rgb(251, 191, 36)',
                        'rgb(156, 163, 175)',
                        'rgb(239, 68, 68)'
                    ]
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: { position: 'bottom' }
                }
            }
        });
    }

    <?php if (!empty($cohortComparison)): ?>
    // Comparison Chart
    const compCtx = document.getElementById('comparisonChart');
    if (compCtx) {
        const colors = [
            'rgb(55, 212, 214)',
            'rgb(16, 185, 129)',
            'rgb(251, 191, 36)',
            'rgb(239, 68, 68)',
            'rgb(139, 92, 246)'
        ];

        const datasets = [];
        let colorIdx = 0;

        <?php foreach ($cohortComparison as $year => $data): ?>
        datasets.push({
            label: 'Kohort <?= $year ?>',
            data: <?= json_encode(array_column($data['retention_data'], 'retention_rate')) ?>,
            borderColor: colors[colorIdx % colors.length],
            fill: false,
            tension: 0.3
        });
        colorIdx++;
        <?php endforeach; ?>

        new Chart(compCtx, {
            type: 'line',
            data: {
                labels: ['Ar 0', 'Ar 1', 'Ar 2', 'Ar 3', 'Ar 4'],
                datasets: datasets
            },
            options: {
                responsive: true,
                plugins: {
                    title: { display: true, text: 'Retention jamforelse (% kvar efter X ar)' },
                    legend: { position: 'bottom' }
                },
                scales: {
                    y: { min: 0, max: 100, title: { display: true, text: '%' } }
                }
            }
        });
    }
    <?php endif; ?>
});

// Filter riders table
function filterRiders(status) {
    const rows = document.querySelectorAll('#ridersTable tbody tr');
    rows.forEach(row => {
        if (status === 'all' || row.dataset.status === status) {
            row.style.display = '';
        } else {
            row.style.display = 'none';
        }
    });
}
</script>

<?php endif; ?>

<style>
/* Info Box */
.info-box {
    display: flex;
    gap: var(--space-md);
    padding: var(--space-md);
    margin-bottom: var(--space-lg);
    background: var(--color-accent-light);
    border: 1px solid var(--color-accent);
    border-radius: var(--radius-md);
}

.info-box-icon {
    flex-shrink: 0;
    width: 32px;
    height: 32px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: var(--color-accent);
    border-radius: var(--radius-sm);
    color: white;
}

.info-box-icon i {
    width: 18px;
    height: 18px;
}

.info-box-content {
    flex: 1;
}

.info-box-content strong {
    display: block;
    margin-bottom: var(--space-xs);
    color: var(--color-text-primary);
}

.info-box-content p {
    margin: 0;
    font-size: var(--text-sm);
    color: var(--color-text-secondary);
    line-height: 1.5;
}

/* Filter Bar */
.filter-bar {
    display: flex;
    gap: var(--space-lg);
    margin-bottom: var(--space-xl);
    padding: var(--space-md);
    background: var(--color-bg-card);
    border: 1px solid var(--color-border);
    border-radius: var(--radius-md);
}

.filter-form {
    display: flex;
    gap: var(--space-lg);
    align-items: flex-end;
    flex-wrap: wrap;
}

.filter-group {
    display: flex;
    flex-direction: column;
    gap: var(--space-xs);
}

.filter-label {
    font-size: var(--text-sm);
    color: var(--color-text-secondary);
    font-weight: var(--weight-medium);
}

.filter-inline {
    display: flex;
    gap: var(--space-sm);
    align-items: center;
}

.filter-inline label {
    font-size: var(--text-sm);
    color: var(--color-text-secondary);
}

/* Dashboard Metrics Grid */
.dashboard-metrics {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: var(--space-md);
    margin-bottom: var(--space-xl);
}

/* Metric Cards */
.metric-card {
    display: flex;
    align-items: flex-start;
    gap: var(--space-md);
    padding: var(--space-lg);
    background: var(--color-bg-card);
    border: 1px solid var(--color-border);
    border-radius: var(--radius-md);
}

.metric-card--primary {
    border-left: 3px solid var(--color-accent);
}

.metric-card--success {
    border-left: 3px solid var(--color-success);
}

.metric-card--warning {
    border-left: 3px solid var(--color-warning);
}

.metric-icon {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 40px;
    height: 40px;
    background: var(--color-bg-hover);
    border-radius: var(--radius-md);
    color: var(--color-accent);
    flex-shrink: 0;
}

.metric-icon i {
    width: 20px;
    height: 20px;
}

.metric-content {
    flex: 1;
    min-width: 0;
}

.metric-value {
    font-size: var(--text-2xl);
    font-weight: var(--weight-bold);
    color: var(--color-text-primary);
    line-height: 1.2;
}

.metric-label {
    font-size: var(--text-sm);
    color: var(--color-text-secondary);
    margin-top: var(--space-2xs);
}

/* Progress Cell */
.progress-cell {
    display: flex;
    align-items: center;
    gap: var(--space-sm);
}

.progress-bar-mini {
    width: 80px;
    height: 6px;
    background: var(--color-bg-hover);
    border-radius: var(--radius-full);
    overflow: hidden;
}

.progress-fill {
    height: 100%;
    background: var(--color-success);
    border-radius: var(--radius-full);
}

/* Compare Form */
.compare-form {
    display: flex;
    flex-direction: column;
    gap: var(--space-md);
}

.compare-checkboxes {
    display: flex;
    flex-wrap: wrap;
    gap: var(--space-sm);
}

.compare-checkbox {
    display: flex;
    align-items: center;
    gap: var(--space-xs);
    padding: var(--space-sm) var(--space-md);
    background: var(--color-bg-surface);
    border: 1px solid var(--color-border);
    border-radius: var(--radius-md);
    cursor: pointer;
    font-size: var(--text-sm);
    transition: all 0.15s ease;
}

.compare-checkbox:hover {
    border-color: var(--color-accent);
}

.compare-checkbox.checked,
.compare-checkbox:has(input:checked) {
    background: var(--color-accent-light);
    border-color: var(--color-accent);
}

.compare-checkbox input {
    margin: 0;
}

/* Table Footer */
.table-footer {
    padding: var(--space-md);
    text-align: center;
    color: var(--color-text-muted);
    border-top: 1px solid var(--color-border);
}

/* Grid */
.grid-2 {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
}

.grid-gap-lg {
    gap: var(--space-lg);
    margin-bottom: var(--space-xl);
}

/* Text link */
.text-link {
    color: var(--color-accent);
    text-decoration: none;
    font-weight: var(--weight-medium);
}

.text-link:hover {
    text-decoration: underline;
}

/* Button icon */
.btn-icon {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 32px;
    height: 32px;
    border-radius: var(--radius-sm);
    color: var(--color-text-muted);
    transition: all 0.15s ease;
}

.btn-icon:hover {
    background: var(--color-bg-hover);
    color: var(--color-accent);
}

.btn-icon i {
    width: 16px;
    height: 16px;
}

/* Responsive */
@media (max-width: 899px) {
    .grid-2 {
        grid-template-columns: 1fr;
    }
}

@media (max-width: 767px) {
    /* Edge-to-edge for all cards and components */
    .filter-bar,
    .admin-card,
    .alert,
    .info-box {
        margin-left: -16px;
        margin-right: -16px;
        border-radius: 0 !important;
        border-left: none !important;
        border-right: none !important;
        width: calc(100% + 32px);
    }

    .filter-form {
        flex-direction: column;
        width: 100%;
    }

    .filter-group {
        width: 100%;
    }

    .filter-group select {
        width: 100%;
    }

    .compare-form button {
        width: 100%;
    }

    /* Dashboard metrics - horizontal scroll */
    .dashboard-metrics {
        display: flex;
        gap: var(--space-sm);
        overflow-x: auto;
        padding-bottom: var(--space-sm);
        margin-left: -16px;
        margin-right: -16px;
        padding-left: 16px;
        padding-right: 16px;
        -webkit-overflow-scrolling: touch;
        scrollbar-width: none;
    }

    .dashboard-metrics::-webkit-scrollbar {
        display: none;
    }

    .metric-card {
        flex: 0 0 auto;
        min-width: 140px;
    }

    /* Table adjustments for mobile */
    .admin-table th,
    .admin-table td {
        padding: var(--space-sm);
        font-size: var(--text-sm);
    }

    /* Hide less important columns on mobile */
    .admin-table th:nth-child(3),
    .admin-table td:nth-child(3),
    .admin-table th:nth-child(7),
    .admin-table td:nth-child(7) {
        display: none;
    }

    /* Chart sizing */
    canvas {
        max-height: 250px !important;
    }

    /* Compare checkboxes - full width scroll */
    .compare-checkboxes {
        overflow-x: auto;
        flex-wrap: nowrap;
        padding-bottom: var(--space-sm);
        -webkit-overflow-scrolling: touch;
    }

    .compare-checkbox {
        flex: 0 0 auto;
        white-space: nowrap;
    }

    /* Progress bar mini - smaller on mobile */
    .progress-bar-mini {
        width: 50px;
    }

    /* Grid gap adjustment */
    .grid-gap-lg {
        gap: var(--space-md);
    }
}

/* Extra small screens */
@media (max-width: 479px) {
    .metric-card {
        min-width: 120px;
        padding: var(--space-sm);
    }

    .metric-value {
        font-size: var(--text-lg);
    }

    .metric-label {
        font-size: var(--text-xs);
    }

    /* Hide even more columns */
    .admin-table th:nth-child(2),
    .admin-table td:nth-child(2) {
        display: none;
    }
}
</style>

<?php include __DIR__ . '/components/unified-layout-footer.php'; ?>
