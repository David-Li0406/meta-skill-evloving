<?php
/**
 * Analytics - Brand Health Report
 *
 * Komplett rapport för ett varumärke med:
 * - Historiska trender
 * - Retention & Churn
 * - Feeder-analys (varifrån kommer nya?)
 * - Exit-analys (vart går de som slutar?)
 * - Cross-participation
 *
 * @package TheHUB Analytics
 * @version 1.0
 */
require_once __DIR__ . '/../config.php';
require_once __DIR__ . '/../includes/auth.php';
require_once __DIR__ . '/../analytics/includes/KPICalculator.php';

requireAnalyticsAccess();

global $pdo;

// Parameters
$currentYear = (int)date('Y');
$selectedYear = isset($_GET['year']) ? (int)$_GET['year'] : $currentYear - 1;
$selectedBrand = isset($_GET['brand']) && $_GET['brand'] !== '' ? (int)$_GET['brand'] : null;
$numYears = isset($_GET['years']) ? max(3, min(15, (int)$_GET['years'])) : 5;

// Initialize
$kpiCalc = new KPICalculator($pdo);

// Get all brands
$allBrands = [];
try {
    $allBrands = $kpiCalc->getAllBrands();
} catch (Exception $e) {}

// Get selected brand info
$brandName = 'Alla varumärken';
$brandColor = '#0066CC';
if ($selectedBrand) {
    foreach ($allBrands as $b) {
        if ($b['id'] == $selectedBrand) {
            $brandName = $b['name'];
            $brandColor = $b['accent_color'] ?? $b['gradient_start'] ?? '#0066CC';
            break;
        }
    }
}

// Collect all data
$reportData = [
    'brand' => $brandName,
    'year' => $selectedYear,
    'trends' => [],
    'current_kpis' => [],
    'feeder_breakdown' => null,
    'exit_analysis' => null,
    'age_distribution' => [],
    'gender_distribution' => [],
    'top_feeder_brands' => [],
    'top_exit_brands' => []
];

try {
    // Current year KPIs
    $reportData['current_kpis'] = $kpiCalc->getAllKPIs($selectedYear, $selectedBrand);

    // Multi-year trends
    $years = range($selectedYear - $numYears + 1, $selectedYear);
    foreach ($years as $year) {
        $yearKpis = $kpiCalc->getAllKPIs($year, $selectedBrand);
        $reportData['trends'][] = [
            'year' => $year,
            'total_riders' => $yearKpis['total_riders'] ?? 0,
            'new_riders' => $yearKpis['new_riders'] ?? 0,
            'retained_riders' => $yearKpis['retained_riders'] ?? 0,
            'retention_rate' => $yearKpis['retention_rate'] ?? 0,
            'churn_rate' => $yearKpis['churn_rate'] ?? 0,
            'growth_rate' => $yearKpis['growth_rate'] ?? 0,
            'cross_participation' => $yearKpis['cross_participation_rate'] ?? 0
        ];
    }

    // Feeder and exit analysis (only for specific brand)
    if ($selectedBrand) {
        $reportData['feeder_breakdown'] = $kpiCalc->getFeederSeriesBreakdown($selectedYear, $selectedBrand);
        $reportData['exit_analysis'] = $kpiCalc->getExitDestinationAnalysis($selectedYear, $selectedBrand);
    }

    // Demographics
    $reportData['age_distribution'] = $kpiCalc->getAgeDistribution($selectedYear, $selectedBrand);
    $reportData['gender_distribution'] = $kpiCalc->getGenderDistribution($selectedYear, $selectedBrand);

} catch (Exception $e) {
    $error = $e->getMessage();
}

// Calculate summary stats
$firstYear = $reportData['trends'][0] ?? null;
$lastYear = $reportData['trends'][count($reportData['trends']) - 1] ?? null;
$totalGrowth = 0;
$avgRetention = 0;

if ($firstYear && $lastYear && $firstYear['total_riders'] > 0) {
    $totalGrowth = round(($lastYear['total_riders'] - $firstYear['total_riders']) / $firstYear['total_riders'] * 100, 1);
}

if (!empty($reportData['trends'])) {
    $retentionRates = array_column($reportData['trends'], 'retention_rate');
    $avgRetention = round(array_sum($retentionRates) / count($retentionRates), 1);
}

// Page config
$page_title = 'Brand Health Report: ' . $brandName;
include __DIR__ . '/components/unified-layout.php';
?>

