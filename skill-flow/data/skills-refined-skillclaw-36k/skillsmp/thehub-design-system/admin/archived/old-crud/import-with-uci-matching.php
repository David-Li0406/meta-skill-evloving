<?php
/**
 * IMPORT PREPROCESSOR: Matcha UCI-ID från databasen
 * 
 * Innan resultat importeras, kontrollera om ridarna finns i databasen
 * och fyll i UCI-ID baserat på namn + klubb
 * 
 * Flöde:
 * 1. Admin laddar upp CSV med resultat
 * 2. Vi parsar CSV och letar efter ridaren i DB via namn + klubb
 * 3. Vi fyller i UCI-ID från DB
 * 4. Vi visar matchningar för granskning
 * 5. Admin godkänner innan import
 */

require_once __DIR__ . '/../config.php';
require_admin();

$db = getDB();
$message = '';
$messageType = 'info';

// ============================================
// HELP-FUNKTIONER
// ============================================

function normalizeForMatch($str) {
 return mb_strtolower(trim($str), 'UTF-8');
}

function stringSimilarity($str1, $str2) {
 $norm1 = normalizeForMatch($str1);
 $norm2 = normalizeForMatch($str2);
 if ($norm1 === $norm2) return 100;
 
 $distance = levenshtein($norm1, $norm2);
 $maxLen = max(strlen($norm1), strlen($norm2));
 return max(0, 100 - ($distance / $maxLen * 100));
}

/**
 * Hitta matchande rider i databasen
 * Baserat på: förnamn + efternamn + klubb
 */
