<?php
/**
 * Admin Results - V3 Design System
 * Promotors can only see results for their own events
 */
require_once __DIR__ . '/../config.php';
require_admin();

global $pdo;
$db = getDB();

// Check if user is a promotor (limited access)
$isPromotorOnly = isRole('promotor');
$promotorEventIds = [];

if ($isPromotorOnly) {
    // Get promotor's events
    $promotorEvents = getPromotorEvents();
    $promotorEventIds = array_column($promotorEvents, 'id');
}

// Get filter parameters
$filterSeries = isset($_GET['series_id']) && is_numeric($_GET['series_id']) ? intval($_GET['series_id']) : null;
$filterYear = isset($_GET['year']) && is_numeric($_GET['year']) ? intval($_GET['year']) : null;

// Build WHERE clause
$where = [];
$params = [];

// Promotor filter - only show their events
if ($isPromotorOnly) {
    if (!empty($promotorEventIds)) {
        $placeholders = implode(',', array_fill(0, count($promotorEventIds), '?'));
        $where[] = "e.id IN ($placeholders)";
        $params = array_merge($params, $promotorEventIds);
    } else {
        // Promotor with no events - show nothing
        $where[] = "1=0";
    }
}

if ($filterSeries) {
    $where[] = "e.series_id = ?";
    $params[] = $filterSeries;
}

if ($filterYear) {
    $where[] = "YEAR(e.date) = ?";
    $params[] = $filterYear;
}

$whereClause = !empty($where) ? 'WHERE ' . implode(' AND ', $where) : '';

// Get all events with result counts
$sql = "SELECT
    e.id, e.name, e.advent_id, e.date, e.location, e.status,
    s.name as series_name,
    s.id as series_id,
    COUNT(DISTINCT r.id) as result_count,
    COUNT(DISTINCT r.category_id) as category_count,
    COUNT(DISTINCT CASE WHEN r.status = 'finished' THEN r.id END) as finished_count,
    COUNT(DISTINCT CASE WHEN r.status = 'dnf' THEN r.id END) as dnf_count,
    COUNT(DISTINCT CASE WHEN r.status = 'dns' THEN r.id END) as dns_count
FROM events e
LEFT JOIN results r ON e.id = r.event_id
LEFT JOIN series s ON e.series_id = s.id
{$whereClause}
GROUP BY e.id
ORDER BY e.date DESC";

try {
    $events = $db->getAll($sql, $params);
} catch (Exception $e) {
    $events = [];
    $error = $e->getMessage();
}

// Get series for filter buttons (limited for promotors)
if ($isPromotorOnly && !empty($promotorEventIds)) {
    $placeholders = implode(',', array_fill(0, count($promotorEventIds), '?'));
    $allSeries = $db->getAll("SELECT DISTINCT s.id, s.name FROM series s INNER JOIN events e ON e.series_id = s.id WHERE e.id IN ($placeholders) ORDER BY s.name", $promotorEventIds);
} elseif ($isPromotorOnly) {
    $allSeries = [];
} else {
    $allSeries = $db->getAll("SELECT id, name FROM series WHERE active = 1 ORDER BY name");
}

// Get all years from events
$allYears = $db->getAll("SELECT DISTINCT YEAR(date) as year FROM events WHERE date IS NOT NULL ORDER BY year DESC");

// Page config
$page_title = 'Resultat';
$breadcrumbs = [
    ['label' => 'Events', 'url' => '/admin/events'],
    ['label' => 'Resultat']
];

// Promotors don't get import button
if ($isPromotorOnly) {
    $page_actions = '';
} else {
    $page_actions = '<a href="/admin/import-results.php" class="btn-admin btn-admin-primary">
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="17 8 12 3 7 8"/><line x1="12" x2="12" y1="3" y2="15"/></svg>
        Importera Resultat
    </a>';
}

// Include unified layout (uses same layout as public site)
include __DIR__ . '/components/unified-layout.php';
?>

<?php if (isset($_SESSION['recalc_message'])): ?>
    <div class="alert alert-<?= h($_SESSION['recalc_type'] ?? 'info') ?> mb-lg">
        <i data-lucide="<?= ($_SESSION['recalc_type'] ?? 'info') === 'success' ? 'check-circle' : 'alert-circle' ?>"></i>
        <?= h($_SESSION['recalc_message']) ?>
    </div>
    <?php
    unset($_SESSION['recalc_message']);
    unset($_SESSION['recalc_type']);
    ?>
<?php endif; ?>

<?php if (isset($error)): ?>
    <div class="alert alert-error mb-lg">
        <strong>Fel:</strong> <?= htmlspecialchars($error) ?>
    </div>
<?php endif; ?>

