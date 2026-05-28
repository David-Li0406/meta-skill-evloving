<?php
require_once __DIR__ . '/../config.php';
require_admin();

$db = getDB();

$message = '';
$messageType = 'info';
$importResults = [];

// Handle template download
if (isset($_GET['download_template'])) {
 header('Content-Type: text/csv; charset=utf-8');
 header('Content-Disposition: attachment; filename="klubbar_mall.csv"');

 $output = fopen('php://output', 'w');

 // Add BOM for Excel UTF-8 compatibility
 fprintf($output, chr(0xEF).chr(0xBB).chr(0xBF));

 // Header row
 fputcsv($output, [
 'name',
 'short_name',
 'scf_id',
 'org_number',
 'description',
 'logo',
 'address',
 'postal_code',
 'city',
 'region',
 'country',
 'email',
 'phone',
 'contact_person',
 'website',
 'facebook',
 'instagram'
 ], ';');

 // Example row
 fputcsv($output, [
 'Exempelklubb CK',
 'ECK',
 'SCF-12345',
 '802000-0000',
 'En kort beskrivning av klubben',
 'https://example.com/logo.png',
 'Storgatan 1',
 '123 45',
 'Stockholm',
 'Stockholms län',
 'Sverige',
 'info@exempelklubb.se',
 '070-123 45 67',
 'Anna Andersson',
 'https://exempelklubb.se',
 'https://facebook.com/exempelklubb',
 'https://instagram.com/exempelklubb'
 ], ';');

 fclose($output);
 exit;
}

// Handle import
if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_FILES['import_file'])) {
 checkCsrf();

 $file = $_FILES['import_file'];

 if ($file['error'] !== UPLOAD_ERR_OK) {
 $message = 'Fel vid uppladdning av fil';
 $messageType = 'error';
 } elseif (!in_array($file['type'], ['text/csv', 'application/vnd.ms-excel', 'text/plain'])) {
 $message = 'Endast CSV-filer stöds';
 $messageType = 'error';
 } else {
 $handle = fopen($file['tmp_name'], 'r');

 if ($handle) {
 // Skip BOM if present
 $bom = fread($handle, 3);
 if ($bom !== chr(0xEF).chr(0xBB).chr(0xBF)) {
 rewind($handle);
 }

 // Read header row
 $header = fgetcsv($handle, 0, ';');

 if (!$header || !in_array('name', $header)) {
 $message = 'Ogiltig CSV-fil. Saknar kolumnrubriker.';
 $messageType = 'error';
 } else {
 $imported = 0;
 $updated = 0;
 $errors = 0;
 $rowNum = 1;

 while (($row = fgetcsv($handle, 0, ';')) !== false) {
  $rowNum++;

  // Skip empty rows
  if (empty(array_filter($row))) {
  continue;
  }

  // Map columns to values
  $data = [];
  foreach ($header as $i => $col) {
  $data[$col] = isset($row[$i]) ? trim($row[$i]) : '';
  }

  // Skip if no name
  if (empty($data['name'])) {
  $importResults[] = ['row' => $rowNum, 'status' => 'error', 'message' => 'Klubbnamn saknas'];
  $errors++;
  continue;
  }

  // Prepare club data
  $clubData = [
  'name' => $data['name'],
  'short_name' => $data['short_name'] ?? '',
  'scf_id' => $data['scf_id'] ?? '',
  'org_number' => $data['org_number'] ?? '',
  'description' => $data['description'] ?? '',
  'logo' => $data['logo'] ?? '',
  'address' => $data['address'] ?? '',
  'postal_code' => $data['postal_code'] ?? '',
  'city' => $data['city'] ?? '',
  'region' => $data['region'] ?? '',
  'country' => $data['country'] ?: 'Sverige',
  'email' => $data['email'] ?? '',
  'phone' => $data['phone'] ?? '',
  'contact_person' => $data['contact_person'] ?? '',
  'website' => $data['website'] ?? '',
  'facebook' => $data['facebook'] ?? '',
  'instagram' => $data['instagram'] ?? '',
  'active' => 1
  ];

  try {
  // Check if club exists (by name or SCF ID)
  $existing = null;
  if (!empty($data['scf_id'])) {
  $existing = $db->getRow("SELECT id FROM clubs WHERE scf_id = ?", [$data['scf_id']]);
  }
  if (!$existing) {
  $existing = $db->getRow("SELECT id FROM clubs WHERE name = ?", [$data['name']]);
  }

  if ($existing) {
  // Update existing
  $db->update('clubs', $clubData, 'id = ?', [$existing['id']]);
  $importResults[] = ['row' => $rowNum, 'status' => 'updated', 'message' => $data['name']];
  $updated++;
  } else {
  // Insert new
  $db->insert('clubs', $clubData);
  $importResults[] = ['row' => $rowNum, 'status' => 'imported', 'message' => $data['name']];
  $imported++;
  }
  } catch (Exception $e) {
  $importResults[] = ['row' => $rowNum, 'status' => 'error', 'message' => $e->getMessage()];
  $errors++;
  }
 }

 fclose($handle);

 $message ="Import klar: $imported nya klubbar, $updated uppdaterade";
 if ($errors > 0) {
  $message .=", $errors fel";
  $messageType = 'warning';
 } else {
  $messageType = 'success';
 }
 }
 } else {
 $message = 'Kunde inte läsa filen';
 $messageType = 'error';
 }
 }
}

