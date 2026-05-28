<?php
/**
 * Cleanup ignored duplicates - Review and selectively remove
 */
require_once __DIR__ . '/../../config.php';
require_admin();

$db = getDB();

$ignoredFile = __DIR__ . '/../../uploads/ignored_rider_duplicates.json';
$ignored = [];
if (file_exists($ignoredFile)) {
    $ignored = json_decode(file_get_contents($ignoredFile), true) ?: [];
}

// Handle actions
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    checkCsrf();

    if (isset($_POST['remove_pair'])) {
        $pairToRemove = $_POST['remove_pair'];
        $ignored = array_filter($ignored, fn($p) => $p !== $pairToRemove);
        file_put_contents($ignoredFile, json_encode(array_values($ignored), JSON_PRETTY_PRINT));
        $_SESSION['msg'] = "Par {$pairToRemove} borttaget från ignorerad-listan";
        header('Location: ' . $_SERVER['REQUEST_URI']);
        exit;
    }

    if (isset($_POST['clear_all'])) {
        file_put_contents($ignoredFile, json_encode([], JSON_PRETTY_PRINT));
        $_SESSION['msg'] = "Alla ignorerade par borttagna!";
        header('Location: /admin/find-duplicates.php');
        exit;
    }

    if (isset($_POST['remove_selected']) && !empty($_POST['pairs'])) {
        $toRemove = $_POST['pairs'];
        $ignored = array_filter($ignored, fn($p) => !in_array($p, $toRemove));
        file_put_contents($ignoredFile, json_encode(array_values($ignored), JSON_PRETTY_PRINT));
        $_SESSION['msg'] = count($toRemove) . " par borttagna från ignorerad-listan";
        header('Location: ' . $_SERVER['REQUEST_URI']);
        exit;
    }
}

$msg = $_SESSION['msg'] ?? null;
unset($_SESSION['msg']);

