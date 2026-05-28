<?php
/**
 * Admin - News/Race Reports Moderation
 * Approve, reject, and manage race reports and news posts
 */
require_once __DIR__ . '/../config.php';
require_once __DIR__ . '/../includes/auth.php';
require_admin();

global $pdo;

// Include RaceReportManager
require_once __DIR__ . '/../includes/RaceReportManager.php';
$reportManager = new RaceReportManager($pdo);

$message = '';
$error = '';

// Handle actions
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $action = $_POST['action'] ?? '';
    $reportId = (int)($_POST['report_id'] ?? 0);

    if ($reportId > 0) {
        $report = $reportManager->getReport($reportId, false);

        if ($report) {
            switch ($action) {
                case 'approve':
                    $result = $reportManager->updateReport($reportId, [
                        'status' => 'published'
                    ]);
                    if ($result) {
                        // Update moderation info
                        $stmt = $pdo->prepare("
                            UPDATE race_reports
                            SET moderated_by = ?, moderated_at = NOW(), moderation_notes = CONCAT(COALESCE(moderation_notes, ''), '\n[', NOW(), '] Godkand av admin')
                            WHERE id = ?
                        ");
                        $stmt->execute([$_SESSION['admin_id'] ?? 0, $reportId]);
                        $message = 'Inlagg godkant och publicerat!';
                    } else {
                        $error = 'Kunde inte godkanna inlagg.';
                    }
                    break;

                case 'reject':
                    $reason = trim($_POST['reason'] ?? '');
                    $result = $reportManager->updateReport($reportId, [
                        'status' => 'archived'
                    ]);
                    if ($result) {
                        $stmt = $pdo->prepare("
                            UPDATE race_reports
                            SET moderated_by = ?, moderated_at = NOW(), moderation_notes = CONCAT(COALESCE(moderation_notes, ''), '\n[', NOW(), '] Avvisad: ', ?)
                            WHERE id = ?
                        ");
                        $stmt->execute([$_SESSION['admin_id'] ?? 0, $reason, $reportId]);
                        $message = 'Inlagg avvisat.';
                    } else {
                        $error = 'Kunde inte avvisa inlagg.';
                    }
                    break;

                case 'feature':
                    $result = $reportManager->updateReport($reportId, [
                        'is_featured' => 1
                    ]);
                    if ($result) {
                        $message = 'Inlagg markerat som utvalt!';
                    }
                    break;

                case 'unfeature':
                    $result = $reportManager->updateReport($reportId, [
                        'is_featured' => 0
                    ]);
                    if ($result) {
                        $message = 'Utvald-markering borttagen.';
                    }
                    break;

                case 'delete':
                    if ($reportManager->deleteReport($reportId)) {
                        $message = 'Inlagg borttaget permanent.';
                    } else {
                        $error = 'Kunde inte ta bort inlagg.';
                    }
                    break;
            }
        }
    }
}

// Get filter parameters
$filterStatus = $_GET['status'] ?? 'pending';
$filterPage = max(1, (int)($_GET['page'] ?? 1));
$perPage = 20;

// Map status filter to actual values
$statusMap = [
    'pending' => 'draft',
    'published' => 'published',
    'archived' => 'archived'
];
$statusFilter = $statusMap[$filterStatus] ?? null;

// Get reports
$filters = [
    'page' => $filterPage,
    'per_page' => $perPage,
    'include_drafts' => true,
    'order_by' => 'recent'
];

if ($statusFilter) {
    $filters['status'] = $statusFilter;
}

$result = $reportManager->listReports($filters);
$reports = $result['reports'];
$totalReports = $result['total'];
$totalPages = $result['total_pages'];

// Get stats
$stats = $reportManager->getStats();

// Count pending
$pendingCount = 0;
try {
    $pendingCount = $pdo->query("SELECT COUNT(*) FROM race_reports WHERE status = 'draft'")->fetchColumn();
} catch (Exception $e) {}

$page_title = 'Nyheter & Race Reports';
$breadcrumbs = [
    ['label' => 'Nyheter & Race Reports']
];
include __DIR__ . '/components/unified-layout.php';
?>

<div class="admin-content">
    <div class="page-header">
        <div class="page-header-content">
            <h1>
                <i data-lucide="newspaper"></i>
                <?= $page_title ?>
            </h1>
            <p class="page-subtitle">Moderera och hantera inlagg fran communityn</p>
        </div>
        <div class="page-header-actions">
            <a href="/news" class="btn btn-secondary" target="_blank">
                <i data-lucide="external-link"></i>
                Visa publikt
            </a>
        </div>
    </div>

    <?php if ($message): ?>
        <div class="alert alert-success mb-lg">
            <i data-lucide="check-circle"></i>
            <?= htmlspecialchars($message) ?>
        </div>
    <?php endif; ?>

    <?php if ($error): ?>
        <div class="alert alert-error mb-lg">
            <i data-lucide="alert-circle"></i>
            <?= htmlspecialchars($error) ?>
        </div>
    <?php endif; ?>

    <!-- Stats Cards -->
    <div class="stats-grid mb-xl">
        <div class="stat-card">
            <div class="stat-icon stat-icon-warning">
                <i data-lucide="clock"></i>
            </div>
            <div class="stat-content">
                <span class="stat-value"><?= $pendingCount ?></span>
                <span class="stat-label">Vantar pa granskning</span>
            </div>
        </div>
        <div class="stat-card">
            <div class="stat-icon stat-icon-success">
                <i data-lucide="check-circle"></i>
            </div>
            <div class="stat-content">
                <span class="stat-value"><?= $stats['published'] ?? 0 ?></span>
                <span class="stat-label">Publicerade</span>
            </div>
        </div>
        <div class="stat-card">
            <div class="stat-icon stat-icon-info">
                <i data-lucide="eye"></i>
            </div>
            <div class="stat-content">
                <span class="stat-value"><?= number_format($stats['total_views'] ?? 0) ?></span>
                <span class="stat-label">Totala visningar</span>
            </div>
        </div>
        <div class="stat-card">
            <div class="stat-icon stat-icon-accent">
                <i data-lucide="heart"></i>
            </div>
            <div class="stat-content">
                <span class="stat-value"><?= number_format($stats['total_likes'] ?? 0) ?></span>
                <span class="stat-label">Totala likes</span>
            </div>
        </div>
    </div>

    <!-- Filter Tabs -->
    <div class="filter-tabs mb-lg">
        <a href="?status=pending" class="filter-tab <?= $filterStatus === 'pending' ? 'active' : '' ?>">
            <i data-lucide="clock"></i>
            Vantar pa granskning
            <?php if ($pendingCount > 0): ?>
            <span class="filter-tab-badge"><?= $pendingCount ?></span>
            <?php endif; ?>
        </a>
        <a href="?status=published" class="filter-tab <?= $filterStatus === 'published' ? 'active' : '' ?>">
            <i data-lucide="check-circle"></i>
            Publicerade
        </a>
        <a href="?status=archived" class="filter-tab <?= $filterStatus === 'archived' ? 'active' : '' ?>">
            <i data-lucide="archive"></i>
            Arkiverade/Avvisade
        </a>
        <a href="?status=all" class="filter-tab <?= $filterStatus === 'all' ? 'active' : '' ?>">
            <i data-lucide="layers"></i>
            Alla
        </a>
    </div>

    <!-- Reports List -->
    <?php if (empty($reports)): ?>
        <div class="empty-state">
            <i data-lucide="inbox" class="icon-xl text-muted"></i>
            <h3>Inga inlagg</h3>
            <p>Det finns inga inlagg att visa med valda filter.</p>
        </div>
    <?php else: ?>
        <div class="card">
            <div class="table-responsive">
                <table class="table">
                    <thead>
                        <tr>
                            <th style="width: 50%">Inlagg</th>
                            <th>Skribent</th>
                            <th>Status</th>
                            <th>Datum</th>
                            <th class="text-right">Atgarder</th>
                        </tr>
                    </thead>
                    <tbody>
                        <?php foreach ($reports as $report): ?>
                        <tr>
                            <td>
                                <div class="report-cell">
                                    <?php if ($report['featured_image']): ?>
                                    <div class="report-thumb">
                                        <img src="<?= htmlspecialchars($report['featured_image']) ?>" alt="">
                                    </div>
                                    <?php elseif ($report['youtube_video_id']): ?>
                                    <div class="report-thumb">
                                        <img src="https://img.youtube.com/vi/<?= htmlspecialchars($report['youtube_video_id']) ?>/default.jpg" alt="">
                                        <span class="report-thumb-badge"><i data-lucide="play"></i></span>
                                    </div>
                                    <?php else: ?>
                                    <div class="report-thumb report-thumb-empty">
                                        <i data-lucide="file-text"></i>
                                    </div>
                                    <?php endif; ?>
                                    <div class="report-info">
                                        <a href="/news/<?= htmlspecialchars($report['slug']) ?>" target="_blank" class="report-title">
                                            <?= htmlspecialchars($report['title']) ?>
                                            <?php if ($report['is_featured']): ?>
                                            <span class="badge badge-accent">Utvalt</span>
                                            <?php endif; ?>
                                        </a>
                                        <?php if ($report['event_name']): ?>
                                        <span class="report-event">
                                            <i data-lucide="flag"></i>
                                            <?= htmlspecialchars($report['event_name']) ?>
                                        </span>
                                        <?php endif; ?>
                                        <?php if (!empty($report['tags'])): ?>
                                        <div class="report-tags">
                                            <?php foreach (array_slice($report['tags'], 0, 3) as $tag): ?>
                                            <span class="tag-pill"><?= htmlspecialchars($tag['name']) ?></span>
                                            <?php endforeach; ?>
                                        </div>
                                        <?php endif; ?>
                                    </div>
                                </div>
                            </td>
                            <td>
                                <a href="/rider/<?= $report['rider_id'] ?>" target="_blank">
                                    <?= htmlspecialchars($report['firstname'] . ' ' . $report['lastname']) ?>
                                </a>
                                <?php if ($report['club_name']): ?>
                                <br><small class="text-muted"><?= htmlspecialchars($report['club_name']) ?></small>
                                <?php endif; ?>
                            </td>
                            <td>
                                <?php
                                $statusConfigs = [
                                    'published' => ['class' => 'badge-success', 'text' => 'Publicerad'],
                                    'draft' => ['class' => 'badge-warning', 'text' => 'Vantar'],
                                    'archived' => ['class' => 'badge-muted', 'text' => 'Arkiverad']
                                ];
                                $statusConfig = $statusConfigs[$report['status']] ?? ['class' => '', 'text' => $report['status']];
                                ?>
                                <span class="badge <?= $statusConfig['class'] ?>"><?= $statusConfig['text'] ?></span>
                                <br>
                                <small class="text-muted">
                                    <i data-lucide="eye"></i> <?= number_format($report['views']) ?>
                                    &nbsp;
                                    <i data-lucide="heart"></i> <?= number_format($report['likes']) ?>
                                </small>
                            </td>
                            <td>
                                <span class="text-nowrap"><?= date('Y-m-d', strtotime($report['created_at'])) ?></span>
                                <br><small class="text-muted"><?= date('H:i', strtotime($report['created_at'])) ?></small>
                            </td>
                            <td class="text-right">
                                <div class="btn-group">
                                    <?php if ($report['status'] === 'draft'): ?>
                                    <form method="POST" style="display: inline;">
                                        <input type="hidden" name="action" value="approve">
                                        <input type="hidden" name="report_id" value="<?= $report['id'] ?>">
                                        <button type="submit" class="btn btn-sm btn-success" title="Godkann">
                                            <i data-lucide="check"></i>
                                        </button>
                                    </form>
                                    <button type="button" class="btn btn-sm btn-warning" onclick="showRejectModal(<?= $report['id'] ?>)" title="Avvisa">
                                        <i data-lucide="x"></i>
                                    </button>
                                    <?php endif; ?>

                                    <?php if ($report['status'] === 'published'): ?>
                                        <?php if (!$report['is_featured']): ?>
                                        <form method="POST" style="display: inline;">
                                            <input type="hidden" name="action" value="feature">
                                            <input type="hidden" name="report_id" value="<?= $report['id'] ?>">
                                            <button type="submit" class="btn btn-sm btn-secondary" title="Markera som utvalt">
                                                <i data-lucide="star"></i>
                                            </button>
                                        </form>
                                        <?php else: ?>
                                        <form method="POST" style="display: inline;">
                                            <input type="hidden" name="action" value="unfeature">
                                            <input type="hidden" name="report_id" value="<?= $report['id'] ?>">
                                            <button type="submit" class="btn btn-sm btn-accent" title="Ta bort utvalt">
                                                <i data-lucide="star-off"></i>
                                            </button>
                                        </form>
                                        <?php endif; ?>
                                    <?php endif; ?>

                                    <a href="/news/<?= htmlspecialchars($report['slug']) ?>" target="_blank" class="btn btn-sm btn-ghost" title="Forhandsgranska">
                                        <i data-lucide="external-link"></i>
                                    </a>

                                    <form method="POST" style="display: inline;" onsubmit="return confirm('Ta bort detta inlagg permanent?');">
                                        <input type="hidden" name="action" value="delete">
                                        <input type="hidden" name="report_id" value="<?= $report['id'] ?>">
                                        <button type="submit" class="btn btn-sm btn-ghost text-error" title="Ta bort">
                                            <i data-lucide="trash-2"></i>
                                        </button>
                                    </form>
                                </div>
                            </td>
                        </tr>
                        <?php endforeach; ?>
                    </tbody>
                </table>
            </div>
        </div>

        <!-- Pagination -->
        <?php if ($totalPages > 1): ?>
        <div class="pagination mt-lg">
            <?php if ($filterPage > 1): ?>
            <a href="?status=<?= $filterStatus ?>&page=<?= $filterPage - 1 ?>" class="pagination-btn">
                <i data-lucide="chevron-left"></i>
                Foregaende
            </a>
            <?php endif; ?>

            <span class="pagination-info">Sida <?= $filterPage ?> av <?= $totalPages ?></span>

            <?php if ($filterPage < $totalPages): ?>
            <a href="?status=<?= $filterStatus ?>&page=<?= $filterPage + 1 ?>" class="pagination-btn">
                Nasta
                <i data-lucide="chevron-right"></i>
            </a>
            <?php endif; ?>
        </div>
        <?php endif; ?>
    <?php endif; ?>
</div>

<!-- Reject Modal -->
<div class="modal" id="rejectModal">
    <div class="modal-backdrop" onclick="closeRejectModal()"></div>
    <div class="modal-content">
        <div class="modal-header">
            <h3>Avvisa inlagg</h3>
            <button type="button" class="modal-close" onclick="closeRejectModal()">
                <i data-lucide="x"></i>
            </button>
        </div>
        <form method="POST" id="rejectForm">
            <div class="modal-body">
                <input type="hidden" name="action" value="reject">
                <input type="hidden" name="report_id" id="rejectReportId">
                <div class="form-group">
                    <label class="form-label">Anledning (visas for skribenten)</label>
                    <textarea name="reason" class="form-textarea" rows="3" placeholder="Forklara varfor inlagget avvisas..."></textarea>
                </div>
            </div>
            <div class="modal-footer">
                <button type="button" class="btn btn-secondary" onclick="closeRejectModal()">Avbryt</button>
                <button type="submit" class="btn btn-warning">Avvisa inlagg</button>
            </div>
        </form>
    </div>
</div>

<style>
/* Report cell styling */
.report-cell {
    display: flex;
    gap: var(--space-md);
    align-items: flex-start;
}

.report-thumb {
    width: 80px;
    height: 60px;
    border-radius: var(--radius-sm);
    overflow: hidden;
    flex-shrink: 0;
    position: relative;
    background: var(--color-bg-surface);
}

.report-thumb img {
    width: 100%;
    height: 100%;
    object-fit: cover;
}

.report-thumb-empty {
    display: flex;
    align-items: center;
    justify-content: center;
    color: var(--color-text-muted);
}

.report-thumb-empty i {
    width: 24px;
    height: 24px;
}

.report-thumb-badge {
    position: absolute;
    bottom: 4px;
    right: 4px;
    width: 20px;
    height: 20px;
    background: rgba(0,0,0,0.7);
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    color: white;
}

.report-thumb-badge i {
    width: 10px;
    height: 10px;
}

.report-info {
    display: flex;
    flex-direction: column;
    gap: var(--space-2xs);
    min-width: 0;
}

.report-title {
    font-weight: 500;
    color: var(--color-text-primary);
    text-decoration: none;
    display: flex;
    align-items: center;
    gap: var(--space-xs);
}

.report-title:hover {
    color: var(--color-accent);
}

.report-event {
    font-size: 0.75rem;
    color: var(--color-text-muted);
    display: flex;
    align-items: center;
    gap: var(--space-2xs);
}

.report-event i {
    width: 12px;
    height: 12px;
}

.report-tags {
    display: flex;
    gap: var(--space-2xs);
    flex-wrap: wrap;
}

.tag-pill {
    font-size: 0.625rem;
    padding: 2px 6px;
    background: var(--color-accent-light);
    color: var(--color-accent);
    border-radius: var(--radius-sm);
}

/* Filter tabs */
.filter-tabs {
    display: flex;
    gap: var(--space-xs);
    border-bottom: 1px solid var(--color-border);
    padding-bottom: var(--space-xs);
}

.filter-tab {
    display: flex;
    align-items: center;
    gap: var(--space-xs);
    padding: var(--space-sm) var(--space-md);
    color: var(--color-text-secondary);
    text-decoration: none;
    border-radius: var(--radius-md) var(--radius-md) 0 0;
    transition: all 0.15s;
}

.filter-tab:hover {
    background: var(--color-bg-hover);
    color: var(--color-text-primary);
}

.filter-tab.active {
    background: var(--color-accent-light);
    color: var(--color-accent);
}

.filter-tab i {
    width: 16px;
    height: 16px;
}

.filter-tab-badge {
    padding: 2px 8px;
    background: var(--color-warning);
    color: white;
    font-size: 0.6875rem;
    font-weight: 600;
    border-radius: var(--radius-full);
}

/* Stats grid */
.stats-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: var(--space-md);
}

