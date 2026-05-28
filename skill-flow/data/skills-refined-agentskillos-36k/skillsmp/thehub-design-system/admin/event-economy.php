<?php
/**
 * EVENT ECONOMY - Översikt
 * Dashboard för event-specifik ekonomi
 */

// Validera event_id
$event_id = isset($_GET['event_id']) ? (int)$_GET['event_id'] : 0;

if (!$event_id) {
    header('Location: /admin/events.php');
    exit;
}

// Inkludera layout
$economy_page_title = 'Ekonomi Översikt';
include __DIR__ . '/components/economy-layout.php';

// Hämta event-data
$event = null;
$stats = [
    'total_registrations' => 0,
    'confirmed_registrations' => 0,
    'pending_registrations' => 0,
    'total_orders' => 0,
    'paid_orders' => 0,
    'pending_orders' => 0,
    'total_revenue' => 0,
    'pending_revenue' => 0
];

try {
    // Hämta event
    $stmt = $pdo->prepare("SELECT * FROM events WHERE id = ?");
    $stmt->execute([$event_id]);
    $event = $stmt->fetch(PDO::FETCH_ASSOC);

    if (!$event) {
        echo '<div class="alert alert-error">Event hittades inte.</div>';
        include __DIR__ . '/components/economy-layout-footer.php';
        exit;
    }

    // Hämta registreringsstatistik
    $stmt = $pdo->prepare("
        SELECT
            COUNT(*) as total,
            SUM(CASE WHEN status = 'confirmed' THEN 1 ELSE 0 END) as confirmed,
            SUM(CASE WHEN status = 'pending' THEN 1 ELSE 0 END) as pending
        FROM event_registrations
        WHERE event_id = ?
    ");
    $stmt->execute([$event_id]);
    $reg_stats = $stmt->fetch(PDO::FETCH_ASSOC);

    $stats['total_registrations'] = (int)($reg_stats['total'] ?? 0);
    $stats['confirmed_registrations'] = (int)($reg_stats['confirmed'] ?? 0);
    $stats['pending_registrations'] = (int)($reg_stats['pending'] ?? 0);

    // Hämta orderstatistik
    $stmt = $pdo->prepare("
        SELECT
            COUNT(*) as total,
            SUM(CASE WHEN payment_status = 'paid' THEN 1 ELSE 0 END) as paid,
            SUM(CASE WHEN payment_status = 'pending' THEN 1 ELSE 0 END) as pending,
            SUM(CASE WHEN payment_status = 'paid' THEN total_amount ELSE 0 END) as revenue,
            SUM(CASE WHEN payment_status = 'pending' THEN total_amount ELSE 0 END) as pending_revenue
        FROM orders
        WHERE event_id = ?
    ");
    $stmt->execute([$event_id]);
    $order_stats = $stmt->fetch(PDO::FETCH_ASSOC);

    $stats['total_orders'] = (int)($order_stats['total'] ?? 0);
    $stats['paid_orders'] = (int)($order_stats['paid'] ?? 0);
    $stats['pending_orders'] = (int)($order_stats['pending'] ?? 0);
    $stats['total_revenue'] = (float)($order_stats['revenue'] ?? 0);
    $stats['pending_revenue'] = (float)($order_stats['pending_revenue'] ?? 0);

} catch (Exception $e) {
    // Tabeller kanske inte existerar än
}
?>

<!-- Statistik-kort -->
<div class="grid grid-4">
    <!-- Anmälningar -->
    <div class="card">
        <div class="card-body">
            <div class="stat-label">Anmälningar</div>
            <div class="stat-value"><?= $stats['total_registrations'] ?></div>
            <div class="stat-detail">
                <span class="text-success"><?= $stats['confirmed_registrations'] ?> bekräftade</span>
                <?php if ($stats['pending_registrations'] > 0): ?>
                    <span class="text-warning"> · <?= $stats['pending_registrations'] ?> väntande</span>
                <?php endif; ?>
            </div>
        </div>
    </div>

    <!-- Ordrar -->
    <div class="card">
        <div class="card-body">
            <div class="stat-label">Ordrar</div>
            <div class="stat-value"><?= $stats['total_orders'] ?></div>
            <div class="stat-detail">
                <span class="text-success"><?= $stats['paid_orders'] ?> betalda</span>
                <?php if ($stats['pending_orders'] > 0): ?>
                    <span class="text-warning"> · <?= $stats['pending_orders'] ?> väntande</span>
                <?php endif; ?>
            </div>
        </div>
    </div>

    <!-- Intäkter -->
    <div class="card">
        <div class="card-body">
            <div class="stat-label">Intäkter</div>
            <div class="stat-value"><?= number_format($stats['total_revenue'], 0, ',', ' ') ?> kr</div>
            <?php if ($stats['pending_revenue'] > 0): ?>
                <div class="stat-detail text-warning">
                    +<?= number_format($stats['pending_revenue'], 0, ',', ' ') ?> kr väntande
                </div>
            <?php endif; ?>
        </div>
    </div>

    <!-- Status -->
    <div class="card">
        <div class="card-body">
            <div class="stat-label">Biljettförsäljning</div>
            <?php if (!empty($event['ticketing_enabled'])): ?>
                <div class="stat-value text-success">
                    <i data-lucide="check-circle" style="width:24px;height:24px;display:inline;vertical-align:middle;"></i>
                    Aktiv
                </div>
            <?php else: ?>
                <div class="stat-value text-muted">
                    <i data-lucide="x-circle" style="width:24px;height:24px;display:inline;vertical-align:middle;"></i>
                    Inaktiv
                </div>
            <?php endif; ?>
        </div>
    </div>
</div>

<!-- Snabbåtgärder -->
<div class="card" class="mt-lg">
    <div class="card-header">
        <h3>Snabbåtgärder</h3>
    </div>
    <div class="card-body">
        <div class="grid grid-3">
            <a href="/admin/event-registrations.php?event_id=<?= $event_id ?>" class="btn btn-secondary">
                <i data-lucide="users"></i>
                Hantera anmälningar
            </a>
            <a href="/admin/event-orders.php?event_id=<?= $event_id ?>" class="btn btn-secondary">
                <i data-lucide="receipt"></i>
                Visa ordrar
            </a>
            <a href="/admin/event-payment.php?event_id=<?= $event_id ?>" class="btn btn-secondary">
                <i data-lucide="credit-card"></i>
                Betalningsinställningar
            </a>
        </div>
    </div>
</div>

<!-- Event-info -->
<div class="card" class="mt-lg">
    <div class="card-header">
        <h3>Event-information</h3>
    </div>
    <div class="card-body">
        <table class="table">
            <tr>
                <th style="width:200px;">Namn</th>
                <td><?= htmlspecialchars($event['name'] ?? '-') ?></td>
            </tr>
            <tr>
                <th>Datum</th>
                <td><?= $event['date'] ? date('Y-m-d', strtotime($event['date'])) : '-' ?></td>
            </tr>
            <tr>
                <th>Anmälningsavgift</th>
                <td><?= isset($event['entry_fee']) ? number_format($event['entry_fee'], 0, ',', ' ') . ' kr' : 'Ej satt' ?></td>
            </tr>
            <tr>
                <th>Sista anmälningsdag</th>
                <td><?= !empty($event['registration_deadline']) ? date('Y-m-d', strtotime($event['registration_deadline'])) : 'Ej satt' ?></td>
            </tr>
        </table>
    </div>
</div>

<style>
.stat-label {
    font-size: var(--text-xs);
    font-weight: var(--weight-medium);
    color: var(--color-text-secondary);
    text-transform: uppercase;
    letter-spacing: 0.05em;
    margin-bottom: var(--space-xs);
}

.stat-value {
    font-size: var(--text-2xl);
    font-weight: var(--weight-bold);
    color: var(--color-text-primary);
    line-height: 1.2;
}

.stat-detail {
    font-size: var(--text-sm);
    color: var(--color-text-secondary);
    margin-top: var(--space-xs);
}

.text-success { color: var(--color-success); }
.text-warning { color: var(--color-warning); }
.text-muted { color: var(--color-text-secondary); }

.btn i[data-lucide] {
    width: 16px;
    height: 16px;
    margin-right: var(--space-xs);
}
</style>

<?php include __DIR__ . '/components/economy-layout-footer.php'; ?>
