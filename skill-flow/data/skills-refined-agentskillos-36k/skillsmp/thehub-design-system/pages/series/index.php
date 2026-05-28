<?php
/**
 * TheHUB V1.0 - Series List
 * Redesigned to match results page layout with row-based cards
 */

// Prevent direct access
if (!defined('HUB_ROOT')) {
    header('Location: /series');
    exit;
}

// Define page type for sponsor placements
define('HUB_PAGE_TYPE', 'series_list');

$pdo = hub_db();

// Check if series_events table exists
$useSeriesEvents = false;
try {
    $check = $pdo->query("SHOW TABLES LIKE 'series_events'");
    $useSeriesEvents = $check->rowCount() > 0;
} catch (Exception $e) {
    $useSeriesEvents = false;
}

// Check if historical_data_verified column exists
$hasVerifiedColumn = false;
try {
    $check = $pdo->query("SHOW COLUMNS FROM series LIKE 'historical_data_verified'");
    $hasVerifiedColumn = $check->rowCount() > 0;
} catch (Exception $e) {
    $hasVerifiedColumn = false;
}

// Get filter parameters
$filterSeriesName = isset($_GET['series']) ? trim($_GET['series']) : null;
$currentYear = (int)date('Y');

// Check if user has set any filter params
// Default: show ALL years (like results page)
if (isset($_GET['year']) && $_GET['year'] !== 'all' && is_numeric($_GET['year'])) {
    $filterYear = intval($_GET['year']);
} else {
    $filterYear = null; // Show all years by default
}

