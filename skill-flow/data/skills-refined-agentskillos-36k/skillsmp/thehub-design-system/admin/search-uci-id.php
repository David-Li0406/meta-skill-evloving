<?php
/**
 * Search UCI-ID Tool
 * Upload CSV to find and fill in License Numbers
 * Version: v1.2.0 [2025-11-22-003]
 */
error_reporting(E_ALL);
ini_set('display_errors', 1);

require_once __DIR__ . '/../config.php';
require_admin();

$db = getDB();
$results = [];
$headers = [];
$matchStats = ['exact' => 0, 'fuzzy' => 0, 'partial' => 0, 'not_found' => 0];
$message = '';
$messageType = '';

// Column mapping defaults
$colMapping = [
 'firstname' => $_POST['col_firstname'] ?? 0,
 'lastname' => $_POST['col_lastname'] ?? 1,
 'club' => $_POST['col_club'] ?? 2,
 'class' => $_POST['col_class'] ?? 3,
 'uci_id' => $_POST['col_uci_id'] ?? 4
];

// Handle selection updates via AJAX
if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['action']) && $_POST['action'] === 'update_selection') {
 header('Content-Type: application/json');
 $selected = json_decode($_POST['selected'] ?? '[]', true);
 $_SESSION['lookup_selected'] = $selected;
 echo json_encode(['success' => true]);
 exit;
}

// Handle CSV export
if (isset($_GET['export']) && !empty($_SESSION['lookup_results'])) {
 $exportData = $_SESSION['lookup_results'];
 $exportHeaders = $_SESSION['lookup_headers'];
 $selected = $_SESSION['lookup_selected'] ?? array_keys($exportData);

 header('Content-Type: text/csv; charset=utf-8');
 header('Content-Disposition: attachment; filename="riders_with_license.csv"');

 $output = fopen('php://output', 'w');
 fprintf($output, chr(0xEF).chr(0xBB).chr(0xBF)); // UTF-8 BOM

 // Write header
 fputcsv($output, $exportHeaders, ';');

 // Write only selected data
 foreach ($exportData as $index => $row) {
 if (in_array($index, $selected)) {
 fputcsv($output, $row, ';');
 }
 }

 fclose($output);
 exit;
}

