<?php
/**
 * Analytics - At-Risk / Churn Prediction
 *
 * Identifierar riders med hog risk att sluta
 * baserat pa aktivitetsmonster och riskfaktorer.
 *
 * Behorighet: super_admin ELLER statistics-permission
 * GDPR: Admin-only, personlig data
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

// Hamta tillgangliga ar (gor detta forst for att kunna satta default)
$availableYears = [];
try {
    $stmt = $pdo->query("SELECT DISTINCT season_year FROM rider_yearly_stats ORDER BY season_year DESC");
    $availableYears = $stmt->fetchAll(PDO::FETCH_COLUMN);
} catch (Exception $e) {
    $currentYear = (int)date('Y');
    $availableYears = range($currentYear, $currentYear - 5);
}

// Arval - default till senaste ar MED DATA (inte kalenderaret)
// Viktigt: At-Risk analys baseras pa avslutade sasonger
$latestDataYear = !empty($availableYears) ? (int)$availableYears[0] : (int)date('Y') - 1;
$selectedYear = isset($_GET['year']) ? (int)$_GET['year'] : $latestDataYear;
$filterLevel = $_GET['level'] ?? 'all';
$filterSeries = isset($_GET['series']) ? (int)$_GET['series'] : null;

// Hamta serier for filter
$seriesList = [];
try {
    $stmt = $pdo->query("SELECT id, name FROM series WHERE active = 1 ORDER BY name");
    $seriesList = $stmt->fetchAll(PDO::FETCH_ASSOC);
} catch (Exception $e) {}

// Initiera KPI Calculator
$kpiCalc = new KPICalculator($pdo);

// Hamta data
$atRiskRiders = [];
$riskDistribution = [];
$cacheInfo = null;

try {
    $riskDistribution = $kpiCalc->getRiskDistribution($selectedYear);
    $atRiskRiders = $kpiCalc->getAtRiskRiders($selectedYear, 200);

    // Filtrera pa risk level
    if ($filterLevel !== 'all') {
        $atRiskRiders = array_filter($atRiskRiders, fn($r) => $r['risk_level'] === $filterLevel);
    }

    // Filtrera pa serie
    if ($filterSeries) {
        $atRiskRiders = array_filter($atRiskRiders, fn($r) => ($r['primary_series_id'] ?? null) == $filterSeries);
    }

    // Kolla cache-info
    $stmt = $pdo->prepare("SELECT MAX(calculated_at) FROM rider_risk_scores WHERE season_year = ?");
    $stmt->execute([$selectedYear]);
    $cacheTime = $stmt->fetchColumn();
    if ($cacheTime) {
        $cacheInfo = "Beraknad: " . date('Y-m-d H:i', strtotime($cacheTime));
    }
} catch (Exception $e) {
    $error = $e->getMessage();
}

// Export
if (isset($_GET['export']) && $_GET['export'] === 'csv' && !isset($error)) {
    header('Content-Type: text/csv; charset=utf-8');
    header('Content-Disposition: attachment; filename="thehub-atrisk-' . $selectedYear . '.csv"');
    $output = fopen('php://output', 'w');
    fprintf($output, chr(0xEF).chr(0xBB).chr(0xBF));

    fputcsv($output, ['Rider ID', 'Fornamn', 'Efternamn', 'Klubb', 'Risk Score', 'Risk Level', 'Disciplin', 'Serie', 'Events', 'Faktorer', 'Profil']);
    foreach ($atRiskRiders as $rider) {
        $factorList = [];
        if (!empty($rider['factors'])) {
            foreach ($rider['factors'] as $key => $f) {
                $factorList[] = $key . ':' . ($f['score'] ?? 0);
            }
        }
        fputcsv($output, [
            $rider['rider_id'],
            $rider['firstname'],
            $rider['lastname'],
            $rider['club_name'] ?? '',
            $rider['risk_score'],
            $rider['risk_level'],
            $rider['primary_discipline'] ?? '',
            $rider['series_name'] ?? '',
            $rider['total_events'] ?? '',
            implode(', ', $factorList),
            'https://thehub.se/rider/' . $rider['rider_id']
        ]);
    }
    fclose($output);

    try {
        $stmt = $pdo->prepare("INSERT INTO analytics_exports (export_type, export_params, exported_by, row_count, ip_address) VALUES (?, ?, ?, ?, ?)");
        $stmt->execute(['at_risk', json_encode(['year' => $selectedYear, 'level' => $filterLevel]), $_SESSION['user_id'] ?? null, count($atRiskRiders), $_SERVER['REMOTE_ADDR'] ?? null]);
    } catch (Exception $e) {}

    exit;
}

// Page config
$page_title = 'At-Risk Analys';
$breadcrumbs = [
    ['label' => 'Analytics', 'url' => '/admin/analytics-dashboard.php'],
    ['label' => 'At-Risk']
];

$page_actions = '
<div class="btn-group">
    <a href="/admin/analytics-dashboard.php" class="btn-admin btn-admin-secondary">
        <i data-lucide="arrow-left"></i> Dashboard
    </a>
</div>
';

include __DIR__ . '/components/unified-layout.php';
?>

<!-- Info Box - Forklaring -->
<div class="info-box">
    <div class="info-box-icon">
        <i data-lucide="alert-triangle"></i>
    </div>
    <div class="info-box-content">
        <strong>Vad ar At-Risk?</strong>
        <p>At-Risk identifierar riders som riskerar att sluta. Systemet analyserar 6 faktorer: minskande deltagande, ingen recent aktivitet, klassnedflytt, enbart en serie, kort karriar och hog alder i klassen. Varje faktor ger poang (0-100) - ju hogre, desto storre risk att de slutar.</p>
    </div>
</div>

<!-- Year/Filter Selector -->
<div class="filter-bar">
    <form method="get" class="filter-form">
        <div class="filter-group">
            <label class="filter-label">Sasong</label>
            <select name="year" class="form-select" onchange="this.form.submit()">
                <?php foreach ($availableYears as $year): ?>
                    <option value="<?= $year ?>" <?= $year == $selectedYear ? 'selected' : '' ?>>
                        <?= $year ?>
                    </option>
                <?php endforeach; ?>
            </select>
        </div>

        <div class="filter-group">
            <label class="filter-label">Riskniva</label>
            <select name="level" class="form-select" onchange="this.form.submit()">
                <option value="all" <?= $filterLevel === 'all' ? 'selected' : '' ?>>Alla</option>
                <option value="critical" <?= $filterLevel === 'critical' ? 'selected' : '' ?>>Kritisk (70+)</option>
                <option value="high" <?= $filterLevel === 'high' ? 'selected' : '' ?>>Hog (50-69)</option>
                <option value="medium" <?= $filterLevel === 'medium' ? 'selected' : '' ?>>Medium (30-49)</option>
                <option value="low" <?= $filterLevel === 'low' ? 'selected' : '' ?>>Lag (0-29)</option>
            </select>
        </div>

        <div class="filter-group">
            <label class="filter-label">Serie</label>
            <select name="series" class="form-select" onchange="this.form.submit()">
                <option value="">Alla serier</option>
                <?php foreach ($seriesList as $s): ?>
                    <option value="<?= $s['id'] ?>" <?= $filterSeries == $s['id'] ? 'selected' : '' ?>>
                        <?= htmlspecialchars($s['name']) ?>
                    </option>
                <?php endforeach; ?>
            </select>
        </div>

        <?php if (!empty($atRiskRiders)): ?>
        <div class="filter-group">
            <a href="?year=<?= $selectedYear ?>&level=<?= $filterLevel ?>&series=<?= $filterSeries ?>&export=csv" class="btn-admin btn-admin-secondary">
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
        <strong>Fel vid inlasning</strong><br>
        <?= htmlspecialchars($error) ?>
    </div>
</div>
<?php else: ?>

<!-- Cache Info -->
<?php if ($cacheInfo): ?>
<div class="cache-info">
    <i data-lucide="database"></i>
    <?= $cacheInfo ?>
    <a href="/admin/analytics-populate.php?action=risk" class="refresh-link">Uppdatera</a>
</div>
<?php elseif (isset($riskDistribution['cache_missing']) && $riskDistribution['cache_missing']): ?>
<div class="alert alert-info">
    <i data-lucide="info"></i>
    <div>
        <strong>Risk-scores ej beraknade</strong><br>
        Kor cron-jobbet eller <a href="/admin/analytics-populate.php">Populate</a> for att generera risk-data.
    </div>
</div>
<?php endif; ?>

<!-- Risk Distribution Overview -->
<div class="dashboard-metrics">
    <div class="metric-card metric-card--danger">
        <div class="metric-icon">
            <i data-lucide="alert-circle"></i>
        </div>
        <div class="metric-content">
            <div class="metric-value"><?= number_format($riskDistribution['critical'] ?? 0) ?></div>
            <div class="metric-label">Kritisk risk (70+)</div>
        </div>
    </div>

    <div class="metric-card metric-card--warning">
        <div class="metric-icon">
            <i data-lucide="alert-triangle"></i>
        </div>
        <div class="metric-content">
            <div class="metric-value"><?= number_format($riskDistribution['high'] ?? 0) ?></div>
            <div class="metric-label">Hog risk (50-69)</div>
        </div>
    </div>

    <div class="metric-card">
        <div class="metric-icon">
            <i data-lucide="minus-circle"></i>
        </div>
        <div class="metric-content">
            <div class="metric-value"><?= number_format($riskDistribution['medium'] ?? 0) ?></div>
            <div class="metric-label">Medium risk (30-49)</div>
        </div>
    </div>

    <div class="metric-card metric-card--success">
        <div class="metric-icon">
            <i data-lucide="check-circle"></i>
        </div>
        <div class="metric-content">
            <div class="metric-value"><?= number_format($riskDistribution['low'] ?? 0) ?></div>
            <div class="metric-label">Lag risk (0-29)</div>
        </div>
    </div>
</div>

<!-- Risk Distribution Chart -->
<div class="grid grid-2 grid-gap-lg">
    <div class="admin-card">
        <div class="admin-card-header">
            <h2>Risk-fordelning <?= $selectedYear ?></h2>
        </div>
        <div class="admin-card-body">
            <canvas id="riskDistChart" height="250"></canvas>
        </div>
    </div>

    <div class="admin-card">
        <div class="admin-card-header">
            <h2>Riskfaktorer (konfiguration)</h2>
        </div>
        <div class="admin-card-body">
            <div class="factor-list">
                <?php foreach (AnalyticsConfig::RISK_FACTORS as $key => $factor): ?>
                <div class="factor-item <?= $factor['enabled'] ? '' : 'disabled' ?>">
                    <div class="factor-header">
                        <span class="factor-name"><?= htmlspecialchars($key) ?></span>
                        <span class="factor-weight"><?= $factor['weight'] ?> poang</span>
                    </div>
                    <div class="factor-desc"><?= htmlspecialchars($factor['description']) ?></div>
                    <?php if (!$factor['enabled']): ?>
                    <span class="badge badge-secondary">Inaktiverad</span>
                    <?php endif; ?>
                </div>
                <?php endforeach; ?>
            </div>
        </div>
    </div>
</div>

<!-- At-Risk Riders List -->
<?php if (!empty($atRiskRiders)): ?>
<div class="admin-card">
    <div class="admin-card-header">
        <h2>At-Risk Riders (<?= number_format(count($atRiskRiders)) ?> st)</h2>
    </div>
    <div class="admin-card-body" style="padding: 0;">
        <div class="admin-table-container">
            <table class="admin-table">
                <thead>
                    <tr>
                        <th>Risk</th>
                        <th>Namn</th>
                        <th>Klubb</th>
                        <th>Serie</th>
                        <th>Events</th>
                        <th>Riskfaktorer</th>
                        <th></th>
                    </tr>
                </thead>
                <tbody>
                    <?php foreach ($atRiskRiders as $rider): ?>
                    <tr>
                        <td>
                            <?php
                            $levelClass = match($rider['risk_level']) {
                                'critical' => 'badge-danger',
                                'high' => 'badge-warning',
                                'medium' => 'badge-secondary',
                                default => 'badge-success'
                            };
                            ?>
                            <div class="risk-cell">
                                <span class="risk-score"><?= $rider['risk_score'] ?></span>
                                <span class="badge <?= $levelClass ?>"><?= ucfirst($rider['risk_level']) ?></span>
                            </div>
                        </td>
                        <td>
                            <a href="/rider/<?= $rider['rider_id'] ?>" class="text-link">
                                <?= htmlspecialchars($rider['firstname'] . ' ' . $rider['lastname']) ?>
                            </a>
                        </td>
                        <td><?= htmlspecialchars($rider['club_name'] ?? '-') ?></td>
                        <td><?= htmlspecialchars($rider['series_name'] ?? '-') ?></td>
                        <td><?= $rider['total_events'] ?? '-' ?></td>
                        <td>
                            <div class="factor-chips">
                                <?php if (!empty($rider['declining_events'])): ?>
                                <span class="chip chip-warning" title="Minskande events">
                                    <i data-lucide="trending-down"></i> Events
                                </span>
                                <?php endif; ?>
                                <?php if (!empty($rider['single_series'])): ?>
                                <span class="chip" title="Endast en serie">
                                    <i data-lucide="box"></i> 1 serie
                                </span>
                                <?php endif; ?>
                                <?php if (!empty($rider['low_tenure'])): ?>
                                <span class="chip" title="Kort karriar">
                                    <i data-lucide="clock"></i> Kort
                                </span>
                                <?php endif; ?>
                                <?php if (!empty($rider['no_recent_activity'])): ?>
                                <span class="chip chip-danger" title="Ingen aktivitet">
                                    <i data-lucide="pause"></i> Inaktiv
                                </span>
                                <?php endif; ?>
                                <?php if (!empty($rider['class_downgrade'])): ?>
                                <span class="chip chip-warning" title="Klassnedflytt">
                                    <i data-lucide="arrow-down"></i> Klass
                                </span>
                                <?php endif; ?>
                            </div>
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
    </div>
</div>
<?php else: ?>
<div class="alert alert-info">
    <i data-lucide="info"></i>
    <div>Inga riders matchar filtret.</div>
</div>
<?php endif; ?>

<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<script>
document.addEventListener('DOMContentLoaded', function() {
    const ctx = document.getElementById('riskDistChart');
    if (ctx) {
        new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: ['Kritisk (70+)', 'Hog (50-69)', 'Medium (30-49)', 'Lag (0-29)'],
                datasets: [{
                    data: [
                        <?= $riskDistribution['critical'] ?? 0 ?>,
                        <?= $riskDistribution['high'] ?? 0 ?>,
                        <?= $riskDistribution['medium'] ?? 0 ?>,
                        <?= $riskDistribution['low'] ?? 0 ?>
                    ],
                    backgroundColor: [
                        'rgb(239, 68, 68)',
                        'rgb(251, 191, 36)',
                        'rgb(156, 163, 175)',
                        'rgb(16, 185, 129)'
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
});
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
    background: var(--color-warning);
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

/* Dashboard Metrics Grid */
.dashboard-metrics {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
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

.metric-card--danger {
    border-left: 3px solid var(--color-error);
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

/* Cache Info */
.cache-info {
    display: flex;
    align-items: center;
    gap: var(--space-sm);
    padding: var(--space-sm) var(--space-md);
    margin-bottom: var(--space-lg);
    background: var(--color-bg-surface);
    border-radius: var(--radius-md);
    font-size: var(--text-sm);
    color: var(--color-text-secondary);
}

.cache-info i {
    width: 16px;
    height: 16px;
}

.refresh-link {
    margin-left: auto;
    color: var(--color-accent);
}

/* Metric Card Variants */
.metric-card--danger {
    border-left: 3px solid var(--color-error);
}

.metric-card--danger .metric-value {
    color: var(--color-error);
}

/* Risk Cell */
.risk-cell {
    display: flex;
    align-items: center;
    gap: var(--space-sm);
}

.risk-score {
    font-weight: var(--weight-bold);
    font-size: var(--text-lg);
}

/* Factor List */
.factor-list {
    display: flex;
    flex-direction: column;
    gap: var(--space-sm);
}

.factor-item {
    padding: var(--space-sm);
    background: var(--color-bg-surface);
    border-radius: var(--radius-sm);
}

.factor-item.disabled {
    opacity: 0.5;
}

.factor-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: var(--space-2xs);
}

.factor-name {
    font-weight: var(--weight-medium);
    font-size: var(--text-sm);
}

.factor-weight {
    font-size: var(--text-xs);
    color: var(--color-accent);
    font-weight: var(--weight-bold);
}

.factor-desc {
    font-size: var(--text-xs);
    color: var(--color-text-muted);
}

/* Factor Chips */
.factor-chips {
    display: flex;
    flex-wrap: wrap;
    gap: 4px;
}

.chip {
    display: inline-flex;
    align-items: center;
    gap: 4px;
    padding: 2px 8px;
    background: var(--color-bg-hover);
    border-radius: var(--radius-full);
    font-size: 11px;
    color: var(--color-text-secondary);
}

.chip i {
    width: 12px;
    height: 12px;
}

.chip-warning {
    background: rgba(251, 191, 36, 0.15);
    color: var(--color-warning);
}

.chip-danger {
    background: rgba(239, 68, 68, 0.15);
    color: var(--color-error);
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
    .cache-info,
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
        min-width: 130px;
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
    .admin-table th:nth-child(5),
    .admin-table td:nth-child(5) {
        display: none;
    }

    /* Risk score - more compact */
    .risk-cell {
        flex-direction: column;
        gap: 4px;
    }

    .risk-score {
        font-size: var(--text-base);
    }

    /* Factor chips - wrap more */
    .factor-chips {
        gap: 2px;
    }

    .chip {
        padding: 2px 6px;
        font-size: 10px;
    }

    /* Chart sizing */
    canvas {
        max-height: 200px !important;
    }

    /* Factor list in card */
    .factor-item {
        padding: var(--space-xs);
    }

    .factor-name {
        font-size: var(--text-xs);
    }

    /* Grid gap adjustment */
    .grid-gap-lg {
        gap: var(--space-md);
    }
}

/* Extra small screens */
@media (max-width: 479px) {
    .metric-card {
        min-width: 110px;
        padding: var(--space-sm);
    }

    .metric-value {
        font-size: var(--text-lg);
    }

    .metric-label {
        font-size: var(--text-xs);
    }

    /* Hide even more columns */
    .admin-table th:nth-child(4),
    .admin-table td:nth-child(4) {
        display: none;
    }

    /* Factor chips hidden on extra small */
    .factor-chips {
        display: none;
    }
}
</style>

<?php include __DIR__ . '/components/unified-layout-footer.php'; ?>
