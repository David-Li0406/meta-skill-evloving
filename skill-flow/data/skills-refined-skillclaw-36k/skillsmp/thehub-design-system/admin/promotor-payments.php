<?php
/**
 * Promotor Payments - Manage payments for a specific event
 * Manual approval and CSV import support for Swish payments
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
$csvResults = null;

// Handle actions
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    checkCsrf();

    $action = $_POST['action'] ?? '';

    // Manual payment confirmation
    if ($action === 'mark_paid') {
        $orderId = intval($_POST['order_id'] ?? 0);
        if ($orderId) {
            $db->update('orders', [
                'payment_status' => 'paid',
                'payment_method' => 'manual',
                'updated_at' => date('Y-m-d H:i:s')
            ], 'id = ? AND event_id = ?', [$orderId, $eventId]);

            // Also confirm the registration
            $db->query("UPDATE event_registrations SET status = 'confirmed', confirmed_date = NOW() WHERE order_id = ?", [$orderId]);

            $message = 'Betalning markerad som betald!';
            $messageType = 'success';
        }

    // Bulk manual confirmation
    } elseif ($action === 'bulk_mark_paid') {
        $ids = $_POST['selected_ids'] ?? [];
        if (!empty($ids)) {
            $placeholders = implode(',', array_fill(0, count($ids), '?'));
            $db->query("UPDATE orders SET payment_status = 'paid', payment_method = 'manual', updated_at = NOW() WHERE id IN ($placeholders) AND event_id = ?", array_merge($ids, [$eventId]));

            // Also confirm the registrations
            $db->query("UPDATE event_registrations SET status = 'confirmed', confirmed_date = NOW() WHERE order_id IN ($placeholders)", $ids);

            $message = count($ids) . ' betalningar markerade som betalda!';
            $messageType = 'success';
        }

    // CSV Import
    } elseif ($action === 'import_csv' && isset($_FILES['csv_file'])) {
        $file = $_FILES['csv_file'];

        if ($file['error'] === UPLOAD_ERR_OK && $file['size'] > 0) {
            $csvResults = processSwishCsv($file['tmp_name'], $eventId, $db);
            if ($csvResults['matched'] > 0) {
                $message = "CSV-import klar! {$csvResults['matched']} av {$csvResults['total']} betalningar matchade.";
                $messageType = 'success';
            } else {
                $message = "Inga betalningar kunde matchas. Kontrollera att CSV-filen innehåller rätt referensnummer.";
                $messageType = 'warning';
            }
        } else {
            $message = 'Kunde inte läsa CSV-filen. Kontrollera att filen är giltig.';
            $messageType = 'error';
        }
    }
}

/**
 * Process Swish CSV file and match payments
 */
