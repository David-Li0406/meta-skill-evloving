<?php
/**
 * Analytics Dashboard - KPI Oversikt
 *
 * Visar nyckeltal for cykelsporten i Sverige:
 * - Retention & Growth
 * - Demographics
 * - Series Flow
 * - Club stats
 *
 * Behorighet: super_admin ELLER statistics-permission
 *
 * @package TheHUB Analytics
 * @version 1.0
 */
require_once __DIR__ . '/../config.php';
require_once __DIR__ . '/../includes/auth.php';
require_once __DIR__ . '/../analytics/includes/KPICalculator.php';

// Kraver super_admin eller statistics-behorighet
requireAnalyticsAccess();

global $pdo;

// Hamta tillgangliga ar FORST for att kunna valja ratt default
$availableYears = [];
try {
    $stmt = $pdo->query("SELECT DISTINCT season_year FROM rider_yearly_stats ORDER BY season_year DESC");
    $availableYears = $stmt->fetchAll(PDO::FETCH_COLUMN);
} catch (Exception $e) {
    $currentYear = (int)date('Y');
    $availableYears = range($currentYear, $currentYear - 5);
}

// Arval - default till senaste aret med data (inte innevarande ar som kanske saknar data)
$latestYearWithData = !empty($availableYears) ? (int)$availableYears[0] : (int)date('Y');
$selectedYear = isset($_GET['year']) ? (int)$_GET['year'] : $latestYearWithData;
$compareYear = isset($_GET['compare']) ? (int)$_GET['compare'] : null;
$selectedBrand = isset($_GET['brand']) && $_GET['brand'] !== '' ? (int)$_GET['brand'] : null;

// Initiera KPI Calculator
$kpiCalc = new KPICalculator($pdo);

// Hamta alla varumarken for dropdown
$allBrands = [];
try {
    $allBrands = $kpiCalc->getAllBrands();
} catch (Exception $e) {
    // Tabellen kanske inte finns annu
}

// Hamta alla KPIs
$kpis = [];
$comparison = null;
$trends = [];
$topClubs = [];
$ageDistribution = [];
$disciplineDistribution = [];
$entryPoints = [];
$feederMatrix = [];

// Feeder series breakdown och exit analysis (endast om varumärke är valt)
$feederBreakdown = null;
$exitAnalysis = null;

try {
    $kpis = $kpiCalc->getAllKPIs($selectedYear, $selectedBrand);

    if ($compareYear) {
        $comparison = $kpiCalc->compareYears($compareYear, $selectedYear, $selectedBrand);
    }

    // Hämta feeder-breakdown och exit-analysis om varumärke är valt
    if ($selectedBrand) {
        $feederBreakdown = $kpiCalc->getFeederSeriesBreakdown($selectedYear, $selectedBrand);
        $exitAnalysis = $kpiCalc->getExitDestinationAnalysis($selectedYear, $selectedBrand);
    }

    $trends = $kpiCalc->getGrowthTrend(5, $selectedBrand);
    $topClubs = $kpiCalc->getTopClubs($selectedYear, 10, $selectedBrand);
    $ageDistribution = $kpiCalc->getAgeDistribution($selectedYear, $selectedBrand);
    $disciplineDistribution = $kpiCalc->getDisciplineDistribution($selectedYear, $selectedBrand);
    $entryPoints = $kpiCalc->getEntryPointDistribution($selectedYear, $selectedBrand);
    $feederMatrix = $kpiCalc->calculateFeederMatrix($selectedYear, $selectedBrand);
} catch (Exception $e) {
    // Tabellerna kanske inte ar befolkade an
    $error = $e->getMessage();
}

// Page config
$page_title = 'Analytics Dashboard';
$breadcrumbs = [
    ['label' => 'Dashboard', 'url' => '/admin/dashboard.php'],
    ['label' => 'Analytics']
];

$page_actions = '';

// Include unified layout
include __DIR__ . '/components/unified-layout.php';
?>

