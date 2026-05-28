<?php
/**
 * Race Reports Management - Admin Page (Super Admin Only)
 * TheHUB - Manage race reports/blog posts from riders
 */
require_once __DIR__ . '/../config.php';
require_once __DIR__ . '/../includes/RaceReportManager.php';
require_once __DIR__ . '/../includes/GlobalSponsorManager.php';

global $pdo;

// Require super admin
if (!hasRole('super_admin')) {
    header('Location: /admin/');
    exit;
}

$reportManager = new RaceReportManager($pdo);
$sponsorManager = new GlobalSponsorManager($pdo);

// Handle form submissions
$message = '';
$error = '';

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $action = $_POST['action'] ?? '';

    if ($action === 'update_status') {
        $report_id = (int)$_POST['report_id'];
        $status = $_POST['status'];
        if ($reportManager->updateReport($report_id, ['status' => $status])) {
            $message = 'Status uppdaterad!';
        } else {
            $error = 'Kunde inte uppdatera status.';
        }
    } elseif ($action === 'toggle_featured') {
        $report_id = (int)$_POST['report_id'];
        $is_featured = (int)$_POST['is_featured'];
        if ($reportManager->updateReport($report_id, ['is_featured' => $is_featured ? 0 : 1])) {
            $message = 'Featured-status uppdaterad!';
        } else {
            $error = 'Kunde inte uppdatera.';
        }
    } elseif ($action === 'delete_report') {
        $report_id = (int)$_POST['report_id'];
        if ($reportManager->deleteReport($report_id)) {
            $message = 'Report borttagen!';
        } else {
            $error = 'Kunde inte ta bort report.';
        }
    } elseif ($action === 'update_setting') {
        $key = $_POST['setting_key'];
        $value = $_POST['setting_value'];
        if ($sponsorManager->updateSetting($key, $value)) {
            $message = 'Inställning sparad!';
        } else {
            $error = 'Kunde inte spara inställning.';
        }
    }
}

// Get filters
$statusFilter = $_GET['status'] ?? '';
$page = (int)($_GET['page'] ?? 1);

// Get reports with admin view (include drafts)
$filters = [
    'page' => $page,
    'per_page' => 20,
    'include_drafts' => true,
    'order_by' => 'recent'
];

if ($statusFilter) {
    $filters['status'] = $statusFilter;
}

$result = $reportManager->listReports($filters);
$reports = $result['reports'];
$totalPages = $result['total_pages'];

// Get stats
$stats = $reportManager->getStats();

// Get settings
$publicEnabled = $sponsorManager->getSetting('race_reports_public', '0');

// Get all tags
$tags = $reportManager->getAllTags();

// Page config
$page_title = 'Race Reports';
$breadcrumbs = [
    ['label' => 'Sponsorer', 'url' => '/admin/sponsors.php'],
    ['label' => 'Race Reports']
];

// Include unified layout
include __DIR__ . '/components/unified-layout.php';
?>

<link rel="stylesheet" href="/assets/css/sponsors-blog.css">

<style>
/* Page-specific styles */
.stats-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
    gap: var(--space-md);
    margin-bottom: var(--space-lg);
}

.stat-card {
    background: var(--color-bg-surface);
    border: 1px solid var(--color-border);
    border-radius: var(--radius-md);
    padding: var(--space-md);
    text-align: center;
}

.stat-value {
    font-size: 2rem;
    font-weight: 700;
    color: var(--color-accent);
}

.stat-label {
    font-size: 0.75rem;
    color: var(--color-text-muted);
    text-transform: uppercase;
}

.settings-section {
    background: var(--color-bg-surface);
    border: 1px solid var(--color-border);
    border-radius: var(--radius-md);
    padding: var(--space-lg);
    margin-bottom: var(--space-lg);
}

.settings-section h3 {
    margin: 0 0 var(--space-md);
    font-size: 1.125rem;
}

.setting-row {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: var(--space-sm) 0;
    border-bottom: 1px solid var(--color-border);
}

.setting-row:last-child {
    border-bottom: none;
}

