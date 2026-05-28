<?php
/**
 * Admin Dashboard - Unified V3 Design System
 * v3.6.0 - Added payment stats and improved quick actions
 */
require_once __DIR__ . '/../config.php';

// Promotors should use their own simplified panel
if (isRole('promotor')) {
    redirect('/admin/promotor.php');
}

global $pdo;

// Get statistics
$stats = [];
try {
    $stats['riders'] = $pdo->query("SELECT COUNT(*) FROM riders")->fetchColumn();
    $stats['events'] = $pdo->query("SELECT COUNT(*) FROM events")->fetchColumn();
    $stats['clubs'] = $pdo->query("SELECT COUNT(*) FROM clubs")->fetchColumn();
    $stats['series'] = $pdo->query("SELECT COUNT(*) FROM series")->fetchColumn();
    $stats['upcoming'] = $pdo->query("SELECT COUNT(*) FROM events WHERE date >= CURDATE()")->fetchColumn();
    $stats['results'] = $pdo->query("SELECT COUNT(*) FROM results")->fetchColumn();

    // Payment stats (if table exists)
    try {
        $stats['pending_orders'] = $pdo->query("SELECT COUNT(*) FROM orders WHERE payment_status = 'pending'")->fetchColumn();
        $stats['total_revenue'] = $pdo->query("SELECT COALESCE(SUM(total_amount), 0) FROM orders WHERE payment_status = 'paid'")->fetchColumn();
    } catch (Exception $e) {
        $stats['pending_orders'] = 0;
        $stats['total_revenue'] = 0;
    }

    // Recent registrations
    try {
        $stats['registrations_today'] = $pdo->query("SELECT COUNT(*) FROM event_registrations WHERE DATE(created_at) = CURDATE()")->fetchColumn();
        $stats['registrations_week'] = $pdo->query("SELECT COUNT(*) FROM event_registrations WHERE created_at >= DATE_SUB(CURDATE(), INTERVAL 7 DAY)")->fetchColumn();
    } catch (Exception $e) {
        $stats['registrations_today'] = 0;
        $stats['registrations_week'] = 0;
    }

    // Pending rider claims
    try {
        $stats['pending_claims'] = $pdo->query("SELECT COUNT(*) FROM rider_claims WHERE status = 'pending'")->fetchColumn();
    } catch (Exception $e) {
        $stats['pending_claims'] = 0;
    }

    // Pending news/race reports
    try {
        $stats['pending_news'] = $pdo->query("SELECT COUNT(*) FROM race_reports WHERE status = 'draft'")->fetchColumn();
    } catch (Exception $e) {
        $stats['pending_news'] = 0;
    }
} catch (Exception $e) {
    $stats = [
        'riders' => 0, 'events' => 0, 'clubs' => 0, 'series' => 0,
        'upcoming' => 0, 'results' => 0, 'pending_orders' => 0,
        'total_revenue' => 0, 'registrations_today' => 0, 'registrations_week' => 0,
        'pending_claims' => 0, 'pending_news' => 0
    ];
}

// Ensure pending_claims is always set (in case of partial failure above)
if (!isset($stats['pending_claims'])) {
    try {
        $stats['pending_claims'] = $pdo->query("SELECT COUNT(*) FROM rider_claims WHERE status = 'pending'")->fetchColumn();
    } catch (Exception $e) {
        $stats['pending_claims'] = 0;
    }
}

// Ensure pending_news is always set
if (!isset($stats['pending_news'])) {
    try {
        $stats['pending_news'] = $pdo->query("SELECT COUNT(*) FROM race_reports WHERE status = 'draft'")->fetchColumn();
    } catch (Exception $e) {
        $stats['pending_news'] = 0;
    }
}

// Count pending roadmap tasks from ROADMAP.md
$roadmapPendingCount = 0;
$roadmapPath = __DIR__ . '/../ROADMAP.md';
if (file_exists($roadmapPath)) {
    $roadmapContent = file_get_contents($roadmapPath);
    $roadmapPendingCount = substr_count($roadmapContent, '[ ]');
}

