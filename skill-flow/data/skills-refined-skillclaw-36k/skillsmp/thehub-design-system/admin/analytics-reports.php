<?php
/**
 * Analytics - Report Generator
 *
 * Genererar rapporter for:
 * - Arssammanfattning
 * - Serieanalys
 * - Klubbrapport
 * - Retention-analys
 * - Demographic overview
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

// Arval
$currentYear = (int)date('Y');
$selectedYear = isset($_GET['year']) ? (int)$_GET['year'] : $currentYear;

// Hamta tillgangliga ar
$availableYears = [];
$dataWarning = null;
try {
    $stmt = $pdo->query("SELECT DISTINCT season_year FROM rider_yearly_stats ORDER BY season_year DESC");
    $availableYears = $stmt->fetchAll(PDO::FETCH_COLUMN);
    if (empty($availableYears)) {
        // Tabellen finns men ar tom - kolla om events finns
        $eventStmt = $pdo->query("SELECT DISTINCT YEAR(date) as year FROM events WHERE date IS NOT NULL ORDER BY year DESC LIMIT 10");
        $eventYears = $eventStmt->fetchAll(PDO::FETCH_COLUMN);
        if (!empty($eventYears)) {
            $availableYears = $eventYears;
            $dataWarning = "Analytics-data saknas. Visar ar med events - kor Populate for att generera statistik.";
        }
    }
} catch (Exception $e) {
    $availableYears = range($currentYear, $currentYear - 5);
}

// Fallback om fortfarande tomt
if (empty($availableYears)) {
    $availableYears = range($currentYear, $currentYear - 5);
}

// Rapporttyp
$reportType = $_GET['report'] ?? 'summary';
$export = isset($_GET['export']);
$selectedSeries = isset($_GET['series']) ? (int)$_GET['series'] : null;
$selectedBrand = isset($_GET['brand']) ? (int)$_GET['brand'] : null;

// Hämta varumärken för filtrering
$availableBrands = [];
try {
    $brandStmt = $pdo->query("SELECT id, name FROM series_brands WHERE active = 1 ORDER BY name");
    $availableBrands = $brandStmt->fetchAll(PDO::FETCH_ASSOC);
} catch (Exception $e) {
    // Ignore
}

// Initiera KPI Calculator
$kpiCalc = new KPICalculator($pdo);

// Hamta serier med rookies for filtrering
$seriesWithRookies = [];

// Hamta data baserat pa rapport
$reportData = [];
$reportTitle = '';

try {
    switch ($reportType) {
        case 'summary':
            $reportTitle = "Arssammanfattning $selectedYear";
            $reportData = [
                'kpis' => $kpiCalc->getAllKPIs($selectedYear),
                'trends' => $kpiCalc->getGrowthTrend(5),
                'topClubs' => $kpiCalc->getTopClubs($selectedYear, 10),
                'disciplines' => $kpiCalc->getDisciplineDistribution($selectedYear),
                'ages' => $kpiCalc->getAgeDistribution($selectedYear)
            ];
            break;

        case 'retention':
            $reportTitle = "Retention & Churn-analys $selectedYear";
            $reportData = [
                'retention_rate' => $kpiCalc->getRetentionRate($selectedYear),
                'churn_rate' => $kpiCalc->getChurnRate($selectedYear),
                'new_riders' => $kpiCalc->getNewRidersCount($selectedYear),
                'retained_riders' => $kpiCalc->getRetainedRidersCount($selectedYear),
                'trend' => $kpiCalc->getRetentionTrend(5),
                'summary' => $kpiCalc->getChurnSummary($selectedYear),
                'by_segment' => $kpiCalc->getChurnBySegment($selectedYear),
                'inactive_duration' => $kpiCalc->getInactiveByDuration($selectedYear),
                'churned_list' => $kpiCalc->getChurnedRiders($selectedYear, 100),
                'one_timers' => $kpiCalc->getOneTimers($selectedYear, 2),
                'comebacks' => $kpiCalc->getComebackRiders($selectedYear),
                'win_back' => $kpiCalc->getWinBackTargets($selectedYear, 50)
            ];
            break;

        case 'series':
            $reportTitle = "Serie-analys $selectedYear";
            $reportData = [
                'entry_points' => $kpiCalc->getEntryPointDistribution($selectedYear),
                'feeder_matrix' => $kpiCalc->calculateFeederMatrix($selectedYear),
                'cross_rate' => $kpiCalc->getCrossParticipationRate($selectedYear)
            ];
            break;

        case 'clubs':
            $reportTitle = "Klubbrapport $selectedYear";
            $reportData = [
                'top_clubs' => $kpiCalc->getTopClubs($selectedYear, 50),
                'regions' => $kpiCalc->getRidersByRegion($selectedYear)
            ];
            break;

        case 'demographics':
            $reportTitle = "Demographic Overview $selectedYear";
            $reportData = [
                'average_age' => $kpiCalc->getAverageAge($selectedYear),
                'gender' => $kpiCalc->getGenderDistribution($selectedYear),
                'ages' => $kpiCalc->getAgeDistribution($selectedYear),
                'disciplines' => $kpiCalc->getDisciplineDistribution($selectedYear),
                'discipline_participation' => $kpiCalc->getDisciplineParticipation($selectedYear)
            ];
            break;

        case 'rookies':
            // Hamta serier for filtrering
            $seriesWithRookies = $kpiCalc->getSeriesWithRookies($selectedYear);

            $filterName = '';
            if ($selectedBrand) {
                foreach ($availableBrands as $b) {
                    if ((int)$b['id'] === $selectedBrand) {
                        $filterName = ' - ' . $b['name'];
                        break;
                    }
                }
            } elseif ($selectedSeries) {
                foreach ($seriesWithRookies as $s) {
                    if ((int)$s['id'] === $selectedSeries) {
                        $filterName = ' - ' . $s['name'];
                        break;
                    }
                }
            }

            $reportTitle = "Nya Deltagare (Rookies) $selectedYear" . $filterName;

            // Hämta listan först så vi kan räkna totaler från den
            // Brand har prioritet över serie
            $rookieList = $selectedBrand
                ? $kpiCalc->getRookiesListByBrand($selectedYear, $selectedBrand)
                : $kpiCalc->getRookiesList($selectedYear, $selectedSeries);

            $reportData = [
                'total_rookies' => count($rookieList),
                'total_riders' => $selectedBrand
                    ? $kpiCalc->getTotalActiveRiders($selectedYear, $selectedBrand)
                    : ($selectedSeries
                        ? $kpiCalc->getSeriesParticipants($selectedYear, $selectedSeries)
                        : $kpiCalc->getTotalActiveRiders($selectedYear)),
                'average_age' => $selectedBrand
                    ? $kpiCalc->getRookieAverageAgeByBrand($selectedYear, $selectedBrand)
                    : $kpiCalc->getRookieAverageAge($selectedYear, $selectedSeries),
                'gender' => $selectedBrand
                    ? $kpiCalc->getRookieGenderDistributionByBrand($selectedYear, $selectedBrand)
                    : $kpiCalc->getRookieGenderDistribution($selectedYear, $selectedSeries),
                'ages' => $selectedBrand
                    ? $kpiCalc->getRookieAgeDistributionByBrand($selectedYear, $selectedBrand)
                    : $kpiCalc->getRookieAgeDistribution($selectedYear, $selectedSeries),
                'classes' => $kpiCalc->getRookieClassDistribution($selectedYear, $selectedSeries),
                'disciplines' => $kpiCalc->getRookieDisciplineParticipation($selectedYear, $selectedSeries),
                'events' => $kpiCalc->getEventsWithMostRookies($selectedYear, 20, $selectedSeries),
                'clubs' => $selectedBrand
                    ? $kpiCalc->getClubsWithMostRookiesByBrand($selectedYear, 20, $selectedBrand)
                    : $kpiCalc->getClubsWithMostRookies($selectedYear, 20, $selectedSeries),
                'list' => $rookieList,
                'series_filter' => $seriesWithRookies,
                'brands_filter' => $availableBrands,
                'selected_brand' => $selectedBrand,
                'trend' => $kpiCalc->getRookieTrend(5),
                'age_trend' => $kpiCalc->getRookieAgeTrend(5)
            ];
            break;
    }
} catch (Throwable $e) {
    $error = $e->getMessage() . ' (Line: ' . $e->getLine() . ' in ' . basename($e->getFile()) . ')';
}

// Export to CSV
$exportType = $_GET['export'] ?? '';
if ($export && !isset($error)) {
    // Special export types
    if ($exportType === 'winback' && $reportType === 'retention') {
        header('Content-Type: text/csv; charset=utf-8');
        header('Content-Disposition: attachment; filename="thehub-winback-targets-' . $selectedYear . '.csv"');
        $output = fopen('php://output', 'w');
        fprintf($output, chr(0xEF).chr(0xBB).chr(0xBF)); // UTF-8 BOM
        fputcsv($output, ['Prioritet', 'Fornamn', 'Efternamn', 'Klubb', 'Alder', 'Sasonger', 'Totalt starter', 'Ar inaktiv', 'Discipliner', 'Profil']);
        foreach ($reportData['win_back'] as $rider) {
            fputcsv($output, [
                $rider['priority'],
                $rider['firstname'],
                $rider['lastname'],
                $rider['club_name'] ?? '',
                $rider['age'] ?? '',
                $rider['total_seasons'],
                $rider['total_events_all_time'],
                $rider['years_inactive'],
                $rider['primary_disciplines'] ?? '',
                'https://svenskmtb.se/rider/' . $rider['id']
            ]);
        }
        fclose($output);
        exit;
    }

    if ($exportType === 'churned' && $reportType === 'retention') {
        header('Content-Type: text/csv; charset=utf-8');
        header('Content-Disposition: attachment; filename="thehub-churned-' . $selectedYear . '.csv"');
        $output = fopen('php://output', 'w');
        fprintf($output, chr(0xEF).chr(0xBB).chr(0xBF)); // UTF-8 BOM
        fputcsv($output, ['Fornamn', 'Efternamn', 'Klubb', 'Alder', 'Starter ' . ($selectedYear-1), 'Disciplin', 'Forsta sasong', 'Sista sasong', 'Sasonger totalt', 'Profil']);
        foreach ($reportData['churned_list'] as $rider) {
            fputcsv($output, [
                $rider['firstname'],
                $rider['lastname'],
                $rider['club_name'] ?? '',
                $rider['age'] ?? '',
                $rider['last_year_events'] ?? '',
                $rider['last_discipline'] ?? '',
                $rider['first_season'] ?? '',
                $rider['last_season'] ?? '',
                $rider['total_seasons'] ?? '',
                'https://svenskmtb.se/rider/' . $rider['id']
            ]);
        }
        fclose($output);
        exit;
    }

    if ($exportType === 'comebacks' && $reportType === 'retention') {
        header('Content-Type: text/csv; charset=utf-8');
        header('Content-Disposition: attachment; filename="thehub-comebacks-' . $selectedYear . '.csv"');
        $output = fopen('php://output', 'w');
        fprintf($output, chr(0xEF).chr(0xBB).chr(0xBF)); // UTF-8 BOM
        fputcsv($output, ['Fornamn', 'Efternamn', 'Klubb', 'Alder', 'Ar borta', 'Forsta sasong ever', 'Starter ' . $selectedYear, 'Profil']);
        foreach ($reportData['comebacks'] as $rider) {
            fputcsv($output, [
                $rider['firstname'],
                $rider['lastname'],
                $rider['club_name'] ?? '',
                $rider['age'] ?? '',
                $rider['years_away'],
                $rider['first_season_ever'] ?? '',
                $rider['current_events'],
                'https://svenskmtb.se/rider/' . $rider['id']
            ]);
        }
        fclose($output);
        exit;
    }

    header('Content-Type: text/csv; charset=utf-8');
    header('Content-Disposition: attachment; filename="thehub-' . $reportType . '-' . $selectedYear . '.csv"');

    $output = fopen('php://output', 'w');
    fprintf($output, chr(0xEF).chr(0xBB).chr(0xBF)); // UTF-8 BOM

    switch ($reportType) {
        case 'summary':
            fputcsv($output, ['Nyckeltal', 'Varde']);
            foreach ($reportData['kpis'] as $key => $value) {
                if (!is_array($value)) {
                    fputcsv($output, [ucfirst(str_replace('_', ' ', $key)), $value]);
                }
            }
            fputcsv($output, []);
            fputcsv($output, ['Top Klubbar']);
            fputcsv($output, ['Klubb', 'Stad', 'Aktiva', 'Poang', 'Vinster']);
            foreach ($reportData['topClubs'] as $club) {
                fputcsv($output, [$club['club_name'], $club['city'] ?? '', $club['active_riders'], $club['total_points'], $club['wins']]);
            }
            break;

        case 'retention':
            fputcsv($output, ['Metric', 'Varde']);
            fputcsv($output, ['Retention Rate', $reportData['retention_rate'] . '%']);
            fputcsv($output, ['Churn Rate', $reportData['churn_rate'] . '%']);
            fputcsv($output, ['Nya Riders', $reportData['new_riders']]);
            fputcsv($output, ['Atervandare', $reportData['retained_riders']]);
            fputcsv($output, []);
            fputcsv($output, ['Trend']);
            fputcsv($output, ['Ar', 'Retention Rate']);
            foreach ($reportData['trend'] as $t) {
                fputcsv($output, [$t['year'], $t['retention_rate'] . '%']);
            }
            break;

        case 'clubs':
            fputcsv($output, ['Klubb', 'Stad', 'Aktiva Riders', 'Totala Poang', 'Vinster', 'Pallplatser']);
            foreach ($reportData['top_clubs'] as $club) {
                fputcsv($output, [
                    $club['club_name'],
                    $club['city'] ?? '',
                    $club['active_riders'],
                    $club['total_points'],
                    $club['wins'],
                    $club['podiums']
                ]);
            }
            break;

        case 'demographics':
            fputcsv($output, ['Demographic', 'Varde']);
            fputcsv($output, ['Snittålder', $reportData['average_age']]);
            fputcsv($output, ['Antal Man', $reportData['gender']['M']]);
            fputcsv($output, ['Antal Kvinnor', $reportData['gender']['F']]);
            fputcsv($output, []);
            fputcsv($output, ['Aldersfordelning']);
            fputcsv($output, ['Grupp', 'Antal']);
            foreach ($reportData['ages'] as $age) {
                fputcsv($output, [$age['age_group'], $age['count']]);
            }
            break;

        case 'rookies':
            fputcsv($output, ['Rider ID', 'Fornamn', 'Efternamn', 'Alder', 'Fodelsear', 'Kon', 'Klubb', 'Serie', 'Events', 'Poang', 'Basta Placering', 'Disciplin', 'Profil URL']);
            foreach ($reportData['list'] as $rookie) {
                $profileUrl = 'https://thehub.se/rider/' . $rookie['rider_id'];
                fputcsv($output, [
                    $rookie['rider_id'],
                    $rookie['firstname'],
                    $rookie['lastname'],
                    $rookie['age'] ?? '-',
                    $rookie['birth_year'] ?? '-',
                    $rookie['gender'] ?? '-',
                    $rookie['club_name'] ?? 'Ingen klubb',
                    $rookie['series_name'] ?? '-',
                    $rookie['total_events'],
                    $rookie['total_points'],
                    $rookie['best_position'],
                    $rookie['primary_discipline'] ?? '-',
                    $profileUrl
                ]);
            }
            break;
    }

    fclose($output);
    exit;
}

// Page config
$page_title = 'Rapportgenerator';
$breadcrumbs = [
    ['label' => 'Analytics', 'url' => '/admin/analytics-dashboard.php'],
    ['label' => 'Rapporter']
];

// Include unified layout
include __DIR__ . '/components/unified-layout.php';
?>

<!-- Report Selector -->
<div class="report-selector">
    <form method="get" class="report-form">
        <div class="report-options">
            <label class="report-option <?= $reportType === 'summary' ? 'active' : '' ?>">
                <input type="radio" name="report" value="summary" <?= $reportType === 'summary' ? 'checked' : '' ?> onchange="this.form.submit()">
                <i data-lucide="file-text"></i>
                <span>Arssammanfattning</span>
            </label>

            <label class="report-option <?= $reportType === 'retention' ? 'active' : '' ?>">
                <input type="radio" name="report" value="retention" <?= $reportType === 'retention' ? 'checked' : '' ?> onchange="this.form.submit()">
                <i data-lucide="refresh-cw"></i>
                <span>Retention</span>
            </label>

            <label class="report-option <?= $reportType === 'series' ? 'active' : '' ?>">
                <input type="radio" name="report" value="series" <?= $reportType === 'series' ? 'checked' : '' ?> onchange="this.form.submit()">
                <i data-lucide="git-branch"></i>
                <span>Serie-analys</span>
            </label>

            <label class="report-option <?= $reportType === 'clubs' ? 'active' : '' ?>">
                <input type="radio" name="report" value="clubs" <?= $reportType === 'clubs' ? 'checked' : '' ?> onchange="this.form.submit()">
                <i data-lucide="building"></i>
                <span>Klubbar</span>
            </label>

            <label class="report-option <?= $reportType === 'demographics' ? 'active' : '' ?>">
                <input type="radio" name="report" value="demographics" <?= $reportType === 'demographics' ? 'checked' : '' ?> onchange="this.form.submit()">
                <i data-lucide="users"></i>
                <span>Demografi</span>
            </label>

            <label class="report-option <?= $reportType === 'rookies' ? 'active' : '' ?>">
                <input type="radio" name="report" value="rookies" <?= $reportType === 'rookies' ? 'checked' : '' ?> onchange="this.form.submit()">
                <i data-lucide="user-plus"></i>
                <span>Nya Deltagare</span>
            </label>
        </div>

        <div class="report-controls">
            <select name="year" class="form-select" onchange="this.form.submit()">
                <?php foreach ($availableYears as $year): ?>
                    <option value="<?= $year ?>" <?= $year == $selectedYear ? 'selected' : '' ?>>
                        <?= $year ?>
                    </option>
                <?php endforeach; ?>
            </select>

            <a href="?report=<?= $reportType ?>&year=<?= $selectedYear ?>&export=1" class="btn-admin btn-admin-primary">
                <i data-lucide="download"></i> Exportera CSV
            </a>
        </div>
    </form>
</div>

<?php if (isset($dataWarning)): ?>
<div class="alert alert-info" style="margin-bottom: var(--space-lg);">
    <i data-lucide="info"></i>
    <div>
        <?= htmlspecialchars($dataWarning) ?>
        <a href="/admin/analytics-populate.php" class="btn-admin btn-admin-sm" style="margin-left: var(--space-md);">Populate Data</a>
    </div>
</div>
<?php endif; ?>

<?php if (isset($error)): ?>
<div class="alert alert-warning">
    <i data-lucide="alert-triangle"></i>
    <div>
        <strong>Fel vid inlasning av data</strong><br>
        <?= htmlspecialchars($error) ?>
        <br><br>
        <small>Kor <a href="/admin/analytics-populate.php">Populate Historical</a> for att generera data.</small>
    </div>
</div>
<?php elseif (empty($availableYears)): ?>
<div class="alert alert-warning">
    <i data-lucide="alert-triangle"></i>
    <div>
        <strong>Ingen data tillganglig</strong><br>
        Kor <a href="/admin/analytics-populate.php">Populate Historical</a> for att generera historisk data.
    </div>
</div>
<?php else: ?>

<!-- Report Content -->
<div class="report-container">
    <div class="report-header">
        <h2><?= htmlspecialchars($reportTitle) ?></h2>
        <span class="report-date">Genererad: <?= date('Y-m-d H:i') ?></span>
    </div>

    <?php if ($reportType === 'summary'): ?>
    <!-- Summary Report -->
    <div class="report-section">
        <h3>Nyckeltal</h3>
        <div class="kpi-grid">
            <div class="kpi-item">
                <span class="kpi-value"><?= number_format($reportData['kpis']['total_riders'] ?? 0) ?></span>
                <span class="kpi-label">Aktiva Riders</span>
            </div>
            <div class="kpi-item">
                <span class="kpi-value"><?= number_format($reportData['kpis']['new_riders'] ?? 0) ?></span>
                <span class="kpi-label">Nya Riders</span>
            </div>
            <div class="kpi-item">
                <span class="kpi-value"><?= number_format($reportData['kpis']['retention_rate'] ?? 0, 1) ?>%</span>
                <span class="kpi-label">Retention Rate</span>
            </div>
            <div class="kpi-item">
                <span class="kpi-value"><?= ($reportData['kpis']['growth_rate'] ?? 0) >= 0 ? '+' : '' ?><?= number_format($reportData['kpis']['growth_rate'] ?? 0, 1) ?>%</span>
                <span class="kpi-label">Tillvaxt</span>
            </div>
        </div>
    </div>

    <div class="report-section">
        <h3>Top 10 Klubbar</h3>
        <table class="report-table">
            <thead>
                <tr>
                    <th>#</th>
                    <th>Klubb</th>
                    <th>Stad</th>
                    <th>Aktiva</th>
                    <th>Poang</th>
                    <th>Vinster</th>
                </tr>
            </thead>
            <tbody>
                <?php foreach ($reportData['topClubs'] as $i => $club): ?>
                <tr>
                    <td><?= $i + 1 ?></td>
                    <td><?= htmlspecialchars($club['club_name']) ?></td>
                    <td><?= htmlspecialchars($club['city'] ?? '-') ?></td>
                    <td><?= number_format($club['active_riders']) ?></td>
                    <td><?= number_format($club['total_points']) ?></td>
                    <td><?= number_format($club['wins']) ?></td>
                </tr>
                <?php endforeach; ?>
            </tbody>
        </table>
    </div>

    <?php elseif ($reportType === 'retention'): ?>
    <!-- Retention & Churn Report -->
    <div class="report-section">
        <h3>Retention & Churn Oversikt</h3>
        <div class="kpi-grid">
            <div class="kpi-item kpi-item--large">
                <span class="kpi-value"><?= number_format($reportData['retention_rate'], 1) ?>%</span>
                <span class="kpi-label">Retention Rate</span>
            </div>
            <div class="kpi-item kpi-item--large" style="--kpi-color: var(--color-error);">
                <span class="kpi-value"><?= number_format($reportData['churn_rate'], 1) ?>%</span>
                <span class="kpi-label">Churn Rate</span>
            </div>
            <div class="kpi-item">
                <span class="kpi-value"><?= number_format($reportData['summary']['churned_last_year'] ?? 0) ?></span>
                <span class="kpi-label">Slutade <?= $selectedYear - 1 ?></span>
            </div>
            <div class="kpi-item" style="--kpi-color: var(--color-success);">
                <span class="kpi-value"><?= number_format($reportData['summary']['comebacks_this_year'] ?? 0) ?></span>
                <span class="kpi-label">Comebacks i ar</span>
            </div>
        </div>

        <div class="retention-breakdown">
            <div class="retention-stat">
                <i data-lucide="user-plus"></i>
                <div>
                    <span class="retention-value"><?= number_format($reportData['new_riders']) ?></span>
                    <span class="retention-label">Nya riders <?= $selectedYear ?></span>
                </div>
            </div>
            <div class="retention-stat">
                <i data-lucide="refresh-cw"></i>
                <div>
                    <span class="retention-value"><?= number_format($reportData['retained_riders']) ?></span>
                    <span class="retention-label">Atervandare fran <?= $selectedYear - 1 ?></span>
                </div>
            </div>
            <div class="retention-stat">
                <i data-lucide="user-x"></i>
                <div>
                    <span class="retention-value"><?= number_format($reportData['summary']['one_timers_total'] ?? 0) ?></span>
                    <span class="retention-label">One-timers (1-2 starter totalt)</span>
                </div>
            </div>
            <div class="retention-stat">
                <i data-lucide="clock"></i>
                <div>
                    <span class="retention-value"><?= number_format($reportData['summary']['inactive_2plus_years'] ?? 0) ?></span>
                    <span class="retention-label">Inaktiva 2+ ar</span>
                </div>
            </div>
        </div>
    </div>

    <!-- Retention Trend Chart -->
    <div class="report-section">
        <h3>Retention & Churn Trend (5 ar)</h3>
        <div style="max-width: 600px; margin-bottom: var(--space-lg);">
            <canvas id="retentionChart"></canvas>
        </div>
        <script>
        document.addEventListener('DOMContentLoaded', function() {
            const ctx = document.getElementById('retentionChart');
            if (ctx) {
                new Chart(ctx, {
                    type: 'line',
                    data: {
                        labels: <?= json_encode(array_column($reportData['trend'], 'year')) ?>,
                        datasets: [{
                            label: 'Retention Rate %',
                            data: <?= json_encode(array_column($reportData['trend'], 'retention_rate')) ?>,
                            borderColor: 'rgb(16, 185, 129)',
                            backgroundColor: 'rgba(16, 185, 129, 0.1)',
                            fill: true,
                            tension: 0.3
                        }, {
                            label: 'Churn Rate %',
                            data: <?= json_encode(array_column($reportData['trend'], 'churn_rate')) ?>,
                            borderColor: 'rgb(239, 68, 68)',
                            backgroundColor: 'rgba(239, 68, 68, 0.1)',
                            fill: true,
                            tension: 0.3
                        }]
                    },
                    options: {
                        responsive: true,
                        plugins: { legend: { position: 'bottom' } },
                        scales: {
                            y: { min: 0, max: 100, title: { display: true, text: '%' } }
                        }
                    }
                });
            }
        });
        </script>
    </div>

    <!-- Inaktiva per duration -->
    <?php if (!empty($reportData['inactive_duration'])): ?>
    <div class="report-section">
        <h3>Hur lange har de varit borta?</h3>
        <p style="color: var(--color-text-secondary); font-size: var(--text-sm); margin-bottom: var(--space-md);">
            Deltagare som inte tavlat <?= $selectedYear ?>, grupperade efter antal ar sedan senaste start.
        </p>
        <table class="report-table">
            <thead>
                <tr>
                    <th>Ar sedan senast</th>
                    <th>Antal</th>
                    <th>Snittålder</th>
                </tr>
            </thead>
            <tbody>
                <?php foreach ($reportData['inactive_duration'] as $row): ?>
                <tr>
                    <td><?= $row['years_inactive'] ?> ar</td>
                    <td><strong><?= number_format($row['count']) ?></strong></td>
                    <td><?= $row['avg_age'] ? number_format($row['avg_age'], 0) . ' ar' : '-' ?></td>
                </tr>
                <?php endforeach; ?>
            </tbody>
        </table>
    </div>
    <?php endif; ?>

    <!-- Churn per segment -->
    <?php if (!empty($reportData['by_segment'])): ?>
    <div class="report-section">
        <h3>Churn per Aldersgrupp</h3>
        <p style="color: var(--color-text-secondary); font-size: var(--text-sm); margin-bottom: var(--space-md);">
            Vilka aldersgrupper tappar vi flest deltagare fran?
        </p>
        <table class="report-table">
            <thead>
                <tr>
                    <th>Aldersgrupp</th>
                    <th>Antal slutat</th>
                    <th>Churn Rate</th>
                </tr>
            </thead>
            <tbody>
                <?php foreach ($reportData['by_segment']['by_age'] as $row): ?>
                <tr>
                    <td><?= htmlspecialchars($row['age_group']) ?></td>
                    <td><strong><?= number_format($row['churned_count']) ?></strong></td>
                    <td>
                        <div class="progress-cell">
                            <div class="progress-bar-mini" style="--bar-color: var(--color-error);">
                                <div class="progress-fill" style="width: <?= min($row['churn_rate'], 100) ?>%; background: var(--color-error);"></div>
                            </div>
                            <span><?= number_format($row['churn_rate'], 1) ?>%</span>
                        </div>
                    </td>
                </tr>
                <?php endforeach; ?>
            </tbody>
        </table>
    </div>

    <div class="report-section">
        <h3>Churn per Disciplin</h3>
        <table class="report-table">
            <thead>
                <tr>
                    <th>Disciplin</th>
                    <th>Antal slutat</th>
                </tr>
            </thead>
            <tbody>
                <?php foreach ($reportData['by_segment']['by_discipline'] as $row): ?>
                <tr>
                    <td><?= htmlspecialchars($row['discipline']) ?></td>
                    <td><strong><?= number_format($row['churned_count']) ?></strong></td>
                </tr>
                <?php endforeach; ?>
            </tbody>
        </table>
    </div>
    <?php endif; ?>

    <!-- Comeback Riders -->
    <?php if (!empty($reportData['comebacks'])): ?>
    <div class="report-section">
        <h3><i data-lucide="rotate-ccw" style="width: 20px; height: 20px;"></i> Comebacks <?= $selectedYear ?></h3>
        <p style="color: var(--color-text-secondary); font-size: var(--text-sm); margin-bottom: var(--space-md);">
            Deltagare som aterkom efter minst ett ars uppehall. Dessa ar vardefulla - de valde att komma tillbaka!
        </p>
        <a href="?report=retention&year=<?= $selectedYear ?>&export=comebacks" class="btn btn-secondary" style="margin-bottom: var(--space-md);">
            <i data-lucide="download"></i> Exportera Comebacks (CSV)
        </a>
        <table class="report-table">
            <thead>
                <tr>
                    <th>Namn</th>
                    <th>Klubb</th>
                    <th>Alder</th>
                    <th>Ar borta</th>
                    <th>Forsta sasong</th>
                    <th>Starter <?= $selectedYear ?></th>
                </tr>
            </thead>
            <tbody>
                <?php foreach (array_slice($reportData['comebacks'], 0, 50) as $rider): ?>
                <tr>
                    <td>
                        <a href="/rider/<?= $rider['id'] ?>" style="color: var(--color-accent);">
                            <?= htmlspecialchars($rider['firstname'] . ' ' . $rider['lastname']) ?>
                        </a>
                    </td>
                    <td><?= htmlspecialchars($rider['club_name'] ?? '-') ?></td>
                    <td><?= $rider['age'] ?? '-' ?></td>
                    <td><strong><?= $rider['years_away'] ?> ar</strong></td>
                    <td><?= $rider['first_season_ever'] ?? '-' ?></td>
                    <td><?= $rider['current_events'] ?></td>
                </tr>
                <?php endforeach; ?>
            </tbody>
        </table>
    </div>
    <?php endif; ?>

    <!-- Win-Back Targets -->
    <?php if (!empty($reportData['win_back'])): ?>
    <div class="report-section">
        <h3><i data-lucide="target" style="width: 20px; height: 20px;"></i> Win-Back Targets</h3>
        <p style="color: var(--color-text-secondary); font-size: var(--text-sm); margin-bottom: var(--space-md);">
            Inaktiva deltagare med hog potential att atervanda. Prioriterade efter tidigare engagemang.
        </p>
        <a href="?report=retention&year=<?= $selectedYear ?>&export=winback" class="btn btn-secondary" style="margin-bottom: var(--space-md);">
            <i data-lucide="download"></i> Exportera Win-Back Lista (CSV)
        </a>
        <table class="report-table">
            <thead>
                <tr>
                    <th>Prioritet</th>
                    <th>Namn</th>
                    <th>Klubb</th>
                    <th>Alder</th>
                    <th>Sasonger</th>
                    <th>Totalt starter</th>
                    <th>Ar inaktiv</th>
                    <th>Discipliner</th>
                </tr>
            </thead>
            <tbody>
                <?php foreach ($reportData['win_back'] as $rider): ?>
                <tr>
                    <td>
                        <span class="badge badge-<?= $rider['priority'] === 'Hog' ? 'success' : ($rider['priority'] === 'Medium' ? 'warning' : 'secondary') ?>">
                            <?= $rider['priority'] ?>
                        </span>
                    </td>
                    <td>
                        <a href="/rider/<?= $rider['id'] ?>" style="color: var(--color-accent);">
                            <?= htmlspecialchars($rider['firstname'] . ' ' . $rider['lastname']) ?>
                        </a>
                    </td>
                    <td><?= htmlspecialchars($rider['club_name'] ?? '-') ?></td>
                    <td><?= $rider['age'] ?? '-' ?></td>
                    <td><?= $rider['total_seasons'] ?></td>
                    <td><?= $rider['total_events_all_time'] ?></td>
                    <td><?= $rider['years_inactive'] ?> ar</td>
                    <td><?= htmlspecialchars($rider['primary_disciplines'] ?? '-') ?></td>
                </tr>
                <?php endforeach; ?>
            </tbody>
        </table>
    </div>
    <?php endif; ?>

    <!-- Churned Riders (slutade forra aret) -->
    <?php if (!empty($reportData['churned_list'])): ?>
    <div class="report-section">
        <h3><i data-lucide="user-x" style="width: 20px; height: 20px;"></i> Slutade <?= $selectedYear - 1 ?></h3>
        <p style="color: var(--color-text-secondary); font-size: var(--text-sm); margin-bottom: var(--space-md);">
            Deltagare som tavlade <?= $selectedYear - 1 ?> men inte <?= $selectedYear ?>.
            Top <?= min(count($reportData['churned_list']), 100) ?> sorterade efter antal starter.
        </p>
        <a href="?report=retention&year=<?= $selectedYear ?>&export=churned" class="btn btn-secondary" style="margin-bottom: var(--space-md);">
            <i data-lucide="download"></i> Exportera Churned Lista (CSV)
        </a>
        <table class="report-table">
            <thead>
                <tr>
                    <th>Namn</th>
                    <th>Klubb</th>
                    <th>Alder</th>
                    <th>Starter <?= $selectedYear - 1 ?></th>
                    <th>Disciplin</th>
                    <th>Aktiv sedan</th>
                    <th>Sasonger</th>
                </tr>
            </thead>
            <tbody>
                <?php foreach ($reportData['churned_list'] as $rider): ?>
                <tr>
                    <td>
                        <a href="/rider/<?= $rider['id'] ?>" style="color: var(--color-accent);">
                            <?= htmlspecialchars($rider['firstname'] . ' ' . $rider['lastname']) ?>
                        </a>
                    </td>
                    <td><?= htmlspecialchars($rider['club_name'] ?? '-') ?></td>
                    <td><?= $rider['age'] ?? '-' ?></td>
                    <td><strong><?= $rider['last_year_events'] ?? '-' ?></strong></td>
                    <td><?= htmlspecialchars($rider['last_discipline'] ?? '-') ?></td>
                    <td><?= $rider['first_season'] ?? '-' ?></td>
                    <td><?= $rider['total_seasons'] ?? '-' ?></td>
                </tr>
                <?php endforeach; ?>
            </tbody>
        </table>
    </div>
    <?php endif; ?>

    <!-- One-Timers -->
    <?php if (!empty($reportData['one_timers'])): ?>
    <div class="report-section">
        <h3><i data-lucide="user-minus" style="width: 20px; height: 20px;"></i> One-Timers (1-2 starter)</h3>
        <p style="color: var(--color-text-secondary); font-size: var(--text-sm); margin-bottom: var(--space-md);">
            Deltagare som bara startat 1-2 ganger totalt. Dessa provade sporten men fortsatte inte.
            Senaste <?= min(count($reportData['one_timers']), 100) ?> visas.
        </p>
        <table class="report-table">
            <thead>
                <tr>
                    <th>Namn</th>
                    <th>Klubb</th>
                    <th>Alder</th>
                    <th>Starter</th>
                    <th>Forsta sasong</th>
                    <th>Sista sasong</th>
                    <th>Discipliner</th>
                </tr>
            </thead>
            <tbody>
                <?php foreach (array_slice($reportData['one_timers'], 0, 100) as $rider): ?>
                <tr>
                    <td>
                        <a href="/rider/<?= $rider['id'] ?>" style="color: var(--color-accent);">
                            <?= htmlspecialchars($rider['firstname'] . ' ' . $rider['lastname']) ?>
                        </a>
                    </td>
                    <td><?= htmlspecialchars($rider['club_name'] ?? '-') ?></td>
                    <td><?= $rider['age'] ?? '-' ?></td>
                    <td><?= $rider['total_events'] ?></td>
                    <td><?= $rider['first_season'] ?></td>
                    <td><?= $rider['last_season'] ?></td>
                    <td><?= htmlspecialchars($rider['disciplines'] ?? '-') ?></td>
                </tr>
                <?php endforeach; ?>
            </tbody>
        </table>
    </div>
    <?php endif; ?>

    <?php elseif ($reportType === 'series'): ?>
    <!-- Series Report -->
    <div class="report-section">
        <h3>Cross-participation</h3>
        <div class="kpi-grid">
            <div class="kpi-item kpi-item--large">
                <span class="kpi-value"><?= number_format($reportData['cross_rate'], 1) ?>%</span>
                <span class="kpi-label">Riders i 2+ serier</span>
            </div>
        </div>
    </div>

    <div class="report-section">
        <h3>Entry Points - Var borjar nya riders?</h3>
        <table class="report-table">
            <thead>
                <tr>
                    <th>Serie</th>
                    <th>Niva</th>
                    <th>Nya Riders</th>
                    <th>Andel</th>
                </tr>
            </thead>
            <tbody>
                <?php
                $totalEntry = array_sum(array_column($reportData['entry_points'], 'rider_count')) ?: 1;
                foreach ($reportData['entry_points'] as $ep):
                    $pct = ($ep['rider_count'] / $totalEntry) * 100;
                ?>
                <tr>
                    <td><?= htmlspecialchars($ep['series_name']) ?></td>
                    <td><?= ucfirst($ep['series_level']) ?></td>
                    <td><?= number_format($ep['rider_count']) ?></td>
                    <td><?= round($pct, 1) ?>%</td>
                </tr>
                <?php endforeach; ?>
            </tbody>
        </table>
    </div>

    <?php elseif ($reportType === 'clubs'): ?>
    <!-- Clubs Report -->
    <div class="report-section">
        <h3>Alla Klubbar</h3>
        <table class="report-table">
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
                <?php foreach ($reportData['top_clubs'] as $i => $club): ?>
                <tr>
                    <td><?= $i + 1 ?></td>
                    <td><?= htmlspecialchars($club['club_name']) ?></td>
                    <td><?= htmlspecialchars($club['city'] ?? '-') ?></td>
                    <td><?= number_format($club['active_riders']) ?></td>
                    <td><?= number_format($club['total_points']) ?></td>
                    <td><?= number_format($club['wins']) ?></td>
                    <td><?= number_format($club['podiums']) ?></td>
                </tr>
                <?php endforeach; ?>
            </tbody>
        </table>
    </div>

    <?php if (!empty($reportData['regions'])): ?>
    <div class="report-section">
        <h3>Riders per Region</h3>
        <table class="report-table">
            <thead>
                <tr>
                    <th>Region</th>
                    <th>Antal Riders</th>
                </tr>
            </thead>
            <tbody>
                <?php foreach ($reportData['regions'] as $region): ?>
                <tr>
                    <td><?= htmlspecialchars($region['region']) ?></td>
                    <td><?= number_format($region['rider_count']) ?></td>
                </tr>
                <?php endforeach; ?>
            </tbody>
        </table>
    </div>
    <?php endif; ?>

    <?php elseif ($reportType === 'demographics'): ?>
    <!-- Demographics Report -->
    <div class="report-section">
        <h3>Oversikt</h3>
        <div class="kpi-grid">
            <div class="kpi-item">
                <span class="kpi-value"><?= number_format($reportData['average_age'], 0) ?> ar</span>
                <span class="kpi-label">Snittålder</span>
            </div>
            <div class="kpi-item">
                <span class="kpi-value"><?= number_format($reportData['gender']['M']) ?></span>
                <span class="kpi-label">Man</span>
            </div>
            <div class="kpi-item">
                <span class="kpi-value"><?= number_format($reportData['gender']['F']) ?></span>
                <span class="kpi-label">Kvinnor</span>
            </div>
            <?php
            $total = $reportData['gender']['M'] + $reportData['gender']['F'];
            $femalePct = $total > 0 ? round($reportData['gender']['F'] / $total * 100, 1) : 0;
            ?>
            <div class="kpi-item">
                <span class="kpi-value"><?= $femalePct ?>%</span>
                <span class="kpi-label">Andel kvinnor</span>
            </div>
        </div>
    </div>

    <div class="report-section">
        <h3>Aldersfordelning</h3>
        <table class="report-table">
            <thead>
                <tr>
                    <th>Aldersgrupp</th>
                    <th>Antal</th>
                    <th>Andel</th>
                </tr>
            </thead>
            <tbody>
                <?php
                $totalAge = array_sum(array_column($reportData['ages'], 'count')) ?: 1;
                foreach ($reportData['ages'] as $age):
                    $pct = ($age['count'] / $totalAge) * 100;
                ?>
                <tr>
                    <td><?= htmlspecialchars($age['age_group']) ?></td>
                    <td><?= number_format($age['count']) ?></td>
                    <td><?= round($pct, 1) ?>%</td>
                </tr>
                <?php endforeach; ?>
            </tbody>
        </table>
    </div>

    <div class="report-section">
        <h3>Deltagande per Disciplin (faktiskt)</h3>
        <p style="color: var(--color-text-secondary); font-size: var(--text-sm); margin-bottom: var(--space-md);">
            Antal unika deltagare som faktiskt deltagit i varje disciplin. En person kan raknas i flera discipliner.
        </p>
        <?php if (!empty($reportData['discipline_participation'])): ?>
        <table class="report-table">
            <thead>
                <tr>
                    <th>Disciplin</th>
                    <th>Unika Deltagare</th>
                    <th>Totalt Starter</th>
                </tr>
            </thead>
            <tbody>
                <?php foreach ($reportData['discipline_participation'] as $disc): ?>
                <tr>
                    <td><?= htmlspecialchars($disc['discipline']) ?></td>
                    <td><strong><?= number_format($disc['unique_riders']) ?></strong></td>
                    <td><?= number_format($disc['total_starts']) ?></td>
                </tr>
                <?php endforeach; ?>
            </tbody>
        </table>
        <?php else: ?>
        <p>Ingen data tillganglig.</p>
        <?php endif; ?>
    </div>

    <div class="report-section">
        <h3>Huvuddisciplin (primary)</h3>
        <p style="color: var(--color-text-secondary); font-size: var(--text-sm); margin-bottom: var(--space-md);">
            Den disciplin varje akare deltagit i MEST. En person raknas bara en gang.
        </p>
        <table class="report-table">
            <thead>
                <tr>
                    <th>Disciplin</th>
                    <th>Antal</th>
                    <th>Andel</th>
                </tr>
            </thead>
            <tbody>
                <?php
                $totalDisc = array_sum(array_column($reportData['disciplines'], 'count')) ?: 1;
                foreach ($reportData['disciplines'] as $disc):
                    $pct = ($disc['count'] / $totalDisc) * 100;
                ?>
                <tr>
                    <td><?= htmlspecialchars($disc['discipline']) ?></td>
                    <td><?= number_format($disc['count']) ?></td>
                    <td><?= round($pct, 1) ?>%</td>
                </tr>
                <?php endforeach; ?>
            </tbody>
        </table>
    </div>

    <?php elseif ($reportType === 'rookies'): ?>
    <!-- Rookies Report -->

    <div class="report-section" style="padding-bottom: 0;">
        <div class="series-filter-row" style="display: flex; align-items: center; gap: var(--space-md); flex-wrap: wrap;">
            <?php if (!empty($reportData['brands_filter'])): ?>
            <label style="font-weight: var(--weight-medium);">Varumärke:</label>
            <select onchange="window.location.href='?report=rookies&year=<?= $selectedYear ?>&brand=' + this.value" class="form-select" style="width: auto; min-width: 200px;">
                <option value="">Alla varumärken</option>
                <?php foreach ($reportData['brands_filter'] as $brand): ?>
                <option value="<?= $brand['id'] ?>" <?= $selectedBrand == $brand['id'] ? 'selected' : '' ?>>
                    <?= htmlspecialchars($brand['name']) ?>
                </option>
                <?php endforeach; ?>
            </select>
            <?php endif; ?>

            <?php if (!$selectedBrand && !empty($reportData['series_filter'])): ?>
            <label style="font-weight: var(--weight-medium);">Serie:</label>
            <select onchange="window.location.href='?report=rookies&year=<?= $selectedYear ?>&series=' + this.value" class="form-select" style="width: auto; min-width: 200px;">
                <option value="">Alla serier</option>
                <?php foreach ($reportData['series_filter'] as $series): ?>
                <option value="<?= $series['id'] ?>" <?= $selectedSeries == $series['id'] ? 'selected' : '' ?>>
                    <?= htmlspecialchars($series['name']) ?> (<?= $series['rookie_count'] ?> rookies)
                </option>
                <?php endforeach; ?>
            </select>
            <?php endif; ?>

            <?php if ($selectedSeries || $selectedBrand): ?>
            <a href="?report=rookies&year=<?= $selectedYear ?>" class="btn-admin btn-admin-ghost btn-admin-sm">
                <i data-lucide="x" style="width:14px;height:14px;"></i> Rensa filter
            </a>
            <?php endif; ?>
        </div>
    </div>

    <div class="report-section">
        <h3>Oversikt <?= ($selectedSeries || $selectedBrand) ? '(filtrerad)' : '' ?></h3>
        <?php
        $rookiePct = $reportData['total_riders'] > 0
            ? round($reportData['total_rookies'] / $reportData['total_riders'] * 100, 1)
            : 0;
        $totalGender = $reportData['gender']['M'] + $reportData['gender']['F'];
        $femalePct = $totalGender > 0 ? round($reportData['gender']['F'] / $totalGender * 100, 1) : 0;
        ?>
        <div class="kpi-grid">
            <div class="kpi-item">
                <span class="kpi-value"><?= number_format($reportData['total_rookies']) ?></span>
                <span class="kpi-label">Nya Deltagare</span>
            </div>
            <div class="kpi-item">
                <span class="kpi-value"><?= $rookiePct ?>%</span>
                <span class="kpi-label">Andel av totalt</span>
            </div>
            <div class="kpi-item">
                <span class="kpi-value"><?= number_format($reportData['average_age'], 0) ?> ar</span>
                <span class="kpi-label">Snittålder</span>
            </div>
            <div class="kpi-item">
                <span class="kpi-value"><?= $femalePct ?>%</span>
                <span class="kpi-label">Andel kvinnor</span>
            </div>
        </div>
    </div>

    <?php if (!empty($reportData['trend'])): ?>
    <div class="report-section">
        <h3>Rookie-trend (5 ar)</h3>
        <div class="trend-chart-container" style="display: grid; grid-template-columns: 1fr 1fr; gap: var(--space-lg);">
            <div>
                <canvas id="rookieTrendChart" height="200"></canvas>
            </div>
            <div>
                <table class="report-table">
                    <thead>
                        <tr>
                            <th>Ar</th>
                            <th>Nya</th>
                            <th>Totalt</th>
                            <th>Andel</th>
                        </tr>
                    </thead>
                    <tbody>
                        <?php foreach ($reportData['trend'] as $t): ?>
                        <tr>
                            <td><?= $t['year'] ?></td>
                            <td><strong><?= number_format($t['rookie_count']) ?></strong></td>
                            <td><?= number_format($t['total_riders']) ?></td>
                            <td><?= $t['rookie_percentage'] ?>%</td>
                        </tr>
                        <?php endforeach; ?>
                    </tbody>
                </table>
            </div>
        </div>
    </div>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <script>
    document.addEventListener('DOMContentLoaded', function() {
        const ctx = document.getElementById('rookieTrendChart');
        if (ctx) {
            new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: <?= json_encode(array_column($reportData['trend'], 'year')) ?>,
                    datasets: [{
                        label: 'Nya deltagare',
                        data: <?= json_encode(array_map('intval', array_column($reportData['trend'], 'rookie_count'))) ?>,
                        backgroundColor: 'rgba(55, 212, 214, 0.8)',
                        borderColor: 'rgba(55, 212, 214, 1)',
                        borderWidth: 1
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: { display: false }
                    },
                    scales: {
                        y: {
                            beginAtZero: true,
                            grid: { color: 'rgba(255,255,255,0.1)' }
                        },
                        x: {
                            grid: { display: false }
                        }
                    }
                }
            });
        }
    });
    </script>
    <?php endif; ?>

    <div class="report-section">
        <h3>Aldersfordelning - Nya Deltagare</h3>
        <table class="report-table">
            <thead>
                <tr>
                    <th>Aldersgrupp</th>
                    <th>Antal</th>
                    <th>Andel</th>
                </tr>
            </thead>
            <tbody>
                <?php
                $totalAge = array_sum(array_column($reportData['ages'], 'count')) ?: 1;
                foreach ($reportData['ages'] as $age):
                    $pct = ($age['count'] / $totalAge) * 100;
                ?>
                <tr>
                    <td><?= htmlspecialchars($age['age_group']) ?></td>
                    <td><?= number_format($age['count']) ?></td>
                    <td>
                        <div class="progress-cell">
                            <div class="progress-bar-mini">
                                <div class="progress-fill" style="width: <?= $pct ?>%;"></div>
                            </div>
                            <span><?= round($pct, 1) ?>%</span>
                        </div>
                    </td>
                </tr>
                <?php endforeach; ?>
            </tbody>
        </table>
    </div>

    <div class="report-section">
        <h3>Klasser - Var startar nya deltagare?</h3>
        <table class="report-table">
            <thead>
                <tr>
                    <th>Klass</th>
                    <th>Antal Rookies</th>
                    <th>Andel</th>
                </tr>
            </thead>
            <tbody>
                <?php
                $totalClass = array_sum(array_column($reportData['classes'], 'rookie_count')) ?: 1;
                foreach ($reportData['classes'] as $class):
                    $pct = ($class['rookie_count'] / $totalClass) * 100;
                ?>
                <tr>
                    <td><?= htmlspecialchars($class['class_name']) ?></td>
                    <td><?= number_format($class['rookie_count']) ?></td>
                    <td><?= round($pct, 1) ?>%</td>
                </tr>
                <?php endforeach; ?>
            </tbody>
        </table>
    </div>

    <div class="report-section">
        <h3>Events med flest nya deltagare</h3>
        <table class="report-table">
            <thead>
                <tr>
                    <th>Event</th>
                    <th>Serie</th>
                    <th>Datum</th>
                    <th>Rookies</th>
                    <th>Totalt</th>
                    <th>Andel</th>
                </tr>
            </thead>
            <tbody>
                <?php foreach ($reportData['events'] as $event): ?>
                <tr>
                    <td>
                        <a href="/event/<?= $event['event_id'] ?>" target="_blank">
                            <?= htmlspecialchars($event['event_name']) ?>
                        </a>
                    </td>
                    <td><?= htmlspecialchars($event['series_name'] ?? '-') ?></td>
                    <td><?= date('Y-m-d', strtotime($event['event_date'])) ?></td>
                    <td><strong><?= number_format($event['rookie_count']) ?></strong></td>
                    <td><?= number_format($event['total_participants']) ?></td>
                    <td><?= $event['rookie_percentage'] ?>%</td>
                </tr>
                <?php endforeach; ?>
            </tbody>
        </table>
    </div>

    <div class="report-section">
        <h3>Klubbar med flest nya deltagare</h3>
        <table class="report-table">
            <thead>
                <tr>
                    <th>Klubb</th>
                    <th>Stad</th>
                    <th>Antal Rookies</th>
                </tr>
            </thead>
            <tbody>
                <?php foreach ($reportData['clubs'] as $club): ?>
                <tr>
                    <td>
                        <a href="/club/<?= $club['club_id'] ?>" target="_blank">
                            <?= htmlspecialchars($club['club_name']) ?>
                        </a>
                    </td>
                    <td><?= htmlspecialchars($club['city'] ?? '-') ?></td>
                    <td><strong><?= number_format($club['rookie_count']) ?></strong></td>
                </tr>
                <?php endforeach; ?>
            </tbody>
        </table>
    </div>

    <div class="report-section">
        <h3>Alla Nya Deltagare (<?= number_format(count($reportData['list'])) ?> st)</h3>
        <p style="color: var(--color-text-secondary); margin-bottom: var(--space-md);">
            Klicka pa "Exportera CSV" for att ladda ner listan med profillänkar.
        </p>
        <div class="table-responsive" style="max-height: 500px; overflow-y: auto;">
        <table class="report-table">
            <thead>
                <tr>
                    <th>Namn</th>
                    <th>Alder</th>
                    <th>Klubb</th>
                    <th>Serie</th>
                    <th>Events</th>
                    <th>Poang</th>
                    <th>Basta</th>
                    <th></th>
                </tr>
            </thead>
            <tbody>
                <?php foreach ($reportData['list'] as $rookie): ?>
                <tr>
                    <td>
                        <a href="/rider/<?= $rookie['rider_id'] ?>" target="_blank">
                            <?= htmlspecialchars($rookie['firstname'] . ' ' . $rookie['lastname']) ?>
                        </a>
                    </td>
                    <td><?= $rookie['age'] ?? '-' ?></td>
                    <td><?= htmlspecialchars($rookie['club_name'] ?? '-') ?></td>
                    <td><?= htmlspecialchars($rookie['series_name'] ?? '-') ?></td>
                    <td><?= $rookie['total_events'] ?></td>
                    <td><?= $rookie['total_points'] ?></td>
                    <td><?= $rookie['best_position'] ? '#' . $rookie['best_position'] : '-' ?></td>
                    <td>
                        <a href="/rider/<?= $rookie['rider_id'] ?>" target="_blank" class="btn-icon" title="Visa profil">
                            <i data-lucide="external-link" style="width:16px;height:16px;"></i>
                        </a>
                    </td>
                </tr>
                <?php endforeach; ?>
            </tbody>
        </table>
        </div>
    </div>
    <?php endif; ?>

</div>

<?php endif; ?>

<style>
/* Report Selector */
.report-selector {
    margin-bottom: var(--space-xl);
    padding: var(--space-lg);
    background: var(--color-bg-card);
    border: 1px solid var(--color-border);
    border-radius: var(--radius-md);
}

