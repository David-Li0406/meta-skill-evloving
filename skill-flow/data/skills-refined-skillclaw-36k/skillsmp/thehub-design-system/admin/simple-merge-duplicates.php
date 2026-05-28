<?php
/**
 * Simple Duplicate Merge - Hittar dubletter med samma enkla matchning som preview
 */
require_once __DIR__ . '/../config.php';
require_admin();

$db = getDB();
$pdo = $db->getPdo();

$message = '';
$stats = ['merged' => 0, 'results_moved' => 0];

// Slå ihop om POST
if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['merge_all'])) {
    checkCsrf();

    try {
        $pdo->beginTransaction();

        // Hitta alla dubletter baserat på exakt namn (samma som preview)
        $duplicates = $pdo->query("
            SELECT firstname, lastname, GROUP_CONCAT(id ORDER BY id) as ids, COUNT(*) as cnt
            FROM riders
            WHERE firstname IS NOT NULL AND firstname != ''
            AND lastname IS NOT NULL AND lastname != ''
            GROUP BY firstname, lastname
            HAVING cnt > 1
        ")->fetchAll(PDO::FETCH_ASSOC);

        foreach ($duplicates as $dup) {
            $ids = explode(',', $dup['ids']);
            $keepId = array_shift($ids); // Behåll första (lägst ID)

            foreach ($ids as $removeId) {
                // Flytta resultat
                $stmt = $pdo->prepare("UPDATE results SET cyclist_id = ? WHERE cyclist_id = ?");
                $stmt->execute([$keepId, $removeId]);
                $stats['results_moved'] += $stmt->rowCount();

                // Flytta series_results
                $pdo->prepare("UPDATE series_results SET cyclist_id = ? WHERE cyclist_id = ?")->execute([$keepId, $removeId]);

                // Ta bort dubletten
                $pdo->prepare("DELETE FROM riders WHERE id = ?")->execute([$removeId]);
            }
            $stats['merged']++;
        }

        $pdo->commit();
        $message = "Klart! Slog ihop {$stats['merged']} dubblettgrupper, flyttade {$stats['results_moved']} resultat.";

    } catch (Exception $e) {
        $pdo->rollBack();
        $message = "Fel: " . $e->getMessage();
    }
}

// Hitta dubletter för visning
$duplicates = $pdo->query("
    SELECT firstname, lastname, GROUP_CONCAT(id ORDER BY id) as ids, COUNT(*) as cnt
    FROM riders
    WHERE firstname IS NOT NULL AND firstname != ''
    AND lastname IS NOT NULL AND lastname != ''
    GROUP BY firstname, lastname
    HAVING cnt > 1
    ORDER BY cnt DESC
    LIMIT 100
")->fetchAll(PDO::FETCH_ASSOC);

$totalDuplicateRiders = 0;
foreach ($duplicates as $dup) {
    $totalDuplicateRiders += $dup['cnt'] - 1; // Räkna bort den vi behåller
}

$pageTitle = 'Snabb dubblettsammanslagning';
include __DIR__ . '/../includes/admin-header.php';
?>

<div class="admin-content">
    <div class="page-header">
        <h1><i data-lucide="git-merge"></i> <?= $pageTitle ?></h1>
    </div>

    <?php if ($message): ?>
    <div class="alert alert-<?= strpos($message, 'Fel') === 0 ? 'error' : 'success' ?> mb-lg">
        <?= h($message) ?>
    </div>
    <?php endif; ?>

    <div class="card mb-lg">
        <div class="card-header">
            <h3>Hittade <?= count($duplicates) ?> dubblettgrupper (<?= $totalDuplicateRiders ?> extra åkare)</h3>
        </div>
        <div class="card-body">
            <?php if (empty($duplicates)): ?>
            <div class="alert alert-success">
                <i data-lucide="check-circle"></i> Inga dubletter hittades!
            </div>
            <?php else: ?>
            <div class="alert alert-warning mb-lg">
                <strong>Detta verktyg slår ihop åkare med EXAKT samma för- och efternamn.</strong><br>
                Första åkaren (lägst ID) behålls, alla resultat flyttas dit, resten raderas.
            </div>

            <form method="POST" onsubmit="return confirm('Slå ihop ALLA <?= count($duplicates) ?> dubblettgrupper?')">
                <?= csrf_field() ?>
                <button type="submit" name="merge_all" class="btn btn-danger btn-lg mb-lg">
                    <i data-lucide="git-merge"></i>
                    Slå ihop alla <?= count($duplicates) ?> dubblettgrupper
                </button>
            </form>

            <div class="table-responsive" style="max-height: 500px; overflow: auto;">
                <table class="table table-sm">
                    <thead>
                        <tr>
                            <th>Namn</th>
                            <th>Antal</th>
                            <th>IDs</th>
                        </tr>
                    </thead>
                    <tbody>
                        <?php foreach ($duplicates as $dup): ?>
                        <tr>
                            <td><strong><?= h($dup['firstname'] . ' ' . $dup['lastname']) ?></strong></td>
                            <td><span class="badge badge-warning"><?= $dup['cnt'] ?></span></td>
                            <td><code><?= h($dup['ids']) ?></code></td>
                        </tr>
                        <?php endforeach; ?>
                    </tbody>
                </table>
            </div>
            <?php endif; ?>
        </div>
    </div>
</div>

<?php include __DIR__ . '/../includes/admin-footer.php'; ?>