.setting-label strong {
    display: block;
    color: var(--color-text-primary);
}

.setting-label small {
    color: var(--color-text-muted);
}

.toggle-switch {
    position: relative;
    width: 50px;
    height: 26px;
}

.toggle-switch input {
    opacity: 0;
    width: 0;
    height: 0;
}

.toggle-slider {
    position: absolute;
    cursor: pointer;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background-color: var(--color-border);
    transition: .4s;
    border-radius: 26px;
}

.toggle-slider:before {
    position: absolute;
    content: "";
    height: 20px;
    width: 20px;
    left: 3px;
    bottom: 3px;
    background-color: white;
    transition: .4s;
    border-radius: 50%;
}

input:checked + .toggle-slider {
    background-color: var(--color-accent);
}

input:checked + .toggle-slider:before {
    transform: translateX(24px);
}

.filters-bar {
    display: flex;
    gap: var(--space-sm);
    margin-bottom: var(--space-lg);
    flex-wrap: wrap;
}

.filter-btn {
    padding: var(--space-xs) var(--space-md);
    border: 1px solid var(--color-border);
    border-radius: var(--radius-sm);
    background: var(--color-bg-surface);
    color: var(--color-text-secondary);
    text-decoration: none;
    font-size: 0.875rem;
}

.filter-btn:hover,
.filter-btn.active {
    background: var(--color-accent);
    border-color: var(--color-accent);
    color: white;
}

.report-card {
    background: var(--color-bg-surface);
    border: 1px solid var(--color-border);
    border-radius: var(--radius-md);
    padding: var(--space-md);
    margin-bottom: var(--space-md);
    display: grid;
    grid-template-columns: auto 1fr auto;
    gap: var(--space-md);
    align-items: center;
}

.report-image {
    width: 100px;
    height: 60px;
    border-radius: var(--radius-sm);
    object-fit: cover;
    background: var(--color-bg-page);
}

.report-info {
    min-width: 0;
}

