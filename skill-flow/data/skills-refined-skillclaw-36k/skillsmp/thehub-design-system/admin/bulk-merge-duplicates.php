<?php
/**
 * Bulk Merge Duplicates - Hitta och slå ihop ALLA dubletter
 * Kombinerar UCI-matchning och namnmatchning
 */
require_once __DIR__ . '/../config.php';
require_admin();

$db = getDB();
$pdo = $db->getPdo();

$message = '';
$messageType = 'info';

// Handle bulk merge
if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['merge_all'])) {
    checkCsrf();

    $mergeCount = 0;
    $resultsMoved = 0;
    $errors = 0;

    // Step 1: Merge by UCI-ID (most reliable)
    $uciDuplicates = $pdo->query("
        SELECT REPLACE(REPLACE(license_number, ' ', ''), '-', '') as uci_normalized,
               GROUP_CONCAT(id ORDER BY id) as ids,
               COUNT(*) as cnt
        FROM riders
        WHERE license_number IS NOT NULL
          AND license_number != ''
          AND LENGTH(REPLACE(REPLACE(license_number, ' ', ''), '-', '')) >= 8
        GROUP BY uci_normalized
        HAVING cnt > 1
    ")->fetchAll(PDO::FETCH_ASSOC);

    foreach ($uciDuplicates as $dup) {
        $ids = explode(',', $dup['ids']);
        if (count($ids) < 2) continue;

        // Get rider details to pick the best one
        $riders = [];
        foreach ($ids as $id) {
            $r = $db->getRow("
                SELECT r.*, (SELECT COUNT(*) FROM results WHERE cyclist_id = r.id) as result_count
                FROM riders r WHERE r.id = ?
            ", [(int)$id]);
            if ($r) {
                // Score: results + completeness
                $r['score'] = $r['result_count'] * 10;
                if (!empty($r['birth_year'])) $r['score'] += 5;
                if (!empty($r['email'])) $r['score'] += 5;
                if (!empty($r['club_id'])) $r['score'] += 5;
                $riders[] = $r;
            }
        }

        if (count($riders) < 2) continue;

        // Sort by score desc
        usort($riders, fn($a, $b) => $b['score'] - $a['score']);

        $keep = array_shift($riders);
        $keepId = $keep['id'];

        foreach ($riders as $remove) {
            try {
                $pdo->beginTransaction();

                // Move results
                $stmt = $pdo->prepare("UPDATE results SET cyclist_id = ? WHERE cyclist_id = ?");
                $stmt->execute([$keepId, $remove['id']]);
                $resultsMoved += $stmt->rowCount();

                // Move series_results
                $pdo->prepare("UPDATE series_results SET cyclist_id = ? WHERE cyclist_id = ?")->execute([$keepId, $remove['id']]);

                // Copy missing data
                $updates = [];
                if (empty($keep['birth_year']) && !empty($remove['birth_year'])) $updates['birth_year'] = $remove['birth_year'];
                if (empty($keep['email']) && !empty($remove['email'])) $updates['email'] = $remove['email'];
                if (empty($keep['club_id']) && !empty($remove['club_id'])) $updates['club_id'] = $remove['club_id'];
                if (!empty($updates)) {
                    $db->update('riders', $updates, 'id = ?', [$keepId]);
                }

                // Delete duplicate
                $pdo->prepare("DELETE FROM riders WHERE id = ?")->execute([$remove['id']]);

                $pdo->commit();
                $mergeCount++;
            } catch (Exception $e) {
                $pdo->rollBack();
                $errors++;
            }
        }
    }

    // Step 2: Merge by exact name (case-insensitive using UPPER)
    $nameDuplicates = $pdo->query("
        SELECT UPPER(firstname) as fn, UPPER(lastname) as ln,
               GROUP_CONCAT(id ORDER BY id) as ids,
               COUNT(*) as cnt
        FROM riders
        WHERE firstname IS NOT NULL AND firstname != ''
          AND lastname IS NOT NULL AND lastname != ''
        GROUP BY UPPER(firstname), UPPER(lastname)
        HAVING cnt > 1
    ")->fetchAll(PDO::FETCH_ASSOC);

    foreach ($nameDuplicates as $dup) {
        $ids = explode(',', $dup['ids']);
        if (count($ids) < 2) continue;

        // Get rider details
        $riders = [];
        foreach ($ids as $id) {
            $r = $db->getRow("
                SELECT r.*, (SELECT COUNT(*) FROM results WHERE cyclist_id = r.id) as result_count
                FROM riders r WHERE r.id = ?
            ", [(int)$id]);
            if ($r) {
                $r['score'] = $r['result_count'] * 10;
                $r['uci_digits'] = preg_replace('/[^0-9]/', '', $r['license_number'] ?? '');
                if (!empty($r['uci_digits']) && strlen($r['uci_digits']) >= 8) $r['score'] += 100;
                if (!empty($r['birth_year'])) $r['score'] += 5;
                if (!empty($r['email'])) $r['score'] += 5;
                if (!empty($r['club_id'])) $r['score'] += 5;
                $riders[] = $r;
            }
        }

        if (count($riders) < 2) continue;

        // Check for UCI conflicts - if different real UCIs, skip (different people)
        $ucis = array_filter(array_column($riders, 'uci_digits'), fn($u) => strlen($u) >= 8);
        $uniqueUcis = array_unique($ucis);
        if (count($uniqueUcis) > 1) {
            // Different UCI-IDs = different people with same name, skip
            continue;
        }

        // Sort by score desc
        usort($riders, fn($a, $b) => $b['score'] - $a['score']);

        $keep = array_shift($riders);
        $keepId = $keep['id'];

        foreach ($riders as $remove) {
            try {
                $pdo->beginTransaction();

                // Move results
                $stmt = $pdo->prepare("UPDATE results SET cyclist_id = ? WHERE cyclist_id = ?");
                $stmt->execute([$keepId, $remove['id']]);
                $resultsMoved += $stmt->rowCount();

                // Move series_results
                $pdo->prepare("UPDATE series_results SET cyclist_id = ? WHERE cyclist_id = ?")->execute([$keepId, $remove['id']]);

                // Copy missing data (including UCI if keep doesn't have one)
                $updates = [];
                if (empty($keep['birth_year']) && !empty($remove['birth_year'])) {
                    $updates['birth_year'] = $remove['birth_year'];
                    $keep['birth_year'] = $remove['birth_year'];
                }
                if (empty($keep['email']) && !empty($remove['email'])) {
                    $updates['email'] = $remove['email'];
                    $keep['email'] = $remove['email'];
                }
                if (empty($keep['club_id']) && !empty($remove['club_id'])) {
                    $updates['club_id'] = $remove['club_id'];
                    $keep['club_id'] = $remove['club_id'];
                }
                if (empty($keep['uci_digits']) && !empty($remove['uci_digits'])) {
                    $updates['license_number'] = $remove['license_number'];
                    $keep['license_number'] = $remove['license_number'];
                }
                if (!empty($updates)) {
                    $db->update('riders', $updates, 'id = ?', [$keepId]);
                }

                // Delete duplicate
                $pdo->prepare("DELETE FROM riders WHERE id = ?")->execute([$remove['id']]);

                $pdo->commit();
                $mergeCount++;
            } catch (Exception $e) {
                $pdo->rollBack();
                $errors++;
            }
        }
    }

    $message = "Klart! Slog ihop {$mergeCount} dubletter, flyttade {$resultsMoved} resultat.";
    if ($errors > 0) {
        $message .= " ({$errors} fel)";
        $messageType = 'warning';
    } else {
        $messageType = 'success';
    }
}

// Count current duplicates
$uciDupCount = $pdo->query("
    SELECT COUNT(*) as cnt FROM (
        SELECT REPLACE(REPLACE(license_number, ' ', ''), '-', '') as uci
        FROM riders
        WHERE license_number IS NOT NULL AND license_number != ''
          AND LENGTH(REPLACE(REPLACE(license_number, ' ', ''), '-', '')) >= 8
        GROUP BY uci
        HAVING COUNT(*) > 1
    ) t
")->fetch()['cnt'] ?? 0;

$nameDupCount = $pdo->query("
    SELECT COUNT(*) as cnt FROM (
        SELECT UPPER(firstname), UPPER(lastname)
        FROM riders
        WHERE firstname IS NOT NULL AND firstname != ''
          AND lastname IS NOT NULL AND lastname != ''
        GROUP BY UPPER(firstname), UPPER(lastname)
        HAVING COUNT(*) > 1
    ) t
")->fetch()['cnt'] ?? 0;

// Get total extra riders (duplicates that would be removed)
$totalUciExtra = $pdo->query("
    SELECT SUM(cnt - 1) as total FROM (
        SELECT COUNT(*) as cnt
        FROM riders
        WHERE license_number IS NOT NULL AND license_number != ''
          AND LENGTH(REPLACE(REPLACE(license_number, ' ', ''), '-', '')) >= 8
        GROUP BY REPLACE(REPLACE(license_number, ' ', ''), '-', '')
        HAVING cnt > 1
    ) t
")->fetch()['total'] ?? 0;

$totalNameExtra = $pdo->query("
    SELECT SUM(cnt - 1) as total FROM (
        SELECT COUNT(*) as cnt
        FROM riders
        WHERE firstname IS NOT NULL AND firstname != ''
          AND lastname IS NOT NULL AND lastname != ''
        GROUP BY UPPER(firstname), UPPER(lastname)
        HAVING cnt > 1
    ) t
")->fetch()['total'] ?? 0;

// Sample duplicates for preview - but filter to only show REAL duplicates
// Same license + different names = license CONFLICT (data error), not a duplicate
$rawUciDups = $pdo->query("
    SELECT REPLACE(REPLACE(license_number, ' ', ''), '-', '') as uci,
           GROUP_CONCAT(CONCAT(firstname, ' ', lastname) ORDER BY id SEPARATOR ' | ') as names,
           GROUP_CONCAT(UPPER(firstname) ORDER BY id SEPARATOR '|') as firstnames,
           GROUP_CONCAT(UPPER(lastname) ORDER BY id SEPARATOR '|') as lastnames,
           GROUP_CONCAT(id ORDER BY id) as ids,
           COUNT(*) as cnt
    FROM riders
    WHERE license_number IS NOT NULL AND license_number != ''
      AND LENGTH(REPLACE(REPLACE(license_number, ' ', ''), '-', '')) >= 8
    GROUP BY uci
    HAVING cnt > 1
    ORDER BY cnt DESC
    LIMIT 50
")->fetchAll(PDO::FETCH_ASSOC);

// Filter: Only show as duplicates if names are the same (or very similar)
// Different names with same license = data conflict, not a duplicate to merge
$sampleUci = [];
$licenseConflicts = [];
foreach ($rawUciDups as $dup) {
    $firstnames = explode('|', $dup['firstnames']);
    $lastnames = explode('|', $dup['lastnames']);

    // Check if all names are the same (case-insensitive)
    $uniqueFirstnames = array_unique($firstnames);
    $uniqueLastnames = array_unique($lastnames);

    if (count($uniqueFirstnames) === 1 && count($uniqueLastnames) === 1) {
        // All names identical = real duplicate
        $sampleUci[] = $dup;
    } else {
        // Different names with same license = conflict
        $licenseConflicts[] = $dup;
    }

    if (count($sampleUci) >= 20) break;
}

// Get name duplicates - but filter to only show MERGEABLE ones
// Include birth_year and club_id to determine if they're really the same person
$rawNameDups = $pdo->query("
    SELECT UPPER(firstname) as fn, UPPER(lastname) as ln,
           GROUP_CONCAT(CONCAT(firstname, ' ', lastname) ORDER BY id SEPARATOR ' | ') as names,
           GROUP_CONCAT(id ORDER BY id) as ids,
           GROUP_CONCAT(COALESCE(REPLACE(REPLACE(license_number, ' ', ''), '-', ''), '') ORDER BY id SEPARATOR '|') as uci_list,
           GROUP_CONCAT(COALESCE(license_number, '-') ORDER BY id SEPARATOR ' | ') as ucis,
           GROUP_CONCAT(COALESCE(birth_year, 0) ORDER BY id SEPARATOR '|') as birth_years,
           GROUP_CONCAT(COALESCE(club_id, 0) ORDER BY id SEPARATOR '|') as club_ids,
           COUNT(*) as cnt
    FROM riders
    WHERE firstname IS NOT NULL AND firstname != ''
      AND lastname IS NOT NULL AND lastname != ''
    GROUP BY UPPER(firstname), UPPER(lastname)
    HAVING cnt > 1
    ORDER BY cnt DESC
    LIMIT 300
")->fetchAll(PDO::FETCH_ASSOC);

// Filter to only show LIKELY duplicates
// Different UCI IDs = different people
// Different birth years AND different clubs = different people (common name)
$sampleName = [];
foreach ($rawNameDups as $dup) {
    $uciValues = explode('|', $dup['uci_list']);
    $birthYears = array_map('intval', explode('|', $dup['birth_years']));
    $clubIds = array_map('intval', explode('|', $dup['club_ids']));

    // Get only valid UCI IDs (10+ digits)
    $validUcis = array_filter($uciValues, function($u) {
        $digits = preg_replace('/[^0-9]/', '', $u);
        return strlen($digits) >= 10;
    });
    $normalizedUcis = array_map(fn($u) => preg_replace('/[^0-9]/', '', $u), $validUcis);
    $uniqueUcis = array_unique($normalizedUcis);

    // SKIP if multiple different valid UCI IDs (definitely different people)
    if (count($uniqueUcis) > 1) {
        continue;
    }

    // Check birth years and clubs
    $validBirthYears = array_filter($birthYears, fn($y) => $y > 1900);
    $uniqueBirthYears = array_unique($validBirthYears);
    $validClubIds = array_filter($clubIds, fn($c) => $c > 0);
    $uniqueClubIds = array_unique($validClubIds);

    // SKIP if different birth years AND different clubs (common name, different people)
    // Example: "Fredrik Nilsson" born 1991 in Club A vs born 1997 in Club B = different people
    if (count($uniqueBirthYears) > 1 && count($uniqueClubIds) > 1) {
        // Check if any pair shares a club - if so, might still be duplicate
        $sharesSomething = false;
        for ($i = 0; $i < count($birthYears); $i++) {
            for ($j = $i + 1; $j < count($birthYears); $j++) {
                // Same club OR one has no birth year OR one has no club
                if ($clubIds[$i] === $clubIds[$j] && $clubIds[$i] > 0) {
                    $sharesSomething = true;
                    break 2;
                }
                if ($birthYears[$i] === 0 || $birthYears[$j] === 0) {
                    $sharesSomething = true;
                    break 2;
                }
                if ($clubIds[$i] === 0 || $clubIds[$j] === 0) {
                    $sharesSomething = true;
                    break 2;
                }
            }
        }
        if (!$sharesSomething) {
            continue; // Skip - different people with common name
        }
    }

    $sampleName[] = $dup;
    if (count($sampleName) >= 50) break;
}

// Also count non-mergeable (different UCIs = different people with same name)
$nonMergeableCount = count($rawNameDups) - count($sampleName);

// Find FUZZY duplicates - middle name variations and spelling differences
// Examples: "Lo Zetterlund" vs "Lo Nyberg Zetterlund", "Johanson" vs "Johansson"
$fuzzyDuplicates = [];

// Get all riders for fuzzy matching
$allRiders = $pdo->query("
    SELECT id, firstname, lastname, license_number,
           REPLACE(REPLACE(license_number, ' ', ''), '-', '') as uci_digits
    FROM riders
    WHERE firstname IS NOT NULL AND firstname != ''
      AND lastname IS NOT NULL AND lastname != ''
    ORDER BY lastname, firstname
")->fetchAll(PDO::FETCH_ASSOC);

// Build lookup by first part of firstname + lastname (for middle name matching)
$fuzzyGroups = [];
foreach ($allRiders as $rider) {
    $firstPart = explode(' ', trim($rider['firstname']))[0];
    $key = strtoupper($firstPart) . '|' . strtoupper(trim($rider['lastname']));
    if (!isset($fuzzyGroups[$key])) {
        $fuzzyGroups[$key] = [];
    }
    $fuzzyGroups[$key][] = $rider;
}

// Find groups with different full names but same first-part + lastname
$middleNameDups = [];
foreach ($fuzzyGroups as $key => $riders) {
    if (count($riders) > 1) {
        // Check if they have different full firstnames (middle name variation)
        $uniqueFirstNames = array_unique(array_map(fn($r) => strtoupper(trim($r['firstname'])), $riders));
        if (count($uniqueFirstNames) > 1) {
            // Check UCI conflicts
            $validUcis = array_filter(array_map(fn($r) => $r['uci_digits'], $riders), fn($u) => strlen($u) >= 8);
            $uniqueUcis = array_unique($validUcis);
            if (count($uniqueUcis) <= 1) {
                $middleNameDups[] = [
                    'key' => $key,
                    'riders' => $riders,
                    'names' => implode(' | ', array_map(fn($r) => $r['firstname'] . ' ' . $r['lastname'], $riders)),
                    'ids' => implode(', ', array_column($riders, 'id')),
                    'cnt' => count($riders)
                ];
            }
        }
    }
}

// Find spelling variations (Soundex/similar sounding names)
// Group by Soundex of firstname + lastname
$soundexGroups = [];

// Helper function to normalize Swedish characters for soundex
$normalizeName = function($name) {
    // Replace Swedish characters with ASCII equivalents
    $replacements = [
        'å' => 'a', 'ä' => 'a', 'ö' => 'o',
        'Å' => 'A', 'Ä' => 'A', 'Ö' => 'O',
        'é' => 'e', 'É' => 'E', 'è' => 'e', 'ë' => 'e',
        'ü' => 'u', 'Ü' => 'U'
    ];
    $name = strtr($name, $replacements);
    // Use transliterator if available, otherwise just return the replaced string
    if (function_exists('transliterator_transliterate')) {
        return transliterator_transliterate('Any-Latin; Latin-ASCII', $name);
    }
    return $name;
};

foreach ($allRiders as $rider) {
    // Create soundex key for firstname + lastname
    $firstSoundex = soundex($normalizeName($rider['firstname']));
    $lastSoundex = soundex($normalizeName($rider['lastname']));
    $key = $firstSoundex . '|' . $lastSoundex;
    if (!isset($soundexGroups[$key])) {
        $soundexGroups[$key] = [];
    }
    $soundexGroups[$key][] = $rider;
}

// Find soundex groups with different actual names - but require names to be ACTUALLY similar
// Soundex is too aggressive: "Andersson" and "Andreasson" have same soundex but are different names
$spellingDups = [];
foreach ($soundexGroups as $key => $riders) {
    if (count($riders) > 1) {
        // Check if they have different actual names
        $uniqueNames = array_unique(array_map(fn($r) => strtoupper($r['firstname'] . ' ' . $r['lastname']), $riders));
        if (count($uniqueNames) > 1) {
            // Check UCI conflicts - different UCIs = different people
            $validUcis = array_filter(array_map(fn($r) => $r['uci_digits'], $riders), fn($u) => strlen($u) >= 8);
            $uniqueUcis = array_unique($validUcis);
            if (count($uniqueUcis) > 1) {
                continue; // Different UCI IDs = definitely different people
            }

            // Additional check: lastnames must be very similar (Levenshtein distance <= 2)
            // This prevents "Andersson" vs "Andreasson" false positives
            $lastnames = array_map(fn($r) => strtoupper(trim($r['lastname'])), $riders);
            $uniqueLastnames = array_unique($lastnames);
            if (count($uniqueLastnames) > 1) {
                // Check if lastnames are actually similar
                $lastnamesSimilar = true;
                $firstLastname = $lastnames[0];
                foreach ($lastnames as $ln) {
                    if (levenshtein($firstLastname, $ln) > 2) {
                        $lastnamesSimilar = false;
                        break;
                    }
                }
                if (!$lastnamesSimilar) {
                    continue; // Lastnames too different
                }
            }

            $spellingDups[] = [
                'soundex' => $key,
                'riders' => $riders,
                'names' => implode(' | ', array_map(fn($r) => $r['firstname'] . ' ' . $r['lastname'], $riders)),
                'ids' => implode(', ', array_column($riders, 'id')),
                'cnt' => count($riders)
            ];
        }
    }
}

$page_title = 'Bulk-sammanslagning av dubletter';
$breadcrumbs = [
    ['label' => 'Verktyg', 'url' => '/admin/tools'],
    ['label' => 'Bulk-sammanslagning']
];
include __DIR__ . '/components/unified-layout.php';
?>

<h1 class="text-primary mb-lg">
    <i data-lucide="git-merge"></i> Bulk-sammanslagning av dubletter
</h1>

<?php if ($message): ?>
<div class="alert alert-<?= $messageType ?> mb-lg">
    <?= h($message) ?>
</div>
<?php endif; ?>

<div class="alert alert-warning mb-lg">
    <i data-lucide="alert-triangle"></i>
    <strong>OBS!</strong> Detta verktyg slår ihop ALLA hittade dubletter automatiskt.
    Den bästa profilen (flest resultat + mest data) behålls.
    Par med olika UCI-ID hoppas över (antas vara olika personer med samma namn).
</div>

<!-- Stats -->
<div class="grid grid-cols-2 md-grid-cols-4 gap-md mb-lg">
    <div class="stat-card">
        <div class="stat-number text-danger"><?= $uciDupCount ?></div>
        <div class="stat-label">UCI-dubbletter</div>
        <div class="text-xs text-muted"><?= $totalUciExtra ?> extra poster</div>
    </div>
    <div class="stat-card">
        <div class="stat-number text-warning"><?= count($sampleName) ?></div>
        <div class="stat-label">Namn-dubbletter</div>
        <div class="text-xs text-muted">(<?= $nonMergeableCount ?> med olika UCI hoppas över)</div>
    </div>
    <div class="stat-card">
        <div class="stat-number text-info"><?= count($middleNameDups) ?></div>
        <div class="stat-label">Mellannamn</div>
        <div class="text-xs text-muted">Manuell granskning</div>
    </div>
    <div class="stat-card">
        <div class="stat-number text-secondary"><?= count($spellingDups) ?></div>
        <div class="stat-label">Stavning</div>
        <div class="text-xs text-muted">Manuell granskning</div>
    </div>
</div>

<div class="mb-lg">
    <form method="POST" class="d-inline">
        <?= csrf_field() ?>
        <button type="submit" name="merge_all" class="btn btn-danger"
                onclick="return confirm('Slå ihop ALLA exakta dubletter?\n\n<?= $totalUciExtra + $totalNameExtra ?> poster kommer att tas bort.\nResultat flyttas till den bästa profilen.\n\nOBS: Mellannamn och stavningsvariationer måste granskas manuellt.')">
            <i data-lucide="git-merge"></i>
            Slå ihop exakta dubletter (<?= $totalUciExtra + $totalNameExtra ?> st)
        </button>
    </form>
</div>

<!-- UCI Duplicates (same license + same name = real duplicates) -->
<div class="card mb-lg">
    <div class="card-header">
        <h3><i data-lucide="fingerprint"></i> UCI-dubletter (<?= count($sampleUci) ?> grupper)</h3>
    </div>
    <div class="card-body gs-padding-0">
        <?php if (!empty($licenseConflicts)): ?>
        <div class="alert alert-warning m-md">
            <i data-lucide="alert-triangle"></i>
            <strong><?= count($licenseConflicts) ?> licenskonflikter hoppas över</strong> - samma licens-ID men olika namn (datafel, ej dubletter).
        </div>
        <?php endif; ?>
        <?php if (empty($sampleUci)): ?>
        <div class="alert alert-success m-md">Inga UCI-dubletter!</div>
        <?php else: ?>
        <div class="table-responsive">
            <table class="table table-sm">
                <thead>
                    <tr>
                        <th>UCI-ID</th>
                        <th>Namn</th>
                        <th>IDs</th>
                        <th>Antal</th>
                    </tr>
                </thead>
                <tbody>
                    <?php foreach ($sampleUci as $dup): ?>
                    <tr>
                        <td><code><?= h($dup['uci']) ?></code></td>
                        <td><?= h($dup['names']) ?></td>
                        <td><code><?= h($dup['ids']) ?></code></td>
                        <td><span class="badge badge-danger"><?= $dup['cnt'] ?></span></td>
                    </tr>
                    <?php endforeach; ?>
                </tbody>
            </table>
        </div>
        <?php endif; ?>
    </div>
</div>

<?php if (!empty($licenseConflicts)): ?>
<!-- License Conflicts (same license but different names = data error) -->
<div class="card mb-lg">
    <div class="card-header" style="background: var(--color-warning); color: #000;">
        <h3><i data-lucide="alert-triangle"></i> Licenskonflikter (<?= count($licenseConflicts) ?>) - INTE dubletter!</h3>
    </div>
    <div class="card-body gs-padding-0">
        <div class="alert alert-warning m-md">
            <i data-lucide="info"></i>
            Dessa har samma licens-ID men <strong>olika namn</strong>. Det är ett datafel - två olika personer har fått samma ID.
            <strong>Slå INTE ihop dessa!</strong> Fixa istället licens-ID:t på en av dem.
        </div>
        <div class="table-responsive">
            <table class="table table-sm">
                <thead>
                    <tr>
                        <th>Licens-ID</th>
                        <th>Namn (olika!)</th>
                        <th>IDs</th>
                    </tr>
                </thead>
                <tbody>
                    <?php foreach ($licenseConflicts as $conflict): ?>
                    <tr>
                        <td><code><?= h($conflict['uci']) ?></code></td>
                        <td style="color: var(--color-danger);"><?= h($conflict['names']) ?></td>
                        <td><code><?= h($conflict['ids']) ?></code></td>
                    </tr>
                    <?php endforeach; ?>
                </tbody>
            </table>
        </div>
    </div>
</div>
<?php endif; ?>

<!-- Name Duplicates -->
<div class="card mb-lg">
    <div class="card-header">
        <h3><i data-lucide="users"></i> Namn-dubletter som kan slås samman (<?= count($sampleName) ?> grupper)</h3>
    </div>
    <div class="card-body gs-padding-0">
        <?php if ($nonMergeableCount > 0): ?>
        <div class="alert alert-info m-md">
            <i data-lucide="info"></i>
            <strong><?= $nonMergeableCount ?> grupper hoppas över</strong> - personer med samma namn men olika UCI-ID (olika personer).
        </div>
        <?php endif; ?>
        <?php if (empty($sampleName)): ?>
        <div class="alert alert-success m-md">Inga namn-dubletter som kan slås samman!</div>
        <?php else: ?>
        <div class="table-responsive">
            <table class="table table-sm">
                <thead>
                    <tr>
                        <th>Namn</th>
                        <th>UCI-IDs</th>
                        <th>IDs</th>
                        <th>Antal</th>
                    </tr>
                </thead>
                <tbody>
                    <?php foreach ($sampleName as $dup): ?>
                    <tr>
                        <td><strong><?= h($dup['fn'] . ' ' . $dup['ln']) ?></strong></td>
                        <td><code class="text-xs"><?= h($dup['ucis']) ?></code></td>
                        <td><code><?= h($dup['ids']) ?></code></td>
                        <td><span class="badge badge-warning"><?= $dup['cnt'] ?></span></td>
                    </tr>
                    <?php endforeach; ?>
                </tbody>
            </table>
        </div>
        <?php endif; ?>
    </div>
</div>

<!-- Middle Name Duplicates (fuzzy) -->
<div class="card mb-lg">
    <div class="card-header">
        <h3><i data-lucide="user-plus"></i> Mellannamn-variationer (<?= count($middleNameDups) ?> grupper)</h3>
    </div>
    <div class="card-body gs-padding-0">
        <div class="alert alert-info m-md">
            <i data-lucide="info"></i>
            Dessa har samma första förnamn och efternamn, men olika mellannamn.
            Exempel: "Lo Zetterlund" vs "Lo Nyberg Zetterlund"
        </div>
        <?php if (empty($middleNameDups)): ?>
        <div class="alert alert-success m-md">Inga mellannamn-variationer hittade!</div>
        <?php else: ?>
        <div class="table-responsive">
            <table class="table table-sm">
                <thead>
                    <tr>
                        <th>Namn-variationer</th>
                        <th>IDs</th>
                        <th>Antal</th>
                        <th></th>
                    </tr>
                </thead>
                <tbody>
                    <?php foreach (array_slice($middleNameDups, 0, 30) as $dup): ?>
                    <tr>
                        <td><?= h($dup['names']) ?></td>
                        <td><code><?= h($dup['ids']) ?></code></td>
                        <td><span class="badge badge-info"><?= $dup['cnt'] ?></span></td>
                        <td>
                            <a href="/admin/rider-merge.php?ids=<?= urlencode($dup['ids']) ?>" class="btn btn-sm btn-secondary">
                                <i data-lucide="git-merge"></i> Granska
                            </a>
                        </td>
                    </tr>
                    <?php endforeach; ?>
                    <?php if (count($middleNameDups) > 30): ?>
                    <tr>
                        <td colspan="4" class="text-center text-muted">
                            ... och <?= count($middleNameDups) - 30 ?> till
                        </td>
                    </tr>
                    <?php endif; ?>
                </tbody>
            </table>
        </div>
        <?php endif; ?>
    </div>
</div>

<!-- Spelling Variations (Soundex) -->
<div class="card mb-lg">
    <div class="card-header">
        <h3><i data-lucide="spell-check"></i> Stavnings-variationer (<?= count($spellingDups) ?> grupper)</h3>
    </div>
    <div class="card-body gs-padding-0">
        <div class="alert alert-warning m-md">
            <i data-lucide="alert-triangle"></i>
            Dessa har liknande uttal men olika stavning.
            Exempel: "Johanson" vs "Johansson", "Erikson" vs "Eriksson"
            <strong>Granska noga innan sammanslagning!</strong>
        </div>
        <?php if (empty($spellingDups)): ?>
        <div class="alert alert-success m-md">Inga stavnings-variationer hittade!</div>
        <?php else: ?>
        <div class="table-responsive">
            <table class="table table-sm">
                <thead>
                    <tr>
                        <th>Namn-variationer</th>
                        <th>IDs</th>
                        <th>Antal</th>
                        <th></th>
                    </tr>
                </thead>
                <tbody>
                    <?php foreach (array_slice($spellingDups, 0, 30) as $dup): ?>
                    <tr>
                        <td><?= h($dup['names']) ?></td>
                        <td><code><?= h($dup['ids']) ?></code></td>
                        <td><span class="badge badge-warning"><?= $dup['cnt'] ?></span></td>
                        <td>
                            <a href="/admin/rider-merge.php?ids=<?= urlencode($dup['ids']) ?>" class="btn btn-sm btn-secondary">
                                <i data-lucide="git-merge"></i> Granska
                            </a>
                        </td>
                    </tr>
                    <?php endforeach; ?>
                    <?php if (count($spellingDups) > 30): ?>
                    <tr>
                        <td colspan="4" class="text-center text-muted">
                            ... och <?= count($spellingDups) - 30 ?> till
                        </td>
                    </tr>
                    <?php endif; ?>
                </tbody>
            </table>
        </div>
        <?php endif; ?>
    </div>
</div>

</div>
<?php include __DIR__ . '/components/unified-layout-footer.php'; ?>