// Get upcoming events
$upcomingEvents = [];
try {
    $upcomingEvents = $pdo->query("
        SELECT e.id, e.name, e.date, e.location, s.name as series_name,
               (SELECT COUNT(*) FROM event_registrations er WHERE er.event_id = e.id) as registration_count
        FROM events e
        LEFT JOIN series s ON e.series_id = s.id
        WHERE e.date >= CURDATE()
        ORDER BY e.date ASC
        LIMIT 5
    ")->fetchAll(PDO::FETCH_ASSOC);
} catch (Exception $e) {
    $upcomingEvents = [];
}

// Get pending orders (if table exists)
$pendingOrders = [];
try {
    $pendingOrders = $pdo->query("
        SELECT o.id, o.order_number, o.total_amount, o.created_at, o.swish_message,
               r.firstname, r.lastname, e.name as event_name
        FROM orders o
        LEFT JOIN riders r ON o.rider_id = r.id
        LEFT JOIN events e ON o.event_id = e.id
        WHERE o.payment_status = 'pending'
        ORDER BY o.created_at DESC
        LIMIT 5
    ")->fetchAll(PDO::FETCH_ASSOC);
} catch (Exception $e) {
    $pendingOrders = [];
}

// Page config
$page_title = 'Dashboard';
$breadcrumbs = [
    ['label' => 'Dashboard']
];

// Include unified layout
include __DIR__ . '/components/unified-layout.php';
?>

<?php if ($stats['pending_claims'] > 0): ?>
<!-- Pending Claims Alert - Prominent Red Box -->
<a href="/admin/rider-claims.php" class="pending-claims-box">
    <div class="claims-box-icon">
        <i data-lucide="user-check"></i>
        <span class="claims-box-count"><?= $stats['pending_claims'] ?></span>
    </div>
    <div class="claims-box-text">
        <strong>Profilkopplingar väntar</strong>
        <span><?= $stats['pending_claims'] ?> användare vill verifiera sina profiler</span>
    </div>
    <div class="claims-box-arrow">
        <i data-lucide="chevron-right"></i>
    </div>
</a>
<style>
.pending-claims-box {
    display: flex;
    align-items: center;
    gap: var(--space-lg);
    padding: var(--space-lg) var(--space-xl);
    margin-bottom: var(--space-lg);
    background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
    border-radius: var(--radius-lg);
    text-decoration: none;
    color: white;
    transition: transform 0.15s ease, box-shadow 0.15s ease;
    box-shadow: 0 4px 12px rgba(239, 68, 68, 0.3);
}
.pending-claims-box:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 20px rgba(239, 68, 68, 0.4);
}
.claims-box-icon {
    position: relative;
    display: flex;
    align-items: center;
    justify-content: center;
    width: 56px;
    height: 56px;
    background: rgba(255,255,255,0.2);
    border-radius: var(--radius-md);
    flex-shrink: 0;
}
.claims-box-icon i {
    width: 28px;
    height: 28px;
}
.claims-box-count {
    position: absolute;
    top: -8px;
    right: -8px;
    display: flex;
    align-items: center;
    justify-content: center;
    min-width: 28px;
    height: 28px;
    padding: 0 6px;
    background: white;
    color: #ef4444;
    font-size: 14px;
    font-weight: 700;
    border-radius: 14px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.2);
}
.claims-box-text {
    flex: 1;
}
.claims-box-text strong {
    display: block;
    font-size: var(--text-lg);
    font-weight: 600;
    margin-bottom: 4px;
}
.claims-box-text span {
    font-size: var(--text-sm);
    opacity: 0.9;
}
.claims-box-arrow {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 40px;
    height: 40px;
    background: rgba(255,255,255,0.2);
    border-radius: 50%;
    flex-shrink: 0;
}
.claims-box-arrow i {
    width: 24px;
    height: 24px;
}
@media (max-width: 600px) {
    .pending-claims-box {
        padding: var(--space-md);
        gap: var(--space-md);
    }
    .claims-box-icon {
        width: 48px;
        height: 48px;
    }
    .claims-box-text strong {
        font-size: var(--text-base);
    }
    .claims-box-arrow {
        display: none;
    }
}
</style>
<?php endif; ?>

