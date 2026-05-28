<?php
/**
 * Smart Duplicate Finder v2
 *
 * Enkel och pålitlig:
 * 1. Hittar riders med exakt samma namn
 * 2. Grupperar efter namn
 * 3. Visar ALLA - inget "ignore"-system
 * 4. Merga direkt, data sparas i rider_merge_map
 */
require_once __DIR__ . '/../config.php';
require_admin();

$db = getDB();
$pdo = $db->getPdo();
$message = null;
$messageType = 'info';

// Handle merge action
if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['merge'])) {
    checkCsrf();

    $keepId = (int)$_POST['keep_id'];
    $removeId = (int)$_POST['remove_id'];

    if ($keepId && $removeId && $keepId !== $removeId) {
        try {
            $pdo->beginTransaction();

            // Get rider info
            $keepRider = $db->getRow("SELECT * FROM riders WHERE id = ?", [$keepId]);
            $removeRider = $db->getRow("SELECT * FROM riders WHERE id = ?", [$removeId]);

            if (!$keepRider || !$removeRider) {
                throw new Exception("Rider hittades inte");
            }

            // Move results
            $moved = 0;
            $deleted = 0;
            $resultsToMove = $db->getAll("SELECT id, event_id, class_id FROM results WHERE cyclist_id = ?", [$removeId]);

            foreach ($resultsToMove as $result) {
                $existing = $db->getRow(
                    "SELECT id FROM results WHERE cyclist_id = ? AND event_id = ? AND class_id <=> ?",
                    [$keepId, $result['event_id'], $result['class_id']]
                );

                if ($existing) {
                    $pdo->prepare("DELETE FROM results WHERE id = ?")->execute([$result['id']]);
                    $deleted++;
                } else {
                    $pdo->prepare("UPDATE results SET cyclist_id = ? WHERE id = ?")->execute([$keepId, $result['id']]);
                    $moved++;
                }
            }

            // Move series_results
            $pdo->prepare("UPDATE series_results SET cyclist_id = ? WHERE cyclist_id = ?")->execute([$keepId, $removeId]);

            // Update keep rider with missing data
            $updates = [];
            if (empty($keepRider['birth_year']) && !empty($removeRider['birth_year'])) {
                $updates['birth_year'] = $removeRider['birth_year'];
            }
            if (empty($keepRider['email']) && !empty($removeRider['email'])) {
                $updates['email'] = $removeRider['email'];
            }
            if (empty($keepRider['club_id']) && !empty($removeRider['club_id'])) {
                $updates['club_id'] = $removeRider['club_id'];
            }
            if (empty($keepRider['gender']) && !empty($removeRider['gender'])) {
                $updates['gender'] = $removeRider['gender'];
            }
            // Prefer real UCI ID over SWE-ID
            if (!empty($removeRider['license_number'])) {
                $keepIsSwe = empty($keepRider['license_number']) || strpos($keepRider['license_number'], 'SWE') === 0;
                $removeIsUci = strpos($removeRider['license_number'], 'SWE') !== 0;
                if ($keepIsSwe && $removeIsUci) {
                    $updates['license_number'] = $removeRider['license_number'];
                } elseif (empty($keepRider['license_number'])) {
                    $updates['license_number'] = $removeRider['license_number'];
                }
            }

            if (!empty($updates)) {
                $setClauses = [];
                $params = [];
                foreach ($updates as $col => $val) {
                    $setClauses[] = "$col = ?";
                    $params[] = $val;
                }
                $params[] = $keepId;
                $pdo->prepare("UPDATE riders SET " . implode(', ', $setClauses) . " WHERE id = ?")->execute($params);
            }

            // Record merge in rider_merge_map (if table exists)
            try {
                $pdo->prepare("
                    INSERT INTO rider_merge_map (canonical_rider_id, merged_rider_id, reason, confidence, status)
                    VALUES (?, ?, 'manual_merge', 100, 'approved')
                    ON DUPLICATE KEY UPDATE canonical_rider_id = VALUES(canonical_rider_id)
                ")->execute([$keepId, $removeId]);
            } catch (Exception $e) {
                // Table might not exist, ignore
            }

            // Delete the duplicate rider
            $pdo->prepare("DELETE FROM riders WHERE id = ?")->execute([$removeId]);

            $pdo->commit();

            $message = "Sammanslagen! {$removeRider['firstname']} {$removeRider['lastname']} → {$keepRider['firstname']} {$keepRider['lastname']} ({$moved} resultat flyttade)";
            $messageType = 'success';

        } catch (Exception $e) {
            $pdo->rollBack();
            $message = "Fel: " . $e->getMessage();
            $messageType = 'error';
        }
    }
}

// Find all duplicate name groups
$duplicateGroups = $db->getAll("
    SELECT
        LOWER(CONCAT(firstname, ' ', lastname)) as name_key,
        firstname,
        lastname,
        COUNT(*) as cnt
    FROM riders
    WHERE firstname IS NOT NULL
      AND lastname IS NOT NULL
      AND firstname != ''
      AND lastname != ''
    GROUP BY name_key
    HAVING cnt > 1
    ORDER BY cnt DESC, lastname, firstname
    LIMIT 200
");

$page_title = 'Hitta Dubbletter v2';
include __DIR__ . '/components/unified-layout.php';
?>

<style>
.dup-group {
    background: var(--color-bg-card);
    border: 1px solid var(--color-border);
    border-radius: var(--radius-md);
    margin-bottom: var(--space-md);
    overflow: hidden;
}
.dup-group-header {
    background: var(--color-bg-surface);
    padding: var(--space-sm) var(--space-md);
    border-bottom: 1px solid var(--color-border);
    display: flex;
    justify-content: space-between;
    align-items: center;
}
.dup-group-header h3 {
    margin: 0;
    font-size: var(--text-md);
}
.dup-riders {
    display: flex;
    flex-wrap: wrap;
    gap: var(--space-sm);
    padding: var(--space-md);
}
.rider-card {
    flex: 1;
    min-width: 250px;
    max-width: 350px;
    padding: var(--space-md);
    background: var(--color-bg-surface);
    border-radius: var(--radius-sm);
    border: 2px solid transparent;
}
.rider-card.best {
    border-color: var(--color-success);
}
.rider-card .name {
    font-weight: 600;
    margin-bottom: var(--space-xs);
}
.rider-card .meta {
    font-size: var(--text-sm);
    color: var(--color-text-secondary);
}
.rider-card .meta span {
    display: inline-block;
    margin-right: var(--space-sm);
}
.rider-card .actions {
    margin-top: var(--space-sm);
    display: flex;
    gap: var(--space-xs);
}
.badge-results {
    background: var(--color-accent-light);
    color: var(--color-accent);
    padding: 2px 8px;
    border-radius: var(--radius-full);
    font-size: var(--text-xs);
    font-weight: 600;
}
.conflict-warning {
    background: rgba(220,53,69,0.1);
    border: 1px solid var(--color-error);
    color: var(--color-error);
    padding: var(--space-xs) var(--space-sm);
    border-radius: var(--radius-sm);
    font-size: var(--text-sm);
    margin-top: var(--space-sm);
}
</style>

<?php if ($message): ?>
<div class="alert alert-<?= $messageType ?> mb-lg">
    <i data-lucide="<?= $messageType === 'success' ? 'check-circle' : 'alert-circle' ?>"></i>
    <?= h($message) ?>
</div>
<?php endif; ?>

<div class="card mb-lg">
    <div class="card-header">
        <h2><i data-lucide="users"></i> Dubbletter (<?= count($duplicateGroups) ?> grupper)</h2>
    </div>
    <div class="card-body">
        <p class="text-secondary mb-lg">
            Visar riders med exakt samma namn. Klicka "Behåll" på den profil du vill behålla -
            den andra raderas och alla resultat flyttas.
        </p>

        <?php if (empty($duplicateGroups)): ?>
        <div class="text-center py-xl">
            <i data-lucide="check-circle" class="text-success" style="width: 48px; height: 48px;"></i>
            <p class="text-success mt-md">Inga dubbletter hittades!</p>
        </div>
        <?php else: ?>

        <?php foreach ($duplicateGroups as $group):
            // Get all riders in this group
            $riders = $db->getAll("
                SELECT r.*,
                       c.name as club_name,
                       (SELECT COUNT(*) FROM results WHERE cyclist_id = r.id) as result_count
                FROM riders r
                LEFT JOIN clubs c ON r.club_id = c.id
                WHERE LOWER(CONCAT(r.firstname, ' ', r.lastname)) = ?
                ORDER BY r.id
            ", [$group['name_key']]);

            // Score each rider
            foreach ($riders as &$r) {
                $score = $r['result_count'] * 10;
                if (!empty($r['license_number']) && strpos($r['license_number'], 'SWE') !== 0) $score += 100;
                if (!empty($r['license_number'])) $score += 10;
                if (!empty($r['birth_year'])) $score += 5;
                if (!empty($r['email'])) $score += 5;
                if (!empty($r['club_id'])) $score += 5;
                $r['score'] = $score;
            }
            unset($r);

            // Sort by score
            usort($riders, fn($a, $b) => $b['score'] - $a['score']);
            $bestId = $riders[0]['id'];

            // Check for conflicts
            $birthYears = array_filter(array_unique(array_column($riders, 'birth_year')));
            $hasBirthConflict = count($birthYears) > 1;

            $uciIds = array_filter(array_map(function($r) {
                return (!empty($r['license_number']) && strpos($r['license_number'], 'SWE') !== 0)
                    ? $r['license_number'] : null;
            }, $riders));
            $hasUciConflict = count(array_unique($uciIds)) > 1;
        ?>
        <div class="dup-group">
            <div class="dup-group-header">
                <h3><?= h($group['firstname'] . ' ' . $group['lastname']) ?></h3>
                <span class="badge badge-warning"><?= $group['cnt'] ?> profiler</span>
            </div>

            <?php if ($hasBirthConflict || $hasUciConflict): ?>
            <div class="conflict-warning" style="margin: var(--space-sm) var(--space-md) 0;">
                <i data-lucide="alert-triangle" style="width:14px;height:14px;vertical-align:middle;"></i>
                <?php if ($hasBirthConflict): ?>
                    <strong>Olika födelseår:</strong> <?= implode(', ', $birthYears) ?>
                <?php endif; ?>
                <?php if ($hasUciConflict): ?>
                    <strong>Olika UCI-ID</strong>
                <?php endif; ?>
                - Kan vara olika personer!
            </div>
            <?php endif; ?>

            <div class="dup-riders">
                <?php foreach ($riders as $rider): ?>
                <div class="rider-card <?= $rider['id'] === $bestId ? 'best' : '' ?>">
                    <div class="name">
                        <?= h($rider['firstname'] . ' ' . $rider['lastname']) ?>
                        <span class="badge-results"><?= $rider['result_count'] ?> resultat</span>
                    </div>
                    <div class="meta">
                        <span>ID: <?= $rider['id'] ?></span>
                        <span>Född: <?= $rider['birth_year'] ?: '-' ?></span>
                        <br>
                        <span>Licens: <?= $rider['license_number'] ?: '-' ?></span>
                        <br>
                        <span>Klubb: <?= $rider['club_name'] ?: '-' ?></span>
                        <?php if ($rider['email']): ?>
                        <br><span>E-post: <?= h($rider['email']) ?></span>
                        <?php endif; ?>
                    </div>
                    <div class="actions">
                        <a href="/rider/<?= $rider['id'] ?>" target="_blank" class="btn btn--sm btn--secondary">
                            <i data-lucide="external-link"></i> Visa
                        </a>
                        <?php
                        // Get other rider IDs for merge
                        $otherIds = array_filter(array_column($riders, 'id'), fn($id) => $id !== $rider['id']);
                        if (!empty($otherIds)):
                            $removeId = $otherIds[0]; // Merge with first other
                        ?>
                        <form method="POST" style="display:inline;">
                            <?= csrf_field() ?>
                            <input type="hidden" name="merge" value="1">
                            <input type="hidden" name="keep_id" value="<?= $rider['id'] ?>">
                            <input type="hidden" name="remove_id" value="<?= $removeId ?>">
                            <button type="submit" class="btn btn--sm btn-success"
                                    onclick="return confirm('Behåll <?= h($rider['firstname']) ?> (ID <?= $rider['id'] ?>) och ta bort ID <?= $removeId ?>?')">
                                <i data-lucide="check"></i> Behåll
                            </button>
                        </form>
                        <?php endif; ?>
                    </div>
                </div>
                <?php endforeach; ?>
            </div>
        </div>
        <?php endforeach; ?>

        <?php endif; ?>
    </div>
</div>

<script>
if (typeof lucide !== 'undefined') lucide.createIcons();
</script>

<?php include __DIR__ . '/components/unified-layout-footer.php'; ?>
