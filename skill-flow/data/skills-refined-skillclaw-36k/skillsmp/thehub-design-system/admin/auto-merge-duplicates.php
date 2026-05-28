<?php
/**
 * UCI Duplicate Analysis & Merge Tool
 *
 * Finds riders with same UCI-ID and categorizes them:
 * - SAFE TO MERGE: Same UCI-ID AND similar names (likely same person)
 * - DATA CONFLICTS: Same UCI-ID but DIFFERENT names (data error - needs manual review)
 */
require_once __DIR__ . '/../config.php';
require_admin();

$db = getDB();

// Only super_admin can run this
if (!hasRole('super_admin')) {
    die('Endast super_admin kan köra detta script');
}

/**
 * Calculate name similarity (0-100%)
 * Uses both Levenshtein distance and common substring matching
 */
function calculateNameSimilarity($name1, $name2) {
    $name1 = mb_strtolower(trim($name1), 'UTF-8');
    $name2 = mb_strtolower(trim($name2), 'UTF-8');

    if ($name1 === $name2) return 100;
    if (empty($name1) || empty($name2)) return 0;

    // Check if one name contains the other (handles middle names)
    $parts1 = preg_split('/\s+/', $name1);
    $parts2 = preg_split('/\s+/', $name2);

    // Check firstname match
    $firstMatch = isset($parts1[0]) && isset($parts2[0]) &&
                  (levenshtein($parts1[0], $parts2[0]) <= 2 ||
                   strpos($parts1[0], $parts2[0]) !== false ||
                   strpos($parts2[0], $parts1[0]) !== false);

    // Check lastname match (last part of each name)
    $last1 = end($parts1);
    $last2 = end($parts2);
    $lastMatch = levenshtein($last1, $last2) <= 2 ||
                 strpos($last1, $last2) !== false ||
                 strpos($last2, $last1) !== false;

    // Both first and last name must be similar
    if ($firstMatch && $lastMatch) {
        // Calculate percentage based on Levenshtein
        $maxLen = max(strlen($name1), strlen($name2));
        $distance = levenshtein($name1, $name2);
        $similarity = (1 - ($distance / $maxLen)) * 100;
        return max($similarity, 70); // At least 70% if first+last match
    }

    // Simple Levenshtein comparison
    $maxLen = max(strlen($name1), strlen($name2));
    $distance = levenshtein($name1, $name2);
    return (1 - ($distance / $maxLen)) * 100;
}

$dryRun = !isset($_GET['execute']);
$safeToMerge = [];      // Same UCI + similar names
$dataConflicts = [];    // Same UCI + different names (data errors)
$totalSafeMerges = 0;
$totalConflicts = 0;
$totalResultsMoved = 0;

// Minimum similarity threshold for auto-merge (70%)
$SIMILARITY_THRESHOLD = 70;

// DEBUG: Check specific riders from screenshot
$debugRiders = [11075, 11055, 11056, 11057]; // Joel Westerlund and Viggo Hallman etc.
$debugInfo = [];
foreach ($debugRiders as $debugId) {
    $r = $db->getRow("SELECT id, firstname, lastname, license_number FROM riders WHERE id = ?", [$debugId]);
    if ($r) {
        $debugInfo[] = "ID {$r['id']}: {$r['firstname']} {$r['lastname']} - UCI: '{$r['license_number']}'";
    }
}

