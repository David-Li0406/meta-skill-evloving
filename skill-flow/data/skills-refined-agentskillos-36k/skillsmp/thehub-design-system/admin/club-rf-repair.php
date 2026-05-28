<?php
/**
 * Club RF Repair Tool
 *
 * Identifies and fixes incorrectly matched/renamed clubs from RF sync
 */

require_once __DIR__ . '/../config.php';
require_once __DIR__ . '/../includes/auth.php';
requireLogin();

$page_title = 'RF-reparation av Klubbar';
$breadcrumbs = [
    ['label' => 'Admin', 'url' => '/admin'],
    ['label' => 'Klubbar', 'url' => '/admin/clubs.php'],
    ['label' => 'RF-reparation']
];

global $pdo;

$message = '';
$messageType = 'info';

// Handle actions
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $action = $_POST['action'] ?? '';

    if ($action === 'rename_club') {
        $clubId = (int)$_POST['club_id'];
        $newName = trim($_POST['new_name']);

        if ($clubId && $newName) {
            $stmt = $pdo->prepare("UPDATE clubs SET name = ? WHERE id = ?");
            $stmt->execute([$newName, $clubId]);
            $message = "Klubb #{$clubId} omdöpt till: {$newName}";
            $messageType = 'success';
        }
    }

    if ($action === 'remove_rf') {
        $clubId = (int)$_POST['club_id'];
        if ($clubId) {
            $stmt = $pdo->prepare("UPDATE clubs SET rf_registered = 0, rf_registered_year = NULL, scf_district = NULL WHERE id = ?");
            $stmt->execute([$clubId]);
            $message = "RF-koppling borttagen från klubb #{$clubId}";
            $messageType = 'success';
        }
    }

    if ($action === 'create_club') {
        $name = trim($_POST['name']);
        $district = trim($_POST['district']);

        if ($name) {
            $stmt = $pdo->prepare("INSERT INTO clubs (name, rf_registered, rf_registered_year, scf_district, active, created_at) VALUES (?, 1, 2025, ?, 1, NOW())");
            $stmt->execute([$name, $district]);
            $newId = $pdo->lastInsertId();
            $message = "Skapade ny klubb: {$name} (ID: {$newId})";
            $messageType = 'success';
        }
    }
}