<?php if ($stats['pending_news'] > 0): ?>
<!-- Pending News Alert - Red Box -->
<a href="/admin/news-moderation.php" class="pending-news-box">
    <div class="news-box-icon">
        <i data-lucide="newspaper"></i>
        <span class="news-box-count"><?= $stats['pending_news'] ?></span>
    </div>
    <div class="news-box-text">
        <strong>Nyheter väntar på godkännande</strong>
        <span><?= $stats['pending_news'] ?> inlägg behöver granskas</span>
    </div>
    <div class="news-box-arrow">
        <i data-lucide="chevron-right"></i>
    </div>
</a>
<style>
.pending-news-box {
    display: flex;
    align-items: center;
    gap: var(--space-lg);
    padding: var(--space-lg) var(--space-xl);
    margin-bottom: var(--space-lg);
    background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
    border-radius: var(--radius-lg);
    text-decoration: none;
    color: white;
    transition: transform 0.15s ease, box-shadow 0.15s ease;
    box-shadow: 0 4px 12px rgba(239, 68, 68, 0.3);
}
.pending-news-box:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 20px rgba(239, 68, 68, 0.4);
}
.news-box-icon {
    position: relative;
    display: flex;
    align-items: center;
    justify-content: center;
    width: 56px;
    height: 56px;
    background: rgba(255,255,255,0.2);
    border-radius: var(--radius-md);
    flex-shrink: 0;
}
.news-box-icon i {
    width: 28px;
    height: 28px;
}
.news-box-count {
    position: absolute;
    top: -8px;
    right: -8px;
    display: flex;
    align-items: center;
    justify-content: center;
    min-width: 28px;
    height: 28px;
    padding: 0 6px;
    background: white;
    color: #ef4444;
    font-size: 14px;
    font-weight: 700;
    border-radius: 14px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.2);
}
.news-box-text {
    flex: 1;
}
.news-box-text strong {
    display: block;
    font-size: var(--text-lg);
    font-weight: 600;
    margin-bottom: 4px;
}
.news-box-text span {
    font-size: var(--text-sm);
    opacity: 0.9;
}
.news-box-arrow {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 40px;
    height: 40px;
    background: rgba(255,255,255,0.2);
    border-radius: 50%;
    flex-shrink: 0;
}
.news-box-arrow i {
    width: 24px;
    height: 24px;
}
@media (max-width: 600px) {
    .pending-news-box {
        padding: var(--space-md);
        gap: var(--space-md);
    }
    .news-box-icon {
        width: 48px;
        height: 48px;
    }
    .news-box-text strong {
        font-size: var(--text-base);
    }
    .news-box-arrow {
        display: none;
    }
}
</style>
<?php endif; ?>

<!-- Key Metrics -->
<div class="dashboard-metrics">
    <div class="metric-card metric-card--primary">
        <div class="metric-icon">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M8 2v4"/><path d="M16 2v4"/><rect width="18" height="18" x="3" y="4" rx="2"/><path d="M3 10h18"/></svg>
        </div>
        <div class="metric-content">
            <div class="metric-value"><?= number_format($stats['upcoming']) ?></div>
            <div class="metric-label">Kommande events</div>
        </div>
    </div>

    <?php if ($stats['pending_orders'] > 0): ?>
    <a href="/admin/orders.php?status=pending" class="metric-card metric-card--warning">
        <div class="metric-icon">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/></svg>
        </div>
        <div class="metric-content">
            <div class="metric-value"><?= number_format($stats['pending_orders']) ?></div>
            <div class="metric-label">Väntande betalningar</div>
        </div>
    </a>
    <?php else: ?>
    <div class="metric-card metric-card--success">
        <div class="metric-icon">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/></svg>
        </div>
        <div class="metric-content">
            <div class="metric-value">0</div>
            <div class="metric-label">Väntande betalningar</div>
        </div>
    </div>
    <?php endif; ?>

    <div class="metric-card">
        <div class="metric-icon">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>
        </div>
        <div class="metric-content">
            <div class="metric-value"><?= number_format($stats['registrations_week']) ?></div>
            <div class="metric-label">Anmälningar (7 dagar)</div>
        </div>
    </div>

    <div class="metric-card">
        <div class="metric-icon">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect width="20" height="14" x="2" y="5" rx="2"/><line x1="2" x2="22" y1="10" y2="10"/></svg>
        </div>
        <div class="metric-content">
            <div class="metric-value"><?= number_format($stats['total_revenue'], 0, ',', ' ') ?> kr</div>
            <div class="metric-label">Totalt inbetalt</div>
        </div>
    </div>