// Get details for each ignored pair
$pairDetails = [];
foreach ($ignored as $pairKey) {
    $ids = explode('-', $pairKey);
    if (count($ids) !== 2) continue;

    $id1 = (int)$ids[0];
    $id2 = (int)$ids[1];

    $r1 = $db->getRow("
        SELECT r.*, c.name as club_name,
               (SELECT COUNT(*) FROM results WHERE cyclist_id = r.id) as results
        FROM riders r
        LEFT JOIN clubs c ON r.club_id = c.id
        WHERE r.id = ?
    ", [$id1]);

    $r2 = $db->getRow("
        SELECT r.*, c.name as club_name,
               (SELECT COUNT(*) FROM results WHERE cyclist_id = r.id) as results
        FROM riders r
        LEFT JOIN clubs c ON r.club_id = c.id
        WHERE r.id = ?
    ", [$id2]);

    // Check if either rider was deleted (merged already)
    if (!$r1 || !$r2) {
        $pairDetails[] = [
            'key' => $pairKey,
            'deleted' => true,
            'r1' => $r1,
            'r2' => $r2
        ];
        continue;
    }

    // Check if names match (potential real duplicate)
    $sameName = strtolower($r1['firstname'] . ' ' . $r1['lastname']) ===
                strtolower($r2['firstname'] . ' ' . $r2['lastname']);

    // Check for conflicts
    $hasBirthYearConflict = !empty($r1['birth_year']) && !empty($r2['birth_year']) &&
                            $r1['birth_year'] !== $r2['birth_year'];

    $pairDetails[] = [
        'key' => $pairKey,
        'deleted' => false,
        'same_name' => $sameName,
        'birth_conflict' => $hasBirthYearConflict,
        'r1' => $r1,
        'r2' => $r2
    ];
}

// Sort: deleted first, then same_name (likely real dups), then others
usort($pairDetails, function($a, $b) {
    if ($a['deleted'] !== $b['deleted']) return $a['deleted'] ? -1 : 1;
    if (($a['same_name'] ?? false) !== ($b['same_name'] ?? false)) {
        return ($a['same_name'] ?? false) ? -1 : 1;
    }
    return 0;
});

// Stats
$deletedCount = count(array_filter($pairDetails, fn($p) => $p['deleted']));
$sameNameCount = count(array_filter($pairDetails, fn($p) => !$p['deleted'] && ($p['same_name'] ?? false)));
$conflictCount = count(array_filter($pairDetails, fn($p) => !$p['deleted'] && ($p['birth_conflict'] ?? false)));

$page_title = 'Granska Ignorerade Dubbletter';
include __DIR__ . '/../components/unified-layout.php';
?>

<?php if ($msg): ?>
<div class="alert alert-success mb-lg"><?= h($msg) ?></div>
<?php endif; ?>

<div class="card mb-lg">
    <div class="card-header">
        <h2>Ignorerade par (<?= count($ignored) ?>)</h2>
    </div>
    <div class="card-body">
        <div class="flex gap-lg mb-lg" style="flex-wrap: wrap;">
            <div style="padding: 1rem; background: var(--color-bg-surface); border-radius: var(--radius-md);">
                <strong style="color: var(--color-text-muted);">Borttagna riders</strong>
                <div style="font-size: 1.5rem; font-weight: 600;"><?= $deletedCount ?></div>
                <small class="text-success">Kan tas bort säkert</small>
            </div>
            <div style="padding: 1rem; background: var(--color-bg-surface); border-radius: var(--radius-md);">
                <strong style="color: var(--color-text-muted);">Samma namn</strong>
                <div style="font-size: 1.5rem; font-weight: 600; color: var(--color-warning);"><?= $sameNameCount ?></div>
                <small class="text-warning">Troligen riktiga dubbletter!</small>
            </div>
            <div style="padding: 1rem; background: var(--color-bg-surface); border-radius: var(--radius-md);">
                <strong style="color: var(--color-text-muted);">Olika födelseår</strong>
                <div style="font-size: 1.5rem; font-weight: 600;"><?= $conflictCount ?></div>
                <small>Troligen olika personer</small>
            </div>
        </div>

        <form method="POST" id="cleanupForm">
            <?= csrf_field() ?>

            <div class="flex gap-md mb-lg">
                <button type="submit" name="remove_selected" class="btn btn-primary">
                    <i data-lucide="trash-2"></i> Ta bort valda från ignorerad-listan
                </button>
                <button type="button" onclick="selectDeleted()" class="btn btn--secondary">
                    Välj alla borttagna
                </button>
                <button type="button" onclick="selectSameName()" class="btn btn--secondary">
                    Välj alla med samma namn
                </button>
                <button type="submit" name="clear_all" class="btn btn-danger"
                        onclick="return confirm('Rensa ALLA ignorerade par? Detta visar alla potentiella dubbletter igen.')">
                    <i data-lucide="trash"></i> Rensa ALLA
                </button>
            </div>

            <div class="table-responsive">
                <table class="table">
                    <thead>
                        <tr>
                            <th style="width: 40px;"><input type="checkbox" id="selectAll" onchange="toggleAll()"></th>
                            <th>Par</th>
                            <th>Rider 1</th>
                            <th>Rider 2</th>
                            <th>Status</th>
                            <th></th>
                        </tr>
                    </thead>
                    <tbody>
                        <?php foreach ($pairDetails as $pair): ?>
                        <tr data-deleted="<?= $pair['deleted'] ? '1' : '0' ?>"
                            data-same-name="<?= ($pair['same_name'] ?? false) ? '1' : '0' ?>">
                            <td>
                                <input type="checkbox" name="pairs[]" value="<?= h($pair['key']) ?>" class="pair-checkbox">
                            </td>
                            <td><code><?= h($pair['key']) ?></code></td>
                            <td>
                                <?php if ($pair['r1']): ?>
                                    <strong><?= h($pair['r1']['firstname'] . ' ' . $pair['r1']['lastname']) ?></strong>
                                    <br><small class="text-secondary">
                                        ID: <?= $pair['r1']['id'] ?> |
                                        <?= $pair['r1']['birth_year'] ?: '-' ?> |
                                        <?= $pair['r1']['results'] ?> resultat
                                    </small>
                                <?php else: ?>
                                    <span class="text-error">BORTTAGEN</span>
                                <?php endif; ?>
                            </td>
                            <td>
                                <?php if ($pair['r2']): ?>
                                    <strong><?= h($pair['r2']['firstname'] . ' ' . $pair['r2']['lastname']) ?></strong>
                                    <br><small class="text-secondary">
                                        ID: <?= $pair['r2']['id'] ?> |
                                        <?= $pair['r2']['birth_year'] ?: '-' ?> |
                                        <?= $pair['r2']['results'] ?> resultat
                                    </small>
                                <?php else: ?>
                                    <span class="text-error">BORTTAGEN</span>
                                <?php endif; ?>
                            </td>
                            <td>
                                <?php if ($pair['deleted']): ?>
                                    <span class="badge badge-secondary">Rider borttagen</span>
                                <?php elseif ($pair['same_name'] ?? false): ?>
                                    <span class="badge badge-warning">Samma namn!</span>
                                    <?php if ($pair['birth_conflict'] ?? false): ?>
                                        <span class="badge badge-danger">Olika födelseår</span>
                                    <?php endif; ?>
                                <?php else: ?>
                                    <span class="badge badge-secondary">Olika namn</span>
                                <?php endif; ?>
                            </td>
                            <td>
                                <button type="submit" name="remove_pair" value="<?= h($pair['key']) ?>"
                                        class="btn btn--sm btn--secondary">
                                    <i data-lucide="x"></i>
                                </button>
                            </td>
                        </tr>
                        <?php endforeach; ?>
                    </tbody>
                </table>
            </div>
        </form>
    </div>
</div>

<script>
function toggleAll() {
    const checked = document.getElementById('selectAll').checked;
    document.querySelectorAll('.pair-checkbox').forEach(cb => cb.checked = checked);
}

function selectDeleted() {
    document.querySelectorAll('tr[data-deleted="1"] .pair-checkbox').forEach(cb => cb.checked = true);
}

function selectSameName() {
    document.querySelectorAll('tr[data-same-name="1"] .pair-checkbox').forEach(cb => cb.checked = true);
}

if (typeof lucide !== 'undefined') lucide.createIcons();
</script>

<?php include __DIR__ . '/../components/unified-layout-footer.php'; ?>
