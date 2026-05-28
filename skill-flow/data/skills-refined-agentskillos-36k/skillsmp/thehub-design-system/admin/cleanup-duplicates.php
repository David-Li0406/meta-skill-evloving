<?php
/**
 * Admin tool to find and merge duplicate riders
 * UPPDATERAD: Med intelligent namn-normalisering för svenska efternamn
 */
require_once __DIR__ . '/../config.php';
require_admin();

$db = getDB();
$message = '';
$messageType = 'info';

// ============================================
// NAMN-NORMALISERING FUNKTION
// ============================================
/**
 * Normaliserar namn genom att ta bort svenska efternamn
 *"ANDERS JONSSON" →"ANDERS"
 *"ANDERS BERTIL JONSSON" →"ANDERS BERTIL"
 *"ANDERS" →"ANDERS"
 */
function normalizeRiderName($name) {
 if (!$name) return '';
 
 // Trimma och gör UPPERCASE (hanterar UTF-8 korrekt)
 $name = trim($name);
 $name = mb_strtoupper($name, 'UTF-8');
 
 // Svenska efternamn-endings (de vanligaste)
 $swedishEndings = [
 'SSON', 'SEN', 'MANN', 'BERG', 'GREN', 'LUND', 'STROM', 'STRÖM',
 'HALL', 'DAHL', 'HOLM', 'NORÉN', 'NOREN', 'ÅBERG', 'ABERG',
 'QUIST', 'HUND', 'LING', 'BLAD', 'VALL', 'MARK',
 'STRAND', 'QVIST', 'STAD', 'TORP', 'HULT', 'FORS'
 ];
 
 // Splitta på mellanslag (och ta bort tomma)
 $parts = preg_split('/\s+/', $name, -1, PREG_SPLIT_NO_EMPTY);
 
 if (count($parts) > 1) {
 $lastName = end($parts);
 
 // Kontrollera om det sista ordet är ett svenskt efternamn
 foreach ($swedishEndings as $ending) {
 if (str_ends_with($lastName, $ending)) {
 // Ta bort efternamnet
 array_pop($parts);
 break;
 }
 }
 }
 
 // Slå ihop och normalisera bindestreck
 $normalized = implode(' ', $parts);
 $normalized = str_replace('-', ' ', $normalized);
 $normalized = preg_replace('/\s+/', ' ', $normalized);
 
 return trim($normalized);
}

// Handle merge action via GET (POST doesn't work on InfinityFree)
if (isset($_GET['action']) && $_GET['action'] === 'merge') {
 $keepId = (int)($_GET['keep'] ?? 0);
 $mergeIdsRaw = $_GET['remove'] ?? '';

 // Split and convert to integers
 $parts = explode(',', $mergeIdsRaw);
 $mergeIds = [];
 foreach ($parts as $part) {
 $part = trim($part);
 if ($part !== '') {
 $mergeIds[] = intval($part);
 }
 }

 // Remove the keep_id from merge list
 $filtered = [];
 foreach ($mergeIds as $id) {
 if ($id !== $keepId && $id > 0) {
 $filtered[] = $id;
 }
 }
 $mergeIds = $filtered;

 error_log("After filtering: mergeIds=" . json_encode($mergeIds));

 if ($keepId && !empty($mergeIds)) {
 try {
 $db->pdo->beginTransaction();

 // Get the rider to keep
 $keepRider = $db->getRow("SELECT * FROM riders WHERE id = ?", [$keepId]);

 if (!$keepRider) {
 throw new Exception("Förare med ID $keepId hittades inte i databasen");
 }

 // MERGE DATA: Collect missing data from duplicates
 $fieldsToMerge = ['birth_year', 'email', 'club_id', 'gender', 'nationality', 'license_number', 'license_category'];
 $mergedData = [];
 $mergeLog = [];

 foreach ($mergeIds as $oldId) {
  $oldRider = $db->getRow("SELECT * FROM riders WHERE id = ?", [$oldId]);
  if (!$oldRider) continue;

  foreach ($fieldsToMerge as $field) {
   // If keepRider is missing this field but oldRider has it, use oldRider's value
   if (empty($keepRider[$field]) && !empty($oldRider[$field])) {
    if (!isset($mergedData[$field])) {
     $mergedData[$field] = $oldRider[$field];
     $mergeLog[] = "$field: '{$oldRider[$field]}' (från ID $oldId)";
    }
   }
  }
 }

 // Apply merged data to kept rider
 if (!empty($mergedData)) {
  $db->update('riders', $mergedData, 'id = ?', [$keepId]);
  // Refresh keepRider with merged data
  $keepRider = $db->getRow("SELECT * FROM riders WHERE id = ?", [$keepId]);
 }

 // Update all results to point to the kept rider
 $resultsUpdated = 0;
 $resultsDeleted = 0;

 foreach ($mergeIds as $oldId) {
 // Get results for this duplicate rider (include class_id for multi-class support)
 $oldResults = $db->getAll(
 "SELECT id, event_id, class_id FROM results WHERE cyclist_id = ?",
  [$oldId]
 );

 foreach ($oldResults as $oldResult) {
  // Check if kept rider already has result for this event AND class
  // Using <=> for NULL-safe comparison (rider can have one result per class per event)
  $existing = $db->getRow(
 "SELECT id FROM results WHERE cyclist_id = ? AND event_id = ? AND class_id <=> ?",
  [$keepId, $oldResult['event_id'], $oldResult['class_id']]
  );

  if ($existing) {
  // Delete the duplicate result (keep the one from the primary rider)
  $db->delete('results', 'id = ?', [$oldResult['id']]);
  $resultsDeleted++;
  } else {
  // Move the result to the kept rider
  $db->update('results', ['cyclist_id' => $keepId], 'id = ?', [$oldResult['id']]);
  $resultsUpdated++;
  }
 }
 }

 // Delete the duplicate riders
 foreach ($mergeIds as $mergeId) {
 $db->delete('riders', 'id = ?', [$mergeId]);
 }

 $db->pdo->commit();

 $msg ="Sammanfogade " . count($mergeIds) . " deltagare till " . $keepRider['firstname'] . " " . $keepRider['lastname'];
 $msg .= " ($resultsUpdated resultat flyttade";
 if ($resultsDeleted > 0) {
  $msg .= ", $resultsDeleted dubbletter borttagna";
 }
 $msg .= ")";
 if (!empty($mergeLog)) {
  $msg .= ". Data överförd: " . implode(', ', $mergeLog);
 }
 $_SESSION['cleanup_message'] = $msg;
 $_SESSION['cleanup_message_type'] = 'success';
 } catch (Exception $e) {
 if ($db->pdo->inTransaction()) {
 $db->pdo->rollBack();
 }
 $_SESSION['cleanup_message'] ="Fel vid sammanfogning:" . $e->getMessage();
 $_SESSION['cleanup_message_type'] = 'error';
 }
 } else {
 $_SESSION['cleanup_message'] ="Sammanfogning kunde inte utföras. keep_id=$keepId, merge_ids_raw='$mergeIdsRaw', merge_ids_filtered=" . json_encode($mergeIds);
 $_SESSION['cleanup_message_type'] = 'error';
 }

 // Refresh duplicate lists
 header('Location: /admin/cleanup-duplicates.php');
 exit;
}