// Find all UCI-ID duplicates - only looking at license_number column
$duplicates = $db->getAll("
    SELECT
        REPLACE(REPLACE(license_number, ' ', ''), '-', '') as normalized_uci,
        GROUP_CONCAT(id ORDER BY id) as rider_ids,
        GROUP_CONCAT(CONCAT(firstname, ' ', lastname) ORDER BY id SEPARATOR ' | ') as rider_names,
        COUNT(*) as count
    FROM riders
    WHERE license_number IS NOT NULL
    AND license_number != ''
    AND REPLACE(REPLACE(license_number, ' ', ''), '-', '') != ''
    AND LENGTH(REPLACE(REPLACE(license_number, ' ', ''), '-', '')) >= 8
    GROUP BY normalized_uci
    HAVING count > 1
    ORDER BY count DESC
    LIMIT 50
");

foreach ($duplicates as $dup) {
    $riderIds = explode(',', $dup['rider_ids']);

    // Get details for each rider
    $riders = [];
    foreach ($riderIds as $riderId) {
        $rider = $db->getRow("
            SELECT r.*,
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

    $keepRider = $riders[0];
    $keepName = $keepRider['firstname'] . ' ' . $keepRider['lastname'];

    // Check each potential duplicate
    $safeMerges = [];
    $conflicts = [];

    foreach (array_slice($riders, 1) as $otherRider) {
        $otherName = $otherRider['firstname'] . ' ' . $otherRider['lastname'];
        $similarity = calculateNameSimilarity($keepName, $otherName);

        $entry = [
            'id' => $otherRider['id'],
            'name' => $otherName,
            'results' => $otherRider['result_count'],
            'birth_year' => $otherRider['birth_year'],
            'club' => $otherRider['club_name'],
            'similarity' => round($similarity, 1)
        ];

        if ($similarity >= $SIMILARITY_THRESHOLD) {
            $safeMerges[] = $entry;
        } else {
            $conflicts[] = $entry;
        }
    }

    $baseEntry = [
        'uci' => $dup['normalized_uci'],
        'keep' => [
            'id' => $keepRider['id'],
            'name' => $keepName,
            'results' => $keepRider['result_count'],
            'birth_year' => $keepRider['birth_year'],
            'club' => $keepRider['club_name']
        ]
    ];

    // Process safe merges
    if (!empty($safeMerges)) {
        $mergeEntry = $baseEntry;
        $mergeEntry['merge'] = $safeMerges;
        $mergeEntry['results_moved'] = 0;

        if (!$dryRun) {
            foreach ($safeMerges as $mergeRider) {
                // Move results
                $db->query(
                    "UPDATE results SET cyclist_id = ? WHERE cyclist_id = ?",
                    [$keepRider['id'], $mergeRider['id']]
                );
                $mergeEntry['results_moved'] += $mergeRider['results'];
                $totalResultsMoved += $mergeRider['results'];

                // Update rider_club_seasons
                $db->query(
                    "UPDATE IGNORE rider_club_seasons SET rider_id = ? WHERE rider_id = ?",
                    [$keepRider['id'], $mergeRider['id']]
                );

                // Delete duplicates from rider_club_seasons that might conflict
                $db->query(
                    "DELETE FROM rider_club_seasons WHERE rider_id = ?",
                    [$mergeRider['id']]
                );

                // Copy missing data
                $riderData = $db->getRow("SELECT * FROM riders WHERE id = ?", [$mergeRider['id']]);
                $updates = [];
                if (empty($keepRider['birth_year']) && !empty($riderData['birth_year'])) {
                    $updates['birth_year'] = $riderData['birth_year'];
                }
                if (empty($keepRider['club_id']) && !empty($riderData['club_id'])) {
                    $updates['club_id'] = $riderData['club_id'];
                }
                if (empty($keepRider['nationality']) && !empty($riderData['nationality'])) {
                    $updates['nationality'] = $riderData['nationality'];
                }
                if (empty($keepRider['gender']) && !empty($riderData['gender'])) {
                    $updates['gender'] = $riderData['gender'];
                }
                if (!empty($updates)) {
                    $db->update('riders', $updates, 'id = ?', [$keepRider['id']]);
                }

                // Delete the duplicate
                $db->delete('riders', 'id = ?', [$mergeRider['id']]);
                $totalSafeMerges++;
            }
        } else {
            $totalSafeMerges += count($safeMerges);
        }

        $safeToMerge[] = $mergeEntry;
    }

    // Record conflicts
    if (!empty($conflicts)) {
        $conflictEntry = $baseEntry;
        $conflictEntry['conflicts'] = $conflicts;
        $dataConflicts[] = $conflictEntry;
        $totalConflicts += count($conflicts);
    }
}

// Page output
$page_title = 'UCI Dublett-analys';
$breadcrumbs = [
    ['label' => 'Inställningar', 'url' => '/admin/settings'],
    ['label' => 'Verktyg', 'url' => '/admin/tools'],
    ['label' => 'UCI Dublett-analys']
];
include __DIR__ . '/components/unified-layout.php';
?>

<style>
.similarity-badge {
    display: inline-block;
    padding: 2px 8px;
    border-radius: 12px;
    font-size: 11px;
    font-weight: 600;
}
.similarity-high { background: #dcfce7; color: #166534; }
.similarity-medium { background: #fef9c3; color: #854d0e; }
.similarity-low { background: #fee2e2; color: #991b1b; }
.conflict-row { background: #fef2f2; }
.safe-row { background: #f0fdf4; }
</style>

<?php if (!empty($debugInfo)): ?>
<div class="alert alert-warning mb-lg">
    <i data-lucide="bug"></i>
    <strong>DEBUG - Specifika åkare från skärmdump:</strong><br>
    <?php foreach ($debugInfo as $d): ?>
        <?= h($d) ?><br>
    <?php endforeach; ?>
</div>
<?php endif; ?>

<?php if (!empty($duplicates) && count($duplicates) <= 5): ?>
<div class="alert alert-secondary mb-lg">
    <i data-lucide="database"></i>
    <strong>DEBUG - Rå SQL-resultat (första 5):</strong><br>
    <?php foreach (array_slice($duplicates, 0, 5) as $d): ?>
        UCI: <?= h($d['normalized_uci']) ?> | IDs: <?= h($d['rider_ids']) ?> | Namn: <?= h(substr($d['rider_names'], 0, 100)) ?>...<br>
    <?php endforeach; ?>
</div>
<?php endif; ?>

<?php if ($dryRun): ?>
<div class="alert alert-info mb-lg">
    <i data-lucide="info"></i>
    <strong>ANALYS</strong> - Inga ändringar görs ännu. Granska listan nedan.
</div>
<?php else: ?>
<div class="alert alert-success mb-lg">
    <i data-lucide="check-circle"></i>
    <strong>KLAR!</strong> Mergade <?= $totalSafeMerges ?> säkra dubletter, flyttade <?= $totalResultsMoved ?> resultat.
</div>
<?php endif; ?>

<div class="card mb-lg">
    <div class="card-header">
        <h3>Sammanfattning</h3>
    </div>
    <div class="card-body">
        <div class="grid grid-cols-3 gap-md">
            <div class="stat-card" style="border-left: 4px solid var(--color-success);">
                <div class="stat-number text-success"><?= $totalSafeMerges ?></div>
                <div class="stat-label">Säkra att slå ihop</div>
                <small class="text-secondary">Samma UCI + liknande namn</small>
            </div>
            <div class="stat-card" style="border-left: 4px solid var(--color-danger);">
                <div class="stat-number text-danger"><?= $totalConflicts ?></div>
                <div class="stat-label">Datakonflikter</div>
                <small class="text-secondary">Samma UCI men olika personer!</small>
            </div>
            <div class="stat-card">
                <div class="stat-number"><?= $totalResultsMoved ?></div>
                <div class="stat-label">Resultat att flytta</div>
            </div>
        </div>

        <?php if ($dryRun && $totalSafeMerges > 0): ?>
        <div class="mt-lg">
            <a href="?execute=1" class="btn btn-success" onclick="return confirm('Slå ihop <?= $totalSafeMerges ?> SÄKRA dubletter?\n\nKonflikter (<?= $totalConflicts ?> st) kommer INTE röras.')">
                <i data-lucide="git-merge"></i>
                Slå ihop <?= $totalSafeMerges ?> säkra dubletter
            </a>
        </div>
        <?php endif; ?>
    </div>
</div>

<?php if (!empty($dataConflicts)): ?>
<div class="card mb-lg">
    <div class="card-header" style="background: #fef2f2;">
        <h3 class="text-danger">
            <i data-lucide="alert-triangle"></i>
            Datakonflikter - Kräver manuell granskning (<?= count($dataConflicts) ?> grupper)
        </h3>
    </div>
    <div class="card-body">
        <div class="alert alert-danger mb-md">
            <i data-lucide="alert-octagon"></i>
            <strong>VARNING!</strong> Dessa poster har samma UCI-ID men OLIKA namn.
            Detta är troligen datafel som behöver rättas manuellt.
            <br><small>Antingen har fel UCI-ID tilldelats, eller så är det olika format av samma namn.</small>
        </div>

        <div class="table-responsive">
            <table class="table">
                <thead>
                    <tr>
                        <th>UCI-ID</th>
                        <th>Person 1 (flest resultat)</th>
                        <th>Person 2+ (konflikt)</th>
                        <th>Likhet</th>
                    </tr>
                </thead>
                <tbody>
                <?php foreach ($dataConflicts as $entry): ?>
                    <tr class="conflict-row">
                        <td><code><?= h($entry['uci']) ?></code></td>
                        <td>
                            <strong><?= h($entry['keep']['name']) ?></strong>
                            <br><small class="text-secondary">
                                <a href="/admin/riders/edit/<?= $entry['keep']['id'] ?>">ID: <?= $entry['keep']['id'] ?></a>,
                                <?= $entry['keep']['results'] ?> resultat
                                <?php if ($entry['keep']['birth_year']): ?>, f.<?= $entry['keep']['birth_year'] ?><?php endif; ?>
                                <?php if ($entry['keep']['club']): ?>, <?= h($entry['keep']['club']) ?><?php endif; ?>
                            </small>
                        </td>
                        <td>
                            <?php foreach ($entry['conflicts'] as $c): ?>
                            <div class="mb-xs">
                                <strong class="text-danger"><?= h($c['name']) ?></strong>
                                <br><small class="text-secondary">
                                    <a href="/admin/riders/edit/<?= $c['id'] ?>">ID: <?= $c['id'] ?></a>,
                                    <?= $c['results'] ?> resultat
                                    <?php if ($c['birth_year']): ?>, f.<?= $c['birth_year'] ?><?php endif; ?>
                                    <?php if ($c['club']): ?>, <?= h($c['club']) ?><?php endif; ?>
                                </small>
                            </div>
                            <?php endforeach; ?>
                        </td>
                        <td>
                            <?php foreach ($entry['conflicts'] as $c): ?>
                            <span class="similarity-badge similarity-low"><?= $c['similarity'] ?>%</span><br>
                            <?php endforeach; ?>
                        </td>
                    </tr>
                <?php endforeach; ?>
                </tbody>
            </table>
        </div>
    </div>
</div>
<?php endif; ?>

<?php if (!empty($safeToMerge)): ?>
<div class="card">
    <div class="card-header" style="background: #f0fdf4;">
        <h3 class="text-success">
            <i data-lucide="check-circle"></i>
            Säkra att slå ihop (<?= count($safeToMerge) ?> grupper)
        </h3>
    </div>
    <div class="card-body">
        <div class="table-responsive">
            <table class="table">
                <thead>
                    <tr>
                        <th>UCI-ID</th>
                        <th>Behåll</th>
                        <th>Ta bort</th>
                        <th>Likhet</th>
                    </tr>
                </thead>
                <tbody>
                <?php foreach ($safeToMerge as $entry): ?>
                    <tr class="safe-row">
                        <td><code><?= h($entry['uci']) ?></code></td>
                        <td>
                            <strong><?= h($entry['keep']['name']) ?></strong>
                            <br><small class="text-secondary">
                                ID: <?= $entry['keep']['id'] ?>,
                                <?= $entry['keep']['results'] ?> resultat
                                <?php if ($entry['keep']['birth_year']): ?>, f.<?= $entry['keep']['birth_year'] ?><?php endif; ?>
                                <?php if ($entry['keep']['club']): ?>, <?= h($entry['keep']['club']) ?><?php endif; ?>
                            </small>
                        </td>
                        <td>
                            <?php foreach ($entry['merge'] as $m): ?>
                            <div class="mb-xs">
                                <?= h($m['name']) ?>
                                <small>(ID: <?= $m['id'] ?>, <?= $m['results'] ?> resultat)</small>
                            </div>
                            <?php endforeach; ?>
                        </td>
                        <td>
                            <?php foreach ($entry['merge'] as $m): ?>
                            <span class="similarity-badge <?= $m['similarity'] >= 90 ? 'similarity-high' : 'similarity-medium' ?>"><?= $m['similarity'] ?>%</span><br>
                            <?php endforeach; ?>
                        </td>
                    </tr>
                <?php endforeach; ?>
                </tbody>
            </table>
        </div>
    </div>
</div>
<?php elseif (empty($dataConflicts)): ?>
<div class="alert alert-success">
    <i data-lucide="check-circle"></i>
    Inga UCI-ID dubletter hittades!
</div>
<?php endif; ?>

<?php include __DIR__ . '/components/unified-layout-footer.php'; ?>