<!-- Filter Bar -->
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
            <label class="filter-label">Jamfor med</label>
            <select name="compare" class="form-select" onchange="this.form.submit()">
                <option value="">-- Ingen jamforelse --</option>
                <?php foreach ($availableYears as $year): ?>
                    <?php if ($year != $selectedYear): ?>
                        <option value="<?= $year ?>" <?= $year == $compareYear ? 'selected' : '' ?>>
                            <?= $year ?>
                        </option>
                    <?php endif; ?>
                <?php endforeach; ?>
            </select>
        </div>
    </form>
</div>

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
        Visar data for <strong><?= htmlspecialchars($brandName) ?></strong>.
        <a href="?year=<?= $selectedYear ?><?= $compareYear ? '&compare=' . $compareYear : '' ?>">Visa alla varumarken</a>
    </div>
</div>
<?php endif; ?>

<!-- Analytics Modules Navigation -->
<div class="analytics-nav-grid">
    <a href="/admin/analytics-trends.php" class="analytics-nav-item">
        <i data-lucide="trending-up"></i>
        <span>Trender</span>
    </a>
    <a href="/admin/analytics-first-season.php" class="analytics-nav-item">
        <i data-lucide="baby"></i>
        <span>First Season</span>
    </a>
    <a href="/admin/analytics-event-participation.php" class="analytics-nav-item">
        <i data-lucide="calendar-days"></i>
        <span>Event Deltagande</span>
    </a>
    <a href="/admin/analytics-class-structure.php" class="analytics-nav-item">
        <i data-lucide="layers-3"></i>
        <span>Klassanalys</span>
    </a>
    <a href="/admin/analytics-cohorts.php" class="analytics-nav-item">
        <i data-lucide="users"></i>
        <span>Kohorter</span>
    </a>
    <a href="/admin/analytics-clubs.php" class="analytics-nav-item">
        <i data-lucide="building-2"></i>
        <span>Klubbar</span>
    </a>
    <a href="/admin/analytics-geography.php" class="analytics-nav-item">
        <i data-lucide="map"></i>
        <span>Geografi</span>
    </a>
    <a href="/admin/analytics-series-compare.php" class="analytics-nav-item">
        <i data-lucide="git-compare"></i>
        <span>Jämför Serier</span>
    </a>
    <a href="/admin/analytics-flow.php" class="analytics-nav-item">
        <i data-lucide="workflow"></i>
        <span>Flöden</span>
    </a>
    <a href="/admin/analytics-reports.php" class="analytics-nav-item">
        <i data-lucide="file-text"></i>
        <span>Rapporter</span>
    </a>
    <a href="/admin/winback-analytics.php" class="analytics-nav-item">
        <i data-lucide="user-minus"></i>
        <span>Win-Back</span>
    </a>
    <a href="/admin/analytics-export-center.php" class="analytics-nav-item">
        <i data-lucide="download"></i>
        <span>Export</span>
    </a>
    <a href="/admin/analytics-data-quality.php" class="analytics-nav-item analytics-nav-item--muted">
        <i data-lucide="check-circle"></i>
        <span>Datakvalitet</span>
    </a>
    <a href="/admin/analytics-diagnose.php" class="analytics-nav-item analytics-nav-item--muted">
        <i data-lucide="stethoscope"></i>
        <span>Diagnostik</span>
    </a>
    <a href="/admin/migrations.php" class="analytics-nav-item analytics-nav-item--muted">
        <i data-lucide="database"></i>
        <span>Migrationer</span>
    </a>
</div>

<?php if (isset($error)): ?>
<div class="alert alert-warning">
    <i data-lucide="alert-triangle"></i>
    <div>
        <strong>Ingen data tillganglig</strong><br>
        Kor <code>php analytics/populate-historical.php</code> for att generera historisk data.
        <br><small><?= htmlspecialchars($error) ?></small>
    </div>
</div>
<?php else: ?>