.report-form {
    display: flex;
    flex-direction: column;
    gap: var(--space-lg);
}

.report-options {
    display: flex;
    flex-wrap: wrap;
    gap: var(--space-sm);
}

.report-option {
    display: flex;
    align-items: center;
    gap: var(--space-sm);
    padding: var(--space-sm) var(--space-md);
    background: var(--color-bg-surface);
    border: 1px solid var(--color-border);
    border-radius: var(--radius-md);
    cursor: pointer;
    transition: all 0.15s ease;
}

.report-option input {
    display: none;
}

.report-option i {
    width: 18px;
    height: 18px;
    color: var(--color-text-muted);
}

.report-option span {
    font-size: var(--text-sm);
    font-weight: var(--weight-medium);
}

.report-option:hover {
    border-color: var(--color-accent);
}

.report-option.active {
    background: var(--color-accent-light);
    border-color: var(--color-accent);
}

.report-option.active i {
    color: var(--color-accent);
}

.report-controls {
    display: flex;
    gap: var(--space-md);
    align-items: center;
}

/* Report Container */
.report-container {
    background: var(--color-bg-card);
    border: 1px solid var(--color-border);
    border-radius: var(--radius-md);
    overflow: hidden;
}

.report-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: var(--space-lg);
    background: var(--color-bg-surface);
    border-bottom: 1px solid var(--color-border);
}

