<?php
/**
 * Admin Venues - REDIRECT till Destinations
 * Behalles for bakatkompatibilitet
 */
header('Location: /admin/destinations.php');
exit;

$db = getDB();

// Initialize message variables
$message = '';
$messageType = 'info';

// Handle delete action
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    checkCsrf();

    $action = $_POST['action'] ?? '';

    if ($action === 'delete') {
        $id = intval($_POST['id']);
        $eventCount = $db->getRow("SELECT COUNT(*) as cnt FROM events WHERE venue_id = ?", [$id])['cnt'] ?? 0;

        if ($eventCount > 0) {
            $message = "Kan inte ta bort anläggning med $eventCount kopplade events.";
            $messageType = 'error';
        } else {
            try {
                $db->delete('venues', 'id = ?', [$id]);
                $message = 'Anläggning borttagen!';
                $messageType = 'success';
            } catch (Exception $e) {
                $message = 'Ett fel uppstod: ' . $e->getMessage();
                $messageType = 'error';
            }
        }
    }
}

// Handle URL messages
if (isset($_GET['msg'])) {
    switch ($_GET['msg']) {
        case 'deleted':
            $message = 'Anläggning borttagen!';
            $messageType = 'success';
            break;
    }
}

// Handle search
$search = $_GET['search'] ?? '';

$where = [];
$params = [];

if ($search) {
    $where[] = "(name LIKE ? OR city LIKE ? OR region LIKE ?)";
    $params[] = "%$search%";
    $params[] = "%$search%";
    $params[] = "%$search%";
}

$whereClause = $where ? 'WHERE ' . implode(' AND ', $where) : '';

// Get venues with event count
$sql = "SELECT
    v.id, v.name, v.city, v.region, v.country, v.address, v.description,
    v.gps_lat, v.gps_lng, v.active, v.logo, v.website,
    COUNT(DISTINCT e.id) as event_count
FROM venues v
LEFT JOIN events e ON v.id = e.venue_id
$whereClause
GROUP BY v.id
ORDER BY v.name";

try {
    $venues = $db->getAll($sql, $params);
} catch (Exception $e) {
    $venues = [];
    $error = $e->getMessage();
}

// Calculate stats
$totalVenues = count($venues);
$activeCount = count(array_filter($venues, fn($v) => $v['active'] == 1));
$totalEvents = array_sum(array_column($venues, 'event_count'));

// Page config
$page_title = 'Anläggningar';
$page_actions = '<a href="/admin/import-venues.php" class="btn-admin btn-admin-secondary mr-sm">
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="17 8 12 3 7 8"/><line x1="12" x2="12" y1="3" y2="15"/></svg>
    Importera
</a>
<a href="/admin/venue-edit.php" class="btn-admin btn-admin-primary">
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M5 12h14"/><path d="M12 5v14"/></svg>
    Ny Anläggning
</a>';

include __DIR__ . '/components/unified-layout.php';
?>

<?php if ($message): ?>
    <div class="alert alert-<?= $messageType === 'success' ? 'success' : ($messageType === 'error' ? 'error' : 'info') ?>">
        <?= htmlspecialchars($message) ?>
    </div>
<?php endif; ?>

<?php if (isset($error)): ?>
    <div class="alert alert-error">
        <strong>Fel:</strong> <?= htmlspecialchars($error) ?>
    </div>
<?php endif; ?>

<!-- Stats Grid -->
<div class="admin-stats-grid">
    <div class="admin-stat-card">
        <div class="admin-stat-icon" style="background: var(--color-info-light); color: var(--color-info);">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="m8 3 4 8 5-5 5 15H2L8 3z"/></svg>
        </div>
        <div class="admin-stat-content">
            <div class="admin-stat-value"><?= $totalVenues ?></div>
            <div class="admin-stat-label">Totalt anläggningar</div>
        </div>
    </div>

    <div class="admin-stat-card">
        <div class="admin-stat-icon" style="background: var(--color-success-light); color: var(--color-success);">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/></svg>
        </div>
        <div class="admin-stat-content">
            <div class="admin-stat-value"><?= $activeCount ?></div>
            <div class="admin-stat-label">Aktiva</div>
        </div>
    </div>

    <div class="admin-stat-card">
        <div class="admin-stat-icon" style="background: var(--color-accent-light); color: var(--color-accent);">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M8 2v4"/><path d="M16 2v4"/><rect width="18" height="18" x="3" y="4" rx="2"/><path d="M3 10h18"/></svg>
        </div>
        <div class="admin-stat-content">
            <div class="admin-stat-value"><?= $totalEvents ?></div>
            <div class="admin-stat-label">Totalt events</div>
        </div>
    </div>
</div>

<!-- Search -->
<div class="admin-card mb-lg">
    <div class="admin-card-body">
        <form method="GET" class="flex gap-md items-end">
            <div class="flex-1">
                <label class="admin-form-label">Sök anläggning</label>
                <input type="text" name="search" class="admin-form-input" placeholder="Sök på namn, stad eller region..." value="<?= htmlspecialchars($search) ?>">
            </div>
            <button type="submit" class="btn-admin btn-admin-primary">Sök</button>
            <?php if ($search): ?>
                <a href="/admin/venues.php" class="btn-admin btn-admin-secondary">Rensa</a>
            <?php endif; ?>
        </form>
    </div>