function findRiderInDatabase($db, $firstName, $lastName, $club = null, $riderClass = null) {
 // Sök efter rider med liknande namn
 $riders = $db->getAll("
 SELECT r.id, r.firstname, r.lastname, r.license_number
 FROM riders r
 WHERE r.firstname IS NOT NULL
 ORDER BY r.id
");
 
 $candidates = [];
 
 foreach ($riders as $rider) {
 // Score för namn-matchning
 $fnameSimilarity = stringSimilarity($firstName, $rider['firstname']);
 $lnameSimilarity = stringSimilarity($lastName, $rider['lastname']);
 
 // Båda namn måste matcha > 80%
 if ($fnameSimilarity >= 80 && $lnameSimilarity >= 80) {
 $score = ($fnameSimilarity + $lnameSimilarity) / 2;
 
 // Bonus om klubb matchar
 if ($club) {
 $riderClubs = $db->getAll("
 SELECT DISTINCT c.name
 FROM results r
 JOIN events e ON r.event_id = e.id
 JOIN clubs c ON e.club_id = c.id
 WHERE r.cyclist_id = ?
", [$rider['id']]);
 
 foreach ($riderClubs as $riderClub) {
 if (stringSimilarity($club, $riderClub['name']) >= 80) {
 $score += 10; // Bonus för klubb-match
 }
 }
 }
 
 // Bonus om klass matchar
 if ($riderClass) {
 $riderClasses = $db->getAll("
 SELECT DISTINCT c.name
 FROM results r
 LEFT JOIN classes c ON r.class_id = c.id
 WHERE r.cyclist_id = ? AND c.name IS NOT NULL
", [$rider['id']]);
 
 foreach ($riderClasses as $rc) {
 if (stringSimilarity($riderClass, $rc['name']) >= 80) {
 $score += 10; // Bonus för klass-match
 }
 }
 }
 
 $candidates[] = [
 'rider_id' => $rider['id'],
 'rider_name' => $rider['firstname'] . ' ' . $rider['lastname'],
 'uci_id' => $rider['license_number'],
 'score' => $score,
 'fname_similarity' => $fnameSimilarity,
 'lname_similarity' => $lnameSimilarity
 ];
 }
 }
 
 // Sortera efter score
 usort($candidates, fn($a, $b) => $b['score'] <=> $a['score']);
 
 // Returnera bästa match om score > 85
 if (!empty($candidates) && $candidates[0]['score'] >= 85) {
 return $candidates[0];
 }
 
 return null;
}

// ============================================
// ADMIN GUI
// ============================================

$pageTitle = 'Import med UCI-ID Matching';
$pageType = 'admin';
include __DIR__ . '/../includes/layout-header.php';
?>

<main class="main-content">
 <div class="container">
 <h1 class="text-primary mb-lg">
 <i data-lucide="upload"></i>
 Import med UCI-ID Matching
 </h1>

 <p class="text-secondary mb-lg">
 Denna sida låter dig ladda upp en resultat-CSV och automatiskt matcha deltagarna 
 mot databasen för att fylla i UCI-ID:n.
 </p>

 <!-- Upload Form -->
 <div class="card mb-lg">
 <div class="card-header">
 <h2 class="text-primary">
  <i data-lucide="file-up"></i>
  1. Ladda upp CSV
 </h2>
 </div>
 <div class="card-body">
 <form method="POST" enctype="multipart/form-data" id="uploadForm">
  <?= csrf_field() ?>
  
  <div class="mb-md">
  <label class="label">CSV-fil med resultat</label>
  <input type="file" name="csv_file" class="input" accept=".csv" required>
  <p class="text-xs text-secondary mt-sm">
  Förväntade kolumner: Förnamn, Efternamn, Klubb (optional), Tävlingsklass (optional)
  </p>
  </div>
  
  <button type="submit" name="preview" class="btn btn--primary">
  <i data-lucide="search"></i>
  Förhandsgranska & Matcha
  </button>
 </form>
 </div>
 </div>

 <!-- Preview & Matching Results -->
 <?php
 if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['preview'])) {
 if (isset($_FILES['csv_file']) && $_FILES['csv_file']['size'] > 0) {
 try {
  $csvPath = $_FILES['csv_file']['tmp_name'];
  $csvContent = file_get_contents($csvPath);
  $rows = array_filter(array_map('str_getcsv', explode("\n", $csvContent)));
  
  if (count($rows) < 2) {
  throw new Exception('CSV-filen är tom eller har bara rubrik');
  }
  
  // Anta att första raden är rubrik
  $header = array_map('trim', $rows[0]);
  $dataRows = array_slice($rows, 1);
  
  echo '<div class="card mb-lg">';
  echo '<div class="card-header">';
  echo '<h2 class="text-primary">';
  echo '<i data-lucide="check-circle"></i>';
  echo '2. Matchning-resultat (' . count($dataRows) . ' rader)';
  echo '</h2>';
  echo '</div>';
  echo '<div class="card-body">';
  
  $matches = [];
  $unmatched = [];
  
  foreach ($dataRows as $idx => $row) {
  $rowData = array_combine($header, $row);
  
  $firstName = $rowData['Förnamn'] ?? $rowData['firstname'] ?? '';
  $lastName = $rowData['Efternamn'] ?? $rowData['lastname'] ?? '';
  $club = $rowData['Klubb'] ?? $rowData['club'] ?? null;
  $class = $rowData['Tävlingsklass'] ?? $rowData['class'] ?? null;
  
  $match = findRiderInDatabase($db, $firstName, $lastName, $club, $class);
  
  if ($match) {
  $matches[] = [
  'row_num' => $idx + 2,
  'input_name' => $firstName . ' ' . $lastName,
  'input_club' => $club,
  'input_class' => $class,
  'matched_name' => $match['rider_name'],
  'matched_uci' => $match['uci_id'],
  'matched_id' => $match['rider_id'],
  'score' => $match['score'],
  'fname_sim' => round($match['fname_similarity'], 0),
  'lname_sim' => round($match['lname_similarity'], 0)
  ];
  } else {
  $unmatched[] = [
  'row_num' => $idx + 2,
  'name' => $firstName . ' ' . $lastName,
  'club' => $club,
  'class' => $class
  ];
  }
  }
  
  // Visa matchade
  echo '<h3 class="text-success mb-md">';
  echo '<i data-lucide="check"></i> Matchade (' . count($matches) . ')';
  echo '</h3>';
  
  if (!empty($matches)) {
  echo '<div class="gs-overflow-x-auto mb-lg">';
  echo '<table class="table table-sm">';
  echo '<thead><tr>';
  echo '<th>Rad</th>';
  echo '<th>Från CSV</th>';
  echo '<th>Match i DB</th>';
  echo '<th>UCI-ID</th>';
  echo '<th>Score</th>';
  echo '</tr></thead>';
  echo '<tbody>';
  
  foreach ($matches as $m) {
  echo '<tr>';
  echo '<td>' . $m['row_num'] . '</td>';
  echo '<td><strong>' . h($m['input_name']) . '</strong><br><span class="text-xs">' . ($m['input_class'] ? h($m['input_class']) : '-') . '</span></td>';
  echo '<td><a href="/rider.php?id=' . $m['matched_id'] . '" target="_blank">' . h($m['matched_name']) . '</a></td>';
  echo '<td><code>' . h($m['matched_uci']) . '</code></td>';
  echo '<td><span class="badge badge-success">' . round($m['score'], 0) . '%</span></td>';
  echo '</tr>';
  }
  
  echo '</tbody></table>';
  echo '</div>';
  }
  
  // Visa omatched
  if (!empty($unmatched)) {
  echo '<h3 class="text-warning mb-md">';
  echo '<i data-lucide="alert-circle"></i> OMATCHED (' . count($unmatched) . ' - Måste skapas manuellt)';
  echo '</h3>';
  
  echo '<div class="gs-overflow-x-auto">';
  echo '<table class="table table-sm">';
  echo '<thead><tr>';
  echo '<th>Rad</th>';
  echo '<th>Namn</th>';
  echo '<th>Klubb</th>';
  echo '<th>Klass</th>';
  echo '</tr></thead>';
  echo '<tbody>';
  
  foreach ($unmatched as $u) {
  echo '<tr style="background-color: #fff5f5;">';
  echo '<td>' . $u['row_num'] . '</td>';
  echo '<td><strong>' . h($u['name']) . '</strong></td>';
  echo '<td>' . ($u['club'] ? h($u['club']) : '-') . '</td>';
  echo '<td>' . ($u['class'] ? h($u['class']) : '-') . '</td>';
  echo '</tr>';
  }
  
  echo '</tbody></table>';
  echo '</div>';
  }
  
  echo '<p class="text-xs text-secondary mt-md">';
  echo 'Matchning använder: Förnamn (>80%), Efternamn (>80%), Klubb (bonus), Tävlingsklass (bonus)';
  echo '</p>';
  echo '</div></div>';
  
 } catch (Exception $e) {
  echo '<div class="alert alert--error mb-lg">';
  echo '<strong>Fel:</strong> ' . h($e->getMessage());
  echo '</div>';
 }
 }
 }
 ?>

 <div class="mt-lg">
 <a href="/admin/import.php" class="btn btn--secondary">
 <i data-lucide="arrow-left"></i>
 Tillbaka till import
 </a>
 </div>
 </div>
</main>

<?php include __DIR__ . '/../includes/layout-footer.php'; ?>