.report-header h2 {
    margin: 0;
    font-size: var(--text-xl);
}

.report-date {
    font-size: var(--text-sm);
    color: var(--color-text-muted);
}

.report-section {
    padding: var(--space-lg);
    border-bottom: 1px solid var(--color-border);
}

.report-section:last-child {
    border-bottom: none;
}

.report-section h3 {
    margin: 0 0 var(--space-md) 0;
    font-size: var(--text-lg);
    color: var(--color-text-secondary);
}

/* KPI Grid */
.kpi-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
    gap: var(--space-md);
}

.kpi-item {
    text-align: center;
    padding: var(--space-md);
    background: var(--color-bg-surface);
    border-radius: var(--radius-md);
}

.kpi-item--large {
    padding: var(--space-xl);
}

.kpi-value {
    display: block;
    font-size: var(--text-2xl);
    font-weight: var(--weight-bold);
    color: var(--color-accent);
}

.kpi-item--large .kpi-value {
    font-size: var(--text-4xl);
}

.kpi-label {
    display: block;
    font-size: var(--text-sm);
    color: var(--color-text-secondary);
    margin-top: var(--space-xs);
}

/* Retention Breakdown */
.retention-breakdown {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: var(--space-md);
    margin-top: var(--space-lg);
}

.retention-stat {
    display: flex;
    align-items: center;
    gap: var(--space-md);
    padding: var(--space-md);
    background: var(--color-bg-surface);
    border-radius: var(--radius-md);
}

