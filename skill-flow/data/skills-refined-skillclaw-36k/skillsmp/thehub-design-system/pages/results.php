<?php
/**
 * V1.0 Results Page - Shows events with results
 * Matching calendar page design with brand colors
 */

// Define page type for sponsor placements
if (!defined('HUB_PAGE_TYPE')) {
    define('HUB_PAGE_TYPE', 'results');
}

$pdo = hub_db();

// Get filter parameters
$filterBrand = isset($_GET['brand']) && is_numeric($_GET['brand']) ? intval($_GET['brand']) : null;
$filterYear = isset($_GET['year']) && is_numeric($_GET['year']) ? intval($_GET['year']) : null;

try {
    // Get years that have results (for filter dropdown)
    $yearsStmt = $pdo->query("
        SELECT DISTINCT YEAR(e.date) as year
        FROM events e
        INNER JOIN results r ON e.id = r.event_id
        WHERE e.date IS NOT NULL
        ORDER BY year DESC
    ");
    $yearsList = $yearsStmt->fetchAll(PDO::FETCH_COLUMN);

    // Get brands for filter - only brands that have results
    $brandsStmt = $pdo->query("
        SELECT DISTINCT sb.id, sb.name, sb.accent_color
        FROM series_brands sb
        INNER JOIN series s ON s.brand_id = sb.id
        INNER JOIN events e ON s.id = e.series_id
        INNER JOIN results r ON e.id = r.event_id
        WHERE sb.active = 1
        ORDER BY sb.name
    ");
    $brandsList = $brandsStmt->fetchAll(PDO::FETCH_ASSOC);

    // Get events with results, including brand colors and logo
    $sql = "
        SELECT e.id, e.name, e.date, e.location, e.is_championship,
               s.id as series_id, s.name as series_name,
               sb.id as brand_id, sb.name as brand_name,
               sb.logo as series_logo,
               sb.accent_color as series_accent,
               v.name as venue_name, v.city as venue_city,
               COUNT(DISTINCT r.id) as result_count,
               COUNT(DISTINCT r.cyclist_id) as rider_count
        FROM events e
        LEFT JOIN series s ON e.series_id = s.id
        LEFT JOIN series_brands sb ON s.brand_id = sb.id
        LEFT JOIN venues v ON e.venue_id = v.id
        INNER JOIN results r ON e.id = r.event_id
        WHERE 1=1
    ";
    $params = [];

    if ($filterBrand) {
        $sql .= " AND s.brand_id = ?";
        $params[] = $filterBrand;
    }

    if ($filterYear) {
        $sql .= " AND YEAR(e.date) = ?";
        $params[] = $filterYear;
    }

    $sql .= " GROUP BY e.id ORDER BY e.date DESC";

    $stmt = $pdo->prepare($sql);
    $stmt->execute($params);
    $events = $stmt->fetchAll(PDO::FETCH_ASSOC);

    // Group events by year (descending)
    $eventsByYear = [];
    foreach ($events as $event) {
        $year = $event['date'] ? date('Y', strtotime($event['date'])) : 'Okänt';
        $eventsByYear[$year][] = $event;
    }
    // Sort years descending
    krsort($eventsByYear);

    $totalEvents = count($events);

} catch (Exception $e) {
    $events = [];
    $brandsList = [];
    $yearsList = [];
    $eventsByYear = [];
    $totalEvents = 0;
    $error = $e->getMessage();
}
?>

<div class="page-header">
    <h1 class="page-title">
        <i data-lucide="trophy" class="page-icon"></i>
        Resultat
    </h1>
    <p class="page-subtitle"><?= $totalEvents ?> tävlingar med publicerade resultat</p>
</div>

<!-- Global Sponsor: Header Banner -->
<?= render_global_sponsors('results', 'header_banner', '') ?>

<!-- Global Sponsor: Content Top -->
<?= render_global_sponsors('results', 'content_top', '') ?>

<!-- Filters -->
<div class="filter-bar">
    <div class="filter-group">
        <label for="filter-series" class="filter-label">Serie</label>
        <select id="filter-series" class="filter-select" onchange="applyFilters()">
            <option value="">Alla serier</option>
            <?php foreach ($brandsList as $brand): ?>
                <option value="<?= $brand['id'] ?>" <?= $filterBrand == $brand['id'] ? 'selected' : '' ?>>
                    <?= htmlspecialchars($brand['name']) ?>
                </option>
            <?php endforeach; ?>
        </select>
    </div>
    <div class="filter-group">
        <label for="filter-year" class="filter-label">År</label>
        <select id="filter-year" class="filter-select" onchange="applyFilters()">
            <option value="">Alla år</option>
            <?php foreach ($yearsList as $year): ?>
                <option value="<?= $year ?>" <?= $filterYear == $year ? 'selected' : '' ?>>
                    <?= $year ?>
                </option>
            <?php endforeach; ?>
        </select>
    </div>
</div>

<link rel="stylesheet" href="/assets/css/pages/results-index.css?v=<?= filemtime(__DIR__ . '/../assets/css/pages/results-index.css') ?>">

<?php if (isset($error)): ?>
<div class="alert alert-error">
    <i data-lucide="alert-circle"></i>
    <?= htmlspecialchars($error) ?>
</div>
<?php endif; ?>

<!-- Events List -->
<div class="results-events">
    <?php if (empty($events)): ?>
        <div class="empty-state">
            <div class="empty-icon"><i data-lucide="trophy"></i></div>
            <h3>Inga resultat hittades</h3>
            <p>Det finns inga publicerade resultat just nu.</p>
        </div>
    <?php else: ?>
        <?php foreach ($eventsByYear as $year => $yearEvents): ?>
            <div class="results-year-section">
                <div class="results-year-divider">
                    <span class="results-year-label"><?= $year ?></span>
                    <span class="results-year-line"></span>
                    <span class="results-year-count"><?= count($yearEvents) ?> event</span>
                </div>
                <div class="event-list">
                    <?php foreach ($yearEvents as $event): ?>
                        <?php
                        $eventDate = $event['date'] ? strtotime($event['date']) : null;
                        $dateFormatted = $eventDate ? date('j', $eventDate) . ' ' . hub_month_short($eventDate) : '-';
                        $location = $event['venue_city'] ?: $event['location'];
                        $accentColor = $event['series_accent'] ?: '#61CE70';
                        $seriesLogo = $event['series_logo'] ?? '';
                        ?>
                        <a href="/event/<?= $event['id'] ?>" class="event-row" style="--event-accent: <?= htmlspecialchars($accentColor) ?>">
                            <div class="event-accent-bar"></div>

                            <?php if ($seriesLogo): ?>
                            <div class="event-logo">
                                <img src="<?= htmlspecialchars($seriesLogo) ?>" alt="<?= htmlspecialchars($event['brand_name']) ?>">
                            </div>
                            <?php else: ?>
                            <div class="event-logo event-logo-placeholder">
                                <i data-lucide="trophy"></i>
                            </div>
                            <?php endif; ?>

                            <span class="event-date-inline"><?= $dateFormatted ?></span>

                            <?php if ($event['brand_name']): ?>
                            <span class="event-series-badge"><?= htmlspecialchars($event['brand_name']) ?></span>
                            <?php endif; ?>

                            <?php if (!empty($event['is_championship'])): ?>
                            <span class="event-sm-badge" title="Svenska Mästerskap">
                                <i data-lucide="medal"></i>
                                SM
                            </span>
                            <?php endif; ?>

                            <h3 class="event-title"><?= htmlspecialchars($event['name']) ?></h3>

                            <?php if ($location): ?>
                            <span class="event-location-inline">
                                <i data-lucide="map-pin"></i>
                                <?= htmlspecialchars($location) ?>
                            </span>
                            <?php endif; ?>

                            <span class="event-riders"><?= $event['rider_count'] ?> deltagare</span>

                            <div class="event-arrow">
                                <i data-lucide="chevron-right"></i>
                            </div>
                        </a>
                    <?php endforeach; ?>
                </div>
            </div>
        <?php endforeach; ?>
    <?php endif; ?>
</div>

<!-- Global Sponsor: Content Bottom -->
<?= render_global_sponsors('results', 'content_bottom', 'Tack till våra partners') ?>

<script>
function applyFilters() {
    const series = document.getElementById('filter-series').value;
    const year = document.getElementById('filter-year').value;
    const params = new URLSearchParams();
    if (series) params.set('brand', series);
    if (year) params.set('year', year);
    window.location.href = '/results' + (params.toString() ? '?' + params : '');
}
</script>
