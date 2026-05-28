<?php
/**
 * Manage Promotor Event Assignments
 * Only accessible by super_admin
 */
require_once __DIR__ . '/../config.php';
require_admin();

// Only super_admin can access this page
if (!hasRole('super_admin')) {
    http_response_code(403);
    die('Access denied: Only super administrators can manage user events.');
}

$db = getDB();

// Get user ID
$id = isset($_GET['id']) && is_numeric($_GET['id']) ? intval($_GET['id']) : null;

if (!$id) {
    header('Location: /admin/users');
    exit;
}

// Fetch user
$user = $db->getRow("SELECT * FROM admin_users WHERE id = ?", [$id]);

if (!$user || $user['role'] !== 'promotor') {
    header('Location: /admin/users');
    exit;
}

$message = '';
$messageType = 'info';

// Handle form submission
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    checkCsrf();

    $action = $_POST['action'] ?? '';

    if ($action === 'add') {
        $eventId = isset($_POST['event_id']) ? intval($_POST['event_id']) : 0;
        $canEdit = isset($_POST['can_edit']) ? 1 : 0;
        $canResults = isset($_POST['can_manage_results']) ? 1 : 0;
        $canRegistrations = isset($_POST['can_manage_registrations']) ? 1 : 0;

        if ($eventId) {
            try {
                // Check if already exists
                $existing = $db->getRow(
                    "SELECT id FROM promotor_events WHERE user_id = ? AND event_id = ?",
                    [$id, $eventId]
                );

                $currentAdmin = getCurrentAdmin();

                if ($existing) {
                    // Update existing
                    $db->update('promotor_events', [
                        'can_edit' => $canEdit,
                        'can_manage_results' => $canResults,
                        'can_manage_registrations' => $canRegistrations,
                        'granted_by' => $currentAdmin['id']
                    ], 'id = ?', [$existing['id']]);
                    $message = 'Event-behörighet uppdaterad!';
                } else {
                    // Insert new
                    $insertId = $db->insert('promotor_events', [
                        'user_id' => $id,
                        'event_id' => $eventId,
                        'can_edit' => $canEdit,
                        'can_manage_results' => $canResults,
                        'can_manage_registrations' => $canRegistrations,
                        'granted_by' => $currentAdmin['id']
                    ]);
                    if ($insertId) {
                        $message = 'Event tillagt!';
                        $messageType = 'success';
                    } else {
                        $message = 'Kunde inte lägga till event. Kontrollera att tabellen promotor_events finns.';
                        $messageType = 'error';
                    }
                }
            } catch (Exception $e) {
                $message = 'Ett fel uppstod: ' . $e->getMessage();
                $messageType = 'error';
            }
        }
    } elseif ($action === 'update') {
        $eventId = isset($_POST['event_id']) ? intval($_POST['event_id']) : 0;
        $canEdit = isset($_POST['can_edit']) ? 1 : 0;
        $canResults = isset($_POST['can_manage_results']) ? 1 : 0;
        $canRegistrations = isset($_POST['can_manage_registrations']) ? 1 : 0;

        if ($eventId) {
            try {
                $db->update('promotor_events', [
                    'can_edit' => $canEdit,
                    'can_manage_results' => $canResults,
                    'can_manage_registrations' => $canRegistrations
                ], 'user_id = ? AND event_id = ?', [$id, $eventId]);
                $message = 'Behörigheter uppdaterade!';
                $messageType = 'success';
            } catch (Exception $e) {
                $message = 'Ett fel uppstod: ' . $e->getMessage();
                $messageType = 'error';
            }
        }
    } elseif ($action === 'remove') {
        $eventId = isset($_POST['event_id']) ? intval($_POST['event_id']) : 0;
        if ($eventId) {
            try {
                $db->delete('promotor_events', 'user_id = ? AND event_id = ?', [$id, $eventId]);
                $message = 'Event borttaget!';
                $messageType = 'success';
            } catch (Exception $e) {
                $message = 'Ett fel uppstod: ' . $e->getMessage();
                $messageType = 'error';
            }
        }
    } elseif ($action === 'add_series') {
        $seriesId = isset($_POST['series_id']) ? intval($_POST['series_id']) : 0;
        $canEdit = isset($_POST['can_edit']) ? 1 : 0;
        $canResults = isset($_POST['can_manage_results']) ? 1 : 0;
        $canRegistrations = isset($_POST['can_manage_registrations']) ? 1 : 0;

        if ($seriesId) {
            try {
                $currentAdmin = getCurrentAdmin();

                // First: Add to promotor_series for series-level access
                $existingSeries = $db->getRow(
                    "SELECT id FROM promotor_series WHERE user_id = ? AND series_id = ?",
                    [$id, $seriesId]
                );

                if (!$existingSeries) {
                    $db->insert('promotor_series', [
                        'user_id' => $id,
                        'series_id' => $seriesId,
                        'granted_by' => $currentAdmin['id']
                    ]);
                }

                // Second: Also add individual events for backward compatibility
                $seriesEvents = $db->getAll("SELECT id FROM events WHERE series_id = ?", [$seriesId]);
                $addedCount = 0;

                $failedCount = 0;
                foreach ($seriesEvents as $event) {
                    $existing = $db->getRow(
                        "SELECT id FROM promotor_events WHERE user_id = ? AND event_id = ?",
                        [$id, $event['id']]
                    );

                    if (!$existing) {
                        $insertId = $db->insert('promotor_events', [
                            'user_id' => $id,
                            'event_id' => $event['id'],
                            'can_edit' => $canEdit,
                            'can_manage_results' => $canResults,
                            'can_manage_registrations' => $canRegistrations,
                            'granted_by' => $currentAdmin['id']
                        ]);
                        if ($insertId) {
                            $addedCount++;
                        } else {
                            $failedCount++;
                        }
                    }
                }

                $seriesName = $db->getValue("SELECT name FROM series WHERE id = ?", [$seriesId]);
                if ($failedCount > 0) {
                    $message = "Kunde inte lägga till events. Kontrollera att tabellen promotor_events finns.";
                    $messageType = 'error';
                } else {
                    $message = "Serie '{$seriesName}' tilldelad! " . ($addedCount > 0 ? "$addedCount event tillagda." : "Alla events fanns redan.");
                    $messageType = 'success';
                }
            } catch (Exception $e) {
                $message = 'Ett fel uppstod: ' . $e->getMessage();
                $messageType = 'error';
            }
        }
    } elseif ($action === 'remove_series') {
        $seriesId = isset($_POST['series_id']) ? intval($_POST['series_id']) : 0;
        if ($seriesId) {
            try {
                // Remove from promotor_series
                $db->delete('promotor_series', 'user_id = ? AND series_id = ?', [$id, $seriesId]);

                // Also remove all events from this series
                $db->query("
                    DELETE pe FROM promotor_events pe
                    JOIN events e ON pe.event_id = e.id
                    WHERE pe.user_id = ? AND e.series_id = ?
                ", [$id, $seriesId]);

                $message = 'Serie och alla dess events borttagna!';
                $messageType = 'success';
            } catch (Exception $e) {
                $message = 'Ett fel uppstod: ' . $e->getMessage();
                $messageType = 'error';
            }
        }
    }
}

