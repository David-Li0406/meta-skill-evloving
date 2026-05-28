<?php
/**
 * Import Events from CSV - V3 Unified Design System
 *
 * Imports basic event data from CSV file with preview.
 * Series and point templates can be assigned after import.
 */

require_once __DIR__ . '/../config.php';
require_admin();

$db = getDB();
$current_admin = get_current_admin();

$message = '';
$messageType = 'info';
$previewData = [];

// Get venues for matching
$venues = $db->getAll("SELECT id, name FROM venues ORDER BY name");
$venueMap = [];
foreach ($venues as $v) {
 $venueMap[mb_strtolower(trim($v['name']), 'UTF-8')] = $v['id'];
}

// Handle template download
if (isset($_GET['template'])) {
 header('Content-Type: text/csv; charset=utf-8');
 header('Content-Disposition: attachment; filename="event_import_mall.csv"');

 $output = fopen('php://output', 'w');
 // UTF-8 BOM for Excel compatibility
 fprintf($output, chr(0xEF).chr(0xBB).chr(0xBF));

 // Header row
 fputcsv($output, [
 'Namn', 'Datum', 'Advent ID', 'Plats', 'Bana', 'Disciplin',
 'Distans (km)', 'Höjdmeter (m)', 'Arrangör', 'Webbplats',
 'Anmälningsfrist', 'Kontakt e-post', 'Kontakt telefon'
 ], ';');

 // Example row
 fputcsv($output, [
 'Exempel Enduro', '2025-06-15', 'EVT-001', 'Stockholm', 'Hammarby Backe',
 'ENDURO', '25', '800', 'Stockholm MTB', 'https://example.com',
 '2025-06-01', 'info@example.com', '070-1234567'
 ], ';');

 fclose($output);
 exit;
}

