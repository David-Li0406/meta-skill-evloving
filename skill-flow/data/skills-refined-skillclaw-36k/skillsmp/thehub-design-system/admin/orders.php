<?php
/**
 * Order Management - View and confirm payments
 * V3 Unified Layout
 *
 * Accessible by:
 * - Super Admin: Can manage all orders
 * - Promotor: Can manage orders for their events
 */

require_once __DIR__ . '/../config.php';
require_once __DIR__ . '/../includes/payment.php';
require_admin();

$db = getDB();
$currentAdmin = getCurrentAdmin();
$isSuperAdmin = hasRole('super_admin');

$message = '';
$messageType = 'info';

// Handle actions
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    checkCsrf();

    $action = $_POST['action'] ?? '';
    $orderId = intval($_POST['order_id'] ?? 0);

    if ($action === 'confirm_payment' && $orderId) {
        $paymentRef = trim($_POST['payment_reference'] ?? '');

        try {
            if (markOrderPaid($orderId, $paymentRef)) {
                $message = 'Betalning bekräftad!';
                $messageType = 'success';
            } else {
                $message = 'Kunde inte bekräfta betalningen.';
                $messageType = 'error';
            }
        } catch (Exception $e) {
            $message = 'Fel: ' . $e->getMessage();
            $messageType = 'error';
        }

    } elseif ($action === 'cancel_order' && $orderId) {
        $db->update('orders', [
            'payment_status' => 'cancelled',
            'cancelled_at' => date('Y-m-d H:i:s')
        ], 'id = ?', [$orderId]);

        // Also cancel registrations
        $db->query("
            UPDATE event_registrations
            SET status = 'cancelled'
            WHERE order_id = ?
        ", [$orderId]);

        $message = 'Order avbruten!';
        $messageType = 'success';
    }
}

// Filter parameters
$filterStatus = $_GET['status'] ?? 'pending';
$filterEvent = isset($_GET['event_id']) ? intval($_GET['event_id']) : 0;
$search = trim($_GET['search'] ?? '');

// Build query
$whereConditions = [];
$params = [];

// Status filter
if ($filterStatus && $filterStatus !== 'all') {
    $whereConditions[] = "o.payment_status = ?";
    $params[] = $filterStatus;
}

// Event filter
if ($filterEvent) {
    $whereConditions[] = "o.event_id = ?";
    $params[] = $filterEvent;
}

// Search
if ($search) {
    $whereConditions[] = "(o.order_number LIKE ? OR o.customer_name LIKE ? OR o.swish_message LIKE ?)";
    $searchTerm = "%{$search}%";
    $params[] = $searchTerm;
    $params[] = $searchTerm;
    $params[] = $searchTerm;
}

// Promotor restriction - only their events
if (!$isSuperAdmin) {
    $whereConditions[] = "o.event_id IN (SELECT event_id FROM promotor_events WHERE user_id = ?)";
    $params[] = $currentAdmin['id'];
}

$whereClause = !empty($whereConditions) ? 'WHERE ' . implode(' AND ', $whereConditions) : '';