// Get user's assigned events
$assignedEvents = $db->getAll("
    SELECT pe.*, e.name as event_name, e.date as event_date, e.location,
           s.name as series_name, s.year as series_year,
           au.full_name as granted_by_name
    FROM promotor_events pe
    JOIN events e ON pe.event_id = e.id
    LEFT JOIN series s ON e.series_id = s.id
    LEFT JOIN admin_users au ON pe.granted_by = au.id
    WHERE pe.user_id = ?
    ORDER BY e.date DESC
", [$id]);

$assignedEventIds = array_column($assignedEvents, 'event_id');

// Get available events (not already assigned)
$availableEvents = $db->getAll("
    SELECT e.id, e.name, e.date, e.location, s.name as series_name, s.year as series_year
    FROM events e
    LEFT JOIN series s ON e.series_id = s.id
    WHERE e.id NOT IN (SELECT event_id FROM promotor_events WHERE user_id = ?)
    ORDER BY e.date DESC
    LIMIT 100
", [$id]);

// Get user's assigned series (full series access)
$assignedSeries = $db->getAll("
    SELECT ps.*, s.name as series_name, s.year as series_year,
           au.full_name as granted_by_name,
           (SELECT COUNT(*) FROM events WHERE series_id = s.id) as event_count
    FROM promotor_series ps
    JOIN series s ON ps.series_id = s.id
    LEFT JOIN admin_users au ON ps.granted_by = au.id
    WHERE ps.user_id = ?
    ORDER BY s.year DESC, s.name
", [$id]);
$assignedSeriesIds = array_column($assignedSeries, 'series_id');

// Get all series for bulk add (exclude already assigned)
$allSeries = $db->getAll("
    SELECT s.id, s.name, s.year, COUNT(e.id) as event_count
    FROM series s
    LEFT JOIN events e ON s.id = e.series_id
    WHERE s.id NOT IN (SELECT series_id FROM promotor_series WHERE user_id = ?)
    GROUP BY s.id
    ORDER BY s.year DESC, s.name
", [$id]);

// Set up page for unified layout
$page_title = 'Event-tilldelning: ' . h($user['full_name'] ?: $user['username']);
$page_actions = '<a href="/admin/user-edit?id=' . $id . '" class="btn btn--secondary">
    <i data-lucide="arrow-left"></i>
    Tillbaka
</a>';

// Include unified layout (uses same layout as public site)
include __DIR__ . '/components/unified-layout.php';
?>

<!-- Message -->
<?php if ($message): ?>
<div class="alert alert--<?= $messageType === 'error' ? 'error' : ($messageType === 'success' ? 'success' : 'info') ?> mb-lg">
    <i data-lucide="<?= $messageType === 'success' ? 'check-circle' : 'alert-circle' ?>"></i>
    <?= h($message) ?>
</div>
<?php endif; ?>

<div class="grid grid-cols-1 lg-grid-cols-2 gap-lg">
    <!-- Assigned Events -->
    <div class="card">
        <div class="card-header">
            <h2>
                <i data-lucide="check-circle"></i>
                Tilldelade events (<?= count($assignedEvents) ?>)
            </h2>
        </div>
        <div class="card-body" style="padding: 0;">
            <?php if (empty($assignedEvents)): ?>
            <div class="text-center text-secondary" style="padding: var(--space-xl);">
                <i data-lucide="calendar-x" style="width: 48px; height: 48px; margin-bottom: var(--space-md);"></i>
                <p>Inga events tilldelade</p>
            </div>
            <?php else: ?>
            <div class="table-responsive">
                <table class="table">
                    <thead>
                        <tr>
                            <th>Event</th>
                            <th class="text-center">Redigera</th>
                            <th class="text-center">Resultat</th>
                            <th class="text-center">Anmälningar</th>
                            <th></th>
                        </tr>
                    </thead>
                    <tbody>
                        <?php foreach ($assignedEvents as $event): ?>
                        <tr>
                            <td>
                                <div class="font-medium"><?= h($event['event_name']) ?></div>
                                <div class="text-xs text-secondary">
                                    <?= date('Y-m-d', strtotime($event['event_date'])) ?>
                                    <?php if ($event['series_name']): ?>
                                    - <?= h($event['series_name']) ?><?= $event['series_year'] ? ' ' . $event['series_year'] : '' ?>
                                    <?php endif; ?>
                                </div>
                            </td>
                            <form method="POST" class="event-perm-form" data-event="<?= $event['event_id'] ?>">
                                <?= csrf_field() ?>
                                <input type="hidden" name="action" value="update">
                                <input type="hidden" name="event_id" value="<?= $event['event_id'] ?>">
                                <td class="text-center">
                                    <input type="checkbox" name="can_edit" value="1" <?= $event['can_edit'] ? 'checked' : '' ?> onchange="this.form.submit()" class="checkbox-input">
                                </td>
                                <td class="text-center">
                                    <input type="checkbox" name="can_manage_results" value="1" <?= $event['can_manage_results'] ? 'checked' : '' ?> onchange="this.form.submit()" class="checkbox-input">
                                </td>
                                <td class="text-center">
                                    <input type="checkbox" name="can_manage_registrations" value="1" <?= $event['can_manage_registrations'] ? 'checked' : '' ?> onchange="this.form.submit()" class="checkbox-input">
                                </td>
                            </form>
                            <td class="text-right">
                                <form method="POST" style="display: inline;">
                                    <?= csrf_field() ?>
                                    <input type="hidden" name="action" value="remove">
                                    <input type="hidden" name="event_id" value="<?= $event['event_id'] ?>">
                                    <button type="submit" class="btn btn--sm btn--danger" onclick="return confirm('Ta bort detta event?')">
                                        <i data-lucide="x"></i>
                                    </button>
                                </form>
                            </td>
                        </tr>
                        <?php endforeach; ?>
                    </tbody>
                </table>
            </div>
            <?php endif; ?>
        </div>
    </div>

    <!-- Add Event -->
    <div class="card">
        <div class="card-header">
            <h2>
                <i data-lucide="plus-circle"></i>
                Lägg till event
            </h2>
        </div>
        <div class="card-body">
            <?php if (empty($availableEvents)): ?>
            <div class="text-center text-secondary" style="padding: var(--space-lg);">
                <i data-lucide="check" style="width: 48px; height: 48px; margin-bottom: var(--space-md);"></i>
                <p>Alla events är redan tilldelade</p>
            </div>
            <?php else: ?>
            <form method="POST">
                <?= csrf_field() ?>
                <input type="hidden" name="action" value="add">

                <div class="form-group">
                    <label for="event_id" class="form-label">Välj event</label>
                    <select id="event_id" name="event_id" class="form-select" required>
                        <option value="">-- Välj event --</option>
                        <?php foreach ($availableEvents as $event): ?>
                        <option value="<?= $event['id'] ?>">
                            <?= h($event['name']) ?> (<?= date('Y-m-d', strtotime($event['date'])) ?>)
                            <?= $event['series_name'] ? ' - ' . h($event['series_name']) . ($event['series_year'] ? ' ' . $event['series_year'] : '') : '' ?>
                        </option>
                        <?php endforeach; ?>
                    </select>
                </div>

                <div class="form-group">
                    <label class="form-label">Behörigheter</label>
                    <div style="display: flex; flex-direction: column; gap: var(--space-sm);">
                        <label style="display: flex; align-items: center; gap: var(--space-sm);">
                            <input type="checkbox" name="can_edit" value="1" checked>
                            <span>Kan redigera eventinformation</span>
                        </label>
                        <label style="display: flex; align-items: center; gap: var(--space-sm);">
                            <input type="checkbox" name="can_manage_results" value="1" checked>
                            <span>Kan hantera resultat</span>
                        </label>
                        <label style="display: flex; align-items: center; gap: var(--space-sm);">
                            <input type="checkbox" name="can_manage_registrations" value="1" checked>
                            <span>Kan hantera anmälningar</span>
                        </label>
                    </div>
                </div>

                <button type="submit" class="btn btn--primary" style="width: 100%;">
                    <i data-lucide="plus"></i>
                    Lägg till event
                </button>
            </form>
            <?php endif; ?>
        </div>
    </div>
</div>

<!-- Series Management -->
<div class="card mt-lg">
    <div class="card-header">
        <h2>
            <i data-lucide="layers"></i>
            Tilldelade serier (<?= count($assignedSeries) ?>)
        </h2>
    </div>
    <div class="card-body" style="padding: 0;">
        <?php if (empty($assignedSeries)): ?>
        <div class="text-center text-secondary" style="padding: var(--space-xl);">
            <i data-lucide="layers" style="width: 48px; height: 48px; margin-bottom: var(--space-md); opacity: 0.5;"></i>
            <p>Inga serier tilldelade</p>
            <p class="text-xs mt-sm">Tilldela en serie för att ge tillgång till alla dess events + Swish-inställningar</p>
        </div>
        <?php else: ?>
        <div class="table-responsive">
            <table class="table">
                <thead>
                    <tr>
                        <th>Serie</th>
                        <th class="text-center">Events</th>
                        <th></th>
                    </tr>
                </thead>
                <tbody>
                    <?php foreach ($assignedSeries as $series): ?>
                    <tr>
                        <td>
                            <div class="font-medium"><?= h($series['series_name']) ?></div>
                            <div class="text-xs text-secondary">
                                <?= $series['series_year'] ? $series['series_year'] : '' ?>
                                <?php if ($series['granted_by_name']): ?>
                                - Tilldelad av <?= h($series['granted_by_name']) ?>
                                <?php endif; ?>
                            </div>
                        </td>
                        <td class="text-center">
                            <span class="badge badge-info"><?= $series['event_count'] ?></span>
                        </td>
                        <td class="text-right">
                            <form method="POST" style="display: inline;">
                                <?= csrf_field() ?>
                                <input type="hidden" name="action" value="remove_series">
                                <input type="hidden" name="series_id" value="<?= $series['series_id'] ?>">
                                <button type="submit" class="btn btn--sm btn--danger" onclick="return confirm('Ta bort hela serien och alla dess events?')">
                                    <i data-lucide="x"></i>
                                </button>
                            </form>
                        </td>
                    </tr>
                    <?php endforeach; ?>
                </tbody>
            </table>
        </div>
        <?php endif; ?>
    </div>
</div>

<!-- Add Series -->
<?php if (!empty($allSeries)): ?>
<div class="card mt-lg">
    <div class="card-header">
        <h2>
            <i data-lucide="plus-circle"></i>
            Lägg till hel serie
        </h2>
    </div>
    <div class="card-body">
        <form method="POST">
            <?= csrf_field() ?>
            <input type="hidden" name="action" value="add_series">

            <div class="grid grid-cols-1 md-grid-cols-2 gap-md">
                <div class="form-group">
                    <label for="series_id" class="form-label">Välj serie</label>
                    <select id="series_id" name="series_id" class="form-select" required>
                        <option value="">-- Välj serie --</option>
                        <?php foreach ($allSeries as $series): ?>
                        <option value="<?= $series['id'] ?>">
                            <?= h($series['name']) ?><?= $series['year'] ? ' ' . $series['year'] : '' ?> (<?= $series['event_count'] ?> events)
                        </option>
                        <?php endforeach; ?>
                    </select>
                </div>
                <div style="display: flex; align-items: flex-end;">
                    <button type="submit" class="btn btn--primary">
                        <i data-lucide="plus"></i>
                        Tilldela serie
                    </button>
                </div>
            </div>

            <div class="form-group mt-md">
                <label class="form-label">Behörigheter för alla events</label>
                <div style="display: flex; gap: var(--space-lg); flex-wrap: wrap;">
                    <label style="display: flex; align-items: center; gap: var(--space-sm);">
                        <input type="checkbox" name="can_edit" value="1" checked>
                        <span>Redigera</span>
                    </label>
                    <label style="display: flex; align-items: center; gap: var(--space-sm);">
                        <input type="checkbox" name="can_manage_results" value="1" checked>
                        <span>Resultat</span>
                    </label>
                    <label style="display: flex; align-items: center; gap: var(--space-sm);">
                        <input type="checkbox" name="can_manage_registrations" value="1" checked>
                        <span>Anmälningar</span>
                    </label>
                </div>
            </div>
        </form>
    </div>
</div>
<?php endif; ?>

<!-- Help Text -->
<div class="card mt-lg">
    <div class="card-body">
        <h3 style="font-weight: 500; margin-bottom: var(--space-sm);">Om tilldelningar</h3>
        <ul class="text-sm text-secondary" style="list-style: disc; padding-left: 1.5rem;">
            <li><strong>Serie-tilldelning</strong> - Ger tillgång till ALLA events i serien (även framtida) + Swish-inställningar</li>
            <li><strong>Event-tilldelning</strong> - Ger tillgång till specifika events (för finkornig kontroll)</li>
        </ul>

        <h3 style="font-weight: 500; margin: var(--space-md) 0 var(--space-sm);">Om behörigheter</h3>
        <ul class="text-sm text-secondary" style="list-style: disc; padding-left: 1.5rem;">
            <li><strong>Redigera</strong> - Kan ändra eventinformation (namn, datum, plats, beskrivning, etc.)</li>
            <li><strong>Resultat</strong> - Kan importera, redigera och publicera resultat</li>
            <li><strong>Anmälningar</strong> - Kan hantera anmälningar, deltagare och startlistor</li>
        </ul>
        <p class="text-sm text-secondary mt-md">
            <i data-lucide="info" style="width: 16px; height: 16px; display: inline-block; vertical-align: middle;"></i>
            Klicka på kryssrutorna i tabellen för att snabbt ändra behörigheter.
        </p>
    </div>
</div>

<style>
.checkbox-input {
    width: 18px;
    height: 18px;
    cursor: pointer;
}
</style>

<?php include __DIR__ . '/components/unified-layout-footer.php'; ?>
