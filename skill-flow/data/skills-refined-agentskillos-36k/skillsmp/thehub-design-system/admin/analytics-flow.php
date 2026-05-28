<?php
/**
 * Analytics - Series Flow Analysis
 *
 * KEY FEATURE: Visualiserar flodet av riders mellan serier.
 * - Feeder patterns (regional -> nationell)
 * - Cross-participation
 * - Serie-lojalitet
 * - Entry points
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
    $stmt = $pdo->query("SELECT DISTINCT season_year FROM series_participation ORDER BY season_year DESC");
    $availableYears = $stmt->fetchAll(PDO::FETCH_COLUMN);
} catch (Exception $e) {
    $currentYear = (int)date('Y');
    $availableYears = range($currentYear, $currentYear - 5);
}

// Arval - default till senaste aret med data
$latestYearWithData = !empty($availableYears) ? (int)$availableYears[0] : (int)date('Y');
$selectedYear = isset($_GET['year']) ? (int)$_GET['year'] : $latestYearWithData;

// Hamta serier med analytics aktiverat
$series = [];
try {
    $stmt = $pdo->query("
        SELECT id, name, series_level, region
        FROM series
        WHERE analytics_enabled = 1 OR analytics_enabled IS NULL
        ORDER BY
            CASE series_level
                WHEN 'national' THEN 1
                WHEN 'regional' THEN 2
                ELSE 3
            END,
            name
    ");
    $series = $stmt->fetchAll(PDO::FETCH_ASSOC);
} catch (Exception $e) {
    // Fallback utan kolumnen
    $stmt = $pdo->query("SELECT id, name FROM series ORDER BY name");
    $series = $stmt->fetchAll(PDO::FETCH_ASSOC);
}

// Initiera KPI Calculator
$kpiCalc = new KPICalculator($pdo);

// Hamta data
$feederMatrix = [];
$entryPoints = [];
$seriesStats = [];
$nationalSeries = [];
$regionalSeries = [];

try {
    $feederMatrix = $kpiCalc->calculateFeederMatrix($selectedYear);
    $entryPoints = $kpiCalc->getEntryPointDistribution($selectedYear);

    // Berakna stats per serie
    foreach ($series as $s) {
        $seriesStats[$s['id']] = [
            'name' => $s['name'],
            'level' => $s['series_level'] ?? 'unknown',
            'region' => $s['region'] ?? null,
            'loyalty' => $kpiCalc->getSeriesLoyaltyRate($s['id'], $selectedYear),
            'exclusivity' => $kpiCalc->getExclusivityRate($s['id'], $selectedYear)
        ];

        // Hamta deltagare
        $stmt = $pdo->prepare("SELECT COUNT(DISTINCT rider_id) FROM series_participation WHERE series_id = ? AND season_year = ?");
        $stmt->execute([$s['id'], $selectedYear]);
        $seriesStats[$s['id']]['participants'] = (int)$stmt->fetchColumn();

        // Kategorisera
        if (($s['series_level'] ?? '') === 'national') {
            $nationalSeries[] = $s['id'];
        } else {
            $regionalSeries[] = $s['id'];
        }
    }

    // Cross-participation rate
    $crossRate = $kpiCalc->getCrossParticipationRate($selectedYear);

    // === NYA KARRIARVAGS-ANALYSER ===
    // Feeder Pipeline - riders som startade regionalt och gick till nationellt
    $feederPipeline = $kpiCalc->getFeederPipeline($selectedYear);

    // National to Regional flow - riders som startade nationellt
    $nationalToRegional = $kpiCalc->getNationalToRegionalFlow($selectedYear);

    // Karriarvags-fordelning
    $careerPaths = $kpiCalc->getCareerPathsAnalysis($selectedYear);

    // Entry points for forsta-gangs-tavlande detta ar
    $entryPointsThisYear = $kpiCalc->getFirstRaceEntryPoints($selectedYear);

    // Graduation trend (senaste 5 aren)
    $graduationTrend = $kpiCalc->getGraduationTrend($selectedYear - 4, $selectedYear);

} catch (Exception $e) {
    $error = $e->getMessage();
}

// Hamta overlapp mellan utvalda serier
$selectedSeries1 = isset($_GET['series1']) ? (int)$_GET['series1'] : null;
$selectedSeries2 = isset($_GET['series2']) ? (int)$_GET['series2'] : null;
$overlap = null;

if ($selectedSeries1 && $selectedSeries2) {
    try {
        $overlap = $kpiCalc->getSeriesOverlap($selectedSeries1, $selectedSeries2, $selectedYear);
    } catch (Exception $e) {
        // Ignorera
    }
}

// Page config
$page_title = 'Series Flow Analysis';
$breadcrumbs = [
    ['label' => 'Analytics', 'url' => '/admin/analytics-dashboard.php'],
    ['label' => 'Series Flow']
];

// Include unified layout
include __DIR__ . '/components/unified-layout.php';
?>

<!-- Year Selector -->
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
    </form>
</div>

<?php if (isset($error)): ?>
<div class="alert alert-warning">
    <i data-lucide="alert-triangle"></i>
    <div>
        <strong>Ingen data tillganglig</strong><br>
        Kor <code>php analytics/populate-historical.php</code> for att generera historisk data.
    </div>
</div>
<?php else: ?>

<!-- Overview Stats -->
<div class="dashboard-metrics">
    <div class="metric-card metric-card--primary">
        <div class="metric-icon">
            <i data-lucide="git-branch"></i>
        </div>
        <div class="metric-content">
            <div class="metric-value"><?= number_format($crossRate ?? 0, 1) ?>%</div>
            <div class="metric-label">Cross-participation</div>
            <div class="metric-sub">Riders i 2+ serier</div>
        </div>
    </div>

    <div class="metric-card">
        <div class="metric-icon">
            <i data-lucide="trophy"></i>
        </div>
        <div class="metric-content">
            <div class="metric-value"><?= count($nationalSeries) ?></div>
            <div class="metric-label">Nationella serier</div>
        </div>
    </div>

    <div class="metric-card">
        <div class="metric-icon">
            <i data-lucide="map"></i>
        </div>
        <div class="metric-content">
            <div class="metric-value"><?= count($regionalSeries) ?></div>
            <div class="metric-label">Regionala serier</div>
        </div>
    </div>

    <div class="metric-card">
        <div class="metric-icon">
            <i data-lucide="arrow-right-left"></i>
        </div>
        <div class="metric-content">
            <div class="metric-value"><?= count($feederMatrix) ?></div>
            <div class="metric-label">Flodesrelationer</div>
        </div>
    </div>
</div>

<!-- Feeder Flow Matrix -->
<div class="admin-card">
    <div class="admin-card-header">
        <h2>Flodesmatris - Regional till Nationell</h2>
        <span class="badge badge-info"><?= $selectedYear ?></span>
    </div>
    <div class="admin-card-body">
        <p class="text-muted" style="margin-bottom: var(--space-md);">
            Visar hur manga riders fran regionala serier som ocksa deltar i nationella serier samma ar.
            Hog conversion rate indikerar en stark feeder-pipeline.
        </p>

        <?php if (!empty($feederMatrix)): ?>
        <div class="flow-grid">
            <?php
            // Filtrera for regional->national flows
            $nationalFlows = array_filter($feederMatrix, function($f) {
                return ($f['from_level'] === 'regional' && $f['to_level'] === 'national');
            });

            if (empty($nationalFlows)) {
                $nationalFlows = array_slice($feederMatrix, 0, 15);
            }

            foreach (array_slice($nationalFlows, 0, 15) as $flow):
            ?>
            <div class="flow-card">
                <div class="flow-from">
                    <span class="flow-series"><?= htmlspecialchars($flow['from_name']) ?></span>
                    <span class="badge badge-<?= $flow['from_level'] === 'regional' ? 'secondary' : 'primary' ?>">
                        <?= ucfirst($flow['from_level']) ?>
                    </span>
                </div>
                <div class="flow-arrow">
                    <i data-lucide="arrow-down"></i>
                    <span class="flow-count"><?= number_format($flow['flow_count']) ?> riders</span>
                </div>
                <div class="flow-to">
                    <span class="flow-series"><?= htmlspecialchars($flow['to_name']) ?></span>
                    <span class="badge badge-<?= $flow['to_level'] === 'national' ? 'primary' : 'secondary' ?>">
                        <?= ucfirst($flow['to_level']) ?>
                    </span>
                </div>
            </div>
            <?php endforeach; ?>
        </div>
        <?php else: ?>
        <div class="empty-state">
            <i data-lucide="git-branch"></i>
            <p>Ingen flodesdata tillganglig for <?= $selectedYear ?></p>
        </div>
        <?php endif; ?>
    </div>
</div>

<!-- Series Comparison Tool -->
<div class="admin-card">
    <div class="admin-card-header">
        <h2>Jamfor Serier - Overlapp</h2>
    </div>
    <div class="admin-card-body">
        <form method="get" class="comparison-form">
            <input type="hidden" name="year" value="<?= $selectedYear ?>">

            <div class="comparison-selects">
                <div class="filter-group">
                    <label class="filter-label">Serie 1</label>
                    <select name="series1" class="form-select">
                        <option value="">Valj serie...</option>
                        <?php foreach ($series as $s): ?>
                            <option value="<?= $s['id'] ?>" <?= $s['id'] == $selectedSeries1 ? 'selected' : '' ?>>
                                <?= htmlspecialchars($s['name']) ?>
                                <?php if (!empty($s['series_level'])): ?>
                                    (<?= ucfirst($s['series_level']) ?>)
                                <?php endif; ?>
                            </option>
                        <?php endforeach; ?>
                    </select>
                </div>

                <div class="comparison-vs">
                    <i data-lucide="git-compare"></i>
                </div>

                <div class="filter-group">
                    <label class="filter-label">Serie 2</label>
                    <select name="series2" class="form-select">
                        <option value="">Valj serie...</option>
                        <?php foreach ($series as $s): ?>
                            <option value="<?= $s['id'] ?>" <?= $s['id'] == $selectedSeries2 ? 'selected' : '' ?>>
                                <?= htmlspecialchars($s['name']) ?>
                                <?php if (!empty($s['series_level'])): ?>
                                    (<?= ucfirst($s['series_level']) ?>)
                                <?php endif; ?>
                            </option>
                        <?php endforeach; ?>
                    </select>
                </div>

                <button type="submit" class="btn-admin btn-admin-primary">
                    <i data-lucide="search"></i> Jamfor
                </button>
            </div>
        </form>

        <?php if ($overlap): ?>
        <div class="overlap-result">
            <h3>Resultat</h3>

            <div class="overlap-visual">
                <div class="overlap-circle overlap-left" style="--size: <?= min(100, $overlap['only_series_1'] / 5) ?>%;">
                    <span class="overlap-value"><?= $overlap['only_series_1'] ?></span>
                    <span class="overlap-label">Endast Serie 1</span>
                </div>
                <div class="overlap-intersection">
                    <span class="overlap-value overlap-value--large"><?= $overlap['both'] ?></span>
                    <span class="overlap-label">Bada</span>
                </div>
                <div class="overlap-circle overlap-right" style="--size: <?= min(100, $overlap['only_series_2'] / 5) ?>%;">
                    <span class="overlap-value"><?= $overlap['only_series_2'] ?></span>
                    <span class="overlap-label">Endast Serie 2</span>
                </div>
            </div>

            <div class="overlap-stats">
                <div class="stat-item">
                    <span class="stat-label">Overlapp</span>
                    <span class="stat-value"><?= $overlap['overlap_percentage'] ?>%</span>
                </div>
                <div class="stat-item">
                    <span class="stat-label">Unika riders</span>
                    <span class="stat-value"><?= $overlap['only_series_1'] + $overlap['only_series_2'] + $overlap['both'] ?></span>
                </div>
            </div>
        </div>
        <?php endif; ?>
    </div>
</div>

<!-- Series Stats Table -->
<div class="admin-card">
    <div class="admin-card-header">
        <h2>Serie-statistik</h2>
        <span class="badge"><?= $selectedYear ?></span>
    </div>
    <div class="admin-card-body" style="padding: var(--space-md); padding-bottom: 0;">
        <p class="text-muted" style="font-size: var(--text-sm); margin: 0;">
            <strong>Lojalitet</strong> = Andel av <?= $selectedYear - 1 ?>-deltagare som aterkom <?= $selectedYear ?>.
            Visar 0% om data fran <?= $selectedYear - 1 ?> saknas.
            <strong>Exklusivitet</strong> = Andel som endast deltar i denna serie.
        </p>
    </div>
    <div class="admin-card-body" style="padding: 0;">
        <div class="admin-table-container">
            <table class="admin-table">
                <thead>
                    <tr>
                        <th>Serie</th>
                        <th>Niva</th>
                        <th>Deltagare</th>
                        <th title="Andel av forra arets deltagare som aterkom detta ar. Kraver data fran foregaende ar.">Lojalitet <i data-lucide="info" style="width: 12px; height: 12px; opacity: 0.5;"></i></th>
                        <th title="Andel deltagare som ENDAST deltar i denna serie (inte andra serier).">Exklusivitet <i data-lucide="info" style="width: 12px; height: 12px; opacity: 0.5;"></i></th>
                    </tr>
                </thead>
                <tbody>
                    <?php
                    // Sortera efter deltagare
                    uasort($seriesStats, fn($a, $b) => $b['participants'] - $a['participants']);

                    foreach (array_slice($seriesStats, 0, 20, true) as $sId => $stats):
                        if ($stats['participants'] == 0) continue;
                    ?>
                    <tr>
                        <td>
                            <a href="/series/<?= $sId ?>" class="text-link">
                                <?= htmlspecialchars($stats['name']) ?>
                            </a>
                        </td>
                        <td>
                            <span class="badge badge-<?= $stats['level'] === 'national' ? 'primary' : 'secondary' ?>">
                                <?= ucfirst($stats['level']) ?>
                            </span>
                        </td>
                        <td><strong><?= number_format($stats['participants']) ?></strong></td>
                        <td>
                            <div class="progress-cell">
                                <div class="progress-bar-mini">
                                    <div class="progress-fill" style="width: <?= $stats['loyalty'] ?>%;"></div>
                                </div>
                                <span><?= number_format($stats['loyalty'], 1) ?>%</span>
                            </div>
                        </td>
                        <td>
                            <div class="progress-cell">
                                <div class="progress-bar-mini">
                                    <div class="progress-fill progress-fill--alt" style="width: <?= $stats['exclusivity'] ?>%;"></div>
                                </div>
                                <span><?= number_format($stats['exclusivity'], 1) ?>%</span>
                            </div>
                        </td>
                    </tr>
                    <?php endforeach; ?>
                </tbody>
            </table>
        </div>
    </div>
</div>

<!-- Entry Points -->
<?php if (!empty($entryPoints)): ?>
<div class="admin-card">
    <div class="admin-card-header">
        <h2>Entry Points - Var borjar nya riders?</h2>
    </div>
    <div class="admin-card-body">
        <div class="entry-points-grid">
            <?php
            $totalEntries = array_sum(array_column($entryPoints, 'rider_count')) ?: 1;
            foreach (array_slice($entryPoints, 0, 8) as $ep):
                $pct = ($ep['rider_count'] / $totalEntries) * 100;
            ?>
            <div class="entry-point-card">
                <div class="entry-point-icon">
                    <i data-lucide="<?= $ep['series_level'] === 'national' ? 'trophy' : 'map-pin' ?>"></i>
                </div>
                <div class="entry-point-info">
                    <span class="entry-point-name"><?= htmlspecialchars($ep['series_name']) ?></span>
                    <span class="badge badge-sm badge-<?= $ep['series_level'] === 'national' ? 'primary' : 'secondary' ?>">
                        <?= ucfirst($ep['series_level']) ?>
                    </span>
                </div>
                <div class="entry-point-stats">
                    <span class="entry-point-count"><?= number_format($ep['rider_count']) ?></span>
                    <span class="entry-point-pct"><?= round($pct, 1) ?>%</span>
                </div>
            </div>
            <?php endforeach; ?>
        </div>
    </div>
</div>
<?php endif; ?>

<?php endif; // end if no error ?>

<style>
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

/* Metric Sub */
.metric-sub {
    font-size: var(--text-xs);
    color: var(--color-text-muted);
    margin-top: 2px;
}

