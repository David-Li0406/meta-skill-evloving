<?php
/**
 * Fix SWE-ID Prefix
 *
 * Finds riders with license numbers that look like SWE-IDs (7 digits starting with 25)
 * but are missing the "SWE" prefix, and adds it.
 */
require_once __DIR__ . '/../config.php';
require_admin();

$db = getDB();

// Only super_admin can run this
if (!hasRole('super_admin')) {
    die('Endast super_admin kan köra detta script');
}

$dryRun = !isset($_GET['execute']);

// Find riders with 7-digit license numbers starting with 25 (missing SWE prefix)
$riders = $db->getAll("
    SELECT id, firstname, lastname, nationality, license_number,
           (SELECT COUNT(*) FROM results WHERE cyclist_id = riders.id) as result_count
    FROM riders
    WHERE license_number REGEXP '^25[0-9]{5}$'
    ORDER BY license_number
");

$fixResult = null;
if (!$dryRun && !empty($riders)) {
    $fixed = 0;
    foreach ($riders as $rider) {
        $newLicense = 'SWE' . $rider['license_number'];
        $db->update('riders',
            ['license_number' => $newLicense],
            'id = ?',
            [$rider['id']]
        );
        $fixed++;
    }
    $fixResult = ['fixed' => $fixed];

    // Reload to show updated state
    $riders = $db->getAll("
        SELECT id, firstname, lastname, nationality, license_number,
               (SELECT COUNT(*) FROM results WHERE cyclist_id = riders.id) as result_count
        FROM riders
        WHERE license_number REGEXP '^SWE25[0-9]{5}$'
        ORDER BY license_number DESC
        LIMIT 50
    ");
}

// Page output
$page_title = 'Fixa SWE-ID prefix';
$breadcrumbs = [
    ['label' => 'Inställningar', 'url' => '/admin/settings'],
    ['label' => 'Verktyg', 'url' => '/admin/tools'],
    ['label' => 'Fixa SWE-ID prefix']
];
include __DIR__ . '/components/unified-layout.php';
?>

<?php if ($fixResult): ?>
<div class="alert alert-success mb-lg">
    <i data-lucide="check-circle"></i>
    <strong>Klart!</strong> Lade till "SWE" prefix på <?= $fixResult['fixed'] ?> licensnummer.
</div>
<?php endif; ?>

<div class="alert alert-info mb-lg">
    <i data-lucide="info"></i>
    <strong>SWE-ID prefix saknas</strong> - Hittar licensnummer som ser ut som SWE-ID (7 siffror som börjar med 25)
    men saknar "SWE" framför. T.ex. "2500581" → "SWE2500581".
</div>

<div class="card mb-lg">
    <div class="card-header" style="display: flex; justify-content: space-between; align-items: center;">
        <h3>Licensnummer utan SWE-prefix (<?= count($riders) ?>)</h3>
        <?php if (!empty($riders) && $dryRun): ?>
        <a href="?execute=1" class="btn btn-primary"
           onclick="return confirm('Lägg till SWE-prefix på <?= count($riders) ?> licensnummer?')">
            <i data-lucide="wrench"></i>
            Fixa alla (<?= count($riders) ?>)
        </a>
        <?php endif; ?>
    </div>
    <div class="card-body">
        <?php if (empty($riders)): ?>
        <div class="alert alert-success">
            <i data-lucide="check-circle"></i>
            Inga licensnummer behöver fixas!
        </div>
        <?php else: ?>
        <div class="table-responsive">
            <table class="table">
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Namn</th>
                        <th>Land</th>
                        <th>Nuvarande</th>
                        <th>Blir</th>
                        <th>Resultat</th>
                    </tr>
                </thead>
                <tbody>
                    <?php foreach ($riders as $rider): ?>
                    <tr>
                        <td><?= $rider['id'] ?></td>
                        <td><?= h($rider['firstname'] . ' ' . $rider['lastname']) ?></td>
                        <td><?= h($rider['nationality']) ?></td>
                        <td><code><?= h($rider['license_number']) ?></code></td>
                        <td><code class="text-success">SWE<?= h($rider['license_number']) ?></code></td>
                        <td><?= $rider['result_count'] ?></td>
                    </tr>
                    <?php endforeach; ?>
                </tbody>
            </table>
        </div>
        <?php endif; ?>
    </div>
</div>

<?php include __DIR__ . '/components/unified-layout-footer.php'; ?>
