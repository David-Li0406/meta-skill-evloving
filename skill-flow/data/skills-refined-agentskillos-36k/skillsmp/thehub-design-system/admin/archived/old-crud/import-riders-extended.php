<?php
/**
 * Extended Rider Import - Full Personal Data
 *
 * This import function handles complete rider data including private information:
 * - Personnummer
 * - Address (street, postal code, city, country)
 * - Phone and emergency contact
 * - District and team
 * - Multiple disciplines
 * - License information
 *
 * PRIVACY: This data is STRICTLY CONFIDENTIAL and must only be used for:
 * - Creating rider profiles
 * - Auto-filling registration forms
 * - Internal administration
 *
 * NEVER expose private fields publicly!
 */

// CRITICAL: Show ALL errors for debugging
error_reporting(E_ALL);
ini_set('display_errors', 1);
ini_set('log_errors', 1);

// Try to catch fatal errors
register_shutdown_function(function() {
 $error = error_get_last();
 if ($error !== null && in_array($error['type'], [E_ERROR, E_PARSE, E_CORE_ERROR, E_COMPILE_ERROR])) {
 echo"<h1>Fatal Error Detected:</h1>";
 echo"<pre class='gs-error-display'>";
 echo"Type:" . $error['type'] ."\n";
 echo"Message:" . htmlspecialchars($error['message']) ."\n";
 echo"File:" . $error['file'] ."\n";
 echo"Line:" . $error['line'];
 echo"</pre>";
 }
});

require_once __DIR__ . '/../config.php';
require_once __DIR__ . '/../includes/helpers.php';
require_admin();
require_once __DIR__ . '/../includes/admin-layout.php';

$db = getDB();
$current_admin = get_current_admin();

$message = '';
$messageType = 'info';
$stats = null;
$errors = [];
$skippedRows = [];

// Handle CSV/Excel upload
if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_FILES['import_file'])) {
 // Validate CSRF token
 checkCsrf();

 $file = $_FILES['import_file'];

 // Validate file
 if ($file['error'] !== UPLOAD_ERR_OK) {
 $message = 'Filuppladdning misslyckades';
 $messageType = 'error';
 } elseif ($file['size'] > MAX_UPLOAD_SIZE) {
 $message = 'Filen är för stor (max ' . (MAX_UPLOAD_SIZE / 1024 / 1024) . 'MB)';
 $messageType = 'error';
 } else {
 $extension = strtolower(pathinfo($file['name'], PATHINFO_EXTENSION));

 if (!in_array($extension, ['csv', 'xlsx', 'xls'])) {
 $message = 'Ogiltigt filformat. Tillåtna: CSV, XLSX, XLS';
 $messageType = 'error';
 } else {
 // Process the file
 $uploaded = UPLOADS_PATH . '/' . time() . '_' . basename($file['name']);

 if (move_uploaded_file($file['tmp_name'], $uploaded)) {
 try {
  // Parse CSV
  if ($extension === 'csv') {
  $result = importRidersExtendedFromCSV($uploaded, $db);
  } else {
  $message = 'Excel-filer stöds inte än. Använd CSV-format istället.';
  $messageType = 'warning';
  @unlink($uploaded);
  goto skip_import;
  }

  $stats = $result['stats'];
  $errors = $result['errors'];
  $skippedRows = $result['skipped_rows'] ?? [];

  if ($stats['success'] > 0 || $stats['updated'] > 0) {
  $message ="Import klar! {$stats['success']} nya, {$stats['updated']} uppdaterade.";
  if ($stats['duplicates'] > 0) {
  $message .=" {$stats['duplicates']} dubletter borttagna.";
  }
  $messageType = 'success';
  } else {
  $message ="Ingen data importerades. Kontrollera filformatet.";
  $messageType = 'error';
  }

 } catch (Exception $e) {
  $message = 'Import misslyckades: ' . $e->getMessage();
  $messageType = 'error';
 }

 @unlink($uploaded);
 } else {
 $message = 'Kunde inte ladda upp filen';
 $messageType = 'error';
 }
 }
 }

 skip_import:
}

/**
 * Import riders from CSV file with extended fields
 */