.stat-card {
    display: flex;
    align-items: center;
    gap: var(--space-md);
    background: var(--color-bg-card);
    border: 1px solid var(--color-border);
    border-radius: var(--radius-lg);
    padding: var(--space-lg);
}

.stat-icon {
    width: 48px;
    height: 48px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: var(--radius-md);
}

.stat-icon i {
    width: 24px;
    height: 24px;
}

.stat-icon-warning {
    background: rgba(251, 191, 36, 0.15);
    color: var(--color-warning);
}

.stat-icon-success {
    background: rgba(16, 185, 129, 0.15);
    color: var(--color-success);
}

.stat-icon-info {
    background: rgba(56, 189, 248, 0.15);
    color: var(--color-info);
}

.stat-icon-accent {
    background: var(--color-accent-light);
    color: var(--color-accent);
}

.stat-content {
    display: flex;
    flex-direction: column;
}

.stat-value {
    font-size: 1.5rem;
    font-weight: 700;
    color: var(--color-text-primary);
    line-height: 1;
}

.stat-label {
    font-size: 0.75rem;
    color: var(--color-text-muted);
    margin-top: var(--space-2xs);
}

/* Modal */
.modal {
    display: none;
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    z-index: 1000;
    align-items: center;
    justify-content: center;
}

.modal.active {
    display: flex;
}

