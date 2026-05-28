<?php
/**
 * Assign Missing SWE-ID
 *
 * Finds riders without any license_number and assigns them unique SWE-IDs.
 * Format: SWE25XXXXX (10 chars)
 */
require_once __DIR__ . '/../config.php';
require_admin();

$db = getDB();

// Only super_admin can run this
if (!hasRole('super_admin')) {
    die('Endast super_admin kan köra detta script');
}

$dryRun = !isset($_GET['execute']);

// Find the highest existing SWE-ID number
function getNextSweIdNumber($db) {
    $result = $db->getRow("
        SELECT MAX(CAST(SUBSTRING(license_number, 4) AS UNSIGNED)) as max_num
        FROM riders
        WHERE license_number REGEXP '^SWE[0-9]{7}$'
    ");
    return ($result['max_num'] ?? 2500000) + 1;
}

// Generate a new unique SWE-ID
function generateNewSweId($number) {
    return 'SWE' . str_pad($number, 7, '0', STR_PAD_LEFT);
}

// Find all riders without license_number
$ridersWithoutId = $db->getAll("
    SELECT r.id, r.firstname, r.lastname, r.birth_year, r.nationality,
           (SELECT COUNT(*) FROM results WHERE cyclist_id = r.id) as result_count,
           c.name as club_name
    FROM riders r
    LEFT JOIN clubs c ON r.club_id = c.id
    WHERE (r.license_number IS NULL OR r.license_number = '')
    ORDER BY result_count DESC, r.lastname, r.firstname
");

$totalWithoutId = count($ridersWithoutId);
$totalAssigned = 0;
$assignedList = [];

if (!$dryRun && $totalWithoutId > 0) {
    $nextSweIdNumber = getNextSweIdNumber($db);

    foreach ($ridersWithoutId as $rider) {
        $newSweId = generateNewSweId($nextSweIdNumber);
        $nextSweIdNumber++;

        $db->update('riders', ['license_number' => $newSweId], 'id = ?', [$rider['id']]);
        $totalAssigned++;

        $assignedList[] = [
            'id' => $rider['id'],
            'name' => $rider['firstname'] . ' ' . $rider['lastname'],
            'new_id' => $newSweId,
            'results' => $rider['result_count']
        ];
    }
}

// Page output
$page_title = 'Tilldela saknade SWE-ID';
$breadcrumbs = [
    ['label' => 'Inställningar', 'url' => '/admin/settings'],
    ['label' => 'Verktyg', 'url' => '/admin/tools'],
    ['label' => 'Tilldela saknade SWE-ID']
];
include __DIR__ . '/components/unified-layout.php';
?>

<style>
.swe-badge { background: #fef3c7; color: #92400e; padding: 2px 8px; border-radius: 4px; font-size: 11px; }
</style>

<?php if ($dryRun): ?>
<div class="alert alert-warning mb-lg">
    <i data-lucide="alert-triangle"></i>
    <strong>FÖRHANDSGRANSKNING</strong> - Inga ändringar görs ännu.
    <br>Detta verktyg tilldelar unika SWE-ID till alla åkare som saknar licens-nummer.
</div>
<?php else: ?>
<div class="alert alert-success mb-lg">
    <i data-lucide="check-circle"></i>
    <strong>KLAR!</strong> Tilldelade <?= $totalAssigned ?> nya SWE-ID.
</div>
<?php endif; ?>

<div class="card mb-lg">
    <div class="card-header">
        <h3>Sammanfattning</h3>
    </div>
    <div class="card-body">
        <div class="stat-card" style="border-left: 4px solid var(--color-warning);">
            <div class="stat-number"><?= $totalWithoutId ?></div>
            <div class="stat-label">Åkare utan licens-ID</div>
            <small class="text-secondary">Dessa saknar helt license_number</small>
        </div>

        <?php if ($dryRun && $totalWithoutId > 0): ?>
        <div class="mt-lg">
            <a href="?execute=1" class="btn btn-warning" onclick="return confirm('Tilldela SWE-ID till <?= $totalWithoutId ?> åkare?\n\nFormat: SWE25XXXXX')">
                <i data-lucide="badge-plus"></i>
                Tilldela SWE-ID (<?= $totalWithoutId ?>)
            </a>
        </div>
        <?php endif; ?>
    </div>
</div>

<?php if (!$dryRun && !empty($assignedList)): ?>
<div class="card mb-lg">
    <div class="card-header">
        <h3>Tilldelade SWE-ID (<?= count($assignedList) ?>)</h3>
    </div>
    <div class="card-body">
        <div class="table-responsive">
            <table class="table table-sm">
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Namn</th>
                        <th>Nytt SWE-ID</th>
                        <th>Resultat</th>
                    </tr>
                </thead>
                <tbody>
                <?php foreach (array_slice($assignedList, 0, 100) as $r): ?>
                    <tr>
                        <td><?= $r['id'] ?></td>
                        <td><?= h($r['name']) ?></td>
                        <td><code class="swe-badge"><?= h($r['new_id']) ?></code></td>
                        <td><?= $r['results'] ?></td>
                    </tr>
                <?php endforeach; ?>
                <?php if (count($assignedList) > 100): ?>
                    <tr>
                        <td colspan="4" class="text-secondary">... och <?= count($assignedList) - 100 ?> till</td>
                    </tr>
                <?php endif; ?>
                </tbody>
            </table>
        </div>
    </div>
</div>
<?php endif; ?>

<?php if ($dryRun && $totalWithoutId > 0): ?>
<div class="card">
    <div class="card-header">
        <h3>Åkare utan licens-ID (<?= $totalWithoutId ?>)</h3>
    </div>
    <div class="card-body">
        <div class="table-responsive">
            <table class="table table-sm">
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Namn</th>
                        <th>År</th>
                        <th>Klubb</th>
                        <th>Resultat</th>
                    </tr>
                </thead>
                <tbody>
                <?php foreach (array_slice($ridersWithoutId, 0, 100) as $r): ?>
                    <tr>
                        <td><?= $r['id'] ?></td>
                        <td><?= h($r['firstname'] . ' ' . $r['lastname']) ?></td>
                        <td><?= $r['birth_year'] ?: '-' ?></td>
                        <td><?= h($r['club_name'] ?: '-') ?></td>
                        <td><?= $r['result_count'] ?></td>
                    </tr>
                <?php endforeach; ?>
                <?php if ($totalWithoutId > 100): ?>
                    <tr>
                        <td colspan="5" class="text-secondary">... och <?= $totalWithoutId - 100 ?> till</td>
                    </tr>
                <?php endif; ?>
                </tbody>
            </table>
        </div>
    </div>
</div>
<?php elseif ($dryRun): ?>
<div class="alert alert-success">
    <i data-lucide="check-circle"></i>
    Alla åkare har redan licens-ID!
</div>
<?php endif; ?>

<?php include __DIR__ . '/components/unified-layout-footer.php'; ?>