function importRidersExtendedFromCSV($filepath, $db) {
 $stats = [
 'total' => 0,
 'success' => 0,
 'updated' => 0,
 'skipped' => 0,
 'failed' => 0,
 'duplicates' => 0
 ];
 $errors = [];
 $skippedRows = [];
 $seenInThisImport = [];

 if (($handle = fopen($filepath, 'r')) === false) {
 throw new Exception('Kunde inte öppna filen');
 }

 // Auto-detect delimiter (comma, semicolon, or tab)
 $firstLine = fgets($handle);
 rewind($handle);

 $delimiter = ','; // default
 if (substr_count($firstLine, ';') > substr_count($firstLine, ',')) {
 $delimiter = ';';
 } elseif (substr_count($firstLine,"\t") > substr_count($firstLine, ',')) {
 $delimiter ="\t";
 }

 // Read header row
 $header = fgetcsv($handle, 10000, $delimiter);

 if (!$header) {
 fclose($handle);
 throw new Exception('Tom fil eller ogiltigt format');
 }

 // Normalize header - map Swedish/English variants to standard names
 $header = array_map(function($col) {
 $col = strtolower(trim($col));
 $col = str_replace([' ', '-', '_'], '', $col); // Remove spaces, hyphens, underscores
 $col = str_replace(['å', 'ä', 'ö'], ['a', 'a', 'o'], $col); // Normalize Swedish chars

 // Comprehensive mapping
 $mappings = [
 // Name fields
 'fornamn' => 'firstname',
 'fornman' => 'firstname',
 'firstname' => 'firstname',
 'fname' => 'firstname',

 'efternamn' => 'lastname',
 'lastname' => 'lastname',
 'surname' => 'lastname',

 // Birth info
 'fodelsedatum' => 'personnummer',
 'fodelsedato' => 'personnummer',
 'personnummer' => 'personnummer',
 'pnr' => 'personnummer',
 'ssn' => 'personnummer',
 'dateofbirth' => 'personnummer',

 'fodelsear' => 'birthyear',
 'birthyear' => 'birthyear',

 // Gender
 'kon' => 'gender',
 'gender' => 'gender',
 'sex' => 'gender',

 // Address
 'postadress' => 'address',
 'adress' => 'address',
 'address' => 'address',
 'streetaddress' => 'address',

 'postnummer' => 'postalcode',
 'postalcode' => 'postalcode',
 'zipcode' => 'postalcode',
 'zip' => 'postalcode',

 'ort' => 'city',
 'stad' => 'city',
 'city' => 'city',

 'land' => 'country',
 'country' => 'country',

 // Contact
 'epost' => 'email',
 'epostadress' => 'email',
 'email' => 'email',
 'mail' => 'email',

 'telefon' => 'phone',
 'phone' => 'phone',
 'tel' => 'phone',
 'mobile' => 'phone',

 'emergencycontact' => 'emergencycontact',
 'nodkontakt' => 'emergencycontact',
 'nodnummer' => 'emergencycontact',

 // Organization
 'distrikt' => 'district',
 'district' => 'district',
 'region' => 'district',

 'huvudforening' => 'club',
 'huvudforningen' => 'club',
 'klubb' => 'club',
 'club' => 'club',
 'klubbnamn' => 'club',

 'team' => 'team',
 'lag' => 'team',

 // Disciplines
 'road' => 'road',
 'landsväg' => 'road',
 'landsvag' => 'road',

 'track' => 'track',
 'bana' => 'track',

 'bmx' => 'bmx',

 'cx' => 'cx',
 'cyclocross' => 'cx',

 'trial' => 'trial',

 'para' => 'para',

 'mtb' => 'mtb',
 'mountainbike' => 'mtb',

 'ecycling' => 'ecycling',

 'gravel' => 'gravel',

 // License
 'kategori' => 'category',
 'category' => 'category',

 'licenstyp' => 'licensetype',
 'licensetype' => 'licensetype',

 'licensar' => 'licenseyear',
 'licenseyear' => 'licenseyear',

 'ucikod' => 'ucicode',
 'ucicode' => 'ucicode',
 'uciid' => 'ucicode',
 ];

 return $mappings[$col] ?? $col;
 }, $header);

 // Cache for club lookups
 $clubCache = [];

 $lineNumber = 1;

 while (($row = fgetcsv($handle, 10000, $delimiter)) !== false) {
 $lineNumber++;
 $stats['total']++;

 // Skip empty rows
 if (empty(array_filter($row))) {
 continue;
 }

 // Map row to associative array
 $data = array_combine($header, $row);

 // Validate required fields
 if (empty($data['firstname']) || empty($data['lastname'])) {
 $stats['skipped']++;
 $errors[] ="Rad {$lineNumber}: Saknar förnamn eller efternamn";
 $skippedRows[] = [
 'row' => $lineNumber,
 'name' => trim(($data['firstname'] ?? '') . ' ' . ($data['lastname'] ?? '')),
 'reason' => 'Saknar förnamn eller efternamn',
 'type' => 'missing_fields'
 ];
 continue;
 }

 try {
 // Parse personnummer to extract birth year
 $birthYear = null;
 $personnummer = null;

 if (!empty($data['personnummer'])) {
 $personnummerRaw = trim($data['personnummer']);
 // Try to extract birth year from personnummer (YYYYMMDD-XXXX or YYMMDD-XXXX)
 if (preg_match('/^(\d{4})(\d{2})(\d{2})/', $personnummerRaw, $matches)) {
  $birthYear = (int)$matches[1];
  $personnummer = $personnummerRaw;
 } elseif (preg_match('/^(\d{2})(\d{2})(\d{2})/', $personnummerRaw, $matches)) {
  $year = (int)$matches[1];
  $birthYear = ($year > 25) ? (1900 + $year) : (2000 + $year);
  $personnummer = $personnummerRaw;
 }
 }

 // Fall back to birthyear column
 if (!$birthYear && !empty($data['birthyear'])) {
 $birthYear = (int)$data['birthyear'];
 }

 // Normalize gender
 $genderRaw = strtolower(trim($data['gender'] ?? 'M'));
 if (in_array($genderRaw, ['woman', 'female', 'kvinna', 'dam', 'f', 'k'])) {
 $gender = 'F';
 } elseif (in_array($genderRaw, ['man', 'male', 'herr', 'm'])) {
 $gender = 'M';
 } else {
 $gender = 'M'; // Default
 }

 // Prepare rider data
 $riderData = [
 'firstname' => trim($data['firstname']),
 'lastname' => trim($data['lastname']),
 'birth_year' => $birthYear,
 'personnummer' => $personnummer,
 'gender' => $gender,

 // Address
 'address' => !empty($data['address']) ? trim($data['address']) : null,
 'postal_code' => !empty($data['postalcode']) ? trim($data['postalcode']) : null,
 'city' => !empty($data['city']) ? trim($data['city']) : null,
 'country' => !empty($data['country']) ? trim($data['country']) : 'Sverige',

 // Contact
 'email' => !empty($data['email']) ? trim($data['email']) : null,
 'phone' => !empty($data['phone']) ? trim($data['phone']) : null,
 'emergency_contact' => !empty($data['emergencycontact']) ? trim($data['emergencycontact']) : null,

 // Organization
 'district' => !empty($data['district']) ? trim($data['district']) : null,
 'team' => !empty($data['team']) ? trim($data['team']) : null,

 // License
 'license_number' => !empty($data['ucicode']) ? trim($data['ucicode']) : null,
 'license_type' => !empty($data['licensetype']) ? trim($data['licensetype']) : null,
 'license_category' => !empty($data['category']) ? trim($data['category']) : null,
 'license_year' => !empty($data['licenseyear']) ? (int)$data['licenseyear'] : null,

 'active' => 1
 ];

 // Build disciplines JSON array
 $disciplines = [];
 $disciplineFields = ['road', 'track', 'bmx', 'cx', 'trial', 'para', 'mtb', 'ecycling', 'gravel'];
 foreach ($disciplineFields as $disc) {
 if (!empty($data[$disc]) && strtolower(trim($data[$disc])) !== '') {
  $value = strtolower(trim($data[$disc]));
  // Consider any non-empty value as active
  if ($value !== '0' && $value !== 'no' && $value !== 'nej') {
  $disciplines[] = ucfirst($disc);
  }
 }
 }

 if (!empty($disciplines)) {
 $riderData['disciplines'] = json_encode($disciplines);
 } else {
 $riderData['disciplines'] = null;
 }

 // Handle club - fuzzy matching
 if (!empty($data['club'])) {
 $clubName = trim($data['club']);

 if (isset($clubCache[$clubName])) {
  $riderData['club_id'] = $clubCache[$clubName];
 } else {
  $club = $db->getRow("SELECT id FROM clubs WHERE name = ? LIMIT 1", [$clubName]);

  if (!$club) {
  $club = $db->getRow("SELECT id FROM clubs WHERE name LIKE ? LIMIT 1", ['%' . $clubName . '%']);
  }

  if (!$club) {
  $clubId = $db->insert('clubs', ['name' => $clubName, 'active' => 1]);
  $clubCache[$clubName] = $clubId;
  $riderData['club_id'] = $clubId;
  } else {
  $clubCache[$clubName] = $club['id'];
  $riderData['club_id'] = $club['id'];
  }
 }
 } else {
 $riderData['club_id'] = null;
 }

 // Check for duplicates within this import
 $uniqueKey = '';
 if ($riderData['license_number']) {
 $uniqueKey = 'lic_' . strtolower(trim($riderData['license_number']));
 } elseif ($personnummer) {
 $uniqueKey = 'pnr_' . $personnummer;
 } else {
 $uniqueKey = 'name_' . strtolower(trim($riderData['firstname'])) . '_' .
  strtolower(trim($riderData['lastname'])) . '_' .
  ($birthYear ?? '0');
 }

 if (isset($seenInThisImport[$uniqueKey])) {
 $stats['duplicates']++;
 $stats['skipped']++;
 $skippedRows[] = [
  'row' => $lineNumber,
  'name' => $riderData['firstname'] . ' ' . $riderData['lastname'],
  'license' => $riderData['license_number'] ?? '-',
  'reason' => 'Dublett (redan i denna import)',
  'type' => 'duplicate'
 ];
 continue;
 }

 $seenInThisImport[$uniqueKey] = true;

 // Check if rider already exists
 $existing = null;

 if ($riderData['license_number']) {
 $existing = $db->getRow(
 "SELECT id FROM riders WHERE license_number = ? LIMIT 1",
  [$riderData['license_number']]
 );
 }

 if (!$existing && $personnummer) {
 $existing = $db->getRow(
 "SELECT id FROM riders WHERE personnummer = ? LIMIT 1",
  [$personnummer]
 );
 }

 if (!$existing && $birthYear) {
 $existing = $db->getRow(
 "SELECT id FROM riders WHERE firstname = ? AND lastname = ? AND birth_year = ? LIMIT 1",
  [$riderData['firstname'], $riderData['lastname'], $birthYear]
 );
 }

 if ($existing) {
 // Update existing rider
 $db->update('riders', $riderData, 'id = ?', [$existing['id']]);
 $stats['updated']++;
 } else {
 // Insert new rider
 $newId = $db->insert('riders', $riderData);
 $stats['success']++;
 }

 } catch (Exception $e) {
 $stats['failed']++;
 $errors[] ="Rad {$lineNumber}:" . $e->getMessage();
 $skippedRows[] = [
 'row' => $lineNumber,
 'name' => trim(($data['firstname'] ?? '') . ' ' . ($data['lastname'] ?? '')),
 'license' => $data['ucicode'] ?? '-',
 'reason' => 'Fel: ' . $e->getMessage(),
 'type' => 'error'
 ];
 }
 }

 fclose($handle);

 return [
 'stats' => $stats,
 'errors' => $errors,
 'skipped_rows' => $skippedRows
 ];
}

