<?php
/**
 * Admin Elimination - Översikt över Dual Slalom / Elimination events
 */
require_once __DIR__ . '/../config.php';
require_admin();

global $pdo;
$db = getDB();

// Get filter parameters
$filterYear = isset($_GET['year']) && is_numeric($_GET['year']) ? intval($_GET['year']) : date('Y');

// Get all elimination events (events with DUAL_SLALOM format or that have elimination data)
$sql = "SELECT
    e.id, e.name, e.date, e.location, e.discipline, e.status,
    e.elimination_bracket_size, e.elimination_qualifying_runs, e.elimination_has_b_final,
    s.name as series_name,
    COUNT(DISTINCT eq.id) as qualifying_count,
    COUNT(DISTINCT eb.id) as bracket_count,
    COUNT(DISTINCT er.id) as result_count
FROM events e
LEFT JOIN series s ON e.series_id = s.id
LEFT JOIN elimination_qualifying eq ON e.id = eq.event_id
LEFT JOIN elimination_brackets eb ON e.id = eb.event_id
LEFT JOIN elimination_results er ON e.id = er.event_id
WHERE (e.event_format = 'DUAL_SLALOM' OR e.discipline = 'DUAL_SLALOM' OR eq.id IS NOT NULL)
    AND YEAR(e.date) = ?
GROUP BY e.id
ORDER BY e.date DESC";

try {
    $stmt = $pdo->prepare($sql);
    $stmt->execute([$filterYear]);
    $events = $stmt->fetchAll(PDO::FETCH_ASSOC);
} catch (Exception $e) {
    // Tables might not exist yet
    $events = [];

    // Try simpler query
    try {
        $sql2 = "SELECT
            e.id, e.name, e.date, e.location, e.discipline, e.status,
            s.name as series_name,
            0 as qualifying_count,
            0 as bracket_count,
            0 as result_count
        FROM events e
        LEFT JOIN series s ON e.series_id = s.id
        WHERE (e.event_format = 'DUAL_SLALOM' OR e.discipline = 'DUAL_SLALOM')
            AND YEAR(e.date) = ?
        ORDER BY e.date DESC";
        $stmt2 = $pdo->prepare($sql2);
        $stmt2->execute([$filterYear]);
        $events = $stmt2->fetchAll(PDO::FETCH_ASSOC);
    } catch (Exception $e2) {
        $events = [];
    }
}

// Get all years from events
$allYears = $db->getAll("SELECT DISTINCT YEAR(date) as year FROM events WHERE date IS NOT NULL ORDER BY year DESC");

// Page config
$page_title = 'Elimination / Dual Slalom';
$breadcrumbs = [
    ['label' => 'Tävlingar', 'url' => '/admin/events.php'],
    ['label' => 'Elimination']
];
$page_actions = '<a href="/admin/elimination-create.php" class="btn-admin btn-admin-primary">
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 5v14"/><path d="M5 12h14"/></svg>
    Nytt Event
</a>';

include __DIR__ . '/components/unified-layout.php';
?>

<!-- Info Card -->
<div class="admin-card mb-lg">
    <div class="admin-card-body">
        <div class="flex items-center gap-md">
            <div style="padding: var(--space-md); background: var(--color-accent); border-radius: var(--radius-md); color: white;">
                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M8.21 13.89 7 23l5-3 5 3-1.21-9.12"/><path d="M15 7a3 3 0 1 0 0-6 3 3 0 0 0 0 6Z"/><path d="M9 7a3 3 0 1 0 0-6 3 3 0 0 0 0 6Z"/><path d="M15 13a4 4 0 0 0-3-3.87"/><path d="M9 13a4 4 0 0 1 3-3.87"/></svg>
            </div>
            <div>
                <h3 style="margin: 0; font-size: var(--text-lg);">Elimination / Dual Slalom</h3>
                <p style="margin: var(--space-xs) 0 0; color: var(--color-text-secondary);">
                    Hantera bracket-tävlingar med kvalificering och utslagning.
                    Stöder 8, 16 eller 32 åkare per klass med A- och B-finaler.
                </p>
            </div>
        </div>
    </div>
