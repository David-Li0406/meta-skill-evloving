<?php
/**
 * Find Name Duplicates
 *
 * Finds riders with the same name but different license numbers.
 * These are likely the same person imported multiple times.
 *
 * Priority for merging:
 * 1. Real UCI-ID (14+ chars) > Temp SWE-ID > No ID
 * 2. Most results
 * 3. Most complete profile
 */
require_once __DIR__ . '/../config.php';
require_admin();

$db = getDB();

// Only super_admin can run this
if (!hasRole('super_admin')) {
    die('Endast super_admin kan köra detta script');
}

// Create exclusions table if not exists
$db->query("CREATE TABLE IF NOT EXISTS duplicate_exclusions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    rider_id_1 INT NOT NULL,
    rider_id_2 INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY unique_pair (rider_id_1, rider_id_2)
)");

$dryRun = !isset($_GET['execute']);
$mergeId = isset($_GET['merge']) ? (int)$_GET['merge'] : null;
$excludeAction = isset($_GET['exclude']);
$mergeAllAction = isset($_GET['merge_all']);

// Handle exclude action (mark as not duplicates)
$excludeResult = null;
if ($excludeAction && !$dryRun) {
    $ids = isset($_GET['ids']) ? array_map('intval', explode(',', $_GET['ids'])) : [];
    if (count($ids) >= 2) {
        sort($ids);
        $excluded = 0;
        // Store all pairs as exclusions
        for ($i = 0; $i < count($ids); $i++) {
            for ($j = $i + 1; $j < count($ids); $j++) {
                $db->query("INSERT IGNORE INTO duplicate_exclusions (rider_id_1, rider_id_2) VALUES (?, ?)",
                    [$ids[$i], $ids[$j]]);
                $excluded++;
            }
        }
        $excludeResult = ['excluded' => $excluded, 'ids' => $ids];
    }
}

// Get all excluded pairs for filtering
$excludedPairs = [];
$exclusions = $db->getAll("SELECT rider_id_1, rider_id_2 FROM duplicate_exclusions");
foreach ($exclusions as $exc) {
    $key = $exc['rider_id_1'] . '-' . $exc['rider_id_2'];
    $excludedPairs[$key] = true;
}

function isExcludedPair($id1, $id2, $excludedPairs) {
    $ids = [$id1, $id2];
    sort($ids);
    $key = $ids[0] . '-' . $ids[1];
    return isset($excludedPairs[$key]);
}

function groupIsExcluded($riderIds, $excludedPairs) {
    // Group is excluded if ALL pairs in the group are excluded
    $ids = array_map('intval', $riderIds);
    for ($i = 0; $i < count($ids); $i++) {
        for ($j = $i + 1; $j < count($ids); $j++) {
            if (!isExcludedPair($ids[$i], $ids[$j], $excludedPairs)) {
                return false; // At least one pair is not excluded
            }
        }
    }
    return true; // All pairs are excluded
}

// Helper function to determine license type priority
function getLicensePriority($license) {
    if (empty($license)) return 0; // No license
    $clean = str_replace([' ', '-'], '', $license);

    // Temp SWE-ID: SWE25XXXXX (SWE + 7 digits) - check first!
    if (preg_match('/^SWE\d{7}$/', $clean)) {
        return 1; // Low priority - temporary ID
    }

    // Real UCI-ID: Pure numeric, typically 9-12 digits
    if (preg_match('/^\d{9,14}$/', $clean)) {
        return 3; // Highest priority - real UCI-ID
    }

    // Other format (unknown)
    return 2; // Medium priority
}

function getLicenseTypeName($license) {
    if (empty($license)) return 'Inget ID';
    $clean = str_replace([' ', '-'], '', $license);

    // Temp SWE-ID - check first!
    if (preg_match('/^SWE\d{7}$/', $clean)) {
        return 'SWE-ID';
    }
    // Real UCI-ID: Pure numeric
    if (preg_match('/^\d{9,14}$/', $clean)) {
        return 'UCI-ID';
    }
    return 'Annat';
}

