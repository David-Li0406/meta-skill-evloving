<?php
require_once __DIR__ . '/../config.php';
require_admin();

$db = getDB();
$current_admin = get_current_admin();

$message = '';
$messageType = 'info';
$stats = null;
$errors = [];

// Handle CSV import
if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_FILES['csv_file'])) {
 checkCsrf();

 $file = $_FILES['csv_file'];

 if ($file['error'] === UPLOAD_ERR_OK) {
 $result = importSeriesFromCSV($file['tmp_name'], $db);
 $stats = $result['stats'];
 $errors = $result['errors'];

 if ($stats['failed'] === 0) {
  $message ="Import klar! {$stats['success']} serier importerade.";
  $messageType = 'success';
 } else {
  $message ="Import klar med fel. {$stats['success']} lyckades, {$stats['failed']} misslyckades.";
  $messageType = 'warning';
 }
 } else {
 $message = 'Fel vid uppladdning av fil.';
 $messageType = 'error';
 }
}

/**
 * Import series from CSV file
 */
function importSeriesFromCSV($filePath, $db) {
 $stats = [
 'total' => 0,
 'success' => 0,
 'updated' => 0,
 'failed' => 0,
 'skipped' => 0
 ];
 $errors = [];

 $handle = fopen($filePath, 'r');
 if (!$handle) {
 return ['stats' => $stats, 'errors' => ['Kunde inte öppna filen']];
 }

 // Auto-detect delimiter (comma or semicolon)
 $firstLine = fgets($handle);
 rewind($handle);
 $delimiter = (substr_count($firstLine, ';') > substr_count($firstLine, ',')) ? ';' : ',';

 // Read header
 $header = fgetcsv($handle, 0, $delimiter);
 if (!$header) {
 fclose($handle);
 return ['stats' => $stats, 'errors' => ['Ogiltig CSV-fil']];
 }

 // Normalize header - accept multiple variants of column names
 $header = array_map(function($col) {
 $col = strtolower(trim($col));
 $col = str_replace([' ', '-', '_'], '', $col); // Remove spaces, hyphens, underscores

 // Map various column name variants to standard names
 $mappings = [
  'namn' => 'name',
  'name' => 'name',
  'serienamn' => 'name',
  'seriesname' => 'name',
  'title' => 'name',

  'typ' => 'type',
  'type' => 'type',
  'serietype' => 'type',
  'serietyp' => 'type',

  'gren' => 'discipline',
  'discipline' => 'discipline',
  'sport' => 'discipline',

  'år' => 'year',
  'ar' => 'year',
  'year' => 'year',
  'säsong' => 'year',
  'sasong' => 'year',
  'season' => 'year',

  'status' => 'status',
  'state' => 'status',
  'tillstånd' => 'status',
  'tillstand' => 'status',

  'startdatum' => 'startdate',
  'startdate' => 'startdate',
  'start' => 'startdate',
  'börjar' => 'startdate',
  'borjar' => 'startdate',
  'begins' => 'startdate',

  'slutdatum' => 'enddate',
  'enddate' => 'enddate',
  'slut' => 'enddate',
  'end' => 'enddate',
  'slutar' => 'enddate',
  'ends' => 'enddate',

  'beskrivning' => 'description',
  'description' => 'description',
  'beskriv' => 'description',
  'info' => 'description',

  'webbplats' => 'website',
  'website' => 'website',
  'url' => 'website',
  'hemsida' => 'website',
  'web' => 'website',

  'arrangör' => 'organizer',
  'arrangor' => 'organizer',
  'organizer' => 'organizer',
  'organisatör' => 'organizer',
  'organisator' => 'organizer',
  'delegat' => 'organizer',
  'delegate' => 'organizer',
 ];

 return $mappings[$col] ?? $col;
 }, $header);

 $lineNumber = 1;

 while (($row = fgetcsv($handle, 0, $delimiter)) !== false) {
 $lineNumber++;
 $stats['total']++;

 if (count($row) !== count($header)) {
  $stats['skipped']++;
  continue;
 }

 $data = array_combine($header, $row);

 try {
  // Required fields
  if (empty($data['name'])) {
  $stats['skipped']++;
  continue;
  }

  // Prepare series data
  $seriesData = [
  'name' => trim($data['name']),
  'type' => trim($data['type'] ?? 'championship'),
  'discipline' => trim($data['discipline'] ?? ''),
  'year' => !empty($data['year']) ? intval($data['year']) : date('Y'),
  'status' => trim($data['status'] ?? 'planning'),
  'start_date' => !empty($data['startdate']) ? trim($data['startdate']) : null,
  'end_date' => !empty($data['enddate']) ? trim($data['enddate']) : null,
  'description' => trim($data['description'] ?? ''),
  'website' => trim($data['website'] ?? ''),
  'organizer' => trim($data['organizer'] ?? ''),
  'active' => 1
  ];

  // Check if series exists (by name and year)
  $existing = $db->getRow(
  "SELECT id FROM series WHERE name = ? AND year = ? LIMIT 1",
  [$seriesData['name'], $seriesData['year']]
  );

  if ($existing) {
  // Update existing series
  $db->update('series', $seriesData, 'id = ?', [$existing['id']]);
  $stats['updated']++;
  error_log("Updated series: {$seriesData['name']} ({$seriesData['year']})");
  } else {
  // Insert new series
  $newId = $db->insert('series', $seriesData);
  $stats['success']++;
  error_log("Inserted series: {$seriesData['name']} ({$seriesData['year']}) (ID: {$newId})");
  }

 } catch (Exception $e) {
  $stats['failed']++;
  $errors[] ="Rad {$lineNumber}:" . $e->getMessage();
  error_log("Import error on line {$lineNumber}:" . $e->getMessage());
 }
 }

 fclose($handle);

 // Verification
 $verifyCount = $db->getRow("SELECT COUNT(*) as count FROM series");
 $totalInDb = $verifyCount['count'] ?? 0;
 error_log("Series import complete: {$stats['success']} new, {$stats['updated']} updated, {$stats['failed']} failed. Total series in DB: {$totalInDb}");

 $stats['total_in_db'] = $totalInDb;

 return [
 'stats' => $stats,
 'errors' => $errors
 ];
}

