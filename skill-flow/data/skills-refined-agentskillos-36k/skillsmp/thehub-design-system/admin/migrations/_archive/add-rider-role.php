<?php
/**
 * Quick Migration: Add rider role to admin_users ENUM
 * Migration 065
 */
require_once __DIR__ . '/../../config.php';
require_admin();

// Only super_admin can run migrations
if (!hasRole('super_admin')) {
    http_response_code(403);
    die('Access denied');
}

$db = getDB();
$message = '';
$messageType = '';
$alreadyDone = false;

// Check current ENUM values
try {
    $result = $db->query("SHOW COLUMNS FROM admin_users WHERE Field = 'role'");
    $row = $result->fetch(PDO::FETCH_ASSOC);
    $currentType = $row['Type'] ?? '';

    if (strpos($currentType, "'rider'") !== false) {
        $alreadyDone = true;
        $message = 'Migrationen har redan körts - rider-rollen finns redan i databasen.';
        $messageType = 'success';
    }
} catch (Exception $e) {
    $message = 'Kunde inte kontrollera status: ' . $e->getMessage();
    $messageType = 'error';
}

// Handle migration
if ($_SERVER['REQUEST_METHOD'] === 'POST' && !$alreadyDone) {
    checkCsrf();

    try {
        $sql = "ALTER TABLE admin_users
                MODIFY COLUMN role ENUM('super_admin', 'admin', 'editor', 'promotor', 'rider') DEFAULT 'rider'";

        $db->query($sql);

        $message = 'Migration 065 har körts! Rider-rollen är nu tillgänglig.';
        $messageType = 'success';
        $alreadyDone = true;
    } catch (Exception $e) {
        $message = 'Fel vid körning av migration: ' . $e->getMessage();
        $messageType = 'error';
    }
}

// Page config
$page_title = 'Migration: Lägg till rider-roll';
$breadcrumbs = [
    ['label' => 'Inställningar', 'url' => '/admin/settings'],
    ['label' => 'Verktyg', 'url' => '/admin/tools'],
    ['label' => 'Lägg till rider-roll']
];
$page_actions = '<a href="/admin/tools" class="btn btn--secondary"><i data-lucide="arrow-left"></i> Tillbaka</a>';

include __DIR__ . '/../components/unified-layout.php';
?>

<div class="gs-max-w-600">
    <div class="card">
        <div class="card-header">
            <h2>Migration 065: Lägg till rider-roll</h2>
        </div>
        <div class="card-body">
            <?php if ($message): ?>
                <div class="alert alert-<?= $messageType ?> mb-lg">
                    <i data-lucide="<?= $messageType === 'success' ? 'check-circle' : 'alert-circle' ?>"></i>
                    <?= htmlspecialchars($message) ?>
                </div>
            <?php endif; ?>

            <div class="mb-lg">
                <h4>Vad gör denna migration?</h4>
                <p class="text-secondary">
                    Lägger till <code>rider</code> som ett giltigt värde i ENUM-fältet <code>role</code>
                    i tabellen <code>admin_users</code>. Detta gör att användare kan skapas med rider-rollen
                    via admin-panelen.
                </p>
            </div>

            <div class="mb-lg" style="background: var(--color-bg-subtle); padding: var(--space-md); border-radius: var(--radius-md);">
                <h5 class="mb-sm">SQL som körs:</h5>
                <code style="font-size: var(--text-sm); white-space: pre-wrap;">ALTER TABLE admin_users
MODIFY COLUMN role ENUM('super_admin', 'admin', 'editor', 'promotor', 'rider') DEFAULT 'rider';</code>
            </div>

            <?php if (!$alreadyDone): ?>
                <form method="POST">
                    <?= csrf_field() ?>
                    <button type="submit" class="btn btn--primary">
                        <i data-lucide="play"></i>
                        Kör migration
                    </button>
                </form>
            <?php else: ?>
                <div class="flex items-center gap-sm text-success">
                    <i data-lucide="check-circle"></i>
                    <span>Migrationen är redan genomförd</span>
                </div>
            <?php endif; ?>
        </div>
    </div>
</div>

<?php include __DIR__ . '/../components/unified-layout-footer.php'; ?>
