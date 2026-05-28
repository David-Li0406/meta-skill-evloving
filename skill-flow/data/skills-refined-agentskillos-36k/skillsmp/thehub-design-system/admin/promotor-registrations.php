<?php
/**
 * Promotor Registrations - View and manage registrations for a specific event
 * Simplified interface for promotors without admin sidebar
 */

require_once __DIR__ . '/../config.php';

// Require at least promotor role
if (!isLoggedIn()) {
    redirect('/admin/login.php');
}

if (!hasRole('promotor')) {
    $_SESSION['flash_message'] = 'Du har inte behörighet till denna sida';
    $_SESSION['flash_type'] = 'error';
    redirect('/');
}

$db = getDB();
$currentUser = getCurrentAdmin();
$userId = $currentUser['id'] ?? 0;

// Get event ID
$eventId = isset($_GET['event_id']) ? intval($_GET['event_id']) : (isset($_GET['id']) ? intval($_GET['id']) : 0);

if ($eventId <= 0) {
    $_SESSION['flash_message'] = 'Ogiltigt event-ID';
    $_SESSION['flash_type'] = 'error';
    redirect('/admin/promotor.php');
}

// Check if promotor has access to this event (admins bypass this check)
if (!hasRole('admin')) {
    $hasAccess = $db->getRow("SELECT 1 FROM promotor_events WHERE user_id = ? AND event_id = ?", [$userId, $eventId]);
    if (!$hasAccess) {
        $_SESSION['flash_message'] = 'Du har inte behörighet till detta event';
        $_SESSION['flash_type'] = 'error';
        redirect('/admin/promotor.php');
    }
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
    redirect('/admin/promotor.php');
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

    } elseif ($action === 'bulk_confirm') {
        $ids = $_POST['selected_ids'] ?? [];
        if (!empty($ids)) {
            $placeholders = implode(',', array_fill(0, count($ids), '?'));
            $db->query("UPDATE event_registrations SET status = 'confirmed', confirmed_date = NOW() WHERE id IN ($placeholders) AND event_id = ?", array_merge($ids, [$eventId]));
            $message = count($ids) . ' anmälningar bekräftade!';
            $messageType = 'success';
        }
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
           o.order_number, o.payment_status as order_payment_status, o.total_amount
    FROM event_registrations er
    LEFT JOIN riders r ON er.rider_id = r.id
    LEFT JOIN orders o ON er.order_id = o.id
    {$whereClause}
    ORDER BY er.created_at DESC
    LIMIT 500
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

$pageTitle = 'Anmälningar - ' . $event['name'];
?>
<!DOCTYPE html>
<html lang="sv" data-theme="light">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title><?= h($pageTitle) ?> - TheHUB</title>
    <link rel="stylesheet" href="/assets/css/reset.css">
    <link rel="stylesheet" href="/assets/css/tokens.css">
    <link rel="stylesheet" href="/assets/css/theme.css">
    <link rel="stylesheet" href="/assets/css/components.css">
    <script src="https://unpkg.com/lucide@latest/dist/umd/lucide.min.js"></script>
    <style>
        .promotor-page {
            min-height: 100vh;
            background: var(--color-bg-page);
        }
        .promotor-header {
            background: var(--color-bg-surface);
            border-bottom: 1px solid var(--color-border);
            padding: var(--space-md) var(--space-lg);
        }
        .promotor-header-content {
            max-width: 1400px;
            margin: 0 auto;
            display: flex;
            justify-content: space-between;
            align-items: center;
            gap: var(--space-md);
            flex-wrap: wrap;
        }
        .promotor-header h1 {
            font-size: 1.25rem;
            font-weight: 600;
            color: var(--color-text-primary);
            display: flex;
            align-items: center;
            gap: var(--space-sm);
        }
        .promotor-header h1 i {
            color: var(--color-accent);
        }
        .event-badge {
            font-size: var(--text-sm);
            color: var(--color-text-secondary);
            font-weight: normal;
        }
        .promotor-content {
            max-width: 1400px;
            margin: 0 auto;
            padding: var(--space-lg);
        }
        .back-link {
            display: inline-flex;
            align-items: center;
            gap: var(--space-xs);
            color: var(--color-text-secondary);
            text-decoration: none;
            font-size: var(--text-sm);
        }
        .back-link:hover {
            color: var(--color-text-primary);
        }
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
            gap: var(--space-md);
            margin-bottom: var(--space-lg);
        }
        .stat-box {
            background: var(--color-bg-surface);
            border: 1px solid var(--color-border);
            border-radius: var(--radius-md);
            text-align: center;
            padding: var(--space-lg);
        }
        .stat-value {
            font-size: 2rem;
            font-weight: 700;
            color: var(--color-text);
        }
        .stat-value.pending { color: var(--color-warning); }
        .stat-value.success { color: var(--color-success); }
        .stat-value.muted { color: var(--color-text-secondary); }
        .stat-label {
            font-size: var(--text-sm);
            color: var(--color-text-secondary);
            margin-top: var(--space-xs);
        }
        .filters-card {
            background: var(--color-bg);
            border: 1px solid var(--color-border);
            border-radius: var(--radius-lg);
            padding: var(--space-md);
            margin-bottom: var(--space-lg);
        }
        .filters-form {
            display: flex;
            flex-wrap: wrap;
            gap: var(--space-md);
            align-items: flex-end;
        }
        .filter-group {
            display: flex;
            flex-direction: column;
            gap: var(--space-xs);
        }
        .filter-group label {
            font-size: var(--text-sm);
            font-weight: 500;
            color: var(--color-text-secondary);
        }
        .filter-group select,
        .filter-group input {
            padding: var(--space-sm) var(--space-md);
            border: 1px solid var(--color-border);
            border-radius: var(--radius-md);
            font-size: var(--text-sm);
            min-width: 150px;
        }
        .filter-group input[type="text"] {
            min-width: 200px;
        }
        .table-card {
            background: var(--color-bg);
            border: 1px solid var(--color-border);
            border-radius: var(--radius-lg);
            overflow: hidden;
        }
        .table-actions {
            padding: var(--space-md);
            border-bottom: 1px solid var(--color-border);
            display: flex;
            justify-content: space-between;
            align-items: center;
            gap: var(--space-md);
            flex-wrap: wrap;
        }
        .table-responsive {
            overflow-x: auto;
        }
        .table {
            width: 100%;
            border-collapse: collapse;
        }
        .table th,
        .table td {
            padding: var(--space-sm) var(--space-md);
            text-align: left;
            border-bottom: 1px solid var(--color-border);
        }
        .table th {
            background: var(--color-bg-subtle);
            font-weight: 600;
            font-size: var(--text-sm);
            color: var(--color-text-secondary);
        }
        .table tbody tr:hover {
            background: var(--color-bg-hover);
        }
        .badge {
            display: inline-flex;
            align-items: center;
            padding: 2px 8px;
            border-radius: var(--radius-full);
            font-size: var(--text-xs);
            font-weight: 500;
        }
        .badge-success {
            background: rgba(97, 206, 112, 0.15);
            color: var(--color-success);
        }
        .badge-warning {
            background: rgba(245, 158, 11, 0.15);
            color: var(--color-warning);
        }
        .badge-secondary {
            background: var(--color-bg-subtle);
            color: var(--color-text-secondary);
        }
        .badge-danger {
            background: rgba(239, 68, 68, 0.15);
            color: var(--color-danger);
        }
        .btn {
            display: inline-flex;
            align-items: center;
            gap: var(--space-xs);
            padding: var(--space-xs) var(--space-sm);
            border-radius: var(--radius-md);
            font-size: var(--text-sm);
            font-weight: 500;
            text-decoration: none;
            cursor: pointer;
            border: none;
            transition: all 0.15s ease;
        }
        .btn i { width: 14px; height: 14px; }
        .btn-sm { padding: 4px 8px; font-size: var(--text-xs); }
        .btn-primary {
            background: var(--color-accent);
            color: white;
        }
        .btn-primary:hover { opacity: 0.9; }
        .btn-secondary {
            background: var(--color-bg);
            color: var(--color-text);
            border: 1px solid var(--color-border);
        }
        .btn-secondary:hover { background: var(--color-bg-hover); }
        .btn-success {
            background: var(--color-success);
            color: white;
        }
        .btn-danger {
            background: transparent;
            color: var(--color-danger);
            border: 1px solid var(--color-danger);
        }
        .btn-danger:hover { background: rgba(239, 68, 68, 0.1); }
        .alert {
            padding: var(--space-md);
            border-radius: var(--radius-md);
            margin-bottom: var(--space-lg);
            display: flex;
            align-items: center;
            gap: var(--space-sm);
        }
        .alert i { width: 20px; height: 20px; }
        .alert-success {
            background: rgba(97, 206, 112, 0.15);
            color: var(--color-success);
            border: 1px solid rgba(97, 206, 112, 0.3);
        }
        .alert-error {
            background: rgba(239, 68, 68, 0.15);
            color: var(--color-danger);
            border: 1px solid rgba(239, 68, 68, 0.3);
        }
        .empty-state {
            text-align: center;
            padding: var(--space-2xl);
            color: var(--color-text-secondary);
        }
        .empty-state i {
            width: 48px;
            height: 48px;
            margin-bottom: var(--space-md);
            opacity: 0.5;
        }
        .text-xs { font-size: var(--text-xs); }
        .text-secondary { color: var(--color-text-secondary); }
        @media (max-width: 768px) {
            .promotor-content {
                padding: var(--space-md);
                padding-bottom: calc(var(--space-md) + 80px);
            }
            .stats-grid { grid-template-columns: repeat(2, 1fr); }
            .table th:nth-child(3),
            .table td:nth-child(3),
            .table th:nth-child(4),
            .table td:nth-child(4) { display: none; }
        }
        /* Bottom Navigation */
        .promotor-bottom-nav {
            position: fixed;
            bottom: 0;
            left: 0;
            right: 0;
            height: 64px;
            padding-bottom: env(safe-area-inset-bottom);
            background: var(--color-bg-surface);
            border-top: 1px solid var(--color-border);
            z-index: 100;
            display: flex;
            justify-content: center;
            align-items: center;
        }
        .promotor-bottom-nav-inner {
            display: flex;
            justify-content: space-around;
            align-items: center;
            width: 100%;
            max-width: 400px;
            height: 100%;
        }
        .promotor-nav-link {
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 4px;
            padding: var(--space-xs) var(--space-md);
            color: var(--color-text-secondary);
            font-size: var(--text-xs);
            font-weight: 500;
            text-decoration: none;
            min-width: 72px;
            transition: color 0.15s ease;
        }
        .promotor-nav-link:hover {
            color: var(--color-text-primary);
        }
        .promotor-nav-link.active {
            color: var(--color-accent);
        }
        .promotor-nav-link i {
            width: 24px;
            height: 24px;
        }
    </style>