function processSwishCsv($filepath, $eventId, $db) {
    $results = [
        'total' => 0,
        'matched' => 0,
        'unmatched' => [],
        'errors' => []
    ];

    $handle = fopen($filepath, 'r');
    if (!$handle) {
        $results['errors'][] = 'Kunde inte öppna filen';
        return $results;
    }

    // Read header row
    $header = fgetcsv($handle, 0, ';');
    if (!$header) {
        $results['errors'][] = 'Kunde inte läsa header';
        fclose($handle);
        return $results;
    }

    // Find relevant columns (Swedish Swish CSV format)
    $colMap = [];
    foreach ($header as $idx => $col) {
        $col = trim(strtolower($col));
        if (strpos($col, 'meddelande') !== false || strpos($col, 'message') !== false) {
            $colMap['message'] = $idx;
        } elseif (strpos($col, 'belopp') !== false || strpos($col, 'amount') !== false) {
            $colMap['amount'] = $idx;
        } elseif (strpos($col, 'datum') !== false || strpos($col, 'date') !== false) {
            $colMap['date'] = $idx;
        } elseif (strpos($col, 'avsändare') !== false || strpos($col, 'sender') !== false || strpos($col, 'från') !== false) {
            $colMap['sender'] = $idx;
        }
    }

    // Process rows
    while (($row = fgetcsv($handle, 0, ';')) !== false) {
        $results['total']++;

        $message = isset($colMap['message']) ? trim($row[$colMap['message']] ?? '') : '';
        $amount = isset($colMap['amount']) ? floatval(str_replace([' ', ','], ['', '.'], $row[$colMap['amount']] ?? '0')) : 0;

        if (empty($message) || $amount <= 0) {
            continue;
        }

        // Try to find matching order by:
        // 1. Order number in message
        // 2. Payment reference in message
        // 3. Exact message match

        $order = null;

        // Look for order number pattern (e.g., "ORD-123" or just numbers)
        if (preg_match('/ORD-?(\d+)/i', $message, $matches)) {
            $order = $db->getRow("SELECT * FROM orders WHERE event_id = ? AND (order_number LIKE ? OR id = ?) AND payment_status = 'pending'",
                [$eventId, '%' . $matches[1] . '%', $matches[1]]);
        }

        // Try payment reference
        if (!$order) {
            $order = $db->getRow("SELECT * FROM orders WHERE event_id = ? AND payment_reference = ? AND payment_status = 'pending'",
                [$eventId, $message]);
        }

        // Try partial match on reference
        if (!$order && strlen($message) >= 4) {
            $order = $db->getRow("SELECT * FROM orders WHERE event_id = ? AND payment_reference LIKE ? AND payment_status = 'pending'",
                [$eventId, '%' . $message . '%']);
        }

        if ($order) {
            // Mark as paid
            $db->update('orders', [
                'payment_status' => 'paid',
                'payment_method' => 'swish_csv',
                'updated_at' => date('Y-m-d H:i:s')
            ], 'id = ?', [$order['id']]);

            // Confirm registration
            $db->query("UPDATE event_registrations SET status = 'confirmed', confirmed_date = NOW() WHERE order_id = ?", [$order['id']]);

            $results['matched']++;
        } else {
            $results['unmatched'][] = [
                'message' => $message,
                'amount' => $amount
            ];
        }
    }

    fclose($handle);
    return $results;
}

// Filter parameters
$filterStatus = $_GET['status'] ?? 'all';
$search = trim($_GET['search'] ?? '');

// Build query for orders
$whereConditions = ["o.event_id = ?"];
$params = [$eventId];

if ($filterStatus && $filterStatus !== 'all') {
    $whereConditions[] = "o.payment_status = ?";
    $params[] = $filterStatus;
}

if ($search) {
    $whereConditions[] = "(er.first_name LIKE ? OR er.last_name LIKE ? OR o.order_number LIKE ? OR o.payment_reference LIKE ?)";
    $searchTerm = "%{$search}%";
    $params[] = $searchTerm;
    $params[] = $searchTerm;
    $params[] = $searchTerm;
    $params[] = $searchTerm;
}

$whereClause = 'WHERE ' . implode(' AND ', $whereConditions);