</div>

<!-- Quick Actions -->
<div class="admin-card">
    <div class="admin-card-header">
        <h2>Snabbåtgärder</h2>
    </div>
    <div class="admin-card-body">
        <div class="quick-actions">
            <a href="/admin/event-create.php" class="quick-action quick-action--primary">
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M5 12h14"/><path d="M12 5v14"/></svg>
                <span>Skapa event</span>
            </a>
            <a href="/admin/import-results.php" class="quick-action">
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="17 8 12 3 7 8"/><line x1="12" x2="12" y1="3" y2="15"/></svg>
                <span>Importera resultat</span>
            </a>
            <a href="/admin/riders.php" class="quick-action">
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>
                <span>Deltagare</span>
            </a>
            <a href="/admin/series.php" class="quick-action">
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M6 9H4.5a2.5 2.5 0 0 1 0-5H6"/><path d="M18 9h1.5a2.5 2.5 0 0 0 0-5H18"/><path d="M4 22h16"/><path d="M10 14.66V17c0 .55-.47.98-.97 1.21C7.85 18.75 7 20.24 7 22"/><path d="M14 14.66V17c0 .55.47.98.97 1.21C16.15 18.75 17 20.24 17 22"/><path d="M18 2H6v7a6 6 0 0 0 12 0V2Z"/></svg>
                <span>Serier</span>
            </a>
            <a href="/admin/payment-settings.php" class="quick-action">
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12.22 2h-.44a2 2 0 0 0-2 2v.18a2 2 0 0 1-1 1.73l-.43.25a2 2 0 0 1-2 0l-.15-.08a2 2 0 0 0-2.73.73l-.22.38a2 2 0 0 0 .73 2.73l.15.1a2 2 0 0 1 1 1.72v.51a2 2 0 0 1-1 1.74l-.15.09a2 2 0 0 0-.73 2.73l.22.38a2 2 0 0 0 2.73.73l.15-.08a2 2 0 0 1 2 0l.43.25a2 2 0 0 1 1 1.73V20a2 2 0 0 0 2 2h.44a2 2 0 0 0 2-2v-.18a2 2 0 0 1 1-1.73l.43-.25a2 2 0 0 1 2 0l.15.08a2 2 0 0 0 2.73-.73l.22-.39a2 2 0 0 0-.73-2.73l-.15-.08a2 2 0 0 1-1-1.74v-.5a2 2 0 0 1 1-1.74l.15-.09a2 2 0 0 0 .73-2.73l-.22-.38a2 2 0 0 0-2.73-.73l-.15.08a2 2 0 0 1-2 0l-.43-.25a2 2 0 0 1-1-1.73V4a2 2 0 0 0-2-2z"/><circle cx="12" cy="12" r="3"/></svg>
                <span>Swish-inställningar</span>
            </a>
            <a href="/admin/analytics-dashboard.php" class="quick-action">
                <i data-lucide="chart-line"></i>
                <span>Analytics</span>
            </a>
            <a href="/admin/winback-campaigns.php" class="quick-action">
                <i data-lucide="mail"></i>
                <span>Kampanjer</span>
            </a>
            <a href="/admin/news-moderation.php" class="quick-action">
                <i data-lucide="newspaper"></i>
                <span>Nyheter</span>
            </a>
            <a href="/admin/roadmap.php" class="quick-action <?= $roadmapPendingCount > 0 ? 'has-badge' : '' ?>">
                <i data-lucide="map"></i>
                <span>Roadmap</span>
                <?php if ($roadmapPendingCount > 0): ?>
                <span class="quick-action-badge"><?= $roadmapPendingCount ?></span>
                <?php endif; ?>
            </a>
        </div>
    </div>
</div>