// Get orders with item count for multi-rider support
$orders = $db->getAll("
    SELECT o.*, e.name as event_name, e.date as event_date,
           r.firstname, r.lastname,
           s.name as series_name,
           (SELECT COUNT(*) FROM order_items oi WHERE oi.order_id = o.id) as item_count
    FROM orders o
    LEFT JOIN events e ON o.event_id = e.id
    LEFT JOIN series s ON o.series_id = s.id
    LEFT JOIN riders r ON o.rider_id = r.id
    {$whereClause}
    ORDER BY o.created_at DESC
    LIMIT 200
", $params);

// Get events for filter (only accessible events)
if ($isSuperAdmin) {
    $events = $db->getAll("
        SELECT DISTINCT e.id, e.name, e.date
        FROM events e
        JOIN orders o ON o.event_id = e.id
        ORDER BY e.date DESC
        LIMIT 50
    ");
} else {
    $events = $db->getAll("
        SELECT DISTINCT e.id, e.name, e.date
        FROM events e
        JOIN promotor_events pe ON pe.event_id = e.id
        WHERE pe.user_id = ?
        ORDER BY e.date DESC
    ", [$currentAdmin['id']]);
}

// Stats
$stats = $db->getRow("
    SELECT
        COUNT(CASE WHEN payment_status = 'pending' THEN 1 END) as pending_count,
        COUNT(CASE WHEN payment_status = 'paid' THEN 1 END) as paid_count,
        SUM(CASE WHEN payment_status = 'paid' THEN total_amount ELSE 0 END) as total_revenue
    FROM orders o
    " . ($isSuperAdmin ? '' : "WHERE o.event_id IN (SELECT event_id FROM promotor_events WHERE user_id = {$currentAdmin['id']})") . "
");

// Page config for unified layout
$page_title = 'Ordrar';
$breadcrumbs = [
    ['label' => 'Ekonomi']
];

include __DIR__ . '/components/unified-layout.php';
?>

<!-- Message -->
<?php if ($message): ?>
<div class="alert alert-<?= $messageType === 'success' ? 'success' : 'error' ?> mb-lg">
    <i data-lucide="<?= $messageType === 'success' ? 'check-circle' : 'alert-circle' ?>"></i>
    <?= h($message) ?>
</div>
<?php endif; ?>

<!-- Stats -->
<div class="admin-stats-grid">
    <div class="admin-stat-card">
        <div class="admin-stat-icon stat-icon-warning">
            <i data-lucide="clock"></i>
        </div>
        <div class="admin-stat-content">
            <div class="admin-stat-value"><?= $stats['pending_count'] ?? 0 ?></div>
            <div class="admin-stat-label">Väntar på betalning</div>
        </div>
    </div>
    <div class="admin-stat-card">
        <div class="admin-stat-icon stat-icon-success">
            <i data-lucide="check-circle"></i>
        </div>
        <div class="admin-stat-content">
            <div class="admin-stat-value"><?= $stats['paid_count'] ?? 0 ?></div>
            <div class="admin-stat-label">Betalda ordrar</div>
        </div>
    </div>
    <div class="admin-stat-card">
        <div class="admin-stat-icon stat-icon-accent">
            <i data-lucide="wallet"></i>
        </div>
        <div class="admin-stat-content">
            <div class="admin-stat-value"><?= number_format($stats['total_revenue'] ?? 0, 0, ',', ' ') ?> kr</div>
            <div class="admin-stat-label">Totalt inbetalt</div>
        </div>
    </div>
</div>

<!-- Filters -->
<div class="admin-card mb-lg">
    <div class="admin-card-body">
        <form method="GET" class="flex flex-wrap gap-md items-end">
            <div class="admin-form-group mb-0">
                <label class="admin-form-label">Status</label>
                <select name="status" class="admin-form-select" onchange="this.form.submit()">
                    <option value="pending" <?= $filterStatus === 'pending' ? 'selected' : '' ?>>Väntar</option>
                    <option value="paid" <?= $filterStatus === 'paid' ? 'selected' : '' ?>>Betalda</option>
                    <option value="cancelled" <?= $filterStatus === 'cancelled' ? 'selected' : '' ?>>Avbrutna</option>
                    <option value="all" <?= $filterStatus === 'all' ? 'selected' : '' ?>>Alla</option>
                </select>
            </div>

            <?php if (!empty($events)): ?>
            <div class="admin-form-group mb-0">
                <label class="admin-form-label">Event</label>
                <select name="event_id" class="admin-form-select" onchange="this.form.submit()">
                    <option value="">Alla event</option>
                    <?php foreach ($events as $event): ?>
                    <option value="<?= $event['id'] ?>" <?= $filterEvent == $event['id'] ? 'selected' : '' ?>>
                        <?= h($event['name']) ?> (<?= date('Y-m-d', strtotime($event['date'])) ?>)
                    </option>
                    <?php endforeach; ?>
                </select>
            </div>
            <?php endif; ?>

            <div class="admin-form-group mb-0 flex-1 min-w-200">
                <label class="admin-form-label">Sök</label>
                <input type="text" name="search" class="admin-form-input"
                       value="<?= h($search) ?>"
                       placeholder="Ordernummer, namn, Swish-ref...">
            </div>

            <button type="submit" class="btn-admin btn-admin-primary">
                <i data-lucide="search"></i>
                Sök
            </button>
        </form>
    </div>
</div>

<!-- Orders list -->
<div class="admin-card">
    <div class="admin-card-header">
        <h2><?= count($orders) ?> ordrar</h2>
    </div>
    <div class="admin-card-body p-0">
        <?php if (empty($orders)): ?>
        <div class="admin-empty-state">
            <i data-lucide="inbox"></i>
            <h3>Inga ordrar hittades</h3>
            <p>Justera filtren för att se fler ordrar.</p>
        </div>
        <?php else: ?>
        <div class="admin-table-container">
            <table class="admin-table">
                <thead>
                    <tr>
                        <th>Order</th>
                        <th>Kund</th>
                        <th>Event/Serie</th>
                        <th>Deltagare</th>
                        <th>Belopp</th>
                        <th>Swish-ref</th>
                        <th>Status</th>
                        <th>Skapad</th>
                        <th></th>
                    </tr>
                </thead>
                <tbody>
                    <?php foreach ($orders as $order): ?>
                    <tr>
                        <td>
                            <code class="font-medium"><?= h($order['order_number']) ?></code>
                        </td>
                        <td>
                            <div class="font-medium">
                                <?= h($order['firstname'] . ' ' . $order['lastname']) ?>
                            </div>
                            <div class="text-xs text-secondary"><?= h($order['customer_email']) ?></div>
                        </td>
                        <td>
                            <?php if ($order['series_name']): ?>
                            <div><span class="admin-badge admin-badge-info">Serie</span> <?= h($order['series_name']) ?></div>
                            <?php elseif ($order['event_name']): ?>
                            <div><?= h($order['event_name']) ?></div>
                            <div class="text-xs text-secondary"><?= date('Y-m-d', strtotime($order['event_date'])) ?></div>
                            <?php else: ?>
                            <span class="text-secondary">-</span>
                            <?php endif; ?>
                        </td>
                        <td class="text-center">
                            <?php if ($order['item_count'] > 1): ?>
                            <span class="admin-badge admin-badge-accent"><?= $order['item_count'] ?> st</span>
                            <?php elseif ($order['item_count'] == 1): ?>
                            <span class="text-secondary">1</span>
                            <?php else: ?>
                            <span class="text-secondary">-</span>
                            <?php endif; ?>
                        </td>
                        <td class="font-medium">
                            <?= number_format($order['total_amount'], 0) ?> kr
                        </td>
                        <td>
                            <?php if ($order['swish_message']): ?>
                            <code><?= h($order['swish_message']) ?></code>
                            <?php endif; ?>
                        </td>
                        <td>
                            <?php
                            $statusClass = [
                                'pending' => 'admin-badge-warning',
                                'paid' => 'admin-badge-success',
                                'cancelled' => 'admin-badge-secondary',
                                'refunded' => 'admin-badge-error',
                                'failed' => 'admin-badge-error'
                            ][$order['payment_status']] ?? 'admin-badge-secondary';

                            $statusText = [
                                'pending' => 'Väntar',
                                'paid' => 'Betald',
                                'cancelled' => 'Avbruten',
                                'refunded' => 'Återbetald',
                                'failed' => 'Misslyckad'
                            ][$order['payment_status']] ?? $order['payment_status'];
                            ?>
                            <span class="admin-badge <?= $statusClass ?>"><?= $statusText ?></span>
                        </td>
                        <td class="text-sm text-secondary">
                            <?= date('Y-m-d H:i', strtotime($order['created_at'])) ?>
                        </td>
                        <td>
                            <?php if ($order['payment_status'] === 'pending'): ?>
                            <div class="table-actions">
                                <button type="button" class="btn-admin btn-admin-sm" style="background: var(--color-success); color: white;"
                                        onclick="openConfirmModal(<?= $order['id'] ?>, '<?= h($order['order_number']) ?>', '<?= h($order['swish_message']) ?>')">
                                    <i data-lucide="check"></i>
                                </button>
                                <form method="POST" class="inline">
                                    <?= csrf_field() ?>
                                    <input type="hidden" name="action" value="cancel_order">
                                    <input type="hidden" name="order_id" value="<?= $order['id'] ?>">
                                    <button type="submit" class="btn-admin btn-admin-sm btn-admin-secondary"
                                            onclick="return confirm('Avbryt denna order?')">
                                        <i data-lucide="x"></i>
                                    </button>
                                </form>
                            </div>
                            <?php elseif ($order['payment_status'] === 'paid'): ?>
                            <span class="text-xs text-secondary">
                                Betald <?= $order['paid_at'] ? date('Y-m-d', strtotime($order['paid_at'])) : '' ?>
                            </span>
                            <?php endif; ?>
                        </td>
                    </tr>
                    <?php endforeach; ?>
                </tbody>
            </table>
        </div>
        <?php endif; ?>
    </div>
</div>

<!-- Confirm Payment Modal -->
<div id="confirm-modal" class="admin-modal hidden">
    <div class="admin-modal-overlay" onclick="closeModal('confirm-modal')"></div>
    <div class="admin-modal-content" style="max-width: 500px;">
        <div class="admin-modal-header">
            <h2>Bekräfta betalning</h2>
            <button type="button" class="admin-modal-close" onclick="closeModal('confirm-modal')">
                <i data-lucide="x"></i>
            </button>
        </div>
        <form method="POST">
            <?= csrf_field() ?>
            <input type="hidden" name="action" value="confirm_payment">
            <input type="hidden" name="order_id" id="confirm-order-id">

            <div class="admin-modal-body">
                <p class="mb-md">
                    Bekräfta att betalning mottagits för order
                    <strong id="confirm-order-number"></strong>
                </p>

                <div class="p-md mb-md" style="background: var(--color-bg-tertiary); border-radius: var(--radius-md);">
                    <div class="text-sm text-secondary">Förväntat Swish-meddelande:</div>
                    <code class="text-lg" id="confirm-swish-ref"></code>
                </div>

                <div class="admin-form-group">
                    <label class="admin-form-label">Betalningsreferens (valfritt)</label>
                    <input type="text" name="payment_reference" class="admin-form-input"
                           placeholder="T.ex. Swish-transaktions-ID">
                    <small class="text-secondary">Ange referens från Swish eller kontoutdrag</small>
                </div>
            </div>

            <div class="admin-modal-footer">
                <button type="button" class="btn-admin btn-admin-secondary" onclick="closeModal('confirm-modal')">Avbryt</button>
                <button type="submit" class="btn-admin" style="background: var(--color-success); color: white;">
                    <i data-lucide="check"></i>
                    Bekräfta betalning
                </button>
            </div>
        </form>
    </div>
</div>

<style>
.admin-modal { position: fixed; top: 0; left: 0; right: 0; bottom: 0; z-index: 1000; display: flex; align-items: center; justify-content: center; }
.admin-modal.hidden { display: none; }
.admin-modal-overlay { position: absolute; top: 0; left: 0; right: 0; bottom: 0; background: rgba(0, 0, 0, 0.5); }
.admin-modal-content { position: relative; background: white; border-radius: var(--radius-lg); box-shadow: var(--shadow-xl); width: 90%; max-width: 500px; max-height: 90vh; overflow: hidden; display: flex; flex-direction: column; }
.admin-modal-header { display: flex; align-items: center; justify-content: space-between; padding: var(--space-lg); border-bottom: 1px solid var(--color-border); }
.admin-modal-header h2 { margin: 0; font-size: var(--text-xl); }
.admin-modal-close { background: none; border: none; padding: var(--space-xs); cursor: pointer; color: var(--color-text-secondary); border-radius: var(--radius-sm); }
.admin-modal-close:hover { background: var(--color-bg-tertiary); color: var(--color-text); }
.admin-modal-close svg, .admin-modal-close i { width: 20px; height: 20px; }
.admin-modal-body { padding: var(--space-lg); overflow-y: auto; flex: 1; }
.admin-modal-footer { display: flex; justify-content: flex-end; gap: var(--space-sm); padding: var(--space-lg); border-top: 1px solid var(--color-border); }
.admin-badge-warning { background: rgba(234, 179, 8, 0.2); color: #ca8a04; }
.admin-badge-error { background: rgba(239, 68, 68, 0.2); color: #dc2626; }
.admin-badge-info { background: rgba(56, 189, 248, 0.2); color: #0284c7; }
.admin-badge-accent { background: rgba(55, 212, 214, 0.2); color: var(--color-accent); font-weight: 600; }
</style>

<script>
function openConfirmModal(orderId, orderNumber, swishRef) {
    document.getElementById('confirm-order-id').value = orderId;
    document.getElementById('confirm-order-number').textContent = orderNumber;
    document.getElementById('confirm-swish-ref').textContent = swishRef;
    document.getElementById('confirm-modal').classList.remove('hidden');
}

function closeModal(modalId) {
    document.getElementById(modalId).classList.add('hidden');
}

document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape') {
        document.querySelectorAll('.admin-modal').forEach(m => m.classList.add('hidden'));
    }
});
</script>

<?php include __DIR__ . '/components/unified-layout-footer.php'; ?>