$page_title = 'Importera Klubbar';
$page_group = 'import';
include __DIR__ . '/components/unified-layout.php';
?>

 <!-- Messages -->
 <?php if ($message): ?>
 <div class="alert alert-<?= $messageType ?> mb-lg">
 <i data-lucide="<?= $messageType === 'success' ? 'check-circle' : ($messageType === 'error' ? 'alert-circle' : 'alert-triangle') ?>"></i>
 <?= h($message) ?>
 </div>
 <?php endif; ?>

 <div class="grid grid-cols-1 gs-lg-grid-cols-2 gap-lg">
 <!-- Download Template -->
 <div class="card">
 <div class="card-header">
  <h2 class="text-primary">
  <i data-lucide="download"></i>
  1. Ladda ner mall
  </h2>
 </div>
 <div class="card-body">
  <p class="text-secondary mb-lg">
  Ladda ner CSV-mallen och fyll i klubbinformation. Öppna filen i Excel eller
  motsvarande program. Spara som CSV med semikolon (;) som avgränsare.
  </p>

  <a href="?download_template=1" class="btn btn--primary">
  <i data-lucide="download"></i>
  Ladda ner mall (CSV)
  </a>

  <div class="mt-lg text-sm text-secondary">
  <strong>Kolumner i mallen:</strong>
  <ul class="mt-sm" style="padding-left: 1.5rem;">
  <li>name (obligatorisk)</li>
  <li>short_name, scf_id, org_number</li>
  <li>description, logo</li>
  <li>address, postal_code, city, region, country</li>
  <li>email, phone, contact_person</li>
  <li>website, facebook, instagram</li>
  </ul>
  </div>
 </div>
 </div>

 <!-- Upload -->
 <div class="card">
 <div class="card-header">
  <h2 class="text-primary">
  <i data-lucide="upload"></i>
  2. Ladda upp fil
  </h2>
 </div>
 <div class="card-body">
  <form method="POST" enctype="multipart/form-data">
  <?= csrf_field() ?>

  <div class="mb-lg">
  <label for="import_file" class="label">Välj CSV-fil</label>
  <input
  type="file"
  id="import_file"
  name="import_file"
  class="input"
  accept=".csv"
  required
  >
  </div>

  <div class="alert alert--info mb-lg">
  <i data-lucide="info"></i>
  <div>
  <strong>Notera:</strong>
  <ul class="mt-sm" style="padding-left: 1.5rem; margin: 0;">
   <li>Befintliga klubbar uppdateras (matchas på namn eller SCF-ID)</li>
   <li>Nya klubbar skapas automatiskt</li>
   <li>Filen måste vara sparad som CSV med semikolon (;) som avgränsare</li>
  </ul>
  </div>
  </div>

  <button type="submit" class="btn btn--primary">
  <i data-lucide="upload"></i>
  Importera
  </button>
  </form>
 </div>
 </div>
 </div>

 <!-- Import Results -->
 <?php if (!empty($importResults)): ?>
 <div class="card mt-lg">
 <div class="card-header">
  <h2 class="text-primary">
  <i data-lucide="list"></i>
  Importresultat
  </h2>
 </div>
 <div class="card-body">
  <div class="table-responsive">
  <table class="table">
  <thead>
  <tr>
   <th>Rad</th>
   <th>Status</th>
   <th>Meddelande</th>
  </tr>
  </thead>
  <tbody>
  <?php foreach ($importResults as $result): ?>
   <tr>
   <td><?= $result['row'] ?></td>
   <td>
   <?php if ($result['status'] === 'imported'): ?>
   <span class="badge badge-success">Ny</span>
   <?php elseif ($result['status'] === 'updated'): ?>
   <span class="badge badge-primary">Uppdaterad</span>
   <?php else: ?>
   <span class="badge badge-danger">Fel</span>
   <?php endif; ?>
   </td>
   <td><?= h($result['message']) ?></td>
   </tr>
  <?php endforeach; ?>
  </tbody>
  </table>
  </div>
 </div>
 </div>
 <?php endif; ?>
<?php include __DIR__ . '/components/unified-layout-footer.php'; ?>
