<?php
/**
 * TheHUB On-Site Registration
 * Allows promotors to register participants at the event venue
 */
require_once __DIR__ . '/../config.php';
require_admin();

// Allow promotors and admins
if (!hasRole('promotor')) {
    set_flash('error', 'Du har inte behörighet till denna sida');
    redirect('/');
}

$db = getDB();
$currentUser = getCurrentAdmin();
$userId = $currentUser['id'] ?? 0;
$isPromotorOnly = isRole('promotor') && !hasRole('admin');

// Get user's assigned events (for promotors) or all upcoming events (for admins)
$upcomingEvents = [];
try {
    if ($isPromotorOnly) {
        // Get promotor's assigned events that haven't happened yet
        // Check both promotor_events (direct assignment) and promotor_series (series-wide)
        $upcomingEvents = $db->getAll("
            SELECT DISTINCT e.id, e.name, e.date, e.location, s.name as series_name
            FROM events e
            LEFT JOIN series s ON e.series_id = s.id
            LEFT JOIN promotor_events pe ON pe.event_id = e.id AND pe.user_id = ?
            LEFT JOIN promotor_series ps ON e.series_id = ps.series_id AND ps.user_id = ?
            WHERE (pe.user_id IS NOT NULL OR ps.user_id IS NOT NULL)
              AND e.date >= CURDATE()
            ORDER BY e.date ASC
            LIMIT 20
        ", [$userId, $userId]);
    } else {
        // Admins see all upcoming events
        $upcomingEvents = $db->getAll("
            SELECT e.id, e.name, e.date, e.location, s.name as series_name
            FROM events e
            LEFT JOIN series s ON e.series_id = s.id
            WHERE e.date >= CURDATE()
            ORDER BY e.date ASC
            LIMIT 20
        ");
    }
} catch (Exception $e) {
    error_log("Error fetching events for on-site registration: " . $e->getMessage());
}

$pageTitle = 'Direktanmälan';
include __DIR__ . '/components/unified-layout.php';
?>

<div class="admin-content">
    <div class="page-header">
        <h1><?= $pageTitle ?></h1>
        <p class="text-muted">Registrera deltagare direkt på tävlingsplatsen</p>
    </div>

    <?php if (empty($upcomingEvents)): ?>
    <div class="card">
        <div class="card-body">
            <p class="text-muted">Inga kommande tävlingar att visa.</p>
        </div>
    </div>
    <?php else: ?>
    <div class="card">
        <div class="card-header">
            <h3>Välj tävling</h3>
        </div>
        <div class="card-body">
            <div class="form-group">
                <label class="form-label">Kommande tävlingar</label>
                <select class="form-select" id="event-select">
                    <option value="">-- Välj tävling --</option>
                    <?php foreach ($upcomingEvents as $event): ?>
                    <option value="<?= $event['id'] ?>">
                        <?= htmlspecialchars($event['name']) ?>
                        (<?= date('d M Y', strtotime($event['date'])) ?>)
                        <?= $event['series_name'] ? ' - ' . htmlspecialchars($event['series_name']) : '' ?>
                    </option>
                    <?php endforeach; ?>
                </select>
            </div>
        </div>
    </div>

    <div class="card" id="registration-form" style="display: none;">
        <div class="card-header">
            <h3>Registrera deltagare</h3>
        </div>
        <div class="card-body">
            <p class="alert alert-info">
                Denna funktion är under utveckling. Här kommer du kunna:
            </p>
            <ul style="margin-left: var(--space-lg); color: var(--color-text-secondary);">
                <li>Söka efter befintliga deltagare i databasen</li>
                <li>Registrera nya deltagare direkt på plats</li>
                <li>Hantera betalning via Swish</li>
                <li>Skriva ut startnummer</li>
            </ul>
        </div>
    </div>
    <?php endif; ?>
</div>

<script>
document.getElementById('event-select')?.addEventListener('change', function() {
    const form = document.getElementById('registration-form');
    if (this.value) {
        form.style.display = 'block';
    } else {
        form.style.display = 'none';
    }
});
</script>

<?php include __DIR__ . '/components/unified-layout-footer.php'; ?>
