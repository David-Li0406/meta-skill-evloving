<?php
/**
 * Find and Fix UCI ID Conflicts
 * Identifies riders where UCI ID might be assigned to wrong person
 */
require_once __DIR__ . '/../../config.php';
require_admin();

$db = getDB();
$message = '';
$messageType = '';

// Handle fix action
if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['action'])) {
    checkCsrf();

    if ($_POST['action'] === 'clear_uci') {
        $riderId = (int)$_POST['rider_id'];
        if ($riderId > 0) {
            $db->update('riders', ['license_number' => null], 'id = ?', [$riderId]);
            $message = "UCI-ID rensat för åkare #$riderId";
            $messageType = 'success';
        }
    } elseif ($_POST['action'] === 'set_uci') {
        $riderId = (int)$_POST['rider_id'];
        $uciId = trim($_POST['uci_id']);
        if ($riderId > 0 && !empty($uciId)) {
            $db->update('riders', ['license_number' => $uciId], 'id = ?', [$riderId]);
            $message = "UCI-ID uppdaterat för åkare #$riderId";
            $messageType = 'success';
        }
    }
}

$pageTitle = 'Fix UCI-ID Konflikter';
include __DIR__ . '/../components/unified-layout.php';
?>

<?php if ($message): ?>
<div class="alert alert-<?= $messageType ?> mb-md"><?= h($message) ?></div>
<?php endif; ?>

<div class="card mb-lg">
    <div class="card-header">
        <h3><i data-lucide="search"></i> Söker efter potentiella UCI-ID konflikter...</h3>
    </div>
    <div class="card-body">

<?php
// Find riders with same last name where one might have the other's UCI ID
// Look for cases where import data times don't match rider's typical times

// First, find all riders with UCI IDs and same last name as another rider
$query = "
    SELECT
        r1.id as rider1_id,
        r1.firstname as rider1_first,
        r1.lastname as rider1_last,
        r1.license_number as rider1_uci,
        r2.id as rider2_id,
        r2.firstname as rider2_first,
        r2.lastname as rider2_last,
        r2.license_number as rider2_uci
    FROM riders r1
    INNER JOIN riders r2 ON r1.lastname = r2.lastname
        AND r1.id < r2.id
        AND r1.firstname != r2.firstname
    WHERE (r1.license_number IS NOT NULL AND r1.license_number != '')
       OR (r2.license_number IS NOT NULL AND r2.license_number != '')
    ORDER BY r1.lastname, r1.firstname
";

$conflicts = $db->getAll($query);

if (empty($conflicts)) {
    echo '<div class="alert alert-success"><i data-lucide="check-circle"></i> Inga potentiella konflikter hittades.</div>';
} else {
    echo '<div class="alert alert-warning mb-md">';
    echo '<strong>' . count($conflicts) . ' åkarpar</strong> med samma efternamn och UCI-ID hittades. Kontrollera om rätt person har rätt UCI-ID.';
    echo '</div>';

    echo '<table class="table table-sm">';
    echo '<thead><tr>';
    echo '<th>Åkare 1</th><th>UCI-ID 1</th>';
    echo '<th>Åkare 2</th><th>UCI-ID 2</th>';
    echo '<th>Åtgärd</th>';
    echo '</tr></thead>';
    echo '<tbody>';

    foreach ($conflicts as $c) {
        echo '<tr>';
        echo '<td>';
        echo '<a href="/rider/' . $c['rider1_id'] . '">' . h($c['rider1_first'] . ' ' . $c['rider1_last']) . '</a>';
        echo ' <span class="text-secondary">(#' . $c['rider1_id'] . ')</span>';
        echo '</td>';
        echo '<td>';
        if ($c['rider1_uci']) {
            echo '<code>' . h($c['rider1_uci']) . '</code>';
            echo '<form method="POST" style="display:inline; margin-left: 8px;">';
            echo csrf_field();
            echo '<input type="hidden" name="action" value="clear_uci">';
            echo '<input type="hidden" name="rider_id" value="' . $c['rider1_id'] . '">';
            echo '<button type="submit" class="btn btn-danger btn--xs" onclick="return confirm(\'Rensa UCI-ID för ' . h($c['rider1_first']) . '?\')">Rensa</button>';
            echo '</form>';
        } else {
            echo '<span class="text-secondary">-</span>';
        }
        echo '</td>';

        echo '<td>';
        echo '<a href="/rider/' . $c['rider2_id'] . '">' . h($c['rider2_first'] . ' ' . $c['rider2_last']) . '</a>';
        echo ' <span class="text-secondary">(#' . $c['rider2_id'] . ')</span>';
        echo '</td>';
        echo '<td>';
        if ($c['rider2_uci']) {
            echo '<code>' . h($c['rider2_uci']) . '</code>';
            echo '<form method="POST" style="display:inline; margin-left: 8px;">';
            echo csrf_field();
            echo '<input type="hidden" name="action" value="clear_uci">';
            echo '<input type="hidden" name="rider_id" value="' . $c['rider2_id'] . '">';
            echo '<button type="submit" class="btn btn-danger btn--xs" onclick="return confirm(\'Rensa UCI-ID för ' . h($c['rider2_first']) . '?\')">Rensa</button>';
            echo '</form>';
        } else {
            echo '<span class="text-secondary">-</span>';
        }
        echo '</td>';

        echo '<td>';
        echo '<a href="/admin/riders.php?search=' . urlencode($c['rider1_last']) . '" class="btn btn--secondary btn--xs">Sök</a>';
        echo '</td>';

        echo '</tr>';
    }

    echo '</tbody></table>';
}
?>

    </div>
