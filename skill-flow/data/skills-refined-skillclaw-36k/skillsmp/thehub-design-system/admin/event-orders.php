<?php
/**
 * Event Orders - Orders for a specific event
 * Uses Economy Tab System
 */

require_once __DIR__ . '/../config.php';
require_once __DIR__ . '/../includes/payment.php';

$db = getDB();

// Get event ID (supports both 'id' and 'event_id')
$eventId = isset($_GET['id']) ? intval($_GET['id']) : (isset($_GET['event_id']) ? intval($_GET['event_id']) : 0);

if ($eventId <= 0) {
    $_SESSION['flash_message'] = 'Ogiltigt event-ID';
    $_SESSION['flash_type'] = 'error';
    header('Location: /admin/events.php');
    exit;
}

// Fetch event
$event = $db->getRow("
    SELECT e.*, s.name as series_name
    FROM events e
    LEFT JOIN series s ON e.series_id = s.id
    WHERE e.id = ?
", [$eventId]);

if (!$event) {
    $_SESSION['flash_message'] = 'Event hittades inte';
    $_SESSION['flash_type'] = 'error';
    header('Location: /admin/events.php');
    exit;
}

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
        $db->query("UPDATE event_registrations SET status = 'cancelled' WHERE order_id = ?", [$orderId]);

        $message = 'Order avbruten!';
        $messageType = 'success';
    }
}

// Filter parameters
$filterStatus = $_GET['status'] ?? 'all';
$search = trim($_GET['search'] ?? '');

// Build query
$whereConditions = ["o.event_id = ?"];
$params = [$eventId];

if ($filterStatus && $filterStatus !== 'all') {
    $whereConditions[] = "o.payment_status = ?";
    $params[] = $filterStatus;
}

if ($search) {
    $whereConditions[] = "(o.order_number LIKE ? OR o.customer_name LIKE ? OR o.swish_message LIKE ?)";
    $searchTerm = "%{$search}%";
    $params[] = $searchTerm;
    $params[] = $searchTerm;
    $params[] = $searchTerm;
}

$whereClause = 'WHERE ' . implode(' AND ', $whereConditions);