// Get unique series names for dropdown
$allSeriesStmt = $pdo->query("
    SELECT DISTINCT name FROM series
    WHERE status IN ('active', 'completed')
    ORDER BY name ASC
");
$allSeriesNames = $allSeriesStmt->fetchAll(PDO::FETCH_COLUMN);

// Get available years
$yearStmt = $pdo->query("
    SELECT DISTINCT year FROM series
    WHERE status IN ('active', 'completed') AND year IS NOT NULL
    ORDER BY year DESC
");
$availableYears = $yearStmt->fetchAll(PDO::FETCH_COLUMN);

// Build WHERE clause
$where = ["s.status IN ('active', 'completed')"];
$params = [];

if ($filterSeriesName) {
    $where[] = "s.name = ?";
    $params[] = $filterSeriesName;
}

if ($filterYear) {
    $where[] = "s.year = ?";
    $params[] = $filterYear;
}

$whereClause = 'WHERE ' . implode(' AND ', $where);

// Get series for display with brand info
$verifiedCol = $hasVerifiedColumn ? 's.historical_data_verified,' : '0 as historical_data_verified,';

if ($useSeriesEvents) {
    $sql = "
        SELECT s.id, s.name, s.description, s.year, s.status, s.logo, s.start_date, s.end_date,
               {$verifiedCol}
               sb.name as brand_name, sb.logo as brand_logo, sb.accent_color,
               COUNT(DISTINCT se.event_id) as event_count,
               (SELECT COUNT(DISTINCT r.cyclist_id)
                FROM results r
                INNER JOIN series_events se2 ON r.event_id = se2.event_id
                WHERE se2.series_id = s.id) as participant_count
        FROM series s
        LEFT JOIN series_brands sb ON s.brand_id = sb.id
        LEFT JOIN series_events se ON s.id = se.series_id
        {$whereClause}
        GROUP BY s.id
        ORDER BY s.year DESC, s.name ASC
    ";
} else {
    $sql = "
        SELECT s.id, s.name, s.description, s.year, s.status, s.logo, s.start_date, s.end_date,
               {$verifiedCol}
               sb.name as brand_name, sb.logo as brand_logo, sb.accent_color,
               COUNT(DISTINCT e.id) as event_count,
               (SELECT COUNT(DISTINCT r.cyclist_id)
                FROM results r
                INNER JOIN events e2 ON r.event_id = e2.id
                WHERE e2.series_id = s.id) as participant_count
        FROM series s
        LEFT JOIN series_brands sb ON s.brand_id = sb.id
        LEFT JOIN events e ON s.id = e.series_id
        {$whereClause}
        GROUP BY s.id
        ORDER BY s.year DESC, s.name ASC
    ";
}
$stmt = $pdo->prepare($sql);
$stmt->execute($params);
$seriesList = $stmt->fetchAll(PDO::FETCH_ASSOC);

// Group series by year
$seriesByYear = [];
foreach ($seriesList as $series) {
    $year = $series['year'] ?: 'Okänt';
    $seriesByYear[$year][] = $series;
}
krsort($seriesByYear);

$totalSeries = count($seriesList);

// Page title - always "Serier" unless filtered to specific series
$pageTitle = 'Serier';
if ($filterSeriesName && !empty($seriesList)) {
    $pageTitle = $seriesList[0]['name'];
}
?>

<link rel="stylesheet" href="/assets/css/pages/series-index.css?v=<?= filemtime(__DIR__ . '/../../assets/css/pages/series-index.css') ?>">

<div class="page-header">
    <h1 class="page-title">
        <i data-lucide="award" class="page-icon"></i>
        <?= htmlspecialchars($pageTitle) ?>
    </h1>
    <p class="page-subtitle">Alla tävlingsserier</p>
</div>

<!-- Global Sponsor: Header Banner -->
<?= render_global_sponsors('series_list', 'header_banner', '') ?>

<!-- Global Sponsor: Content Top -->
<?= render_global_sponsors('series_list', 'content_top', '') ?>

<!-- Filters -->
<div class="filter-bar">
    <div class="filter-group">
        <label for="filter-series" class="filter-label">Serie</label>
        <select id="filter-series" class="filter-select" onchange="applyFilters()">
            <option value="">Alla serier</option>
            <?php foreach ($allSeriesNames as $name): ?>
            <option value="<?= htmlspecialchars($name) ?>" <?= $filterSeriesName === $name ? 'selected' : '' ?>>
                <?= htmlspecialchars($name) ?>
            </option>
            <?php endforeach; ?>
        </select>
    </div>
    <div class="filter-group">
        <label for="filter-year" class="filter-label">År</label>
        <select id="filter-year" class="filter-select" onchange="applyFilters()">
            <option value="">Alla år</option>
            <?php foreach ($availableYears as $year): ?>
            <option value="<?= $year ?>" <?= $filterYear == $year ? 'selected' : '' ?>>
                <?= $year ?>
            </option>
            <?php endforeach; ?>
        </select>
    </div>
</div>

<?php if (empty($seriesList)): ?>
    <div class="empty-state">
        <i data-lucide="trophy" class="icon-xl text-muted mb-md"></i>
        <h2>Inga serier hittades</h2>
        <p>Prova ett annat filter.</p>
    </div>
<?php else: ?>
    <div class="series-list-container">
        <?php foreach ($seriesByYear as $year => $yearSeries):
            // Check if any series in this year is unverified (for years <= 2024)
            $hasUnverifiedSeries = false;
            if (is_numeric($year) && $year <= 2024) {
                foreach ($yearSeries as $ys) {
                    if (empty($ys['historical_data_verified'])) {
                        $hasUnverifiedSeries = true;
                        break;
                    }
                }
            }
        ?>
            <div class="series-year-section">
                <div class="series-year-divider">
                    <span class="series-year-label"><?= $year ?></span>
                    <span class="series-year-line"></span>
                    <span class="series-year-count"><?= count($yearSeries) ?> serier</span>
                </div>
                <?php if ($hasUnverifiedSeries): ?>
                <div class="series-historical-warning">
                    <i data-lucide="alert-triangle"></i>
                    <span>Serietabellerna för äldre serier är under arbete. Dessa kräver en del manuellt arbete för att bli korrekta och arbete pågår.</span>
                </div>
                <?php endif; ?>
                <div class="series-list">
                    <?php foreach ($yearSeries as $s):
                        $accentColor = $s['accent_color'] ?: '#61CE70';
                        $logo = $s['brand_logo'] ?: $s['logo'];
                        $statusClass = $s['status'] === 'active' ? 'status-active' : 'status-completed';
                        $statusText = $s['status'] === 'active' ? 'Pågår' : 'Avslutad';
                    ?>
                    <a href="/series/<?= $s['id'] ?>" class="series-row" style="--series-accent: <?= htmlspecialchars($accentColor) ?>">
                        <div class="series-accent-bar"></div>

                        <?php if ($logo): ?>
                        <div class="series-logo">
                            <img src="<?= htmlspecialchars($logo) ?>" alt="<?= htmlspecialchars($s['name']) ?>">
                        </div>
                        <?php else: ?>
                        <div class="series-logo series-logo-placeholder">
                            <i data-lucide="trophy"></i>
                        </div>
                        <?php endif; ?>

                        <h3 class="series-title"><?= htmlspecialchars($s['name']) ?></h3>

                        <span class="series-status <?= $statusClass ?>"><?= $statusText ?></span>

                        <div class="series-stats">
                            <span class="series-stat-inline"><?= $s['event_count'] ?> tävlingar</span>
                            <span class="series-stat-sep">|</span>
                            <span class="series-stat-inline"><?= $s['participant_count'] ?: 0 ?> deltagare</span>
                        </div>

                        <div class="series-arrow">
                            <i data-lucide="chevron-right"></i>
                        </div>
                    </a>
                    <?php endforeach; ?>
                </div>
            </div>
        <?php endforeach; ?>
    </div>
<?php endif; ?>

<!-- Global Sponsor: Content Bottom -->
<?= render_global_sponsors('series_list', 'content_bottom', 'Tack till våra partners') ?>

<script>
function applyFilters() {
    const series = document.getElementById('filter-series').value;
    const year = document.getElementById('filter-year').value;
    const params = new URLSearchParams();
    if (series) params.set('series', series);
    if (year) params.set('year', year);
    window.location.href = '/series' + (params.toString() ? '?' + params : '');
}
</script>
