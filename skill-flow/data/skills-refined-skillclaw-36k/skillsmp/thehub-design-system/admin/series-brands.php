<?php
/**
 * Admin Series Brands - V3 Design System
 * Manage parent series (brands) like "Swecup", "GravitySeries Enduro" etc.
 */
require_once __DIR__ . '/../config.php';
require_admin();

$pdo = $GLOBALS['pdo'];

// Get session messages from create/edit pages
$message = $_SESSION['message'] ?? '';
$messageType = $_SESSION['messageType'] ?? 'info';
unset($_SESSION['message'], $_SESSION['messageType']);

// Check if series_brands table exists
$tableExists = false;
try {
    $check = $pdo->query("SHOW TABLES LIKE 'series_brands'")->fetchAll();
    $tableExists = !empty($check);
} catch (Exception $e) {
    $tableExists = false;
}

if (!$tableExists) {
    $page_title = 'Serie-varumärken';
    $page_group = 'standings';
    include __DIR__ . '/components/unified-layout.php';
    ?>
    <div class="alert alert-warning">
        <i data-lucide="alert-triangle"></i>
        Tabellen <code>series_brands</code> finns inte. Kör migrationen först.
    </div>
    <div class="admin-card">
        <div class="admin-card-body">
            <p>Kör följande migration för att skapa tabellen:</p>
            <code>database/migrations/050_add_series_brands.sql</code>
        </div>
    </div>
    <?php
    include __DIR__ . '/components/unified-layout-footer.php';
    exit;
}

// Handle delete action
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    checkCsrf();

    $action = $_POST['action'] ?? '';

    if ($action === 'delete') {
        $id = intval($_POST['id']);
        try {
            // First unlink any series using this brand
            $stmt = $pdo->prepare("UPDATE series SET brand_id = NULL WHERE brand_id = ?");
            $stmt->execute([$id]);

            $stmt = $pdo->prepare("DELETE FROM series_brands WHERE id = ?");
            $stmt->execute([$id]);

            $message = 'Varumärke borttaget!';
            $messageType = 'success';
        } catch (Exception $e) {
            $message = 'Ett fel uppstod: ' . $e->getMessage();
            $messageType = 'error';
        }
    }
}