// Get orders
$orders = $db->getAll("
    SELECT o.*, r.firstname, r.lastname
    FROM orders o
    LEFT JOIN riders r ON o.rider_id = r.id
    {$whereClause}
    ORDER BY o.created_at DESC
    LIMIT 100
", $params);

// Get stats
$stats = $db->getRow("
    SELECT
        COUNT(*) as total,
        SUM(CASE WHEN payment_status = 'pending' THEN 1 ELSE 0 END) as pending,
        SUM(CASE WHEN payment_status = 'paid' THEN 1 ELSE 0 END) as paid,
        SUM(CASE WHEN payment_status = 'paid' THEN total_amount ELSE 0 END) as revenue
    FROM orders
    WHERE event_id = ?
", [$eventId]);

// Set page variables for economy layout
$economy_page_title = 'Ordrar';

include __DIR__ . '/components/economy-layout.php';
?>

        <!-- Message -->
        <?php if ($message): ?>
        <div class="alert alert-<?= h($messageType) ?> mb-lg">
            <i data-lucide="<?= $messageType === 'success' ? 'check-circle' : 'alert-circle' ?>"></i>
            <?= h($message) ?>
        </div>
        <?php endif; ?>

        <!-- Stats -->
        <div class="grid grid-4 gap-md mb-lg">
            <div class="card">
                <div class="card-body text-center">
                    <div class="text-3xl font-bold"><?= $stats['total'] ?? 0 ?></div>
                    <div class="text-sm text-secondary">Totalt</div>
                </div>
            </div>
            <div class="card">
                <div class="card-body text-center">
                    <div class="text-3xl font-bold text-warning"><?= $stats['pending'] ?? 0 ?></div>
                    <div class="text-sm text-secondary">Väntar på betalning</div>
                </div>
            </div>
            <div class="card">
                <div class="card-body text-center">
                    <div class="text-3xl font-bold text-success"><?= $stats['paid'] ?? 0 ?></div>
                    <div class="text-sm text-secondary">Betalda ordrar</div>
                </div>
            </div>
            <div class="card">
                <div class="card-body text-center">
                    <div class="text-3xl font-bold"><?= number_format($stats['revenue'] ?? 0, 0, ',', ' ') ?> kr</div>
                    <div class="text-sm text-secondary">Totalt inbetalt</div>
                </div>
            </div>
        </div>

        <!-- Filters -->
        <div class="card mb-lg">
            <div class="card-body">
                <form method="GET" class="flex flex-wrap gap-md items-end">
                    <input type="hidden" name="id" value="<?= $eventId ?>">

                    <div class="form-group mb-0">
                        <label class="label">Status</label>
                        <select name="status" class="input" onchange="this.form.submit()">
                            <option value="all" <?= $filterStatus === 'all' ? 'selected' : '' ?>>Alla</option>
                            <option value="pending" <?= $filterStatus === 'pending' ? 'selected' : '' ?>>Väntar</option>
                            <option value="paid" <?= $filterStatus === 'paid' ? 'selected' : '' ?>>Betalda</option>
                            <option value="cancelled" <?= $filterStatus === 'cancelled' ? 'selected' : '' ?>>Avbrutna</option>
                        </select>
                    </div>

                    <div class="form-group mb-0">
                        <label class="label">Sök</label>
                        <input type="text" name="search" class="input"
                               value="<?= h($search) ?>"
                               placeholder="Ordernummer, namn, Swish-ref...">
                    </div>

                    <button type="submit" class="btn btn--primary">
                        <i data-lucide="search"></i>
                        Sök
                    </button>
                </form>
            </div>
        </div>

        <!-- Orders Table -->
        <div class="card">
            <div class="card-body gs-p-0">
                <?php if (empty($orders)): ?>
                <div class="p-xl text-center text-secondary">
                    <i data-lucide="inbox" class="icon-xl mb-md" style="opacity: 0.3;"></i>
                    <p>Inga ordrar hittades</p>
                </div>
                <?php else: ?>
                <div class="table-responsive">
                    <table class="table">
                        <thead>
                            <tr>
                                <th>Order</th>
                                <th>Kund</th>
                                <th>Belopp</th>
                                <th>Swish-meddelande</th>
                                <th>Status</th>
                                <th>Skapad</th>
                                <th></th>
                            </tr>
                        </thead>
                        <tbody>
                            <?php foreach ($orders as $order): ?>
                            <tr>
                                <td>
                                    <strong><?= htmlspecialchars($order['order_number']) ?></strong>
                                </td>
                                <td>
                                    <?= htmlspecialchars($order['customer_name'] ?: ($order['firstname'] . ' ' . $order['lastname'])) ?>
                                    <?php if ($order['customer_email']): ?>
                                    <div class="text-xs text-secondary"><?= htmlspecialchars($order['customer_email']) ?></div>
                                    <?php endif; ?>
                                </td>
                                <td>
                                    <strong><?= number_format($order['total_amount'], 0) ?> kr</strong>
                                </td>
                                <td>
                                    <?php if ($order['swish_message']): ?>
                                    <code><?= htmlspecialchars($order['swish_message']) ?></code>
                                    <?php else: ?>
                                    <span class="text-secondary">-</span>
                                    <?php endif; ?>
                                </td>
                                <td>
                                    <?php
                                    $statusBadge = match($order['payment_status']) {
                                        'pending' => 'badge-warning',
                                        'paid' => 'badge-success',
                                        'cancelled' => 'badge-secondary',
                                        'refunded' => 'badge-info',
                                        default => 'badge-secondary'
                                    };
                                    $statusLabel = match($order['payment_status']) {
                                        'pending' => 'Väntande',
                                        'paid' => 'Betald',
                                        'cancelled' => 'Avbruten',
                                        'refunded' => 'Återbetald',
                                        default => $order['payment_status']
                                    };
                                    ?>
                                    <span class="badge <?= $statusBadge ?>"><?= $statusLabel ?></span>
                                </td>
                                <td>
                                    <span class="text-sm"><?= date('Y-m-d H:i', strtotime($order['created_at'])) ?></span>
                                </td>
                                <td class="text-right">
                                    <?php if ($order['payment_status'] === 'pending'): ?>
                                    <div class="flex gap-xs justify-end">
                                        <form method="POST" style="display: inline;">
                                            <?= csrf_field() ?>
                                            <input type="hidden" name="action" value="confirm_payment">
                                            <input type="hidden" name="order_id" value="<?= $order['id'] ?>">
                                            <button type="submit" class="btn btn--sm btn--success"
                                                    onclick="return confirm('Bekräfta betalning för <?= htmlspecialchars($order['order_number']) ?>?')">
                                                <i data-lucide="check"></i>
                                            </button>
                                        </form>
                                        <form method="POST" style="display: inline;">
                                            <?= csrf_field() ?>
                                            <input type="hidden" name="action" value="cancel_order">
                                            <input type="hidden" name="order_id" value="<?= $order['id'] ?>">
                                            <button type="submit" class="btn btn--sm btn--secondary"
                                                    onclick="return confirm('Avbryta order <?= htmlspecialchars($order['order_number']) ?>?')">
                                                <i data-lucide="x"></i>
                                            </button>
                                        </form>
                                    </div>
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

<style>
.icon-xl {
    width: 48px;
    height: 48px;
}
</style>

<?php include __DIR__ . '/components/economy-layout-footer.php'; ?>