$page_title = 'Importera Serier';
$page_group = 'import';
include __DIR__ . '/components/unified-layout.php';
?>

 <?php if ($message): ?>
  <div class="alert alert-<?= h($messageType) ?> mb-lg">
  <i data-lucide="<?= $messageType === 'success' ? 'check-circle' : 'alert-circle' ?>"></i>
  <?= h($message) ?>
  </div>
 <?php endif; ?>

 <?php if (!empty($errors)): ?>
  <div class="alert alert--error mb-lg">
  <strong>Fel under import:</strong>
  <ul class="mt-sm">
   <?php foreach ($errors as $error): ?>
   <li><?= h($error) ?></li>
   <?php endforeach; ?>
  </ul>
  </div>
 <?php endif; ?>

 <?php if ($stats): ?>
  <div class="card mb-lg">
  <div class="card-header">
   <h2 class="">Import-statistik</h2>
  </div>
  <div class="card-body">
   <div class="grid grid-cols-5 gap-md">
   <div class="stat-card">
    <div class="stat-value"><?= $stats['total'] ?></div>
    <div class="stat-label">Totalt rader</div>
   </div>
   <div class="stat-card">
    <div class="stat-value text-success"><?= $stats['success'] ?></div>
    <div class="stat-label">Nya</div>
   </div>
   <div class="stat-card">
    <div class="stat-value gs-text-info"><?= $stats['updated'] ?></div>
    <div class="stat-label">Uppdaterade</div>
   </div>
   <div class="stat-card">
    <div class="stat-value text-secondary"><?= $stats['skipped'] ?></div>
    <div class="stat-label">Överhoppade</div>
   </div>
   <div class="stat-card">
    <div class="stat-value text-error"><?= $stats['failed'] ?></div>
    <div class="stat-label">Misslyckade</div>
   </div>
   </div>

   <div class="mt-lg">
   <h3 class="mb-sm">Verifiering</h3>
   <p class="text-lg"><strong>Totalt i databasen:</strong> <?= $stats['total_in_db'] ?> serier</p>
   </div>
  </div>
  </div>
 <?php endif; ?>

 <!-- Upload Form -->
 <div class="card mb-lg">
  <div class="card-header">
  <h2 class="">Bulk-import av serier från CSV-fil</h2>
  </div>
  <div class="card-body">
  <form method="POST" enctype="multipart/form-data" class="gs-form">
   <?= csrf_field() ?>

   <div class="alert alert--info mb-md">
   <i data-lucide="info"></i>
   <strong>CSV-format:</strong> Första raden ska innehålla kolumnnamn.
   </div>

   <div class="form-group">
   <label class="label">
    <i data-lucide="upload"></i>
    Välj CSV-fil
   </label>
   <input
    type="file"
    name="csv_file"
    accept=".csv"
    required
    class="input"
   >
   <small class="text-secondary">Max 10 MB. Format: CSV (komma-separerad)</small>
   </div>

   <div class="flex gap-md">
   <button type="submit" class="btn btn--primary">
    <i data-lucide="upload"></i>
    Importera Serier
   </button>
   <a href="/admin/series.php" class="btn btn--secondary">
    <i data-lucide="arrow-left"></i>
    Tillbaka
   </a>
   <a href="/templates/import-series-template.csv" class="btn btn--secondary" download>
    <i data-lucide="download"></i>
    Ladda ner mall
   </a>
   </div>
  </form>
  </div>
 </div>

 <!-- CSV Format Info -->
 <div class="card">
  <div class="card-header">
  <h2 class="">CSV-kolumner</h2>
  </div>
  <div class="card-body">
  <table class="table">
   <thead>
   <tr>
    <th>Kolumn</th>
    <th>Beskrivning</th>
    <th>Obligatorisk</th>
    <th>Exempel</th>
   </tr>
   </thead>
   <tbody>
   <tr>
    <td><code>name</code></td>
    <td>Serie-namn</td>
    <td>✅ Ja</td>
    <td>Enduro Series 2025</td>
   </tr>
   <tr>
    <td><code>type</code></td>
    <td>Typ (championship/cup/challenge)</td>
    <td>Nej</td>
    <td>championship</td>
   </tr>
   <tr>
    <td><code>discipline</code></td>
    <td>Disciplin</td>
    <td>Nej</td>
    <td>Enduro</td>
   </tr>
   <tr>
    <td><code>year</code></td>
    <td>År</td>
    <td>Nej</td>
    <td>2025</td>
   </tr>
   <tr>
    <td><code>status</code></td>
    <td>Status (planning/active/completed)</td>
    <td>Nej</td>
    <td>active</td>
   </tr>
   <tr>
    <td><code>start_date</code></td>
    <td>Startdatum (YYYY-MM-DD)</td>
    <td>Nej</td>
    <td>2025-05-01</td>
   </tr>
   <tr>
    <td><code>end_date</code></td>
    <td>Slutdatum (YYYY-MM-DD)</td>
    <td>Nej</td>
    <td>2025-09-30</td>
   </tr>
   <tr>
    <td><code>description</code></td>
    <td>Beskrivning</td>
    <td>Nej</td>
    <td>Svenska Enduro-mästerskapen 2025</td>
   </tr>
   <tr>
    <td><code>website</code></td>
    <td>Hemsida</td>
    <td>Nej</td>
    <td>https://enduro.se</td>
   </tr>
   </tbody>
  </table>
  </div>
 </div>
<?php include __DIR__ . '/components/unified-layout-footer.php'; ?>
