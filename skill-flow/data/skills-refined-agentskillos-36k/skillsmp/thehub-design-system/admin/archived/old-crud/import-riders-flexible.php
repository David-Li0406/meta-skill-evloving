<?php
/**
 * Flexible Rider Import - ANY Column Order
 *
 * SUPER FLEXIBEL IMPORT:
 * - Kolumner kan vara i VILKEN ORDNING SOM HELST
 * - Okända kolumner IGNORERAS automatiskt
 * - Fungerar med CSV från olika källor (Excel, Google Sheets, etc.)
 * - Stödjer ALLA separatorer (tab, semikolon, komma)
 *
 * PRIVACY: Hanterar känslig data säkert
 */

error_reporting(E_ALL);
ini_set('display_errors', 1);

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
$columnMapping = null;
$previewMode = false;

// Handle file upload
if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_FILES['import_file'])) {
 checkCsrf();

 $file = $_FILES['import_file'];
 $previewMode = isset($_POST['preview_mode']);

 if ($file['error'] !== UPLOAD_ERR_OK) {
 $message = 'Filuppladdning misslyckades';
 $messageType = 'error';
 } elseif ($file['size'] > MAX_UPLOAD_SIZE) {
 $message = 'Filen är för stor (max ' . (MAX_UPLOAD_SIZE / 1024 / 1024) . 'MB)';
 $messageType = 'error';
 } else {
 $extension = strtolower(pathinfo($file['name'], PATHINFO_EXTENSION));

 if ($extension !== 'csv') {
 $message = 'Endast CSV-filer stöds. Exportera från Excel/Google Sheets som CSV.';
 $messageType = 'error';
 } else {
 $uploaded = UPLOADS_PATH . '/' . time() . '_' . basename($file['name']);

 if (move_uploaded_file($file['tmp_name'], $uploaded)) {
 try {
  if ($previewMode) {
  // Preview mode - just show column mapping
  $columnMapping = analyzeCSVColumns($uploaded);
  $message = 'Förhandsgranskning klar! Granska kolumnmappningen nedan.';
  $messageType = 'info';
  } else {
  // Import mode
  $result = importRidersFlexible($uploaded, $db);
  $stats = $result['stats'];
  $errors = $result['errors'];
  $skippedRows = $result['skipped_rows'] ?? [];
  $columnMapping = $result['column_mapping'];

  if ($stats['success'] > 0 || $stats['updated'] > 0) {
  $message ="Import klar! {$stats['success']} nya, {$stats['updated']} uppdaterade.";
  if ($stats['duplicates'] > 0) {
  $message .=" {$stats['duplicates']} dubletter hoppades över.";
  }
  $messageType = 'success';
  } else {
  $message ="Ingen data importerades. Kontrollera filformatet.";
  $messageType = 'error';
  }
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
}

/**
 * Analyze CSV columns without importing
 */
function analyzeCSVColumns($filepath) {
 if (($handle = fopen($filepath, 'r')) === false) {
 throw new Exception('Kunde inte öppna filen');
 }

 // Detect delimiter
 $firstLine = fgets($handle);
 rewind($handle);
 $delimiter = detectDelimiter($firstLine);

 // Read header
 $header = fgetcsv($handle, 10000, $delimiter);
 fclose($handle);

 if (!$header) {
 throw new Exception('Tom fil eller ogiltigt format');
 }

 // Map columns
 return mapColumns($header);
}

/**
 * Detect CSV delimiter
 */
function detectDelimiter($line) {
 $delimiters = ["\t" => 0, ';' => 0, ',' => 0];

 foreach ($delimiters as $delimiter => $count) {
 $delimiters[$delimiter] = substr_count($line, $delimiter);
 }

 return array_search(max($delimiters), $delimiters);
}

/**
 * Map CSV columns to database fields
 */
function mapColumns($header) {
 $mapping = [
 'recognized' => [],
 'ignored' => [],
 'delimiter' => null
 ];

 // Define all possible column name variants
 $columnVariants = [
 // Name fields
 'firstname' => ['förnamn', 'fornamn', 'firstname', 'first_name', 'fname', 'givenname', 'name'],
 'lastname' => ['efternamn', 'lastname', 'last_name', 'surname', 'familyname', 'lname'],

 // Birth info
 'personnummer' => ['födelsedatum', 'fodelsedatum', 'personnummer', 'pnr', 'ssn', 'dateofbirth', 'birthdate'],
 'birthyear' => ['födelseår', 'fodelsear', 'birthyear', 'birth_year', 'född', 'fodd', 'year', 'ålder', 'alder', 'age'],

 // Gender
 'gender' => ['kön', 'kon', 'gender', 'sex', 'kategori'],

 // Address (PRIVATE)
 'address' => ['postadress', 'adress', 'address', 'streetaddress', 'street'],
 'postalcode' => ['postnummer', 'postalcode', 'postal_code', 'zipcode', 'zip'],
 'city' => ['ort', 'stad', 'city'],
 'country' => ['land', 'country'],

 // Contact (PRIVATE)
 'email' => ['epost', 'epostadress', 'email', 'e-post', 'mail', 'emailaddress'],
 'phone' => ['telefon', 'phone', 'tel', 'mobile', 'mobil'],
 'emergencycontact' => ['emergencycontact', 'emergency_contact', 'nödkontakt', 'nodkontakt', 'nodnummer'],

 // Organization
 'district' => ['distrikt', 'district', 'region'],
 'club' => ['huvudförening', 'huvudforening', 'klubb', 'club', 'klubbnamn', 'clubname', 'forening'],
 'team' => ['team', 'lag'],

 // Disciplines
 'road' => ['road', 'landsväg', 'landsvag'],
 'track' => ['track', 'bana'],
 'bmx' => ['bmx'],
 'cx' => ['cx', 'cyclocross'],
 'trial' => ['trial'],
 'para' => ['para'],
 'mtb' => ['mtb', 'mountainbike', 'mountain'],
 'ecycling' => ['ecycling', 'e-cycling'],
 'gravel' => ['gravel'],

 // License
 'category' => ['category', 'cat'],
 'licensetype' => ['licenstyp', 'licensetype', 'licenstype'],
 'licenseyear' => ['licensår', 'licensar', 'licenseyear', 'år', 'ar'],
 'ucicode' => ['ucikod', 'ucicode', 'uciid', 'licens', 'license', 'licensnummer', 'licensenumber'],
 ];

 foreach ($header as $index => $column) {
 $originalColumn = $column;
 $column = normalizeColumnName($column);

 $matched = false;
 foreach ($columnVariants as $field => $variants) {
 if (in_array($column, $variants)) {
 $mapping['recognized'][] = [
  'original' => $originalColumn,
  'normalized' => $column,
  'maps_to' => $field,
  'index' => $index
 ];
 $matched = true;
 break;
 }
 }

 if (!$matched) {
 $mapping['ignored'][] = [
 'original' => $originalColumn,
 'index' => $index
 ];
 }
 }

 return $mapping;
}

/**
 * Normalize column name for matching
 */
function normalizeColumnName($name) {
 $name = mb_strtolower(trim($name), 'UTF-8');
 $name = str_replace([' ', '-', '_'], '', $name);
 // DO NOT replace å, ä, ö - we need them for proper Swedish column matching!
 return $name;
}

/**
 * Import riders with flexible column mapping
 */
function importRidersFlexible($filepath, $db) {
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

 // Detect delimiter
 $firstLine = fgets($handle);
 rewind($handle);
 $delimiter = detectDelimiter($firstLine);

 // Read and map header
 $header = fgetcsv($handle, 10000, $delimiter);
 if (!$header) {
 fclose($handle);
 throw new Exception('Tom fil eller ogiltigt format');
 }

 $columnMapping = mapColumns($header);

 // Build index map for quick lookup
 $fieldIndexMap = [];
 foreach ($columnMapping['recognized'] as $col) {
 $fieldIndexMap[$col['maps_to']] = $col['index'];
 }

 // Helper function to get field value
 $getField = function($row, $fieldName) use ($fieldIndexMap) {
 if (isset($fieldIndexMap[$fieldName]) && isset($row[$fieldIndexMap[$fieldName]])) {
 $value = trim($row[$fieldIndexMap[$fieldName]]);
 return $value !== '' ? $value : null;
 }
 return null;
 };

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

 // Extract data using flexible mapping
 $firstname = $getField($row, 'firstname');
 $lastname = $getField($row, 'lastname');

 // Validate required fields
 if (empty($firstname) || empty($lastname)) {
 $stats['skipped']++;
 $errors[] ="Rad {$lineNumber}: Saknar förnamn eller efternamn";
 $skippedRows[] = [
 'row' => $lineNumber,
 'name' => trim(($firstname ?? '') . ' ' . ($lastname ?? '')),
 'reason' => 'Saknar förnamn eller efternamn',
 'type' => 'missing_fields'
 ];
 continue;
 }

 try {
 // Parse personnummer for birth year
 $birthYear = null;
 $personnummer = $getField($row, 'personnummer');

 if ($personnummer) {
 if (preg_match('/^(\d{4})(\d{2})(\d{2})/', $personnummer, $matches)) {
  $birthYear = (int)$matches[1];
 } elseif (preg_match('/^(\d{2})(\d{2})(\d{2})/', $personnummer, $matches)) {
  $year = (int)$matches[1];
  $birthYear = ($year > 25) ? (1900 + $year) : (2000 + $year);
 }
 }

 // Fallback to birth_year field
 if (!$birthYear) {
 $birthYearField = $getField($row, 'birthyear');
 if ($birthYearField) {
  $birthYear = (int)$birthYearField;
 }
 }

 // Normalize gender
 $genderRaw = mb_strtolower($getField($row, 'gender') ?? 'M', 'UTF-8');
 if (in_array($genderRaw, ['woman', 'women', 'female', 'kvinna', 'dam', 'f', 'k'])) {
 $gender = 'F';
 } elseif (in_array($genderRaw, ['man', 'men', 'male', 'herr', 'm'])) {
 $gender = 'M';
 } else {
 $gender = 'M';
 }

 // Build rider data
 $riderData = [
 'firstname' => $firstname,
 'lastname' => $lastname,
 'birth_year' => $birthYear,
 'personnummer' => $personnummer,
 'gender' => $gender,
 'address' => $getField($row, 'address'),
 'postal_code' => $getField($row, 'postalcode'),
 'city' => $getField($row, 'city'),
 'country' => $getField($row, 'country') ?? 'Sverige',
 'email' => $getField($row, 'email'),
 'phone' => $getField($row, 'phone'),
 'emergency_contact' => $getField($row, 'emergencycontact'),
 'district' => $getField($row, 'district'),
 'team' => $getField($row, 'team'),
 'license_number' => $getField($row, 'ucicode'),
 'license_type' => $getField($row, 'licensetype'),
 'license_category' => $getField($row, 'category'),
 'license_year' => $getField($row, 'licenseyear') ? (int)$getField($row, 'licenseyear') : null,
 'active' => 1
 ];

 // Build disciplines JSON
 $disciplines = [];
 $disciplineFields = ['road', 'track', 'bmx', 'cx', 'trial', 'para', 'mtb', 'ecycling', 'gravel'];
 foreach ($disciplineFields as $disc) {
 $value = $getField($row, $disc);
 if ($value && strtolower($value) !== '0' && strtolower($value) !== 'no' && strtolower($value) !== 'nej') {
  $disciplines[] = ucfirst($disc);
 }
 }
 $riderData['disciplines'] = !empty($disciplines) ? json_encode($disciplines) : null;

 // Handle club
 $clubName = $getField($row, 'club');
 if ($clubName) {
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

 // Check for duplicates
 $uniqueKey = '';
 if ($riderData['license_number']) {
 $uniqueKey = 'lic_' . strtolower($riderData['license_number']);
 } elseif ($personnummer) {
 $uniqueKey = 'pnr_' . $personnummer;
 } else {
 $uniqueKey = 'name_' . strtolower($firstname) . '_' . strtolower($lastname) . '_' . ($birthYear ?? '0');
 }

 if (isset($seenInThisImport[$uniqueKey])) {
 $stats['duplicates']++;
 $stats['skipped']++;
 $skippedRows[] = [
  'row' => $lineNumber,
  'name' => $firstname . ' ' . $lastname,
  'license' => $riderData['license_number'] ?? '-',
  'reason' => 'Dublett i denna import',
  'type' => 'duplicate'
 ];
 continue;
 }

 $seenInThisImport[$uniqueKey] = true;

 // Check if rider exists in database
 $existing = null;
 if ($riderData['license_number']) {
 $existing = $db->getRow("SELECT id FROM riders WHERE license_number = ? LIMIT 1", [$riderData['license_number']]);
 }
 if (!$existing && $personnummer) {
 $existing = $db->getRow("SELECT id FROM riders WHERE personnummer = ? LIMIT 1", [$personnummer]);
 }
 if (!$existing && $birthYear) {
 $existing = $db->getRow(
 "SELECT id FROM riders WHERE firstname = ? AND lastname = ? AND birth_year = ? LIMIT 1",
  [$firstname, $lastname, $birthYear]
 );
 }

 if ($existing) {
 $db->update('riders', $riderData, 'id = ?', [$existing['id']]);
 $stats['updated']++;
 } else {
 $db->insert('riders', $riderData);
 $stats['success']++;
 }

 } catch (Exception $e) {
 $stats['failed']++;
 $errors[] ="Rad {$lineNumber}:" . $e->getMessage();
 $skippedRows[] = [
 'row' => $lineNumber,
 'name' => $firstname . ' ' . $lastname,
 'license' => $riderData['license_number'] ?? '-',
 'reason' => 'Fel: ' . $e->getMessage(),
 'type' => 'error'
 ];
 }
 }

 fclose($handle);

 return [
 'stats' => $stats,
 'errors' => $errors,
 'skipped_rows' => $skippedRows,
 'column_mapping' => $columnMapping
 ];
}

$pageTitle = 'Flexibel Import';
$pageType = 'admin';
include __DIR__ . '/../includes/layout-header.php';
?>

<main class="main-content">
 <div class="container">
 <?php render_admin_header('Import & Data'); ?>

 <!-- Features Info -->
 <div class="alert alert--success mb-lg">
 <i data-lucide="check-circle"></i>
 <strong>Superflexibel import!</strong>
 <ul class="gs-list-ml-1-5">
 <li>✅ Kolumner kan vara i VILKEN ORDNING SOM HELST</li>
 <li>✅ Okända kolumner IGNORERAS automatiskt</li>
 <li>✅ Fungerar med CSV från Excel, Google Sheets, etc.</li>
 <li>✅ Automatisk detektering av separator (tab, semikolon, komma)</li>
 <li>✅ Förhandsgranska kolumnmappning innan import</li>
 </ul>
 </div>

 <!-- Message -->
 <?php if ($message): ?>
 <div class="alert alert-<?= h($messageType) ?> mb-lg">
 <i data-lucide="<?= $messageType === 'success' ? 'check-circle' : 'info' ?>"></i>
 <?= h($message) ?>
 </div>
 <?php endif; ?>

 <!-- Column Mapping Preview -->
 <?php if ($columnMapping): ?>
 <div class="card mb-lg">
 <div class="card-header">
  <h2 class="text-primary">
  <i data-lucide="git-branch"></i>
  Kolumnmappning
  </h2>
 </div>
 <div class="card-body">
  <div class="grid grid-cols-1 md-grid-cols-2 gap-lg">
  <!-- Recognized Columns -->
  <div>
  <h3 class="text-success mb-md">
  <i data-lucide="check"></i>
  Igenkända Kolumner (<?= count($columnMapping['recognized']) ?>)
  </h3>
  <div class="table-responsive">
  <table class="table table-sm">
   <thead>
   <tr>
   <th>Din Kolumn</th>
   <th>Mappas Till</th>
   </tr>
   </thead>
   <tbody>
   <?php foreach ($columnMapping['recognized'] as $col): ?>
   <tr>
   <td><code><?= h($col['original']) ?></code></td>
   <td>
    <span class="badge badge-success badge-sm">
    <?= h($col['maps_to']) ?>
    </span>
   </td>
   </tr>
   <?php endforeach; ?>
   </tbody>
  </table>
  </div>
  </div>

  <!-- Ignored Columns -->
  <?php if (!empty($columnMapping['ignored'])): ?>
  <div>
  <h3 class="text-secondary mb-md">
   <i data-lucide="x"></i>
   Ignorerade Kolumner (<?= count($columnMapping['ignored']) ?>)
  </h3>
  <div class="table-responsive">
   <table class="table table-sm">
   <thead>
   <tr>
   <th>Kolumnnamn</th>
   <th>Status</th>
   </tr>
   </thead>
   <tbody>
   <?php foreach ($columnMapping['ignored'] as $col): ?>
   <tr>
    <td><code><?= h($col['original']) ?></code></td>
    <td>
    <span class="badge badge-secondary badge-sm">
    Ignorerad
    </span>
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

  <!-- Skipped Rows -->
  <?php if (!empty($skippedRows)): ?>
  <div class="mt-lg section-divider-top">
  <h3 class="text-warning mb-md">
  <i data-lucide="alert-circle"></i>
  Överhoppade rader (<?= count($skippedRows) ?>)
  </h3>
  <div class="gs-scroll-y-400-simple">
  <table class="table table-sm">
   <thead>
   <tr>
   <th>Rad</th>
   <th>Namn</th>
   <th>Anledning</th>
   </tr>
   </thead>
   <tbody>
   <?php foreach (array_slice($skippedRows, 0, 100) as $skip): ?>
   <tr>
   <td><code><?= $skip['row'] ?></code></td>
   <td><?= h($skip['name']) ?></td>
   <td><?= h($skip['reason']) ?></td>
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
 <form method="POST" enctype="multipart/form-data" class="container-max-600">
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
  Max storlek: <?= round(MAX_UPLOAD_SIZE / 1024 / 1024) ?>MB
  </small>
  </div>

  <div class="flex gap-sm">
  <button type="submit" name="preview_mode" value="1" class="btn btn--secondary">
  <i data-lucide="eye"></i>
  Förhandsgranska
  </button>
  <button type="submit" class="btn btn--primary btn-lg">
  <i data-lucide="upload"></i>
  Importera
  </button>
  </div>
 </form>
 </div>
 </div>

 <!-- Example Formats -->
 <div class="card">
 <div class="card-header">
 <h2 class="text-primary">
  <i data-lucide="info"></i>
  Exempel på Kolumnnamn
 </h2>
 </div>
 <div class="card-body">
 <p class="text-secondary mb-md">
  Systemet känner automatiskt igen följande kolumnnamn (på svenska eller engelska):
 </p>

 <div class="grid grid-cols-1 md-grid-cols-3 gap-md">
  <div>
  <h3 class="mb-sm">Obligatoriska</h3>
  <ul class="text-sm gs-line-height-1-8">
  <li><code>Förnamn</code> / <code>Firstname</code></li>
  <li><code>Efternamn</code> / <code>Lastname</code></li>
  </ul>
  </div>

  <div>
  <h3 class="mb-sm">Personuppgifter</h3>
  <ul class="text-sm gs-line-height-1-8">
  <li><code>Födelsedatum</code> / <code>Personnummer</code></li>
  <li><code>Födelseår</code> / <code>Birth Year</code></li>
  <li><code>Kön</code> / <code>Gender</code></li>
  <li><code>Epost</code> / <code>Email</code></li>
  <li><code>Telefon</code> / <code>Phone</code></li>
  </ul>
  </div>

  <div>
  <h3 class="mb-sm">Adress</h3>
  <ul class="text-sm gs-line-height-1-8">
  <li><code>Postadress</code> / <code>Address</code></li>
  <li><code>Postnummer</code> / <code>Postal Code</code></li>
  <li><code>Ort</code> / <code>City</code></li>
  <li><code>Land</code> / <code>Country</code></li>
  </ul>
  </div>

  <div>
  <h3 class="mb-sm">Organisation</h3>
  <ul class="text-sm gs-line-height-1-8">
  <li><code>Klubb</code> / <code>Club</code></li>
  <li><code>Huvudförening</code></li>
  <li><code>Team</code></li>
  <li><code>Distrikt</code> / <code>District</code></li>
  </ul>
  </div>

  <div>
  <h3 class="mb-sm">Licens</h3>
  <ul class="text-sm gs-line-height-1-8">
  <li><code>UCI Kod</code> / <code>UCI ID</code></li>
  <li><code>Licenstyp</code> / <code>License Type</code></li>
  <li><code>Kategori</code> / <code>Category</code></li>
  <li><code>Licensår</code> / <code>License Year</code></li>
  </ul>
  </div>

  <div>
  <h3 class="mb-sm">Grenar</h3>
  <ul class="text-sm gs-line-height-1-8">
  <li><code>Road</code> / <code>Landsväg</code></li>
  <li><code>MTB</code></li>
  <li><code>Gravel</code></li>
  <li><code>CX</code> / <code>Cyclocross</code></li>
  <li><code>Track</code> / <code>Bana</code></li>
  <li>+ BMX, Trial, Para, E-cycling</li>
  </ul>
  </div>
 </div>

 <div class="alert alert--info mt-lg">
  <h3 class="mb-sm">
  <i data-lucide="lightbulb"></i>
  Tips
  </h3>
  <ul class="text-sm gs-line-height-1-8">
  <li>Kolumnerna kan vara i VILKEN ORDNING SOM HELST</li>
  <li>Mellanslag, bindestreck och understreck ignoreras (<code>First Name</code> = <code>FirstName</code> = <code>first_name</code>)</li>
  <li>Svenska tecken normaliseras (å→a, ä→a, ö→o)</li>
  <li>Okända kolumner hoppar systemet över automatiskt</li>
  <li>Använd"Förhandsgranska" för att se hur kolumnerna mappas</li>
  </ul>
 </div>
 </div>
 </div>
 </div>
 <?php render_admin_footer(); ?>
</main>

<?php include __DIR__ . '/../includes/layout-footer.php'; ?>
