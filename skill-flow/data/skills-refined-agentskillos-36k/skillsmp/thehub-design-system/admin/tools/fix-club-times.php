<?php
/**
 * Fix Club Times Issue
 * Fixes riders whose club names look like stage times (column offset problem)
 */
require_once __DIR__ . '/../../config.php';
require_admin();

$db = getDB();
$message = '';
$messageType = 'info';

// Handle fix action
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    checkCsrf();

    $action = $_POST['action'] ?? '';

    if ($action === 'clear_rider_club') {
        // Clear club from specific rider
        $riderId = (int)$_POST['rider_id'];
        $db->update('riders', ['club_id' => null], 'id = ?', [$riderId]);
        $message = "Klubb borttagen från åkare #$riderId";
        $messageType = 'success';
    }

    if ($action === 'clear_all_from_club') {
        // Clear all riders from a specific club
        $clubId = (int)$_POST['club_id'];
        $club = $db->getRow("SELECT name FROM clubs WHERE id = ?", [$clubId]);
        $affected = $db->execute("UPDATE riders SET club_id = NULL WHERE club_id = ?", [$clubId]);
        $message = "Klubb '" . h($club['name']) . "' borttagen från alla åkare";
        $messageType = 'success';
    }

    if ($action === 'delete_club') {
        // Delete a club (must have no riders)
        $clubId = (int)$_POST['club_id'];
        $club = $db->getRow("SELECT name FROM clubs WHERE id = ?", [$clubId]);
        $riderCount = $db->getRow("SELECT COUNT(*) as cnt FROM riders WHERE club_id = ?", [$clubId]);

        if ($riderCount['cnt'] > 0) {
            $message = "Kan inte ta bort klubb - har fortfarande {$riderCount['cnt']} åkare";
            $messageType = 'error';
        } else {
            $db->delete('clubs', 'id = ?', [$clubId]);
            $message = "Klubb '" . h($club['name']) . "' borttagen";
            $messageType = 'success';
        }
    }

    if ($action === 'delete_all_time_clubs') {
        // Delete all clubs with time-like names (that have no riders)
        $timePattern = "^[0-9]{1,2}:[0-9]{2}";
        $deleted = $db->execute("
            DELETE FROM clubs
            WHERE name REGEXP ?
            AND id NOT IN (SELECT DISTINCT club_id FROM riders WHERE club_id IS NOT NULL)
        ", [$timePattern]);
        $message = "Alla oanvända tidsklubbnamn borttagna";
        $messageType = 'success';
    }

    if ($action === 'reassign_rider') {
        // Reassign rider to correct club
        $riderId = (int)$_POST['rider_id'];
        $newClubId = (int)$_POST['new_club_id'];

        if ($newClubId > 0) {
            $db->update('riders', ['club_id' => $newClubId], 'id = ?', [$riderId]);
            $message = "Åkare #$riderId flyttad till rätt klubb";
            $messageType = 'success';
        } else {
            $db->update('riders', ['club_id' => null], 'id = ?', [$riderId]);
            $message = "Klubbtillhörighet borttagen från åkare #$riderId";
            $messageType = 'success';
        }
    }
}

$pageTitle = 'Fixa klubbar som ser ut som tider';
include __DIR__ . '/../components/unified-layout.php';