<!-- Key Metrics -->
<div class="dashboard-metrics">
    <div class="metric-card metric-card--primary">
        <div class="metric-icon">
            <i data-lucide="users"></i>
        </div>
        <div class="metric-content">
            <div class="metric-value"><?= number_format($kpis['total_riders'] ?? 0) ?></div>
            <div class="metric-label">Aktiva riders</div>
            <?php if ($comparison && isset($comparison['total_riders'])): ?>
                <div class="metric-trend <?= $comparison['total_riders']['trend'] ?>">
                    <i data-lucide="<?= $comparison['total_riders']['trend'] === 'up' ? 'trending-up' : ($comparison['total_riders']['trend'] === 'down' ? 'trending-down' : 'minus') ?>"></i>
                    <?= $comparison['total_riders']['difference_pct'] ?>%
                </div>
            <?php endif; ?>
        </div>
    </div>

    <div class="metric-card metric-card--success">
        <div class="metric-icon">
            <i data-lucide="user-plus"></i>
        </div>
        <div class="metric-content">
            <?php
            // Om varumärke valt: visa "nya i varumärket" från feeder breakdown
            // Annars: visa globala rookies från KPI
            if ($feederBreakdown && $feederBreakdown['total_new'] > 0):
            ?>
                <div class="metric-value"><?= number_format($feederBreakdown['total_new']) ?></div>
                <div class="metric-label">Nya i varumärket</div>
                <div class="metric-breakdown" style="margin-top: var(--space-xs); font-size: var(--text-xs); color: var(--color-text-secondary);">
                    <span title="Helt nya - aldrig tävlat innan"><?= number_format($feederBreakdown['true_rookies']) ?> rookies</span>
                    <?php if ($feederBreakdown['crossover'] > 0): ?>
                        + <span title="Kom från andra varumärken"><?= number_format($feederBreakdown['crossover']) ?> crossover</span>
                    <?php endif; ?>
                </div>
            <?php else: ?>
                <div class="metric-value"><?= number_format($kpis['new_riders'] ?? 0) ?></div>
                <div class="metric-label">Nya riders (rookies)</div>
                <?php if ($comparison && isset($comparison['new_riders'])): ?>
                    <div class="metric-trend <?= $comparison['new_riders']['trend'] ?>">
                        <i data-lucide="<?= $comparison['new_riders']['trend'] === 'up' ? 'trending-up' : 'trending-down' ?>"></i>
                        <?= $comparison['new_riders']['difference_pct'] ?>%
                    </div>
                <?php endif; ?>
            <?php endif; ?>
        </div>
    </div>

    <div class="metric-card">
        <div class="metric-icon">
            <i data-lucide="refresh-cw"></i>
        </div>
        <div class="metric-content">
            <div class="metric-value"><?= number_format($kpis['retention_rate'] ?? 0, 1) ?>%</div>
            <div class="metric-label">Retention rate</div>
            <?php if ($comparison && isset($comparison['retention_rate'])): ?>
                <div class="metric-trend <?= $comparison['retention_rate']['trend'] ?>">
                    <i data-lucide="<?= $comparison['retention_rate']['trend'] === 'up' ? 'trending-up' : 'trending-down' ?>"></i>
                    <?= abs($comparison['retention_rate']['difference']) ?>pp
                </div>
            <?php endif; ?>
        </div>
    </div>

    <div class="metric-card <?= ($kpis['growth_rate'] ?? 0) >= 0 ? 'metric-card--success' : 'metric-card--warning' ?>">
        <div class="metric-icon">
            <i data-lucide="<?= ($kpis['growth_rate'] ?? 0) >= 0 ? 'trending-up' : 'trending-down' ?>"></i>
        </div>
        <div class="metric-content">
            <div class="metric-value"><?= ($kpis['growth_rate'] ?? 0) >= 0 ? '+' : '' ?><?= number_format($kpis['growth_rate'] ?? 0, 1) ?>%</div>
            <div class="metric-label">Tillvaxt</div>
        </div>
    </div>
</div>

<!-- Secondary Metrics -->
<div class="dashboard-metrics" style="margin-bottom: var(--space-xl);">
    <div class="metric-card metric-card--small">
        <div class="metric-content">
            <div class="metric-value"><?= number_format($kpis['cross_participation_rate'] ?? 0, 1) ?>%</div>
            <div class="metric-label">Cross-participation</div>
        </div>
    </div>

    <div class="metric-card metric-card--small">
        <div class="metric-content">
            <div class="metric-value"><?= number_format($kpis['average_age'] ?? 0, 0) ?> ar</div>
            <div class="metric-label">Snittålder</div>
        </div>
    </div>

    <div class="metric-card metric-card--small">
        <div class="metric-content">
            <?php
            $genderDist = $kpis['gender_distribution'] ?? ['M' => 0, 'F' => 0];
            $total = ($genderDist['M'] + $genderDist['F']) ?: 1;
            $femalePct = round($genderDist['F'] / $total * 100, 1);
            ?>
            <div class="metric-value"><?= $femalePct ?>%</div>
            <div class="metric-label">Kvinnor</div>
        </div>
    </div>

    <div class="metric-card metric-card--small">
        <div class="metric-content">
            <div class="metric-value"><?= number_format($kpis['retained_riders'] ?? 0) ?></div>
            <div class="metric-label">Atervandare</div>
        </div>
    </div>
