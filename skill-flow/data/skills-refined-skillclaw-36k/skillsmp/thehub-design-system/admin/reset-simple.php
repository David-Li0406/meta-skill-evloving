<?php
/**
 * Simple Reset Tool
 */
require_once __DIR__ . '/../config.php';
require_admin();

if (!hasRole('super_admin')) {
    die('Endast superadmin');
}

$db = getDB();
$message = '';
$error = '';

// Handle reset
if ($_POST['confirm'] ?? '' === 'RADERA ALLT') {
    try {
        $db->pdo->exec("SET FOREIGN_KEY_CHECKS = 0");

        $tables = [
            'ranking_snapshots',
            'club_ranking_snapshots',
            'ranking_history',
            'series_results',
            'rider_club_seasons',
            'rider_parents',
            'rider_claims',
            'results',
            'registrations',
            'club_points',
            'club_points_riders',
            'riders',
            'clubs',
        ];

        foreach ($tables as $t) {
            try {
                $db->pdo->exec("DELETE FROM `$t`");
                $db->pdo->exec("ALTER TABLE `$t` AUTO_INCREMENT = 1");
            } catch (Exception $e) {
                // skip
            }
        }

        $db->pdo->exec("SET FOREIGN_KEY_CHECKS = 1");
        $message = 'Data raderad!';
    } catch (Exception $e) {
        $error = $e->getMessage();
    }
}

// Count
$riders = $db->getRow("SELECT COUNT(*) as c FROM riders")['c'] ?? 0;
$clubs = $db->getRow("SELECT COUNT(*) as c FROM clubs")['c'] ?? 0;
$results = $db->getRow("SELECT COUNT(*) as c FROM results")['c'] ?? 0;

// Page config
$page_title = 'Enkel återställning';
$breadcrumbs = [
    ['label' => 'Verktyg', 'url' => '/admin/tools.php'],
    ['label' => 'Enkel återställning']
];

include __DIR__ . '/components/unified-layout.php';
?>

<?php if ($message): ?>
    <div class="alert alert-success"><?= htmlspecialchars($message) ?></div>
<?php endif; ?>

<?php if ($error): ?>
    <div class="alert alert-danger">Fel: <?= htmlspecialchars($error) ?></div>
<?php endif; ?>

<div class="card">
    <div class="card-header">
        <h3>Nuvarande data</h3>
    </div>
    <div class="card-body">
        <table class="table">
            <tr><td>Åkare</td><td><strong><?= number_format($riders) ?></strong></td></tr>
            <tr><td>Klubbar</td><td><strong><?= number_format($clubs) ?></strong></td></tr>
            <tr><td>Resultat</td><td><strong><?= number_format($results) ?></strong></td></tr>
        </table>
    </div>
</div>

<?php if ($riders > 0 || $clubs > 0): ?>
<div class="card" style="margin-top: var(--space-md);">
    <div class="card-header">
        <h3 class="text-danger">Radera all data</h3>
    </div>
    <div class="card-body">
        <div class="alert alert-danger" style="margin-bottom: var(--space-md);">
            <strong>VARNING!</strong> Detta raderar ALL data i systemet.
        </div>
        <p>Skriv <strong>RADERA ALLT</strong> för att bekräfta:</p>
        <form method="POST" style="margin-top: var(--space-md);">
            <div class="form-group" style="display: flex; gap: var(--space-sm); align-items: center;">
                <input type="text" name="confirm" class="form-input" placeholder="Skriv här..." style="max-width: 200px;">
                <button type="submit" class="btn btn-danger">Radera</button>
            </div>
        </form>
    </div>
</div>
<?php else: ?>
<div class="alert alert-success" style="margin-top: var(--space-md);">
    Databasen är tom - redo för import!
</div>
<?php endif; ?>

<div style="margin-top: var(--space-lg);">
    <a href="/admin/import.php" class="btn btn-primary">Gå till Import</a>
</div>

<?php include __DIR__ . '/components/unified-layout-footer.php'; ?>