</div>

<!-- Filter Section -->
<div class="admin-card mb-lg">
    <div class="admin-card-body">
        <form method="GET" class="admin-form-row">
            <div class="admin-form-group" style="margin-bottom: 0;">
                <label for="year-filter" class="admin-form-label">År</label>
                <select id="year-filter" name="year" class="admin-form-select" onchange="this.form.submit()">
                    <?php foreach ($allYears as $yearRow): ?>
                        <option value="<?= $yearRow['year'] ?>" <?= $filterYear == $yearRow['year'] ? 'selected' : '' ?>>
                            <?= $yearRow['year'] ?>
                        </option>
                    <?php endforeach; ?>
                </select>
            </div>
        </form>
    </div>
</div>

<?php if (empty($events)): ?>
    <div class="admin-card">
        <div class="admin-card-body">
            <div class="admin-empty-state">
                <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M8.21 13.89 7 23l5-3 5 3-1.21-9.12"/><path d="M15 7a3 3 0 1 0 0-6 3 3 0 0 0 0 6Z"/><path d="M9 7a3 3 0 1 0 0-6 3 3 0 0 0 0 6Z"/></svg>
                <h3>Inga elimination-events hittades</h3>
                <p>Det finns inga Dual Slalom eller elimination-events för <?= $filterYear ?>.</p>
                <p style="color: var(--color-text-secondary); font-size: var(--text-sm); margin-top: var(--space-sm);">
                    Tips: Skapa ett event och välj "DUAL_SLALOM" som format, eller koppla elimination-data till ett befintligt event.
                </p>
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
                        <th class="text-center">Kval</th>
                        <th class="text-center">Bracket</th>
                        <th class="text-center">Status</th>
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
                            </td>
                            <td><?= h($event['location'] ?? '-') ?></td>
                            <td><?= h($event['series_name'] ?? '-') ?></td>
                            <td class="text-center">
                                <span class="admin-badge admin-badge-<?= ($event['qualifying_count'] ?? 0) > 0 ? 'success' : 'secondary' ?>">
                                    <?= $event['qualifying_count'] ?? 0 ?>
                                </span>
                            </td>
                            <td class="text-center">
                                <span class="admin-badge admin-badge-<?= ($event['bracket_count'] ?? 0) > 0 ? 'success' : 'secondary' ?>">
                                    <?= $event['bracket_count'] ?? 0 ?>
                                </span>
                            </td>
                            <td class="text-center">
                                <?php
                                $statusClass = 'secondary';
                                $statusText = 'Ej startat';
                                if (($event['result_count'] ?? 0) > 0) {
                                    $statusClass = 'success';
                                    $statusText = 'Slutfört';
                                } elseif (($event['bracket_count'] ?? 0) > 0) {
                                    $statusClass = 'warning';
                                    $statusText = 'Pågår';
                                } elseif (($event['qualifying_count'] ?? 0) > 0) {
                                    $statusClass = 'info';
                                    $statusText = 'Kval klart';
                                }
                                ?>
                                <span class="admin-badge admin-badge-<?= $statusClass ?>"><?= $statusText ?></span>
                            </td>
                            <td class="table-actions">
                                <a href="/admin/elimination-manage.php?event_id=<?= $event['id'] ?>" class="btn-admin btn-admin-primary btn-admin-sm" title="Hantera">
                                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M17 3a2.85 2.83 0 1 1 4 4L7.5 20.5 2 22l1.5-5.5Z"/><path d="m15 5 4 4"/></svg>
                                </a>
                                <a href="/event/<?= $event['id'] ?>?tab=elimination" class="btn-admin btn-admin-secondary btn-admin-sm" title="Visa">
                                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M2 12s3-7 10-7 10 7 10 7-3 7-10 7-10-7-10-7Z"/><circle cx="12" cy="12" r="3"/></svg>
                                </a>
                            </td>
                        </tr>
                    <?php endforeach; ?>
                </tbody>
            </table>
        </div>
    </div>
<?php endif; ?>

<?php include __DIR__ . '/components/unified-layout-footer.php'; ?>