</div>

<!-- Feeder Series Breakdown (visas endast när varumärke är valt) -->
<?php if ($feederBreakdown && $feederBreakdown['crossover'] > 0): ?>
<div class="admin-card" style="margin-bottom: var(--space-xl);">
    <div class="admin-card-header">
        <h2><i data-lucide="git-merge" style="width:20px;height:20px;margin-right:var(--space-sm);"></i> Feeder-serier - Varifrån kom de nya?</h2>
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
                    <div style="font-size: var(--text-2xl); font-weight: var(--weight-bold); color: var(--color-text-primary);"><?= number_format($feederBreakdown['total_new']) ?></div>
                    <div style="font-size: var(--text-sm); color: var(--color-text-secondary);">Totalt nya</div>
                    <div style="font-size: var(--text-xs); color: var(--color-text-muted);">I detta varumärke</div>
                </div>
            </div>

            <?php if (!empty($feederBreakdown['feeder_series'])): ?>
            <h4 style="margin-bottom: var(--space-md);">Crossover kom från:</h4>
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

<!-- Exit Destination Analysis (visas endast när varumärke är valt) -->
<?php if ($exitAnalysis && $exitAnalysis['total_churned'] > 0): ?>
<div class="admin-card" style="margin-bottom: var(--space-xl);">
    <div class="admin-card-header">
        <h2><i data-lucide="log-out" style="width:20px;height:20px;margin-right:var(--space-sm);"></i> Exit-analys - Vart går de som slutar?</h2>
    </div>
    <div class="admin-card-body">
        <div class="exit-breakdown">
            <div class="exit-summary" style="display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: var(--space-lg); margin-bottom: var(--space-lg);">
                <div class="exit-stat" style="text-align: center; padding: var(--space-md); background: var(--color-bg-sunken); border-radius: var(--radius-md);">
                    <div style="font-size: var(--text-2xl); font-weight: var(--weight-bold); color: var(--color-error);"><?= number_format($exitAnalysis['quit_completely']) ?></div>
                    <div style="font-size: var(--text-sm); color: var(--color-text-secondary);">Slutade helt</div>
                    <div style="font-size: var(--text-xs); color: var(--color-text-muted);">Ingen serie <?= $selectedYear ?></div>
                </div>
                <div class="exit-stat" style="text-align: center; padding: var(--space-md); background: var(--color-bg-sunken); border-radius: var(--radius-md);">
                    <div style="font-size: var(--text-2xl); font-weight: var(--weight-bold); color: var(--color-warning);"><?= number_format($exitAnalysis['continued_elsewhere']) ?></div>
                    <div style="font-size: var(--text-sm); color: var(--color-text-secondary);">Bytte serie</div>
                    <div style="font-size: var(--text-xs); color: var(--color-text-muted);">Fortsatte i annan</div>
                </div>
                <div class="exit-stat" style="text-align: center; padding: var(--space-md); background: var(--color-bg-sunken); border-radius: var(--radius-md);">
                    <div style="font-size: var(--text-2xl); font-weight: var(--weight-bold); color: var(--color-text-primary);"><?= number_format($exitAnalysis['total_churned']) ?></div>
                    <div style="font-size: var(--text-sm); color: var(--color-text-secondary);">Lämnade serien</div>
                    <div style="font-size: var(--text-xs); color: var(--color-text-muted);">Från <?= $selectedYear - 1 ?></div>
                </div>
            </div>

            <?php if (!empty($exitAnalysis['destination_series'])): ?>
            <h4 style="margin-bottom: var(--space-md);">De som bytte serie gick till:</h4>
            <div class="exit-destinations" style="display: flex; flex-wrap: wrap; gap: var(--space-sm);">
                <?php foreach ($exitAnalysis['destination_series'] as $dest): ?>
                <div class="exit-badge" style="display: inline-flex; align-items: center; gap: var(--space-xs); padding: var(--space-xs) var(--space-sm); background: rgba(var(--color-warning-rgb, 217, 119, 6), 0.1); border-radius: var(--radius-sm); font-size: var(--text-sm);">
                    <span style="font-weight: var(--weight-semibold);"><?= htmlspecialchars($dest['brand_name']) ?></span>
                    <span style="background: var(--color-warning); color: white; padding: 2px 6px; border-radius: var(--radius-full); font-size: var(--text-xs);"><?= number_format($dest['rider_count']) ?></span>
                </div>
                <?php endforeach; ?>
            </div>
            <?php endif; ?>
        </div>
    </div>
