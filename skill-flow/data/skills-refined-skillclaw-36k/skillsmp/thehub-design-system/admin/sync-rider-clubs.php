<?php
/**
 * Sync Rider Clubs - Sets rider club_id based on their most recent results
 * For riders without a club, finds their most recent club from rider_club_seasons
 */
require_once __DIR__ . '/../config.php';
require_admin();

if (!hasRole('super_admin') && !hasRole('admin')) {
    header('Location: /admin?error=access_denied');
    exit;
}

$db = getDB();
$message = '';
$messageType = 'info';
$stats = [];

// Handle sync request
if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['sync_clubs'])) {
    checkCsrf();

    try {
        $updated = 0;
        $skipped = 0;
        $noData = 0;

        // Find riders without a club_id
        $ridersWithoutClub = $db->getAll("
            SELECT id, firstname, lastname
            FROM riders
            WHERE club_id IS NULL OR club_id = 0
        ");

        foreach ($ridersWithoutClub as $rider) {
            // Try to get club from rider_club_seasons (most recent year first)
            $seasonClub = $db->getRow("
                SELECT club_id, season_year
                FROM rider_club_seasons
                WHERE rider_id = ? AND club_id IS NOT NULL
                ORDER BY season_year DESC
                LIMIT 1
            ", [$rider['id']]);

            if ($seasonClub && $seasonClub['club_id']) {
                $db->update('riders', ['club_id' => $seasonClub['club_id']], 'id = ?', [$rider['id']]);
                $updated++;
            } else {
                // No club in rider_club_seasons - try to get from results table
                $resultClub = $db->getRow("
                    SELECT r.club_id, e.date
                    FROM results r
                    JOIN events e ON r.event_id = e.id
                    WHERE r.cyclist_id = ? AND r.club_id IS NOT NULL
                    ORDER BY e.date DESC
                    LIMIT 1
                ", [$rider['id']]);

                if ($resultClub && $resultClub['club_id']) {
                    $db->update('riders', ['club_id' => $resultClub['club_id']], 'id = ?', [$rider['id']]);
                    $updated++;
                } else {
                    $noData++;
                }
            }
        }

        // Also count how many riders now have clubs
        $stats['updated'] = $updated;
        $stats['no_data'] = $noData;
        $stats['total_checked'] = count($ridersWithoutClub);

        $message = "Synkronisering klar! {$updated} ryttare uppdaterade. {$noData} ryttare saknar klubbdata.";
        $messageType = 'success';

    } catch (Exception $e) {
        $message = 'Fel vid synkronisering: ' . $e->getMessage();
        $messageType = 'error';
    }
}

// Get current stats
$totalRiders = (int)($db->getRow("SELECT COUNT(*) as c FROM riders")['c'] ?? 0);
$ridersWithClub = (int)($db->getRow("SELECT COUNT(*) as c FROM riders WHERE club_id IS NOT NULL AND club_id > 0")['c'] ?? 0);
$ridersWithoutClub = $totalRiders - $ridersWithClub;

// Page config
$page_title = 'Synka Ryttarklubbkopplingar';
$breadcrumbs = [
    ['label' => 'Verktyg'],
    ['label' => 'Synka Klubbar']
];
include __DIR__ . '/components/unified-layout.php';
?>

<?php if ($message): ?>
<div class="alert alert-<?= $messageType === 'success' ? 'success' : ($messageType === 'error' ? 'danger' : 'info') ?> mb-lg">
    <i data-lucide="<?= $messageType === 'success' ? 'check-circle' : 'alert-circle' ?>"></i>
    <?= h($message) ?>
</div>
<?php endif; ?>

<div class="card">
    <div class="card-header">
        <h2 class="text-primary">
            <i data-lucide="link"></i>
            Synka Ryttarklubbkopplingar
        </h2>
    </div>
    <div class="card-body">
        <p class="mb-lg">
            Detta verktyg hittar ryttare utan klubbkoppling och kopplar dem till sin senaste klubb
            baserat på historiska resultat eller rider_club_seasons-tabellen.
        </p>

        <div class="admin-stats-grid mb-lg">
            <div class="admin-stat-card">
                <div class="admin-stat-content">
                    <div class="admin-stat-value"><?= number_format($totalRiders) ?></div>
                    <div class="admin-stat-label">Totalt ryttare</div>
                </div>
            </div>
            <div class="admin-stat-card">
                <div class="admin-stat-content">
                    <div class="admin-stat-value text-success"><?= number_format($ridersWithClub) ?></div>
                    <div class="admin-stat-label">Med klubbkoppling</div>
                </div>
            </div>
            <div class="admin-stat-card">
                <div class="admin-stat-content">
                    <div class="admin-stat-value text-warning"><?= number_format($ridersWithoutClub) ?></div>
                    <div class="admin-stat-label">Utan klubbkoppling</div>
                </div>
            </div>
        </div>

        <?php if ($ridersWithoutClub > 0): ?>
        <form method="POST">
            <?= csrf_field() ?>
            <button type="submit" name="sync_clubs" class="btn btn--primary btn-lg">
                <i data-lucide="refresh-cw"></i>
                Synka <?= number_format($ridersWithoutClub) ?> ryttare till klubbar
            </button>
        </form>
        <?php else: ?>
        <div class="alert alert-success">
            <i data-lucide="check-circle"></i>
            Alla ryttare har redan en klubbkoppling!
        </div>
        <?php endif; ?>
    </div>
</div>

<?php if (!empty($stats)): ?>
<div class="card mt-lg">
    <div class="card-header">
        <h3>
            <i data-lucide="bar-chart-2"></i>
            Resultat
        </h3>
    </div>
    <div class="card-body">
        <table class="table">
            <tr>
                <td>Kontrollerade ryttare</td>
                <td><strong><?= number_format($stats['total_checked']) ?></strong></td>
            </tr>
            <tr>
                <td>Uppdaterade med klubb</td>
                <td><strong class="text-success"><?= number_format($stats['updated']) ?></strong></td>
            </tr>
            <tr>
                <td>Saknar historisk klubbdata</td>
                <td><strong class="text-warning"><?= number_format($stats['no_data']) ?></strong></td>
            </tr>
        </table>
    </div>
</div>
<?php endif; ?>

<div class="card mt-lg">
    <div class="card-header">
        <h3>
            <i data-lucide="info"></i>
            Hur det fungerar
        </h3>
    </div>
    <div class="card-body">
        <ol class="mb-0">
            <li>Hittar alla ryttare utan <code>club_id</code> i riders-tabellen</li>
            <li>Letar efter klubb i <code>rider_club_seasons</code> (senaste året)</li>
            <li>Om ingen finns, letar i <code>results</code>-tabellen (senaste resultatet)</li>
            <li>Uppdaterar <code>riders.club_id</code> med funnen klubb</li>
        </ol>
    </div>
</div>

<?php include __DIR__ . '/components/unified-layout-footer.php'; ?>