// Get all RF-registered clubs with rider counts
$rfClubs = $pdo->query("
    SELECT
        c.id,
        c.name,
        c.scf_district,
        c.rf_registered_year,
        (SELECT COUNT(*) FROM riders r WHERE r.club_id = c.id) as rider_count,
        (SELECT COUNT(*) FROM results res WHERE res.club_id = c.id) as result_count
    FROM clubs c
    WHERE c.rf_registered = 1
    ORDER BY c.name
")->fetchAll();

// Get clubs with "suspicious" names (might have been renamed incorrectly)
// These are clubs where the name contains common patterns that suggest renaming
$suspiciousClubs = $pdo->query("
    SELECT
        c.id,
        c.name,
        c.scf_district,
        (SELECT COUNT(*) FROM riders r WHERE r.club_id = c.id) as rider_count,
        (SELECT COUNT(*) FROM results res WHERE res.club_id = c.id) as result_count
    FROM clubs c
    WHERE c.rf_registered = 1
    AND (
        c.name LIKE '%Idrottssällskap%'
        OR c.name LIKE '%Idrottsförening%'
        OR c.name LIKE '%Sportklubb%'
        OR c.name LIKE '%Gymnastik%'
        OR c.name LIKE '%Fotboll%'
        OR c.name LIKE '%Skid%'
    )
    AND c.rider_count > 0
    ORDER BY (SELECT COUNT(*) FROM riders r WHERE r.club_id = c.id) DESC
")->fetchAll();

// Get clubs that have many riders but short/abbreviated names (likely the original cycling clubs)
$likelyCyclingClubs = $pdo->query("
    SELECT
        c.id,
        c.name,
        c.scf_district,
        c.rf_registered,
        (SELECT COUNT(*) FROM riders r WHERE r.club_id = c.id) as rider_count
    FROM clubs c
    WHERE (SELECT COUNT(*) FROM riders r WHERE r.club_id = c.id) > 5
    AND (
        c.name LIKE '%CK%'
        OR c.name LIKE '%Cykel%'
        OR c.name LIKE '% SC'
        OR c.name LIKE '%MTB%'
    )
    ORDER BY (SELECT COUNT(*) FROM riders r WHERE r.club_id = c.id) DESC
")->fetchAll();

// Find potential duplicates (similar names)
$potentialDuplicates = $pdo->query("
    SELECT
        c1.id as id1, c1.name as name1, c1.rf_registered as rf1,
        (SELECT COUNT(*) FROM riders WHERE club_id = c1.id) as riders1,
        c2.id as id2, c2.name as name2, c2.rf_registered as rf2,
        (SELECT COUNT(*) FROM riders WHERE club_id = c2.id) as riders2
    FROM clubs c1
    JOIN clubs c2 ON c1.id < c2.id
    WHERE (
        SUBSTRING_INDEX(c1.name, ' ', 1) = SUBSTRING_INDEX(c2.name, ' ', 1)
        AND LENGTH(SUBSTRING_INDEX(c1.name, ' ', 1)) > 3
    )
    ORDER BY SUBSTRING_INDEX(c1.name, ' ', 1), c1.name
")->fetchAll();

include __DIR__ . '/components/unified-layout.php';
?>

<div class="container py-lg">
    <?php if ($message): ?>
        <div class="alert alert-<?= $messageType ?> mb-lg"><?= htmlspecialchars($message) ?></div>
    <?php endif; ?>

    <div class="alert alert-warning mb-lg">
        <strong>OBS!</strong> Detta verktyg hjälper dig identifiera och fixa klubbar som kan ha blivit felaktigt matchade eller omdöpta av RF-synkningen.
    </div>

    <!-- Potential Duplicates -->
    <div class="card mb-4">
        <div class="card-header" style="background: var(--color-error); color: white;">
            <h3>Potentiella dubbletter (<?= count($potentialDuplicates) ?>)</h3>
        </div>
        <div class="card-body">
            <p class="text-muted mb-md">Klubbar som börjar på samma ord - kan vara dubbletter eller felmatchningar.</p>

            <?php if (empty($potentialDuplicates)): ?>
                <p class="text-success">Inga potentiella dubbletter hittades.</p>
            <?php else: ?>
                <div class="table-responsive">
                    <table class="table table-sm">
                        <thead>
                            <tr>
                                <th>Klubb 1</th>
                                <th>RF</th>
                                <th>Åkare</th>
                                <th>Klubb 2</th>
                                <th>RF</th>
                                <th>Åkare</th>
                                <th>Åtgärd</th>
                            </tr>
                        </thead>
                        <tbody>
                            <?php foreach ($potentialDuplicates as $dup): ?>
                            <tr>
                                <td>
                                    <a href="/admin/club-edit.php?id=<?= $dup['id1'] ?>" style="color: var(--color-accent);">
                                        <?= htmlspecialchars($dup['name1']) ?>
                                    </a>
                                </td>
                                <td><?= $dup['rf1'] ? '<span class="badge badge-success">Ja</span>' : '<span class="badge badge-secondary">Nej</span>' ?></td>
                                <td><strong><?= $dup['riders1'] ?></strong></td>
                                <td>
                                    <a href="/admin/club-edit.php?id=<?= $dup['id2'] ?>" style="color: var(--color-accent);">
                                        <?= htmlspecialchars($dup['name2']) ?>
                                    </a>
                                </td>
                                <td><?= $dup['rf2'] ? '<span class="badge badge-success">Ja</span>' : '<span class="badge badge-secondary">Nej</span>' ?></td>
                                <td><strong><?= $dup['riders2'] ?></strong></td>
                                <td>
                                    <a href="/admin/club-edit.php?id=<?= $dup['id1'] ?>" class="btn btn-sm btn-secondary">
                                        <i data-lucide="pencil"></i>
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

    <!-- Suspicious Clubs (might have been renamed) -->
    <div class="card mb-4">
        <div class="card-header" style="background: var(--color-warning); color: black;">
            <h3>Misstänkta felmatchningar (<?= count($suspiciousClubs) ?>)</h3>
        </div>
        <div class="card-body">
            <p class="text-muted mb-md">RF-kopplade klubbar med "Idrottssällskap/Idrottsförening" i namnet som har många åkare - kan vara cykelklubbar som fått fel namn.</p>

            <?php if (empty($suspiciousClubs)): ?>
                <p class="text-success">Inga misstänkta felmatchningar hittades.</p>
            <?php else: ?>
                <div class="table-responsive">
                    <table class="table table-sm">
                        <thead>
                            <tr>
                                <th>Klubbnamn</th>
                                <th>Distrikt</th>
                                <th>Åkare</th>
                                <th>Resultat</th>
                                <th>Åtgärder</th>
                            </tr>
                        </thead>
                        <tbody>
                            <?php foreach ($suspiciousClubs as $club): ?>
                            <tr>
                                <td>
                                    <a href="/admin/club-edit.php?id=<?= $club['id'] ?>" style="color: var(--color-accent);">
                                        <?= htmlspecialchars($club['name']) ?>
                                    </a>
                                </td>
                                <td><?= htmlspecialchars($club['scf_district'] ?? '-') ?></td>
                                <td><strong><?= $club['rider_count'] ?></strong></td>
                                <td><?= $club['result_count'] ?></td>
                                <td>
                                    <form method="POST" style="display: inline-flex; gap: 4px; align-items: center;">
                                        <input type="hidden" name="action" value="rename_club">
                                        <input type="hidden" name="club_id" value="<?= $club['id'] ?>">
                                        <input type="text" name="new_name" placeholder="Nytt namn..." class="form-input" style="width: 150px; padding: 4px 8px; font-size: 0.8rem;">
                                        <button type="submit" class="btn btn-sm btn-warning" title="Döp om">
                                            <i data-lucide="edit-2"></i>
                                        </button>
                                    </form>
                                    <form method="POST" style="display: inline;">
                                        <input type="hidden" name="action" value="remove_rf">
                                        <input type="hidden" name="club_id" value="<?= $club['id'] ?>">
                                        <button type="submit" class="btn btn-sm btn-danger" title="Ta bort RF-koppling" onclick="return confirm('Ta bort RF-koppling?')">
                                            <i data-lucide="unlink"></i>
                                        </button>
                                    </form>
                                </td>
                            </tr>
                            <?php endforeach; ?>
                        </tbody>
                    </table>
                </div>
            <?php endif; ?>
        </div>
    </div>

    <!-- Cycling clubs with many riders -->
    <div class="card mb-4">
        <div class="card-header">
            <h3>Cykelklubbar med många åkare (<?= count($likelyCyclingClubs) ?>)</h3>
        </div>
        <div class="card-body">
            <p class="text-muted mb-md">Klubbar med "CK", "Cykel", "SC" eller "MTB" i namnet och mer än 5 åkare.</p>

            <div class="table-responsive" style="max-height: 400px; overflow-y: auto;">
                <table class="table table-sm">
                    <thead style="position: sticky; top: 0; background: var(--color-bg-surface);">
                        <tr>
                            <th>Klubbnamn</th>
                            <th>Distrikt</th>
                            <th>RF</th>
                            <th>Åkare</th>
                            <th>Åtgärd</th>
                        </tr>
                    </thead>
                    <tbody>
                        <?php foreach ($likelyCyclingClubs as $club): ?>
                        <tr>
                            <td>
                                <a href="/admin/club-edit.php?id=<?= $club['id'] ?>" style="color: var(--color-accent);">
                                    <?= htmlspecialchars($club['name']) ?>
                                </a>
                            </td>
                            <td><?= htmlspecialchars($club['scf_district'] ?? '-') ?></td>
                            <td><?= $club['rf_registered'] ? '<span class="badge badge-success">Ja</span>' : '<span class="badge badge-secondary">Nej</span>' ?></td>
                            <td><strong><?= $club['rider_count'] ?></strong></td>
                            <td>
                                <a href="/admin/club-edit.php?id=<?= $club['id'] ?>" class="btn btn-sm btn-secondary">
                                    <i data-lucide="pencil"></i> Redigera
                                </a>
                            </td>
                        </tr>
                        <?php endforeach; ?>
                    </tbody>
                </table>
            </div>
        </div>
    </div>

    <!-- Quick Create Club -->
    <div class="card mb-4">
        <div class="card-header">
            <h3>Skapa saknad klubb</h3>
        </div>
        <div class="card-body">
            <form method="POST">
                <input type="hidden" name="action" value="create_club">
                <div style="display: flex; gap: var(--space-md); flex-wrap: wrap;">
                    <div class="form-group" style="flex: 1; min-width: 200px;">
                        <label class="form-label">Klubbnamn</label>
                        <input type="text" name="name" class="form-input" placeholder="T.ex. Arvika CK" required>
                    </div>
                    <div class="form-group" style="flex: 1; min-width: 200px;">
                        <label class="form-label">SCF-distrikt</label>
                        <input type="text" name="district" class="form-input" placeholder="T.ex. Värmlands Cykelförbund">
                    </div>
                    <div class="form-group" style="align-self: flex-end;">
                        <button type="submit" class="btn btn-primary">
                            <i data-lucide="plus"></i> Skapa klubb
                        </button>
                    </div>
                </div>
            </form>
        </div>
    </div>

</div>

<?php include __DIR__ . '/components/unified-layout-footer.php'; ?>