</div>
<?php endif; ?>

<!-- Growth Trend Chart -->
<?php if (!empty($trends)): ?>
<div class="admin-card">
    <div class="admin-card-header">
        <h2>Tillvaxttrender</h2>
    </div>
    <div class="admin-card-body">
        <div class="trend-chart">
            <div class="trend-bars">
                <?php
                $maxRiders = max(array_column($trends, 'total_riders')) ?: 1;
                foreach ($trends as $t):
                    $height = ($t['total_riders'] / $maxRiders) * 100;
                ?>
                <div class="trend-bar-group">
                    <div class="trend-bar-container">
                        <div class="trend-bar" style="height: <?= $height ?>%;">
                            <span class="trend-bar-value"><?= number_format($t['total_riders']) ?></span>
                        </div>
                    </div>
                    <div class="trend-bar-label"><?= $t['season_year'] ?></div>
                    <div class="trend-bar-sub">
                        <span class="badge badge-success"><?= $t['new_riders'] ?> nya</span>
                    </div>
                </div>
                <?php endforeach; ?>
            </div>
        </div>
    </div>
</div>
<?php endif; ?>

<!-- Two Column Layout -->
<div class="grid grid-2 grid-gap-lg">
    <!-- Age Distribution -->
    <?php if (!empty($ageDistribution)): ?>
    <div class="admin-card">
        <div class="admin-card-header">
            <h2>Aldersfordelning</h2>
        </div>
        <div class="admin-card-body">
            <?php
            $totalAge = array_sum(array_column($ageDistribution, 'count')) ?: 1;
            foreach ($ageDistribution as $age):
                $pct = ($age['count'] / $totalAge) * 100;
            ?>
            <div class="distribution-row">
                <span class="distribution-label"><?= htmlspecialchars($age['age_group']) ?></span>
                <div class="distribution-bar-container">
                    <div class="distribution-bar" style="width: <?= $pct ?>%;"></div>
                </div>
                <span class="distribution-value"><?= number_format($age['count']) ?> (<?= round($pct, 1) ?>%)</span>
            </div>
            <?php endforeach; ?>
        </div>
    </div>
    <?php endif; ?>

    <!-- Discipline Distribution -->
    <?php if (!empty($disciplineDistribution)): ?>
    <div class="admin-card">
        <div class="admin-card-header">
            <h2>Disciplinfordelning</h2>
        </div>
        <div class="admin-card-body">
            <?php
            $totalDisc = array_sum(array_column($disciplineDistribution, 'count')) ?: 1;
            foreach (array_slice($disciplineDistribution, 0, 6) as $disc):
                $pct = ($disc['count'] / $totalDisc) * 100;
            ?>
            <div class="distribution-row">
                <span class="distribution-label"><?= htmlspecialchars($disc['discipline']) ?></span>
                <div class="distribution-bar-container">
                    <div class="distribution-bar distribution-bar--accent" style="width: <?= $pct ?>%;"></div>
                </div>
                <span class="distribution-value"><?= number_format($disc['count']) ?> (<?= round($pct, 1) ?>%)</span>
            </div>
            <?php endforeach; ?>
        </div>
    </div>
    <?php endif; ?>
</div>