$pageTitle = 'Importera Deltagare (Utökad)';
$pageType = 'admin';
include __DIR__ . '/../includes/layout-header.php';
?>

<main class="main-content">
 <div class="container">
 <?php render_admin_header('Import & Data'); ?>

 <!-- Privacy Warning -->
 <div class="alert alert--warning mb-lg alert-border-danger">
 <i data-lucide="shield-alert"></i>
 <strong>SEKRETESS:</strong> Denna import hanterar känslig persondata (personnummer, adress, telefon, nödkontakt).
 Data får ENDAST användas för:
 <ul class="gs-list-ml-1-5">
 <li>Skapa deltagarprofiler</li>
 <li>Autofylla formulär vid bokning</li>
 <li>Intern administration</li>
 </ul>
 Känslig data får ALDRIG visas publikt!
 </div>

 <!-- Message -->
 <?php if ($message): ?>
 <div class="alert alert-<?= h($messageType) ?> mb-lg">
 <i data-lucide="<?= $messageType === 'success' ? 'check-circle' : 'alert-circle' ?>"></i>
 <?= h($message) ?>
 </div>
 <?php endif; ?>

 <!-- Statistics -->
 <?php if ($stats): ?>
 <div class="card mb-lg">
 <div class="card-header">
  <h2 class="text-primary">
  <i data-lucide="bar-chart"></i>
  Import-statistik
  </h2>
 </div>
 <div class="card-body">
  <div class="grid grid-cols-2 gs-md-grid-cols-5 gap-md">
  <div class="stat-card">
  <i data-lucide="file-text" class="icon-lg text-primary mb-sm"></i>
  <div class="stat-number"><?= number_format($stats['total']) ?></div>
  <div class="stat-label">Totalt rader</div>
  </div>
  <div class="stat-card">
  <i data-lucide="check-circle" class="icon-lg text-success mb-sm"></i>
  <div class="stat-number"><?= number_format($stats['success']) ?></div>
  <div class="stat-label">Nya</div>
  </div>
  <div class="stat-card">
  <i data-lucide="refresh-cw" class="icon-lg text-accent mb-sm"></i>
  <div class="stat-number"><?= number_format($stats['updated']) ?></div>
  <div class="stat-label">Uppdaterade</div>
  </div>
  <div class="stat-card">
  <i data-lucide="minus-circle" class="icon-lg text-secondary mb-sm"></i>
  <div class="stat-number"><?= number_format($stats['skipped']) ?></div>
  <div class="stat-label">Överhoppade</div>
  </div>
  <div class="stat-card">
  <i data-lucide="x-circle" class="icon-lg text-error mb-sm"></i>
  <div class="stat-number"><?= number_format($stats['failed']) ?></div>
  <div class="stat-label">Misslyckade</div>
  </div>
  </div>

  <!-- Skipped Rows Details -->
  <?php if (!empty($skippedRows)): ?>
  <div class="mt-lg section-divider-top">
  <h3 class="text-warning mb-md">
  <i data-lucide="alert-circle"></i>
  Överhoppade rader (<?= count($skippedRows) ?>)
  </h3>
  <div class="gs-scroll-container-400">
  <table class="table table-sm">
   <thead>
   <tr>
   <th>Rad</th>
   <th>Namn</th>
   <th>Licens</th>
   <th>Anledning</th>
   <th>Typ</th>
   </tr>
   </thead>
   <tbody>
   <?php foreach (array_slice($skippedRows, 0, 100) as $skip): ?>
   <tr>
   <td><code><?= $skip['row'] ?></code></td>
   <td><?= h($skip['name']) ?></td>
   <td><?= h($skip['license'] ?? '-') ?></td>
   <td><?= h($skip['reason']) ?></td>
   <td>
    <?php if ($skip['type'] === 'duplicate'): ?>
    <span class="badge badge-warning text-xs">Dublett</span>
    <?php elseif ($skip['type'] === 'missing_fields'): ?>
    <span class="badge badge-secondary text-xs">Saknar fält</span>
    <?php elseif ($skip['type'] === 'error'): ?>
    <span class="badge badge-danger text-xs">Fel</span>
    <?php endif; ?>
   </td>
   </tr>
   <?php endforeach; ?>
   </tbody>
  </table>
  </div>
  </div>
  <?php endif; ?>
 </div>
 </div>
 <?php endif; ?>

 <!-- Upload Form -->
 <div class="card mb-lg">
 <div class="card-header">
 <h2 class="text-primary">
  <i data-lucide="upload"></i>
  Ladda upp CSV-fil
 </h2>
 </div>
 <div class="card-body">
 <form method="POST" enctype="multipart/form-data" id="uploadForm" class="gs-form-max-width-600">
  <?= csrf_field() ?>

  <div class="form-group">
  <label for="import_file" class="label">
  <i data-lucide="file"></i>
  Välj CSV-fil
  </label>
  <input
  type="file"
  id="import_file"
  name="import_file"
  class="input"
  accept=".csv"
  required
  >
  <small class="text-secondary text-sm">
  Max storlek: <?= round(MAX_UPLOAD_SIZE / 1024 / 1024) ?>MB. Endast CSV-filer.
  </small>
  </div>

  <button type="submit" class="btn btn--primary btn-lg">
  <i data-lucide="upload"></i>
  Importera
  </button>
 </form>
 </div>
 </div>

 <!-- File Format Guide -->
 <div class="card">
 <div class="card-header">
 <h2 class="text-primary">
  <i data-lucide="info"></i>
  CSV-filformat (Utökad Mall)
 </h2>
 </div>
 <div class="card-body">
 <p class="text-secondary mb-md">
  CSV-filen ska ha följande kolumner (kolumnnamn kan vara på svenska eller engelska):
 </p>

 <div class="table-responsive">
  <table class="table table-sm">
  <thead>
  <tr>
  <th>Kolumn</th>
  <th>Obligatorisk</th>
  <th>Beskrivning</th>
  <th>Exempel</th>
  </tr>
  </thead>
  <tbody>
  <tr class="table-section-yellow">
  <td colspan="4"><strong>Grunddata</strong></td>
  </tr>
  <tr>
  <td><code>Födelsedatum</code></td>
  <td><span class="badge badge-warning">Rekommenderat</span></td>
  <td>Personnummer (YYYYMMDD-XXXX)</td>
  <td>19400525-0651</td>
  </tr>
  <tr>
  <td><code>Förnamn</code></td>
  <td><span class="badge badge-danger">Ja</span></td>
  <td>Förnamn</td>
  <td>Lars</td>
  </tr>
  <tr>
  <td><code>Efternamn</code></td>
  <td><span class="badge badge-danger">Ja</span></td>
  <td>Efternamn</td>
  <td>Nordenson</td>
  </tr>

  <tr class="table-section-red">
  <td colspan="4"><strong>Adress (PRIVAT)</strong></td>
  </tr>
  <tr>
  <td><code>Postadress</code></td>
  <td><span class="badge badge-secondary">Nej</span></td>
  <td>Gatuadress</td>
  <td>När Andarve 358</td>
  </tr>
  <tr>
  <td><code>Postnummer</code></td>
  <td><span class="badge badge-secondary">Nej</span></td>
  <td>Postnummer</td>
  <td>62348</td>
  </tr>
  <tr>
  <td><code>Ort</code></td>
  <td><span class="badge badge-secondary">Nej</span></td>
  <td>Stad/Ort</td>
  <td>Stånga</td>
  </tr>
  <tr>
  <td><code>Land</code></td>
  <td><span class="badge badge-secondary">Nej</span></td>
  <td>Land (standard: Sverige)</td>
  <td>Sverige</td>
  </tr>

  <tr class="table-section-red">
  <td colspan="4"><strong>Kontakt (PRIVAT)</strong></td>
  </tr>
  <tr>
  <td><code>Epostadress</code></td>
  <td><span class="badge badge-secondary">Nej</span></td>
  <td>E-postadress</td>
  <td>ernorde@gmail.com</td>
  </tr>
  <tr>
  <td><code>Telefon</code></td>
  <td><span class="badge badge-secondary">Nej</span></td>
  <td>Telefonnummer</td>
  <td>070-1234567</td>
  </tr>
  <tr>
  <td><code>Emergency contact</code></td>
  <td><span class="badge badge-secondary">Nej</span></td>
  <td>Nödkontakt (namn och telefon)</td>
  <td>Helen Nordenson, +46709609560</td>
  </tr>

  <tr class="table-section-blue">
  <td colspan="4"><strong>Organisation</strong></td>
  </tr>
  <tr>
  <td><code>Distrikt</code></td>
  <td><span class="badge badge-secondary">Nej</span></td>
  <td>Distriktsförbund</td>
  <td>Smålands Cykelförbund</td>
  </tr>
  <tr>
  <td><code>Huvudförening</code></td>
  <td><span class="badge badge-secondary">Nej</span></td>
  <td>Klubb/Förening</td>
  <td>Ringmurens Cykelklubb</td>
  </tr>
  <tr>
  <td><code>Team</code></td>
  <td><span class="badge badge-secondary">Nej</span></td>
  <td>Team (kan skilja sig från klubb)</td>
  <td>Team GravitySeries</td>
  </tr>

  <tr class="table-section-green">
  <td colspan="4"><strong>Grenar</strong></td>
  </tr>
  <tr>
  <td><code>Road</code>, <code>Track</code>, <code>BMX</code>, <code>CX</code>, <code>Trial</code>, <code>Para</code>, <code>MTB</code>, <code>E-cycling</code>, <code>Gravel</code></td>
  <td><span class="badge badge-secondary">Nej</span></td>
  <td>Markera grenar (tom för nej, valfritt värde för ja)</td>
  <td>Road, Gravel</td>
  </tr>

  <tr class="table-section-purple">
  <td colspan="4"><strong>Licens</strong></td>
  </tr>
  <tr>
  <td><code>Kategori</code></td>
  <td><span class="badge badge-secondary">Nej</span></td>
  <td>Licensk kategori</td>
  <td>Men</td>
  </tr>
  <tr>
  <td><code>Licenstyp</code></td>
  <td><span class="badge badge-secondary">Nej</span></td>
  <td>Typ av licens</td>
  <td>Master Men</td>
  </tr>
  <tr>
  <td><code>LicensÅr</code></td>
  <td><span class="badge badge-secondary">Nej</span></td>
  <td>Licensår</td>
  <td>2025</td>
  </tr>
  <tr>
  <td><code>UCIKod</code></td>
  <td><span class="badge badge-secondary">Nej</span></td>
  <td>UCI ID-nummer</td>
  <td>101 637 581 11</td>
  </tr>
  </tbody>
  </table>
 </div>

 <div class="mt-lg alert alert--info">
  <h3 class="text-primary mb-sm">
  <i data-lucide="lightbulb"></i>
  Tips
  </h3>
  <ul class="text-sm gs-list-ml-lg-lh-1-8">
  <li>Använd <strong>tabulator</strong>, semikolon (;) eller komma (,) som separator</li>
  <li>UTF-8 encoding för svenska tecken</li>
  <li>Personnummer används för att extrahera födelseår automatiskt</li>
  <li>Grenar markeras genom att fylla i kolumnen (tomt = nej, valfritt värde = ja)</li>
  <li>Befintliga deltagare uppdateras automatiskt baserat på personnummer eller UCI-kod</li>
  <li>Klubbar som inte finns skapas automatiskt</li>
  </ul>
 </div>

 <div class="mt-md">
  <p class="text-sm text-secondary">
  <strong>Exempel på CSV-rad (från din fil):</strong>
  </p>
  <pre class="gs-pre-format">Födelsedatum	Förnamn	Efternamn	Postadress	Postnummer	Ort	Land	Epostadress	Telefon	Emergency contact	Distrikt	Huvudförening	Road	Track	BMX	CX	Trial	Para	MTB	E-cycling	Gravel	Kategori	Licenstyp	LicensÅr	UCIKod	Team
19400525-0651	Lars	Nordenson	När Andarve 358	62348	Stånga	Sverige	ernorde@gmail.com		Helen Nordenson, +46709609560	Smålands Cykelförbund	Ringmurens Cykelklubb	Road								Gravel	Men	Master Men	2025	101 637 581 11	</pre>
 </div>
 </div>
 </div>
 </div>
 <?php render_admin_footer(); ?>
</main>

<?php include __DIR__ . '/../includes/layout-footer.php'; ?>
