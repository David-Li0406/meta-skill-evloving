<?php
/**
 * Admin: Smart Duplicate Finder
 *
 * Uses DuplicateService with Jaro-Winkler similarity
 */
require_once __DIR__ . '/../config.php';
require_admin();

require_once __DIR__ . '/../includes/DuplicateService.php';

$db = getDB();
$pdo = $db->getPdo();
$duplicateService = new DuplicateService($pdo);

// Handle actions
$msg = null;
$msgType = 'success';

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    checkCsrf();

    // Merge action
    if (isset($_POST['merge'])) {
        $keepId = (int)$_POST['keep_id'];
        $removeId = (int)$_POST['remove_id'];
        $userId = $_SESSION['admin_id'] ?? null;

        $result = $duplicateService->merge($keepId, $removeId, $userId);

        if ($result['success']) {
            $msg = "Merge klar! {$result['results_moved']} resultat flyttade, {$result['results_deleted']} dubletter borttagna.";
            if (!empty($result['fields_updated'])) {
                $msg .= " Fält uppdaterade: " . implode(', ', $result['fields_updated']);
            }
        } else {
            $msg = "Fel vid merge: " . ($result['error'] ?? 'Okänt fel');
            $msgType = 'danger';
        }
    }

    // Ignore action
    if (isset($_POST['ignore'])) {
        $id1 = (int)$_POST['id1'];
        $id2 = (int)$_POST['id2'];
        $userId = $_SESSION['admin_id'] ?? null;

        if ($duplicateService->ignorePair($id1, $id2, $userId)) {
            $msg = "Par markerat som 'ej dubbletter'";
        } else {
            $msg = "Kunde inte markera par";
            $msgType = 'warning';
        }
    }
}

// Filters
$minScore = isset($_GET['min_score']) ? (float)$_GET['min_score'] : 0.80;
$showIgnored = isset($_GET['show_ignored']);
$limit = isset($_GET['limit']) ? (int)$_GET['limit'] : 100;

// Get duplicate groups
$queryError = null;
try {
    $groups = $duplicateService->findAllDuplicates($limit);
} catch (Exception $e) {
    $groups = [];
    $queryError = $e->getMessage();
}

// Filter out ignored pairs unless requested
if (!$showIgnored) {
    foreach ($groups as &$group) {
        $group['pairs'] = array_filter($group['pairs'], function($pair) use ($duplicateService) {
            return !$duplicateService->isIgnored($pair['rider1']['id'], $pair['rider2']['id']);
        });
        // Recalculate max score
        if (!empty($group['pairs'])) {
            $group['max_score'] = max(array_column($group['pairs'], 'score'));
        }
    }
    // Remove empty groups
    $groups = array_filter($groups, fn($g) => !empty($g['pairs']));
}

// Filter by min score
$groups = array_filter($groups, fn($g) => $g['max_score'] >= $minScore);

// Stats
$totalGroups = count($groups);
$certainGroups = count(array_filter($groups, fn($g) => $g['max_score'] >= 0.92));
$possibleGroups = count(array_filter($groups, fn($g) => $g['max_score'] >= 0.80 && $g['max_score'] < 0.92));

$page_title = 'Smart Dubblettfinnare';
$page_actions = '<a href="/admin/find-duplicates.php" class="btn btn--secondary"><i data-lucide="list"></i> Enkel vy</a>';
include __DIR__ . '/components/unified-layout.php';
?>

<?php if ($msg): ?>
<div class="alert alert-<?= $msgType ?> mb-lg"><?= h($msg) ?></div>
<?php endif; ?>

<?php if ($queryError): ?>
<div class="alert alert-danger mb-lg">
    <strong>SQL-fel:</strong> <?= h($queryError) ?>
</div>
<?php endif; ?>