<!-- Entry Points -->
<?php if (!empty($entryPoints)): ?>
<div class="admin-card">
    <div class="admin-card-header">
        <h2>Entry Points - Var borjar nya riders?</h2>
        <span class="badge"><?= $selectedYear ?></span>
    </div>
    <div class="admin-card-body" style="padding: 0;">
        <div class="admin-table-container">
            <table class="admin-table">
                <thead>
                    <tr>
                        <th>Serie</th>
                        <th>Niva</th>
                        <th>Nya riders</th>
                        <th>Andel</th>
                    </tr>
                </thead>
                <tbody>
                    <?php
                    $totalEntry = array_sum(array_column($entryPoints, 'rider_count')) ?: 1;
                    foreach (array_slice($entryPoints, 0, 10) as $ep):
                        $pct = ($ep['rider_count'] / $totalEntry) * 100;
                    ?>
                    <tr>
                        <td>
                            <a href="/series/<?= $ep['series_id'] ?>" class="text-link">
                                <?= htmlspecialchars($ep['series_name']) ?>
                            </a>
                        </td>
                        <td>
                            <span class="badge badge-<?= $ep['series_level'] === 'national' ? 'primary' : 'secondary' ?>">
                                <?= ucfirst($ep['series_level']) ?>
                            </span>
                        </td>
                        <td><?= number_format($ep['rider_count']) ?></td>
                        <td>
                            <div class="inline-bar">
                                <div class="inline-bar-fill" style="width: <?= min($pct * 2, 100) ?>%;"></div>
                            </div>
                            <?= round($pct, 1) ?>%
                        </td>
                    </tr>
                    <?php endforeach; ?>
                </tbody>
            </table>
        </div>
    </div>
</div>
<?php endif; ?>

<!-- Top Clubs -->
<?php if (!empty($topClubs)): ?>
<div class="admin-card">
    <div class="admin-card-header">
        <h2>Top Klubbar</h2>
        <a href="/admin/analytics-clubs.php" class="btn-admin btn-admin-sm btn-admin-secondary">
            Visa alla
        </a>
    </div>
    <div class="admin-card-body" style="padding: 0;">
        <div class="admin-table-container">
            <table class="admin-table">
                <thead>
                    <tr>
                        <th>#</th>
                        <th>Klubb</th>
                        <th>Stad</th>
                        <th>Aktiva</th>
                        <th>Poang</th>
                        <th>Vinster</th>
                        <th>Pallplatser</th>
                    </tr>
                </thead>
                <tbody>
                    <?php foreach ($topClubs as $i => $club): ?>
                    <tr>
                        <td><?= $i + 1 ?></td>
                        <td>
                            <a href="/club/<?= $club['club_id'] ?>" class="text-link">
                                <?= htmlspecialchars($club['club_name']) ?>
                            </a>
                        </td>
                        <td><?= htmlspecialchars($club['city'] ?? '-') ?></td>
                        <td><strong><?= number_format($club['active_riders']) ?></strong></td>
                        <td><?= number_format($club['total_points']) ?></td>
                        <td><?= number_format($club['wins']) ?></td>
                        <td><?= number_format($club['podiums']) ?></td>
                    </tr>
                    <?php endforeach; ?>
                </tbody>
            </table>
        </div>
    </div>
</div>
<?php endif; ?>

<!-- Feeder Matrix Preview -->
<?php if (!empty($feederMatrix)): ?>
<div class="admin-card">
    <div class="admin-card-header">
        <h2>Series Flow (Topp 10)</h2>
        <a href="/admin/analytics-flow.php" class="btn-admin btn-admin-sm btn-admin-primary">
            <i data-lucide="git-branch"></i> Detaljerad analys
        </a>
    </div>
    <div class="admin-card-body" style="padding: 0;">
        <div class="admin-table-container">
            <table class="admin-table">
                <thead>
                    <tr>
                        <th>Fran serie</th>
                        <th></th>
                        <th>Till serie</th>
                        <th>Antal</th>
                    </tr>
                </thead>
                <tbody>
                    <?php foreach (array_slice($feederMatrix, 0, 10) as $flow): ?>
                    <tr>
                        <td>
                            <?= htmlspecialchars($flow['from_name']) ?>
                            <span class="badge badge-sm"><?= ucfirst($flow['from_level']) ?></span>
                        </td>
                        <td class="text-center">
                            <i data-lucide="arrow-right" class="icon-sm"></i>
                        </td>
                        <td>
                            <?= htmlspecialchars($flow['to_name']) ?>
                            <span class="badge badge-sm"><?= ucfirst($flow['to_level']) ?></span>
                        </td>
                        <td><strong><?= number_format($flow['flow_count']) ?></strong></td>
                    </tr>
                    <?php endforeach; ?>
                </tbody>
            </table>
        </div>
    </div>