/* Flow Grid */
.flow-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
    gap: var(--space-md);
}

.flow-card {
    display: flex;
    flex-direction: column;
    padding: var(--space-md);
    background: var(--color-bg-surface);
    border: 1px solid var(--color-border);
    border-radius: var(--radius-md);
    transition: all 0.15s ease;
}

.flow-card:hover {
    border-color: var(--color-accent);
    box-shadow: var(--shadow-sm);
}

.flow-from,
.flow-to {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: var(--space-sm);
}

.flow-series {
    font-weight: var(--weight-medium);
    font-size: var(--text-sm);
}

.flow-arrow {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: var(--space-sm) 0;
    color: var(--color-accent);
}

.flow-arrow i {
    width: 20px;
    height: 20px;
}

.flow-count {
    font-size: var(--text-sm);
    font-weight: var(--weight-semibold);
    color: var(--color-accent);
}

/* Comparison Form */
.comparison-form {
    margin-bottom: var(--space-lg);
}

.comparison-selects {
    display: flex;
    align-items: flex-end;
    gap: var(--space-md);
    flex-wrap: wrap;
}

.comparison-selects .filter-group {
    flex: 1;
    min-width: 200px;
}

.comparison-vs {
    display: flex;
    align-items: center;
    justify-content: center;
    padding: var(--space-sm);
    color: var(--color-text-muted);
}