// Handle normalize UCI-IDs action
if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['normalize_all'])) {
 checkCsrf();

 try {
 // Get all riders with UCI-IDs that need normalization
 $ridersToNormalize = $db->getAll("
 SELECT id, license_number
 FROM riders
 WHERE license_number IS NOT NULL
 AND license_number != ''
 AND license_number NOT LIKE 'SWE%'
");

 $updated = 0;
 foreach ($ridersToNormalize as $rider) {
 $normalized = normalizeUciId($rider['license_number']);
 if ($normalized !== $rider['license_number']) {
 $db->update('riders', ['license_number' => $normalized], 'id = ?', [$rider['id']]);
 $updated++;
 }
 }

 // Store message in session and redirect
 $_SESSION['cleanup_message'] ="Normaliserade UCI-ID format för $updated deltagare till XXX XXX XXX XX";
 $_SESSION['cleanup_message_type'] = 'success';
 } catch (Exception $e) {
 $_SESSION['cleanup_message'] ="Fel vid normalisering:" . $e->getMessage();
 $_SESSION['cleanup_message_type'] = 'error';
 }

 header('Location: /admin/cleanup-duplicates.php');
 exit;
}

// Handle assign SWE-IDs to riders without license numbers
if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['assign_swe_ids'])) {
 checkCsrf();

 try {
 // Find all riders without license numbers
 $ridersWithoutId = $db->getAll("
 SELECT id, firstname, lastname
 FROM riders
 WHERE license_number IS NULL OR license_number = ''
 ORDER BY id ASC
");

 $updated = 0;
 foreach ($ridersWithoutId as $rider) {
 $sweId = generateSweLicenseNumber($db);
 $db->update('riders', ['license_number' => $sweId], 'id = ?', [$rider['id']]);
 $updated++;
 }

 $_SESSION['cleanup_message'] ="Tilldelade SWE-ID till $updated förare som saknade licensnummer";
 $_SESSION['cleanup_message_type'] = 'success';
 } catch (Exception $e) {
 $_SESSION['cleanup_message'] ="Fel vid tilldelning av SWE-ID:" . $e->getMessage();
 $_SESSION['cleanup_message_type'] = 'error';
 }

 header('Location: /admin/cleanup-duplicates.php');
 exit;
}

// Handle auto merge by last name + birth year
if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['auto_merge_by_lastname_year'])) {
 checkCsrf();

 try {
 $db->pdo->beginTransaction();

 // Find riders with same lastname + birth_year but different firstnames
 $duplicates = $db->getAll("
 SELECT
 LOWER(lastname) as lastname_key,
 birth_year,
 GROUP_CONCAT(id ORDER BY
  (SELECT COUNT(*) FROM results WHERE cyclist_id = riders.id) DESC,
  CASE WHEN license_number IS NOT NULL AND license_number != '' THEN 0 ELSE 1 END,
  created_at ASC
 ) as ids,
 COUNT(*) as count
 FROM riders
 WHERE birth_year IS NOT NULL
 GROUP BY lastname_key, birth_year
 HAVING count > 1
");

 $totalMerged = 0;
 $totalDeleted = 0;

 $fieldsToMerge = ['birth_year', 'email', 'club_id', 'gender', 'nationality', 'license_number', 'license_category'];
 $totalDataMerged = 0;

 foreach ($duplicates as $dup) {
 $ids = array_map('intval', explode(',', $dup['ids']));
 if (count($ids) < 2) continue;

 $keepId = array_shift($ids); // First one (most results) to keep
 $keepRider = $db->getRow("SELECT * FROM riders WHERE id = ?", [$keepId]);

 if (!$keepRider) continue;

 // Merge data from duplicates
 $mergedData = [];
 foreach ($ids as $oldId) {
  $oldRider = $db->getRow("SELECT * FROM riders WHERE id = ?", [$oldId]);
  if (!$oldRider) continue;

  foreach ($fieldsToMerge as $field) {
   if (empty($keepRider[$field]) && !empty($oldRider[$field]) && !isset($mergedData[$field])) {
    $mergedData[$field] = $oldRider[$field];
    $totalDataMerged++;
   }
  }
 }

 if (!empty($mergedData)) {
  $db->update('riders', $mergedData, 'id = ?', [$keepId]);
 }

 foreach ($ids as $oldId) {
 // Move all results (include class_id for multi-class support)
 $oldResults = $db->getAll("SELECT id, event_id, class_id FROM results WHERE cyclist_id = ?", [$oldId]);

 foreach ($oldResults as $oldResult) {
  // Check if kept rider already has result for this event AND class
  $existing = $db->getRow(
 "SELECT id FROM results WHERE cyclist_id = ? AND event_id = ? AND class_id <=> ?",
  [$keepId, $oldResult['event_id'], $oldResult['class_id']]
  );

  if ($existing) {
  $db->delete('results', 'id = ?', [$oldResult['id']]);
  } else {
  $db->update('results', ['cyclist_id' => $keepId], 'id = ?', [$oldResult['id']]);
  $totalMerged++;
  }
 }

 // Delete the duplicate rider
 $db->delete('riders', 'id = ?', [$oldId]);
 $totalDeleted++;
 }
 }

 $db->pdo->commit();

 $msg = "Auto-sammanslagning klar! $totalMerged resultat flyttade, $totalDeleted dubbletter borttagna.";
 if ($totalDataMerged > 0) {
  $msg .= " $totalDataMerged datafält sammanfogade.";
 }
 $_SESSION['cleanup_message'] = $msg;
 $_SESSION['cleanup_message_type'] = 'success';
 } catch (Exception $e) {
 if ($db->pdo->inTransaction()) {
 $db->pdo->rollBack();
 }
 $_SESSION['cleanup_message'] ="Fel vid auto-sammanslagning:" . $e->getMessage();
 $_SESSION['cleanup_message_type'] = 'error';
 }

 header('Location: /admin/cleanup-duplicates.php');
 exit;
}

// Handle auto merge ALL duplicates action
if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['auto_merge_all'])) {
 checkCsrf();

 try {
 $db->pdo->beginTransaction();

 // Find all duplicates by normalized UCI-ID
 $duplicates = $db->getAll("
 SELECT
 REPLACE(REPLACE(license_number, ' ', ''), '-', '') as normalized_uci,
 GROUP_CONCAT(id ORDER BY
  (SELECT COUNT(*) FROM results WHERE cyclist_id = riders.id) DESC,
  CASE WHEN club_id IS NOT NULL THEN 0 ELSE 1 END,
  CASE WHEN birth_year IS NOT NULL THEN 0 ELSE 1 END,
  created_at ASC
 ) as ids
 FROM riders
 WHERE license_number IS NOT NULL
 AND license_number != ''
 GROUP BY normalized_uci
 HAVING COUNT(*) > 1
");

 $totalMerged = 0;
 $totalResultsMoved = 0;
 $totalResultsDeleted = 0;
 $ridersDeleted = 0;
 $totalDataMerged = 0;
 $fieldsToMerge = ['birth_year', 'email', 'club_id', 'gender', 'nationality', 'license_category'];

 foreach ($duplicates as $dup) {
 $ids = array_map('intval', explode(',', $dup['ids']));
 if (count($ids) < 2) continue;

 $keepId = $ids[0]; // First ID has most results (ordered by COUNT DESC)
 array_shift($ids); // Remove keep ID from list

 $keepRider = $db->getRow("SELECT * FROM riders WHERE id = ?", [$keepId]);
 if (!$keepRider) continue;

 // Merge data from duplicates
 $mergedData = [];
 foreach ($ids as $oldId) {
  $oldRider = $db->getRow("SELECT * FROM riders WHERE id = ?", [$oldId]);
  if (!$oldRider) continue;

  foreach ($fieldsToMerge as $field) {
   if (empty($keepRider[$field]) && !empty($oldRider[$field]) && !isset($mergedData[$field])) {
    $mergedData[$field] = $oldRider[$field];
    $totalDataMerged++;
   }
  }
 }

 if (!empty($mergedData)) {
  $db->update('riders', $mergedData, 'id = ?', [$keepId]);
 }

 foreach ($ids as $oldId) {
 // Get results for duplicate rider (include class_id for multi-class support)
 $oldResults = $db->getAll(
 "SELECT id, event_id, class_id FROM results WHERE cyclist_id = ?",
  [$oldId]
 );

 foreach ($oldResults as $oldResult) {
  // Check if kept rider already has result for this event AND class
  $existing = $db->getRow(
 "SELECT id FROM results WHERE cyclist_id = ? AND event_id = ? AND class_id <=> ?",
  [$keepId, $oldResult['event_id'], $oldResult['class_id']]
  );

  if ($existing) {
  // Delete duplicate result
  $db->delete('results', 'id = ?', [$oldResult['id']]);
  $totalResultsDeleted++;
  } else {
  // Move result to kept rider
  $db->update('results', ['cyclist_id' => $keepId], 'id = ?', [$oldResult['id']]);
  $totalResultsMoved++;
  }
 }

 // Delete the duplicate rider
 $db->delete('riders', 'id = ?', [$oldId]);
 $ridersDeleted++;
 }

 $totalMerged++;
 }

 $db->pdo->commit();

 $msg = "Automatisk sammanslagning klar: ";
 $msg .= "$totalMerged dubblettgrupper, ";
 $msg .= "$ridersDeleted åkare borttagna, ";
 $msg .= "$totalResultsMoved resultat flyttade";
 if ($totalResultsDeleted > 0) {
  $msg .= ", $totalResultsDeleted dubbletter borttagna";
 }
 if ($totalDataMerged > 0) {
  $msg .= ". $totalDataMerged datafält sammanfogade";
 }

 $_SESSION['cleanup_message'] = $msg;
 $_SESSION['cleanup_message_type'] = 'success';

 } catch (Exception $e) {
 if ($db->pdo->inTransaction()) {
 $db->pdo->rollBack();
 }
 $_SESSION['cleanup_message'] ="Fel vid automatisk sammanslagning:" . $e->getMessage();
 $_SESSION['cleanup_message_type'] = 'error';
 }

 header('Location: /admin/cleanup-duplicates.php');
 exit;
}

// Handle normalize names action (proper case)
if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['normalize_names'])) {
 checkCsrf();

 try {
 // Get all riders with names that need normalization
 $riders = $db->getAll("
 SELECT id, firstname, lastname
 FROM riders
 WHERE firstname IS NOT NULL OR lastname IS NOT NULL
");

 $updated = 0;
 foreach ($riders as $rider) {
 $newFirstname = $rider['firstname'];
 $newLastname = $rider['lastname'];
 $needsUpdate = false;

 // Normalize firstname
 if ($rider['firstname']) {
 $normalized = mb_convert_case(mb_strtolower($rider['firstname'], 'UTF-8'), MB_CASE_TITLE, 'UTF-8');
 if ($normalized !== $rider['firstname']) {
  $newFirstname = $normalized;
  $needsUpdate = true;
 }
 }

 // Normalize lastname
 if ($rider['lastname']) {
 $normalized = mb_convert_case(mb_strtolower($rider['lastname'], 'UTF-8'), MB_CASE_TITLE, 'UTF-8');
 if ($normalized !== $rider['lastname']) {
  $newLastname = $normalized;
  $needsUpdate = true;
 }
 }

 if ($needsUpdate) {
 $db->update('riders', [
  'firstname' => $newFirstname,
  'lastname' => $newLastname
 ], 'id = ?', [$rider['id']]);
 $updated++;
 }
 }

 $_SESSION['cleanup_message'] ="Normaliserade namn för $updated deltagare till versalgemener";
 $_SESSION['cleanup_message_type'] = 'success';
 } catch (Exception $e) {
 $_SESSION['cleanup_message'] ="Fel vid normalisering av namn:" . $e->getMessage();
 $_SESSION['cleanup_message_type'] = 'error';
 }

 header('Location: /admin/cleanup-duplicates.php');
 exit;
}

// Check for message from redirect
if (isset($_SESSION['cleanup_message'])) {
 $message = $_SESSION['cleanup_message'];
 $messageType = $_SESSION['cleanup_message_type'] ?? 'info';
 unset($_SESSION['cleanup_message'], $_SESSION['cleanup_message_type']);
}

// Count riders without license numbers
$ridersWithoutId = $db->getRow("
 SELECT COUNT(*) as count
 FROM riders
 WHERE license_number IS NULL OR license_number = ''
");
$ridersWithoutIdCount = $ridersWithoutId['count'] ?? 0;

// Find duplicate riders by normalized UCI-ID
$duplicatesByUci = $db->getAll("
 SELECT
 REPLACE(REPLACE(license_number, ' ', ''), '-', '') as normalized_uci,
 GROUP_CONCAT(id ORDER BY
 CASE WHEN club_id IS NOT NULL THEN 0 ELSE 1 END,
 CASE WHEN birth_year IS NOT NULL THEN 0 ELSE 1 END,
 created_at ASC
 ) as ids,
 GROUP_CONCAT(CONCAT(firstname, ' ', lastname) SEPARATOR ' | ') as names,
 COUNT(*) as count
 FROM riders
 WHERE license_number IS NOT NULL AND license_number != ''
 GROUP BY normalized_uci
 HAVING count > 1
 ORDER BY count DESC
");

// Find duplicate riders by name (exact match)
$duplicatesByNameRaw = $db->getAll("
 SELECT
 CONCAT(LOWER(firstname), '|', LOWER(lastname)) as name_key,
 GROUP_CONCAT(id ORDER BY
 CASE WHEN license_number IS NOT NULL AND license_number != '' THEN 0 ELSE 1 END,
 CASE WHEN club_id IS NOT NULL THEN 0 ELSE 1 END,
 created_at ASC
 ) as ids,
 GROUP_CONCAT(COALESCE(REPLACE(REPLACE(license_number, ' ', ''), '-', ''), '') SEPARATOR '|') as normalized_licenses,
 MIN(firstname) as firstname,
 MIN(lastname) as lastname,
 COUNT(*) as count
 FROM riders
 GROUP BY name_key
 HAVING count > 1
 ORDER BY count DESC
");

// Filter out entries where people have different UCI-IDs (those are different people)
$duplicatesByName = [];
foreach ($duplicatesByNameRaw as $dup) {
 $licenses = array_filter(explode('|', $dup['normalized_licenses']), fn($l) => $l !== '');

 // If there are different UCI-IDs, these are different people - skip
 if (count($licenses) > 1) {
 $uniqueLicenses = array_unique($licenses);
 if (count($uniqueLicenses) > 1) {
 continue;
 }
 }

 $duplicatesByName[] = $dup;
}

// ============================================
// POTENTIELLA DUBBLETTER VIA NORMALISERAT NAMN
// ============================================
$potentialDuplicatesByNormalized = [];
$allRidersForCompare = $db->getAll("
 SELECT id, firstname, lastname, 
 (SELECT COUNT(*) FROM results WHERE cyclist_id = riders.id) as results_count
 FROM riders
 WHERE license_number IS NULL OR license_number = ''
 ORDER BY id
");

foreach ($allRidersForCompare as $i => $rider1) {
 for ($j = $i + 1; $j < count($allRidersForCompare); $j++) {
 $rider2 = $allRidersForCompare[$j];
 
 $name1_normalized = normalizeRiderName($rider1['firstname'] . ' ' . $rider1['lastname']);
 $name2_normalized = normalizeRiderName($rider2['firstname'] . ' ' . $rider2['lastname']);
 
 if (empty($name1_normalized) || empty($name2_normalized)) {
 continue;
 }
 
 if ($name1_normalized === $name2_normalized) {
 $potentialDuplicatesByNormalized[] = [
 'rider1_id' => $rider1['id'],
 'rider1_name' => $rider1['firstname'] . ' ' . $rider1['lastname'],
 'rider1_normalized' => $name1_normalized,
 'rider1_results' => $rider1['results_count'],
 'rider2_id' => $rider2['id'],
 'rider2_name' => $rider2['firstname'] . ' ' . $rider2['lastname'],
 'rider2_normalized' => $name2_normalized,
 'rider2_results' => $rider2['results_count'],
 'match_type' => 'EXACT',
 'similarity' => 100
 ];
 } else {
 $distance = levenshtein($name1_normalized, $name2_normalized);
 $maxLen = max(strlen($name1_normalized), strlen($name2_normalized));
 $similarity = round((1 - ($distance / $maxLen)) * 100);
 
 if ($similarity > 85) {
 $potentialDuplicatesByNormalized[] = [
 'rider1_id' => $rider1['id'],
 'rider1_name' => $rider1['firstname'] . ' ' . $rider1['lastname'],
 'rider1_normalized' => $name1_normalized,
 'rider1_results' => $rider1['results_count'],
 'rider2_id' => $rider2['id'],
 'rider2_name' => $rider2['firstname'] . ' ' . $rider2['lastname'],
 'rider2_normalized' => $name2_normalized,
 'rider2_results' => $rider2['results_count'],
 'match_type' => 'FUZZY',
 'similarity' => $similarity
 ];
 }
 }
 }
}

// Find potential duplicates using fuzzy matching
$potentialDuplicates = $db->getAll("
 SELECT
 r1.id as id1,
 r1.firstname as firstname1,
 r1.lastname as lastname1,
 r1.license_number as license1,
 r1.birth_year as birth_year1,
 r2.id as id2,
 r2.firstname as firstname2,
 r2.lastname as lastname2,
 r2.license_number as license2,
 r2.birth_year as birth_year2,
 (SELECT COUNT(*) FROM results WHERE cyclist_id = r1.id) as results1,
 (SELECT COUNT(*) FROM results WHERE cyclist_id = r2.id) as results2
 FROM riders r1
 JOIN riders r2 ON r1.id < r2.id
 WHERE (
 -- Same lastname OR lastname appears anywhere in other's full name
 LOWER(r1.lastname) = LOWER(r2.lastname)
 OR LOWER(CONCAT(r2.firstname, ' ', r2.lastname)) LIKE CONCAT('%', LOWER(r1.lastname), '%')
 OR LOWER(CONCAT(r1.firstname, ' ', r1.lastname)) LIKE CONCAT('%', LOWER(r2.lastname), '%')
 -- Or names swapped between fields
 OR (LOWER(r1.firstname) = LOWER(r2.lastname) AND LOWER(r1.lastname) = LOWER(r2.firstname))
 )
 AND (
 -- And share firstname component
 LEFT(LOWER(r1.firstname), 3) = LEFT(LOWER(r2.firstname), 3)
 OR LOWER(r1.firstname) LIKE CONCAT('%', LOWER(r2.firstname), '%')
 OR LOWER(r2.firstname) LIKE CONCAT('%', LOWER(r1.firstname), '%')
 -- Or firstname appears in other's full name
 OR LOWER(CONCAT(r2.firstname, ' ', r2.lastname)) LIKE CONCAT('%', LOWER(r1.firstname), '%')
 OR LOWER(CONCAT(r1.firstname, ' ', r1.lastname)) LIKE CONCAT('%', LOWER(r2.firstname), '%')
 )
 AND NOT (
 -- Exclude if both have different UCI-IDs (different people)
 r1.license_number IS NOT NULL AND r1.license_number != ''
 AND r2.license_number IS NOT NULL AND r2.license_number != ''
 AND REPLACE(REPLACE(r1.license_number, ' ', ''), '-', '') != REPLACE(REPLACE(r2.license_number, ' ', ''), '-', '')
 )
 AND NOT (
 -- Exclude exact full name matches (already in duplicatesByName)
 LOWER(r1.firstname) = LOWER(r2.firstname) AND LOWER(r1.lastname) = LOWER(r2.lastname)
 )
 ORDER BY r1.lastname, r1.firstname
 LIMIT 200
");

// Handle search for riders
$searchQuery = $_GET['search'] ?? '';
$searchResults = [];
if (!empty($searchQuery)) {
 $searchTerm = '%' . $searchQuery . '%';
 $searchResults = $db->getAll("
 SELECT id, firstname, lastname, license_number, birth_year,
 (SELECT COUNT(*) FROM results WHERE cyclist_id = riders.id) as result_count
 FROM riders
 WHERE firstname LIKE ? OR lastname LIKE ?
 OR CONCAT(firstname, ' ', lastname) LIKE ?
 OR CONCAT(lastname, ' ', firstname) LIKE ?
 ORDER BY lastname, firstname
 LIMIT 50
", [$searchTerm, $searchTerm, $searchTerm, $searchTerm]);
}

// Page config for unified layout
$page_title = 'Rensa dubbletter';
$breadcrumbs = [
    ['label' => 'Verktyg', 'url' => '/admin/tools'],
    ['label' => 'Rensa dubbletter']
];
include __DIR__ . '/components/unified-layout.php';
?>


 
 <h1 class="text-primary mb-lg">
 <i data-lucide="copy-x"></i>
 Rensa dubbletter
 </h1>

 <?php if ($message): ?>
 <div class="alert alert-<?= $messageType ?> mb-lg">
 <i data-lucide="<?= $messageType === 'success' ? 'check-circle' : 'alert-circle' ?>"></i>
 <?= h($message) ?>
 </div>
 <?php endif; ?>

 <!-- Manual Merge -->
 <div class="card mb-lg">
 <div class="card-header">
 <h2 class="text-primary">
  <i data-lucide="git-merge"></i>
  Manuell sammanslagning
 </h2>
 </div>
 <div class="card-body">
 <p class="text-secondary mb-md">
  Slå ihop två förare genom att ange deras ID-nummer. Förare 1 behålls, förare 2:s resultat flyttas dit.
 </p>
 <div class="flex gap-md gs-items-end">
  <div>
  <label class="label">Behåll (ID)</label>
  <input type="number" id="manual_keep" class="input" placeholder="t.ex. 10624" style="width: 120px;">
  </div>
  <div>
  <label class="label">Ta bort (ID)</label>
  <input type="number" id="manual_remove" class="input" placeholder="t.ex. 9460" style="width: 120px;">
  </div>
  <button type="button" class="btn btn-warning" onclick="doManualMerge()">
  <i data-lucide="git-merge"></i>
  Slå ihop
  </button>
 </div>
 <p class="text-xs text-secondary mt-sm">
  Tips: Hitta ID i URL:en på förarsidan, t.ex. rider.php?id=<strong>10624</strong>
 </p>
 <script>
 function doManualMerge() {
  var keep = document.getElementById('manual_keep').value;
  var remove = document.getElementById('manual_remove').value;
  if (!keep || !remove) {
  alert('Fyll i båda ID-fälten');
  return;
  }
  if (confirm('Slå ihop förare ' + remove + ' till ' + keep + '? Detta kan inte ångras.')) {
  window.location.href = '/admin/cleanup-duplicates.php?action=merge&keep=' + keep + '&remove=' + remove;
  }
 }
 </script>
 </div>
 </div>

 <!-- Search and Merge -->
 <div class="card mb-lg">
 <div class="card-header">
 <h2 class="text-primary">
  <i data-lucide="search"></i>
  Sök och slå ihop
 </h2>
 </div>
 <div class="card-body">
 <form method="GET" class="mb-md">
  <div class="flex gap-md gs-items-end">
  <div class="flex-1">
  <label class="label">Sök på namn</label>
  <input type="text" name="search" class="input" placeholder="t.ex. Andersson" value="<?= h($searchQuery) ?>">
  </div>
  <button type="submit" class="btn btn--primary">
  <i data-lucide="search"></i>
  Sök
  </button>
  </div>
 </form>

 <?php if (!empty($searchQuery)): ?>
  <?php if (empty($searchResults)): ?>
  <div class="alert alert--info">
  Inga förare hittades för"<?= h($searchQuery) ?>"
  </div>
  <?php else: ?>
  <form method="POST" onsubmit="return confirmMerge()">
  <?= csrf_field() ?>
  <input type="hidden" name="merge_riders" value="1">

  <div class="gs-overflow-x-auto mb-md">
  <table class="table table-compact">
   <thead>
   <tr>
   <th style="width: 60px;">Behåll</th>
   <th style="width: 60px;">Ta bort</th>
   <th>Namn</th>
   <th>ID</th>
   <th>Licens</th>
   <th>År</th>
   <th>Res.</th>
   </tr>
   </thead>
   <tbody>
   <?php foreach ($searchResults as $rider): ?>
   <tr>
   <td>
    <input type="radio" name="keep_id" value="<?= $rider['id'] ?>">
   </td>
   <td>
    <input type="checkbox" name="merge_list[]" value="<?= $rider['id'] ?>">
   </td>
   <td>
    <a href="/rider.php?id=<?= $rider['id'] ?>" target="_blank">
    <?= h($rider['firstname'] . ' ' . $rider['lastname']) ?>
    </a>
   </td>
   <td class="text-xs"><?= $rider['id'] ?></td>
   <td class="text-xs"><?= h($rider['license_number'] ?: '-') ?></td>
   <td><?= $rider['birth_year'] ?: '-' ?></td>
   <td><?= $rider['result_count'] ?></td>
   </tr>
   <?php endforeach; ?>
   </tbody>
  </table>
  </div>

  <button type="submit" class="btn btn-warning">
  <i data-lucide="git-merge"></i>
  Slå ihop valda
  </button>
  <p class="text-xs text-secondary mt-sm">
  Välj EN förare att behålla (radio) och markera de som ska tas bort (checkbox)
  </p>
  </form>

  <script>
  function confirmMerge() {
  const keepId = document.querySelector('input[name="keep_id"]:checked');
  const mergeList = document.querySelectorAll('input[name="merge_list[]"]:checked');

  if (!keepId) {
  alert('Välj en förare att behålla (radio-knapp)');
  return false;
  }
  if (mergeList.length === 0) {
  alert('Välj minst en förare att ta bort (checkbox)');
  return false;
  }

  // Build merge_ids string
  const mergeIds = Array.from(mergeList).map(cb => cb.value).join(',');

  // Add hidden field with merge_ids
  const input = document.createElement('input');
  input.type = 'hidden';
  input.name = 'merge_ids';
  input.value = mergeIds;
  keepId.form.appendChild(input);

  return confirm('Slå ihop ' + mergeList.length + ' förare till den valda? Detta kan inte ångras.');
  }
  </script>
  <?php endif; ?>
 <?php endif; ?>
 </div>
 </div>

 <!-- Normalize Names -->
 <div class="card mb-lg">
 <div class="card-header">
 <h2 class="text-primary">
  <i data-lucide="type"></i>
  Normalisera namn
 </h2>
 </div>
 <div class="card-body">
 <p class="text-secondary mb-md">
  Konvertera alla namn till versalgemener (första bokstaven stor, resten små).
  <br><strong>Exempel:</strong>"JOHAN ANDERSSON" eller"johan andersson" blir"Johan Andersson"
 </p>
 <form method="POST" onsubmit="return confirm('Detta kommer ändra alla deltagarnamn till versalgemener. Fortsätt?');">
  <?= csrf_field() ?>
  <button type="submit" name="normalize_names" class="btn btn--primary">
  <i data-lucide="case-sensitive"></i>
  Normalisera alla namn
  </button>
 </form>
 </div>
 </div>

 <!-- Normalize All UCI-IDs -->
 <div class="card mb-lg">
 <div class="card-header">
 <h2 class="text-primary">
  <i data-lucide="wand-2"></i>
  Normalisera UCI-ID format
 </h2>
 </div>
 <div class="card-body">
 <p class="text-secondary mb-md">
  Formatera alla UCI-ID till standardformat för bättre läsbarhet och förhindra dubbletter.
  <br><strong>Exempel:</strong>"10108943209" eller"101-089-432-09" blir"101 089 432 09"
 </p>
 <div class="flex gap-md">
  <form method="POST">
  <?= csrf_field() ?>
  <button type="submit" name="normalize_all" class="btn btn--primary">
  <i data-lucide="zap"></i>
  Normalisera alla UCI-ID
  </button>
  </form>
  <form method="POST" onsubmit="return confirm('Detta tilldelar SWE-ID till <?= $ridersWithoutIdCount ?> förare som saknar licensnummer. Fortsätt?');">
  <?= csrf_field() ?>
  <button type="submit" name="assign_swe_ids" class="btn btn-success" <?= $ridersWithoutIdCount === 0 ? 'disabled' : '' ?>>
  <i data-lucide="id-card"></i>
  Tilldela SWE-ID (<?= $ridersWithoutIdCount ?>)
  </button>
  </form>
  <form method="POST" onsubmit="return confirm('Detta sammanfogar alla med samma EFTERNAMN + FÖDELSEÅR. Föraren med flest resultat behålls. Fortsätt?');">
  <?= csrf_field() ?>
  <button type="submit" name="auto_merge_by_lastname_year" class="btn btn-success">
  <i data-lucide="users"></i>
  Sammanfoga efternamn+år
  </button>
  </form>
  <form method="POST" onsubmit="return confirm('Detta kommer automatiskt sammanfoga ALLA dubbletter via UCI-ID. Åkaren med flest resultat behålls. Fortsätt?');">
  <?= csrf_field() ?>
  <button type="submit" name="auto_merge_all" class="btn btn-warning">
  <i data-lucide="git-merge"></i>
  Sammanfoga UCI-ID
  </button>
  </form>
 </div>
 </div>
 </div>

 <!-- Potentiella dubbletter via normaliserat namn (NYT) -->
 <div class="card mb-lg">
 <div class="card-header">
 <h2 class="text-success">
  <i data-lucide="star"></i>
  Potentiella dubbletter (normaliserat namn) (<?= count($potentialDuplicatesByNormalized) ?>)
 </h2>
 </div>
 <div class="card-body">
 <p class="text-secondary mb-md">
  <i data-lucide="lightbulb" class="gs-icon-inline"></i>
  Matchar namn genom att först normalisera dem (ta bort svenska efternamn).
  <br>T.ex."ANDERS JONSSON" och"ANDERS" matchas automatiskt.
 </p>
 
 <?php if (empty($potentialDuplicatesByNormalized)): ?>
  <div class="alert alert--success">
  <i data-lucide="check"></i>
  Inga potentiella dubbletter hittades!
  </div>
 <?php else: ?>
  <div class="gs-overflow-x-auto">
  <table class="table table-compact">
  <thead>
  <tr>
   <th>Förare 1 (Original)</th>
   <th>Normaliserat</th>
   <th>Förare 2 (Original)</th>
   <th>Normaliserat</th>
   <th>Match</th>
   <th>Res.</th>
   <th>Åtgärd</th>
  </tr>
  </thead>
  <tbody>
  <?php foreach ($potentialDuplicatesByNormalized as $dup): ?>
   <tr>
   <td>
   <a href="/rider.php?id=<?= $dup['rider1_id'] ?>" target="_blank">
   <strong><?= h($dup['rider1_name']) ?></strong>
   </a>
   <br><span class="text-xs text-secondary">(ID: <?= $dup['rider1_id'] ?>)</span>
   </td>
   <td class="text-xs" style="background-color: #f9f9f9; font-family: monospace;">
   <?= h($dup['rider1_normalized']) ?>
   </td>
   <td>
   <a href="/rider.php?id=<?= $dup['rider2_id'] ?>" target="_blank">
   <strong><?= h($dup['rider2_name']) ?></strong>
   </a>
   <br><span class="text-xs text-secondary">(ID: <?= $dup['rider2_id'] ?>)</span>
   </td>
   <td class="text-xs" style="background-color: #f9f9f9; font-family: monospace;">
   <?= h($dup['rider2_normalized']) ?>
   </td>
   <td>
   <?php if ($dup['match_type'] === 'EXACT'): ?>
   <span class="badge badge-success">Exakt</span>
   <?php else: ?>
   <span class="badge badge-warning"><?= $dup['similarity'] ?>%</span>
   <?php endif; ?>
   </td>
   <td class="text-xs">
   <?= $dup['rider1_results'] ?> + <?= $dup['rider2_results'] ?>
   </td>
   <td>
   <?php
   $keepId = $dup['rider1_results'] >= $dup['rider2_results'] ? $dup['rider1_id'] : $dup['rider2_id'];
   $mergeId = $dup['rider1_results'] >= $dup['rider2_results'] ? $dup['rider2_id'] : $dup['rider1_id'];
   ?>
   <form method="POST" class="gs-inline" onsubmit="return confirm('Sammanfoga denna? Föraren med flest resultat behålls.');">
   <?= csrf_field() ?>
   <input type="hidden" name="merge_riders" value="1">
   <input type="hidden" name="keep_id" value="<?= $keepId ?>">
   <input type="hidden" name="merge_ids" value="<?= $mergeId ?>">
   <button type="submit" class="btn btn-xs btn-success">
    <i data-lucide="git-merge"></i>
    Slå ihop
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

 <!-- Duplicates by UCI-ID -->
 <div class="card mb-lg">
 <div class="card-header">
 <h2 class="text-primary">
  <i data-lucide="fingerprint"></i>
  Dubbletter via UCI-ID (<?= count($duplicatesByUci) ?>)
 </h2>
 </div>
 <div class="card-body">
 <?php if (empty($duplicatesByUci)): ?>
  <div class="alert alert--success">
  <i data-lucide="check"></i>
  Inga dubbletter hittades baserat på UCI-ID
  </div>
 <?php else: ?>
  <div class="table-responsive" style="max-height: 400px; overflow: auto;">
  <table class="table table-sm">
  <thead>
  <tr>
   <th>UCI-ID</th>
   <th>Namn</th>
   <th>Antal</th>
   <th>Åtgärd</th>
  </tr>
  </thead>
  <tbody>
  <?php foreach ($duplicatesByUci as $dup): ?>
   <?php
   $ids = explode(',', $dup['ids']);
   $riders = $db->getAll(
  "SELECT id, firstname, lastname, license_number, birth_year, club_id,
   (SELECT name FROM clubs WHERE id = riders.club_id) as club_name,
   (SELECT COUNT(*) FROM results WHERE cyclist_id = riders.id) as results_count
   FROM riders WHERE id IN (" . implode(',', $ids) .")
   ORDER BY FIELD(id," . implode(',', $ids) .")"
   );
   ?>
   <tr>
   <td><code><?= h($dup['normalized_uci']) ?></code></td>
   <td>
   <?php foreach ($riders as $i => $rider): ?>
   <div class="mb-sm <?= $i === 0 ? 'text-success' : 'text-secondary' ?>">
    <strong><?= h($rider['firstname'] . ' ' . $rider['lastname']) ?></strong>
    <?php if ($rider['club_name']): ?>
    <span class="text-xs">(<?= h($rider['club_name']) ?>)</span>
    <?php endif; ?>
    <span class="badge badge-sm <?= $i === 0 ? 'badge-success' : 'badge-secondary' ?>">
    <?= $rider['results_count'] ?> resultat
    </span>
   </div>
   <?php endforeach; ?>
   </td>
   <td><?= $dup['count'] ?></td>
   <td>
   <form method="POST" style="display: inline;" onsubmit="return confirm('Sammanfoga dessa deltagare? Alla resultat flyttas till den första.');">
   <?= csrf_field() ?>
   <input type="hidden" name="keep_id" value="<?= $ids[0] ?>">
   <input type="hidden" name="merge_ids" value="<?= $dup['ids'] ?>">
   <button type="submit" name="merge_riders" class="btn btn--sm btn-warning">
    <i data-lucide="merge"></i>
    Sammanfoga
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

 <!-- Duplicates by Name -->
 <div class="card">
 <div class="card-header">
 <h2 class="text-primary">
  <i data-lucide="users"></i>
  Dubbletter via namn (<?= count($duplicatesByName) ?>)
 </h2>
 </div>
 <div class="card-body">
 <?php if (empty($duplicatesByName)): ?>
  <div class="alert alert--success">
  <i data-lucide="check"></i>
  Inga dubbletter hittades baserat på namn
  </div>
 <?php else: ?>
  <p class="text-sm text-secondary mb-md">
  <strong>Varning:</strong> Dubbletter via namn kan vara olika personer med samma namn.
  Kontrollera UCI-ID och klubb innan sammanfogning.
  </p>
  <div class="table-responsive" style="max-height: 400px; overflow: auto;">
  <table class="table table-sm">
  <thead>
  <tr>
   <th>Namn</th>
   <th>UCI-ID</th>
   <th>Antal</th>
   <th>Åtgärd</th>
  </tr>
  </thead>
  <tbody>
  <?php foreach (array_slice($duplicatesByName, 0, 50) as $dup): ?>
   <?php
   $ids = explode(',', $dup['ids']);
   $riders = $db->getAll(
  "SELECT id, firstname, lastname, license_number, birth_year, club_id,
   (SELECT name FROM clubs WHERE id = riders.club_id) as club_name,
   (SELECT COUNT(*) FROM results WHERE cyclist_id = riders.id) as results_count
   FROM riders WHERE id IN (" . implode(',', $ids) .")
   ORDER BY FIELD(id," . implode(',', $ids) .")"
   );
   ?>
   <tr>
   <td>
   <strong><?= h($dup['firstname'] . ' ' . $dup['lastname']) ?></strong>
   </td>
   <td>
   <?php foreach ($riders as $i => $rider): ?>
   <div class="text-xs <?= $i === 0 ? 'text-success' : 'text-secondary' ?>">
    <?= $rider['license_number'] ?: '<em>ingen</em>' ?>
    <?php if ($rider['club_name']): ?>
    (<?= h($rider['club_name']) ?>)
    <?php endif; ?>
    <span class="badge badge-xs"><?= $rider['results_count'] ?> res</span>
   </div>
   <?php endforeach; ?>
   </td>
   <td><?= $dup['count'] ?></td>
   <td>
   <form method="POST" style="display: inline;" onsubmit="return confirm('Sammanfoga dessa deltagare? Kontrollera att det verkligen är samma person!');">
   <?= csrf_field() ?>
   <input type="hidden" name="keep_id" value="<?= $ids[0] ?>">
   <input type="hidden" name="merge_ids" value="<?= $dup['ids'] ?>">
   <button type="submit" name="merge_riders" class="btn btn--sm btn--secondary">
    <i data-lucide="merge"></i>
    Sammanfoga
   </button>
   </form>
   </td>
   </tr>
  <?php endforeach; ?>
  </tbody>
  </table>
  </div>
  <?php if (count($duplicatesByName) > 50): ?>
  <p class="text-sm text-secondary mt-md">
  Visar 50 av <?= count($duplicatesByName) ?> dubbletter
  </p>
  <?php endif; ?>
 <?php endif; ?>
 </div>
 </div>

 <!-- Potential Duplicates (Fuzzy Matching) -->
 <div class="card mb-lg">
 <div class="card-header">
 <h2 class="text-warning">
  <i data-lucide="search"></i>
  Potentiella dubbletter (<?= count($potentialDuplicates) ?>)
 </h2>
 </div>
 <div class="card-body">
 <p class="text-secondary mb-md">
  <i data-lucide="alert-triangle" class="gs-icon-inline"></i>
  Dessa har liknande namn men inte exakt matchning. Granska manuellt innan sammanslagning.
 </p>
 <?php if (empty($potentialDuplicates)): ?>
  <div class="alert alert--success">
  <i data-lucide="check"></i>
  Inga potentiella dubbletter hittades med fuzzy-matchning!
  </div>
 <?php else: ?>
  <div class="gs-overflow-x-auto">
  <table class="table table-compact">
  <thead>
  <tr>
   <th>Förare 1</th>
   <th>ID/År</th>
   <th>Res.</th>
   <th>Förare 2</th>
   <th>ID/År</th>
   <th>Res.</th>
   <th>Åtgärd</th>
  </tr>
  </thead>
  <tbody>
  <?php foreach ($potentialDuplicates as $dup): ?>
   <tr>
   <td>
   <a href="/rider.php?id=<?= $dup['id1'] ?>" target="_blank">
   <?= h($dup['firstname1'] . ' ' . $dup['lastname1']) ?>
   </a>
   </td>
   <td class="text-xs text-secondary">
   <?= h($dup['license1'] ?: '-') ?><br>
   <?= $dup['birth_year1'] ?: '-' ?>
   </td>
   <td><?= $dup['results1'] ?></td>
   <td>
   <a href="/rider.php?id=<?= $dup['id2'] ?>" target="_blank">
   <?= h($dup['firstname2'] . ' ' . $dup['lastname2']) ?>
   </a>
   </td>
   <td class="text-xs text-secondary">
   <?= h($dup['license2'] ?: '-') ?><br>
   <?= $dup['birth_year2'] ?: '-' ?>
   </td>
   <td><?= $dup['results2'] ?></td>
   <td>
   <?php
   // Determine which rider to keep (more results wins)
   $keepId = $dup['results1'] >= $dup['results2'] ? $dup['id1'] : $dup['id2'];
   $mergeId = $dup['results1'] >= $dup['results2'] ? $dup['id2'] : $dup['id1'];
   ?>
   <form method="POST" class="gs-inline" onsubmit="return confirm('Sammanfoga dessa förare? Föraren med flest resultat behålls.');">
   <?= csrf_field() ?>
   <input type="hidden" name="merge_riders" value="1">
   <input type="hidden" name="keep_id" value="<?= $keepId ?>">
   <input type="hidden" name="merge_ids" value="<?= $mergeId ?>">
   <button type="submit" class="btn btn-xs btn-warning">
    <i data-lucide="git-merge"></i>
    Slå ihop
   </button>
   </form>
   </td>
   </tr>
  <?php endforeach; ?>
  </tbody>
  </table>
  </div>
  <?php if (count($potentialDuplicates) >= 100): ?>
  <p class="text-sm text-secondary mt-md">
  Visar max 100 potentiella dubbletter
  </p>
  <?php endif; ?>
 <?php endif; ?>
 </div>
 </div>

 <div class="mt-lg">
 <a href="/admin/import.php" class="btn btn--secondary">
 <i data-lucide="arrow-left"></i>
 Tillbaka till import
 </a>
 </div>
 </div>


<?php include __DIR__ . '/components/unified-layout-footer.php'; ?>