<!-- Two Column Layout -->
<div class="grid grid-wide grid-gap-lg">
    <!-- Upcoming Events -->
    <div class="admin-card">
        <div class="admin-card-header">
            <h2>Kommande events</h2>
            <a href="/admin/events.php" class="btn-admin btn-admin-sm btn-admin-secondary">Visa alla</a>
        </div>
        <div class="admin-card-body" style="padding: 0;">
            <?php if (empty($upcomingEvents)): ?>
                <div class="admin-empty-state" style="padding: var(--space-xl);">
                    <p>Inga kommande events</p>
                    <a href="/admin/event-create.php" class="btn-admin btn-admin-primary">Skapa event</a>
                </div>
            <?php else: ?>
                <div class="admin-table-container">
                    <table class="admin-table">
                        <thead>
                            <tr>
                                <th>Event</th>
                                <th>Datum</th>
                                <th>Anmälda</th>
                            </tr>
                        </thead>
                        <tbody>
                            <?php foreach ($upcomingEvents as $event): ?>
                                <tr>
                                    <td>
                                        <a href="/admin/event-edit.php?id=<?= $event['id'] ?>" style="color: var(--color-accent); text-decoration: none; font-weight: 500;">
                                            <?= htmlspecialchars($event['name']) ?>
                                        </a>
                                        <?php if ($event['series_name']): ?>
                                            <div style="font-size: var(--text-xs); color: var(--color-text-secondary);">
                                                <?= htmlspecialchars($event['series_name']) ?>
                                            </div>
                                        <?php endif; ?>
                                    </td>
                                    <td><?= date('j M', strtotime($event['date'])) ?></td>
                                    <td>
                                        <span class="badge"><?= number_format($event['registration_count']) ?></span>
                                    </td>
                                </tr>
                            <?php endforeach; ?>
                        </tbody>
                    </table>
                </div>
            <?php endif; ?>
        </div>
    </div>

    <!-- Pending Payments -->
    <div class="admin-card">
        <div class="admin-card-header">
            <h2>Väntande betalningar</h2>
            <a href="/admin/orders.php?status=pending" class="btn-admin btn-admin-sm btn-admin-secondary">Visa alla</a>
        </div>
        <div class="admin-card-body" style="padding: 0;">
            <?php if (empty($pendingOrders)): ?>
                <div class="admin-empty-state" style="padding: var(--space-xl);">
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="width: 48px; height: 48px; color: var(--color-success); margin-bottom: var(--space-md);"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/></svg>
                    <p>Inga väntande betalningar</p>
                </div>
            <?php else: ?>
                <div class="admin-table-container">
                    <table class="admin-table">
                        <thead>
                            <tr>
                                <th>Order</th>
                                <th>Belopp</th>
                                <th>Swish-ref</th>
                            </tr>
                        </thead>
                        <tbody>
                            <?php foreach ($pendingOrders as $order): ?>
                                <tr>
                                    <td>
                                        <div style="font-weight: 500;"><?= htmlspecialchars($order['firstname'] . ' ' . $order['lastname']) ?></div>
                                        <div style="font-size: var(--text-xs); color: var(--color-text-secondary);">
                                            <?= htmlspecialchars($order['event_name'] ?? 'Okänt event') ?>
                                        </div>
                                    </td>
                                    <td><?= number_format($order['total_amount'], 0) ?> kr</td>
                                    <td><code style="font-size: var(--text-xs);"><?= htmlspecialchars($order['swish_message'] ?? '-') ?></code></td>
                                </tr>
                            <?php endforeach; ?>
                        </tbody>
                    </table>
                </div>
            <?php endif; ?>
        </div>
    </div>
</div>

