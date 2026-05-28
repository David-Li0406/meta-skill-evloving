<?php
/**
 * Import Gravity ID for riders
 * Assigns unique Gravity IDs to platform members for discount benefits
 */
require_once __DIR__ . '/../config.php';
require_admin();

$db = getDB();
$message = '';
$messageType = '';
$results = [];
$stats = ['matched' => 0, 'updated' => 0, 'created' => 0, 'not_found' => 0, 'skipped' => 0];

// Handle template download
if (isset($_GET['template'])) {
 header('Content-Type: text/csv; charset=utf-8');
 header('Content-Disposition: attachment; filename="gravity_id_import_mall.csv"');

 $output = fopen('php://output', 'w');
 fprintf($output, chr(0xEF).chr(0xBB).chr(0xBF)); // UTF-8 BOM

 // Header row
 fputcsv($output, [
 'Gravity_ID',
 'Förnamn',
 'Efternamn',
 'UCI-ID',
 'E-post',
 'Födelseår',
 'Klubb'
 ], ';');

 // Example rows
 fputcsv($output, [
 'GRV-001',
 'Anna',
 'Andersson',
 '101 089 432 09',
 'anna@example.com',
 '1990',
 'Sundsvalls CK'
 ], ';');

 fputcsv($output, [
 'GRV-002',
 'Erik',
 'Eriksson',
 '',
 'erik@example.com',
 '1985',
 ''
 ], ';');

 fclose($output);
 exit;
}

// Handle CSV import
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
 }

 // Parse header
 $headers = str_getcsv(trim($lines[0]), $separator);
 $headers = array_map('trim', $headers);

 // Find column indices
 $colGravityId = findColumnIndex($headers, ['gravity_id', 'gravityid', 'grv_id', 'grvid']);
 $colFirstname = findColumnIndex($headers, ['förnamn', 'firstname', 'first_name']);
 $colLastname = findColumnIndex($headers, ['efternamn', 'lastname', 'last_name']);
 $colUciId = findColumnIndex($headers, ['uci-id', 'uciid', 'uci_id', 'licens', 'license']);
 $colEmail = findColumnIndex($headers, ['e-post', 'epost', 'email', 'mail']);
 $colBirthYear = findColumnIndex($headers, ['födelseår', 'birth_year', 'birthyear', 'år']);
 $colClub = findColumnIndex($headers, ['klubb', 'club', 'förening']);

 if ($colGravityId === false) {
 $message = 'Kolumnen Gravity_ID hittades inte i CSV-filen';
 $messageType = 'error';
 } else {
 // Process data rows
 for ($i = 1; $i < count($lines); $i++) {
 $line = trim($lines[$i]);
 if (empty($line)) continue;

 $parts = str_getcsv($line, $separator);

 $gravityId = trim($parts[$colGravityId] ?? '');
 $firstname = $colFirstname !== false ? trim($parts[$colFirstname] ?? '') : '';
 $lastname = $colLastname !== false ? trim($parts[$colLastname] ?? '') : '';
 $uciId = $colUciId !== false ? trim($parts[$colUciId] ?? '') : '';
 $email = $colEmail !== false ? trim($parts[$colEmail] ?? '') : '';
 $birthYear = $colBirthYear !== false ? trim($parts[$colBirthYear] ?? '') : '';
 $club = $colClub !== false ? trim($parts[$colClub] ?? '') : '';

 if (empty($gravityId)) {
  $stats['skipped']++;
  continue;
 }

 // Try to find matching rider
 $rider = null;
 $matchMethod = '';

 // 1. Try by UCI-ID (most reliable)
 if (!empty($uciId)) {
  $normalizedUci = preg_replace('/[^0-9]/', '', $uciId);
  $rider = $db->getRow(
 "SELECT id, firstname, lastname, license_number FROM riders
  WHERE REPLACE(REPLACE(license_number, ' ', ''), '-', '') = ?",
  [$normalizedUci]
  );
  if ($rider) $matchMethod = 'UCI-ID';
 }

 // 2. Try by email
 if (!$rider && !empty($email)) {
  $rider = $db->getRow(
 "SELECT id, firstname, lastname, license_number FROM riders WHERE email = ?",
  [$email]
  );
  if ($rider) $matchMethod = 'E-post';
 }

 // 3. Try by name + birth year
 if (!$rider && !empty($firstname) && !empty($lastname)) {
  $query ="SELECT id, firstname, lastname, license_number FROM riders
  WHERE LOWER(firstname) = LOWER(?) AND LOWER(lastname) = LOWER(?)";
  $params = [$firstname, $lastname];

  if (!empty($birthYear)) {
  $query .=" AND birth_year = ?";
  $params[] = $birthYear;
  }

  $rider = $db->getRow($query, $params);
  if ($rider) $matchMethod = 'Namn' . (!empty($birthYear) ? '+År' : '');
 }

 // 4. Try by name only (less reliable)
 if (!$rider && !empty($firstname) && !empty($lastname)) {
  $rider = $db->getRow(
 "SELECT id, firstname, lastname, license_number FROM riders
  WHERE LOWER(firstname) = LOWER(?) AND LOWER(lastname) = LOWER(?)",
  [$firstname, $lastname]
  );
  if ($rider) $matchMethod = 'Namn';
 }

 $result = [
  'gravity_id' => $gravityId,
  'input_name' => $firstname . ' ' . $lastname,
  'input_uci' => $uciId,
  'input_email' => $email,
  'match_method' => $matchMethod,
  'rider_id' => null,
  'rider_name' => '',
  'status' => 'not_found'
 ];

 if ($rider) {
  $result['rider_id'] = $rider['id'];
  $result['rider_name'] = $rider['firstname'] . ' ' . $rider['lastname'];

  // Update rider with Gravity ID
  $db->update('riders', [
  'gravity_id' => $gravityId,
  'gravity_id_since' => date('Y-m-d')
  ], 'id = ?', [$rider['id']]);

  $result['status'] = 'updated';
  $stats['matched']++;
  $stats['updated']++;
 } else {
  $stats['not_found']++;
 }

 $results[] = $result;
 }

 $message ="Import klar: {$stats['updated']} Gravity ID tilldelade, {$stats['not_found']} ej matchade, {$stats['skipped']} överhoppade";
 $messageType = $stats['not_found'] > 0 ? 'warning' : 'success';
 }
 }
}