</head>
<body class="promotor-page">

<header class="promotor-header">
    <div class="promotor-header-content">
        <h1>
            <i data-lucide="users"></i>
            Anmälningar
            <span class="event-badge">- <?= h($event['name']) ?></span>
        </h1>
        <a href="/admin/promotor.php" class="back-link">
            <i data-lucide="arrow-left"></i>
            Tillbaka till mina tävlingar
        </a>
    </div>
</header>

<main class="promotor-content">
    <?php if ($message): ?>
    <div class="alert alert-<?= $messageType === 'success' ? 'success' : 'error' ?>">
        <i data-lucide="<?= $messageType === 'success' ? 'check-circle' : 'alert-circle' ?>"></i>
        <?= h($message) ?>
    </div>
    <?php endif; ?>

    <!-- Stats -->
    <div class="stats-grid">
        <div class="stat-box">
            <div class="stat-value"><?= (int)($stats['total'] ?? 0) ?></div>
            <div class="stat-label">Totalt</div>
        </div>
        <div class="stat-box">
            <div class="stat-value pending"><?= (int)($stats['pending'] ?? 0) ?></div>
            <div class="stat-label">Väntande</div>
        </div>
        <div class="stat-box">
            <div class="stat-value success"><?= (int)($stats['confirmed'] ?? 0) ?></div>
            <div class="stat-label">Bekräftade</div>
        </div>
        <div class="stat-box">
            <div class="stat-value muted"><?= (int)($stats['cancelled'] ?? 0) ?></div>
            <div class="stat-label">Avbrutna</div>
        </div>
    </div>

    <!-- Filters -->
    <div class="filters-card">
        <form method="GET" class="filters-form">
            <input type="hidden" name="event_id" value="<?= $eventId ?>">

            <div class="filter-group">
                <label>Status</label>
                <select name="status" onchange="this.form.submit()">
                    <option value="all" <?= $filterStatus === 'all' ? 'selected' : '' ?>>Alla</option>
                    <option value="pending" <?= $filterStatus === 'pending' ? 'selected' : '' ?>>Väntande</option>
                    <option value="confirmed" <?= $filterStatus === 'confirmed' ? 'selected' : '' ?>>Bekräftade</option>
                    <option value="cancelled" <?= $filterStatus === 'cancelled' ? 'selected' : '' ?>>Avbrutna</option>
                </select>
            </div>

            <?php if (!empty($classes)): ?>
            <div class="filter-group">
                <label>Klass</label>
                <select name="class" onchange="this.form.submit()">
                    <option value="">Alla klasser</option>
                    <?php foreach ($classes as $c): ?>
                    <option value="<?= h($c['category']) ?>" <?= $filterClass === $c['category'] ? 'selected' : '' ?>>
                        <?= h($c['category']) ?>
                    </option>
                    <?php endforeach; ?>
                </select>
            </div>
            <?php endif; ?>

            <div class="filter-group" style="flex: 1;">
                <label>Sök</label>
                <input type="text" name="search" value="<?= h($search) ?>" placeholder="Namn, e-post...">
            </div>

            <button type="submit" class="btn btn-secondary">
                <i data-lucide="search"></i>
                Sök
            </button>
        </form>
    </div>

    <!-- Registrations Table -->
    <div class="table-card">
        <?php if (empty($registrations)): ?>
        <div class="empty-state">
            <i data-lucide="users"></i>
            <h3>Inga anmälningar</h3>
            <p>Det finns inga anmälningar som matchar dina filter.</p>
        </div>
        <?php else: ?>
        <form method="POST" id="bulkForm">
            <?= csrf_field() ?>
            <input type="hidden" name="action" value="bulk_confirm" id="bulkAction">

            <div class="table-actions">
                <div>
                    <label style="display: flex; align-items: center; gap: var(--space-xs); cursor: pointer;">
                        <input type="checkbox" id="selectAll" onchange="toggleAll(this)">
                        <span class="text-xs text-secondary">Markera alla</span>
                    </label>
                </div>
                <div style="display: flex; gap: var(--space-sm);">
                    <button type="submit" class="btn btn-success btn-sm" onclick="return confirmBulk()">
                        <i data-lucide="check"></i>
                        Bekräfta markerade
                    </button>
                    <a href="/admin/promotor-payments.php?event_id=<?= $eventId ?>" class="btn btn-secondary btn-sm">
                        <i data-lucide="credit-card"></i>
                        Hantera betalningar
                    </a>
                </div>
            </div>

            <div class="table-responsive">
                <table class="table">
                    <thead>
                        <tr>
                            <th style="width: 40px;"></th>
                            <th>Namn</th>
                            <th>Klass</th>
                            <th>Klubb</th>
                            <th>Betalning</th>
                            <th>Status</th>
                            <th>Anmäld</th>
                            <th style="width: 100px;"></th>
                        </tr>
                    </thead>
                    <tbody>
                        <?php foreach ($registrations as $reg): ?>
                        <tr>
                            <td>
                                <?php if ($reg['status'] === 'pending'): ?>
                                <input type="checkbox" name="selected_ids[]" value="<?= $reg['id'] ?>" class="row-checkbox">
                                <?php endif; ?>
                            </td>
                            <td>
                                <strong><?= h($reg['first_name'] . ' ' . $reg['last_name']) ?></strong>
                                <?php if ($reg['email']): ?>
                                <div class="text-xs text-secondary"><?= h($reg['email']) ?></div>
                                <?php endif; ?>
                            </td>
                            <td>
                                <span class="badge badge-secondary"><?= h($reg['category'] ?: '-') ?></span>
                            </td>
                            <td class="text-secondary">
                                <?= h($reg['club'] ?: '-') ?>
                            </td>
                            <td>
                                <?php if ($reg['order_payment_status'] === 'paid'): ?>
                                <span class="badge badge-success">
                                    <i data-lucide="check" style="width:12px;height:12px;margin-right:2px;"></i>
                                    Betald
                                </span>
                                <?php elseif ($reg['order_payment_status'] === 'pending'): ?>
                                <span class="badge badge-warning">Väntar</span>
                                <?php else: ?>
                                <span class="text-secondary">-</span>
                                <?php endif; ?>
                            </td>
                            <td>
                                <?php if ($reg['status'] === 'confirmed'): ?>
                                <span class="badge badge-success">Bekräftad</span>
                                <?php elseif ($reg['status'] === 'pending'): ?>
                                <span class="badge badge-warning">Väntande</span>
                                <?php elseif ($reg['status'] === 'cancelled'): ?>
                                <span class="badge badge-danger">Avbruten</span>
                                <?php endif; ?>
                            </td>
                            <td class="text-xs text-secondary">
                                <?= date('j M H:i', strtotime($reg['created_at'])) ?>
                            </td>
                            <td>
                                <?php if ($reg['status'] === 'pending'): ?>
                                <form method="POST" style="display: inline;">
                                    <?= csrf_field() ?>
                                    <input type="hidden" name="registration_id" value="<?= $reg['id'] ?>">
                                    <input type="hidden" name="action" value="confirm">
                                    <button type="submit" class="btn btn-success btn-sm" title="Bekräfta">
                                        <i data-lucide="check"></i>
                                    </button>
                                </form>
                                <form method="POST" style="display: inline;">
                                    <?= csrf_field() ?>
                                    <input type="hidden" name="registration_id" value="<?= $reg['id'] ?>">
                                    <input type="hidden" name="action" value="cancel">
                                    <button type="submit" class="btn btn-danger btn-sm" title="Avbryt" onclick="return confirm('Vill du avbryta denna anmälan?')">
                                        <i data-lucide="x"></i>
                                    </button>
                                </form>
                                <?php endif; ?>
                            </td>
                        </tr>
                        <?php endforeach; ?>
                    </tbody>
                </table>
            </div>
        </form>
        <?php endif; ?>
    </div>
</main>

<!-- Bottom Navigation -->
<nav class="promotor-bottom-nav">
    <div class="promotor-bottom-nav-inner">
        <a href="/" class="promotor-nav-link">
            <i data-lucide="home"></i>
            <span>Hem</span>
        </a>
        <a href="/admin/promotor.php" class="promotor-nav-link active">
            <i data-lucide="calendar-check"></i>
            <span>Tävlingar</span>
        </a>
    </div>
</nav>

<script>
    lucide.createIcons();

    function toggleAll(checkbox) {
        document.querySelectorAll('.row-checkbox').forEach(cb => {
            cb.checked = checkbox.checked;
        });
    }

    function confirmBulk() {
        const checked = document.querySelectorAll('.row-checkbox:checked');
        if (checked.length === 0) {
            alert('Välj minst en anmälan att bekräfta');
            return false;
        }
        return confirm('Bekräfta ' + checked.length + ' anmälningar?');
    }
</script>
</body>
</html>