<style>
/* Report Styles */
.report-header {
    background: linear-gradient(135deg, <?= htmlspecialchars($brandColor) ?>, <?= htmlspecialchars($brandColor) ?>dd);
    color: white;
    padding: var(--space-xl);
    border-radius: var(--radius-lg);
    margin-bottom: var(--space-xl);
}

.report-header h1 {
    font-family: var(--font-heading);
    font-size: var(--text-3xl);
    margin: 0 0 var(--space-sm);
}

.report-header .subtitle {
    opacity: 0.9;
    font-size: var(--text-lg);
}

.report-section {
    margin-bottom: var(--space-xl);
}

.report-section h2 {
    font-family: var(--font-heading-secondary);
    font-size: var(--text-xl);
    color: var(--color-text-primary);
    margin: 0 0 var(--space-md);
    padding-bottom: var(--space-sm);
    border-bottom: 2px solid <?= htmlspecialchars($brandColor) ?>;
}

.summary-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: var(--space-md);
    margin-bottom: var(--space-xl);
}

.summary-card {
    background: var(--color-bg-card);
    border: 1px solid var(--color-border);
    border-radius: var(--radius-md);
    padding: var(--space-lg);
    text-align: center;
}

.summary-card .value {
    font-size: var(--text-3xl);
    font-weight: var(--weight-bold);
    color: <?= htmlspecialchars($brandColor) ?>;
    line-height: 1.2;
}

.summary-card .label {
    font-size: var(--text-sm);
    color: var(--color-text-secondary);
    margin-top: var(--space-xs);
}

.summary-card .change {
    font-size: var(--text-xs);
    margin-top: var(--space-xs);
    padding: 2px 8px;
    border-radius: var(--radius-full);
    display: inline-block;
}

.summary-card .change.positive {
    background: rgba(16, 185, 129, 0.1);
    color: var(--color-success);
}

.summary-card .change.negative {
    background: rgba(239, 68, 68, 0.1);
    color: var(--color-error);
}

/* Trend Chart */
.trend-chart {
    background: var(--color-bg-card);
    border: 1px solid var(--color-border);
    border-radius: var(--radius-md);
    padding: var(--space-lg);
}

.trend-bars {
    display: flex;
    align-items: flex-end;
    justify-content: space-around;
    height: 200px;
    gap: var(--space-sm);
    margin-top: var(--space-md);
}

.trend-bar-group {
    flex: 1;
    display: flex;
    flex-direction: column;
    align-items: center;
    max-width: 80px;
}

.trend-bar-stack {
    width: 100%;
    height: 160px;
    display: flex;
    flex-direction: column;
    justify-content: flex-end;
    gap: 2px;
}

.trend-bar {
    width: 100%;
    border-radius: var(--radius-sm) var(--radius-sm) 0 0;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: var(--text-xs);
    font-weight: 600;
    color: white;
    min-height: 4px;
}

.trend-bar.new { background: <?= htmlspecialchars($brandColor) ?>; }
.trend-bar.retained { background: <?= htmlspecialchars($brandColor) ?>88; }

.trend-bar-label {
    margin-top: var(--space-xs);
    font-size: var(--text-sm);
    font-weight: var(--weight-semibold);
    color: var(--color-text-primary);
}

.trend-bar-total {
    font-size: var(--text-xs);
    color: var(--color-text-secondary);
}

/* Flow Diagram */
.flow-section {
    display: grid;
    grid-template-columns: 1fr auto 1fr;
    gap: var(--space-lg);
    align-items: start;
}

.flow-box {
    background: var(--color-bg-card);
    border: 1px solid var(--color-border);
    border-radius: var(--radius-md);
    padding: var(--space-lg);
}

.flow-box h3 {
    font-size: var(--text-md);
    color: var(--color-text-primary);
    margin: 0 0 var(--space-md);
    display: flex;
    align-items: center;
    gap: var(--space-sm);
}

.flow-box h3 i { color: <?= htmlspecialchars($brandColor) ?>; }

.flow-center {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: var(--space-xl);
}

.flow-center .brand-circle {
    width: 120px;
    height: 120px;
    border-radius: 50%;
    background: <?= htmlspecialchars($brandColor) ?>;
    color: white;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    font-weight: var(--weight-bold);
}

.flow-center .brand-circle .count {
    font-size: var(--text-2xl);
}

.flow-center .brand-circle .label {
    font-size: var(--text-xs);
    opacity: 0.9;
}

