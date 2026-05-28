<?php
/**
 * Ekonomi Dashboard - Unified Payment & Registration Hub
 * TheHUB V3
 *
 * Central panel för all ekonomisk administration:
 * - Betalningsmetoder (Swish, Stripe, Manuell)
 * - Mottagare (klubbar, arrangörer)
 * - Ordrar och betalningar
 * - Prismallar och prissättning
 * - Statistik och rapporter
 */
require_once __DIR__ . '/../config.php';
require_admin();

$db = getDB();
$currentAdmin = getCurrentAdmin();
$isSuperAdmin = hasRole('super_admin');

// Hämta statistik
$stats = [];

// Totalt antal ordrar
$stats['total_orders'] = $db->getRow("SELECT COUNT(*) as cnt FROM orders")['cnt'] ?? 0;

// Väntande betalningar
$stats['pending_orders'] = $db->getRow("SELECT COUNT(*) as cnt FROM orders WHERE payment_status = 'pending'")['cnt'] ?? 0;

// Bekräftade betalningar (senaste 30 dagarna)
$stats['confirmed_30d'] = $db->getRow("
    SELECT COUNT(*) as cnt FROM orders
    WHERE payment_status = 'paid'
    AND paid_at >= DATE_SUB(NOW(), INTERVAL 30 DAY)
")['cnt'] ?? 0;

// Total omsättning (senaste 30 dagarna)
$stats['revenue_30d'] = $db->getRow("
    SELECT COALESCE(SUM(total_amount), 0) as total FROM orders
    WHERE payment_status = 'paid'
    AND paid_at >= DATE_SUB(NOW(), INTERVAL 30 DAY)
")['total'] ?? 0;

// Antal aktiva mottagare
$stats['active_recipients'] = $db->getRow("
    SELECT COUNT(*) as cnt FROM payment_recipients WHERE is_active = 1
")['cnt'] ?? 0;

// Antal prismallar
$stats['pricing_templates'] = $db->getRow("SELECT COUNT(*) as cnt FROM pricing_templates")['cnt'] ?? 0;

// Väntande återbetalningar
$stats['pending_refunds'] = $db->getRow("
    SELECT COUNT(*) as cnt FROM refund_requests WHERE status = 'pending'
")['cnt'] ?? 0;

// Senaste ordrar
$recentOrders = $db->getAll("
    SELECT o.*, e.name as event_name,
           r.firstname, r.lastname
    FROM orders o
    LEFT JOIN events e ON o.event_id = e.id
    LEFT JOIN riders r ON o.rider_id = r.id
    ORDER BY o.created_at DESC
    LIMIT 5
");

// Page config
$page_title = 'Ekonomi';
$breadcrumbs = [
    ['label' => 'Ekonomi']
];

include __DIR__ . '/components/unified-layout.php';
?>

<style>
.ekonomi-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: var(--space-lg);
    margin-bottom: var(--space-xl);
}

.ekonomi-card {
    background: var(--color-bg-card);
    border: 1px solid var(--color-border);
    border-radius: var(--radius-lg);
    padding: var(--space-lg);
    transition: all 0.2s ease;
}

.ekonomi-card:hover {
    border-color: var(--color-accent);
    box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}

.ekonomi-card-header {
    display: flex;
    align-items: center;
    gap: var(--space-md);
    margin-bottom: var(--space-md);
}

.ekonomi-card-icon {
    width: 48px;
    height: 48px;
    border-radius: var(--radius-md);
    display: flex;
    align-items: center;
    justify-content: center;
    color: white;
}

.ekonomi-card-icon svg {
    width: 24px;
    height: 24px;
}

.ekonomi-card-icon.blue { background: linear-gradient(135deg, #3b82f6, #1d4ed8); }
.ekonomi-card-icon.green { background: linear-gradient(135deg, #10b981, #059669); }
.ekonomi-card-icon.purple { background: linear-gradient(135deg, #8b5cf6, #6d28d9); }
.ekonomi-card-icon.orange { background: linear-gradient(135deg, #f59e0b, #d97706); }
.ekonomi-card-icon.red { background: linear-gradient(135deg, #ef4444, #dc2626); }
.ekonomi-card-icon.cyan { background: linear-gradient(135deg, #06b6d4, #0891b2); }

.ekonomi-card-title {
    font-size: var(--text-lg);
    font-weight: 600;
    color: var(--color-text-primary);
    margin: 0;
}

.ekonomi-card-subtitle {
    font-size: var(--text-sm);
    color: var(--color-text-secondary);
    margin: 0;
}

.ekonomi-card-body {
    margin-bottom: var(--space-md);
}

.ekonomi-card-body p {
    color: var(--color-text-secondary);
    font-size: var(--text-sm);
    margin: 0;
}

.ekonomi-card-links {
    display: flex;
    flex-direction: column;
    gap: var(--space-xs);
}

.ekonomi-card-link {
    display: flex;
    align-items: center;
    gap: var(--space-sm);
    padding: var(--space-sm) var(--space-md);
    background: var(--color-bg-hover);
    border-radius: var(--radius-sm);
    color: var(--color-text-primary);
    text-decoration: none;
    font-size: var(--text-sm);
    transition: all 0.15s ease;
}

.ekonomi-card-link:hover {
    background: var(--color-accent-light);
    color: var(--color-accent);
}

.ekonomi-card-link svg {
    width: 16px;
    height: 16px;
    color: var(--color-text-muted);
}

.ekonomi-card-link:hover svg {
    color: var(--color-accent);
}

.stats-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
    gap: var(--space-md);
    margin-bottom: var(--space-xl);
}

.stat-card {
    background: var(--color-bg-card);
    border: 1px solid var(--color-border);
    border-radius: var(--radius-md);
    padding: var(--space-md);
    text-align: center;
}

.stat-value {
    font-size: var(--text-2xl);
    font-weight: 700;
    color: var(--color-text-primary);
}

.stat-value.warning { color: var(--color-warning); }
.stat-value.success { color: var(--color-success); }
.stat-value.accent { color: var(--color-accent); }

.stat-label {
    font-size: var(--text-sm);
    color: var(--color-text-secondary);
    margin-top: var(--space-xs);
}

.recent-orders {
    background: var(--color-bg-card);
    border: 1px solid var(--color-border);
    border-radius: var(--radius-lg);
    overflow: hidden;
}

.recent-orders-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: var(--space-md) var(--space-lg);
    border-bottom: 1px solid var(--color-border);
}

.recent-orders-header h3 {
    margin: 0;
    font-size: var(--text-lg);
}

.order-row {
    display: flex;
    align-items: center;
    padding: var(--space-md) var(--space-lg);
    border-bottom: 1px solid var(--color-border);
    gap: var(--space-md);
}

.order-row:last-child {
    border-bottom: none;
}

.order-row:hover {
    background: var(--color-bg-hover);
}

.order-status {
    padding: 2px 8px;
    border-radius: var(--radius-full);
    font-size: var(--text-xs);
    font-weight: 600;
}

.order-status.pending { background: rgba(251, 191, 36, 0.2); color: #d97706; }
.order-status.paid { background: rgba(16, 185, 129, 0.2); color: #059669; }
.order-status.cancelled { background: rgba(239, 68, 68, 0.2); color: #dc2626; }

.quick-actions {
    display: flex;
    gap: var(--space-md);
    flex-wrap: wrap;
    margin-bottom: var(--space-xl);
}

.quick-action-btn {
    display: inline-flex;
    align-items: center;
    gap: var(--space-sm);
    padding: var(--space-sm) var(--space-lg);
    background: var(--color-accent);
    color: white;
    border-radius: var(--radius-md);
    text-decoration: none;
    font-weight: 500;
    transition: all 0.15s ease;
}

.quick-action-btn:hover {
    background: var(--color-accent-hover);
    transform: translateY(-1px);
}

.quick-action-btn svg {
    width: 18px;
    height: 18px;
}

.section-title {
    font-size: var(--text-xl);
    font-weight: 600;
    margin-bottom: var(--space-lg);
    color: var(--color-text-primary);
    display: flex;
    align-items: center;
    gap: var(--space-sm);
}

.section-title svg {
    width: 24px;
    height: 24px;
    color: var(--color-accent);
}
</style>

<!-- Snabbstatistik -->
<div class="stats-grid">
    <div class="stat-card">
        <div class="stat-value <?= $stats['pending_orders'] > 0 ? 'warning' : '' ?>">
            <?= number_format($stats['pending_orders']) ?>
        </div>
        <div class="stat-label">Väntande betalningar</div>
    </div>
    <div class="stat-card">
        <div class="stat-value success"><?= number_format($stats['confirmed_30d']) ?></div>
        <div class="stat-label">Bekräftade (30 dagar)</div>
    </div>
    <div class="stat-card">
        <div class="stat-value accent"><?= number_format($stats['revenue_30d']) ?> kr</div>
        <div class="stat-label">Omsättning (30 dagar)</div>
    </div>
    <div class="stat-card">
        <div class="stat-value"><?= number_format($stats['active_recipients']) ?></div>
        <div class="stat-label">Aktiva mottagare</div>
    </div>
    <?php if ($stats['pending_refunds'] > 0): ?>
    <div class="stat-card">
        <div class="stat-value warning"><?= number_format($stats['pending_refunds']) ?></div>
        <div class="stat-label">Väntande återbetalningar</div>
    </div>
    <?php endif; ?>
</div>

<!-- Snabbåtgärder -->
<div class="quick-actions">
    <a href="/admin/orders?status=pending" class="quick-action-btn">
        <i data-lucide="clock"></i>
        Hantera väntande (<?= $stats['pending_orders'] ?>)
    </a>
    <?php if ($isSuperAdmin): ?>
    <a href="/admin/gateway-settings" class="quick-action-btn">
        <i data-lucide="settings"></i>
        Konfigurera betalmetoder
    </a>
    <?php endif; ?>
    <a href="/admin/pricing-templates" class="quick-action-btn">
        <i data-lucide="receipt"></i>
        Prismallar
    </a>
</div>

<!-- Huvudsektioner -->
<h2 class="section-title">
    <i data-lucide="layout-grid"></i>
    Administrera
</h2>

<div class="ekonomi-grid">
    <!-- Betalningsmetoder -->
    <div class="ekonomi-card">
        <div class="ekonomi-card-header">
            <div class="ekonomi-card-icon blue">
                <i data-lucide="credit-card"></i>
            </div>
            <div>
                <h3 class="ekonomi-card-title">Betalningsmetoder</h3>
                <p class="ekonomi-card-subtitle">Swish, Stripe, Manuell</p>
            </div>
        </div>
        <div class="ekonomi-card-body">
            <p>Konfigurera hur deltagare kan betala för anmälningar. Stöd för Swish Handel (automatisk), Stripe (kort) och manuell betalning.</p>
        </div>
        <div class="ekonomi-card-links">
            <a href="/admin/swish-accounts" class="ekonomi-card-link">
                <i data-lucide="smartphone"></i>
                Swish-konton (Alla)
            </a>
            <?php if ($isSuperAdmin): ?>
            <a href="/admin/gateway-settings" class="ekonomi-card-link">
                <i data-lucide="sliders"></i>
                Gateway-inställningar
            </a>
            <a href="/admin/certificates" class="ekonomi-card-link">
                <i data-lucide="shield-check"></i>
                Certifikat (Swish Handel)
            </a>
            <?php endif; ?>
            <a href="/admin/payment-settings" class="ekonomi-card-link">
                <i data-lucide="settings"></i>
                Betalningsinställningar
            </a>
        </div>
    </div>

    <!-- Mottagare -->
    <div class="ekonomi-card">
        <div class="ekonomi-card-header">
            <div class="ekonomi-card-icon green">
                <i data-lucide="users"></i>
            </div>
            <div>
                <h3 class="ekonomi-card-title">Mottagare</h3>
                <p class="ekonomi-card-subtitle"><?= $stats['active_recipients'] ?> aktiva</p>
            </div>
        </div>
        <div class="ekonomi-card-body">
            <p>Hantera vem som tar emot betalningar. Varje arrangör/klubb kan ha egna Swish-nummer eller bankkonton.</p>
        </div>
        <div class="ekonomi-card-links">
            <a href="/admin/payment-recipients" class="ekonomi-card-link">
                <i data-lucide="building-2"></i>
                Hantera mottagare
            </a>
            <?php if ($isSuperAdmin): ?>
            <a href="/admin/payment-recipients?action=create" class="ekonomi-card-link">
                <i data-lucide="plus"></i>
                Lägg till mottagare
            </a>
            <?php endif; ?>
        </div>
    </div>

    <!-- Ordrar & Betalningar -->
    <div class="ekonomi-card">
        <div class="ekonomi-card-header">
            <div class="ekonomi-card-icon purple">
                <i data-lucide="receipt"></i>
            </div>
            <div>
                <h3 class="ekonomi-card-title">Ordrar</h3>
                <p class="ekonomi-card-subtitle"><?= $stats['pending_orders'] ?> väntande</p>
            </div>
        </div>
        <div class="ekonomi-card-body">
            <p>Se alla ordrar, bekräfta manuella betalningar, och hantera återbetalningar.</p>
        </div>
        <div class="ekonomi-card-links">
            <a href="/admin/orders" class="ekonomi-card-link">
                <i data-lucide="list"></i>
                Alla ordrar
            </a>
            <a href="/admin/orders?status=pending" class="ekonomi-card-link">
                <i data-lucide="clock"></i>
                Väntande betalningar
            </a>
            <a href="/admin/refund-requests" class="ekonomi-card-link">
                <i data-lucide="rotate-ccw"></i>
                Återbetalningar
            </a>
        </div>
    </div>

    <!-- Prissättning -->
    <div class="ekonomi-card">
        <div class="ekonomi-card-header">
            <div class="ekonomi-card-icon orange">
                <i data-lucide="tag"></i>
            </div>
            <div>
                <h3 class="ekonomi-card-title">Prissättning</h3>
                <p class="ekonomi-card-subtitle"><?= $stats['pricing_templates'] ?> mallar</p>
            </div>
        </div>
        <div class="ekonomi-card-body">
            <p>Skapa prismallar som kan återanvändas för events. Sätt priser per klass, early bird-rabatter, och mer.</p>
        </div>
        <div class="ekonomi-card-links">
            <a href="/admin/pricing-templates" class="ekonomi-card-link">
                <i data-lucide="file-text"></i>
                Prismallar
            </a>
            <a href="/admin/pricing-templates?action=create" class="ekonomi-card-link">
                <i data-lucide="plus"></i>
                Skapa ny mall
            </a>
        </div>
    </div>

    <!-- Anmälningsregler -->
    <div class="ekonomi-card">
        <div class="ekonomi-card-header">
            <div class="ekonomi-card-icon cyan">
                <i data-lucide="shield-check"></i>
            </div>
            <div>
                <h3 class="ekonomi-card-title">Anmälningsregler</h3>
                <p class="ekonomi-card-subtitle">Licenskrav & begränsningar</p>
            </div>
        </div>
        <div class="ekonomi-card-body">
            <p>Definiera vilka licenser som krävs för olika klasser, åldersgränser, och andra anmälningsregler.</p>
        </div>
        <div class="ekonomi-card-links">
            <a href="/admin/registration-rules" class="ekonomi-card-link">
                <i data-lucide="list-checks"></i>
                Regler
            </a>
            <a href="/admin/license-class-matrix" class="ekonomi-card-link">
                <i data-lucide="grid-3x3"></i>
                Licens-klassmatris
            </a>
            <a href="/admin/classes" class="ekonomi-card-link">
                <i data-lucide="layers"></i>
                Klasser
            </a>
        </div>
    </div>

    <!-- Rapporter -->
    <div class="ekonomi-card">
        <div class="ekonomi-card-header">
            <div class="ekonomi-card-icon red">
                <i data-lucide="bar-chart-3"></i>
            </div>
            <div>
                <h3 class="ekonomi-card-title">Rapporter</h3>
                <p class="ekonomi-card-subtitle">Statistik & export</p>
            </div>
        </div>
        <div class="ekonomi-card-body">
            <p>Se ekonomiska rapporter, exportera data, och analysera anmälningsstatistik.</p>
        </div>
        <div class="ekonomi-card-links">
            <a href="/admin/orders?export=csv" class="ekonomi-card-link">
                <i data-lucide="download"></i>
                Exportera ordrar (CSV)
            </a>
            <?php if ($isSuperAdmin): ?>
            <a href="/admin/promotor-payments" class="ekonomi-card-link">
                <i data-lucide="wallet"></i>
                Arrangörsbetalningar
            </a>
            <?php endif; ?>
        </div>
    </div>
</div>

<!-- Senaste ordrar -->
<?php if (!empty($recentOrders)): ?>
<h2 class="section-title">
    <i data-lucide="clock"></i>
    Senaste ordrar
</h2>

<div class="recent-orders">
    <div class="recent-orders-header">
        <h3>Senaste 5 ordrar</h3>
        <a href="/admin/orders" class="btn btn--secondary btn--sm">Visa alla</a>
    </div>
    <?php foreach ($recentOrders as $order): ?>
    <div class="order-row">
        <span class="order-status <?= $order['payment_status'] ?>">
            <?= $order['payment_status'] === 'paid' ? 'Betald' : ($order['payment_status'] === 'pending' ? 'Väntar' : 'Avbruten') ?>
        </span>
        <div style="flex: 1;">
            <strong><?= h($order['firstname'] . ' ' . $order['lastname']) ?></strong>
            <span style="color: var(--color-text-secondary); margin-left: var(--space-sm);">
                <?= h($order['event_name'] ?? 'Okänt event') ?>
            </span>
        </div>
        <div style="text-align: right;">
            <strong><?= number_format($order['total_amount'] ?? 0) ?> kr</strong>
            <div style="font-size: var(--text-xs); color: var(--color-text-muted);">
                <?= date('j M H:i', strtotime($order['created_at'])) ?>
            </div>
        </div>
    </div>
    <?php endforeach; ?>
</div>
<?php endif; ?>

<!-- Hjälpsektion -->
<div class="card" style="margin-top: var(--space-xl);">
    <div class="card-header">
        <h3><i data-lucide="help-circle"></i> Hur fungerar anmälningssystemet?</h3>
    </div>
    <div class="card-body">
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: var(--space-lg);">
            <div>
                <h4 style="color: var(--color-accent); margin-bottom: var(--space-sm);">1. Skapa event</h4>
                <p style="color: var(--color-text-secondary); font-size: var(--text-sm);">
                    Skapa ett event under Tävlingar och aktivera anmälan. Välj vilka klasser som ska vara tillgängliga.
                </p>
            </div>
            <div>
                <h4 style="color: var(--color-accent); margin-bottom: var(--space-sm);">2. Sätt priser</h4>
                <p style="color: var(--color-text-secondary); font-size: var(--text-sm);">
                    Använd en prismall eller sätt priser direkt på eventet. Konfigurera early bird och sena anmälningar.
                </p>
            </div>
            <div>
                <h4 style="color: var(--color-accent); margin-bottom: var(--space-sm);">3. Konfigurera betalning</h4>
                <p style="color: var(--color-text-secondary); font-size: var(--text-sm);">
                    Välj mottagare för betalningar. Kan vara Swish Handel (automatisk) eller manuell Swish.
                </p>
            </div>
            <div>
                <h4 style="color: var(--color-accent); margin-bottom: var(--space-sm);">4. Öppna anmälan</h4>
                <p style="color: var(--color-text-secondary); font-size: var(--text-sm);">
                    Deltagare kan nu anmäla sig via hemsidan. Betalningar bekräftas automatiskt (Swish Handel) eller manuellt.
                </p>
            </div>
        </div>
    </div>
</div>

<script>
// Initialize Lucide icons
if (typeof lucide !== 'undefined') {
    lucide.createIcons();
}
</script>

<?php include __DIR__ . '/components/unified-layout-footer.php'; ?>
