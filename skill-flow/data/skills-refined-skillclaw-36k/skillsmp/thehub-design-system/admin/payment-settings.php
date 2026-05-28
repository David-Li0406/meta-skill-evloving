<?php
/**
 * Payment Settings - Manage Swish/payment configuration
 *
 * Accessible by:
 * - Super Admin: Can manage all payment configs
 * - Promotor: Can manage their own payment settings
 */

require_once __DIR__ . '/../config.php';
require_admin();

$db = getDB();
$currentAdmin = getCurrentAdmin();
$isSuperAdmin = hasRole('super_admin');
$isPromotor = $currentAdmin['role'] === 'promotor';

// Get user ID from URL (super admin only) or use current user
$userId = $isSuperAdmin && isset($_GET['user_id']) ? intval($_GET['user_id']) : $currentAdmin['id'];

// Verify access
if (!$isSuperAdmin && $userId !== $currentAdmin['id']) {
    http_response_code(403);
    die('Access denied');
}

// Get user info
$user = $db->getRow("SELECT * FROM admin_users WHERE id = ?", [$userId]);
if (!$user) {
    // If user not found, try to get the current logged in admin's info from session
    $user = [
        'id' => $currentAdmin['id'],
        'username' => $currentAdmin['username'] ?? '',
        'name' => $currentAdmin['name'] ?? $currentAdmin['username'] ?? 'Admin',
        'role' => $currentAdmin['role'] ?? 'admin',
        'swish_number' => null,
        'swish_name' => null
    ];
}

$message = '';
$messageType = 'info';

// Handle form submission
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    checkCsrf();

    $action = $_POST['action'] ?? '';

    if ($action === 'save_profile_swish') {
        // Save Swish number directly on user profile
        $swishNumber = trim($_POST['swish_number'] ?? '');
        $swishName = trim($_POST['swish_name'] ?? '');

        $db->update('admin_users', [
            'swish_number' => $swishNumber ?: null,
            'swish_name' => $swishName ?: null
        ], 'id = ?', [$userId]);

        $user = $db->getRow("SELECT * FROM admin_users WHERE id = ?", [$userId]);
        $message = 'Swish-uppgifter sparade!';
        $messageType = 'success';

    } elseif ($action === 'save_event_config') {
        // Save event-specific payment config
        $eventId = intval($_POST['event_id'] ?? 0);
        $swishEnabled = isset($_POST['swish_enabled']) ? 1 : 0;
        $swishNumber = trim($_POST['event_swish_number'] ?? '');
        $swishName = trim($_POST['event_swish_name'] ?? '');

        if ($eventId && $swishNumber) {
            // Check if config exists
            $existing = $db->getRow("SELECT id FROM payment_configs WHERE event_id = ?", [$eventId]);

            if ($existing) {
                $db->update('payment_configs', [
                    'swish_enabled' => $swishEnabled,
                    'swish_number' => $swishNumber,
                    'swish_name' => $swishName
                ], 'id = ?', [$existing['id']]);
            } else {
                $db->insert('payment_configs', [
                    'event_id' => $eventId,
                    'swish_enabled' => $swishEnabled,
                    'swish_number' => $swishNumber,
                    'swish_name' => $swishName
                ]);
            }

            $message = 'Event-betalning sparad!';
            $messageType = 'success';
        }

    } elseif ($action === 'save_series_config') {
        // Save series-specific payment config
        $seriesId = intval($_POST['series_id'] ?? 0);
        $swishEnabled = isset($_POST['swish_enabled']) ? 1 : 0;
        $swishNumber = trim($_POST['series_swish_number'] ?? '');
        $swishName = trim($_POST['series_swish_name'] ?? '');

        if ($seriesId && $swishNumber) {
            $existing = $db->getRow("SELECT id FROM payment_configs WHERE series_id = ?", [$seriesId]);

            if ($existing) {
                $db->update('payment_configs', [
                    'swish_enabled' => $swishEnabled,
                    'swish_number' => $swishNumber,
                    'swish_name' => $swishName
                ], 'id = ?', [$existing['id']]);
            } else {
                $db->insert('payment_configs', [
                    'series_id' => $seriesId,
                    'swish_enabled' => $swishEnabled,
                    'swish_number' => $swishNumber,
                    'swish_name' => $swishName
                ]);
            }

            $message = 'Serie-betalning sparad!';
            $messageType = 'success';
        }

    } elseif ($action === 'delete_config') {
        $configId = intval($_POST['config_id'] ?? 0);
        if ($configId) {
            $db->delete('payment_configs', 'id = ?', [$configId]);
            $message = 'Betalningskonfiguration borttagen!';
            $messageType = 'success';
        }
    }
}