.flow-item {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: var(--space-sm);
    background: var(--color-bg-surface);
    border-radius: var(--radius-sm);
    margin-bottom: var(--space-xs);
}

.flow-item .name {
    font-weight: var(--weight-medium);
}

.flow-item .count {
    background: <?= htmlspecialchars($brandColor) ?>22;
    color: <?= htmlspecialchars($brandColor) ?>;
    padding: 2px 10px;
    border-radius: var(--radius-full);
    font-weight: var(--weight-semibold);
    font-size: var(--text-sm);
}

.flow-stat {
    text-align: center;
    padding: var(--space-md);
    background: var(--color-bg-surface);
    border-radius: var(--radius-sm);
    margin-bottom: var(--space-sm);
}

.flow-stat .value {
    font-size: var(--text-xl);
    font-weight: var(--weight-bold);
    color: <?= htmlspecialchars($brandColor) ?>;
}

.flow-stat .label {
    font-size: var(--text-xs);
    color: var(--color-text-secondary);
}

/* Retention Trend Line */
.retention-trend {
    background: var(--color-bg-card);
    border: 1px solid var(--color-border);
    border-radius: var(--radius-md);
    padding: var(--space-lg);
}

.retention-line {
    display: flex;
    align-items: flex-end;
    height: 120px;
    gap: var(--space-md);
    padding: var(--space-md) 0;
}

.retention-point {
    flex: 1;
    display: flex;
    flex-direction: column;
    align-items: center;
}

.retention-dot {
    width: 12px;
    height: 12px;
    border-radius: 50%;
    background: <?= htmlspecialchars($brandColor) ?>;
    margin-bottom: var(--space-xs);
}

.retention-value {
    font-size: var(--text-sm);
    font-weight: var(--weight-bold);
    color: var(--color-text-primary);
}

.retention-year {
    font-size: var(--text-xs);
    color: var(--color-text-muted);
}