// Find clubs with time-like names
$timePattern = "^[0-9]{1,2}:[0-9]{2}";
$timeClubs = $db->getAll("
    SELECT
        c.id,
        c.name,
        COUNT(DISTINCT rd.id) as rider_count
    FROM clubs c
    LEFT JOIN riders rd ON rd.club_id = c.id
    WHERE c.name REGEXP ?
    GROUP BY c.id
    ORDER BY rider_count DESC
", [$timePattern]);

// Get all valid clubs for reassignment dropdown
$validClubs = $db->getAll("
    SELECT id, name
    FROM clubs
    WHERE name NOT REGEXP ?
    AND active = 1
    ORDER BY name
", [$timePattern]);
?>

<?php if ($message): ?>
<div class="alert alert-<?= $messageType ?> mb-lg">
    <i data-lucide="<?= $messageType === 'success' ? 'check-circle' : 'alert-circle' ?>"></i>
    <?= $message ?>
</div>
<?php endif; ?>

<div class="card mb-lg">
    <div class="card-header">
        <h2 class="text-primary">
            <i data-lucide="wrench"></i>
            Fixa klubbar med tidsliknande namn
        </h2>
    </div>
    <div class="card-body">
        <?php if (empty($timeClubs)): ?>
        <div class="alert alert-success">
            <i data-lucide="check-circle"></i>
            Inga klubbar med tidsliknande namn hittades!
        </div>
        <?php else: ?>
        <div class="alert alert-warning mb-lg">
            <i data-lucide="alert-triangle"></i>
            <strong><?= count($timeClubs) ?> klubbar</strong> med tidsliknande namn hittades.
        </div>

        <!-- Bulk action: Delete unused time clubs -->
        <form method="POST" class="mb-lg">
            <?= csrf_field() ?>
            <input type="hidden" name="action" value="delete_all_time_clubs">
            <button type="submit" class="btn btn--danger"
                    onclick="return confirm('Är du säker? Detta tar bort alla tidsklubbnamn som inte har några åkare.')">
                <i data-lucide="trash-2"></i>
                Ta bort alla oanvända tidsklubbnamn
            </button>
        </form>

        <div class="table-responsive">
            <table class="table">
                <thead>
                    <tr>
                        <th>Klubb-ID</th>
                        <th>Namn (tid)</th>
                        <th>Antal åkare</th>
                        <th>Åtgärder</th>
                    </tr>
                </thead>
                <tbody>
                    <?php foreach ($timeClubs as $club): ?>
                    <tr>
                        <td><?= $club['id'] ?></td>
                        <td><code class="text-warning" style="font-size: 1.1em;"><?= h($club['name']) ?></code></td>
                        <td>
                            <?php if ($club['rider_count'] > 0): ?>
                            <span class="badge badge-warning"><?= $club['rider_count'] ?></span>
                            <?php else: ?>
                            <span class="badge badge-secondary">0</span>
                            <?php endif; ?>
                        </td>
                        <td>
                            <?php if ($club['rider_count'] > 0): ?>
                            <form method="POST" style="display: inline;">
                                <?= csrf_field() ?>
                                <input type="hidden" name="action" value="clear_all_from_club">
                                <input type="hidden" name="club_id" value="<?= $club['id'] ?>">
                                <button type="submit" class="btn btn--sm btn--warning"
                                        onclick="return confirm('Ta bort klubbtillhörighet från <?= $club['rider_count'] ?> åkare?')">
                                    <i data-lucide="user-minus"></i>
                                    Ta bort från alla åkare
                                </button>
                            </form>
                            <?php else: ?>
                            <form method="POST" style="display: inline;">
                                <?= csrf_field() ?>
                                <input type="hidden" name="action" value="delete_club">
                                <input type="hidden" name="club_id" value="<?= $club['id'] ?>">
                                <button type="submit" class="btn btn--sm btn--danger">
                                    <i data-lucide="trash-2"></i>
                                    Ta bort
                                </button>
                            </form>
                            <?php endif; ?>
                        </td>
                    </tr>
                    <?php endforeach; ?>
                </tbody>
            </table>
        </div>
        <?php endif; ?>
    </div>
</div>

<?php
// Show affected riders for each time-club
foreach ($timeClubs as $club):
    if ($club['rider_count'] == 0) continue;

    $riders = $db->getAll("
        SELECT
            r.id,
            r.firstname,
            r.lastname,
            r.license_number
        FROM riders r
        WHERE r.club_id = ?
        ORDER BY r.lastname, r.firstname
        LIMIT 50
    ", [$club['id']]);
?>
<div class="card mb-lg">
    <div class="card-header">
        <h3 class="text-warning">
            <i data-lucide="users"></i>
            Åkare med klubb "<?= h($club['name']) ?>" (<?= $club['rider_count'] ?>)
        </h3>
    </div>
    <div class="card-body">
        <div class="table-responsive">
            <table class="table table-sm">
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Namn</th>
                        <th>UCI-ID</th>
                        <th>Byt klubb till</th>
                    </tr>
                </thead>
                <tbody>
                    <?php foreach ($riders as $rider): ?>
                    <tr>
                        <td><?= $rider['id'] ?></td>
                        <td>
                            <a href="/rider/<?= $rider['id'] ?>" target="_blank">
                                <?= h($rider['firstname'] . ' ' . $rider['lastname']) ?>
                            </a>
                        </td>
                        <td><code><?= h($rider['license_number'] ?? '-') ?></code></td>
                        <td>
                            <form method="POST" class="flex gap-sm">
                                <?= csrf_field() ?>
                                <input type="hidden" name="action" value="reassign_rider">
                                <input type="hidden" name="rider_id" value="<?= $rider['id'] ?>">
                                <select name="new_club_id" class="input input-sm" style="max-width: 200px;">
                                    <option value="0">-- Ingen klubb --</option>
                                    <?php foreach ($validClubs as $vc): ?>
                                    <option value="<?= $vc['id'] ?>"><?= h($vc['name']) ?></option>
                                    <?php endforeach; ?>
                                </select>
                                <button type="submit" class="btn btn--sm btn--primary">
                                    <i data-lucide="save"></i>
                                </button>
                            </form>
                        </td>
                    </tr>
                    <?php endforeach; ?>
                </tbody>
            </table>
        </div>
        <?php if ($club['rider_count'] > 50): ?>
        <p class="text-secondary mt-md">Visar 50 av <?= $club['rider_count'] ?> åkare</p>
        <?php endif; ?>
    </div>
</div>
<?php endforeach; ?>

<div class="card mt-lg">
    <div class="card-header">
        <h3 class="text-primary">
            <i data-lucide="info"></i>
            Förebyggande åtgärder
        </h3>
    </div>
    <div class="card-body">
        <p class="mb-md">Detta problem uppstår när importfilen har fel kolumnordning eller tomma kolumner.</p>

        <h4 class="mb-sm">Korrekt kolumnordning för Enduro:</h4>
        <code class="gs-code-block mb-md">
Category, PlaceByCategory, Bib, FirstName, LastName, Club, UCI-ID, NetTime, Status, SS1, SS2...
        </code>

        <h4 class="mb-sm">Vanliga fel:</h4>
        <ul style="margin-left: 20px;">
            <li>Tom kolumn mellan Club och UCI-ID</li>
            <li>Sträcktider före NetTime istället för efter</li>
            <li>Kolumner i fel ordning</li>
        </ul>

        <div class="mt-lg">
            <a href="/admin/tools/diagnose-club-times.php" class="btn btn--secondary">
                <i data-lucide="search"></i>
                Tillbaka till diagnostik
            </a>
        </div>
    </div>
</div>

<?php include __DIR__ . '/../components/unified-layout-footer.php'; ?>
