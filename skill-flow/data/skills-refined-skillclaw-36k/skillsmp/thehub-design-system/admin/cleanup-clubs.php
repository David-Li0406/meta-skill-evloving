<?php
/**
 * Club Duplicate Cleanup Tool
 * Find and merge duplicate clubs created during import
 * Version: v1.1.0 [2025-12-13]
 */
require_once __DIR__ . '/../config.php';
require_admin();

$db = getDB();
$message = '';
$messageType = '';

// File to store ignored duplicate groups
$ignoredFile = __DIR__ . '/../uploads/ignored_club_duplicates.json';

// Load ignored duplicates
function loadIgnoredDuplicates($file) {
    if (file_exists($file)) {
        $data = json_decode(file_get_contents($file), true);
        return is_array($data) ? $data : [];
    }
    return [];
}

// Save ignored duplicates
function saveIgnoredDuplicates($file, $data) {
    $dir = dirname($file);
    if (!is_dir($dir)) {
        mkdir($dir, 0755, true);
    }
    file_put_contents($file, json_encode($data, JSON_PRETTY_PRINT));
}

$ignoredDuplicates = loadIgnoredDuplicates($ignoredFile);

// Handle ignore action
if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['ignore_group'])) {
    checkCsrf();
    $groupKey = $_POST['ignore_group'];
    if (!in_array($groupKey, $ignoredDuplicates)) {
        $ignoredDuplicates[] = $groupKey;
        saveIgnoredDuplicates($ignoredFile, $ignoredDuplicates);
        $message = 'Gruppen markerad som "inte dubbletter" och kommer inte visas igen';
        $messageType = 'success';
    }
}

// Handle un-ignore (reset) action
if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['reset_ignored'])) {
    checkCsrf();
    $ignoredDuplicates = [];
    saveIgnoredDuplicates($ignoredFile, $ignoredDuplicates);
    $message = 'Alla ignorerade grupper återställda';
    $messageType = 'info';
}

// Handle merge action
if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['merge'])) {
 checkCsrf();

 $keepId = (int)$_POST['keep_club'];
 $mergeIds = array_map('intval', $_POST['merge_clubs'] ?? []);

 // Validation: Need both a target club and clubs to merge
 if (!$keepId) {
  $message = 'Välj en klubb att behålla (radioknapp)';
  $messageType = 'error';
 } elseif (empty($mergeIds)) {
  $message = 'Välj minst en klubb att slå samman (kryssruta). Kryssa i klubbarna som ska tas bort.';
  $messageType = 'error';
 } elseif ($keepId && !empty($mergeIds)) {
 try {
  $movedCount = 0;
  $deletedCount = 0;
  $rfProtectedCount = 0;

  // Move all riders from each merge club to keep club
  foreach ($mergeIds as $mergeId) {
  // Check if club is RF-registered (cannot be deleted)
  $club = $db->getRow("SELECT rf_registered FROM clubs WHERE id = ?", [$mergeId]);
  if ($club && !empty($club['rf_registered'])) {
   $rfProtectedCount++;
   continue;
  }

  // Count riders to move
  $count = $db->getRow("SELECT COUNT(*) as cnt FROM riders WHERE club_id = ?", [$mergeId])['cnt'] ?? 0;
  $movedCount += $count;

  // Update riders
  if ($count > 0) {
   $db->update('riders', ['club_id' => $keepId], 'club_id = ?', [$mergeId]);
  }

  // Delete the empty club
  $db->delete('clubs', 'id = ?', [$mergeId]);
  $deletedCount++;
  }

  $messageParts = [];
  if ($movedCount > 0) $messageParts[] = "flyttade $movedCount deltagare";
  if ($deletedCount > 0) $messageParts[] = "tog bort $deletedCount dubblettklubbar";
  if ($rfProtectedCount > 0) $messageParts[] = "skyddade $rfProtectedCount RF-registrerade klubbar";

  $message = ucfirst(implode(' och ', $messageParts));
  $messageType = $rfProtectedCount > 0 ? 'warning' : 'success';
 } catch (Exception $e) {
  $message = 'Fel vid sammanslagning: ' . $e->getMessage();
  $messageType = 'error';
 }
 }
}