// Handle form submissions
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
 checkCsrf();

 $action = $_POST['action'] ?? '';

 if ($action === 'preview' && isset($_FILES['csv_file'])) {
 $file = $_FILES['csv_file'];

 if ($file['error'] !== UPLOAD_ERR_OK) {
 $message = 'Fel vid uppladdning av fil';
 $messageType = 'error';
 } else {
 $content = file_get_contents($file['tmp_name']);

 // Detect encoding
 $encoding = mb_detect_encoding($content, ['UTF-8', 'ISO-8859-1', 'Windows-1252'], true);
 if ($encoding && $encoding !== 'UTF-8') {
 $content = mb_convert_encoding($content, 'UTF-8', $encoding);
 }

 // Remove BOM if present
 $content = preg_replace('/^\xEF\xBB\xBF/', '', $content);

 // Parse CSV
 $lines = explode("\n", $content);
 $header = null;
 $rows = [];

 foreach ($lines as $lineNum => $line) {
 $line = trim($line);
 if (empty($line)) continue;

 // Detect delimiter
 $delimiter = (strpos($line, ';') !== false) ? ';' : ',';
 $fields = str_getcsv($line, $delimiter);

 if ($header === null) {
  $header = array_map(function($h) {
  return mb_strtolower(trim($h), 'UTF-8');
  }, $fields);
  continue;
 }

 if (count($fields) < 2) continue;

 $row = [];
 foreach ($header as $i => $col) {
  $row[$col] = isset($fields[$i]) ? trim($fields[$i]) : '';
 }
 $rows[] = $row;
 }

 if (empty($rows)) {
 $message = 'Ingen data hittades i CSV-filen';
 $messageType = 'error';
 } else {
 // Store in session for import
 $_SESSION['import_events_data'] = $rows;
 $_SESSION['import_events_header'] = $header;

 // Build preview
 foreach ($rows as $row) {
  $preview = [
  'name' => $row['namn'] ?? $row['name'] ?? '',
  'external_id' => $row['advent id'] ?? $row['external_id'] ?? $row['externt id'] ?? '',
  'date' => $row['datum'] ?? $row['date'] ?? '',
  'location' => $row['plats'] ?? $row['location'] ?? '',
  'venue' => $row['bana'] ?? $row['anläggning'] ?? $row['venue'] ?? $row['bana/anläggning'] ?? '',
  'discipline' => $row['disciplin'] ?? $row['discipline'] ?? '',
  'distance_km' => $row['distans'] ?? $row['distans (km)'] ?? $row['distance_km'] ?? '',
  'elevation_m' => $row['höjdmeter'] ?? $row['höjdmeter (m)'] ?? $row['elevation_m'] ?? '',
  'organizer' => $row['arrangör'] ?? $row['organizer'] ?? '',
  'website' => $row['webbplats'] ?? $row['website'] ?? '',
  'registration_deadline' => $row['anmälningsfrist'] ?? $row['registration_deadline'] ?? '',
  'contact_email' => $row['kontakt e-post'] ?? $row['contact_email'] ?? $row['e-post'] ?? '',
  'contact_phone' => $row['kontakt telefon'] ?? $row['contact_phone'] ?? $row['telefon'] ?? '',
  'status' => 'ready',
  'venue_id' => null
  ];

  // Try to match venue
  if ($preview['venue']) {
  $venueLower = mb_strtolower(trim($preview['venue']), 'UTF-8');
  if (isset($venueMap[$venueLower])) {
  $preview['venue_id'] = $venueMap[$venueLower];
  }
  }

  // Validate required fields
  if (empty($preview['name'])) {
  $preview['status'] = 'error';
  $preview['error'] = 'Namn saknas';
  } elseif (empty($preview['date'])) {
  $preview['status'] = 'error';
  $preview['error'] = 'Datum saknas';
  } else {
  // Parse date
  $parsedDate = strtotime($preview['date']);
  if ($parsedDate === false) {
  $preview['status'] = 'error';
  $preview['error'] = 'Ogiltigt datumformat';
  } else {
  $preview['parsed_date'] = date('Y-m-d', $parsedDate);
  }
  }

  $previewData[] = $preview;
 }

 $message = count($previewData) . ' events hittades i filen';
 $messageType = 'success';
 }
 }
 } elseif ($action === 'import') {
 $rows = $_SESSION['import_events_data'] ?? [];

 if (empty($rows)) {
 $message = 'Ingen data att importera. Ladda upp CSV-filen igen.';
 $messageType = 'error';
 } else {
 $imported = 0;
 $skipped = 0;
 $errors = [];

 foreach ($rows as $row) {
 $name = $row['namn'] ?? $row['name'] ?? '';
 $externalId = $row['advent id'] ?? $row['external_id'] ?? $row['externt id'] ?? '';
 $date = $row['datum'] ?? $row['date'] ?? '';
 $location = $row['plats'] ?? $row['location'] ?? '';
 $venue = $row['bana'] ?? $row['anläggning'] ?? $row['venue'] ?? $row['bana/anläggning'] ?? '';
 $discipline = $row['disciplin'] ?? $row['discipline'] ?? '';
 $distanceKm = $row['distans'] ?? $row['distans (km)'] ?? $row['distance_km'] ?? '';
 $elevationM = $row['höjdmeter'] ?? $row['höjdmeter (m)'] ?? $row['elevation_m'] ?? '';
 $organizer = $row['arrangör'] ?? $row['organizer'] ?? '';
 $website = $row['webbplats'] ?? $row['website'] ?? '';
 $registrationDeadline = $row['anmälningsfrist'] ?? $row['registration_deadline'] ?? '';
 $contactEmail = $row['kontakt e-post'] ?? $row['contact_email'] ?? $row['e-post'] ?? '';
 $contactPhone = $row['kontakt telefon'] ?? $row['contact_phone'] ?? $row['telefon'] ?? '';

 // Validate required fields
 if (empty($name) || empty($date)) {
  $skipped++;
  continue;
 }

 // Parse date
 $parsedDate = strtotime($date);
 if ($parsedDate === false) {
  $errors[] ="Ogiltigt datum för '{$name}'";
  $skipped++;
  continue;
 }

 // Generate advent_id if empty
 if (empty($externalId)) {
  $externalId = 'EVT-' . date('Ymd', $parsedDate) . '-' . substr(md5($name . $date), 0, 6);
 }

 // Check if event already exists (by advent_id or name+date)
 $existing = $db->getRow(
 "SELECT id FROM events WHERE advent_id = ? OR (name = ? AND date = ?)",
  [$externalId, $name, date('Y-m-d', $parsedDate)]
 );

 if ($existing) {
  $skipped++;
  continue;
 }

 // Find venue_id
 $venueId = null;
 if ($venue) {
  $venueLower = mb_strtolower(trim($venue), 'UTF-8');
  if (isset($venueMap[$venueLower])) {
  $venueId = $venueMap[$venueLower];
  }
 }

 // Parse registration deadline
 $deadlineDate = null;
 if ($registrationDeadline) {
  $parsedDeadline = strtotime($registrationDeadline);
  if ($parsedDeadline !== false) {
  $deadlineDate = date('Y-m-d', $parsedDeadline);
  }
 }

 // Insert event
 try {
  $db->insert('events', [
  'name' => $name,
  'advent_id' => $externalId,
  'date' => date('Y-m-d', $parsedDate),
  'location' => $location ?: null,
  'venue_id' => $venueId,
  'discipline' => $discipline ?: null,
  'distance_km' => $distanceKm ? floatval($distanceKm) : null,
  'elevation_m' => $elevationM ? intval($elevationM) : null,
  'organizer' => $organizer ?: null,
  'website' => $website ?: null,
  'registration_deadline' => $deadlineDate,
  'contact_email' => $contactEmail ?: null,
  'contact_phone' => $contactPhone ?: null,
  'active' => 1,
  'created_at' => date('Y-m-d H:i:s')
  ]);
  $imported++;
 } catch (Exception $e) {
  $errors[] ="Fel vid import av '{$name}':" . $e->getMessage();
  $skipped++;
 }
 }

 // Clear session data
 unset($_SESSION['import_events_data']);
 unset($_SESSION['import_events_header']);

 if ($imported > 0) {
 $message ="{$imported} events importerades!";
 if ($skipped > 0) {
  $message .=" ({$skipped} hoppades över)";
 }
 $messageType = 'success';
 } else {
 $message ="Inga events importerades. {$skipped} hoppades över.";
 $messageType = 'warning';
 }

 if (!empty($errors)) {
 $message .= '<br><br>Fel:<br>' . implode('<br>', array_slice($errors, 0, 5));
 }
 }
 }
}

