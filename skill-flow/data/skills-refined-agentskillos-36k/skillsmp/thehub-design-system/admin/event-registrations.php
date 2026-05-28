<?php
/**
 * Event Registrations - View registrations for a specific event
 * Uses Economy Tab System
 */

require_once __DIR__ . '/../config.php';

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

$message = '';
$messageType = 'info';

// Handle actions
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    checkCsrf();

    $action = $_POST['action'] ?? '';
    $regId = intval($_POST['registration_id'] ?? 0);

    if ($action === 'confirm' && $regId) {
        $db->update('event_registrations', [
            'status' => 'confirmed',
            'confirmed_date' => date('Y-m-d H:i:s')
        ], 'id = ?', [$regId]);
        $message = 'Anmälan bekräftad!';
        $messageType = 'success';

    } elseif ($action === 'cancel' && $regId) {
        $db->update('event_registrations', ['status' => 'cancelled'], 'id = ?', [$regId]);
        $message = 'Anmälan avbruten!';
        $messageType = 'success';
    }
}

// Filter parameters
$filterStatus = $_GET['status'] ?? 'all';
$filterClass = $_GET['class'] ?? '';
$search = trim($_GET['search'] ?? '');

// Build query
$whereConditions = ["er.event_id = ?"];
$params = [$eventId];

if ($filterStatus && $filterStatus !== 'all') {
    $whereConditions[] = "er.status = ?";
    $params[] = $filterStatus;
}

if ($filterClass) {
    $whereConditions[] = "er.category = ?";
    $params[] = $filterClass;
}

if ($search) {
    $whereConditions[] = "(er.first_name LIKE ? OR er.last_name LIKE ? OR r.email LIKE ?)";
    $searchTerm = "%{$search}%";
    $params[] = $searchTerm;
    $params[] = $searchTerm;
    $params[] = $searchTerm;
}

$whereClause = 'WHERE ' . implode(' AND ', $whereConditions);