<!-- Overview Stats -->
<div class="grid grid-stats grid-gap-md" class="mt-lg">
    <div class="admin-stat-card">
        <div class="stat-icon">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>
        </div>
        <div class="stat-value"><?= number_format($stats['riders']) ?></div>
        <div class="stat-label">Deltagare totalt</div>
    </div>

    <div class="admin-stat-card">
        <div class="stat-icon">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M8 2v4"/><path d="M16 2v4"/><rect width="18" height="18" x="3" y="4" rx="2"/><path d="M3 10h18"/></svg>
        </div>
        <div class="stat-value"><?= number_format($stats['events']) ?></div>
        <div class="stat-label">Events totalt</div>
    </div>

    <div class="admin-stat-card">
        <div class="stat-icon">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M6 9H4.5a2.5 2.5 0 0 1 0-5H6"/><path d="M18 9h1.5a2.5 2.5 0 0 0 0-5H18"/><path d="M4 22h16"/><path d="M10 14.66V17c0 .55-.47.98-.97 1.21C7.85 18.75 7 20.24 7 22"/><path d="M14 14.66V17c0 .55.47.98.97 1.21C16.15 18.75 17 20.24 17 22"/><path d="M18 2H6v7a6 6 0 0 0 12 0V2Z"/></svg>
        </div>
        <div class="stat-value"><?= number_format($stats['series']) ?></div>
        <div class="stat-label">Serier</div>
    </div>

    <div class="admin-stat-card">
        <div class="stat-icon">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M6 22V4a2 2 0 0 1 2-2h8a2 2 0 0 1 2 2v18Z"/><path d="M6 12H4a2 2 0 0 0-2 2v6a2 2 0 0 0 2 2h2"/><path d="M18 9h2a2 2 0 0 1 2 2v9a2 2 0 0 1-2 2h-2"/><path d="M10 6h4"/><path d="M10 10h4"/><path d="M10 14h4"/><path d="M10 18h4"/></svg>
        </div>
        <div class="stat-value"><?= number_format($stats['clubs']) ?></div>
        <div class="stat-label">Klubbar</div>
    </div>

    <div class="admin-stat-card">
        <div class="stat-icon">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/></svg>
        </div>
        <div class="stat-value"><?= number_format($stats['results']) ?></div>
        <div class="stat-label">Resultat</div>
    </div>
</div>

<style>
/* Dashboard Metrics */
.dashboard-metrics {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: var(--space-md);
    margin-bottom: var(--space-lg);
}

.metric-card {
    display: flex;
    align-items: center;
    gap: var(--space-md);
    padding: var(--space-lg);
    background: var(--color-bg-card);
    border: 1px solid var(--color-border);
    border-radius: var(--radius-lg);
    text-decoration: none;
    color: inherit;
    transition: all 0.15s ease;
}

.metric-card:hover {
    border-color: var(--color-border-strong);
    box-shadow: var(--shadow-md);
}

.metric-card--primary {
    background: var(--color-accent);
    border-color: var(--color-accent);
    color: white;
}

.metric-card--warning {
    background: rgba(234, 179, 8, 0.1);
    border-color: #eab308;
}

.metric-card--warning .metric-icon {
    color: #ca8a04;
}

.metric-card--warning .metric-value {
    color: #ca8a04;
}

.metric-card--success {
    background: rgba(34, 197, 94, 0.1);
    border-color: #22c55e;
}

.metric-card--success .metric-icon {
    color: #16a34a;
}

.metric-icon {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 48px;
    height: 48px;
    border-radius: var(--radius-md);
    background: rgba(0,0,0,0.05);
    flex-shrink: 0;
}

.metric-card--primary .metric-icon {
    background: rgba(255,255,255,0.2);
}

.metric-icon svg {
    width: 24px;
    height: 24px;
}

.metric-value {
    font-size: var(--text-2xl);
    font-weight: var(--weight-bold);
    line-height: 1;
}

.metric-label {
    font-size: var(--text-sm);
    color: var(--color-text-secondary);
    margin-top: 2px;
}

.metric-card--primary .metric-label {
    color: rgba(255,255,255,0.8);
}

/* Quick Actions */
.quick-actions {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
    gap: var(--space-sm);
}

.quick-action {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: var(--space-xs);
    padding: var(--space-md);
    background: var(--color-bg-card);
    border: 1px solid var(--color-border);
    border-radius: var(--radius-md);
    text-decoration: none;
    color: var(--color-text-primary);
    font-size: var(--text-sm);
    font-weight: var(--weight-medium);
    transition: all 0.15s ease;
}

.quick-action:hover {
    border-color: var(--color-accent);
    background: var(--color-bg-hover);
}