.comparison-vs i {
    width: 24px;
    height: 24px;
}

/* Overlap Result */
.overlap-result {
    margin-top: var(--space-xl);
    padding-top: var(--space-xl);
    border-top: 1px solid var(--color-border);
}

.overlap-result h3 {
    margin-bottom: var(--space-lg);
    font-size: var(--text-lg);
}

.overlap-visual {
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 0;
    margin-bottom: var(--space-xl);
}

.overlap-circle {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    width: 120px;
    height: 120px;
    border-radius: 50%;
    background: var(--color-bg-hover);
    border: 2px solid var(--color-border);
}

.overlap-left {
    margin-right: -30px;
    z-index: 1;
}

.overlap-right {
    margin-left: -30px;
    z-index: 1;
}

.overlap-intersection {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    width: 100px;
    height: 100px;
    border-radius: 50%;
    background: var(--color-accent-light);
    border: 3px solid var(--color-accent);
    z-index: 2;
}

.overlap-value {
    font-size: var(--text-xl);
    font-weight: var(--weight-bold);
}

.overlap-value--large {
    font-size: var(--text-2xl);
    color: var(--color-accent);
}

.overlap-label {
    font-size: var(--text-xs);
    color: var(--color-text-muted);
    text-align: center;
}

.overlap-stats {
    display: flex;
    justify-content: center;
    gap: var(--space-2xl);
}