// Get registrations
$registrations = $db->getAll("
    SELECT er.*, r.email, r.phone,
           o.order_number, o.payment_status as order_payment_status
    FROM event_registrations er
    LEFT JOIN riders r ON er.rider_id = r.id
    LEFT JOIN orders o ON er.order_id = o.id
    {$whereClause}
    ORDER BY er.created_at DESC
    LIMIT 200
", $params);

// Get stats
$stats = $db->getRow("
    SELECT
        COUNT(*) as total,
        SUM(CASE WHEN status = 'pending' THEN 1 ELSE 0 END) as pending,
        SUM(CASE WHEN status = 'confirmed' THEN 1 ELSE 0 END) as confirmed,
        SUM(CASE WHEN status = 'cancelled' THEN 1 ELSE 0 END) as cancelled
    FROM event_registrations
    WHERE event_id = ?
", [$eventId]);

// Get available classes for filter
$classes = $db->getAll("
    SELECT DISTINCT category FROM event_registrations WHERE event_id = ? ORDER BY category
", [$eventId]);

// Set page variables for economy layout
$economy_page_title = 'Anmälningar';

include __DIR__ . '/components/economy-layout.php';
?>

        <?php if ($message): ?>
        <div class="alert alert-<?= $messageType ?> mb-lg">
            <i data-lucide="<?= $messageType === 'success' ? 'check-circle' : 'alert-circle' ?>"></i>
            <?= htmlspecialchars($message) ?>
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
                    <div class="text-sm text-secondary">Väntande</div>
                </div>
            </div>
            <div class="card">
                <div class="card-body text-center">
                    <div class="text-3xl font-bold text-success"><?= $stats['confirmed'] ?? 0 ?></div>
                    <div class="text-sm text-secondary">Bekräftade</div>
                </div>
            </div>
            <div class="card">
                <div class="card-body text-center">
                    <div class="text-3xl font-bold text-secondary"><?= $stats['cancelled'] ?? 0 ?></div>
                    <div class="text-sm text-secondary">Avbrutna</div>
                </div>
            </div>
        </div>

        <!-- Filters -->
        <div class="card mb-lg">
            <div class="card-body">
                <form method="GET" class="flex gap-md flex-wrap items-end">
                    <input type="hidden" name="id" value="<?= $eventId ?>">

                    <div class="form-group" style="min-width: 130px;">
                        <label class="label">Status</label>
                        <select name="status" class="input" onchange="this.form.submit()">
                            <option value="all" <?= $filterStatus === 'all' ? 'selected' : '' ?>>Alla</option>
                            <option value="pending" <?= $filterStatus === 'pending' ? 'selected' : '' ?>>Väntande</option>
                            <option value="confirmed" <?= $filterStatus === 'confirmed' ? 'selected' : '' ?>>Bekräftade</option>
                            <option value="cancelled" <?= $filterStatus === 'cancelled' ? 'selected' : '' ?>>Avbrutna</option>
                        </select>
                    </div>

                    <?php if (!empty($classes)): ?>
                    <div class="form-group" style="min-width: 130px;">
                        <label class="label">Klass</label>
                        <select name="class" class="input" onchange="this.form.submit()">
                            <option value="">Alla klasser</option>
                            <?php foreach ($classes as $c): ?>
                            <option value="<?= htmlspecialchars($c['category']) ?>" <?= $filterClass === $c['category'] ? 'selected' : '' ?>>
                                <?= htmlspecialchars($c['category']) ?>
                            </option>
                            <?php endforeach; ?>
                        </select>
                    </div>
                    <?php endif; ?>

                    <div class="form-group" style="flex: 1; min-width: 200px;">
                        <label class="label">Sök</label>
                        <input type="text" name="search" class="input"
                               value="<?= htmlspecialchars($search) ?>"
                               placeholder="Namn, e-post...">
                    </div>

                    <button type="submit" class="btn btn--secondary">
                        <i data-lucide="search"></i>
                        Sök
                    </button>
                </form>
            </div>
        </div>

        <!-- Registrations Table -->
        <div class="card">
            <div class="card-body gs-p-0">
                <?php if (empty($registrations)): ?>
                <div class="p-xl text-center text-secondary">
                    <i data-lucide="users" class="icon-xl mb-md" style="opacity: 0.3;"></i>
                    <p>Inga anmälningar hittades</p>
                </div>
                <?php else: ?>
                <div class="table-responsive">
                    <table class="table">
                        <thead>
                            <tr>
                                <th>Namn</th>
                                <th>Klass</th>
                                <th>Klubb</th>
                                <th>Order</th>
                                <th>Status</th>
                                <th>Anmäld</th>
                                <th></th>
                            </tr>
                        </thead>
                        <tbody>
                            <?php foreach ($registrations as $reg): ?>
                            <tr>
                                <td>
                                    <strong><?= htmlspecialchars($reg['first_name'] . ' ' . $reg['last_name']) ?></strong>
                                    <?php if ($reg['email']): ?>
                                    <div class="text-xs text-secondary"><?= htmlspecialchars($reg['email']) ?></div>
                                    <?php endif; ?>
                                </td>
                                <td>
                                    <span class="badge badge-secondary"><?= htmlspecialchars($reg['category']) ?></span>
                                </td>
                                <td>
                                    <?= htmlspecialchars($reg['club'] ?: '-') ?>
                                </td>
                                <td>
                                    <?php if ($reg['order_number']): ?>
                                    <code class="text-xs"><?= htmlspecialchars($reg['order_number']) ?></code>
                                    <?php if ($reg['order_payment_status'] === 'paid'): ?>
                                    <span class="badge badge-success badge-sm">Betald</span>
                                    <?php elseif ($reg['order_payment_status'] === 'pending'): ?>
                                    <span class="badge badge-warning badge-sm">Väntar</span>
                                    <?php endif; ?>
                                    <?php else: ?>
                                    <span class="text-secondary">-</span>
                                    <?php endif; ?>
                                </td>
                                <td>
                                    <?php
                                    $statusBadge = match($reg['status']) {
                                        'pending' => 'badge-warning',
                                        'confirmed' => 'badge-success',
                                        'cancelled' => 'badge-secondary',
                                        default => 'badge-secondary'
                                    };
                                    $statusLabel = match($reg['status']) {
                                        'pending' => 'Väntande',
                                        'confirmed' => 'Bekräftad',
                                        'cancelled' => 'Avbruten',
                                        default => $reg['status']
                                    };
                                    ?>
                                    <span class="badge <?= $statusBadge ?>"><?= $statusLabel ?></span>
                                </td>
                                <td>
                                    <span class="text-sm"><?= date('Y-m-d H:i', strtotime($reg['created_at'])) ?></span>
                                </td>
                                <td class="text-right">
                                    <?php if ($reg['status'] === 'pending'): ?>
                                    <div class="flex gap-xs justify-end">
                                        <form method="POST" style="display: inline;">
                                            <?= csrf_field() ?>
                                            <input type="hidden" name="action" value="confirm">
                                            <input type="hidden" name="registration_id" value="<?= $reg['id'] ?>">
                                            <button type="submit" class="btn btn--sm btn--success" title="Bekräfta">
                                                <i data-lucide="check"></i>
                                            </button>
                                        </form>
                                        <form method="POST" style="display: inline;">
                                            <?= csrf_field() ?>
                                            <input type="hidden" name="action" value="cancel">
                                            <input type="hidden" name="registration_id" value="<?= $reg['id'] ?>">
                                            <button type="submit" class="btn btn--sm btn--secondary" title="Avbryt"
                                                    onclick="return confirm('Avbryta denna anmälan?')">
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
.badge-sm {
    font-size: var(--text-xs);
    padding: 2px 6px;
}
</style>

<?php include __DIR__ . '/components/economy-layout-footer.php'; ?>