.quick-action--primary {
    background: var(--color-accent);
    border-color: var(--color-accent);
    color: white;
}

.quick-action--primary:hover {
    opacity: 0.9;
}

.quick-action svg {
    width: 24px;
    height: 24px;
}

.quick-action.has-badge {
    position: relative;
}

.quick-action-badge {
    position: absolute;
    top: -6px;
    right: -6px;
    display: flex;
    align-items: center;
    justify-content: center;
    min-width: 20px;
    height: 20px;
    padding: 0 5px;
    background: var(--color-warning);
    color: #000;
    font-size: 11px;
    font-weight: 700;
    border-radius: 10px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.2);
}

.badge {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    padding: 2px 8px;
    font-size: var(--text-xs);
    font-weight: var(--weight-medium);
    background: var(--color-accent-light);
    color: var(--color-accent);
    border-radius: var(--radius-full);
}

/* Tablet */
@media (max-width: 899px) {
    .dashboard-metrics {
        grid-template-columns: repeat(2, 1fr);
    }

    .metric-card {
        padding: var(--space-md);
    }

    .metric-icon {
        width: 40px;
        height: 40px;
    }

    .metric-icon svg {
        width: 20px;
        height: 20px;
    }

    .metric-value {
        font-size: var(--text-xl);
    }

    .quick-actions {
        grid-template-columns: repeat(3, 1fr);
    }
}

/* Mobile portrait */
@media (max-width: 767px) {
    /* Metrics: keep 2x2 grid, just smaller */
    .dashboard-metrics {
        grid-template-columns: repeat(2, 1fr);
        gap: var(--space-sm);
    }

    .metric-card {
        padding: var(--space-md);
        border-radius: var(--radius-md);
    }

    .metric-icon {
        width: 36px;
        height: 36px;
    }

    .metric-icon svg {
        width: 18px;
        height: 18px;
    }

    .metric-value {
        font-size: var(--text-lg);
    }

    .metric-label {
        font-size: var(--text-xs);
    }

    /* Quick actions: 3 columns for 5 items */
    .quick-actions {
        grid-template-columns: repeat(3, 1fr);
        gap: var(--space-xs);
    }

    .quick-action {
        padding: var(--space-sm);
        font-size: var(--text-xs);
    }

    .quick-action svg {
        width: 20px;
        height: 20px;
    }

    /* Grid wide - single column for card stacking */
    .grid-wide {
        grid-template-columns: 1fr !important;
    }

    /* Admin card edge-to-edge */
    .admin-card {
        margin-left: calc(-1 * var(--container-padding, 16px));
        margin-right: calc(-1 * var(--container-padding, 16px));
        width: auto;
        border-radius: 0;
        border-left: none;
        border-right: none;
    }

    /* Restore internal padding for card content */
    .admin-card-body,
    .admin-card-header {
        padding-left: var(--container-padding, 16px);
        padding-right: var(--container-padding, 16px);
    }

    /* Tables inside cards - ensure proper scrolling */
    .admin-card-body .admin-table-container {
        margin-left: calc(-1 * var(--container-padding, 16px));
        margin-right: calc(-1 * var(--container-padding, 16px));
        overflow-x: auto;
        -webkit-overflow-scrolling: touch;
    }

    .admin-card-body .admin-table-container .admin-table {
        min-width: 400px;
    }

    .admin-card-body .admin-table-container .admin-table th:first-child,
    .admin-card-body .admin-table-container .admin-table td:first-child {
        padding-left: var(--container-padding, 16px);
    }

    .admin-card-body .admin-table-container .admin-table th:last-child,
    .admin-card-body .admin-table-container .admin-table td:last-child {
        padding-right: var(--container-padding, 16px);
    }

    /* Stat cards grid - keep 2x2 */
    .grid-stats {
        grid-template-columns: repeat(2, 1fr) !important;
        gap: var(--space-sm);
    }

    .admin-stat-card {
        padding: var(--space-md);
    }

    .admin-stat-card .stat-value {
        font-size: var(--text-lg);
    }
}
</style>

<?php include __DIR__ . '/components/unified-layout-footer.php'; ?>