</div>
<?php endif; ?>

<?php endif; // end if no error ?>

<style>
/* Analytics Navigation Grid */
.analytics-nav-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(110px, 1fr));
    gap: var(--space-sm);
    margin-bottom: var(--space-xl);
    padding: var(--space-md);
    background: var(--color-bg-card);
    border: 1px solid var(--color-border);
    border-radius: var(--radius-md);
}

.analytics-nav-item {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: var(--space-xs);
    padding: var(--space-sm) var(--space-xs);
    background: var(--color-bg-surface);
    border: 1px solid transparent;
    border-radius: var(--radius-sm);
    text-decoration: none;
    color: var(--color-text-primary);
    font-size: var(--text-xs);
    font-weight: var(--weight-medium);
    text-align: center;
    transition: all 0.15s ease;
}

.analytics-nav-item i {
    width: 20px;
    height: 20px;
    color: var(--color-accent);
}

.analytics-nav-item:hover {
    background: var(--color-accent-light);
    border-color: var(--color-accent);
    transform: translateY(-1px);
}

.analytics-nav-item--muted {
    opacity: 0.7;
}

.analytics-nav-item--muted i {
    color: var(--color-text-muted);
}

.analytics-nav-item--muted:hover {
    opacity: 1;
}

@media (max-width: 767px) {
    .analytics-nav-grid {
        grid-template-columns: repeat(4, 1fr);
        margin-left: calc(-1 * var(--container-padding, 16px));
        margin-right: calc(-1 * var(--container-padding, 16px));
        border-radius: 0;
        border-left: none;
        border-right: none;
    }

    .analytics-nav-item {
        padding: var(--space-xs);
        font-size: 10px;
    }

    .analytics-nav-item i {
        width: 18px;
        height: 18px;
    }
}

/* Dashboard Metrics Grid */
.dashboard-metrics {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: var(--space-md);
    margin-bottom: var(--space-lg);
}

/* Metric Card Base */
.metric-card {
    display: flex;
    align-items: flex-start;
    gap: var(--space-md);
    padding: var(--space-lg);
    background: var(--color-bg-card);
    border: 1px solid var(--color-border);
    border-radius: var(--radius-md);
    transition: all 0.15s ease;
}

.metric-card:hover {
    border-color: var(--color-accent);
    box-shadow: var(--shadow-sm);
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
    width: 48px;
    height: 48px;
    background: var(--color-accent-light);
    border-radius: var(--radius-md);
    color: var(--color-accent);
    flex-shrink: 0;
}