<div class="card mb-lg">
    <div class="card-header">
        <h2>Filter</h2>
    </div>
    <div class="card-body">
        <form method="GET" class="flex gap-md" style="flex-wrap: wrap; align-items: flex-end;">
            <div class="form-group" style="margin-bottom: 0;">
                <label class="form-label">Min. poäng</label>
                <select name="min_score" class="form-select" style="width: 150px;">
                    <option value="0.92" <?= $minScore >= 0.92 ? 'selected' : '' ?>>0.92+ (Säkra)</option>
                    <option value="0.85" <?= $minScore >= 0.85 && $minScore < 0.92 ? 'selected' : '' ?>>0.85+ (Troliga)</option>
                    <option value="0.80" <?= $minScore >= 0.80 && $minScore < 0.85 ? 'selected' : '' ?>>0.80+ (Möjliga)</option>
                    <option value="0.75" <?= $minScore >= 0.75 && $minScore < 0.80 ? 'selected' : '' ?>>0.75+ (Alla)</option>
                </select>
            </div>
            <div class="form-group" style="margin-bottom: 0;">
                <label class="form-label">Antal grupper</label>
                <select name="limit" class="form-select" style="width: 120px;">
                    <option value="50" <?= $limit == 50 ? 'selected' : '' ?>>50</option>
                    <option value="100" <?= $limit == 100 ? 'selected' : '' ?>>100</option>
                    <option value="200" <?= $limit == 200 ? 'selected' : '' ?>>200</option>
                </select>
            </div>
            <div class="form-group" style="margin-bottom: 0;">
                <label class="form-label" style="display: flex; align-items: center; gap: var(--space-xs);">
                    <input type="checkbox" name="show_ignored" <?= $showIgnored ? 'checked' : '' ?>>
                    Visa ignorerade
                </label>
            </div>
            <button type="submit" class="btn btn-primary">
                <i data-lucide="search"></i> Sök
            </button>
        </form>
    </div>
</div>

<div class="flex gap-lg mb-lg" style="flex-wrap: wrap;">
    <div style="padding: 1rem; background: var(--color-bg-surface); border-radius: var(--radius-md); flex: 1; min-width: 150px;">
        <strong style="color: var(--color-text-muted);">Totalt grupper</strong>
        <div style="font-size: 1.5rem; font-weight: 600;"><?= $totalGroups ?></div>
    </div>
    <div style="padding: 1rem; background: var(--color-bg-surface); border-radius: var(--radius-md); flex: 1; min-width: 150px;">
        <strong style="color: var(--color-text-muted);">Säkra (92%+)</strong>
        <div style="font-size: 1.5rem; font-weight: 600; color: var(--color-error);"><?= $certainGroups ?></div>
        <small class="text-error">Bör slås ihop</small>
    </div>
    <div style="padding: 1rem; background: var(--color-bg-surface); border-radius: var(--radius-md); flex: 1; min-width: 150px;">
        <strong style="color: var(--color-text-muted);">Möjliga (80-92%)</strong>
        <div style="font-size: 1.5rem; font-weight: 600; color: var(--color-warning);"><?= $possibleGroups ?></div>
        <small class="text-warning">Granska manuellt</small>
    </div>
</div>

<?php if (empty($groups)): ?>
<div class="card">
    <div class="card-body text-center" style="padding: var(--space-2xl);">
        <i data-lucide="check-circle" style="width: 48px; height: 48px; color: var(--color-success); margin-bottom: var(--space-md);"></i>
        <h3>Inga dubbletter hittades!</h3>
        <p class="text-secondary">Alla riders med matchande namn har granskats eller är under tröskelvärdet.</p>
    </div>
</div>
<?php else: ?>