// Get all brands with series count
$stmt = $pdo->query("
    SELECT sb.*,
           COUNT(s.id) as series_count
    FROM series_brands sb
    LEFT JOIN series s ON s.brand_id = sb.id
    GROUP BY sb.id
    ORDER BY sb.display_order ASC, sb.name ASC
");
$brands = $stmt->fetchAll(PDO::FETCH_ASSOC);

// Get unassigned series count
$unassignedCount = $pdo->query("SELECT COUNT(*) as cnt FROM series WHERE brand_id IS NULL")->fetch(PDO::FETCH_ASSOC);
$unassignedSeries = $unassignedCount['cnt'] ?? 0;

// Page config
$page_title = 'Serie-varumärken';
$page_group = 'standings';
$page_actions = '<a href="/admin/series-brands-create.php" class="btn-admin btn-admin-primary">
    <i data-lucide="plus"></i>
    Nytt varumärke
</a>';

include __DIR__ . '/components/unified-layout.php';
?>

<?php if ($message): ?>
    <div class="alert alert-<?= $messageType === 'success' ? 'success' : ($messageType === 'error' ? 'error' : 'info') ?>">
        <i data-lucide="<?= $messageType === 'success' ? 'check-circle' : 'alert-circle' ?>"></i>
        <?= htmlspecialchars($message) ?>
    </div>
<?php endif; ?>

<!-- Stats Grid -->
<div class="grid grid-stats grid-gap-md">
    <div class="admin-stat-card">
        <div class="admin-stat-icon" style="background: var(--color-info-light); color: var(--color-info);">
            <i data-lucide="trophy"></i>
        </div>
        <div class="admin-stat-content">
            <div class="admin-stat-value"><?= count($brands) ?></div>
            <div class="admin-stat-label">Varumärken</div>
        </div>
    </div>

    <div class="admin-stat-card">
        <div class="admin-stat-icon" style="background: var(--color-success-light); color: var(--color-success);">
            <i data-lucide="check-circle"></i>
        </div>
        <div class="admin-stat-content">
            <div class="admin-stat-value"><?= count(array_filter($brands, fn($b) => $b['active'])) ?></div>
            <div class="admin-stat-label">Aktiva</div>
        </div>
    </div>

    <div class="admin-stat-card">
        <div class="admin-stat-icon" style="background: var(--color-warning-light); color: var(--color-warning);">
            <i data-lucide="alert-circle"></i>
        </div>
        <div class="admin-stat-content">
            <div class="admin-stat-value"><?= $unassignedSeries ?></div>
            <div class="admin-stat-label">Otilldelade serier</div>
        </div>
    </div>
</div>

<!-- Brands Table -->
<div class="admin-card">
    <div class="admin-card-header">
        <h2><?= count($brands) ?> varumärken</h2>
    </div>
    <div class="admin-card-body" style="padding: 0;">
        <?php if (empty($brands)): ?>
            <div class="admin-empty-state">
                <i data-lucide="trophy" style="width: 48px; height: 48px; opacity: 0.5;"></i>
                <h3>Inga varumärken hittades</h3>
                <p>Skapa ett varumärke för att gruppera serier.</p>
                <a href="/admin/series-brands-create.php" class="btn-admin btn-admin-primary">Skapa varumärke</a>
            </div>
        <?php else: ?>
            <div class="admin-table-container">
                <table class="admin-table">
                    <thead>
                        <tr>
                            <th style="width: 60px;">Logo</th>
                            <th>Namn</th>
                            <th>Färg</th>
                            <th>Serier</th>
                            <th>Status</th>
                            <th>Ordning</th>
                            <th style="width: 120px;">Åtgärder</th>
                        </tr>
                    </thead>
                    <tbody>
                        <?php foreach ($brands as $brand): ?>
                            <tr>
                                <td>
                                    <?php if ($brand['logo']): ?>
                                        <img src="<?= htmlspecialchars($brand['logo']) ?>" alt="" style="max-width: 40px; max-height: 40px; object-fit: contain;">
                                    <?php else: ?>
                                        <span class="text-secondary">-</span>
                                    <?php endif; ?>
                                </td>
                                <td>
                                    <a href="/admin/series-brands-edit.php?id=<?= $brand['id'] ?>" class="brand-name-link">
                                        <strong><?= htmlspecialchars($brand['name']) ?></strong>
                                    </a>
                                </td>
                                <td>
                                    <div class="color-swatch-mini" style="background: <?= htmlspecialchars($brand['accent_color'] ?? $brand['gradient_start'] ?? '#004A98') ?>;"></div>
                                </td>
                                <td>
                                    <span class="admin-badge admin-badge-info"><?= $brand['series_count'] ?></span>
                                </td>
                                <td>
                                    <?php if ($brand['active']): ?>
                                        <span class="admin-badge admin-badge-success">Aktiv</span>
                                    <?php else: ?>
                                        <span class="admin-badge admin-badge-secondary">Inaktiv</span>
                                    <?php endif; ?>
                                </td>
                                <td><?= $brand['display_order'] ?></td>
                                <td>
                                    <div class="table-actions">
                                        <a href="/admin/series-brands-edit.php?id=<?= $brand['id'] ?>" class="btn-admin btn-admin-sm btn-admin-secondary" title="Redigera">
                                            <i data-lucide="pencil"></i>
                                        </a>
                                        <button onclick="deleteBrand(<?= $brand['id'] ?>, '<?= addslashes($brand['name']) ?>')" class="btn-admin btn-admin-sm btn-admin-danger" title="Ta bort">
                                            <i data-lucide="trash-2"></i>
                                        </button>
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
.brand-name-link {
    color: inherit;
    text-decoration: none;
}

.brand-name-link:hover {
    color: var(--color-accent);
}

.color-swatch-mini {
    width: 24px;
    height: 24px;
    border-radius: var(--radius-sm);
    border: 2px solid var(--color-border);
}

.admin-empty-state {
    padding: var(--space-2xl);
    text-align: center;
    color: var(--color-text-secondary);
}

.admin-empty-state h3 {
    margin: var(--space-md) 0 var(--space-xs);
    color: var(--color-text);
}

.admin-empty-state p {
    margin: 0 0 var(--space-lg);
}
</style>

<script>
const csrfToken = '<?= htmlspecialchars(generate_csrf_token()) ?>';

function deleteBrand(id, name) {
    if (!confirm('Är du säker på att du vill ta bort "' + name + '"?\n\nAlla serier kopplade till detta varumärke blir otilldelade.')) {
        return;
    }

    const form = document.createElement('form');
    form.method = 'POST';
    form.innerHTML = '<input type="hidden" name="action" value="delete">' +
                     '<input type="hidden" name="id" value="' + id + '">' +
                     '<input type="hidden" name="csrf_token" value="' + csrfToken + '">';
    document.body.appendChild(form);
    form.submit();
}

// Initialize Lucide icons
document.addEventListener('DOMContentLoaded', function() {
    if (typeof lucide !== 'undefined') {
        lucide.createIcons();
    }
});
</script>

<?php include __DIR__ . '/components/unified-layout-footer.php'; ?>