.report-title {
    font-weight: 600;
    color: var(--color-text-primary);
    margin-bottom: var(--space-2xs);
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

.report-meta {
    display: flex;
    gap: var(--space-md);
    font-size: 0.75rem;
    color: var(--color-text-muted);
    flex-wrap: wrap;
}

.report-meta-item {
    display: flex;
    align-items: center;
    gap: var(--space-2xs);
}

.status-badge {
    display: inline-block;
    padding: 2px 8px;
    border-radius: 10px;
    font-size: 0.65rem;
    font-weight: 600;
    text-transform: uppercase;
}

.status-published {
    background: rgba(16, 185, 129, 0.2);
    color: var(--color-success);
}

.status-draft {
    background: rgba(251, 191, 36, 0.2);
    color: var(--color-warning);
}

.status-archived {
    background: rgba(156, 163, 175, 0.2);
    color: var(--color-text-muted);
}

.featured-badge {
    display: inline-flex;
    align-items: center;
    gap: var(--space-2xs);
    padding: 2px 8px;
    background: rgba(139, 92, 246, 0.2);
    color: #8B5CF6;
    border-radius: 10px;
    font-size: 0.65rem;
    font-weight: 600;
}

.report-actions {
    display: flex;
    gap: var(--space-xs);
    flex-shrink: 0;
}

.alert {
    padding: var(--space-md);
    border-radius: var(--radius-sm);
    margin-bottom: var(--space-md);
}

.alert-success {
    background: rgba(16, 185, 129, 0.1);
    border: 1px solid var(--color-success);
    color: var(--color-success);
}

.alert-error {
    background: rgba(239, 68, 68, 0.1);
    border: 1px solid var(--color-error);
    color: var(--color-error);
}

.pagination {
    display: flex;
    gap: var(--space-xs);
    justify-content: center;
    margin-top: var(--space-lg);
}

.pagination a {
    padding: var(--space-xs) var(--space-sm);
    border: 1px solid var(--color-border);
    border-radius: var(--radius-sm);
    text-decoration: none;
    color: var(--color-text-secondary);
}

.pagination a:hover,
.pagination a.active {
    background: var(--color-accent);
    border-color: var(--color-accent);
    color: white;
}

.tags-cloud {
    display: flex;
    flex-wrap: wrap;
    gap: var(--space-xs);
    margin-top: var(--space-md);
}

.tag-item {
    padding: var(--space-2xs) var(--space-sm);
    background: var(--color-bg-page);
    border-radius: var(--radius-sm);
    font-size: 0.75rem;
    color: var(--color-text-secondary);
}
</style>

<?php if ($message): ?>
    <div class="alert alert-success"><?= htmlspecialchars($message) ?></div>
<?php endif; ?>

<?php if ($error): ?>
    <div class="alert alert-error"><?= htmlspecialchars($error) ?></div>
<?php endif; ?>

<!-- Stats -->
<div class="stats-grid">
    <div class="stat-card">
        <div class="stat-value"><?= number_format($stats['total'] ?? 0) ?></div>
        <div class="stat-label">Totalt</div>
    </div>
    <div class="stat-card">
        <div class="stat-value"><?= number_format($stats['published'] ?? 0) ?></div>
        <div class="stat-label">Publicerade</div>
    </div>
    <div class="stat-card">
        <div class="stat-value"><?= number_format($stats['drafts'] ?? 0) ?></div>
        <div class="stat-label">Utkast</div>
    </div>
    <div class="stat-card">
        <div class="stat-value"><?= number_format($stats['total_views'] ?? 0) ?></div>
        <div class="stat-label">Visningar</div>
    </div>
    <div class="stat-card">
        <div class="stat-value"><?= number_format($stats['total_likes'] ?? 0) ?></div>
        <div class="stat-label">Likes</div>
    </div>
</div>

<!-- Settings -->
<div class="settings-section">
    <h3><i data-lucide="settings"></i> Inställningar</h3>

    <div class="setting-row">
        <div class="setting-label">
            <strong>Publik synlighet</strong>
            <small>Visa race reports för vanliga besökare (inte bara admin)</small>
        </div>
        <form method="POST" style="display: inline;">
            <input type="hidden" name="action" value="update_setting">
            <input type="hidden" name="setting_key" value="race_reports_public">
            <input type="hidden" name="setting_value" value="<?= $publicEnabled === '1' ? '0' : '1' ?>">
            <label class="toggle-switch">
                <input type="checkbox" <?= $publicEnabled === '1' ? 'checked' : '' ?> onchange="this.form.submit()">
                <span class="toggle-slider"></span>
            </label>
        </form>
    </div>
</div>

<!-- Filters -->
<div class="filters-bar">
    <a href="?status=" class="filter-btn <?= !$statusFilter ? 'active' : '' ?>">Alla</a>
    <a href="?status=published" class="filter-btn <?= $statusFilter === 'published' ? 'active' : '' ?>">Publicerade</a>
    <a href="?status=draft" class="filter-btn <?= $statusFilter === 'draft' ? 'active' : '' ?>">Utkast</a>
    <a href="?status=archived" class="filter-btn <?= $statusFilter === 'archived' ? 'active' : '' ?>">Arkiverade</a>
</div>

<!-- Reports List -->
<?php if (empty($reports)): ?>
    <div class="card">
        <div class="card-body" style="text-align: center; padding: var(--space-2xl);">
            <i data-lucide="file-text" style="width: 48px; height: 48px; color: var(--color-text-muted);"></i>
            <p style="margin-top: var(--space-md); color: var(--color-text-muted);">
                Inga race reports än. Riders kan skapa reports via sin profil.
            </p>
        </div>
    </div>
<?php else: ?>
    <?php foreach ($reports as $report): ?>
        <div class="report-card">
            <?php if ($report['featured_image']): ?>
                <img src="<?= htmlspecialchars($report['featured_image']) ?>"
                     alt="" class="report-image">
            <?php else: ?>
                <div class="report-image" style="display: flex; align-items: center; justify-content: center;">
                    <i data-lucide="image" style="color: var(--color-text-muted);"></i>
                </div>
            <?php endif; ?>

            <div class="report-info">
                <div class="report-title"><?= htmlspecialchars($report['title']) ?></div>
                <div class="report-meta">
                    <span class="report-meta-item">
                        <i data-lucide="user"></i>
                        <?= htmlspecialchars(($report['firstname'] ?? '') . ' ' . ($report['lastname'] ?? '')) ?>
                    </span>
                    <span class="report-meta-item">
                        <i data-lucide="calendar"></i>
                        <?= $report['published_at'] ? date('Y-m-d', strtotime($report['published_at'])) : 'Ej publicerad' ?>
                    </span>
                    <span class="report-meta-item">
                        <i data-lucide="eye"></i>
                        <?= number_format($report['views']) ?>
                    </span>
                    <span class="report-meta-item">
                        <i data-lucide="heart"></i>
                        <?= number_format($report['likes']) ?>
                    </span>
                    <span class="status-badge status-<?= $report['status'] ?>">
                        <?= $report['status'] ?>
                    </span>
                    <?php if ($report['is_featured']): ?>
                        <span class="featured-badge">
                            <i data-lucide="star"></i> Featured
                        </span>
                    <?php endif; ?>
                </div>
            </div>

            <div class="report-actions">
                <!-- Toggle Featured -->
                <form method="POST" style="display: inline;">
                    <input type="hidden" name="action" value="toggle_featured">
                    <input type="hidden" name="report_id" value="<?= $report['id'] ?>">
                    <input type="hidden" name="is_featured" value="<?= $report['is_featured'] ?>">
                    <button type="submit" class="btn btn-ghost btn-sm" title="<?= $report['is_featured'] ? 'Ta bort featured' : 'Markera featured' ?>">
                        <i data-lucide="<?= $report['is_featured'] ? 'star-off' : 'star' ?>"></i>
                    </button>
                </form>

                <!-- Status Dropdown -->
                <form method="POST" style="display: inline;">
                    <input type="hidden" name="action" value="update_status">
                    <input type="hidden" name="report_id" value="<?= $report['id'] ?>">
                    <select name="status" onchange="this.form.submit()" class="btn btn-ghost btn-sm" style="padding: var(--space-xs);">
                        <option value="draft" <?= $report['status'] === 'draft' ? 'selected' : '' ?>>Utkast</option>
                        <option value="published" <?= $report['status'] === 'published' ? 'selected' : '' ?>>Publicerad</option>
                        <option value="archived" <?= $report['status'] === 'archived' ? 'selected' : '' ?>>Arkiverad</option>
                    </select>
                </form>

                <!-- Delete -->
                <form method="POST" style="display: inline;" onsubmit="return confirm('Ta bort denna report?');">
                    <input type="hidden" name="action" value="delete_report">
                    <input type="hidden" name="report_id" value="<?= $report['id'] ?>">
                    <button type="submit" class="btn btn-ghost btn-sm" title="Ta bort">
                        <i data-lucide="trash-2"></i>
                    </button>
                </form>
            </div>
        </div>
    <?php endforeach; ?>

    <!-- Pagination -->
    <?php if ($totalPages > 1): ?>
        <div class="pagination">
            <?php for ($i = 1; $i <= $totalPages; $i++): ?>
                <a href="?page=<?= $i ?>&status=<?= htmlspecialchars($statusFilter) ?>"
                   class="<?= $i === $page ? 'active' : '' ?>">
                    <?= $i ?>
                </a>
            <?php endfor; ?>
        </div>
    <?php endif; ?>
<?php endif; ?>

<!-- Tags -->
<?php if (!empty($tags)): ?>
    <div class="settings-section" style="margin-top: var(--space-lg);">
        <h3><i data-lucide="tag"></i> Taggar</h3>
        <div class="tags-cloud">
            <?php foreach ($tags as $tag): ?>
                <span class="tag-item">
                    <?= htmlspecialchars($tag['name']) ?>
                    (<?= $tag['usage_count'] ?>)
                </span>
            <?php endforeach; ?>
        </div>
    </div>
<?php endif; ?>

<script>
lucide.createIcons();
</script>