// Get promotor's assigned events
$assignedEvents = $db->getAll("
    SELECT e.id, e.name, e.date, e.location, s.name as series_name,
           pc.id as config_id, pc.swish_enabled, pc.swish_number, pc.swish_name
    FROM promotor_events pe
    JOIN events e ON pe.event_id = e.id
    LEFT JOIN series s ON e.series_id = s.id
    LEFT JOIN payment_configs pc ON pc.event_id = e.id
    WHERE pe.user_id = ?
    ORDER BY e.date DESC
", [$userId]);

// Get series (for super admin or series promotors)
$series = [];
if ($isSuperAdmin) {
    $series = $db->getAll("
        SELECT s.id, s.name, COUNT(e.id) as event_count,
               pc.id as config_id, pc.swish_enabled, pc.swish_number, pc.swish_name
        FROM series s
        LEFT JOIN events e ON s.id = e.series_id
        LEFT JOIN payment_configs pc ON pc.series_id = s.id
        GROUP BY s.id
        ORDER BY s.name
    ");
}

// Page settings for unified layout
$page_title = 'Betalningsinställningar';
$page_actions = $isSuperAdmin ? '<a href="/admin/users.php" class="btn btn--secondary"><i data-lucide="arrow-left"></i> Tillbaka</a>' : '';
include __DIR__ . '/components/unified-layout.php';
?>

        <!-- Message -->
        <?php if ($message): ?>
        <div class="alert alert-<?= h($messageType) ?> mb-lg">
            <i data-lucide="<?= $messageType === 'success' ? 'check-circle' : 'alert-circle' ?>"></i>
            <?= h($message) ?>
        </div>
        <?php endif; ?>

        <!-- Profile Swish Settings -->
        <div class="card mb-lg">
            <div class="card-header">
                <h2 class="">
                    <i data-lucide="user"></i>
                    Ditt Swish-konto (standard)
                </h2>
            </div>
            <div class="card-body">
                <p class="text-secondary mb-md">
                    Detta Swish-nummer används som standard för alla dina event om inte annat anges.
                </p>
                <form method="POST">
                    <?= csrf_field() ?>
                    <input type="hidden" name="action" value="save_profile_swish">

                    <div class="grid grid-2 gap-md">
                        <div class="form-group">
                            <label class="label">Swish-nummer</label>
                            <input type="text" name="swish_number" class="input"
                                   value="<?= h($user['swish_number'] ?? '') ?>"
                                   placeholder="073-123 45 67">
                            <small class="text-secondary">Mobilnummer eller företagsnummer</small>
                        </div>
                        <div class="form-group">
                            <label class="label">Visningsnamn</label>
                            <input type="text" name="swish_name" class="input"
                                   value="<?= h($user['swish_name'] ?? '') ?>"
                                   placeholder="Klubbnamn eller ditt namn">
                            <small class="text-secondary">Visas för betalaren</small>
                        </div>
                    </div>

                    <button type="submit" class="btn btn--primary mt-md">
                        <i data-lucide="save"></i>
                        Spara
                    </button>
                </form>
            </div>
        </div>

        <!-- Event-specific settings -->
        <?php if (!empty($assignedEvents)): ?>
        <div class="card mb-lg">
            <div class="card-header">
                <h2 class="">
                    <i data-lucide="calendar"></i>
                    Event-specifika inställningar
                </h2>
            </div>
            <div class="card-body gs-p-0">
                <div class="table-container">
                    <table class="table">
                        <thead>
                            <tr>
                                <th>Event</th>
                                <th>Datum</th>
                                <th>Swish-nummer</th>
                                <th>Status</th>
                                <th></th>
                            </tr>
                        </thead>
                        <tbody>
                            <?php foreach ($assignedEvents as $event): ?>
                            <tr>
                                <td>
                                    <div class="font-medium"><?= h($event['name']) ?></div>
                                    <?php if ($event['series_name']): ?>
                                    <div class="text-xs text-secondary"><?= h($event['series_name']) ?></div>
                                    <?php endif; ?>
                                </td>
                                <td><?= date('Y-m-d', strtotime($event['date'])) ?></td>
                                <td>
                                    <?php if ($event['swish_number']): ?>
                                        <code><?= h($event['swish_number']) ?></code>
                                    <?php else: ?>
                                        <span class="text-secondary">Använder standard</span>
                                    <?php endif; ?>
                                </td>
                                <td>
                                    <?php if ($event['config_id'] && $event['swish_enabled']): ?>
                                        <span class="badge badge-success">Aktiv</span>
                                    <?php elseif ($event['config_id']): ?>
                                        <span class="badge badge-secondary">Inaktiv</span>
                                    <?php else: ?>
                                        <span class="badge badge-warning">Standard</span>
                                    <?php endif; ?>
                                </td>
                                <td class="text-right">
                                    <button type="button" class="btn btn--sm btn--secondary"
                                            onclick="openEventModal(<?= $event['id'] ?>, '<?= h($event['name']) ?>', '<?= h($event['swish_number'] ?? '') ?>', '<?= h($event['swish_name'] ?? '') ?>', <?= $event['swish_enabled'] ?? 0 ?>)">
                                        <i data-lucide="edit"></i>
                                    </button>
                                </td>
                            </tr>
                            <?php endforeach; ?>
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
        <?php endif; ?>

        <!-- Series settings (super admin only) -->
        <?php if ($isSuperAdmin && !empty($series)): ?>
        <div class="card">
            <div class="card-header">
                <h2 class="">
                    <i data-lucide="layers"></i>
                    Serie-inställningar
                </h2>
            </div>
            <div class="card-body gs-p-0">
                <div class="table-container">
                    <table class="table">
                        <thead>
                            <tr>
                                <th>Serie</th>
                                <th>Events</th>
                                <th>Swish-nummer</th>
                                <th>Status</th>
                                <th></th>
                            </tr>
                        </thead>
                        <tbody>
                            <?php foreach ($series as $s): ?>
                            <tr>
                                <td class="font-medium"><?= h($s['name']) ?></td>
                                <td><?= $s['event_count'] ?> st</td>
                                <td>
                                    <?php if ($s['swish_number']): ?>
                                        <code><?= h($s['swish_number']) ?></code>
                                    <?php else: ?>
                                        <span class="text-secondary">Ej konfigurerat</span>
                                    <?php endif; ?>
                                </td>
                                <td>
                                    <?php if ($s['config_id'] && $s['swish_enabled']): ?>
                                        <span class="badge badge-success">Aktiv</span>
                                    <?php elseif ($s['config_id']): ?>
                                        <span class="badge badge-secondary">Inaktiv</span>
                                    <?php else: ?>
                                        <span class="badge badge-warning">Ej satt</span>
                                    <?php endif; ?>
                                </td>
                                <td class="text-right">
                                    <button type="button" class="btn btn--sm btn--secondary"
                                            onclick="openSeriesModal(<?= $s['id'] ?>, '<?= h($s['name']) ?>', '<?= h($s['swish_number'] ?? '') ?>', '<?= h($s['swish_name'] ?? '') ?>', <?= $s['swish_enabled'] ?? 0 ?>)">
                                        <i data-lucide="edit"></i>
                                    </button>
                                </td>
                            </tr>
                            <?php endforeach; ?>
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
        <?php endif; ?>

        <!-- Help text -->
        <div class="card mt-lg">
            <div class="card-body">
                <h3 class="font-medium mb-sm">Hur det fungerar</h3>
                <ul class="text-sm text-secondary" style="list-style: disc; padding-left: 1.5rem;">
                    <li><strong>Standard Swish:</strong> Används för alla dina event om inget annat anges</li>
                    <li><strong>Event-specifikt:</strong> Överskrider standard för ett enskilt event</li>
                    <li><strong>Serie-Swish:</strong> Används för alla event i serien (om inget event-specifikt)</li>
                </ul>
                <p class="text-sm text-secondary mt-md">
                    Prioritetsordning: Event-specifik > Serie > Din standard > WooCommerce
                </p>
            </div>
        </div>

<!-- Event Modal -->
<div id="event-modal" class="modal hidden">
    <div class="modal-backdrop" onclick="closeModal('event-modal')"></div>
    <div class="modal-content">
        <div class="modal-header">
            <h3 id="event-modal-title">Redigera event</h3>
            <button type="button" class="modal-close" onclick="closeModal('event-modal')">&times;</button>
        </div>
        <form method="POST">
            <?= csrf_field() ?>
            <input type="hidden" name="action" value="save_event_config">
            <input type="hidden" name="event_id" id="event-id">

            <div class="modal-body">
                <div class="form-group">
                    <label class="checkbox-label">
                        <input type="checkbox" name="swish_enabled" id="event-swish-enabled" value="1">
                        <span>Aktivera Swish för detta event</span>
                    </label>
                </div>
                <div class="form-group">
                    <label class="label">Swish-nummer</label>
                    <input type="text" name="event_swish_number" id="event-swish-number" class="input"
                           placeholder="073-123 45 67">
                </div>
                <div class="form-group">
                    <label class="label">Visningsnamn</label>
                    <input type="text" name="event_swish_name" id="event-swish-name" class="input"
                           placeholder="Arrangörens namn">
                </div>
            </div>

            <div class="modal-footer">
                <button type="button" class="btn btn--secondary" onclick="closeModal('event-modal')">Avbryt</button>
                <button type="submit" class="btn btn--primary">Spara</button>
            </div>
        </form>
    </div>
</div>

<!-- Series Modal -->
<div id="series-modal" class="modal hidden">
    <div class="modal-backdrop" onclick="closeModal('series-modal')"></div>
    <div class="modal-content">
        <div class="modal-header">
            <h3 id="series-modal-title">Redigera serie</h3>
            <button type="button" class="modal-close" onclick="closeModal('series-modal')">&times;</button>
        </div>
        <form method="POST">
            <?= csrf_field() ?>
            <input type="hidden" name="action" value="save_series_config">
            <input type="hidden" name="series_id" id="series-id">

            <div class="modal-body">
                <div class="form-group">
                    <label class="checkbox-label">
                        <input type="checkbox" name="swish_enabled" id="series-swish-enabled" value="1">
                        <span>Aktivera Swish för hela serien</span>
                    </label>
                </div>
                <div class="form-group">
                    <label class="label">Swish-nummer</label>
                    <input type="text" name="series_swish_number" id="series-swish-number" class="input"
                           placeholder="073-123 45 67">
                </div>
                <div class="form-group">
                    <label class="label">Visningsnamn</label>
                    <input type="text" name="series_swish_name" id="series-swish-name" class="input"
                           placeholder="Seriens namn">
                </div>
            </div>

            <div class="modal-footer">
                <button type="button" class="btn btn--secondary" onclick="closeModal('series-modal')">Avbryt</button>
                <button type="submit" class="btn btn--primary">Spara</button>
            </div>
        </form>
    </div>
</div>

<style>
.modal {
    position: fixed;
    inset: 0;
    z-index: 1000;
    display: flex;
    align-items: center;
    justify-content: center;
}
.modal.hidden {
    display: none;
}
.modal-backdrop {
    position: absolute;
    inset: 0;
    background: rgba(0, 0, 0, 0.5);
}
.modal-content {
    position: relative;
    background: var(--color-bg-surface);
    border-radius: var(--radius-lg);
    width: 100%;
    max-width: 500px;
    margin: var(--space-md);
}
.modal-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: var(--space-md) var(--space-lg);
    border-bottom: 1px solid var(--color-border);
}
.modal-close {
    background: none;
    border: none;
    font-size: 1.5rem;
    cursor: pointer;
    color: var(--color-text-secondary);
}
.modal-body {
    padding: var(--space-lg);
}
.modal-footer {
    display: flex;
    justify-content: flex-end;
    gap: var(--space-sm);
    padding: var(--space-md) var(--space-lg);
    border-top: 1px solid var(--color-border);
}
</style>

<script>
function openEventModal(eventId, eventName, swishNumber, swishName, swishEnabled) {
    document.getElementById('event-modal-title').textContent = eventName;
    document.getElementById('event-id').value = eventId;
    document.getElementById('event-swish-number').value = swishNumber;
    document.getElementById('event-swish-name').value = swishName;
    document.getElementById('event-swish-enabled').checked = swishEnabled == 1;
    document.getElementById('event-modal').classList.remove('hidden');
}

function openSeriesModal(seriesId, seriesName, swishNumber, swishName, swishEnabled) {
    document.getElementById('series-modal-title').textContent = seriesName;
    document.getElementById('series-id').value = seriesId;
    document.getElementById('series-swish-number').value = swishNumber;
    document.getElementById('series-swish-name').value = swishName;
    document.getElementById('series-swish-enabled').checked = swishEnabled == 1;
    document.getElementById('series-modal').classList.remove('hidden');
}

function closeModal(modalId) {
    document.getElementById(modalId).classList.add('hidden');
}

// Close on escape
document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape') {
        document.querySelectorAll('.modal').forEach(m => m.classList.add('hidden'));
    }
});
</script>

<?php include __DIR__ . '/components/unified-layout-footer.php'; ?>