// Handle file upload
if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_FILES['csv_file'])) {
 checkCsrf();

 $file = $_FILES['csv_file'];

 if ($file['error'] !== UPLOAD_ERR_OK) {
 $message = 'Filuppladdning misslyckades';
 $messageType = 'error';
 } else {
 $content = file_get_contents($file['tmp_name']);

 // Detect encoding and convert to UTF-8
 $encoding = mb_detect_encoding($content, ['UTF-8', 'ISO-8859-1', 'Windows-1252'], true);
 if ($encoding && $encoding !== 'UTF-8') {
 $content = mb_convert_encoding($content, 'UTF-8', $encoding);
 }

 // Remove BOM if present
 $content = preg_replace('/^\xEF\xBB\xBF/', '', $content);

 $lines = explode("\n", $content);

 // Detect separator
 $firstLine = $lines[0] ?? '';
 $separator = ';';
 if (substr_count($firstLine, ',') > substr_count($firstLine, ';')) {
 $separator = ',';
 } elseif (substr_count($firstLine,"\t") > substr_count($firstLine, ';')) {
 $separator ="\t";
 }

 // Parse header
 $headers = str_getcsv(trim($lines[0]), $separator);
 $headers = array_map('trim', $headers);

 // Get column indices from POST or auto-detect
 $colMapping['firstname'] = (int)($_POST['col_firstname'] ?? findColumn($headers, ['förnamn', 'firstname', 'first_name', 'first name']));
 $colMapping['lastname'] = (int)($_POST['col_lastname'] ?? findColumn($headers, ['efternamn', 'lastname', 'last_name', 'last name', 'name']));
 $colMapping['club'] = (int)($_POST['col_club'] ?? findColumn($headers, ['klubb', 'club', 'team', 'förening']));
 $colMapping['class'] = (int)($_POST['col_class'] ?? findColumn($headers, ['klass', 'class', 'kategori', 'category']));
 $colMapping['uci_id'] = (int)($_POST['col_uci_id'] ?? findColumn($headers, ['uci_id', 'uci id', 'uciid', 'license', 'licens', 'license_number']));

 // Process data rows
 $exportData = [];

 for ($i = 1; $i < count($lines); $i++) {
 $line = trim($lines[$i]);
 if (empty($line)) continue;

 $parts = str_getcsv($line, $separator);

 $firstname = trim($parts[$colMapping['firstname']] ?? '');
 $lastname = trim($parts[$colMapping['lastname']] ?? '');
 $club = trim($parts[$colMapping['club']] ?? '');
 $inputClass = trim($parts[$colMapping['class']] ?? '');
 $existingUciId = trim($parts[$colMapping['uci_id']] ?? '');

 if (empty($firstname) && empty($lastname)) {
 continue;
 }

 // Search for rider if no UCI ID exists
 $match = null;
 $uciId = normalizeUciId($existingUciId);

 if (empty($existingUciId) || strpos($existingUciId, 'SWE25') === 0) {
 $match = findRider($db, $firstname, $lastname, $club);
 if ($match && !empty($match['license_number'])) {
  $uciId = normalizeUciId($match['license_number']);
 }
 }

 // Update stats
 if ($match) {
 $matchStats[$match['match_type']]++;
 } elseif (empty($existingUciId)) {
 $matchStats['not_found']++;
 }

 // Fill in UCI ID in the row
 while (count($parts) <= $colMapping['uci_id']) {
 $parts[] = '';
 }
 $parts[$colMapping['uci_id']] = $uciId;

 $exportData[] = $parts;

 $results[] = [
 'firstname' => $firstname,
 'lastname' => $lastname,
 'club' => $club,
 'class' => $inputClass,
 'original_uci_id' => $existingUciId,
 'uci_id' => $uciId,
 'match_type' => $match ? $match['match_type'] : ($existingUciId ? 'existing' : 'not_found'),
 'found_name' => $match ? $match['firstname'] . ' ' . $match['lastname'] : '',
 'found_club' => $match ? $match['club_name'] : '',
 'confidence' => $match ? $match['confidence'] : 0
 ];
 }

 // Store for export
 $_SESSION['lookup_results'] = $exportData;
 $_SESSION['lookup_headers'] = $headers;
 // Initialize all rows as selected
 $_SESSION['lookup_selected'] = array_keys($exportData);

 $message = 'CSV bearbetad: ' . count($results) . ' rader';
 $messageType = 'success';
 }
}

// Get current selection state
$selectedRows = $_SESSION['lookup_selected'] ?? [];

/**
 * Find column index by name
 */
function findColumn($headers, $names) {
 foreach ($headers as $i => $header) {
 $normalized = strtolower(trim($header));
 foreach ($names as $name) {
 if ($normalized === strtolower($name)) {
 return $i;
 }
 }
 }
 return 0;
}

/**
 * Find rider in database using multiple strategies
 * Uses license_number field (TheHUB structure)
 */