<?php foreach ($groups as $group): ?>
<div class="card mb-lg duplicate-group" data-max-score="<?= $group['max_score'] ?>">
    <div class="card-header" style="display: flex; justify-content: space-between; align-items: center;">
        <h3>
            <?= h($group['name']) ?>
            <span class="badge <?= $group['max_score'] >= 0.92 ? 'badge-danger' : 'badge-warning' ?>" style="margin-left: var(--space-sm);">
                <?= number_format($group['max_score'] * 100, 0) ?>%
            </span>
        </h3>
        <span class="text-secondary"><?= $group['count'] ?> riders</span>
    </div>
    <div class="card-body">
        <?php foreach ($group['pairs'] as $pair): ?>
        <?php
            $r1 = $pair['rider1'];
            $r2 = $pair['rider2'];
            $scoreClass = $pair['score'] >= 0.92 ? 'badge-danger' : ($pair['score'] >= 0.80 ? 'badge-warning' : 'badge-secondary');
        ?>
        <div class="duplicate-pair" style="border: 1px solid var(--color-border); border-radius: var(--radius-md); padding: var(--space-md); margin-bottom: var(--space-md); background: var(--color-bg-surface);">
            <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: var(--space-md);">
                <div>
                    <span class="badge <?= $scoreClass ?>" style="font-size: 1rem;">
                        <?= number_format($pair['score'] * 100, 0) ?>% match
                    </span>
                    <?php if ($pair['conflict']): ?>
                    <span class="badge badge-secondary" style="margin-left: var(--space-xs);">
                        Konflikt: <?= $pair['conflict'] ?>
                    </span>
                    <?php endif; ?>
                </div>
                <div style="text-align: right;">
                    <?php foreach ($pair['reasons'] as $reason): ?>
                    <small style="display: block; color: var(--color-text-muted);"><?= h($reason) ?></small>
                    <?php endforeach; ?>
                </div>
            </div>

            <div class="table-responsive">
                <table class="table" style="margin-bottom: var(--space-md);">
                    <thead>
                        <tr>
                            <th style="width: 50px;"></th>
                            <th>Namn</th>
                            <th>Födelseår</th>
                            <th>UCI/Licens</th>
                            <th>Klubb</th>
                            <th>Resultat</th>
                            <th style="width: 80px;"></th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td><input type="radio" name="keep_<?= $r1['id'] ?>_<?= $r2['id'] ?>" value="<?= $r1['id'] ?>" checked class="keep-radio" data-pair="<?= $r1['id'] ?>-<?= $r2['id'] ?>"></td>
                            <td>
                                <strong><?= h($r1['firstname'] . ' ' . $r1['lastname']) ?></strong>
                                <br><small class="text-secondary">ID: <?= $r1['id'] ?></small>
                            </td>
                            <td><?= $r1['birth_year'] ?: '-' ?></td>
                            <td><code style="font-size: 0.85em;"><?= h($r1['license_number'] ?: '-') ?></code></td>
                            <td><?= h($r1['club_name'] ?? '-') ?></td>
                            <td><strong><?= $r1['result_count'] ?></strong></td>
                            <td><a href="/admin/rider-edit.php?id=<?= $r1['id'] ?>" class="btn btn--xs btn--secondary" target="_blank"><i data-lucide="external-link"></i></a></td>
                        </tr>
                        <tr>
                            <td><input type="radio" name="keep_<?= $r1['id'] ?>_<?= $r2['id'] ?>" value="<?= $r2['id'] ?>" class="keep-radio" data-pair="<?= $r1['id'] ?>-<?= $r2['id'] ?>"></td>
                            <td>
                                <strong><?= h($r2['firstname'] . ' ' . $r2['lastname']) ?></strong>
                                <br><small class="text-secondary">ID: <?= $r2['id'] ?></small>
                            </td>
                            <td><?= $r2['birth_year'] ?: '-' ?></td>
                            <td><code style="font-size: 0.85em;"><?= h($r2['license_number'] ?: '-') ?></code></td>
                            <td><?= h($r2['club_name'] ?? '-') ?></td>
                            <td><strong><?= $r2['result_count'] ?></strong></td>
                            <td><a href="/admin/rider-edit.php?id=<?= $r2['id'] ?>" class="btn btn--xs btn--secondary" target="_blank"><i data-lucide="external-link"></i></a></td>
                        </tr>
                    </tbody>
                </table>
            </div>

            <div class="flex gap-sm">
                <form method="POST" style="display: inline;" class="merge-form" data-pair="<?= $r1['id'] ?>-<?= $r2['id'] ?>">
                    <?= csrf_field() ?>
                    <input type="hidden" name="keep_id" class="keep-id" value="<?= $r1['id'] ?>">
                    <input type="hidden" name="remove_id" class="remove-id" value="<?= $r2['id'] ?>">
                    <button type="submit" name="merge" class="btn btn-primary"
                            onclick="return confirm('Slå ihop dessa riders? Den valda behålls, den andra tas bort.')">
                        <i data-lucide="git-merge"></i> Slå ihop
                    </button>
                </form>
                <form method="POST" style="display: inline;">
                    <?= csrf_field() ?>
                    <input type="hidden" name="id1" value="<?= min($r1['id'], $r2['id']) ?>">
                    <input type="hidden" name="id2" value="<?= max($r1['id'], $r2['id']) ?>">
                    <button type="submit" name="ignore" class="btn btn--secondary">
                        <i data-lucide="x"></i> Ej dubbletter
                    </button>
                </form>
            </div>
        </div>
        <?php endforeach; ?>
    </div>
</div>
<?php endforeach; ?>

<?php endif; ?>

<script>
// Handle radio button changes to update merge form
document.querySelectorAll('.keep-radio').forEach(radio => {
    radio.addEventListener('change', function() {
        const pair = this.dataset.pair;
        const [id1, id2] = pair.split('-').map(Number);
        const keepId = parseInt(this.value);
        const removeId = keepId === id1 ? id2 : id1;

        const form = document.querySelector(`.merge-form[data-pair="${pair}"]`);
        if (form) {
            form.querySelector('.keep-id').value = keepId;
            form.querySelector('.remove-id').value = removeId;
        }
    });
});

if (typeof lucide !== 'undefined') lucide.createIcons();
</script>

<?php include __DIR__ . '/components/unified-layout-footer.php'; ?>
