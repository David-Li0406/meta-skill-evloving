<?php
/**
 * Merge Specific Riders - Slå ihop två specifika åkare manuellt
 */
require_once __DIR__ . '/../config.php';
require_admin();

$db = getDB();
$pdo = $db->getPdo();

$message = '';
$messageType = 'info';

// Hantera sammanslagning
if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['merge'])) {
    checkCsrf();

    $keepId = (int)$_POST['keep_id'];
    $removeId = (int)$_POST['remove_id'];

    if ($keepId === $removeId) {
        $message = "Kan inte slå ihop en åkare med sig själv!";
        $messageType = 'error';
    } elseif ($keepId > 0 && $removeId > 0) {
        try {
            $pdo->beginTransaction();

            // Flytta resultat
            $stmt = $pdo->prepare("UPDATE results SET cyclist_id = ? WHERE cyclist_id = ?");
            $stmt->execute([$keepId, $removeId]);
            $resultsMoved = $stmt->rowCount();

            // Flytta series_results
            $stmt = $pdo->prepare("UPDATE series_results SET cyclist_id = ? WHERE cyclist_id = ?");
            $stmt->execute([$keepId, $removeId]);
            $seriesResultsMoved = $stmt->rowCount();

            // Flytta elimination_qualifying
            $eliminationMoved = 0;
            try {
                $stmt = $pdo->prepare("UPDATE elimination_qualifying SET rider_id = ? WHERE rider_id = ?");
                $stmt->execute([$keepId, $removeId]);
                $eliminationMoved += $stmt->rowCount();
            } catch (Exception $e) {
                // Table might not exist
            }

            // Flytta elimination_brackets (alla rider-fält)
            try {
                $stmt = $pdo->prepare("UPDATE elimination_brackets SET rider_1_id = ? WHERE rider_1_id = ?");
                $stmt->execute([$keepId, $removeId]);
                $eliminationMoved += $stmt->rowCount();

                $stmt = $pdo->prepare("UPDATE elimination_brackets SET rider_2_id = ? WHERE rider_2_id = ?");
                $stmt->execute([$keepId, $removeId]);
                $eliminationMoved += $stmt->rowCount();

                $stmt = $pdo->prepare("UPDATE elimination_brackets SET winner_id = ? WHERE winner_id = ?");
                $stmt->execute([$keepId, $removeId]);
                $eliminationMoved += $stmt->rowCount();

                $stmt = $pdo->prepare("UPDATE elimination_brackets SET loser_id = ? WHERE loser_id = ?");
                $stmt->execute([$keepId, $removeId]);
                $eliminationMoved += $stmt->rowCount();
            } catch (Exception $e) {
                // Table might not exist
            }

            // Flytta elimination_results
            try {
                $stmt = $pdo->prepare("UPDATE elimination_results SET rider_id = ? WHERE rider_id = ?");
                $stmt->execute([$keepId, $removeId]);
                $eliminationMoved += $stmt->rowCount();
            } catch (Exception $e) {
                // Table might not exist
            }

            // Flytta event_registrations
            $regMoved = 0;
            try {
                // First delete any duplicate registrations (same event, keep has registration already)
                $pdo->prepare("
                    DELETE er1 FROM event_registrations er1
                    INNER JOIN event_registrations er2 ON er1.event_id = er2.event_id
                    WHERE er1.rider_id = ? AND er2.rider_id = ?
                ")->execute([$removeId, $keepId]);

                $stmt = $pdo->prepare("UPDATE event_registrations SET rider_id = ? WHERE rider_id = ?");
                $stmt->execute([$keepId, $removeId]);
                $regMoved += $stmt->rowCount();
            } catch (Exception $e) {
                // Table might not exist
            }

            // Flytta event_tickets
            try {
                $pdo->prepare("
                    DELETE et1 FROM event_tickets et1
                    INNER JOIN event_tickets et2 ON et1.event_id = et2.event_id
                    WHERE et1.rider_id = ? AND et2.rider_id = ?
                ")->execute([$removeId, $keepId]);

                $stmt = $pdo->prepare("UPDATE event_tickets SET rider_id = ? WHERE rider_id = ?");
                $stmt->execute([$keepId, $removeId]);
                $regMoved += $stmt->rowCount();
            } catch (Exception $e) {
                // Table might not exist
            }

            // Flytta club_rider_points
            try {
                $stmt = $pdo->prepare("UPDATE club_rider_points SET rider_id = ? WHERE rider_id = ?");
                $stmt->execute([$keepId, $removeId]);
            } catch (Exception $e) {
                // Table might not exist
            }

            // Flytta event_refund_requests
            try {
                $stmt = $pdo->prepare("UPDATE event_refund_requests SET rider_id = ? WHERE rider_id = ?");
                $stmt->execute([$keepId, $removeId]);
            } catch (Exception $e) {
                // Table might not exist
            }

            // Flytta rider_claims (update both columns)
            try {
                $pdo->prepare("UPDATE rider_claims SET claimant_rider_id = ? WHERE claimant_rider_id = ?")->execute([$keepId, $removeId]);
                $pdo->prepare("UPDATE rider_claims SET target_rider_id = ? WHERE target_rider_id = ?")->execute([$keepId, $removeId]);
            } catch (Exception $e) {
                // Table might not exist
            }

            // Ta bort dubletten
            $pdo->prepare("DELETE FROM riders WHERE id = ?")->execute([$removeId]);

            $pdo->commit();

            $msg = "Klart! Flyttade {$resultsMoved} resultat, {$seriesResultsMoved} serieresultat";
            if ($eliminationMoved > 0) {
                $msg .= ", {$eliminationMoved} elimination-poster";
            }
            if ($regMoved > 0) {
                $msg .= ", {$regMoved} anmälningar/biljetter";
            }
            $msg .= " från ID {$removeId} till ID {$keepId}. Åkare {$removeId} raderad.";
            $message = $msg;
            $messageType = 'success';
        } catch (Exception $e) {
            $pdo->rollBack();
            $message = "Fel: " . $e->getMessage();
            $messageType = 'error';
        }
    }
}

// Hämta åkare för jämförelse
$rider1 = null;
$rider2 = null;
$rider1Id = isset($_GET['id1']) ? (int)$_GET['id1'] : null;
$rider2Id = isset($_GET['id2']) ? (int)$_GET['id2'] : null;

if ($rider1Id) {
    $rider1 = $db->getRow("
        SELECT r.*, c.name as club_name,
               (SELECT COUNT(*) FROM results WHERE cyclist_id = r.id) as result_count
        FROM riders r
        LEFT JOIN clubs c ON r.club_id = c.id
        WHERE r.id = ?
    ", [$rider1Id]);
}

if ($rider2Id) {
    $rider2 = $db->getRow("
        SELECT r.*, c.name as club_name,
               (SELECT COUNT(*) FROM results WHERE cyclist_id = r.id) as result_count
        FROM riders r
        LEFT JOIN clubs c ON r.club_id = c.id
        WHERE r.id = ?
    ", [$rider2Id]);
}

// Visa senaste dubbletter - optimerad query
// Först hitta namn som har dubbletter, sedan hämta detaljerna
$recentDuplicates = $db->getAll("
    WITH duplicate_names AS (
        SELECT LOWER(TRIM(firstname)) as fn, LOWER(TRIM(lastname)) as ln
        FROM riders
        WHERE firstname IS NOT NULL AND lastname IS NOT NULL
        GROUP BY LOWER(TRIM(firstname)), LOWER(TRIM(lastname))
        HAVING COUNT(*) > 1
        LIMIT 100
    )
    SELECT r1.id as id1, r2.id as id2,
           r1.firstname as name1_first, r1.lastname as name1_last,
           r2.firstname as name2_first, r2.lastname as name2_last,
           r1.license_number as license1, r2.license_number as license2,
           COALESCE(res1.cnt, 0) as results1,
           COALESCE(res2.cnt, 0) as results2
    FROM duplicate_names dn
    JOIN riders r1 ON LOWER(TRIM(r1.firstname)) = dn.fn AND LOWER(TRIM(r1.lastname)) = dn.ln
    JOIN riders r2 ON LOWER(TRIM(r2.firstname)) = dn.fn AND LOWER(TRIM(r2.lastname)) = dn.ln AND r1.id < r2.id
    LEFT JOIN (SELECT cyclist_id, COUNT(*) as cnt FROM results GROUP BY cyclist_id) res1 ON res1.cyclist_id = r1.id
    LEFT JOIN (SELECT cyclist_id, COUNT(*) as cnt FROM results GROUP BY cyclist_id) res2 ON res2.cyclist_id = r2.id
    ORDER BY r2.id DESC
    LIMIT 50
");

$page_title = 'Slå ihop specifika åkare';
$breadcrumbs = [
    ['label' => 'Verktyg', 'url' => '/admin/tools'],
    ['label' => 'Slå ihop åkare']
];
include __DIR__ . '/components/unified-layout.php';
?>

<h1 class="text-primary mb-lg">
    <i data-lucide="git-merge"></i> Slå ihop specifika åkare
</h1>

<?php if ($message): ?>
<div class="alert alert-<?= $messageType ?> mb-lg">
    <?= h($message) ?>
</div>
<?php endif; ?>

<!-- Sök efter åkare -->
<div class="card mb-lg">
    <div class="card-header">
        <h3><i data-lucide="search"></i> Välj två åkare att jämföra</h3>
    </div>
    <div class="card-body">
        <form method="GET" class="grid grid-cols-2 gap-md">
            <div class="form-group">
                <label class="form-label">Åkare 1 (ID)</label>
                <input type="number" name="id1" class="form-input" value="<?= $rider1Id ?>" placeholder="t.ex. 16470">
            </div>
            <div class="form-group">
                <label class="form-label">Åkare 2 (ID)</label>
                <input type="number" name="id2" class="form-input" value="<?= $rider2Id ?>" placeholder="t.ex. 17264">
            </div>
            <div class="col-span-2">
                <button type="submit" class="btn btn-primary">
                    <i data-lucide="search"></i> Jämför
                </button>
            </div>
        </form>
    </div>
</div>

<?php if ($rider1 && $rider2): ?>
<!-- Jämförelse -->
<div class="card mb-lg">
    <div class="card-header">
        <h3><i data-lucide="git-compare"></i> Jämförelse</h3>
    </div>
    <div class="card-body">
        <div class="table-responsive">
            <table class="table">
                <thead>
                    <tr>
                        <th>Fält</th>
                        <th>Åkare <?= $rider1['id'] ?></th>
                        <th>Åkare <?= $rider2['id'] ?></th>
                        <th>Match?</th>
                    </tr>
                </thead>
                <tbody>
                    <?php
                    $fields = [
                        'firstname' => 'Förnamn',
                        'lastname' => 'Efternamn',
                        'license_number' => 'UCI-ID/Licens',
                        'uci_id' => 'UCI-ID (alt)',
                        'club_name' => 'Klubb',
                        'birth_year' => 'Födelseår',
                        'gender' => 'Kön',
                        'result_count' => 'Antal resultat'
                    ];
                    foreach ($fields as $field => $label):
                        $val1 = $rider1[$field] ?? '';
                        $val2 = $rider2[$field] ?? '';
                        $match = (strtolower(trim($val1)) === strtolower(trim($val2)));
                    ?>
                    <tr>
                        <td><strong><?= $label ?></strong></td>
                        <td><?= h($val1) ?: '<em class="text-muted">-</em>' ?></td>
                        <td><?= h($val2) ?: '<em class="text-muted">-</em>' ?></td>
                        <td>
                            <?php if ($match): ?>
                            <span class="badge badge-success">✓</span>
                            <?php else: ?>
                            <span class="badge badge-warning">≠</span>
                            <?php endif; ?>
                        </td>
                    </tr>
                    <?php endforeach; ?>
                </tbody>
            </table>
        </div>

        <div class="alert alert-warning mt-lg mb-lg">
            <strong>Välj vilken åkare som ska behållas.</strong> Alla resultat flyttas dit och den andra raderas.
        </div>

        <div class="grid grid-cols-2 gap-lg">
            <form method="POST" onsubmit="return confirm('Behåll åkare <?= $rider1['id'] ?> och radera <?= $rider2['id'] ?>?')">
                <?= csrf_field() ?>
                <input type="hidden" name="keep_id" value="<?= $rider1['id'] ?>">
                <input type="hidden" name="remove_id" value="<?= $rider2['id'] ?>">
                <button type="submit" name="merge" class="btn btn-primary w-full">
                    <i data-lucide="arrow-left"></i>
                    Behåll <?= $rider1['id'] ?>, radera <?= $rider2['id'] ?>
                </button>
                <div class="text-center text-sm text-muted mt-sm">
                    <?= $rider1['result_count'] ?> + <?= $rider2['result_count'] ?> = <?= $rider1['result_count'] + $rider2['result_count'] ?> resultat
                </div>
            </form>

            <form method="POST" onsubmit="return confirm('Behåll åkare <?= $rider2['id'] ?> och radera <?= $rider1['id'] ?>?')">
                <?= csrf_field() ?>
                <input type="hidden" name="keep_id" value="<?= $rider2['id'] ?>">
                <input type="hidden" name="remove_id" value="<?= $rider1['id'] ?>">
                <button type="submit" name="merge" class="btn btn-primary w-full">
                    <i data-lucide="arrow-right"></i>
                    Behåll <?= $rider2['id'] ?>, radera <?= $rider1['id'] ?>
                </button>
                <div class="text-center text-sm text-muted mt-sm">
                    <?= $rider2['result_count'] ?> + <?= $rider1['result_count'] ?> = <?= $rider1['result_count'] + $rider2['result_count'] ?> resultat
                </div>
            </form>
        </div>
    </div>
</div>
<?php elseif ($rider1Id || $rider2Id): ?>
<div class="alert alert-error mb-lg">
    <?php if (!$rider1 && $rider1Id): ?>Åkare <?= $rider1Id ?> hittades inte.<br><?php endif; ?>
    <?php if (!$rider2 && $rider2Id): ?>Åkare <?= $rider2Id ?> hittades inte.<?php endif; ?>
</div>
<?php endif; ?>

<!-- Senaste potentiella dubletter -->
<div class="card">
    <div class="card-header">
        <h3><i data-lucide="users"></i> Potentiella dubletter (senaste)</h3>
    </div>
    <div class="card-body gs-padding-0">
        <?php if (empty($recentDuplicates)): ?>
        <div class="alert alert-success m-md">
            <i data-lucide="check-circle"></i> Inga potentiella dubletter hittades!
        </div>
        <?php else: ?>
        <div class="table-responsive">
            <table class="table">
                <thead>
                    <tr>
                        <th>Namn</th>
                        <th>ID 1</th>
                        <th>ID 2</th>
                        <th>Licens 1</th>
                        <th>Licens 2</th>
                        <th>Resultat</th>
                        <th>Åtgärd</th>
                    </tr>
                </thead>
                <tbody>
                    <?php foreach ($recentDuplicates as $dup): ?>
                    <tr>
                        <td><strong><?= h($dup['name1_first'] . ' ' . $dup['name1_last']) ?></strong></td>
                        <td><?= $dup['id1'] ?></td>
                        <td><?= $dup['id2'] ?></td>
                        <td><code><?= h($dup['license1'] ?: '-') ?></code></td>
                        <td><code><?= h($dup['license2'] ?: '-') ?></code></td>
                        <td><?= $dup['results1'] ?> / <?= $dup['results2'] ?></td>
                        <td>
                            <a href="?id1=<?= $dup['id1'] ?>&id2=<?= $dup['id2'] ?>" class="btn btn-sm btn-secondary">
                                <i data-lucide="git-merge"></i> Jämför
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

</div>
<?php include __DIR__ . '/components/unified-layout-footer.php'; ?>