// Handle merge action
$mergeResult = null;
if ($mergeId !== null && !$dryRun) {
    // Get the merge group
    $keepId = isset($_GET['keep']) ? (int)$_GET['keep'] : 0;
    $removeIds = isset($_GET['remove']) ? array_map('intval', explode(',', $_GET['remove'])) : [];

    if ($keepId && !empty($removeIds)) {
        $totalMoved = 0;

        foreach ($removeIds as $removeId) {
            if ($removeId <= 0) continue;

            // Move results from remove to keep using proper update method
            $moved = $db->update('results',
                ['cyclist_id' => $keepId],
                'cyclist_id = ?',
                [$removeId]
            );
            $totalMoved += $moved;

            // Delete the duplicate rider using proper delete method
            $db->delete('riders', 'id = ?', [$removeId]);
        }

        $mergeResult = [
            'success' => true,
            'kept' => $keepId,
            'removed' => $removeIds,
            'results_moved' => $totalMoved
        ];
    }
}

// Handle merge all action - will be processed after we find duplicates
$mergeAllResult = null;

// Helper to normalize names (collapse spaces, trim, lowercase)
function normalizeName($name) {
    $name = trim($name);
    $name = preg_replace('/\s+/', ' ', $name); // Collapse multiple spaces
    $name = mb_strtolower($name, 'UTF-8');
    return $name;
}

// Helper to get last word of surname (for fuzzy matching)
function getLastSurnamePart($lastname) {
    $parts = preg_split('/[\s\-]+/', trim($lastname));
    return mb_strtolower(end($parts), 'UTF-8');
}

// Helper for Levenshtein-based name similarity
function lastnameSimilarity($ln1, $ln2) {
    $ln1 = mb_strtolower(trim($ln1), 'UTF-8');
    $ln2 = mb_strtolower(trim($ln2), 'UTF-8');
    if ($ln1 === $ln2) return 100;
    if (strlen($ln1) < 2 || strlen($ln2) < 2) return 0;
    // Limit for levenshtein
    $ln1 = substr($ln1, 0, 255);
    $ln2 = substr($ln2, 0, 255);
    $maxLen = max(strlen($ln1), strlen($ln2));
    if ($maxLen === 0) return 0;
    $distance = levenshtein($ln1, $ln2);
    return round((1 - $distance / $maxLen) * 100);
}