// Handle single delete action
if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['delete_club'])) {
 checkCsrf();

 $deleteId = (int)$_POST['delete_club'];

 // Check if club is RF-registered
 $club = $db->getRow("SELECT name, rf_registered FROM clubs WHERE id = ?", [$deleteId]);
 if ($club && !empty($club['rf_registered'])) {
  $message = "Kan inte ta bort RF-registrerad klubb: " . ($club['name'] ?? '');
  $messageType = 'error';
 } else {
  // Check if club has riders
  $riderCount = $db->getRow("SELECT COUNT(*) as cnt FROM riders WHERE club_id = ?", [$deleteId])['cnt'] ?? 0;

  if ($riderCount == 0) {
   try {
    $db->delete('clubs', 'id = ?', [$deleteId]);
    $message = 'Klubb borttagen';
    $messageType = 'success';
   } catch (Exception $e) {
    $message = 'Fel vid borttagning: ' . $e->getMessage();
    $messageType = 'error';
   }
  } else {
   $message ="Kan inte ta bort klubb med $riderCount deltagare";
   $messageType = 'error';
  }
 }
}

// Handle delete all empty clubs action
if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['delete_all_empty'])) {
 checkCsrf();

 $clubIds = array_map('intval', $_POST['merge_clubs'] ?? []);
 $deletedCount = 0;
 $skippedCount = 0;
 $rfProtectedCount = 0;

 if (!empty($clubIds)) {
 try {
  foreach ($clubIds as $clubId) {
  // Check if club is RF-registered
  $club = $db->getRow("SELECT rf_registered FROM clubs WHERE id = ?", [$clubId]);
  if ($club && !empty($club['rf_registered'])) {
   $rfProtectedCount++;
   continue;
  }

  // Verify club is actually empty
  $riderCount = $db->getRow("SELECT COUNT(*) as cnt FROM riders WHERE club_id = ?", [$clubId])['cnt'] ?? 0;

  if ($riderCount == 0) {
   $db->delete('clubs', 'id = ?', [$clubId]);
   $deletedCount++;
  } else {
   $skippedCount++;
  }
  }

  $messageParts = [];
  if ($deletedCount > 0) $messageParts[] = "tog bort $deletedCount tomma klubbar";
  if ($skippedCount > 0) $messageParts[] = "hoppade över $skippedCount klubbar med deltagare";
  if ($rfProtectedCount > 0) $messageParts[] = "skyddade $rfProtectedCount RF-registrerade klubbar";

  $message = ucfirst(implode(', ', $messageParts));
  $messageType = ($skippedCount > 0 || $rfProtectedCount > 0) ? 'warning' : 'success';
 } catch (Exception $e) {
  $message = 'Fel vid borttagning: ' . $e->getMessage();
  $messageType = 'error';
 }
 }
}

