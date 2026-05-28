<?php
/**
 * Fix Corrupted License IDs
 *
 * Handles two types of problems:
 * 1. Real UCI-IDs (14+ chars) assigned to multiple different people
 * 2. Temporary SWE-IDs (format SWE25XXXXX) assigned to multiple people
 *
 * For real UCI-IDs: Keep for person with most results, give others new SWE-ID
 * For temp SWE-IDs: Keep for person with most results, give others new unique SWE-ID
 */
require_once __DIR__ . '/../config.php';
require_admin();

$db = getDB();

// Only super_admin can run this
if (!hasRole('super_admin')) {
    die('Endast super_admin kan köra detta script');
}

$dryRun = !isset($_GET['execute']);
$mode = $_GET['mode'] ?? 'all'; // 'all', 'uci', 'swe'

// Helper function to determine if license is real UCI or temp SWE
function isRealUciId($license) {
    if (empty($license)) return false;

    // Remove spaces
    $clean = str_replace(' ', '', $license);

    // Temp SWE-ID format with dashes: SWE-2025-00001
    if (preg_match('/^SWE-\d{4}-\d{5}$/', $clean)) {
        return false; // This is a temp SWE-ID, not real UCI
    }

    // Temp SWE-ID format without dashes: SWE2500318 (10 chars, 7 digits after SWE)
    if (preg_match('/^SWE\d{7}$/', $clean)) {
        return false; // This is a temp SWE-ID, not real UCI
    }

    // Real UCI format: 3 letter country code + 11 chars = 14+ total
    // Example: SWE19900515001
    if (strlen($clean) >= 14 && preg_match('/^[A-Z]{3}\d{11}/', $clean)) {
        return true;
    }

    return false;
}

// Find the highest existing SWE-ID number to generate new unique ones
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

// Get next SWE-ID number (will be incremented as we use them)
$nextSweIdNumber = getNextSweIdNumber($db);