.modal-backdrop {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(0,0,0,0.5);
}

.modal-content {
    position: relative;
    background: var(--color-bg-card);
    border-radius: var(--radius-lg);
    width: 100%;
    max-width: 500px;
    box-shadow: 0 20px 60px rgba(0,0,0,0.3);
}

.modal-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: var(--space-lg);
    border-bottom: 1px solid var(--color-border);
}

.modal-header h3 {
    margin: 0;
    font-size: 1.125rem;
}

.modal-close {
    background: none;
    border: none;
    color: var(--color-text-muted);
    cursor: pointer;
    padding: var(--space-xs);
}

.modal-close:hover {
    color: var(--color-text-primary);
}

.modal-body {
    padding: var(--space-lg);
}

.modal-footer {
    display: flex;
    justify-content: flex-end;
    gap: var(--space-sm);
    padding: var(--space-lg);
    border-top: 1px solid var(--color-border);
}

/* Responsive */
@media (max-width: 1024px) {
    .stats-grid {
        grid-template-columns: repeat(2, 1fr);
    }
}

@media (max-width: 767px) {
    .stats-grid {
        grid-template-columns: 1fr;
    }

    .filter-tabs {
        flex-wrap: wrap;
    }

    .report-cell {
        flex-direction: column;
    }

    .report-thumb {
        width: 100%;
        height: 120px;
    }
}
</style>

<script>
function showRejectModal(reportId) {
    document.getElementById('rejectReportId').value = reportId;
    document.getElementById('rejectModal').classList.add('active');
}

function closeRejectModal() {
    document.getElementById('rejectModal').classList.remove('active');
}

// Close modal on escape
document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape') {
        closeRejectModal();
    }
});
</script>

<?php include __DIR__ . '/components/unified-layout-footer.php'; ?>
