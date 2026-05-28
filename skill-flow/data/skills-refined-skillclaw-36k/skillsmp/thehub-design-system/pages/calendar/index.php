<?php
/**
 * TheHUB V1.0 - Kalender
 * Visar kommande event med filter (månad, serie, format)
 */

// Define page type for sponsor placements
if (!defined('HUB_PAGE_TYPE')) {
    define('HUB_PAGE_TYPE', 'calendar');
}

$pdo = hub_db();
$currentUser = hub_current_user();

// Filters
$filterSeries = $_GET['series'] ?? '';
$filterFormat = $_GET['format'] ?? '';

// Get upcoming events with series colors and logo from brand
$sql = "
    SELECT e.*,
           e.is_championship,
           s.name as series_name,
           s.id as series_id,
           sb.logo as series_logo,
           sb.accent_color as series_accent,
           v.name as venue_name,
           v.city as venue_city,
           COUNT(DISTINCT er.id) as registration_count
    FROM events e
    LEFT JOIN series s ON e.series_id = s.id
    LEFT JOIN series_brands sb ON s.brand_id = sb.id
    LEFT JOIN venues v ON e.venue_id = v.id
    LEFT JOIN event_registrations er ON e.id = er.event_id AND er.status != 'cancelled'
    WHERE e.date >= CURDATE() AND e.active = 1
";
$params = [];

if ($filterSeries) {
    $sql .= " AND e.series_id = ?";
    $params[] = $filterSeries;
}

if ($filterFormat) {
    $sql .= " AND e.discipline = ?";
    $params[] = $filterFormat;
}

$sql .= " GROUP BY e.id ORDER BY e.date ASC LIMIT 50";

$events = [];
$seriesList = [];
$formatList = [];