.stat-item {
    text-align: center;
}

.stat-label {
    display: block;
    font-size: var(--text-sm);
    color: var(--color-text-secondary);
}

.stat-value {
    display: block;
    font-size: var(--text-2xl);
    font-weight: var(--weight-bold);
    color: var(--color-accent);
}

/* Progress Cell */
.progress-cell {
    display: flex;
    align-items: center;
    gap: var(--space-sm);
}

.progress-bar-mini {
    width: 60px;
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

.progress-fill--alt {
    background: var(--color-accent);
}

/* Entry Points Grid */
.entry-points-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
    gap: var(--space-md);
}

.entry-point-card {
    display: flex;
    align-items: center;
    gap: var(--space-md);
    padding: var(--space-md);
    background: var(--color-bg-surface);
    border: 1px solid var(--color-border);
    border-radius: var(--radius-md);
}

.entry-point-icon {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 40px;
    height: 40px;
    background: var(--color-accent-light);
    border-radius: var(--radius-md);
    color: var(--color-accent);
}

.entry-point-icon i {
    width: 20px;
    height: 20px;
}

.entry-point-info {
    flex: 1;
    display: flex;
    flex-direction: column;
    gap: 4px;
}

.entry-point-name {
    font-weight: var(--weight-medium);
    font-size: var(--text-sm);
}