// Get all clubs with rider counts
$clubs = $db->getAll("
 SELECT c.id, c.name, c.short_name, c.city, c.region, c.country,
  c.rf_registered, c.scf_district,
  COUNT(r.id) as rider_count
 FROM clubs c
 LEFT JOIN riders r ON c.id = r.club_id
 GROUP BY c.id
 ORDER BY c.name
");

// Group clubs by normalized name to find potential duplicates
$clubGroups = [];
foreach ($clubs as $club) {
 $normalized = normalizeClubName($club['name']);

 if (!isset($clubGroups[$normalized])) {
 $clubGroups[$normalized] = [];
 }
 $clubGroups[$normalized][] = $club;
}

// Also find fuzzy duplicates - clubs with similar normalized names
$normalizedNames = [];
foreach ($clubs as $club) {
    $normalized = normalizeClubName($club['name']);
    $normalizedNames[$club['id']] = $normalized;
}

// Check for fuzzy matches using Levenshtein distance
$fuzzyPairs = [];
$clubIds = array_keys($normalizedNames);
$numClubs = count($clubIds);

for ($i = 0; $i < $numClubs - 1; $i++) {
    for ($j = $i + 1; $j < $numClubs; $j++) {
        $id1 = $clubIds[$i];
        $id2 = $clubIds[$j];
        $name1 = $normalizedNames[$id1];
        $name2 = $normalizedNames[$id2];

        // Skip if already exact match (handled above)
        if ($name1 === $name2) continue;

        // Skip very short names
        if (strlen($name1) < 3 || strlen($name2) < 3) continue;

        // Check if one contains the other (e.g., "naten" in "natensater")
        $containsMatch = false;
        if (strlen($name1) >= 4 && strlen($name2) >= 4) {
            if (strpos($name2, $name1) === 0 || strpos($name1, $name2) === 0) {
                $containsMatch = true;
            }
        }

        // Calculate Levenshtein distance
        $maxLen = max(strlen($name1), strlen($name2));
        $distance = levenshtein(substr($name1, 0, 50), substr($name2, 0, 50));
        $similarity = round((1 - $distance / $maxLen) * 100);

        // Match if: contains match OR high similarity (>75%)
        if ($containsMatch || $similarity >= 75) {
            $key = min($name1, $name2) . '|' . max($name1, $name2);
            if (!isset($fuzzyPairs[$key])) {
                $fuzzyPairs[$key] = [];
            }
            // Find the club objects
            foreach ($clubs as $club) {
                if ($club['id'] == $id1 || $club['id'] == $id2) {
                    $fuzzyPairs[$key][$club['id']] = $club;
                }
            }
        }
    }
}

// Add fuzzy pairs to club groups with special key
foreach ($fuzzyPairs as $key => $pair) {
    if (count($pair) >= 2) {
        $groupKey = 'fuzzy_' . $key;
        if (!isset($clubGroups[$groupKey])) {
            $clubGroups[$groupKey] = array_values($pair);
        }
    }
}

// Filter to only show groups with potential duplicates (2+ clubs) and not ignored
$duplicateGroups = array_filter($clubGroups, function($group, $key) use ($ignoredDuplicates) {
 return count($group) >= 2 && !in_array($key, $ignoredDuplicates);
}, ARRAY_FILTER_USE_BOTH);

// Count ignored groups for display
$ignoredCount = count($ignoredDuplicates);

// Sort groups by total rider count (most important first)
uasort($duplicateGroups, function($a, $b) {
 $totalA = array_sum(array_column($a, 'rider_count'));
 $totalB = array_sum(array_column($b, 'rider_count'));
 return $totalB - $totalA;
});

// Also find empty clubs (excluding RF-registered which are protected)
$emptyClubs = array_filter($clubs, function($club) {
 return $club['rider_count'] == 0 && empty($club['rf_registered']);
});

// RF-registered empty clubs (for info)
$rfEmptyClubs = array_filter($clubs, function($club) {
 return $club['rider_count'] == 0 && !empty($club['rf_registered']);
});

/**
 * Normalize club name for comparison
 * Handles variations like: CK Fix, Ck Fix, Cykelklubben Fix, Cykelklubb Fix
 */
function normalizeClubName($name) {
    $name = mb_strtolower(trim($name), 'UTF-8');

    // Remove common prefixes/suffixes (order matters - longer patterns first)
    $patterns = [
        '/^cykelklubben\s+/u',           // "Cykelklubben Fix" -> "fix"
        '/^cykelklubb\s+/u',             // "Cykelklubb Fix" -> "fix"
        '/^cykelföreningen\s+/u',        // "Cykelföreningen X" -> "x"
        '/^ck\s+/u',                     // "CK Fix" -> "fix"
        '/^if\s+/u',                     // "IF Ceres" -> "ceres"
        '/^ik\s+/u',                     // "IK X" -> "x"
        '/^sk\s+/u',                     // "SK X" -> "x"
        '/^fk\s+/u',                     // "FK X" -> "x"
        '/^bk\s+/u',                     // "BK X" -> "x"
        '/\s+ck$/u',                     // "Fix CK" -> "fix"
        '/\s+cykelklubb$/u',             // "Fix Cykelklubb" -> "fix"
        '/\s+cykelklubben$/u',           // "Fix Cykelklubben" -> "fix"
        '/\s+if$/u',                     // "Fix IF" -> "fix"
        '/\s+ik$/u',                     // "X IK" -> "X"
        '/\s+sk$/u',                     // "X SK" -> "X"
        '/\s+mtb$/u',                    // "Fix MTB" -> "fix"
        '/\s+enduro$/u',                 // "Fix Enduro" -> "fix"
        '/\s+idrottssällskap$/u',
        '/\s+idrottsällskap$/u',
        '/\s+idrottsförening$/u',
    ];

    foreach ($patterns as $pattern) {
        $name = preg_replace($pattern, '', $name);
    }

    // Replace Swedish chars for comparison
    $name = preg_replace('/[åä]/u', 'a', $name);
    $name = preg_replace('/[ö]/u', 'o', $name);
    $name = preg_replace('/[é]/u', 'e', $name);

    // Remove non-alphanumeric (keeps only letters and numbers)
    $name = preg_replace('/[^a-z0-9]/u', '', $name);

    // Remove trailing 's' to match singular/plural (e.g., "masters" vs "master")
    $name = preg_replace('/s$/u', '', $name);

    return $name;
}

// Page config for unified layout
$page_title = 'Rensa Klubbdubbletter';
$breadcrumbs = [
    ['label' => 'Verktyg', 'url' => '/admin/tools'],
    ['label' => 'Rensa Klubbdubbletter']
];
include __DIR__ . '/components/unified-layout.php';
?>


 

 <!-- Header -->
 <div class="flex justify-between items-center mb-lg">
  <div>
  <h1 class="">
   <i data-lucide="building-2"></i>
   Rensa Klubbdubbletter
  </h1>
  <p class="text-secondary">
   Hitta och slå samman dubblettklubbar skapade vid import
  </p>
  </div>
  <a href="/admin/clubs.php" class="btn btn--secondary">
  <i data-lucide="arrow-left"></i>
  Tillbaka
  </a>
 </div>

 <?php if ($message): ?>
  <div class="alert alert-<?= h($messageType) ?> mb-lg">
  <i data-lucide="<?= $messageType === 'success' ? 'check-circle' : 'alert-circle' ?>"></i>
  <?= h($message) ?>
  </div>
 <?php endif; ?>

 <!-- Stats -->
 <div class="grid grid-cols-2 gs-md-grid-cols-4 gap-md mb-lg">
  <div class="card">
  <div class="card-body text-center">
   <div class="text-2xl text-primary"><?= count($clubs) ?></div>
   <div class="text-sm text-secondary">Totalt klubbar</div>
  </div>
  </div>
  <div class="card">
  <div class="card-body text-center">
   <div class="text-2xl text-warning"><?= count($duplicateGroups) ?></div>
   <div class="text-sm text-secondary">Dubblettgrupper</div>
  </div>
  </div>
  <div class="card">
  <div class="card-body text-center">
   <div class="text-2xl text-error"><?= count($emptyClubs) ?></div>
   <div class="text-sm text-secondary">Tomma klubbar</div>
  </div>
  </div>
  <div class="card">
  <div class="card-body text-center">
   <div class="text-2xl text-success"><?= count($clubs) - count($emptyClubs) ?></div>
   <div class="text-sm text-secondary">Med deltagare</div>
  </div>
  </div>
 </div>

 <?php if (!empty($emptyClubs)): ?>
 <!-- Quick action: Delete all empty clubs -->
 <div class="card mb-lg" style="background: var(--color-error-light, #fee2e2);">
  <div class="card-body flex items-center justify-between">
   <div>
    <strong class="text-error"><i data-lucide="alert-triangle" class="icon-sm"></i> <?= count($emptyClubs) ?> tomma klubbar</strong>
    <p class="text-sm text-secondary gs-mb-0">Klubbar utan några deltagare kan tas bort</p>
   </div>
   <form method="POST">
    <?= csrf_field() ?>
    <?php foreach ($emptyClubs as $club): ?>
    <input type="hidden" name="merge_clubs[]" value="<?= $club['id'] ?>">
    <?php endforeach; ?>
    <input type="hidden" name="keep_club" value="0">
    <button type="submit" name="delete_all_empty" value="1"
     class="btn btn-danger"
     onclick="return confirm('Ta bort ALLA <?= count($emptyClubs) ?> tomma klubbar?')">
    <i data-lucide="trash-2"></i>
    Ta bort alla tomma klubbar
    </button>
   </form>
  </div>
 </div>
 <?php endif; ?>

 <?php if (!empty($rfEmptyClubs)): ?>
 <!-- Info about RF-protected empty clubs -->
 <div class="card mb-lg" style="background: var(--color-success-light, #d1fae5);">
  <div class="card-body flex items-center justify-between">
   <div>
    <strong class="text-success"><i data-lucide="shield-check" class="icon-sm"></i> <?= count($rfEmptyClubs) ?> RF-skyddade tomma klubbar</strong>
    <p class="text-sm text-secondary gs-mb-0">Dessa klubbar är RF-registrerade och kan inte raderas, även om de saknar deltagare</p>
   </div>
  </div>
 </div>
 <?php endif; ?>

 <?php if ($ignoredCount > 0): ?>
  <!-- Ignored groups info -->
  <div class="card mb-lg" style="background: var(--color-bg-sunken, #f5f5f5);">
   <div class="card-body flex items-center justify-between">
    <div>
     <strong class="text-secondary"><i data-lucide="eye-off" class="icon-sm"></i> <?= $ignoredCount ?> grupper dolda</strong>
     <p class="text-sm text-secondary gs-mb-0">Grupper markerade som "inte dubbletter"</p>
    </div>
    <form method="POST">
     <?= csrf_field() ?>
     <button type="submit" name="reset_ignored" value="1" class="btn btn--secondary btn--sm"
      onclick="return confirm('Återställa alla dolda grupper?')">
      <i data-lucide="refresh-cw"></i>
      Visa alla igen
     </button>
    </form>
   </div>
  </div>
 <?php endif; ?>

 <?php if (!empty($duplicateGroups)): ?>
  <!-- Duplicate Groups -->
  <div class="card mb-lg">
  <div class="card-header">
   <h2 class="">
   <i data-lucide="copy"></i>
   Potentiella dubbletter (<?= count($duplicateGroups) ?> grupper)
   </h2>
  </div>
  <div class="card-body">
   <?php foreach ($duplicateGroups as $normalized => $group): ?>
   <form method="POST" class="mb-lg gs-pb-lg border-b">
    <?= csrf_field() ?>

    <h4 class="mb-md">
    <?= h($group[0]['name']) ?>
    <span class="badge badge-secondary"><?= count($group) ?> varianter</span>
    </h4>

    <div class="table-responsive mb-md">
    <table class="table">
     <thead>
     <tr>
      <th>Behåll</th>
      <th>Slå samman</th>
      <th>Klubbnamn</th>
      <th>Kort</th>
      <th>Stad</th>
      <th>Deltagare</th>
     </tr>
     </thead>
     <tbody>
     <?php
     // Sort by rider count desc
     usort($group, function($a, $b) {
      return $b['rider_count'] - $a['rider_count'];
     });
     $first = true;
     foreach ($group as $club):
     ?>
      <tr class="<?= $club['rider_count'] == 0 && empty($club['rf_registered']) ? 'gs-bg-danger-light' : '' ?>">
      <td>
       <input type="radio" name="keep_club" value="<?= $club['id'] ?>"
        <?= $first ? 'checked' : '' ?>>
      </td>
      <td>
       <?php if (!$first): ?>
       <?php if (!empty($club['rf_registered'])): ?>
       <span class="text-muted" title="RF-registrerade klubbar kan inte raderas"><i data-lucide="shield-check" class="icon-sm text-success"></i></span>
       <?php else: ?>
       <input type="checkbox" name="merge_clubs[]" value="<?= $club['id'] ?>"
        <?= $club['rider_count'] == 0 ? 'checked' : '' ?>>
       <?php endif; ?>
       <?php else: ?>
       <span class="text-secondary">-</span>
       <?php endif; ?>
      </td>
      <td>
       <strong><?= h($club['name']) ?></strong>
       <?php if (!empty($club['rf_registered'])): ?>
       <span class="badge badge-success badge-sm" title="RF-registrerad <?= h($club['scf_district'] ?? '') ?>">RF</span>
       <?php endif; ?>
       <?php if ($club['rider_count'] > 0): ?>
       <span class="badge badge-success badge-sm">Huvudklubb</span>
       <?php endif; ?>
      </td>
      <td><?= h($club['short_name']) ?: '-' ?></td>
      <td><?= h($club['city']) ?: '-' ?></td>
      <td>
       <?php if ($club['rider_count'] > 0): ?>
       <strong class="text-success"><?= $club['rider_count'] ?></strong>
       <?php else: ?>
       <span class="text-error">0</span>
       <?php endif; ?>
      </td>
      </tr>
     <?php
     $first = false;
     endforeach;
     ?>
     </tbody>
    </table>
    </div>

    <p class="text-sm text-secondary mb-sm">
     <i data-lucide="info" class="icon-xs"></i>
     Välj "Behåll" (radioknapp) för klubben som ska finnas kvar, kryssa i "Slå samman" för de som ska tas bort.
    </p>
    <div class="flex gap-sm">
     <button type="submit" name="merge" value="1" class="btn btn-warning">
      <i data-lucide="merge"></i>
      Slå samman markerade till vald klubb
     </button>
     <button type="submit" name="ignore_group" value="<?= h($normalized) ?>" class="btn btn--secondary">
      <i data-lucide="eye-off"></i>
      Inte dubbletter
     </button>
    </div>
   </form>
   <?php endforeach; ?>
  </div>
  </div>
 <?php else: ?>
  <div class="card mb-lg">
  <div class="card-body text-center py-xl">
   <i data-lucide="check-circle" class="text-success" style="width: 48px; height: 48px;"></i>
   <p class="text-lg mt-md">Inga dubblettgrupper hittades!</p>
  </div>
  </div>
 <?php endif; ?>

 <?php if (!empty($emptyClubs)): ?>
  <!-- Empty Clubs -->
  <div class="card">
  <div class="card-header">
   <h2 class="">
   <i data-lucide="trash-2"></i>
   Tomma klubbar (<?= count($emptyClubs) ?>)
   </h2>
  </div>
  <div class="card-body">
   <div class="table-responsive">
   <table class="table">
    <thead>
    <tr>
     <th>Klubbnamn</th>
     <th>Kort</th>
     <th>Stad</th>
     <th>Åtgärd</th>
    </tr>
    </thead>
    <tbody>
    <?php foreach ($emptyClubs as $club): ?>
     <tr>
     <td><?= h($club['name']) ?></td>
     <td><?= h($club['short_name']) ?: '-' ?></td>
     <td><?= h($club['city']) ?: '-' ?></td>
     <td>
      <form method="POST" style="display: inline;">
      <?= csrf_field() ?>
      <button type="submit" name="delete_club" value="<?= $club['id'] ?>"
       class="btn btn--sm btn-danger"
       onclick="return confirm('Ta bort <?= h($club['name']) ?>?')">
       <i data-lucide="trash-2"></i>
       Ta bort
      </button>
      </form>
     </td>
     </tr>
    <?php endforeach; ?>
    </tbody>
   </table>
   </div>

   <!-- Button moved to top of page -->
  </div>
  </div>
 <?php endif; ?>

 <div class="gs-py-sm">
  <small class="text-secondary">Cleanup Clubs v1.2.0 [2025-12-15]</small>
 </div>

<?php include __DIR__ . '/components/unified-layout-footer.php'; ?>