// Find all name duplicates using PHP normalization
// This catches variations with different spacing, invisible chars, etc.
$allRiders = $db->getAll("
    SELECT id, firstname, lastname
    FROM riders
    WHERE firstname IS NOT NULL AND firstname != ''
    AND lastname IS NOT NULL AND lastname != ''
");

// Group by normalized name (PHP handles all whitespace normalization)
$nameGroups = [];
foreach ($allRiders as $r) {
    $normalizedFn = preg_replace('/\s+/', ' ', mb_strtolower(trim($r['firstname']), 'UTF-8'));
    $normalizedLn = preg_replace('/\s+/', ' ', mb_strtolower(trim($r['lastname']), 'UTF-8'));
    $key = $normalizedFn . '|' . $normalizedLn;
    $nameGroups[$key][] = $r['id'];
}

// Filter groups with 2+ riders
$nameDuplicates = [];
foreach ($nameGroups as $key => $ids) {
    if (count($ids) > 1) {
        list($fn, $ln) = explode('|', $key);
        $nameDuplicates[] = [
            'fn' => $fn,
            'ln' => $ln,
            'rider_ids' => implode(',', $ids),
            'count' => count($ids)
        ];
    }
}

// Sort by count DESC and limit
usort($nameDuplicates, fn($a, $b) => $b['count'] - $a['count']);
$nameDuplicates = array_slice($nameDuplicates, 0, 200);

// Also find fuzzy duplicates (same firstname + same last part of surname)
// This catches "Mattias Sjöström-Varg" vs "Mattias Varg"
// Using UPPER() instead of LOWER() for MySQL compatibility
$fuzzyDuplicates = $db->getAll("
    SELECT
        UPPER(TRIM(firstname)) as fn,
        SUBSTRING_INDEX(UPPER(TRIM(lastname)), '-', -1) as ln_last,
        SUBSTRING_INDEX(UPPER(TRIM(lastname)), ' ', -1) as ln_word,
        GROUP_CONCAT(DISTINCT id ORDER BY id) as rider_ids,
        COUNT(DISTINCT id) as count
    FROM riders
    WHERE firstname IS NOT NULL AND firstname != ''
    AND lastname IS NOT NULL AND lastname != ''
    GROUP BY fn, ln_last
    HAVING count > 1 AND COUNT(DISTINCT UPPER(TRIM(lastname))) > 1
    ORDER BY count DESC
    LIMIT 100
");

// Merge the two result sets (exact + fuzzy), avoiding duplicates
$allDuplicates = $nameDuplicates;
$seenIds = [];
foreach ($nameDuplicates as $dup) {
    foreach (explode(',', $dup['rider_ids']) as $id) {
        $seenIds[$id] = true;
    }
}
foreach ($fuzzyDuplicates as $dup) {
    $ids = explode(',', $dup['rider_ids']);
    $newIds = array_filter($ids, fn($id) => !isset($seenIds[$id]));
    if (count($newIds) >= 2 || (count($newIds) >= 1 && count($ids) >= 2)) {
        $allDuplicates[] = [
            'fn' => $dup['fn'],
            'ln' => $dup['ln_last'] . ' (fuzzy)',
            'rider_ids' => $dup['rider_ids'],
            'count' => $dup['count']
        ];
    }
}

// Find spelling-variation duplicates (Ågren vs Åhgren, etc.)
// Group by firstname, then compare lastnames with Levenshtein
$ridersByFirstname = [];
foreach ($allRiders as $r) {
    $normalizedFn = preg_replace('/\s+/', ' ', mb_strtolower(trim($r['firstname']), 'UTF-8'));
    $ridersByFirstname[$normalizedFn][] = $r;
}

foreach ($ridersByFirstname as $fn => $ridersWithSameFn) {
    if (count($ridersWithSameFn) < 2) continue;

    // Compare all pairs for similar lastnames
    for ($i = 0; $i < count($ridersWithSameFn); $i++) {
        for ($j = $i + 1; $j < count($ridersWithSameFn); $j++) {
            $r1 = $ridersWithSameFn[$i];
            $r2 = $ridersWithSameFn[$j];

            // Skip if already in seenIds together
            if (isset($seenIds[$r1['id']]) && isset($seenIds[$r2['id']])) continue;

            $similarity = lastnameSimilarity($r1['lastname'], $r2['lastname']);

            // If 80-99% similar (not exact, but close), it's a potential spelling variation
            if ($similarity >= 80 && $similarity < 100) {
                $allDuplicates[] = [
                    'fn' => $fn,
                    'ln' => $r1['lastname'] . ' / ' . $r2['lastname'] . " ({$similarity}%)",
                    'rider_ids' => $r1['id'] . ',' . $r2['id'],
                    'count' => 2
                ];
                $seenIds[$r1['id']] = true;
                $seenIds[$r2['id']] = true;
            }
        }
    }
}

$duplicateGroups = [];
$totalDuplicates = 0;

foreach ($allDuplicates as $dup) {
    $riderIds = explode(',', $dup['rider_ids']);

    // Get details for each rider
    $riders = [];
    foreach ($riderIds as $riderId) {
        $rider = $db->getRow("
            SELECT r.id, r.firstname, r.lastname, r.birth_year, r.nationality,
                   r.license_number, r.club_id,
                   (SELECT COUNT(*) FROM results WHERE cyclist_id = r.id) as result_count,
                   c.name as club_name
            FROM riders r
            LEFT JOIN clubs c ON r.club_id = c.id
            WHERE r.id = ?
        ", [$riderId]);
        if ($rider) {
            $rider['license_priority'] = getLicensePriority($rider['license_number']);
            $rider['license_type'] = getLicenseTypeName($rider['license_number']);
            $riders[] = $rider;
        }
    }

    if (count($riders) < 2) continue;

    // Check birth years - flag but don't skip different birth years
    // Different birth years might still be the same person with wrong data
    $birthYears = [];
    foreach ($riders as $r) {
        if (!empty($r['birth_year'])) {
            $birthYears[$r['birth_year']] = true;
        }
    }
    $hasDifferentBirthYears = count($birthYears) > 1;

    // Check if they have different license numbers (not just format differences)
    $uniqueLicenses = [];
    foreach ($riders as $r) {
        $normalized = preg_replace('/[^A-Z0-9]/i', '', $r['license_number'] ?? '');
        if (!empty($normalized)) {
            $uniqueLicenses[$normalized] = true;
        }
    }

    // Check license status for info display
    $hasNoLicense = false;
    $hasDifferentLicenses = count($uniqueLicenses) > 1;
    foreach ($riders as $r) {
        if (empty($r['license_number'])) {
            $hasNoLicense = true;
            break;
        }
    }
    $allSameLicense = !$hasDifferentLicenses && !$hasNoLicense && count($uniqueLicenses) === 1;

    // IMPORTANT: Skip if multiple riders have DIFFERENT real UCI-IDs
    // Different UCI-IDs = different people with same name, NOT duplicates!
    $realUciIds = [];
    foreach ($riders as $r) {
        if ($r['license_priority'] == 3) { // Real UCI-ID (not SWE-ID)
            $normalized = preg_replace('/[^0-9]/', '', $r['license_number'] ?? '');
            if (!empty($normalized)) {
                $realUciIds[$normalized] = true;
            }
        }
    }
    // If we have 2+ different real UCI-IDs, these are definitely different people
    if (count($realUciIds) >= 2) {
        continue; // Skip this group - not duplicates!
    }

    // Skip if this group has been excluded (marked as "not duplicates")
    if (groupIsExcluded($riderIds, $excludedPairs)) continue;

    // Sort by priority: license type, then results, then completeness
    usort($riders, function($a, $b) {
        // First by license priority (higher = better)
        if ($a['license_priority'] != $b['license_priority']) {
            return $b['license_priority'] - $a['license_priority'];
        }
        // Then by result count
        if ($a['result_count'] != $b['result_count']) {
            return $b['result_count'] - $a['result_count'];
        }
        // Then by completeness
        $aComplete = (!empty($a['birth_year']) ? 1 : 0) + (!empty($a['club_id']) ? 1 : 0);
        $bComplete = (!empty($b['birth_year']) ? 1 : 0) + (!empty($b['club_id']) ? 1 : 0);
        return $bComplete - $aComplete;
    });

    $keepRider = $riders[0];
    $mergeRiders = array_slice($riders, 1);

    $duplicateGroups[] = [
        'name' => $riders[0]['firstname'] . ' ' . $riders[0]['lastname'],
        'total_riders' => count($riders),
        'total_results' => array_sum(array_column($riders, 'result_count')),
        'keep' => $keepRider,
        'merge' => $mergeRiders,
        'all_riders' => $riders,
        'has_different_birth_years' => $hasDifferentBirthYears,
        'all_same_license' => $allSameLicense,
        'birth_years' => array_keys($birthYears)
    ];

    $totalDuplicates += count($mergeRiders);
}

// Handle merge all action (after we have the duplicate groups)
if ($mergeAllAction && !$dryRun && !empty($duplicateGroups)) {
    $totalMerged = 0;
    $totalResultsMoved = 0;
    $groupsMerged = 0;

    foreach ($duplicateGroups as $group) {
        $keepId = $group['keep']['id'];
        foreach ($group['merge'] as $mergeRider) {
            $removeId = $mergeRider['id'];
            if ($removeId <= 0) continue;

            // Move results
            $moved = $db->update('results',
                ['cyclist_id' => $keepId],
                'cyclist_id = ?',
                [$removeId]
            );
            $totalResultsMoved += $moved;

            // Delete duplicate
            $db->delete('riders', 'id = ?', [$removeId]);
            $totalMerged++;
        }
        $groupsMerged++;
    }

    $mergeAllResult = [
        'groups' => $groupsMerged,
        'merged' => $totalMerged,
        'results_moved' => $totalResultsMoved
    ];

    // Clear the groups since we just merged them all
    $duplicateGroups = [];
    $totalDuplicates = 0;
}

// Page output
$page_title = 'Hitta namndubletter';
$breadcrumbs = [
    ['label' => 'Inställningar', 'url' => '/admin/settings'],
    ['label' => 'Verktyg', 'url' => '/admin/tools'],
    ['label' => 'Hitta namndubletter']
];
include __DIR__ . '/components/unified-layout.php';
?>

<style>
.keep-badge { background: #dcfce7; color: #166534; padding: 2px 8px; border-radius: 4px; font-size: 11px; }
.merge-badge { background: #fef3c7; color: #92400e; padding: 2px 8px; border-radius: 4px; font-size: 11px; }
.uci-badge { background: #dbeafe; color: #1e40af; padding: 2px 8px; border-radius: 4px; font-size: 11px; }
.swe-badge { background: #fef3c7; color: #92400e; padding: 2px 8px; border-radius: 4px; font-size: 11px; }
.no-badge { background: #f3f4f6; color: #6b7280; padding: 2px 8px; border-radius: 4px; font-size: 11px; }
.duplicate-card { border: 1px solid var(--color-border); border-radius: var(--radius-md); margin-bottom: var(--space-md); }
.duplicate-card-header { background: var(--color-star-fade); padding: var(--space-md); border-bottom: 1px solid var(--color-border); display: flex; justify-content: space-between; align-items: center; }
.duplicate-card-body { padding: var(--space-md); }
.rider-row { display: flex; gap: var(--space-md); align-items: center; padding: var(--space-sm) 0; border-bottom: 1px solid var(--color-border); }
.rider-row:last-child { border-bottom: none; }
.rider-info { flex: 1; }
.rider-stats { display: flex; gap: var(--space-md); font-size: 13px; color: var(--color-text); }
</style>

<?php if ($mergeResult): ?>
<div class="alert alert-success mb-lg">
    <i data-lucide="check-circle"></i>
    <strong>Sammanslagning klar!</strong>
    Behöll rider #<?= $mergeResult['kept'] ?>, tog bort <?= count($mergeResult['removed']) ?> dubbletter.
    <?= $mergeResult['results_moved'] ?> resultat flyttades.
</div>
<?php endif; ?>

<?php if ($mergeAllResult): ?>
<div class="alert alert-success mb-lg">
    <i data-lucide="check-circle"></i>
    <strong>Alla sammanslagningar klara!</strong>
    <?= $mergeAllResult['groups'] ?> grupper, <?= $mergeAllResult['merged'] ?> dubletter borttagna,
    <?= $mergeAllResult['results_moved'] ?> resultat flyttade.
</div>
<?php endif; ?>

<?php if ($excludeResult): ?>
<div class="alert alert-info mb-lg">
    <i data-lucide="ban"></i>
    <strong>Markerade som ej dubletter!</strong>
    <?= count($excludeResult['ids']) ?> riders kommer inte längre visas som dubletter av varandra.
</div>
<?php endif; ?>

<div class="alert alert-info mb-lg">
    <i data-lucide="info"></i>
    <strong>Namndubletter</strong> - Samma namn, samma födelseår, men olika licens-ID.
    <br>Endast åkare med samma (eller tomt) födelseår visas - olika födelseår = olika personer.
    <br><strong>Prioritet:</strong> UCI-ID > SWE-ID > Inget ID, sedan flest resultat.
</div>

<div class="card mb-lg">
    <div class="card-header">
        <h3>Sammanfattning</h3>
    </div>
    <div class="card-body">
        <div class="grid grid-cols-2 gap-md">
            <div class="stat-card" style="border-left: 4px solid var(--color-warning);">
                <div class="stat-number"><?= count($duplicateGroups) ?></div>
                <div class="stat-label">Namngrupper med dubletter</div>
            </div>
            <div class="stat-card" style="border-left: 4px solid var(--color-danger);">
                <div class="stat-number"><?= $totalDuplicates ?></div>
                <div class="stat-label">Riders att slå ihop</div>
            </div>
        </div>
    </div>
</div>

<?php if (!empty($duplicateGroups)): ?>
<div class="card">
    <div class="card-header" style="display: flex; justify-content: space-between; align-items: center;">
        <h3>Namndubletter (<?= count($duplicateGroups) ?>)</h3>
        <a href="?execute=1&merge_all=1"
           class="btn btn-danger"
           onclick="return confirm('SLÅ IHOP ALLA <?= count($duplicateGroups) ?> GRUPPER?\\n\\nDetta slår ihop <?= $totalDuplicates ?> dubletter och kan inte ångras!')">
            <i data-lucide="git-merge"></i>
            Slå ihop alla (<?= $totalDuplicates ?>)
        </a>
    </div>
    <div class="card-body">
        <?php foreach ($duplicateGroups as $index => $group): ?>
        <div class="duplicate-card" <?= !empty($group['has_different_birth_years']) ? 'style="border-color: var(--color-warning);"' : '' ?>>
            <div class="duplicate-card-header">
                <div>
                    <strong><?= h($group['name']) ?></strong>
                    <span class="text-secondary">(<?= $group['total_riders'] ?> poster, <?= $group['total_results'] ?> resultat totalt)</span>
                    <?php if (!empty($group['has_different_birth_years'])): ?>
                        <span class="badge badge-warning" style="margin-left: 8px;">Olika födelseår: <?= implode(', ', $group['birth_years']) ?></span>
                    <?php endif; ?>
                    <?php if (!empty($group['all_same_license'])): ?>
                        <span class="badge badge-info" style="margin-left: 8px;">Samma licens-ID</span>
                    <?php endif; ?>
                </div>
                <?php
                $keepId = $group['keep']['id'];
                $removeIds = implode(',', array_column($group['merge'], 'id'));
                $allIds = implode(',', array_column($group['all_riders'], 'id'));
                ?>
                <div style="display: flex; gap: var(--space-sm);">
                    <a href="?execute=1&exclude=1&ids=<?= $allIds ?>"
                       class="btn btn-sm btn-secondary"
                       title="Markera som ej dubletter"
                       onclick="return confirm('Markera dessa <?= $group['total_riders'] ?> som EJ dubletter?\\n\\nDe kommer inte längre visas i denna lista.')">
                        <i data-lucide="ban"></i>
                        Ej dubbletter
                    </a>
                    <a href="?execute=1&merge=<?= $index ?>&keep=<?= $keepId ?>&remove=<?= $removeIds ?>"
                       class="btn btn-sm btn-warning"
                       onclick="return confirm('Slå ihop <?= count($group['merge']) ?> dubletter till <?= h($group['keep']['firstname'] . ' ' . $group['keep']['lastname']) ?> (ID: <?= $keepId ?>)?\\n\\nResultat flyttas och dubbletter tas bort.')">
                        <i data-lucide="git-merge"></i>
                        Slå ihop
                    </a>
                </div>
            </div>
            <div class="duplicate-card-body">
                <!-- Keep this one -->
                <div class="rider-row" style="background: #f0fdf4;">
                    <span class="keep-badge">BEHÅLL</span>
                    <div class="rider-info">
                        <strong><?= h($group['keep']['firstname'] . ' ' . $group['keep']['lastname']) ?></strong>
                        <?php if ($group['keep']['birth_year']): ?>
                            <small>(<?= $group['keep']['birth_year'] ?>)</small>
                        <?php endif; ?>
                        <?php if ($group['keep']['club_name']): ?>
                            <small class="text-secondary">- <?= h($group['keep']['club_name']) ?></small>
                        <?php endif; ?>
                    </div>
                    <div class="rider-stats">
                        <span>
                            <?php if ($group['keep']['license_priority'] == 3): ?>
                                <span class="uci-badge">UCI-ID</span>
                            <?php elseif ($group['keep']['license_priority'] == 1): ?>
                                <span class="swe-badge">SWE-ID</span>
                            <?php else: ?>
                                <span class="no-badge"><?= $group['keep']['license_type'] ?></span>
                            <?php endif; ?>
                            <code><?= h($group['keep']['license_number'] ?: '-') ?></code>
                        </span>
                        <span><strong><?= $group['keep']['result_count'] ?></strong> resultat</span>
                        <span>ID: <?= $group['keep']['id'] ?></span>
                    </div>
                </div>

                <!-- Merge these -->
                <?php foreach ($group['merge'] as $rider): ?>
                <div class="rider-row" style="background: #fefce8;">
                    <span class="merge-badge">SLÅ IHOP</span>
                    <div class="rider-info">
                        <?= h($rider['firstname'] . ' ' . $rider['lastname']) ?>
                        <?php if ($rider['birth_year']): ?>
                            <small>(<?= $rider['birth_year'] ?>)</small>
                        <?php endif; ?>
                        <?php if ($rider['nationality'] && $rider['nationality'] != $group['keep']['nationality']): ?>
                            <small class="text-warning"><?= h($rider['nationality']) ?></small>
                        <?php endif; ?>
                        <?php if ($rider['club_name']): ?>
                            <small class="text-secondary">- <?= h($rider['club_name']) ?></small>
                        <?php endif; ?>
                    </div>
                    <div class="rider-stats">
                        <span>
                            <?php if ($rider['license_priority'] == 3): ?>
                                <span class="uci-badge">UCI-ID</span>
                            <?php elseif ($rider['license_priority'] == 1): ?>
                                <span class="swe-badge">SWE-ID</span>
                            <?php else: ?>
                                <span class="no-badge"><?= $rider['license_type'] ?></span>
                            <?php endif; ?>
                            <code><?= h($rider['license_number'] ?: '-') ?></code>
                        </span>
                        <span><strong><?= $rider['result_count'] ?></strong> resultat</span>
                        <span>ID: <?= $rider['id'] ?></span>
                    </div>
                </div>
                <?php endforeach; ?>
            </div>
        </div>
        <?php endforeach; ?>
    </div>
</div>
<?php else: ?>
<div class="alert alert-success">
    <i data-lucide="check-circle"></i>
    Inga namndubletter hittades!
</div>
<?php endif; ?>

<!-- Debug: Search for specific name -->
<?php
$searchName = $_GET['search'] ?? '';
$debugResults = [];
if ($searchName) {
    $debugResults = $db->getAll("
        SELECT id, firstname, lastname, birth_year, nationality, license_number,
               HEX(firstname) as fn_hex, HEX(lastname) as ln_hex,
               LENGTH(firstname) as fn_len, LENGTH(lastname) as ln_len,
               (SELECT COUNT(*) FROM results WHERE cyclist_id = riders.id) as result_count
        FROM riders
        WHERE LOWER(firstname) LIKE ? OR LOWER(lastname) LIKE ?
        ORDER BY lastname, firstname
    ", ['%' . strtolower($searchName) . '%', '%' . strtolower($searchName) . '%']);

    // Check if any are excluded
    $excludedWith = [];
    foreach ($debugResults as $r) {
        foreach ($debugResults as $r2) {
            if ($r['id'] < $r2['id']) {
                $key = $r['id'] . '-' . $r2['id'];
                if (isset($excludedPairs[$key])) {
                    $excludedWith[] = "ID {$r['id']} ↔ ID {$r2['id']} är markerade som EJ dubletter";
                }
            }
        }
    }
}
?>

<div class="card mt-lg">
    <div class="card-header">
        <h3>Debug: Sök specifikt namn</h3>
    </div>
    <div class="card-body">
        <form method="get" style="display: flex; gap: var(--space-md); align-items: center; margin-bottom: var(--space-md);">
            <input type="text" name="search" class="form-input" placeholder="Sök namn..." value="<?= h($searchName) ?>" style="width: 300px;">
            <button type="submit" class="btn btn-primary">Sök</button>
        </form>

        <?php if ($searchName && !empty($debugResults)): ?>
        <div class="alert alert-info mb-md">
            Hittade <?= count($debugResults) ?> träffar för "<?= h($searchName) ?>"
        </div>

        <?php if (!empty($excludedWith)): ?>
        <div class="alert alert-warning mb-md">
            <strong>Exkluderade par:</strong><br>
            <?= implode('<br>', $excludedWith) ?>
        </div>
        <?php endif; ?>

        <div class="table-responsive">
            <table class="table">
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Förnamn</th>
                        <th>Efternamn</th>
                        <th>År</th>
                        <th>Land</th>
                        <th>Licens</th>
                        <th>Resultat</th>
                        <th>FN längd</th>
                        <th>LN längd</th>
                    </tr>
                </thead>
                <tbody>
                    <?php foreach ($debugResults as $r): ?>
                    <tr>
                        <td><?= $r['id'] ?></td>
                        <td><code><?= h($r['firstname']) ?></code></td>
                        <td><code><?= h($r['lastname']) ?></code></td>
                        <td><?= $r['birth_year'] ?: '-' ?></td>
                        <td><?= h($r['nationality']) ?></td>
                        <td><code><?= h($r['license_number']) ?></code></td>
                        <td><?= $r['result_count'] ?></td>
                        <td><?= $r['fn_len'] ?></td>
                        <td><?= $r['ln_len'] ?></td>
                    </tr>
                    <?php endforeach; ?>
                </tbody>
            </table>
        </div>

        <?php if (count($debugResults) >= 2): ?>
        <div class="mt-md">
            <strong>Jämförelse av första två:</strong><br>
            <?php
            $r1 = $debugResults[0];
            $r2 = $debugResults[1];
            $fn1 = strtolower(trim($r1['firstname']));
            $fn2 = strtolower(trim($r2['firstname']));
            $ln1 = strtolower(trim($r1['lastname']));
            $ln2 = strtolower(trim($r2['lastname']));
            ?>
            <code>fn1: "<?= $fn1 ?>" (<?= strlen($fn1) ?> tecken)</code><br>
            <code>fn2: "<?= $fn2 ?>" (<?= strlen($fn2) ?> tecken)</code><br>
            <code>Förnamn matchar: <?= $fn1 === $fn2 ? 'JA' : 'NEJ' ?></code><br><br>
            <code>ln1: "<?= $ln1 ?>" (<?= strlen($ln1) ?> tecken)</code><br>
            <code>ln2: "<?= $ln2 ?>" (<?= strlen($ln2) ?> tecken)</code><br>
            <code>Efternamn matchar: <?= $ln1 === $ln2 ? 'JA' : 'NEJ' ?></code>
        </div>
        <?php endif; ?>

        <?php elseif ($searchName): ?>
        <div class="alert alert-warning">Inga träffar för "<?= h($searchName) ?>"</div>
        <?php endif; ?>
    </div>
</div>

<?php include __DIR__ . '/components/unified-layout-footer.php'; ?>