.entry-point-stats {
    text-align: right;
}

.entry-point-count {
    display: block;
    font-size: var(--text-lg);
    font-weight: var(--weight-bold);
}

.entry-point-pct {
    display: block;
    font-size: var(--text-xs);
    color: var(--color-text-muted);
}

/* Empty State */
.empty-state {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: var(--space-2xl);
    color: var(--color-text-muted);
}

.empty-state i {
    width: 48px;
    height: 48px;
    margin-bottom: var(--space-md);
    opacity: 0.5;
}

/* Badges */
.badge-primary {
    background: var(--color-accent-light);
    color: var(--color-accent);
}

.badge-secondary {
    background: var(--color-bg-hover);
    color: var(--color-text-secondary);
}

.badge-info {
    background: rgba(56, 189, 248, 0.15);
    color: var(--color-info);
}

.badge-sm {
    font-size: 10px;
    padding: 2px 6px;
}

/* Text Link */
.text-link {
    color: var(--color-accent);
    text-decoration: none;
    font-weight: var(--weight-medium);
}

.text-link:hover {
    text-decoration: underline;
}

.text-muted {
    color: var(--color-text-muted);
    font-size: var(--text-sm);
}

/* Responsive */
@media (max-width: 899px) {
    .comparison-selects {
        flex-direction: column;
    }

    .comparison-selects .filter-group {
        width: 100%;
    }

    .comparison-vs {
        transform: rotate(90deg);
    }

    .overlap-visual {
        flex-direction: column;
    }

    .overlap-left,
    .overlap-right {
        margin: 0;
    }

    .overlap-left {
        margin-bottom: -30px;
    }

    .overlap-right {
        margin-top: -30px;
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

    .flow-grid {
        grid-template-columns: 1fr;
    }

    .entry-points-grid {
        grid-template-columns: 1fr;
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
        flex: 0 0 240px;
        scroll-snap-align: start;
    }

    .metric-value {
        font-size: var(--text-xl);
    }
}
</style>

<?php include __DIR__ . '/components/unified-layout-footer.php'; ?>