// Page config for unified layout
$page_title = 'Importera Events';
$breadcrumbs = [
    ['label' => 'Import', 'url' => '/admin/import'],
    ['label' => 'Events']
];

// Include unified layout
include __DIR__ . '/components/unified-layout.php';
?>

 <!-- Messages -->
 <?php if ($message): ?>
 <div class="alert alert-<?= $messageType ?> mb-md">
 <?= $message ?>
 </div>
 <?php endif; ?>

 <div class="grid grid-cols-1 gs-lg-grid-cols-4 gap-md">
 <!-- Upload Card -->
 <div>
 <div class="card">
  <div class="card-header">
  <h2 class="">Ladda upp CSV</h2>
  </div>
  <div class="card-body">
  <a href="?template=1" class="btn btn--secondary btn--sm w-full mb-md">
  <i data-lucide="download"></i>
  Ladda ner mall
  </a>

  <form method="POST" enctype="multipart/form-data">
  <?= csrf_field() ?>
  <input type="hidden" name="action" value="preview">

  <div class="form-group mb-md">
  <input type="file" name="csv_file" id="csv_file" class="input input-sm" accept=".csv,.txt" required>
  </div>

  <button type="submit" class="btn btn--primary btn--sm w-full">
  <i data-lucide="eye"></i>
  Förhandsgranska
  </button>
  </form>

  <hr class="gs-my-md">

  <p class="text-xs text-secondary mb-sm"><strong>Obligatoriskt:</strong></p>
  <p class="text-xs text-secondary mb-sm">Namn, Datum</p>

  <p class="text-xs text-secondary mb-sm"><strong>Valfritt:</strong></p>
  <p class="text-xs text-secondary">
  Advent ID, Plats, Bana, Disciplin, Distans, Höjdmeter, Arrangör, Webbplats, Anmälningsfrist, E-post, Telefon
  </p>
  </div>
 </div>
 </div>

 <!-- Preview / Results -->
 <div class="gs-lg-col-span-3">
 <?php if (!empty($previewData)): ?>
  <div class="card">
  <div class="card-header flex justify-between items-center">
  <h2 class="">
  Förhandsgranskning
  <span class="badge badge-secondary badge-sm ml-sm"><?= count($previewData) ?></span>
  </h2>
  <form method="POST" style="display: inline;">
  <?= csrf_field() ?>
  <input type="hidden" name="action" value="import">
  <button type="submit" class="btn btn-success btn--sm">
   <i data-lucide="download"></i>
   Importera
  </button>
  </form>
  </div>
  <div class="card-body gs-p-0">
  <div class="table-responsive">
  <table class="table table-sm">
   <thead>
   <tr>
   <th style="width: 50px;"></th>
   <th>Namn</th>
   <th>Datum</th>
   <th>Plats</th>
   <th>Bana</th>
   <th>Disciplin</th>
   </tr>
   </thead>
   <tbody>
   <?php foreach ($previewData as $preview): ?>
   <tr>
   <td class="text-center">
    <?php if ($preview['status'] === 'ready'): ?>
    <span class="text-success">✓</span>
    <?php else: ?>
    <span class="text-error" title="<?= h($preview['error'] ?? '') ?>">✗</span>
    <?php endif; ?>
   </td>
   <td><strong><?= h($preview['name']) ?></strong></td>
   <td>
    <?php if (isset($preview['parsed_date'])): ?>
    <?= $preview['parsed_date'] ?>
    <?php else: ?>
    <span class="text-error"><?= h($preview['date']) ?></span>
    <?php endif; ?>
   </td>
   <td><?= h($preview['location']) ?: '-' ?></td>
   <td>
    <?= h($preview['venue']) ?: '-' ?>
    <?php if ($preview['venue_id']): ?>
    <span class="text-success text-xs">✓</span>
    <?php endif; ?>
   </td>
   <td><?= h($preview['discipline']) ?: '-' ?></td>
   </tr>
   <?php endforeach; ?>
   </tbody>
  </table>
  </div>
  </div>
  </div>
 <?php else: ?>
  <div class="card">
  <div class="card-body text-center py-xl">
  <i data-lucide="calendar" style="width: 48px; height: 48px; opacity: 0.3;"></i>
  <p class="text-secondary mt-md">
  Ladda upp en CSV-fil för att förhandsgranska events
  </p>
  </div>
  </div>
 <?php endif; ?>
 </div>
 </div>
 </div>

<?php include __DIR__ . '/components/unified-layout-footer.php'; ?>