</div>

<!-- Venues Table -->
<div class="admin-card">
    <div class="admin-card-header">
        <h2><?= count($venues) ?> anläggningar<?= $search ? ' (filtrerat)' : '' ?></h2>
    </div>
    <div class="admin-card-body" style="padding: 0;">
        <?php if (empty($venues)): ?>
            <div class="admin-empty-state">
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="m8 3 4 8 5-5 5 15H2L8 3z"/></svg>
                <h3>Inga anläggningar hittades</h3>
                <p>Skapa en ny anläggning för att komma igång.</p>
                <a href="/admin/venue-edit.php" class="btn-admin btn-admin-primary">Skapa anläggning</a>
            </div>
        <?php else: ?>
            <div class="admin-table-container">
                <table class="admin-table">
                    <thead>
                        <tr>
                            <th>Anläggning</th>
                            <th>Plats</th>
                            <th>GPS</th>
                            <th>Events</th>
                            <th>Status</th>
                            <th style="width: 120px;">Åtgärder</th>
                        </tr>
                    </thead>
                    <tbody>
                        <?php foreach ($venues as $venue): ?>
                            <tr>
                                <td>
                                    <div style="display: flex; align-items: center; gap: var(--space-sm);">
                                        <?php if (!empty($venue['logo'])): ?>
                                            <img src="<?= htmlspecialchars($venue['logo']) ?>" alt="" style="width: 32px; height: 32px; object-fit: contain; border-radius: var(--radius-sm);">
                                        <?php endif; ?>
                                        <div>
                                            <a href="/admin/venue-edit.php?id=<?= $venue['id'] ?>" style="color: var(--color-accent); text-decoration: none; font-weight: 500;">
                                                <?= htmlspecialchars($venue['name']) ?>
                                            </a>
                                            <?php if (!empty($venue['description'])): ?>
                                                <div style="font-size: var(--text-xs); color: var(--color-text-secondary); margin-top: 2px;">
                                                    <?= htmlspecialchars(substr($venue['description'], 0, 60)) ?><?= strlen($venue['description']) > 60 ? '...' : '' ?>
                                                </div>
                                            <?php endif; ?>
                                        </div>
                                    </div>
                                </td>
                                <td class="text-secondary">
                                    <?php if ($venue['city'] || $venue['region']): ?>
                                        <?= htmlspecialchars($venue['city']) ?><?= $venue['city'] && $venue['region'] ? ', ' : '' ?><?= htmlspecialchars($venue['region']) ?>
                                    <?php else: ?>-<?php endif; ?>
                                </td>
                                <td>
                                    <?php if ($venue['gps_lat'] && $venue['gps_lng']): ?>
                                        <a href="https://www.google.com/maps?q=<?= $venue['gps_lat'] ?>,<?= $venue['gps_lng'] ?>" target="_blank" style="color: var(--color-accent); text-decoration: none; font-size: var(--text-xs);">
                                            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="width: 12px; height: 12px; vertical-align: middle;"><path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0Z"/><circle cx="12" cy="10" r="3"/></svg>
                                            Karta
                                        </a>
                                    <?php else: ?>-<?php endif; ?>
                                </td>
                                <td>
                                    <?php if ($venue['event_count'] > 0): ?>
                                        <a href="/admin/events.php?venue_id=<?= $venue['id'] ?>" class="btn-admin btn-admin-sm btn-admin-secondary">
                                            <?= $venue['event_count'] ?>
                                        </a>
                                    <?php else: ?>
                                        <span class="text-secondary">0</span>
                                    <?php endif; ?>
                                </td>
                                <td>
                                    <span class="admin-badge <?= $venue['active'] ? 'admin-badge-success' : 'admin-badge-secondary' ?>">
                                        <?= $venue['active'] ? 'Aktiv' : 'Inaktiv' ?>
                                    </span>
                                </td>
                                <td>
                                    <div class="table-actions">
                                        <a href="/admin/venue-edit.php?id=<?= $venue['id'] ?>" class="btn-admin btn-admin-sm btn-admin-secondary" title="Redigera">
                                            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M17 3a2.85 2.83 0 1 1 4 4L7.5 20.5 2 22l1.5-5.5Z"/><path d="m15 5 4 4"/></svg>
                                        </a>
                                        <?php if ($venue['event_count'] == 0): ?>
                                        <form method="POST" style="display: inline;" onsubmit="return confirm('Är du säker på att du vill ta bort denna anläggning?')">
                                            <?= csrf_field() ?>
                                            <input type="hidden" name="action" value="delete">
                                            <input type="hidden" name="id" value="<?= $venue['id'] ?>">
                                            <button type="submit" class="btn-admin btn-admin-sm btn-admin-danger" title="Ta bort">
                                                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 6h18"/><path d="M19 6v14c0 1-1 2-2 2H7c-1 0-2-1-2-2V6"/><path d="M8 6V4c0-1 1-2 2-2h4c1 0 2 1 2 2v2"/></svg>
                                            </button>
                                        </form>
                                        <?php endif; ?>
                                    </div>
                                </td>
                            </tr>
                        <?php endforeach; ?>
                    </tbody>
                </table>
            </div>
        <?php endif; ?>
    </div>
</div>

<?php include __DIR__ . '/components/unified-layout-footer.php'; ?>
