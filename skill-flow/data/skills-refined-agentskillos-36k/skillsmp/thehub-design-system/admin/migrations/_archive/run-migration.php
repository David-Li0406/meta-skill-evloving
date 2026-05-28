<?php
/**
 * Run a single SQL migration file
 * Usage: /admin/run-migration.php?file=071_club_points_system.sql
 */
require_once __DIR__ . '/../config.php';
require_admin();

$db = getDB();
$pdo = $db->getPdo();

$file = $_GET['file'] ?? '';
$migrationPath = __DIR__ . '/../database/migrations/' . basename($file);

$message = '';
$messageType = 'info';

// Handle form submission
if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['run_migration'])) {
    checkCsrf();

    if (!file_exists($migrationPath)) {
        $message = "Migrationen finns inte: {$file}";
        $messageType = 'error';
    } else {
        try {
            $sql = file_get_contents($migrationPath);

            // Split by semicolons and execute each statement
            $statements = array_filter(array_map('trim', preg_split('/;\s*$/m', $sql)));
            $executed = 0;

            foreach ($statements as $statement) {
                if (empty($statement) || strpos(trim($statement), '--') === 0) {
                    continue;
                }
                $pdo->exec($statement);
                $executed++;
            }

            $message = "Migration kördes! {$executed} SQL-satser utförda.";
            $messageType = 'success';
        } catch (PDOException $e) {
            $message = "Fel vid migration: " . $e->getMessage();
            $messageType = 'error';
        }
    }
}

// Read migration content for preview
$migrationContent = '';
if (file_exists($migrationPath)) {
    $migrationContent = file_get_contents($migrationPath);
}

$page_title = 'Kör migration: ' . $file;
$breadcrumbs = [
    ['label' => 'Verktyg', 'url' => '/admin/tools'],
    ['label' => 'Migration']
];

include __DIR__ . '/components/unified-layout.php';
?>

<?php if ($message): ?>
<div class="admin-alert admin-alert-<?= $messageType ?>">
    <?= h($message) ?>
</div>
<?php endif; ?>

<?php if (!file_exists($migrationPath)): ?>
<div class="admin-alert admin-alert-error">
    Migrationen "<?= h($file) ?>" finns inte i database/migrations/
</div>
<?php else: ?>

<div class="admin-card">
    <div class="admin-card-header">
        <h3>Migration: <?= h($file) ?></h3>
    </div>
    <div class="admin-card-body">
        <p class="admin-help-text">Granska SQL-koden nedan innan du kör migrationen.</p>

        <pre style="background: #f5f5f5; padding: 1rem; border-radius: 8px; overflow-x: auto; max-height: 400px; font-size: 0.85rem;"><?= h($migrationContent) ?></pre>

        <form method="POST" style="margin-top: 1rem;">
            <?= csrf_field() ?>
            <button type="submit" name="run_migration" class="btn-admin btn-admin-primary"
                    onclick="return confirm('Kör migrationen nu?\n\nDetta kan göra permanenta ändringar i databasen.')">
                Kör migration
            </button>
            <a href="/admin/tools" class="btn-admin btn-admin-secondary" style="margin-left: 0.5rem;">
                Avbryt
            </a>
        </form>
    </div>
</div>

<?php endif; ?>

<?php include __DIR__ . '/components/unified-layout-footer.php'; ?>