try {
    $stmt = $pdo->prepare($sql);
    $stmt->execute($params);
    $events = $stmt->fetchAll(PDO::FETCH_ASSOC);

    // Get series for filter - only series that have upcoming events (color from brand)
    $seriesStmt = $pdo->query("
        SELECT DISTINCT s.id, s.name, sb.accent_color
        FROM series s
        LEFT JOIN series_brands sb ON s.brand_id = sb.id
        INNER JOIN events e ON s.id = e.series_id
        WHERE e.date >= CURDATE() AND e.active = 1 AND s.active = 1
        ORDER BY s.name
    ");
    $seriesList = $seriesStmt->fetchAll(PDO::FETCH_ASSOC);

    // Get formats for filter - only formats that have upcoming events
    $formatStmt = $pdo->query("
        SELECT DISTINCT discipline
        FROM events
        WHERE date >= CURDATE() AND active = 1 AND discipline IS NOT NULL AND discipline != ''
        ORDER BY discipline
    ");
    $formatList = $formatStmt->fetchAll(PDO::FETCH_ASSOC);
} catch (PDOException $e) {
    // Database error - show empty state
    error_log("Calendar index database error: " . $e->getMessage());
}

// Format display names
$formatNames = [
    'ENDURO' => 'Enduro',
    'DH' => 'Downhill',
    'XC' => 'XC',
    'XCO' => 'XCO',
    'XCM' => 'XCM',
    'DUAL_SLALOM' => 'Dual Slalom',
    'PUMPTRACK' => 'Pumptrack',
    'GRAVEL' => 'Gravel',
    'E-MTB' => 'E-MTB'
];

// Group events by month
$eventsByMonth = [];
foreach ($events as $event) {
    $month = date('Y-m', strtotime($event['date']));
    $eventsByMonth[$month][] = $event;
}

// Helper function for deadline text
if (!function_exists('getDeadlineInfo')) {
    function getDeadlineInfo($deadline) {
        if (empty($deadline)) {
            return null;
        }

        $now = new DateTime();
        $deadlineDate = new DateTime($deadline);
        $diff = $now->diff($deadlineDate);

        if ($deadlineDate < $now) {
            return ['text' => 'Stängd', 'class' => 'closed', 'days' => -1];
        }

        $days = $diff->days;
        if ($days == 0) {
            return ['text' => 'Sista dagen!', 'class' => 'urgent', 'days' => 0];
        } elseif ($days == 1) {
            return ['text' => '1 dag', 'class' => 'soon', 'days' => 1];
        } elseif ($days <= 7) {
            return ['text' => $days . ' dagar', 'class' => 'soon', 'days' => $days];
        } else {
            return ['text' => $days . ' dagar', 'class' => '', 'days' => $days];
        }
    }
}
?>

<div class="page-header">
    <h1 class="page-title">
        <i data-lucide="calendar" class="page-icon"></i>
        Kalender
    </h1>
    <p class="page-subtitle">Kommande tävlingar och event</p>
</div>

<!-- Global Sponsor: Header Banner -->
<?= render_global_sponsors('calendar', 'header_banner', '') ?>

<!-- Global Sponsor: Content Top -->
<?= render_global_sponsors('calendar', 'content_top', '') ?>

<!-- Filters -->
<div class="filter-bar">
    <div class="filter-group">
        <label for="filter-series" class="filter-label">Serie</label>
        <select id="filter-series" class="filter-select" onchange="applyFilters()">
            <option value="">Alla serier</option>
            <?php foreach ($seriesList as $series): ?>
                <option value="<?= $series['id'] ?>" <?= $filterSeries == $series['id'] ? 'selected' : '' ?>>
                    <?= htmlspecialchars($series['name']) ?>
                </option>
            <?php endforeach; ?>
        </select>
    </div>
    <div class="filter-group">
        <label for="filter-format" class="filter-label">Format</label>
        <select id="filter-format" class="filter-select" onchange="applyFilters()">
            <option value="">Alla format</option>
            <?php foreach ($formatList as $format): ?>
                <option value="<?= htmlspecialchars($format['discipline']) ?>" <?= $filterFormat == $format['discipline'] ? 'selected' : '' ?>>
                    <?= htmlspecialchars($formatNames[$format['discipline']] ?? $format['discipline']) ?>
                </option>
            <?php endforeach; ?>
        </select>
    </div>
</div>

<!-- Events List -->
<div class="calendar-events">
    <?php if (empty($events)): ?>
        <div class="empty-state">
            <div class="empty-icon"><i data-lucide="calendar-x"></i></div>
            <h3>Inga kommande event</h3>
            <p>Det finns inga schemalagda tävlingar just nu.</p>
        </div>
    <?php else: ?>
        <?php foreach ($eventsByMonth as $month => $monthEvents): ?>
            <div class="calendar-month-section">
                <div class="calendar-month-divider">
                    <span class="calendar-month-label"><?= hub_format_month_year($month . '-01') ?></span>
                    <span class="calendar-month-line"></span>
                    <span class="calendar-month-count"><?= count($monthEvents) ?> event</span>
                </div>
                <div class="event-list">
                    <?php foreach ($monthEvents as $event): ?>
                        <?php
                        $eventDate = strtotime($event['date']);
                        $dateFormatted = date('j', $eventDate) . ' ' . hub_month_short($eventDate);
                        $dayName = hub_day_short($eventDate);
                        $deadlineInfo = getDeadlineInfo($event['registration_deadline']);
                        $location = $event['venue_city'] ?: $event['location'];
                        $accentColor = $event['series_accent'] ?: '#61CE70';
                        $seriesLogo = $event['series_logo'] ?? '';
                        ?>
                        <a href="/calendar/<?= $event['id'] ?>" class="event-row" style="--event-accent: <?= htmlspecialchars($accentColor) ?>">
                            <div class="event-accent-bar"></div>

                            <?php if ($seriesLogo): ?>
                            <div class="event-logo">
                                <img src="<?= htmlspecialchars($seriesLogo) ?>" alt="<?= htmlspecialchars($event['series_name']) ?>">
                            </div>
                            <?php else: ?>
                            <div class="event-logo event-logo-placeholder">
                                <i data-lucide="calendar"></i>
                            </div>
                            <?php endif; ?>

                            <span class="event-date-inline">
                                <strong><?= $dateFormatted ?></strong>
                                <span class="event-day-name"><?= $dayName ?></span>
                            </span>

                            <?php if ($event['series_name']): ?>
                            <span class="event-series-badge"><?= htmlspecialchars($event['series_name']) ?></span>
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

                            <?php if ($event['registration_count'] > 0): ?>
                            <span class="event-registrations"><?= $event['registration_count'] ?> anmälda</span>
                            <?php endif; ?>

                            <?php if ($deadlineInfo && $deadlineInfo['days'] >= 0): ?>
                            <span class="event-deadline <?= $deadlineInfo['class'] ?>">
                                <i data-lucide="clock"></i>
                                <span class="deadline-label">Anmälan stänger:</span>
                                <?= $deadlineInfo['text'] ?>
                            </span>
                            <?php endif; ?>

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
<?= render_global_sponsors('calendar', 'content_bottom', 'Tack till våra partners') ?>

<script>
function applyFilters() {
    const series = document.getElementById('filter-series').value;
    const format = document.getElementById('filter-format').value;
    const params = new URLSearchParams();
    if (series) params.set('series', series);
    if (format) params.set('format', format);
    window.location.href = '/calendar' + (params.toString() ? '?' + params : '');
}
</script>