.metric-icon i {
    width: 24px;
    height: 24px;
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

/* Metric Cards with Trends */
.metric-card--small {
    padding: var(--space-md);
}

.metric-card--small .metric-value {
    font-size: var(--text-xl);
}

.metric-trend {
    display: inline-flex;
    align-items: center;
    gap: 4px;
    margin-top: var(--space-xs);
    padding: 2px 8px;
    border-radius: var(--radius-full);
    font-size: var(--text-xs);
    font-weight: var(--weight-semibold);
}

.metric-trend.up {
    background: rgba(34, 197, 94, 0.15);
    color: var(--color-success);
}

.metric-trend.down {
    background: rgba(239, 68, 68, 0.15);
    color: var(--color-error);
}

.metric-trend.stable {
    background: var(--color-bg-hover);
    color: var(--color-text-secondary);
}

.metric-trend i {
    width: 14px;
    height: 14px;
}

/* Trend Chart */
.trend-chart {
    padding: var(--space-md) 0;
}

.trend-bars {
    display: flex;
    justify-content: space-around;
    align-items: flex-end;
    height: 200px;
    gap: var(--space-md);
}

.trend-bar-group {
    flex: 1;
    display: flex;
    flex-direction: column;
    align-items: center;
    max-width: 100px;
}

.trend-bar-container {
    width: 100%;
    height: 150px;
    display: flex;
    align-items: flex-end;
}

.trend-bar {
    width: 100%;
    background: linear-gradient(180deg, var(--color-accent), var(--color-accent-hover));
    border-radius: var(--radius-sm) var(--radius-sm) 0 0;
    display: flex;
    justify-content: center;
    align-items: flex-start;
    padding-top: var(--space-xs);
    min-height: 20px;
    transition: height 0.3s ease;
}

.trend-bar-value {
    font-size: var(--text-xs);
    font-weight: var(--weight-bold);
    color: white;
    text-shadow: 0 1px 2px rgba(0,0,0,0.3);
}

.trend-bar-label {
    margin-top: var(--space-xs);
    font-weight: var(--weight-semibold);
    color: var(--color-text-primary);
}

.trend-bar-sub {
    margin-top: 4px;
}

/* Distribution Rows */
.distribution-row {
    display: flex;
    align-items: center;
    gap: var(--space-md);
    padding: var(--space-sm) 0;
    border-bottom: 1px solid var(--color-border);
}

.distribution-row:last-child {
    border-bottom: none;
}

.distribution-label {
    flex: 0 0 80px;
    font-size: var(--text-sm);
    color: var(--color-text-secondary);
}

.distribution-bar-container {
    flex: 1;
    height: 8px;
    background: var(--color-bg-hover);
    border-radius: var(--radius-full);
    overflow: hidden;
}

.distribution-bar {
    height: 100%;
    background: var(--color-success);
    border-radius: var(--radius-full);
    transition: width 0.3s ease;
}

.distribution-bar--accent {
    background: var(--color-accent);
}

.distribution-value {
    flex: 0 0 100px;
    text-align: right;
    font-size: var(--text-sm);
    font-weight: var(--weight-medium);
}

/* Inline Bar */
.inline-bar {
    display: inline-block;
    width: 60px;
    height: 6px;
    background: var(--color-bg-hover);
    border-radius: var(--radius-full);
    overflow: hidden;
    vertical-align: middle;
    margin-right: var(--space-xs);
}

.inline-bar-fill {
    height: 100%;
    background: var(--color-accent);
    border-radius: var(--radius-full);
}

/* Icon sizes */
.icon-sm {
    width: 16px;
    height: 16px;
    color: var(--color-text-muted);
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


/* Grid */
.grid-2 {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
}

.grid-gap-lg {
    gap: var(--space-lg);
}

/* Button group */
.btn-group {
    display: flex;
    gap: var(--space-sm);
}

/* Responsive */
@media (max-width: 899px) {
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

    .grid-2 {
        grid-template-columns: 1fr;
    }

    .trend-bars {
        height: 150px;
    }

    .trend-bar-container {
        height: 100px;
    }

    .btn-group {
        flex-direction: column;
    }
}

@media (max-width: 767px) {
    .filter-bar {
        margin-left: calc(-1 * var(--container-padding, 16px));
        margin-right: calc(-1 * var(--container-padding, 16px));
        border-radius: 0;
        border-left: none;
        border-right: none;
    }

    .distribution-label {
        flex: 0 0 60px;
        font-size: var(--text-xs);
    }

    .distribution-value {
        flex: 0 0 80px;
        font-size: var(--text-xs);
    }

    /* Mobile horizontal scroll for metrics */
    .dashboard-metrics {
        display: flex;
        overflow-x: auto;
        scroll-snap-type: x mandatory;
        -webkit-overflow-scrolling: touch;
        gap: var(--space-md);
        padding-bottom: var(--space-sm);
        margin-left: calc(-1 * var(--container-padding, 16px));
        margin-right: calc(-1 * var(--container-padding, 16px));
        padding-left: var(--space-md);
        padding-right: var(--space-md);
    }

    .metric-card {
        flex: 0 0 280px;
        scroll-snap-align: start;
    }

    .metric-card--small {
        flex: 0 0 160px;
    }

    .metric-value {
        font-size: var(--text-xl);
    }
}
</style>

<?php include __DIR__ . '/components/unified-layout-footer.php'; ?>