.retention-stat i {
    width: 32px;
    height: 32px;
    color: var(--color-accent);
}

.retention-value {
    display: block;
    font-size: var(--text-xl);
    font-weight: var(--weight-bold);
}

.retention-label {
    display: block;
    font-size: var(--text-sm);
    color: var(--color-text-secondary);
}

/* Report Table */
.report-table {
    width: 100%;
    border-collapse: collapse;
}

.report-table th,
.report-table td {
    padding: var(--space-sm) var(--space-md);
    text-align: left;
    border-bottom: 1px solid var(--color-border);
}

.report-table th {
    background: var(--color-bg-surface);
    font-weight: var(--weight-semibold);
    font-size: var(--text-sm);
    color: var(--color-text-secondary);
}

.report-table tbody tr:hover {
    background: var(--color-bg-hover);
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

/* Responsive */
@media (max-width: 767px) {
    .report-selector {
        margin-left: calc(-1 * var(--container-padding, 16px));
        margin-right: calc(-1 * var(--container-padding, 16px));
        border-radius: 0;
        border-left: none;
        border-right: none;
    }

    .report-container {
        margin-left: calc(-1 * var(--container-padding, 16px));
        margin-right: calc(-1 * var(--container-padding, 16px));
        border-radius: 0;
        border-left: none;
        border-right: none;
    }

    .report-options {
        flex-direction: column;
    }

    .report-controls {
        flex-direction: column;
        width: 100%;
    }

    .report-controls select,
    .report-controls a {
        width: 100%;
    }

    .kpi-grid {
        grid-template-columns: repeat(2, 1fr);
    }

    .report-table {
        font-size: var(--text-sm);
    }

    .report-table th,
    .report-table td {
        padding: var(--space-xs) var(--space-sm);
    }
}
</style>

<?php include __DIR__ . '/components/unified-layout-footer.php'; ?>
