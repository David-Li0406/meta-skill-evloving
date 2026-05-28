<?php
/**
 * Series Registrations Admin
 *
 * View and manage series (season pass) registrations.
 * Shows all riders who have purchased a series pass.
 *
 * URL: /admin/series-registrations.php?series_id=X
 *
 * @since 2026-01-11
 */

require_once __DIR__ . '/../config.php';
require_admin();

$db = getDB();

// Get series ID from URL
$seriesId = intval($_GET['series_id'] ?? $_GET['id'] ?? 0);

// If no series ID, show series list
if (!$seriesId) {
    // Get all series with registration counts
    $series = $db->getAll("
        SELECT s.*,
               COUNT(sr.id) AS registration_count,
               SUM(CASE WHEN sr.payment_status = 'paid' THEN 1 ELSE 0 END) AS paid_count,
               SUM(CASE WHEN sr.payment_status = 'paid' THEN sr.final_price ELSE 0 END) AS total_revenue
        FROM series s
        LEFT JOIN series_registrations sr ON s.id = sr.series_id AND sr.status = 'active'
        WHERE s.active = 1
        GROUP BY s.id
        ORDER BY s.year DESC, s.name ASC
    ");

    $page_title = 'Serie-registreringar';
    $page_group = 'registrations';
    include __DIR__ . '/components/unified-layout.php';
    ?>

    <div class="card">
        <div class="card-header">
            <h2>
                <i data-lucide="ticket"></i>
                Välj serie
            </h2>
        </div>
        <div class="card-body">
            <?php if (empty($series)): ?>
                <p class="text-secondary">Inga aktiva serier hittades.</p>
            <?php else: ?>
                <div class="table-responsive">
                    <table class="table">
                        <thead>
                            <tr>
                                <th>Serie</th>
                                <th>År</th>
                                <th class="text-right">Registreringar</th>
                                <th class="text-right">Betalda</th>
                                <th class="text-right">Intäkter</th>
                                <th></th>
                            </tr>
                        </thead>
                        <tbody>
                            <?php foreach ($series as $s): ?>
                                <tr>
                                    <td>
                                        <strong><?= h($s['name']) ?></strong>
                                    </td>
                                    <td><?= h($s['year']) ?></td>
                                    <td class="text-right">
                                        <span class="badge badge-neutral"><?= $s['registration_count'] ?></span>
                                    </td>
                                    <td class="text-right">
                                        <span class="badge badge-success"><?= $s['paid_count'] ?></span>
                                    </td>
                                    <td class="text-right">
                                        <?= number_format($s['total_revenue'], 0, ',', ' ') ?> kr
                                    </td>
                                    <td class="text-right">
                                        <a href="?series_id=<?= $s['id'] ?>" class="btn btn--sm btn--primary">
                                            <i data-lucide="eye"></i>
                                            Visa
                                        </a>
                                    </td>
                                </tr>
                            <?php endforeach; ?>
                        </tbody>
                    </table>
                </div>
            <?php endif; ?>
        </div>
    </div>

    <?php
    include __DIR__ . '/components/unified-layout-footer.php';
    exit;
}

// Get series info
$series = $db->getRow("SELECT * FROM series WHERE id = ?", [$seriesId]);

if (!$series) {
    $_SESSION['flash_message'] = 'Serie hittades inte';
    $_SESSION['flash_type'] = 'error';
    header('Location: /admin/series-registrations.php');
    exit;
}

$message = '';
$messageType = 'info';

// Handle actions
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    checkCsrf();

    $action = $_POST['action'] ?? '';
    $regId = intval($_POST['registration_id'] ?? 0);

    if ($action === 'mark_paid' && $regId) {
        $db->update('series_registrations', [
            'payment_status' => 'paid',
            'payment_method' => 'manual',
            'paid_at' => date('Y-m-d H:i:s')
        ], 'id = ?', [$regId]);
        $message = 'Registrering markerad som betald!';
        $messageType = 'success';

    } elseif ($action === 'cancel' && $regId) {
        $db->update('series_registrations', [
            'status' => 'cancelled',
            'cancelled_at' => date('Y-m-d H:i:s')
        ], 'id = ?', [$regId]);

        // Also cancel event registrations
        $db->query("
            UPDATE series_registration_events
            SET status = 'cancelled'
            WHERE series_registration_id = ?
        ", [$regId]);

        $message = 'Registrering avbruten!';
        $messageType = 'success';

    } elseif ($action === 'refund' && $regId) {
        $db->update('series_registrations', [
            'payment_status' => 'refunded'
        ], 'id = ?', [$regId]);
        $message = 'Registrering markerad som återbetald!';
        $messageType = 'success';
    }
}

// Filter parameters
$filterStatus = $_GET['status'] ?? 'all';
$filterPayment = $_GET['payment'] ?? 'all';
$filterClass = $_GET['class'] ?? '';
$search = trim($_GET['search'] ?? '');

// Build query
$whereConditions = ["sr.series_id = ?"];
$params = [$seriesId];

if ($filterStatus && $filterStatus !== 'all') {
    $whereConditions[] = "sr.status = ?";
    $params[] = $filterStatus;
}

if ($filterPayment && $filterPayment !== 'all') {
    $whereConditions[] = "sr.payment_status = ?";
    $params[] = $filterPayment;
}

if ($filterClass) {
    $whereConditions[] = "sr.class_id = ?";
    $params[] = intval($filterClass);
}

if ($search) {
    $whereConditions[] = "(r.firstname LIKE ? OR r.lastname LIKE ? OR r.email LIKE ? OR r.license_number LIKE ?)";
    $searchTerm = "%{$search}%";
    $params[] = $searchTerm;
    $params[] = $searchTerm;
    $params[] = $searchTerm;
    $params[] = $searchTerm;
}

$whereClause = 'WHERE ' . implode(' AND ', $whereConditions);

// Get registrations
$registrations = $db->getAll("
    SELECT sr.*,
           CONCAT(r.firstname, ' ', r.lastname) AS rider_name,
           r.email AS rider_email,
           r.license_number,
           r.gender AS rider_gender,
           c.name AS class_name,
           c.display_name AS class_display_name,
           (SELECT COUNT(*) FROM series_registration_events WHERE series_registration_id = sr.id) AS event_count,
           (SELECT COUNT(*) FROM series_registration_events WHERE series_registration_id = sr.id AND status = 'attended') AS events_attended
    FROM series_registrations sr
    JOIN riders r ON sr.rider_id = r.id
    JOIN classes c ON sr.class_id = c.id
    {$whereClause}
    ORDER BY sr.created_at DESC
    LIMIT 500
", $params);

// Get classes for filter
$classes = $db->getAll("
    SELECT DISTINCT c.id, c.name, c.display_name
    FROM series_registrations sr
    JOIN classes c ON sr.class_id = c.id
    WHERE sr.series_id = ?
    ORDER BY c.name
", [$seriesId]);

// Get stats
$stats = $db->getRow("
    SELECT
        COUNT(*) AS total,
        SUM(CASE WHEN status = 'active' THEN 1 ELSE 0 END) AS active,
        SUM(CASE WHEN payment_status = 'paid' THEN 1 ELSE 0 END) AS paid,
        SUM(CASE WHEN payment_status = 'pending' THEN 1 ELSE 0 END) AS pending,
        SUM(CASE WHEN payment_status = 'paid' THEN final_price ELSE 0 END) AS revenue
    FROM series_registrations
    WHERE series_id = ?
", [$seriesId]);

$page_title = 'Registreringar - ' . $series['name'];
$page_group = 'registrations';
include __DIR__ . '/components/unified-layout.php';
?>

<!-- Messages -->
<?php if ($message): ?>
    <div class="alert alert-<?= $messageType ?> mb-lg">
        <i data-lucide="<?= $messageType === 'success' ? 'check-circle' : 'info' ?>"></i>
        <?= h($message) ?>
    </div>
<?php endif; ?>

<!-- Breadcrumb -->
<div class="breadcrumb mb-md">
    <a href="/admin/series-registrations.php">Serie-registreringar</a>
    <i data-lucide="chevron-right"></i>
    <span><?= h($series['name']) ?></span>
</div>

<!-- Stats cards -->
<div class="stats-grid mb-lg">
    <div class="stat-card">
        <div class="stat-card__value"><?= $stats['total'] ?></div>
        <div class="stat-card__label">Totalt</div>
    </div>
    <div class="stat-card stat-card--success">
        <div class="stat-card__value"><?= $stats['paid'] ?></div>
        <div class="stat-card__label">Betalda</div>
    </div>
    <div class="stat-card stat-card--warning">
        <div class="stat-card__value"><?= $stats['pending'] ?></div>
        <div class="stat-card__label">Väntande</div>
    </div>
    <div class="stat-card stat-card--accent">
        <div class="stat-card__value"><?= number_format($stats['revenue'], 0, ',', ' ') ?> kr</div>
        <div class="stat-card__label">Intäkter</div>
    </div>
</div>

<!-- Filters -->
<div class="card mb-lg">
    <div class="card-body">
        <form method="GET" class="filter-form">
            <input type="hidden" name="series_id" value="<?= $seriesId ?>">
            <div class="filter-row">
                <div class="form-group">
                    <label class="form-label">Sök</label>
                    <input type="text" name="search" class="form-input" placeholder="Namn, e-post, licens..."
                           value="<?= h($search) ?>">
                </div>
                <div class="form-group">
                    <label class="form-label">Status</label>
                    <select name="status" class="form-select">
                        <option value="all">Alla</option>
                        <option value="active" <?= $filterStatus === 'active' ? 'selected' : '' ?>>Aktiva</option>
                        <option value="cancelled" <?= $filterStatus === 'cancelled' ? 'selected' : '' ?>>Avbrutna</option>
                    </select>
                </div>
                <div class="form-group">
                    <label class="form-label">Betalning</label>
                    <select name="payment" class="form-select">
                        <option value="all">Alla</option>
                        <option value="paid" <?= $filterPayment === 'paid' ? 'selected' : '' ?>>Betalda</option>
                        <option value="pending" <?= $filterPayment === 'pending' ? 'selected' : '' ?>>Väntande</option>
                        <option value="refunded" <?= $filterPayment === 'refunded' ? 'selected' : '' ?>>Återbetalda</option>
                    </select>
                </div>
                <div class="form-group">
                    <label class="form-label">Klass</label>
                    <select name="class" class="form-select">
                        <option value="">Alla</option>
                        <?php foreach ($classes as $c): ?>
                            <option value="<?= $c['id'] ?>" <?= $filterClass == $c['id'] ? 'selected' : '' ?>>
                                <?= h($c['display_name'] ?: $c['name']) ?>
                            </option>
                        <?php endforeach; ?>
                    </select>
                </div>
                <div class="form-group" style="align-self: flex-end;">
                    <button type="submit" class="btn btn--primary">
                        <i data-lucide="search"></i>
                        Filtrera
                    </button>
                </div>
            </div>
        </form>
    </div>
</div>

<!-- Registrations table -->
<div class="card">
    <div class="card-header">
        <h2>
            <i data-lucide="users"></i>
            Registreringar (<?= count($registrations) ?>)
        </h2>
        <div class="card-header-actions">
            <a href="/admin/series-edit.php?id=<?= $seriesId ?>" class="btn btn--secondary btn--sm">
                <i data-lucide="settings"></i>
                Serie-inställningar
            </a>
        </div>
    </div>
    <div class="card-body">
        <?php if (empty($registrations)): ?>
            <p class="text-secondary text-center py-lg">Inga registreringar hittades.</p>
        <?php else: ?>
            <div class="table-responsive">
                <table class="table">
                    <thead>
                        <tr>
                            <th>Cyklist</th>
                            <th>Klass</th>
                            <th class="text-right">Pris</th>
                            <th>Betalning</th>
                            <th>Status</th>
                            <th>Event</th>
                            <th>Registrerad</th>
                            <th></th>
                        </tr>
                    </thead>
                    <tbody>
                        <?php foreach ($registrations as $reg): ?>
                            <tr>
                                <td>
                                    <div>
                                        <strong><?= h($reg['rider_name']) ?></strong>
                                        <?php if ($reg['license_number']): ?>
                                            <br><small class="text-muted">#<?= h($reg['license_number']) ?></small>
                                        <?php endif; ?>
                                    </div>
                                </td>
                                <td>
                                    <?= h($reg['class_display_name'] ?: $reg['class_name']) ?>
                                </td>
                                <td class="text-right">
                                    <strong><?= number_format($reg['final_price'], 0, ',', ' ') ?> kr</strong>
                                    <?php if ($reg['discount_amount'] > 0): ?>
                                        <br><small class="text-success">-<?= number_format($reg['discount_amount'], 0, ',', ' ') ?> kr</small>
                                    <?php endif; ?>
                                </td>
                                <td>
                                    <?php if ($reg['payment_status'] === 'paid'): ?>
                                        <span class="badge badge-success">Betald</span>
                                    <?php elseif ($reg['payment_status'] === 'pending'): ?>
                                        <span class="badge badge-warning">Väntande</span>
                                    <?php elseif ($reg['payment_status'] === 'refunded'): ?>
                                        <span class="badge badge-info">Återbetald</span>
                                    <?php else: ?>
                                        <span class="badge badge-neutral"><?= h($reg['payment_status']) ?></span>
                                    <?php endif; ?>
                                </td>
                                <td>
                                    <?php if ($reg['status'] === 'active'): ?>
                                        <span class="badge badge-success">Aktiv</span>
                                    <?php elseif ($reg['status'] === 'cancelled'): ?>
                                        <span class="badge badge-error">Avbruten</span>
                                    <?php else: ?>
                                        <span class="badge badge-neutral"><?= h($reg['status']) ?></span>
                                    <?php endif; ?>
                                </td>
                                <td>
                                    <span class="text-sm">
                                        <?= $reg['events_attended'] ?>/<?= $reg['event_count'] ?>
                                    </span>
                                </td>
                                <td>
                                    <span class="text-sm text-muted">
                                        <?= date('Y-m-d H:i', strtotime($reg['created_at'])) ?>
                                    </span>
                                </td>
                                <td class="text-right">
                                    <div class="btn-group">
                                        <?php if ($reg['payment_status'] === 'pending' && $reg['status'] === 'active'): ?>
                                            <form method="POST" style="display:inline;">
                                                <?= csrf_field() ?>
                                                <input type="hidden" name="action" value="mark_paid">
                                                <input type="hidden" name="registration_id" value="<?= $reg['id'] ?>">
                                                <button type="submit" class="btn btn--sm btn--success" title="Markera betald">
                                                    <i data-lucide="check"></i>
                                                </button>
                                            </form>
                                        <?php endif; ?>

                                        <?php if ($reg['status'] === 'active'): ?>
                                            <form method="POST" style="display:inline;"
                                                  onsubmit="return confirm('Avbryta denna registrering?');">
                                                <?= csrf_field() ?>
                                                <input type="hidden" name="action" value="cancel">
                                                <input type="hidden" name="registration_id" value="<?= $reg['id'] ?>">
                                                <button type="submit" class="btn btn--sm btn--danger" title="Avbryt">
                                                    <i data-lucide="x"></i>
                                                </button>
                                            </form>
                                        <?php endif; ?>
                                    </div>
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
.stats-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: var(--space-md);
}

@media (min-width: 768px) {
    .stats-grid {
        grid-template-columns: repeat(4, 1fr);
    }
}

.stat-card {
    background: var(--color-bg-card);
    border: 1px solid var(--color-border);
    border-radius: var(--radius-md);
    padding: var(--space-md);
    text-align: center;
}

.stat-card__value {
    font-family: var(--font-heading);
    font-size: 1.75rem;
    color: var(--color-text-primary);
}

.stat-card__label {
    font-size: 0.875rem;
    color: var(--color-text-muted);
}

.stat-card--success {
    border-color: var(--color-success);
}

.stat-card--success .stat-card__value {
    color: var(--color-success);
}

.stat-card--warning {
    border-color: var(--color-warning);
}

.stat-card--warning .stat-card__value {
    color: var(--color-warning);
}

.stat-card--accent {
    border-color: var(--color-accent);
}

.stat-card--accent .stat-card__value {
    color: var(--color-accent);
}

.filter-row {
    display: flex;
    flex-wrap: wrap;
    gap: var(--space-md);
}

.filter-row .form-group {
    flex: 1;
    min-width: 150px;
}

.breadcrumb {
    display: flex;
    align-items: center;
    gap: var(--space-xs);
    font-size: 0.875rem;
    color: var(--color-text-muted);
}

.breadcrumb a {
    color: var(--color-accent);
    text-decoration: none;
}

.breadcrumb a:hover {
    text-decoration: underline;
}

.breadcrumb i {
    width: 16px;
    height: 16px;
}

.btn-group {
    display: flex;
    gap: var(--space-2xs);
}
</style>

<?php include __DIR__ . '/components/unified-layout-footer.php'; ?>