// Get orders with registration info
$orders = $db->getAll("
    SELECT o.*,
           er.first_name, er.last_name, er.category, er.club,
           r.email, r.phone
    FROM orders o
    LEFT JOIN event_registrations er ON er.order_id = o.id
    LEFT JOIN riders r ON er.rider_id = r.id
    {$whereClause}
    ORDER BY o.created_at DESC
    LIMIT 500
", $params);

// Get stats
$stats = $db->getRow("
    SELECT
        COUNT(*) as total,
        SUM(CASE WHEN payment_status = 'pending' THEN 1 ELSE 0 END) as pending,
        SUM(CASE WHEN payment_status = 'paid' THEN 1 ELSE 0 END) as paid,
        COALESCE(SUM(CASE WHEN payment_status = 'paid' THEN total_amount ELSE 0 END), 0) as total_paid_amount,
        COALESCE(SUM(CASE WHEN payment_status = 'pending' THEN total_amount ELSE 0 END), 0) as total_pending_amount
    FROM orders
    WHERE event_id = ?
", [$eventId]);

$pageTitle = 'Betalningar - ' . $event['name'];
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
            grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
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
            font-size: 1.75rem;
            font-weight: 700;
            color: var(--color-text);
        }
        .stat-value.pending { color: var(--color-warning); }
        .stat-value.success { color: var(--color-success); }
        .stat-label {
            font-size: var(--text-sm);
            color: var(--color-text-secondary);
            margin-top: var(--space-xs);
        }
        .card {
            background: var(--color-bg);
            border: 1px solid var(--color-border);
            border-radius: var(--radius-lg);
            margin-bottom: var(--space-lg);
        }
        .card-header {
            padding: var(--space-md) var(--space-lg);
            border-bottom: 1px solid var(--color-border);
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .card-header h2 {
            font-size: 1rem;
            font-weight: 600;
            display: flex;
            align-items: center;
            gap: var(--space-sm);
        }
        .card-header h2 i {
            color: var(--color-accent);
        }
        .card-body {
            padding: var(--space-lg);
        }
        .import-form {
            display: flex;
            flex-wrap: wrap;
            gap: var(--space-md);
            align-items: flex-end;
        }
        .import-form .file-input-wrapper {
            flex: 1;
            min-width: 200px;
        }
        .import-form label {
            display: block;
            font-size: var(--text-sm);
            font-weight: 500;
            color: var(--color-text-secondary);
            margin-bottom: var(--space-xs);
        }
        .import-form input[type="file"] {
            display: block;
            width: 100%;
            padding: var(--space-sm);
            border: 2px dashed var(--color-border);
            border-radius: var(--radius-md);
            background: var(--color-bg-subtle);
            cursor: pointer;
        }
        .import-form input[type="file"]:hover {
            border-color: var(--color-accent);
        }
        .import-help {
            font-size: var(--text-xs);
            color: var(--color-text-secondary);
            margin-top: var(--space-sm);
        }
        .filters-form {
            display: flex;
            flex-wrap: wrap;
            gap: var(--space-md);
            align-items: flex-end;
            padding: var(--space-md) var(--space-lg);
            border-bottom: 1px solid var(--color-border);
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
        .table-actions {
            padding: var(--space-md) var(--space-lg);
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
        .btn-secondary {
            background: var(--color-bg);
            color: var(--color-text);
            border: 1px solid var(--color-border);
        }
        .btn-success {
            background: var(--color-success);
            color: white;
        }
        .alert {
            padding: var(--space-md);
            border-radius: var(--radius-md);
            margin-bottom: var(--space-lg);
            display: flex;
            align-items: flex-start;
            gap: var(--space-sm);
        }
        .alert i { width: 20px; height: 20px; flex-shrink: 0; margin-top: 2px; }
        .alert-success {
            background: rgba(97, 206, 112, 0.15);
            color: var(--color-success);
            border: 1px solid rgba(97, 206, 112, 0.3);
        }
        .alert-warning {
            background: rgba(245, 158, 11, 0.15);
            color: #92400e;
            border: 1px solid rgba(245, 158, 11, 0.3);
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
        .unmatched-list {
            margin-top: var(--space-md);
            padding: var(--space-md);
            background: var(--color-bg-subtle);
            border-radius: var(--radius-md);
            font-size: var(--text-sm);
        }
        .unmatched-list h4 {
            font-weight: 600;
            margin-bottom: var(--space-sm);
        }
        .unmatched-list ul {
            list-style: none;
            padding: 0;
        }
        .unmatched-list li {
            padding: var(--space-xs) 0;
            border-bottom: 1px solid var(--color-border);
        }
        .unmatched-list li:last-child {
            border-bottom: none;
        }
        .text-xs { font-size: var(--text-xs); }
        .text-secondary { color: var(--color-text-secondary); }
        @media (max-width: 768px) {
            .promotor-content {
                padding: var(--space-md);
                padding-bottom: calc(var(--space-md) + 80px);
            }
            .stats-grid { grid-template-columns: repeat(2, 1fr); }
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
            <i data-lucide="credit-card"></i>
            Betalningar
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
    <div class="alert alert-<?= $messageType === 'success' ? 'success' : ($messageType === 'warning' ? 'warning' : 'error') ?>">
        <i data-lucide="<?= $messageType === 'success' ? 'check-circle' : ($messageType === 'warning' ? 'alert-triangle' : 'alert-circle') ?>"></i>
        <div>
            <?= h($message) ?>
            <?php if ($csvResults && !empty($csvResults['unmatched'])): ?>
            <div class="unmatched-list">
                <h4>Kunde inte matcha följande betalningar:</h4>
                <ul>
                    <?php foreach (array_slice($csvResults['unmatched'], 0, 10) as $unmatched): ?>
                    <li>
                        <strong><?= h($unmatched['message']) ?></strong>
                        - <?= number_format($unmatched['amount'], 2, ',', ' ') ?> kr
                    </li>
                    <?php endforeach; ?>
                    <?php if (count($csvResults['unmatched']) > 10): ?>
                    <li><em>... och <?= count($csvResults['unmatched']) - 10 ?> till</em></li>
                    <?php endif; ?>
                </ul>
            </div>
            <?php endif; ?>
        </div>
    </div>
    <?php endif; ?>

    <!-- Stats -->
    <div class="stats-grid">
        <div class="stat-box">
            <div class="stat-value"><?= (int)($stats['total'] ?? 0) ?></div>
            <div class="stat-label">Totalt ordrar</div>
        </div>
        <div class="stat-box">
            <div class="stat-value pending"><?= (int)($stats['pending'] ?? 0) ?></div>
            <div class="stat-label">Väntar på betalning</div>
        </div>
        <div class="stat-box">
            <div class="stat-value success"><?= (int)($stats['paid'] ?? 0) ?></div>
            <div class="stat-label">Betalda</div>
        </div>
        <div class="stat-box">
            <div class="stat-value success"><?= number_format($stats['total_paid_amount'] ?? 0, 0, ',', ' ') ?> kr</div>
            <div class="stat-label">Totalt inbetalt</div>
        </div>
    </div>

    <!-- CSV Import -->
    <div class="card">
        <div class="card-header">
            <h2>
                <i data-lucide="upload"></i>
                Importera Swish-betalningar
            </h2>
        </div>
        <div class="card-body">
            <form method="POST" enctype="multipart/form-data" class="import-form">
                <?= csrf_field() ?>
                <input type="hidden" name="action" value="import_csv">

                <div class="file-input-wrapper">
                    <label for="csv_file">CSV-fil från Swish/Banken</label>
                    <input type="file" name="csv_file" id="csv_file" accept=".csv,.txt" required>
                    <p class="import-help">
                        Ladda upp en CSV-fil exporterad från Swish eller din bank.
                        Systemet matchar betalningar automatiskt baserat på meddelandefältet.
                    </p>
                </div>

                <button type="submit" class="btn btn-primary">
                    <i data-lucide="upload"></i>
                    Importera
                </button>
            </form>
        </div>
    </div>

    <!-- Orders Table -->
    <div class="card">
        <div class="card-header">
            <h2>
                <i data-lucide="list"></i>
                Ordrar
            </h2>
            <a href="/admin/promotor-registrations.php?event_id=<?= $eventId ?>" class="btn btn-secondary btn-sm">
                <i data-lucide="users"></i>
                Visa anmälningar
            </a>
        </div>

        <form method="GET" class="filters-form">
            <input type="hidden" name="event_id" value="<?= $eventId ?>">

            <div class="filter-group">
                <label>Status</label>
                <select name="status" onchange="this.form.submit()">
                    <option value="all" <?= $filterStatus === 'all' ? 'selected' : '' ?>>Alla</option>
                    <option value="pending" <?= $filterStatus === 'pending' ? 'selected' : '' ?>>Väntar</option>
                    <option value="paid" <?= $filterStatus === 'paid' ? 'selected' : '' ?>>Betalda</option>
                </select>
            </div>

            <div class="filter-group" style="flex: 1;">
                <label>Sök</label>
                <input type="text" name="search" value="<?= h($search) ?>" placeholder="Namn, ordernummer...">
            </div>

            <button type="submit" class="btn btn-secondary">
                <i data-lucide="search"></i>
                Sök
            </button>
        </form>

        <?php if (empty($orders)): ?>
        <div class="empty-state">
            <i data-lucide="credit-card"></i>
            <h3>Inga ordrar</h3>
            <p>Det finns inga ordrar för detta event ännu.</p>
        </div>
        <?php else: ?>
        <form method="POST" id="bulkForm">
            <?= csrf_field() ?>
            <input type="hidden" name="action" value="bulk_mark_paid">

            <div class="table-actions">
                <div>
                    <label style="display: flex; align-items: center; gap: var(--space-xs); cursor: pointer;">
                        <input type="checkbox" id="selectAll" onchange="toggleAll(this)">
                        <span class="text-xs text-secondary">Markera alla</span>
                    </label>
                </div>
                <button type="submit" class="btn btn-success btn-sm" onclick="return confirmBulk()">
                    <i data-lucide="check"></i>
                    Markera som betalda
                </button>
            </div>

            <div class="table-responsive">
                <table class="table">
                    <thead>
                        <tr>
                            <th style="width: 40px;"></th>
                            <th>Order</th>
                            <th>Kund</th>
                            <th>Belopp</th>
                            <th>Referens</th>
                            <th>Status</th>
                            <th>Datum</th>
                            <th style="width: 80px;"></th>
                        </tr>
                    </thead>
                    <tbody>
                        <?php foreach ($orders as $order): ?>
                        <tr>
                            <td>
                                <?php if ($order['payment_status'] === 'pending'): ?>
                                <input type="checkbox" name="selected_ids[]" value="<?= $order['id'] ?>" class="row-checkbox">
                                <?php endif; ?>
                            </td>
                            <td>
                                <code class="text-xs"><?= h($order['order_number'] ?: '#' . $order['id']) ?></code>
                            </td>
                            <td>
                                <strong><?= h(($order['first_name'] ?? '') . ' ' . ($order['last_name'] ?? '')) ?></strong>
                                <?php if ($order['email']): ?>
                                <div class="text-xs text-secondary"><?= h($order['email']) ?></div>
                                <?php endif; ?>
                            </td>
                            <td>
                                <strong><?= number_format($order['total_amount'] ?? 0, 0, ',', ' ') ?> kr</strong>
                            </td>
                            <td class="text-xs text-secondary">
                                <?= h($order['payment_reference'] ?: '-') ?>
                            </td>
                            <td>
                                <?php if ($order['payment_status'] === 'paid'): ?>
                                <span class="badge badge-success">
                                    <i data-lucide="check" style="width:12px;height:12px;margin-right:2px;"></i>
                                    Betald
                                </span>
                                <?php elseif ($order['payment_status'] === 'pending'): ?>
                                <span class="badge badge-warning">Väntar</span>
                                <?php else: ?>
                                <span class="badge badge-secondary"><?= h($order['payment_status']) ?></span>
                                <?php endif; ?>
                            </td>
                            <td class="text-xs text-secondary">
                                <?= date('j M H:i', strtotime($order['created_at'])) ?>
                            </td>
                            <td>
                                <?php if ($order['payment_status'] === 'pending'): ?>
                                <form method="POST" style="display: inline;">
                                    <?= csrf_field() ?>
                                    <input type="hidden" name="order_id" value="<?= $order['id'] ?>">
                                    <input type="hidden" name="action" value="mark_paid">
                                    <button type="submit" class="btn btn-success btn-sm" title="Markera som betald">
                                        <i data-lucide="check"></i>
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
            alert('Välj minst en order att markera som betald');
            return false;
        }
        return confirm('Markera ' + checked.length + ' ordrar som betalda?');
    }
</script>
</body>
</html>
