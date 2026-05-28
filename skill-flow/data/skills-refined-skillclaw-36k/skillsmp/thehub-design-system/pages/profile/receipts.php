<?php
/**
 * TheHUB V1.0 - My Receipts
 */

$currentUser = hub_current_user();
if (!$currentUser) {
    header('Location: /profile/login');
    exit;
}

$pdo = hub_db();

// Get payment history (would be from WooCommerce in production)
// For now, show registrations with payment status (if table exists)
$payments = [];
$totalSpent = 0;

try {
    $tableCheck = $pdo->query("SHOW TABLES LIKE 'event_registrations'");
    if ($tableCheck->rowCount() > 0) {
        $stmt = $pdo->prepare("
            SELECT r.*, e.name as event_name, e.date as event_date,
                   cls.display_name as class_name, epr.base_price as price
            FROM event_registrations r
            JOIN events e ON r.event_id = e.id
            LEFT JOIN classes cls ON r.class_id = cls.id
            LEFT JOIN event_pricing_rules epr ON r.event_id = epr.event_id AND r.class_id = epr.class_id
            WHERE r.rider_id = ? AND r.status = 'confirmed'
            ORDER BY r.registration_date DESC
        ");
        $stmt->execute([$currentUser['id']]);
        $payments = $stmt->fetchAll(PDO::FETCH_ASSOC);
        $totalSpent = array_sum(array_column($payments, 'price'));
    }
} catch (PDOException $e) {
    $payments = [];
    $totalSpent = 0;
}
?>

<div class="page-header">
    <nav class="breadcrumb">
        <a href="/profile">Min Sida</a>
        <span class="breadcrumb-sep">›</span>
        <span>Kvitton</span>
    </nav>
    <h1 class="page-title">
        <i data-lucide="receipt" class="page-icon"></i>
        Kvitton
    </h1>
</div>

<!-- Summary -->
<div class="summary-card">
    <div class="summary-stat">
        <span class="summary-value"><?= count($payments) ?></span>
        <span class="summary-label">Betalningar</span>
    </div>
    <div class="summary-stat">
        <span class="summary-value"><?= number_format($totalSpent) ?> kr</span>
        <span class="summary-label">Totalt betalt</span>
    </div>
</div>

<!-- Receipts List -->
<?php if (empty($payments)): ?>
    <div class="empty-state">
        <div class="empty-icon"><i data-lucide="receipt" class="icon-xl"></i></div>
        <h3>Inga kvitton</h3>
        <p>Dina betalningar och kvitton visas här.</p>
    </div>
<?php else: ?>
    <div class="receipts-list">
        <?php foreach ($payments as $payment): ?>
            <div class="receipt-card">
                <div class="receipt-header">
                    <span class="receipt-event"><?= htmlspecialchars($payment['event_name']) ?></span>
                    <span class="receipt-amount"><?= number_format($payment['price'] ?? 0) ?> kr</span>
                </div>
                <div class="receipt-details">
                    <span><?= htmlspecialchars($payment['class_name'] ?? 'Anmälan') ?></span>
                    <span class="receipt-date"><?= date('Y-m-d', strtotime($payment['created_at'])) ?></span>
                </div>
                <div class="receipt-footer">
                    <span class="receipt-status status-paid">✓ Betald</span>
                </div>
            </div>
        <?php endforeach; ?>
    </div>
<?php endif; ?>


<!-- CSS loaded from /assets/css/pages/profile-receipts.css -->