// Find all license_numbers with multiple owners
$duplicates = $db->getAll("
    SELECT
        license_number,
        GROUP_CONCAT(id ORDER BY id) as rider_ids,
        COUNT(*) as count
    FROM riders
    WHERE license_number IS NOT NULL
    AND license_number != ''
    AND LENGTH(license_number) >= 5
    GROUP BY license_number
    HAVING count > 1
    ORDER BY count DESC
");

$realUciConflicts = [];
$tempSweConflicts = [];
$totalUciFixed = 0;
$totalSweFixed = 0;
$newIdsAssigned = [];

foreach ($duplicates as $entry) {
    $riderIds = explode(',', $entry['rider_ids']);
    $isRealUci = isRealUciId($entry['license_number']);

    // Get details for each rider
    $riders = [];
    foreach ($riderIds as $riderId) {
        $rider = $db->getRow("
            SELECT r.id, r.firstname, r.lastname, r.birth_year, r.club_id, r.license_number,
                   (SELECT COUNT(*) FROM results WHERE cyclist_id = r.id) as result_count,
                   c.name as club_name
            FROM riders r
            LEFT JOIN clubs c ON r.club_id = c.id
            WHERE r.id = ?
        ", [$riderId]);
        if ($rider) {
            $riders[] = $rider;
        }
    }

    if (count($riders) < 2) continue;

    // Sort by result count (highest first), then by completeness
    usort($riders, function($a, $b) {
        if ($a['result_count'] != $b['result_count']) {
            return $b['result_count'] - $a['result_count'];
        }
        $aComplete = (!empty($a['birth_year']) ? 1 : 0) + (!empty($a['club_id']) ? 1 : 0);
        $bComplete = (!empty($b['birth_year']) ? 1 : 0) + (!empty($b['club_id']) ? 1 : 0);
        return $bComplete - $aComplete;
    });

    if ($isRealUci) {
        // Real UCI-ID: Check if names are different (corruption)
        $firstRider = $riders[0];
        $firstName1 = mb_strtolower($firstRider['firstname'], 'UTF-8');
        $lastName1 = mb_strtolower($firstRider['lastname'], 'UTF-8');

        $hasDifferentNames = false;
        foreach (array_slice($riders, 1) as $otherRider) {
            $firstName2 = mb_strtolower($otherRider['firstname'], 'UTF-8');
            $lastName2 = mb_strtolower($otherRider['lastname'], 'UTF-8');

            $firstNameDist = levenshtein($firstName1, $firstName2);
            $lastNameDist = levenshtein($lastName1, $lastName2);

            if ($firstNameDist > 3 && $lastNameDist > 3) {
                $hasDifferentNames = true;
                break;
            }
        }

        // Only process if different names (otherwise it's a real duplicate, not corruption)
        if (!$hasDifferentNames) continue;

        // Keep UCI for first rider (most results), give others new SWE-ID
        $keepRider = $riders[0];
        $fixRiders = array_slice($riders, 1);

        $logEntry = [
            'license' => $entry['license_number'],
            'total_affected' => count($riders),
            'keep' => [
                'id' => $keepRider['id'],
                'name' => $keepRider['firstname'] . ' ' . $keepRider['lastname'],
                'results' => $keepRider['result_count'],
                'birth_year' => $keepRider['birth_year'],
                'club' => $keepRider['club_name']
            ],
            'fix' => []
        ];

        foreach ($fixRiders as $rider) {
            $newSweId = generateNewSweId($nextSweIdNumber);
            $nextSweIdNumber++;

            $logEntry['fix'][] = [
                'id' => $rider['id'],
                'name' => $rider['firstname'] . ' ' . $rider['lastname'],
                'results' => $rider['result_count'],
                'new_id' => $newSweId
            ];

            if (!$dryRun && $mode !== 'swe') {
                $db->update('riders', ['license_number' => $newSweId], 'id = ?', [$rider['id']]);
                $totalUciFixed++;
                $newIdsAssigned[] = ['rider_id' => $rider['id'], 'name' => $rider['firstname'] . ' ' . $rider['lastname'], 'new_id' => $newSweId];
            }
        }

        $realUciConflicts[] = $logEntry;
    } else {
        // Temp SWE-ID: Keep for person with most results, give others new unique SWE-ID
        $keepRider = $riders[0];
        $fixRiders = array_slice($riders, 1);

        $logEntry = [
            'license' => $entry['license_number'],
            'total_affected' => count($riders),
            'keep' => [
                'id' => $keepRider['id'],
                'name' => $keepRider['firstname'] . ' ' . $keepRider['lastname'],
                'results' => $keepRider['result_count'],
                'birth_year' => $keepRider['birth_year'],
                'club' => $keepRider['club_name']
            ],
            'fix' => []
        ];

        foreach ($fixRiders as $rider) {
            $newSweId = generateNewSweId($nextSweIdNumber);
            $nextSweIdNumber++;

            $logEntry['fix'][] = [
                'id' => $rider['id'],
                'name' => $rider['firstname'] . ' ' . $rider['lastname'],
                'results' => $rider['result_count'],
                'new_id' => $newSweId
            ];

            if (!$dryRun && $mode !== 'uci') {
                $db->update('riders', ['license_number' => $newSweId], 'id = ?', [$rider['id']]);
                $totalSweFixed++;
                $newIdsAssigned[] = ['rider_id' => $rider['id'], 'name' => $rider['firstname'] . ' ' . $rider['lastname'], 'new_id' => $newSweId];
            }
        }

        $tempSweConflicts[] = $logEntry;
    }
}

// Calculate totals
$totalUciToFix = array_sum(array_map(fn($e) => count($e['fix']), $realUciConflicts));
$totalSweToFix = array_sum(array_map(fn($e) => count($e['fix']), $tempSweConflicts));

// Page output
$page_title = 'Fixa duplicerade licens-ID';
$breadcrumbs = [
    ['label' => 'Inställningar', 'url' => '/admin/settings'],
    ['label' => 'Verktyg', 'url' => '/admin/tools'],
    ['label' => 'Fixa duplicerade licens-ID']
];
include __DIR__ . '/components/unified-layout.php';
?>

<style>
.keep-badge { background: #dcfce7; color: #166534; padding: 2px 8px; border-radius: 4px; font-size: 11px; }
.new-badge { background: #dbeafe; color: #1e40af; padding: 2px 8px; border-radius: 4px; font-size: 11px; }
.uci-badge { background: #dbeafe; color: #1e40af; padding: 2px 8px; border-radius: 4px; font-size: 11px; }
.swe-badge { background: #fef3c7; color: #92400e; padding: 2px 8px; border-radius: 4px; font-size: 11px; }
</style>

<?php if ($dryRun): ?>
<div class="alert alert-warning mb-lg">
    <i data-lucide="alert-triangle"></i>
    <strong>FÖRHANDSGRANSKNING</strong> - Inga ändringar görs ännu.
    <br>Detta verktyg hittar licens-ID:n som felaktigt tilldelats flera personer.
    <br><strong>Åkare som får sitt ID ändrat tilldelas ett nytt unikt SWE-ID.</strong>
</div>
<?php else: ?>
<div class="alert alert-success mb-lg">
    <i data-lucide="check-circle"></i>
    <strong>KLAR!</strong>
    <?php if ($mode === 'all' || $mode === 'uci'): ?>Fixade <?= $totalUciFixed ?> åkare med UCI-konflikt. <?php endif; ?>
    <?php if ($mode === 'all' || $mode === 'swe'): ?>Fixade <?= $totalSweFixed ?> åkare med SWE-ID-konflikt.<?php endif; ?>
    <br><small>Alla berörda åkare har fått nya unika SWE-ID.</small>
</div>

<?php if (!empty($newIdsAssigned)): ?>
<div class="card mb-lg">
    <div class="card-header">
        <h3>Nya tilldelade SWE-ID (<?= count($newIdsAssigned) ?>)</h3>
    </div>
    <div class="card-body">
        <div class="table-responsive">
            <table class="table table-sm">
                <thead>
                    <tr>
                        <th>Rider ID</th>
                        <th>Namn</th>
                        <th>Nytt SWE-ID</th>
                    </tr>
                </thead>
                <tbody>
                <?php foreach (array_slice($newIdsAssigned, 0, 50) as $assignment): ?>
                    <tr>
                        <td><?= $assignment['rider_id'] ?></td>
                        <td><?= h($assignment['name']) ?></td>
                        <td><code class="new-badge"><?= h($assignment['new_id']) ?></code></td>
                    </tr>
                <?php endforeach; ?>
                <?php if (count($newIdsAssigned) > 50): ?>
                    <tr>
                        <td colspan="3" class="text-secondary">... och <?= count($newIdsAssigned) - 50 ?> till</td>
                    </tr>
                <?php endif; ?>
                </tbody>
            </table>
        </div>
    </div>
</div>
<?php endif; ?>
<?php endif; ?>

<div class="card mb-lg">
    <div class="card-header">
        <h3>Sammanfattning</h3>
    </div>
    <div class="card-body">
        <div class="grid grid-cols-2 gap-md">
            <div class="stat-card" style="border-left: 4px solid #1e40af;">
                <div class="stat-number" style="color: #1e40af;"><?= count($realUciConflicts) ?></div>
                <div class="stat-label">Riktiga UCI-ID konflikter</div>
                <small class="text-secondary"><?= $totalUciToFix ?> åkare får nytt SWE-ID</small>
            </div>
            <div class="stat-card" style="border-left: 4px solid #92400e;">
                <div class="stat-number" style="color: #92400e;"><?= count($tempSweConflicts) ?></div>
                <div class="stat-label">Temporära SWE-ID konflikter</div>
                <small class="text-secondary"><?= $totalSweToFix ?> åkare får nytt SWE-ID</small>
            </div>
        </div>

        <?php if ($dryRun && ($totalUciToFix > 0 || $totalSweToFix > 0)): ?>
        <div class="mt-lg" style="display: flex; gap: var(--space-md); flex-wrap: wrap;">
            <?php if ($totalUciToFix > 0): ?>
            <a href="?execute=1&mode=uci" class="btn btn-primary" onclick="return confirm('Fixa UCI-ID för <?= $totalUciToFix ?> åkare?\n\nDe får nya unika SWE-ID.')">
                <i data-lucide="badge-check"></i>
                Fixa UCI-ID (<?= $totalUciToFix ?>)
            </a>
            <?php endif; ?>

            <?php if ($totalSweToFix > 0): ?>
            <a href="?execute=1&mode=swe" class="btn btn-warning" onclick="return confirm('Fixa SWE-ID för <?= $totalSweToFix ?> åkare?\n\nDe får nya unika SWE-ID.')">
                <i data-lucide="refresh-cw"></i>
                Fixa SWE-ID (<?= $totalSweToFix ?>)
            </a>
            <?php endif; ?>

            <?php if ($totalUciToFix > 0 && $totalSweToFix > 0): ?>
            <a href="?execute=1&mode=all" class="btn btn-danger" onclick="return confirm('Fixa ALLA (<?= $totalUciToFix + $totalSweToFix ?> åkare)?\n\nAlla får nya unika SWE-ID.')">
                <i data-lucide="zap"></i>
                Fixa ALLA (<?= $totalUciToFix + $totalSweToFix ?>)
            </a>
            <?php endif; ?>
        </div>
        <?php endif; ?>
    </div>
</div>

<!-- Tabs for different views -->
<div class="tabs mb-lg">
    <nav class="tabs-nav">
        <button class="tab-btn active" data-tab="swe-conflicts">
            Temporära SWE-ID <span class="badge" style="background: #fef3c7; color: #92400e;"><?= count($tempSweConflicts) ?></span>
        </button>
        <button class="tab-btn" data-tab="uci-conflicts">
            Riktiga UCI-ID <span class="badge" style="background: #dbeafe; color: #1e40af;"><?= count($realUciConflicts) ?></span>
        </button>
    </nav>

    <!-- SWE-ID Conflicts -->
    <div class="tab-content active" id="swe-conflicts">
        <?php if (!empty($tempSweConflicts)): ?>
        <div class="alert alert-info mb-md">
            <i data-lucide="info"></i>
            Temporära SWE-ID (format: <code>SWE25XXXXX</code>) ska vara unika och låsta till varje åkare.
            <br><strong>Åkaren med flest resultat behåller ID:t, övriga får nya unika SWE-ID.</strong>
        </div>
        <div class="table-responsive">
            <table class="table">
                <thead>
                    <tr>
                        <th>Duplicerat ID</th>
                        <th>Behåller <span class="keep-badge">BEHÅLL</span></th>
                        <th>Får nytt ID <span class="new-badge">NYTT</span></th>
                        <th>Antal</th>
                    </tr>
                </thead>
                <tbody>
                <?php foreach ($tempSweConflicts as $entry): ?>
                    <tr>
                        <td>
                            <code class="swe-badge"><?= h($entry['license']) ?></code>
                            <br><small class="text-warning"><?= $entry['total_affected'] ?> personer</small>
                        </td>
                        <td>
                            <strong class="text-success"><?= h($entry['keep']['name']) ?></strong>
                            <br><small class="text-secondary">
                                ID: <?= $entry['keep']['id'] ?>,
                                <?= $entry['keep']['results'] ?> resultat
                                <?php if ($entry['keep']['birth_year']): ?>, f.<?= $entry['keep']['birth_year'] ?><?php endif; ?>
                            </small>
                        </td>
                        <td>
                            <?php
                            $showCount = min(3, count($entry['fix']));
                            $hiddenCount = count($entry['fix']) - $showCount;
                            foreach (array_slice($entry['fix'], 0, $showCount) as $f): ?>
                            <div class="mb-xs">
                                <span><?= h($f['name']) ?></span>
                                <code class="new-badge"><?= h($f['new_id']) ?></code>
                                <small>(<?= $f['results'] ?> res)</small>
                            </div>
                            <?php endforeach; ?>
                            <?php if ($hiddenCount > 0): ?>
                            <small class="text-secondary">... och <?= $hiddenCount ?> till</small>
                            <?php endif; ?>
                        </td>
                        <td><strong><?= count($entry['fix']) ?></strong></td>
                    </tr>
                <?php endforeach; ?>
                </tbody>
            </table>
        </div>
        <?php else: ?>
        <div class="alert alert-success">
            <i data-lucide="check-circle"></i>
            Inga duplicerade temporära SWE-ID hittades!
        </div>
        <?php endif; ?>
    </div>

    <!-- UCI-ID Conflicts -->
    <div class="tab-content" id="uci-conflicts">
        <?php if (!empty($realUciConflicts)): ?>
        <div class="alert alert-info mb-md">
            <i data-lucide="info"></i>
            Riktiga UCI-ID (14+ tecken) som tilldelats flera OLIKA personer. Detta är datakorruption.
            <br><strong>Åkaren med flest resultat behåller UCI-ID:t, övriga får nya SWE-ID.</strong>
        </div>
        <div class="table-responsive">
            <table class="table">
                <thead>
                    <tr>
                        <th>UCI-ID</th>
                        <th>Behåller <span class="keep-badge">BEHÅLL</span></th>
                        <th>Får nytt SWE-ID <span class="new-badge">NYTT</span></th>
                        <th>Antal</th>
                    </tr>
                </thead>
                <tbody>
                <?php foreach ($realUciConflicts as $entry): ?>
                    <tr>
                        <td>
                            <code class="uci-badge"><?= h($entry['license']) ?></code>
                            <br><small class="text-danger"><?= $entry['total_affected'] ?> personer</small>
                        </td>
                        <td>
                            <strong class="text-success"><?= h($entry['keep']['name']) ?></strong>
                            <br><small class="text-secondary">
                                ID: <?= $entry['keep']['id'] ?>,
                                <?= $entry['keep']['results'] ?> resultat
                                <?php if ($entry['keep']['birth_year']): ?>, f.<?= $entry['keep']['birth_year'] ?><?php endif; ?>
                                <?php if ($entry['keep']['club']): ?>, <?= h($entry['keep']['club']) ?><?php endif; ?>
                            </small>
                        </td>
                        <td>
                            <?php
                            $showCount = min(3, count($entry['fix']));
                            $hiddenCount = count($entry['fix']) - $showCount;
                            foreach (array_slice($entry['fix'], 0, $showCount) as $f): ?>
                            <div class="mb-xs">
                                <span><?= h($f['name']) ?></span>
                                <code class="new-badge"><?= h($f['new_id']) ?></code>
                                <small>(<?= $f['results'] ?> res)</small>
                            </div>
                            <?php endforeach; ?>
                            <?php if ($hiddenCount > 0): ?>
                            <small class="text-secondary">... och <?= $hiddenCount ?> till</small>
                            <?php endif; ?>
                        </td>
                        <td><strong><?= count($entry['fix']) ?></strong></td>
                    </tr>
                <?php endforeach; ?>
                </tbody>
            </table>
        </div>
        <?php else: ?>
        <div class="alert alert-success">
            <i data-lucide="check-circle"></i>
            Inga korrupta riktiga UCI-ID hittades!
        </div>
        <?php endif; ?>
    </div>
</div>

<script>
document.querySelectorAll('.tab-btn').forEach(btn => {
    btn.addEventListener('click', () => {
        const tabId = btn.dataset.tab;
        document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
        document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
        btn.classList.add('active');
        document.getElementById(tabId).classList.add('active');
    });
});
</script>

<?php include __DIR__ . '/components/unified-layout-footer.php'; ?>
