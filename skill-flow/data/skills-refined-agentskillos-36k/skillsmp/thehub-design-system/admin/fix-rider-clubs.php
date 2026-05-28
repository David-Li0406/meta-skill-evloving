<?php
/**
 * Fix Rider Clubs - Uppdatera alla åkares klubbtillhörighet från resultat
 */
require_once __DIR__ . '/../config.php';
require_admin();

$db = getDB();

// Kör uppdatering om POST
if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['run_fix'])) {
    checkCsrf();

    $stats = [
        'riders_updated' => 0,
        'riders_skipped' => 0,
        'errors' => []
    ];

    // Hitta alla åkare utan klubb men som har resultat med klubb
    $ridersToFix = $db->getAll("
        SELECT DISTINCT r.id as rider_id, r.firstname, r.lastname, r.club_id as current_club_id
        FROM riders r
        WHERE r.club_id IS NULL
        AND EXISTS (
            SELECT 1 FROM results res WHERE res.cyclist_id = r.id AND res.club_id IS NOT NULL
        )
    ");

    foreach ($ridersToFix as $rider) {
        // Hämta senaste resultat med klubb för denna åkare
        $latestResult = $db->getRow("
            SELECT res.club_id, c.name as club_name, e.date
            FROM results res
            JOIN clubs c ON res.club_id = c.id
            JOIN events e ON res.event_id = e.id
            WHERE res.cyclist_id = ? AND res.club_id IS NOT NULL
            ORDER BY e.date DESC
            LIMIT 1
        ", [$rider['rider_id']]);

        if ($latestResult && $latestResult['club_id']) {
            $db->update('riders',
                ['club_id' => $latestResult['club_id']],
                'id = ?',
                [$rider['rider_id']]
            );
            $stats['riders_updated']++;
        } else {
            $stats['riders_skipped']++;
        }
    }

    // Även uppdatera åkare som har klubb men där resultaten har annan klubb (ta senaste)
    if (isset($_POST['update_all'])) {
        $allRidersWithResults = $db->getAll("
            SELECT DISTINCT r.id as rider_id, r.firstname, r.lastname, r.club_id as current_club_id
            FROM riders r
            WHERE EXISTS (
                SELECT 1 FROM results res WHERE res.cyclist_id = r.id AND res.club_id IS NOT NULL
            )
        ");

        foreach ($allRidersWithResults as $rider) {
            $latestResult = $db->getRow("
                SELECT res.club_id, c.name as club_name, e.date
                FROM results res
                JOIN clubs c ON res.club_id = c.id
                JOIN events e ON res.event_id = e.id
                WHERE res.cyclist_id = ? AND res.club_id IS NOT NULL
                ORDER BY e.date DESC
                LIMIT 1
            ", [$rider['rider_id']]);

            if ($latestResult && $latestResult['club_id'] && $latestResult['club_id'] != $rider['current_club_id']) {
                $db->update('riders',
                    ['club_id' => $latestResult['club_id']],
                    'id = ?',
                    [$rider['rider_id']]
                );
                $stats['riders_updated']++;
            }
        }
    }

    $message = "Klart! {$stats['riders_updated']} åkare uppdaterade, {$stats['riders_skipped']} hoppades över.";
    $messageType = 'success';
}

// Hämta statistik
$totalRiders = $db->getRow("SELECT COUNT(*) as cnt FROM riders")['cnt'];
$ridersWithClub = $db->getRow("SELECT COUNT(*) as cnt FROM riders WHERE club_id IS NOT NULL")['cnt'];
$ridersWithoutClub = $totalRiders - $ridersWithClub;

$ridersFixable = $db->getRow("
    SELECT COUNT(DISTINCT r.id) as cnt
    FROM riders r
    WHERE r.club_id IS NULL
    AND EXISTS (
        SELECT 1 FROM results res WHERE res.cyclist_id = r.id AND res.club_id IS NOT NULL
    )
")['cnt'];

// Exempel på åkare som kan fixas
$exampleRiders = $db->getAll("
    SELECT r.id, r.firstname, r.lastname,
           (SELECT c.name FROM results res
            JOIN clubs c ON res.club_id = c.id
            JOIN events e ON res.event_id = e.id
            WHERE res.cyclist_id = r.id AND res.club_id IS NOT NULL
            ORDER BY e.date DESC LIMIT 1) as suggested_club
    FROM riders r
    WHERE r.club_id IS NULL
    AND EXISTS (
        SELECT 1 FROM results res WHERE res.cyclist_id = r.id AND res.club_id IS NOT NULL
    )
    LIMIT 10
");

$pageTitle = 'Fixa åkares klubbtillhörighet';
include __DIR__ . '/../includes/admin-header.php';
?>

<div class="admin-content">
    <div class="page-header">
        <h1><i data-lucide="building"></i> <?= $pageTitle ?></h1>
    </div>

    <?php if (isset($message)): ?>
    <div class="alert alert-<?= $messageType ?> mb-lg">
        <?= h($message) ?>
    </div>
    <?php endif; ?>

    <div class="grid grid-cols-1 md-grid-cols-3 gap-lg mb-lg">
        <div class="stat-card">
            <div class="stat-number"><?= number_format($totalRiders) ?></div>
            <div class="stat-label">Totalt åkare</div>
        </div>
        <div class="stat-card">
            <div class="stat-number text-success"><?= number_format($ridersWithClub) ?></div>
            <div class="stat-label">Med klubb</div>
        </div>
        <div class="stat-card">
            <div class="stat-number text-warning"><?= number_format($ridersWithoutClub) ?></div>
            <div class="stat-label">Utan klubb</div>
        </div>
    </div>

    <div class="card mb-lg">
        <div class="card-header">
            <h3>Åkare som kan fixas automatiskt</h3>
        </div>
        <div class="card-body">
            <p class="mb-md">
                <strong><?= number_format($ridersFixable) ?></strong> åkare saknar klubb men har resultat med klubbinfo.
            </p>

            <?php if (!empty($exampleRiders)): ?>
            <p class="text-sm text-secondary mb-md">Exempel (första 10):</p>
            <div class="table-responsive" style="max-height: 300px;">
                <table class="table table-sm">
                    <thead>
                        <tr>
                            <th>Åkare</th>
                            <th>Föreslagen klubb (senaste resultat)</th>
                        </tr>
                    </thead>
                    <tbody>
                        <?php foreach ($exampleRiders as $rider): ?>
                        <tr>
                            <td><?= h($rider['firstname'] . ' ' . $rider['lastname']) ?></td>
                            <td><span class="badge badge-primary"><?= h($rider['suggested_club'] ?? '-') ?></span></td>
                        </tr>
                        <?php endforeach; ?>
                    </tbody>
                </table>
            </div>
            <?php endif; ?>
        </div>
    </div>

    <div class="card">
        <div class="card-header">
            <h3>Kör uppdatering</h3>
        </div>
        <div class="card-body">
            <form method="POST">
                <?= csrf_field() ?>

                <div class="form-group mb-md">
                    <label class="flex items-center gap-sm">
                        <input type="checkbox" name="update_all" value="1">
                        <span>Uppdatera ALLA åkare (även de som redan har klubb) till senaste resultat</span>
                    </label>
                </div>

                <button type="submit" name="run_fix" class="btn btn-primary btn-lg">
                    <i data-lucide="play"></i>
                    Kör uppdatering (<?= number_format($ridersFixable) ?> åkare)
                </button>
            </form>
        </div>
    </div>
</div>

<?php include __DIR__ . '/../includes/admin-footer.php'; ?>