/**
 * Find column index by possible names
 */
function findColumnIndex($headers, $names) {
 foreach ($headers as $i => $header) {
 $normalized = strtolower(trim($header));
 $normalized = str_replace([' ', '-', '_'], '', $normalized);
 foreach ($names as $name) {
 $nameNorm = str_replace([' ', '-', '_'], '', strtolower($name));
 if ($normalized === $nameNorm) {
 return $i;
 }
 }
 }
 return false;
}

// Get current Gravity ID stats
$gravityStats = $db->getRow("
 SELECT
 COUNT(CASE WHEN gravity_id IS NOT NULL THEN 1 END) as with_id,
 COUNT(*) as total
 FROM riders
");

$page_title = 'Importera Gravity ID';
$page_group = 'import';
include __DIR__ . '/components/unified-layout.php';
?>

 <?php if ($message): ?>
 <div class="alert alert--<?= h($messageType) ?> mb-lg">
 <i data-lucide="<?= $messageType === 'success' ? 'check-circle' : ($messageType === 'warning' ? 'alert-triangle' : 'alert-circle') ?>"></i>
 <?= h($message) ?>
 </div>
 <?php endif; ?>

 <!-- Stats -->
 <div class="grid grid-cols-2 gap-md mb-lg">
 <div class="card">
 <div class="card-body text-center">
  <div class="text-2xl text-primary"><?= $gravityStats['with_id'] ?? 0 ?></div>
  <div class="text-sm text-secondary">Deltagare med Gravity ID</div>
 </div>
 </div>
 <div class="card">
 <div class="card-body text-center">
  <div class="text-2xl text-secondary"><?= $gravityStats['total'] ?? 0 ?></div>
  <div class="text-sm text-secondary">Totalt antal deltagare</div>
 </div>
 </div>
 </div>

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
  <label class="label">CSV-fil med Gravity ID</label>
  <input type="file" name="csv_file" accept=".csv,.txt" class="input" required>
  <small class="text-secondary">
  Systemet matchar deltagare via UCI-ID, e-post eller namn+födelseår
  </small>
  </div>

  <div class="flex gap-md">
  <button type="submit" class="btn btn--primary">
  <i data-lucide="upload"></i>
  Importera Gravity ID
  </button>
  <a href="?template=1" class="btn btn--secondary">
  <i data-lucide="download"></i>
  Ladda ner mall
  </a>
  </div>
 </form>
 </div>
 </div>

 <!-- Matching Info -->
 <div class="card mb-lg">
 <div class="card-header">
 <h2 class="">
  <i data-lucide="info"></i>
  Matchningsordning
 </h2>
 </div>
 <div class="card-body">
 <ol class="text-sm">
  <li class="mb-sm"><strong>UCI-ID</strong> - Mest pålitligt, matchar på licensnummer</li>
  <li class="mb-sm"><strong>E-post</strong> - Matchar på e-postadress</li>
  <li class="mb-sm"><strong>Namn + Födelseår</strong> - Matchar på förnamn, efternamn och födelseår</li>
  <li><strong>Namn</strong> - Matchar endast på förnamn och efternamn (minst pålitligt)</li>
 </ol>
 </div>
 </div>

 <?php if (!empty($results)): ?>
 <!-- Results Table -->
 <div class="card">
 <div class="card-header">
  <h2 class="">
  <i data-lucide="list"></i>
  Importresultat (<?= count($results) ?> rader)
  </h2>
 </div>
 <div class="card-body">
  <div class="table-responsive">
  <table class="table">
  <thead>
  <tr>
   <th>Gravity ID</th>
   <th>Input</th>
   <th>Matchad deltagare</th>
   <th>Matchningsmetod</th>
   <th>Status</th>
  </tr>
  </thead>
  <tbody>
  <?php foreach ($results as $result): ?>
   <tr class="<?= $result['status'] === 'not_found' ? 'bg-error-light' : '' ?>">
   <td><code class="text-primary"><?= h($result['gravity_id']) ?></code></td>
   <td>
   <strong><?= h($result['input_name']) ?></strong>
   <?php if ($result['input_uci']): ?>
   <br><small class="text-secondary">UCI: <?= h($result['input_uci']) ?></small>
   <?php endif; ?>
   <?php if ($result['input_email']): ?>
   <br><small class="text-secondary"><?= h($result['input_email']) ?></small>
   <?php endif; ?>
   </td>
   <td>
   <?php if ($result['rider_id']): ?>
   <a href="/rider.php?id=<?= $result['rider_id'] ?>" target="_blank">
    <?= h($result['rider_name']) ?>
   </a>
   <?php else: ?>
   <span class="text-error">Ej hittad</span>
   <?php endif; ?>
   </td>
   <td>
   <?php if ($result['match_method']): ?>
   <span class="badge badge--primary"><?= h($result['match_method']) ?></span>
   <?php else: ?>
   -
   <?php endif; ?>
   </td>
   <td>
   <?php if ($result['status'] === 'updated'): ?>
   <span class="badge badge--success">Tilldelad</span>
   <?php else: ?>
   <span class="badge badge--error">Ej matchad</span>
   <?php endif; ?>
   </td>
   </tr>
  <?php endforeach; ?>
  </tbody>
  </table>
  </div>
 </div>
 </div>
 <?php endif; ?>

<?php include __DIR__ . '/components/unified-layout-footer.php'; ?>