/* Print styles */
@media print {
    .filter-bar, .analytics-nav-grid, .btn-admin { display: none !important; }
    .report-header { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
    .trend-bar, .flow-center .brand-circle { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
}

@media (max-width: 899px) {
    .flow-section {
        grid-template-columns: 1fr;
    }
    .flow-center {
        order: -1;
    }
}
</style>

<!-- Filter Bar -->
<div class="filter-bar" style="display: flex; gap: var(--space-lg); margin-bottom: var(--space-xl); padding: var(--space-md); background: var(--color-bg-card); border: 1px solid var(--color-border); border-radius: var(--radius-md);">
    <form method="get" style="display: flex; gap: var(--space-lg); align-items: flex-end; flex-wrap: wrap;">
        <div style="display: flex; flex-direction: column; gap: var(--space-xs);">
            <label style="font-size: var(--text-sm); color: var(--color-text-secondary);">Varumärke</label>
            <select name="brand" class="form-select" onchange="this.form.submit()">
                <option value="">Alla varumärken</option>
                <?php foreach ($allBrands as $brand): ?>
                    <option value="<?= $brand['id'] ?>" <?= $selectedBrand == $brand['id'] ? 'selected' : '' ?>>
                        <?= htmlspecialchars($brand['name']) ?>
                    </option>
                <?php endforeach; ?>
            </select>
        </div>
        <div style="display: flex; flex-direction: column; gap: var(--space-xs);">
            <label style="font-size: var(--text-sm); color: var(--color-text-secondary);">År</label>
            <select name="year" class="form-select" onchange="this.form.submit()">
                <?php for ($y = $currentYear; $y >= $currentYear - 10; $y--): ?>
                    <option value="<?= $y ?>" <?= $selectedYear == $y ? 'selected' : '' ?>><?= $y ?></option>
                <?php endfor; ?>
            </select>
        </div>
        <div style="display: flex; flex-direction: column; gap: var(--space-xs);">
            <label style="font-size: var(--text-sm); color: var(--color-text-secondary);">Trendperiod</label>
            <select name="years" class="form-select" onchange="this.form.submit()">
                <option value="3" <?= $numYears == 3 ? 'selected' : '' ?>>3 år</option>
                <option value="5" <?= $numYears == 5 ? 'selected' : '' ?>>5 år</option>
                <option value="10" <?= $numYears == 10 ? 'selected' : '' ?>>10 år</option>
            </select>
        </div>
        <button type="button" class="btn-admin btn-admin-secondary" onclick="window.print()">
            <i data-lucide="printer"></i> Skriv ut
        </button>
    </form>
</div>

<!-- Report Header -->
<div class="report-header">
    <h1><?= htmlspecialchars($brandName) ?></h1>
    <div class="subtitle">Brand Health Report <?= $selectedYear ?> | Trendanalys <?= $numYears ?> år</div>
</div>

<?php if (isset($error)): ?>
<div class="alert alert-warning">
    <i data-lucide="alert-triangle"></i>
    <?= htmlspecialchars($error) ?>
</div>
<?php else: ?>

<!-- Summary Cards -->
<div class="summary-grid">
    <div class="summary-card">
        <div class="value"><?= number_format($reportData['current_kpis']['total_riders'] ?? 0) ?></div>
        <div class="label">Aktiva deltagare <?= $selectedYear ?></div>
        <?php if ($totalGrowth != 0): ?>
            <div class="change <?= $totalGrowth >= 0 ? 'positive' : 'negative' ?>">
                <?= $totalGrowth >= 0 ? '+' : '' ?><?= $totalGrowth ?>% sedan <?= $selectedYear - $numYears + 1 ?>
            </div>
        <?php endif; ?>
    </div>

    <div class="summary-card">
        <div class="value"><?= number_format($reportData['current_kpis']['new_riders'] ?? 0) ?></div>
        <div class="label">Nya deltagare <?= $selectedYear ?></div>
    </div>

    <div class="summary-card">
        <div class="value"><?= number_format($reportData['current_kpis']['retention_rate'] ?? 0, 1) ?>%</div>
        <div class="label">Retention <?= $selectedYear ?></div>
        <div class="change <?= ($reportData['current_kpis']['retention_rate'] ?? 0) >= $avgRetention ? 'positive' : 'negative' ?>">
            Snitt: <?= $avgRetention ?>%
        </div>
    </div>

    <div class="summary-card">
        <div class="value"><?= number_format($reportData['current_kpis']['cross_participation_rate'] ?? 0, 1) ?>%</div>
        <div class="label">Cross-participation</div>
    </div>
</div>

<!-- Trend Chart -->
<div class="report-section">
    <h2><i data-lucide="trending-up"></i> Deltagarutveckling <?= $selectedYear - $numYears + 1 ?>-<?= $selectedYear ?></h2>
    <div class="trend-chart">
        <div class="trend-bars">
            <?php
            $maxTotal = max(array_column($reportData['trends'], 'total_riders')) ?: 1;
            foreach ($reportData['trends'] as $t):
                $newHeight = ($t['new_riders'] / $maxTotal) * 140;
                $retainedHeight = ($t['retained_riders'] / $maxTotal) * 140;
            ?>
            <div class="trend-bar-group">
                <div class="trend-bar-stack">
                    <?php if ($t['new_riders'] > 0): ?>
                    <div class="trend-bar new" style="height: <?= $newHeight ?>px;" title="Nya: <?= $t['new_riders'] ?>">
                        <?= $t['new_riders'] > 20 ? $t['new_riders'] : '' ?>
                    </div>
                    <?php endif; ?>
                    <?php if ($t['retained_riders'] > 0): ?>
                    <div class="trend-bar retained" style="height: <?= $retainedHeight ?>px;" title="Återkommande: <?= $t['retained_riders'] ?>">
                        <?= $t['retained_riders'] > 20 ? $t['retained_riders'] : '' ?>
                    </div>
                    <?php endif; ?>
                </div>
                <div class="trend-bar-label"><?= $t['year'] ?></div>
                <div class="trend-bar-total"><?= number_format($t['total_riders']) ?></div>
            </div>
            <?php endforeach; ?>
        </div>
        <div style="display: flex; justify-content: center; gap: var(--space-lg); margin-top: var(--space-md); font-size: var(--text-sm);">
            <span><span style="display: inline-block; width: 12px; height: 12px; background: <?= $brandColor ?>; border-radius: 2px; margin-right: 4px;"></span> Nya</span>
            <span><span style="display: inline-block; width: 12px; height: 12px; background: <?= $brandColor ?>88; border-radius: 2px; margin-right: 4px;"></span> Återkommande</span>
        </div>
    </div>
</div>

<!-- Retention Trend -->
<div class="report-section">
    <h2><i data-lucide="refresh-cw"></i> Retention över tid</h2>
    <div class="retention-trend">
        <div class="retention-line">
            <?php foreach ($reportData['trends'] as $t):
                $dotBottom = max(0, min(100, ($t['retention_rate'] / 100) * 100));
            ?>
            <div class="retention-point">
                <div style="height: <?= 100 - $dotBottom ?>px;"></div>
                <div class="retention-dot"></div>
                <div class="retention-value"><?= number_format($t['retention_rate'], 0) ?>%</div>
                <div class="retention-year"><?= $t['year'] ?></div>
            </div>
            <?php endforeach; ?>
        </div>
    </div>
</div>

<?php if ($selectedBrand && ($reportData['feeder_breakdown'] || $reportData['exit_analysis'])): ?>
<!-- Flow Diagram -->
<div class="report-section">
    <h2><i data-lucide="git-branch"></i> Deltagarflöde <?= $selectedYear ?></h2>
    <div class="flow-section">
        <!-- Inflow (Feeder) -->
        <div class="flow-box">
            <h3><i data-lucide="log-in"></i> Varifrån kommer nya?</h3>
            <?php if ($reportData['feeder_breakdown']): ?>
                <div class="flow-stat">
                    <div class="value"><?= number_format($reportData['feeder_breakdown']['true_rookies'] ?? 0) ?></div>
                    <div class="label">True rookies (helt nya)</div>
                </div>
                <div class="flow-stat">
                    <div class="value"><?= number_format($reportData['feeder_breakdown']['crossover'] ?? 0) ?></div>
                    <div class="label">Crossover (från andra serier)</div>
                </div>
                <?php if (!empty($reportData['feeder_breakdown']['feeder_series'])): ?>
                    <h4 style="font-size: var(--text-sm); margin: var(--space-md) 0 var(--space-sm); color: var(--color-text-secondary);">Kom från:</h4>
                    <?php foreach (array_slice($reportData['feeder_breakdown']['feeder_series'], 0, 5) as $feeder): ?>
                    <div class="flow-item">
                        <span class="name"><?= htmlspecialchars($feeder['brand_name']) ?></span>
                        <span class="count"><?= $feeder['rider_count'] ?></span>
                    </div>
                    <?php endforeach; ?>
                <?php endif; ?>
            <?php else: ?>
                <p style="color: var(--color-text-muted);">Ingen data tillgänglig</p>
            <?php endif; ?>
        </div>

        <!-- Center (Brand) -->
        <div class="flow-center">
            <div class="brand-circle">
                <span class="count"><?= number_format($reportData['current_kpis']['total_riders'] ?? 0) ?></span>
                <span class="label">aktiva</span>
            </div>
            <div style="margin-top: var(--space-md); text-align: center;">
                <strong><?= htmlspecialchars($brandName) ?></strong><br>
                <span style="font-size: var(--text-sm); color: var(--color-text-secondary);"><?= $selectedYear ?></span>
            </div>
        </div>

        <!-- Outflow (Exit) -->
        <div class="flow-box">
            <h3><i data-lucide="log-out"></i> Vart går de som slutar?</h3>
            <?php if ($reportData['exit_analysis']): ?>
                <div class="flow-stat">
                    <div class="value"><?= number_format($reportData['exit_analysis']['quit_completely'] ?? 0) ?></div>
                    <div class="label">Slutade helt</div>
                </div>
                <div class="flow-stat">
                    <div class="value"><?= number_format($reportData['exit_analysis']['continued_elsewhere'] ?? 0) ?></div>
                    <div class="label">Bytte till annan serie</div>
                </div>
                <?php if (!empty($reportData['exit_analysis']['destination_series'])): ?>
                    <h4 style="font-size: var(--text-sm); margin: var(--space-md) 0 var(--space-sm); color: var(--color-text-secondary);">Gick till:</h4>
                    <?php foreach (array_slice($reportData['exit_analysis']['destination_series'], 0, 5) as $dest): ?>
                    <div class="flow-item">
                        <span class="name"><?= htmlspecialchars($dest['brand_name']) ?></span>
                        <span class="count"><?= $dest['rider_count'] ?></span>
                    </div>
                    <?php endforeach; ?>
                <?php endif; ?>
            <?php else: ?>
                <p style="color: var(--color-text-muted);">Ingen data tillgänglig</p>
            <?php endif; ?>
        </div>
    </div>
</div>
<?php endif; ?>

<!-- Demographics -->
<div class="report-section">
    <h2><i data-lucide="users"></i> Demografi <?= $selectedYear ?></h2>
    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: var(--space-lg);">
        <!-- Age Distribution -->
        <div class="flow-box">
            <h3><i data-lucide="calendar"></i> Åldersfördelning</h3>
            <?php
            $totalAge = array_sum(array_column($reportData['age_distribution'], 'count')) ?: 1;
            foreach ($reportData['age_distribution'] as $age):
                $pct = ($age['count'] / $totalAge) * 100;
            ?>
            <div style="display: flex; align-items: center; gap: var(--space-sm); margin-bottom: var(--space-xs);">
                <span style="width: 60px; font-size: var(--text-sm);"><?= $age['age_group'] ?></span>
                <div style="flex: 1; height: 20px; background: var(--color-bg-surface); border-radius: var(--radius-sm); overflow: hidden;">
                    <div style="width: <?= $pct ?>%; height: 100%; background: <?= $brandColor ?>; display: flex; align-items: center; padding-left: 8px; color: white; font-size: var(--text-xs);">
                        <?= $pct > 15 ? number_format($age['count']) : '' ?>
                    </div>
                </div>
                <span style="width: 50px; text-align: right; font-size: var(--text-sm);"><?= round($pct, 0) ?>%</span>
            </div>
            <?php endforeach; ?>
        </div>

        <!-- Gender Distribution -->
        <div class="flow-box">
            <h3><i data-lucide="pie-chart"></i> Könsfördelning</h3>
            <?php
            $gender = $reportData['gender_distribution'];
            $total = ($gender['M'] ?? 0) + ($gender['F'] ?? 0);
            $malePct = $total > 0 ? round(($gender['M'] ?? 0) / $total * 100, 1) : 0;
            $femalePct = $total > 0 ? round(($gender['F'] ?? 0) / $total * 100, 1) : 0;
            ?>
            <div style="display: flex; gap: var(--space-lg); justify-content: center; padding: var(--space-lg);">
                <div style="text-align: center;">
                    <div style="font-size: var(--text-3xl); font-weight: var(--weight-bold); color: <?= $brandColor ?>;">
                        <?= $malePct ?>%
                    </div>
                    <div style="font-size: var(--text-sm); color: var(--color-text-secondary);">Män</div>
                    <div style="font-size: var(--text-xs); color: var(--color-text-muted);"><?= number_format($gender['M'] ?? 0) ?> st</div>
                </div>
                <div style="width: 1px; background: var(--color-border);"></div>
                <div style="text-align: center;">
                    <div style="font-size: var(--text-3xl); font-weight: var(--weight-bold); color: <?= $brandColor ?>;">
                        <?= $femalePct ?>%
                    </div>
                    <div style="font-size: var(--text-sm); color: var(--color-text-secondary);">Kvinnor</div>
                    <div style="font-size: var(--text-xs); color: var(--color-text-muted);"><?= number_format($gender['F'] ?? 0) ?> st</div>
                </div>
            </div>
        </div>
    </div>
</div>

<!-- Data Table -->
<div class="report-section">
    <h2><i data-lucide="table"></i> Årlig sammanställning</h2>
    <div class="table-responsive">
        <table class="table">
            <thead>
                <tr>
                    <th>År</th>
                    <th class="text-right">Totalt</th>
                    <th class="text-right">Nya</th>
                    <th class="text-right">Återkom</th>
                    <th class="text-right">Retention</th>
                    <th class="text-right">Churn</th>
                    <th class="text-right">Tillväxt</th>
                    <th class="text-right">Cross-part.</th>
                </tr>
            </thead>
            <tbody>
                <?php foreach ($reportData['trends'] as $t): ?>
                <tr>
                    <td><strong><?= $t['year'] ?></strong></td>
                    <td class="text-right"><?= number_format($t['total_riders']) ?></td>
                    <td class="text-right"><?= number_format($t['new_riders']) ?></td>
                    <td class="text-right"><?= number_format($t['retained_riders']) ?></td>
                    <td class="text-right"><?= number_format($t['retention_rate'], 1) ?>%</td>
                    <td class="text-right"><?= number_format($t['churn_rate'], 1) ?>%</td>
                    <td class="text-right <?= $t['growth_rate'] >= 0 ? 'text-success' : 'text-danger' ?>">
                        <?= $t['growth_rate'] >= 0 ? '+' : '' ?><?= number_format($t['growth_rate'], 1) ?>%
                    </td>
                    <td class="text-right"><?= number_format($t['cross_participation'], 1) ?>%</td>
                </tr>
                <?php endforeach; ?>
            </tbody>
        </table>
    </div>
</div>

<?php endif; ?>

<?php include __DIR__ . '/components/unified-layout-footer.php'; ?>