</div>

<div class="card mb-lg">
    <div class="card-header">
        <h3><i data-lucide="users"></i> Sök specifik åkare</h3>
    </div>
    <div class="card-body">
        <form method="GET" class="flex gap-md items-end">
            <div class="form-group mb-0">
                <label class="form-label">Efternamn</label>
                <input type="text" name="search" class="input" value="<?= h($_GET['search'] ?? '') ?>" placeholder="T.ex. Månsson">
            </div>
            <button type="submit" class="btn btn--primary">Sök</button>
        </form>

        <?php if (!empty($_GET['search'])): ?>
        <?php
        $searchName = trim($_GET['search']);
        $riders = $db->getAll("
            SELECT id, firstname, lastname, license_number, birth_year, club_id,
                   (SELECT name FROM clubs WHERE id = riders.club_id) as club_name
            FROM riders
            WHERE lastname LIKE ? OR firstname LIKE ?
            ORDER BY lastname, firstname
        ", ["%$searchName%", "%$searchName%"]);
        ?>

        <?php if (!empty($riders)): ?>
        <table class="table table-sm mt-md">
            <thead><tr><th>ID</th><th>Namn</th><th>Födelseår</th><th>Klubb</th><th>UCI-ID</th><th>Åtgärd</th></tr></thead>
            <tbody>
            <?php foreach ($riders as $r): ?>
            <tr>
                <td><?= $r['id'] ?></td>
                <td><a href="/rider/<?= $r['id'] ?>"><?= h($r['firstname'] . ' ' . $r['lastname']) ?></a></td>
                <td><?= $r['birth_year'] ?: '-' ?></td>
                <td><?= h($r['club_name'] ?: '-') ?></td>
                <td>
                    <form method="POST" class="flex gap-xs">
                        <?= csrf_field() ?>
                        <input type="hidden" name="action" value="set_uci">
                        <input type="hidden" name="rider_id" value="<?= $r['id'] ?>">
                        <input type="text" name="uci_id" class="input input-w150" value="<?= h($r['license_number'] ?? '') ?>" placeholder="UCI-ID">
                        <button type="submit" class="btn btn--primary btn--sm">Spara</button>
                        <?php if ($r['license_number']): ?>
                        <button type="submit" name="action" value="clear_uci" class="btn btn-danger btn--sm" onclick="return confirm('Rensa?')">Rensa</button>
                        <?php endif; ?>
                    </form>
                </td>
                <td>
                    <a href="/admin/edit-rider.php?id=<?= $r['id'] ?>" class="btn btn--secondary btn--sm">Editera</a>
                </td>
            </tr>
            <?php endforeach; ?>
            </tbody>
        </table>
        <?php else: ?>
        <p class="text-secondary mt-md">Inga åkare hittades.</p>
        <?php endif; ?>
        <?php endif; ?>
    </div>
</div>

<script src="https://unpkg.com/lucide@latest"></script>
<script>lucide.createIcons();</script>

<?php include __DIR__ . '/../components/unified-layout-footer.php'; ?>