<!-- Filter Section -->
<div class="admin-card">
    <div class="admin-card-body">
        <form method="GET" class="admin-form-row">
            <!-- Year Filter -->
            <div class="admin-form-group" style="margin-bottom: 0;">
                <label for="year-filter" class="admin-form-label">År</label>
                <select id="year-filter" name="year" class="admin-form-select" onchange="this.form.submit()">
                    <option value="">Alla år</option>
                    <?php foreach ($allYears as $yearRow): ?>
                        <option value="<?= $yearRow['year'] ?>" <?= $filterYear == $yearRow['year'] ? 'selected' : '' ?>>
                            <?= $yearRow['year'] ?>
                        </option>
                    <?php endforeach; ?>
                </select>
            </div>

            <!-- Series Filter -->
            <div class="admin-form-group" style="margin-bottom: 0;">
                <label for="series-filter" class="admin-form-label">Serie<?= $filterYear ? ' (' . $filterYear . ')' : '' ?></label>
                <select id="series-filter" name="series_id" class="admin-form-select" onchange="this.form.submit()">
                    <option value="">Alla serier</option>
                    <?php foreach ($allSeries as $series): ?>
                        <option value="<?= $series['id'] ?>" <?= $filterSeries == $series['id'] ? 'selected' : '' ?>>
                            <?= htmlspecialchars($series['name']) ?>
                        </option>
                    <?php endforeach; ?>
                </select>
            </div>
        </form>

        <!-- Active Filters Info -->
        <?php if ($filterSeries || $filterYear): ?>
            <div class="mt-md" style="padding-top: var(--space-md); border-top: 1px solid var(--color-border);">
                <div class="flex items-center gap-sm flex-wrap">
                    <span class="text-sm text-secondary">Visar:</span>
                    <?php if ($filterSeries): ?>
                        <span class="admin-badge admin-badge-info">
                            <?php
                            $seriesName = array_filter($allSeries, function($s) use ($filterSeries) {
                                return $s['id'] == $filterSeries;
                            });
                            echo $seriesName ? htmlspecialchars(reset($seriesName)['name']) : 'Serie #' . $filterSeries;
                            ?>
                        </span>
                    <?php endif; ?>
                    <?php if ($filterYear): ?>
                        <span class="admin-badge admin-badge-warning"><?= $filterYear ?></span>
                    <?php endif; ?>
                    <a href="/admin/results.php" class="btn-admin btn-admin-secondary btn-admin-sm">
                        Visa alla
                    </a>
                </div>
            </div>
        <?php endif; ?>
    </div>
</div>

<?php if (empty($events)): ?>
    <div class="admin-card">
        <div class="admin-card-body">
            <div class="admin-empty-state">
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M8 2v4"/><path d="M16 2v4"/><rect width="18" height="18" x="3" y="4" rx="2"/><path d="M3 10h18"/></svg>
                <h3>Inga event hittades</h3>
                <p>Skapa ett event först eller ändra filtren.</p>
                <a href="/admin/events/create" class="btn-admin btn-admin-primary">Skapa Event</a>
            </div>
        </div>
    </div>
<?php else: ?>
    <!-- Events Table -->
    <div class="admin-card">
        <div class="admin-table-container">
            <table class="admin-table">
                <thead>
                    <tr>
                        <th>Datum</th>
                        <th>Event</th>
                        <th>Plats</th>
                        <th>Serie</th>
                        <th class="text-center" title="Totalt antal deltagare. Siffror inom parentes: (DNF/DNS) - DNF=Bröt, DNS=Startade ej">
                                        Deltagare
                                        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="14" height="14" style="vertical-align: middle; opacity: 0.5; cursor: help;"><circle cx="12" cy="12" r="10"/><path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3"/><path d="M12 17h.01"/></svg>
                                    </th>
                        <th class="text-right">Åtgärder</th>
                    </tr>
                </thead>
                <tbody>
                    <?php foreach ($events as $event): ?>
                        <tr>
                            <td style="white-space: nowrap;">
                                <?= date('Y-m-d', strtotime($event['date'])) ?>
                            </td>
                            <td>
                                <strong><?= h($event['name']) ?></strong>
                                <?php if ($event['advent_id']): ?>
                                    <span style="color: var(--color-text-secondary); font-size: var(--text-sm);">#<?= h($event['advent_id']) ?></span>
                                <?php endif; ?>
                            </td>
                            <td><?= h($event['location'] ?? '-') ?></td>
                            <td><?= h($event['series_name'] ?? '-') ?></td>
                            <td class="text-center">
                                <span class="admin-badge admin-badge-<?= $event['result_count'] > 0 ? 'success' : 'info' ?>" title="Totalt antal resultat">
                                    <?= $event['result_count'] ?>
                                </span>
                                <?php if ($event['dnf_count'] > 0 || $event['dns_count'] > 0): ?>
                                    <span style="color: var(--color-text-secondary); font-size: var(--text-xs); cursor: help;" title="<?= $event['dnf_count'] ?> bröt (DNF), <?= $event['dns_count'] ?> startade ej (DNS)">
                                        (<?= $event['dnf_count'] ?>/<?= $event['dns_count'] ?>)
                                    </span>
                                <?php endif; ?>
                            </td>
                            <td class="table-actions">
                                <a href="/event/<?= $event['id'] ?>" class="btn-admin btn-admin-secondary btn-admin-sm" title="Visa">
                                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M2 12s3-7 10-7 10 7 10 7-3 7-10 7-10-7-10-7Z"/><circle cx="12" cy="12" r="3"/></svg>
                                </a>
                                <?php if ($event['result_count'] > 0): ?>
                                    <a href="/admin/edit-results.php?event_id=<?= $event['id'] ?>" class="btn-admin btn-admin-primary btn-admin-sm" title="Editera">
                                        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M17 3a2.85 2.83 0 1 1 4 4L7.5 20.5 2 22l1.5-5.5Z"/><path d="m15 5 4 4"/></svg>
                                    </a>
                                <?php else: ?>
                                    <a href="/admin/import-results.php" class="btn-admin btn-admin-secondary btn-admin-sm" title="Importera">
                                        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="17 8 12 3 7 8"/><line x1="12" x2="12" y1="3" y2="15"/></svg>
                                    </a>
                                <?php endif; ?>
                            </td>
                        </tr>
                    <?php endforeach; ?>
                </tbody>
            </table>
        </div>
    </div>
<?php endif; ?>

<?php include __DIR__ . '/components/unified-layout-footer.php'; ?>