function findRider($db, $firstname, $lastname, $club) {
 $normFirstname = normalizeString($firstname);
 $normLastname = normalizeString($lastname);
 $normClub = normalizeString($club);

 // Strategy 1: Exact match with club
 if (!empty($club)) {
 try {
 $riders = $db->getAll("
 SELECT r.id, r.firstname, r.lastname, r.license_number,
  r.birth_year, r.gender, c.name as club_name
 FROM riders r
 LEFT JOIN clubs c ON r.club_id = c.id
 WHERE LOWER(r.firstname) = ?
  AND LOWER(r.lastname) = ?
  AND LOWER(c.name) LIKE ?
  AND r.license_number IS NOT NULL
  AND r.license_number != ''
 ORDER BY r.license_year DESC
 LIMIT 1
", [strtolower($firstname), strtolower($lastname), '%' . strtolower($club) . '%']);

 if (!empty($riders)) {
 $rider = $riders[0];
 return array_merge($rider, ['match_type' => 'exact', 'confidence' => 100]);
 }
 } catch (Exception $e) {
 // Fallthrough to next strategy
 }
 }

 // Strategy 2: Exact name match (any club)
 try {
 $riders = $db->getAll("
 SELECT r.id, r.firstname, r.lastname, r.license_number,
  r.birth_year, r.gender, c.name as club_name
 FROM riders r
 LEFT JOIN clubs c ON r.club_id = c.id
 WHERE LOWER(r.firstname) = ?
 AND LOWER(r.lastname) = ?
 AND r.license_number IS NOT NULL
 AND r.license_number != ''
 ORDER BY r.license_year DESC
 LIMIT 1
", [strtolower($firstname), strtolower($lastname)]);

 if (!empty($riders)) {
 $rider = $riders[0];
 $confidence = empty($club) ? 90 : (stripos($rider['club_name'] ?? '', $club) !== false ? 95 : 80);
 return array_merge($rider, ['match_type' => 'exact', 'confidence' => $confidence]);
 }
 } catch (Exception $e) {
 // Fallthrough to next strategy
 }

 // Strategy 2b: Handle double last names (e.g.,"Svensson Lindberg")
 try {
 $riders = $db->getAll("
 SELECT r.id, r.firstname, r.lastname, r.license_number,
  r.birth_year, r.gender, c.name as club_name
 FROM riders r
 LEFT JOIN clubs c ON r.club_id = c.id
 WHERE LOWER(r.firstname) = ?
 AND (LOWER(r.lastname) LIKE ? OR ? LIKE CONCAT('%', LOWER(r.lastname), '%'))
 AND r.license_number IS NOT NULL
 AND r.license_number != ''
 ORDER BY r.license_year DESC
 LIMIT 1
", [strtolower($firstname), '%' . strtolower($lastname) . '%', strtolower($lastname)]);

 if (!empty($riders)) {
 $rider = $riders[0];
 $confidence = 85;
 if (!empty($club) && stripos($rider['club_name'] ?? '', $club) !== false) {
 $confidence = 90;
 }
 return array_merge($rider, ['match_type' => 'exact', 'confidence' => $confidence]);
 }
 } catch (Exception $e) {
 // Fallthrough to next strategy
 }

 // Strategy 2c: If lastname has space, try matching last part only
 if (strpos($lastname, ' ') !== false) {
 try {
 $lastnameParts = explode(' ', $lastname);
 $lastPart = end($lastnameParts);

 $riders = $db->getAll("
 SELECT r.id, r.firstname, r.lastname, r.license_number,
  r.birth_year, r.gender, c.name as club_name
 FROM riders r
 LEFT JOIN clubs c ON r.club_id = c.id
 WHERE LOWER(r.firstname) = ?
  AND LOWER(r.lastname) LIKE ?
  AND r.license_number IS NOT NULL
  AND r.license_number != ''
 ORDER BY r.license_year DESC
 LIMIT 1
", [strtolower($firstname), '%' . strtolower($lastPart)]);

 if (!empty($riders)) {
 $rider = $riders[0];
 $confidence = 80;
 if (!empty($club) && stripos($rider['club_name'] ?? '', $club) !== false) {
  $confidence = 85;
 }
 return array_merge($rider, ['match_type' => 'fuzzy', 'confidence' => $confidence]);
 }
 } catch (Exception $e) {
 // Fallthrough to next strategy
 }
 }

 // Strategy 3: Fuzzy match (normalized names) - no LIMIT to search all riders
 try {
 $riders = $db->getAll("
 SELECT r.id, r.firstname, r.lastname, r.license_number,
  r.birth_year, r.gender, c.name as club_name
 FROM riders r
 LEFT JOIN clubs c ON r.club_id = c.id
 WHERE r.license_number IS NOT NULL
 AND r.license_number != ''
 ORDER BY r.license_year DESC
", []);

 $bestMatch = null;
 $bestScore = 0;

 foreach ($riders as $rider) {
 $riderNormFirst = normalizeString($rider['firstname']);
 $riderNormLast = normalizeString($rider['lastname']);

 if ($riderNormFirst === $normFirstname && $riderNormLast === $normLastname) {
 $score = 85;

 if (!empty($normClub) && !empty($rider['club_name'])) {
  $riderNormClub = normalizeString($rider['club_name']);
  if (strpos($riderNormClub, $normClub) !== false || strpos($normClub, $riderNormClub) !== false) {
  $score = 90;
  }
 }

 if ($score > $bestScore) {
  $bestScore = $score;
  $bestMatch = array_merge($rider, ['match_type' => 'fuzzy', 'confidence' => $score]);
 }
 }

 // Partial match (first 3 chars)
 if (strlen($normFirstname) >= 3 && strlen($normLastname) >= 3) {
 if (substr($riderNormFirst, 0, 3) === substr($normFirstname, 0, 3) &&
  substr($riderNormLast, 0, 3) === substr($normLastname, 0, 3)) {
  $score = 60;

  if (!empty($normClub) && !empty($rider['club_name'])) {
  $riderNormClub = normalizeString($rider['club_name']);
  if (strpos($riderNormClub, $normClub) !== false || strpos($normClub, $riderNormClub) !== false) {
  $score = 70;
  }
  }

  if ($score > $bestScore) {
  $bestScore = $score;
  $bestMatch = array_merge($rider, ['match_type' => 'partial', 'confidence' => $score]);
  }
 }
 }
 }

 if ($bestMatch) {
 return $bestMatch;
 }
 } catch (Exception $e) {
 // No matches found
 }

 return null;
}

/**
 * Normalize string for comparison (without iconv for compatibility)
 */
function normalizeString($str) {
 $str = mb_strtolower(trim($str), 'UTF-8');
 // Replace Swedish characters
 $str = preg_replace('/[åä]/u', 'a', $str);
 $str = preg_replace('/[ö]/u', 'o', $str);
 $str = preg_replace('/[é]/u', 'e', $str);
 $str = preg_replace('/[^a-z0-9]/u', '', $str);
 return $str;
}

// Page config for unified layout
$page_title = 'Sök License Number (UCI-ID)';
$breadcrumbs = [
    ['label' => 'Verktyg', 'url' => '/admin/tools'],
    ['label' => 'Sök UCI-ID']
];
include __DIR__ . '/components/unified-layout.php';
?>


 

 <!-- Header -->
 <div class="flex justify-between items-center mb-lg">
 <div>
 <h1 class="">
  <i data-lucide="search"></i>
  Sök License Number (UCI-ID)
 </h1>
 <p class="text-secondary">
  Ladda upp CSV för att hitta och fylla i license numbers
 </p>
 </div>
 </div>

 <?php if ($message): ?>
 <div class="alert alert-<?= h($messageType) ?> mb-lg">
 <i data-lucide="<?= $messageType === 'success' ? 'check-circle' : 'alert-circle' ?>"></i>
 <?= h($message) ?>
 </div>
 <?php endif; ?>

 <!-- Upload Form -->
 <div class="card mb-lg">
 <div class="card-header">
 <h2 class="">
  <i data-lucide="upload"></i>
  Ladda upp CSV
 </h2>
 </div>
 <div class="card-body">
 <form method="POST" enctype="multipart/form-data">
  <?= csrf_field() ?>

  <div class="form-group mb-md">
  <label class="label">CSV-fil</label>
  <input type="file" name="csv_file" accept=".csv,.txt" class="input" required>
  <small class="text-secondary">
  CSV med kolumner för förnamn, efternamn, klubb och license number
  </small>
  </div>

  <p class="text-secondary mb-sm">Kolumnnummer (0 = första kolumnen):</p>
  <div class="grid grid-cols-2 gs-md-grid-cols-5 gap-md mb-md">
  <div class="form-group">
  <label class="label">Förnamn</label>
  <input type="number" name="col_firstname" value="0" min="0" class="input">
  </div>
  <div class="form-group">
  <label class="label">Efternamn</label>
  <input type="number" name="col_lastname" value="1" min="0" class="input">
  </div>
  <div class="form-group">
  <label class="label">Klubb</label>
  <input type="number" name="col_club" value="2" min="0" class="input">
  </div>
  <div class="form-group">
  <label class="label">Klass</label>
  <input type="number" name="col_class" value="3" min="0" class="input">
  </div>
  <div class="form-group">
  <label class="label">License</label>
  <input type="number" name="col_uci_id" value="4" min="0" class="input">
  </div>
  </div>

  <button type="submit" class="btn btn--primary">
  <i data-lucide="search"></i>
  Sök och fyll i License Numbers
  </button>
 </form>
 </div>
 </div>

 <?php if (!empty($results)): ?>
 <!-- Stats -->
 <div class="grid grid-cols-2 gs-md-grid-cols-4 gap-md mb-lg">
 <div class="card">
  <div class="card-body text-center">
  <div class="text-2xl text-success"><?= $matchStats['exact'] ?></div>
  <div class="text-sm text-secondary">Exakt match</div>
  </div>
 </div>
 <div class="card">
  <div class="card-body text-center">
  <div class="text-2xl text-warning"><?= $matchStats['fuzzy'] ?></div>
  <div class="text-sm text-secondary">Fuzzy match</div>
  </div>
 </div>
 <div class="card">
  <div class="card-body text-center">
  <div class="text-2xl gs-text-info"><?= $matchStats['partial'] ?></div>
  <div class="text-sm text-secondary">Delvis match</div>
  </div>
 </div>
 <div class="card">
  <div class="card-body text-center">
  <div class="text-2xl text-error"><?= $matchStats['not_found'] ?></div>
  <div class="text-sm text-secondary">Ej hittade</div>
  </div>
 </div>
 </div>

 <!-- Selection Controls & Export -->
 <div class="card mb-lg">
 <div class="card-body">
  <div class="flex flex-wrap gap-md items-center mb-md">
  <span class="text-sm text-secondary">Välj matchningar:</span>
  <button type="button" onclick="selectByType('all')" class="btn btn--secondary btn--sm">
  Alla
  </button>
  <button type="button" onclick="selectByType('none')" class="btn btn--secondary btn--sm">
  Inga
  </button>
  <button type="button" onclick="selectByType('exact')" class="btn btn-success btn--sm">
  Exakta
  </button>
  <button type="button" onclick="selectByType('fuzzy')" class="btn btn-warning btn--sm">
  Fuzzy
  </button>
  <button type="button" onclick="selectByType('partial')" class="btn btn-info btn--sm">
  Delvisa
  </button>
  <button type="button" onclick="selectByType('existing')" class="btn btn--secondary btn--sm">
  Befintliga
  </button>
  </div>
  <div class="flex gap-md items-center">
  <a href="?export=1" class="btn btn-success">
  <i data-lucide="download"></i>
  Ladda ner valda (<span id="selectedCount"><?= count($selectedRows) ?></span> rader)
  </a>
  <span class="text-sm text-secondary">
  Avmarkera rader du vill skippa i exporten
  </span>
  </div>
 </div>
 </div>

 <!-- Results Table -->
 <?php
 // Sort results by match type: partial first (needs review), then fuzzy, then exact last (no review needed)
 $sortOrder = ['partial' => 1, 'fuzzy' => 2, 'not_found' => 3, 'existing' => 4, 'exact' => 5];
 $sortedResults = $results;
 usort($sortedResults, function($a, $b) use ($sortOrder) {
   $orderA = $sortOrder[$a['match_type']] ?? 99;
   $orderB = $sortOrder[$b['match_type']] ?? 99;
   return $orderA - $orderB;
 });

 // Group results by match type for section headers
 $groupedResults = [];
 foreach ($sortedResults as $result) {
   $type = $result['match_type'];
   if (!isset($groupedResults[$type])) {
     $groupedResults[$type] = [];
   }
   $groupedResults[$type][] = $result;
 }

 $groupLabels = [
   'partial' => ['label' => 'GRANSKA: Delvisa matchningar', 'icon' => 'alert-triangle', 'color' => 'warning'],
   'fuzzy' => ['label' => 'GRANSKA: Fuzzy matchningar', 'icon' => 'help-circle', 'color' => 'info'],
   'not_found' => ['label' => 'Ej hittade', 'icon' => 'x-circle', 'color' => 'danger'],
   'existing' => ['label' => 'Befintliga (redan ifyllda)', 'icon' => 'database', 'color' => 'secondary'],
   'exact' => ['label' => 'OK: Exakta matchningar', 'icon' => 'check-circle', 'color' => 'success']
 ];
 ?>

 <div class="card">
 <div class="card-header">
  <h2 class="">
  <i data-lucide="list"></i>
  Resultat (<?= count($results) ?> rader)
  </h2>
 </div>
 <div class="card-body">
  <div class="table-responsive">
  <table class="table">
  <thead>
  <tr>
   <th style="width: 40px;">
   <input type="checkbox" id="selectAll" checked onchange="toggleAll(this.checked)">
   </th>
   <th>Namn</th>
   <th>Klubb</th>
   <th>Original License</th>
   <th>Hittad License</th>
   <th>Match</th>
  </tr>
  </thead>
  <tbody>
  <?php
  $displayOrder = ['partial', 'fuzzy', 'not_found', 'existing', 'exact'];
  foreach ($displayOrder as $groupType):
    if (!isset($groupedResults[$groupType]) || empty($groupedResults[$groupType])) continue;
    $groupInfo = $groupLabels[$groupType];
    $groupCount = count($groupedResults[$groupType]);
  ?>
  <!-- Group Header -->
  <tr class="group-header" style="background: var(--color-bg-sunken);">
    <td colspan="6" style="padding: var(--space-md); border-top: 2px solid var(--color-<?= $groupInfo['color'] ?>);">
      <div style="display: flex; align-items: center; gap: var(--space-sm);">
        <i data-lucide="<?= $groupInfo['icon'] ?>" style="color: var(--color-<?= $groupInfo['color'] ?>);"></i>
        <strong style="font-size: 1.1em;"><?= $groupInfo['label'] ?></strong>
        <span class="badge badge-<?= $groupInfo['color'] ?>"><?= $groupCount ?></span>
      </div>
    </td>
  </tr>
  <?php foreach ($groupedResults[$groupType] as $result): ?>
   <?php
   $rowClass = '';
   if ($result['match_type'] === 'not_found') {
   $rowClass = 'gs-bg-danger-light';
   }

   $badgeClass = 'badge-secondary';
   $matchLabel = 'Okänd';

   if ($result['match_type'] === 'exact') {
   $badgeClass = 'badge-success';
   $matchLabel = 'Exakt';
   } elseif ($result['match_type'] === 'fuzzy') {
   $badgeClass = 'badge-warning';
   $matchLabel = 'Fuzzy';
   } elseif ($result['match_type'] === 'partial') {
   $badgeClass = 'badge-info';
   $matchLabel = 'Delvis';
   } elseif ($result['match_type'] === 'existing') {
   $badgeClass = 'badge-secondary';
   $matchLabel = 'Befintlig';
   } elseif ($result['match_type'] === 'not_found') {
   $badgeClass = 'badge-danger';
   $matchLabel = 'Ej hittad';
   }

   // Find original index for selection tracking
   $rowIndex = array_search($result, $results);
   ?>
   <tr class="<?= $rowClass ?>" data-match-type="<?= h($result['match_type']) ?>">
   <td>
   <input type="checkbox"
    class="row-select"
    data-index="<?= $rowIndex ?>"
    <?= in_array($rowIndex, $selectedRows) ? 'checked' : '' ?>
    onchange="updateSelection()">
   </td>
   <td>
   <div style="font-size: 1.1em; font-weight: 600;"><?= h($result['firstname'] . ' ' . $result['lastname']) ?></div>
   <?php if ($result['found_name'] && $result['found_name'] !== $result['firstname'] . ' ' . $result['lastname']): ?>
   <div style="font-size: 1.15em; font-weight: 700; color: var(--color-success); margin-top: 4px;">
     <i data-lucide="arrow-right" style="width: 14px; height: 14px; display: inline;"></i>
     <?= h($result['found_name']) ?>
   </div>
   <?php endif; ?>
   </td>
   <td>
   <?= h($result['club']) ?>
   <?php if ($result['found_club'] && $result['found_club'] !== $result['club']): ?>
   <div style="color: var(--color-success); margin-top: 4px;">
     <i data-lucide="arrow-right" style="width: 12px; height: 12px; display: inline;"></i>
     <?= h($result['found_club']) ?>
   </div>
   <?php endif; ?>
   </td>
   <td>
   <?php if ($result['original_uci_id']): ?>
   <code><?= h($result['original_uci_id']) ?></code>
   <?php else: ?>
   <span class="text-secondary">-</span>
   <?php endif; ?>
   </td>
   <td>
   <?php if ($result['uci_id'] && $result['uci_id'] !== $result['original_uci_id']): ?>
   <code class="text-success" style="font-size: 1.05em; font-weight: 600;"><?= h($result['uci_id']) ?></code>
   <?php elseif ($result['uci_id']): ?>
   <code><?= h($result['uci_id']) ?></code>
   <?php else: ?>
   <span class="text-error">-</span>
   <?php endif; ?>
   </td>
   <td>
   <span class="badge <?= $badgeClass ?>">
   <?= $matchLabel ?>
   <?php if ($result['confidence']): ?>
    (<?= $result['confidence'] ?>%)
   <?php endif; ?>
   </span>
   </td>
   </tr>
  <?php endforeach; ?>
  <!-- Spacer after group -->
  <tr class="group-spacer"><td colspan="6" style="height: 20px; background: transparent; border: none;"></td></tr>
  <?php endforeach; ?>
  </tbody>
  </table>
  </div>
 </div>
 </div>
 <?php endif; ?>

 </div>


<?php if (!empty($results)): ?>
<script>
const csrfToken = '<?= htmlspecialchars(generate_csrf_token()) ?>';

function updateSelection() {
 const checkboxes = document.querySelectorAll('.row-select');
 const selected = [];

 checkboxes.forEach(cb => {
 if (cb.checked) {
 selected.push(parseInt(cb.dataset.index));
 }
 });

 // Update count display
 document.getElementById('selectedCount').textContent = selected.length;

 // Save to server
 fetch(window.location.pathname, {
 method: 'POST',
 headers: {'Content-Type': 'application/x-www-form-urlencoded'},
 body: 'action=update_selection&selected=' + encodeURIComponent(JSON.stringify(selected))
 });
}

function toggleAll(checked) {
 document.querySelectorAll('.row-select').forEach(cb => {
 cb.checked = checked;
 });
 updateSelection();
}

function selectByType(type) {
 const checkboxes = document.querySelectorAll('.row-select');

 checkboxes.forEach(cb => {
 const row = cb.closest('tr');
 const matchType = row.dataset.matchType;

 if (type === 'all') {
 cb.checked = true;
 } else if (type === 'none') {
 cb.checked = false;
 } else {
 cb.checked = (matchType === type);
 }
 });

 updateSelection();
}
</script>
<?php endif; ?>

<div class="container gs-py-sm">
 <small class="text-secondary">Search UCI-ID v1.3.0 [2025-11-22-004]</small>
</div>

<?php include __DIR__ . '/components/unified-layout-footer.php'; ?>
