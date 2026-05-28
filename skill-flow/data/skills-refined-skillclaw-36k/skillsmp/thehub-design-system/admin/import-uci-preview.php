<?php
/**
 * UCI Import with Preview System
 * Two-phase import: Preview → Confirm → Save
 */
require_once __DIR__ . '/../config.php';
require_once __DIR__ . '/../includes/helpers.php';
require_admin();

$db = getDB();
$current_admin = get_current_admin();
require_once __DIR__ . '/../includes/import-history.php';

$message = '';
$messageType = 'info';
$preview_data = null;
$stats = null;

/**
 * Parse Swedish personnummer (10 or 12 digits) and extract birth year
 * Formats:
 * - 12 digits: YYYYMMDDXXXX or YYYYMMDD-XXXX → extract YYYY
 * - 10 digits: YYMMDDXXXX or YYMMDD-XXXX → convert YY to YYYY
 * - Just year: YYYY → return as-is
 * @param string $pnr Personnummer string
 * @return int|null Birth year (4 digits) or null if parsing failed
 */
function parsePersonnummer($pnr) {
    if (empty($pnr)) {
        return null;
    }

    // Remove whitespace, dashes, and plus signs
    $pnr = preg_replace('/[\s\-\+]/', '', trim($pnr));

    // If it's already just a 4-digit year, return it
    if (preg_match('/^\d{4}$/', $pnr)) {
        $year = (int)$pnr;
        if ($year >= 1900 && $year <= date('Y')) {
            return $year;
        }
    }

    // 12 digits: YYYYMMDDXXXX
    if (preg_match('/^(\d{4})\d{8}$/', $pnr, $matches)) {
        $year = (int)$matches[1];
        if ($year >= 1900 && $year <= date('Y')) {
            return $year;
        }
    }

    // 10 digits: YYMMDDXXXX
    if (preg_match('/^(\d{2})\d{8}$/', $pnr, $matches)) {
        $yy = (int)$matches[1];
        $currentYear = (int)date('Y');
        $currentCentury = (int)floor($currentYear / 100) * 100;

        // Determine century: if YY > current year's last 2 digits, it's previous century
        if ($yy > ($currentYear % 100)) {
            $year = $currentCentury - 100 + $yy;
        } else {
            $year = $currentCentury + $yy;
        }

        return $year;
    }

    // 8 digits without last 4: YYYYMMDD
    if (preg_match('/^(\d{4})\d{4}$/', $pnr, $matches)) {
        $year = (int)$matches[1];
        if ($year >= 1900 && $year <= date('Y')) {
            return $year;
        }
    }

    // 6 digits: YYMMDD
    if (preg_match('/^(\d{2})\d{4}$/', $pnr, $matches)) {
        $yy = (int)$matches[1];
        $currentYear = (int)date('Y');
        $currentCentury = (int)floor($currentYear / 100) * 100;

        if ($yy > ($currentYear % 100)) {
            $year = $currentCentury - 100 + $yy;
        } else {
            $year = $currentCentury + $yy;
        }

        return $year;
    }

    return null;
}

// ============================================================================
// PHASE 1: UPLOAD & PREVIEW
// ============================================================================
if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_FILES['uci_file']) && !isset($_POST['confirm_import'])) {
 checkCsrf();

 $file = $_FILES['uci_file'];

 // Validate file
 if ($file['error'] !== UPLOAD_ERR_OK) {
 $message = 'Filuppladdning misslyckades';
 $messageType = 'error';
 } elseif ($file['size'] > MAX_UPLOAD_SIZE) {
 $message = 'Filen är för stor (max ' . (MAX_UPLOAD_SIZE / 1024 / 1024) . 'MB)';
 $messageType = 'error';
 } else {
 $extension = strtolower(pathinfo($file['name'], PATHINFO_EXTENSION));

 if ($extension !== 'csv') {
  $message = 'Ogiltigt filformat. Endast CSV tillåten.';
  $messageType = 'error';
 } else {
  // Save temporarily
  $temp_path = UPLOADS_PATH . '/' . time() . '_preview_' . basename($file['name']);

  if (move_uploaded_file($file['tmp_name'], $temp_path)) {
  try {
   // Parse and preview WITHOUT saving to database
   $preview_data = parseUCIForPreview($temp_path, $db);

   // Store in session for confirmation step
   $_SESSION['import_preview'] = [
   'file_path' => $temp_path,
   'filename' => $file['name'],
   'data' => $preview_data
   ];

   $message = 'Förhandsgranskning klar! Granska data nedan och bekräfta för att spara.';
   $messageType = 'info';

  } catch (Exception $e) {
   $message = 'Parsning misslyckades: ' . $e->getMessage();
   $messageType = 'error';
   @unlink($temp_path);
  }
  } else {
  $message = 'Kunde inte ladda upp filen';
  $messageType = 'error';
  }
 }
 }
}

// ============================================================================
// PHASE 2: CONFIRM & SAVE
// ============================================================================
if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['confirm_import'])) {
 checkCsrf();

 if (!isset($_SESSION['import_preview'])) {
 $message = 'Ingen förhandsgranskning hittades. Försök igen.';
 $messageType = 'error';
 } else {
 $preview = $_SESSION['import_preview'];
 $file_path = $preview['file_path'];

 try {
  // Start import history tracking
  $importId = startImportHistory(
  $db,
  'uci',
  $preview['filename'],
  filesize($file_path),
  $current_admin['username'] ?? 'admin'
  );

  // Actually save to database
  $result = savePreviewedData($preview['data'], $db, $importId);

  $stats = $result['stats'];
  $errors = $result['errors'];

  // Update import history
  $importStatus = ($stats['success'] > 0 || $stats['updated'] > 0) ? 'completed' : 'failed';
  updateImportHistory($db, $importId, $stats, $errors, $importStatus);

  if ($stats['success'] > 0 || $stats['updated'] > 0) {
  $message ="✅ Import genomförd! {$stats['success']} nya riders, {$stats['updated']} uppdaterade. <a href='/admin/import-history.php' class='gs-text-underline'>Visa historik</a>";
  $messageType = 'success';
  } else {
  $message ="Ingen data importerades.";
  $messageType = 'error';
  }

  // Cleanup
  @unlink($file_path);
  unset($_SESSION['import_preview']);

 } catch (Exception $e) {
  $message = 'Import misslyckades: ' . $e->getMessage();
  $messageType = 'error';

  if (isset($importId)) {
  updateImportHistory($db, $importId, ['total' => 0], [$e->getMessage()], 'failed');
  }
 }
 }
}

// ============================================================================
// CANCEL PREVIEW
// ============================================================================
if (isset($_GET['cancel']) && isset($_SESSION['import_preview'])) {
 $preview = $_SESSION['import_preview'];
 @unlink($preview['file_path']);
 unset($_SESSION['import_preview']);
 header('Location: /admin/import-uci-preview.php');
 exit;
}

// Restore preview if in session
if (isset($_SESSION['import_preview']) && !$preview_data) {
 $preview_data = $_SESSION['import_preview']['data'];
}

// ============================================================================
// HELPER FUNCTIONS
// ============================================================================

/**
 * Parse UCI CSV for preview (does NOT save to database)
 */
function parseUCIForPreview($filepath, $db) {
 require_once __DIR__ . '/../admin/import-uci.php'; // Reuse helper functions

 // Convert encoding
 ensureUTF8($filepath);

 if (($handle = fopen($filepath, 'r')) === false) {
 throw new Exception('Kunde inte öppna filen');
 }

 // Auto-detect separator
 $separator = detectCsvSeparator($filepath);

 // Skip header if exists
 $first_line = fgets($handle);
 if (!preg_match('/^\d{8}-\d{4}/', $first_line)) {
 // Header found, continue
 } else {
 rewind($handle);
 }

 $preview_riders = [];
 $line_number = 1;
 $clubCache = [];

 while (($line = fgets($handle)) !== false && count($preview_riders) < 500) { // Limit to 500 rows
 $line_number++;

 if (trim($line) === '') continue;

 try {
  $row = str_getcsv($line, $separator);

  // Pad to 11 columns
  while (count($row) < 11) {
  $row[] = '';
  }

  $row = array_map('trim', $row);

  // Extract data
  // Note: personnummer from CSV is only used to extract birth_year - NOT stored in database
  $personnummer = $row[0]; // Used to extract birth_year only
  $firstname = $row[1];
  $lastname = $row[2];
  $email = $row[4];
  $club_name = $row[5];
  $discipline = $row[6];
  $gender_raw = $row[7];
  $license_category = $row[8];
  $license_year = $row[9];
  $uci_code = $row[10];

  // Validate
  $status = 'ready';
  $message = '';

  if (empty($firstname) || empty($lastname)) {
  $status = 'error';
  $message = 'Saknar namn';
  } else {
  // Parse birth year
  $birth_year = parsePersonnummer($personnummer);
  if (!$birth_year) {
   $status = 'warning';
   $message = 'Ogiltigt personnummer';
  }

  // Gender
  $gender = 'M';
  if (stripos($gender_raw, 'women') !== false || stripos($gender_raw, 'dam') !== false) {
   $gender = 'F';
  }

  // UCI ID or generate SWE-ID
  $license_number = !empty($uci_code) ? $uci_code : 'SWE-' . str_pad($line_number, 6, '0', STR_PAD_LEFT);

  // License type
  $license_type = 'Base';
  if (stripos($license_category, 'Master') !== false) {
   $license_type = 'Master';
  } elseif (stripos($license_category, 'Elite') !== false) {
   $license_type = 'Elite';
  } elseif (stripos($license_category, 'Youth') !== false) {
   $license_type = 'Youth';
  }

  // License valid until
  $license_valid_until = null;
  if (!empty($license_year) && is_numeric($license_year)) {
   $license_valid_until = $license_year . '-12-31';
  }

  // Check if club exists (for preview)
  $club_status = 'new';
  if (!empty($club_name)) {
   if (isset($clubCache[$club_name])) {
   $club_status = $clubCache[$club_name];
   } else {
   $existing_club = $db->getRow(
   "SELECT id FROM clubs WHERE name = ? OR name LIKE ? LIMIT 1",
    [$club_name, '%' . $club_name . '%']
   );
   $club_status = $existing_club ? 'existing' : 'new';
   $clubCache[$club_name] = $club_status;
   }
  }

  // Check if rider exists
  $rider_status = 'new';
  if (!empty($license_number)) {
   $existing_rider = $db->getRow(
   "SELECT id FROM riders WHERE license_number = ? LIMIT 1",
   [$license_number]
   );
   if ($existing_rider) {
   $rider_status = 'update';
   $message = 'Uppdaterar befintlig';
   }
  }

  if (!$existing_rider && $birth_year) {
   $existing_rider = $db->getRow(
   "SELECT id FROM riders WHERE firstname = ? AND lastname = ? AND birth_year = ? LIMIT 1",
   [$firstname, $lastname, $birth_year]
   );
   if ($existing_rider) {
   $rider_status = 'update';
   $message = 'Uppdaterar befintlig';
   }
  }

  $preview_riders[] = [
   'line' => $line_number,
   'firstname' => $firstname,
   'lastname' => $lastname,
   'birth_year' => $birth_year ?? null,
   'gender' => $gender,
   'club_name' => $club_name,
   'club_status' => $club_status,
   'license_number' => $license_number,
   'license_type' => $license_type,
   'license_category' => $license_category,
   'discipline' => $discipline,
   'license_valid_until' => $license_valid_until,
   'email' => $email,
   'status' => $status,
   'rider_status' => $rider_status,
   'message' => $message
  ];
  }

 } catch (Exception $e) {
  $preview_riders[] = [
  'line' => $line_number,
  'firstname' => '',
  'lastname' => '',
  'status' => 'error',
  'message' => $e->getMessage()
  ];
 }
 }

 fclose($handle);

 return [
 'riders' => $preview_riders,
 'separator' => $separator,
 'total' => count($preview_riders)
 ];
}

/**
 * Save previewed data to database
 */
function savePreviewedData($preview_data, $db, $importId) {
 require_once __DIR__ . '/../admin/import-uci.php'; // Reuse helper functions

 $stats = [
 'total' => 0,
 'success' => 0,
 'updated' => 0,
 'skipped' => 0,
 'failed' => 0
 ];
 $errors = [];
 $clubCache = [];

 foreach ($preview_data['riders'] as $rider_data) {
 $stats['total']++;

 // Skip errors
 if ($rider_data['status'] === 'error') {
  $stats['skipped']++;
  continue;
 }

 try {
  // Find or create club
  $club_id = null;
  if (!empty($rider_data['club_name'])) {
  $club_name = $rider_data['club_name'];

  if (isset($clubCache[$club_name])) {
   $club_id = $clubCache[$club_name];
  } else {
   $club = $db->getRow(
   "SELECT id FROM clubs WHERE name = ? OR name LIKE ? LIMIT 1",
   [$club_name, '%' . $club_name . '%']
   );

   if (!$club) {
   $club_id = $db->insert('clubs', [
    'name' => $club_name,
    'country' => 'Sverige',
    'active' => 1
   ]);
   } else {
   $club_id = $club['id'];
   }

   $clubCache[$club_name] = $club_id;
  }
  }

  // Prepare rider data
  $riderData = [
  'firstname' => $rider_data['firstname'],
  'lastname' => $rider_data['lastname'],
  'birth_year' => $rider_data['birth_year'],
  'gender' => $rider_data['gender'],
  'club_id' => $club_id,
  'license_number' => $rider_data['license_number'],
  'license_type' => $rider_data['license_type'],
  'license_category' => $rider_data['license_category'],
  'discipline' => $rider_data['discipline'],
  'license_valid_until' => $rider_data['license_valid_until'],
  'email' => !empty($rider_data['email']) ? $rider_data['email'] : null,
  'active' => 1
  ];

  // Check if exists
  $existing = null;
  if (!empty($rider_data['license_number'])) {
  $existing = $db->getRow(
  "SELECT id FROM riders WHERE license_number = ? LIMIT 1",
   [$rider_data['license_number']]
  );
  }

  if (!$existing && $rider_data['birth_year']) {
  $existing = $db->getRow(
  "SELECT id FROM riders WHERE firstname = ? AND lastname = ? AND birth_year = ? LIMIT 1",
   [$rider_data['firstname'], $rider_data['lastname'], $rider_data['birth_year']]
  );
  }

  if ($existing) {
  // Get old data for rollback
  $oldData = null;
  if ($importId) {
   $oldData = $db->getRow("SELECT * FROM riders WHERE id = ?", [$existing['id']]);
  }

  // Update
  $db->update('riders', $riderData, 'id = ?', [$existing['id']]);
  $stats['updated']++;

  // Track
  if ($importId) {
   trackImportRecord($db, $importId, 'rider', $existing['id'], 'updated', $oldData);
  }
  } else {
  // Insert
  $riderId = $db->insert('riders', $riderData);
  $stats['success']++;

  // Track
  if ($importId && $riderId) {
   trackImportRecord($db, $importId, 'rider', $riderId, 'created');
  }
  }

 } catch (Exception $e) {
  $stats['failed']++;
  $errors[] ="Rad {$rider_data['line']}:" . $e->getMessage();
 }
 }

 return [
 'stats' => $stats,
 'errors' => $errors
 ];
}

// Page title
$page_title = 'UCI Import med Förhandsgranskning';
$page_group = 'import';
include __DIR__ . '/components/unified-layout.php';
?>

 <!-- Messages -->
 <?php if ($message): ?>
  <div class="alert alert-<?= h($messageType) ?> mb-lg">
  <i data-lucide="<?= $messageType === 'success' ? 'check-circle' : ($messageType === 'error' ? 'alert-circle' : 'info') ?>"></i>
  <?= h($message) ?>
  </div>
 <?php endif; ?>

 <?php if (!$preview_data): ?>
  <!-- STEP 1: Upload Form -->
  <div class="card">
  <div class="card-header">
   <h2 class="">
   <i data-lucide="file-up"></i>
   Steg 1: Ladda upp CSV-fil
   </h2>
  </div>
  <div class="card-body">
   <form method="POST" enctype="multipart/form-data">
   <?= csrf_field() ?>

   <div class="form-group">
    <label for="uci_file" class="label">
    <i data-lucide="file-text"></i>
    UCI CSV-fil
    </label>
    <input type="file"
     id="uci_file"
     name="uci_file"
     class="input"
     accept=".csv"
     required>
    <p class="text-sm text-secondary mt-sm">
    Maximalt <?= MAX_UPLOAD_SIZE / 1024 / 1024 ?>MB.
    CSV format från SCF/UCI.
    </p>
   </div>

   <button type="submit" class="btn btn--primary btn-lg">
    <i data-lucide="search"></i>
    Förhandsgranska
   </button>
   </form>

   <div class="alert alert--info mt-lg">
   <h4>💡 Så fungerar förhandsgranskning:</h4>
   <ol>
    <li>Ladda upp CSV-fil → <strong>Ingen data sparas ännu</strong></li>
    <li>Granska parsad data → Se fel och varningar</li>
    <li>Bekräfta → Data sparas till databasen</li>
    <li>Rollback tillgänglig → Kan ångra om något blir fel</li>
   </ol>
   </div>
  </div>
  </div>

 <?php else: ?>
  <!-- STEP 2: Preview & Confirm -->
  <div class="card">
  <div class="card-header flex justify-between items-center">
   <h2 class="">
   <i data-lucide="eye"></i>
   Steg 2: Granska data
   </h2>
   <div>
   <span class="badge badge-info">
    <?= count($preview_data['riders']) ?> rader
   </span>
   <span class="badge badge-secondary">
    Separator: <?= $preview_data['separator'] ==="\t" ? 'TAB' : $preview_data['separator'] ?>
   </span>
   </div>
  </div>
  <div class="card-body">

   <!-- Statistics -->
   <?php
   $ready = 0;
   $updates = 0;
   $warnings = 0;
   $errors_count = 0;
   $new_clubs = 0;

   foreach ($preview_data['riders'] as $r) {
   if ($r['status'] === 'ready') $ready++;
   if ($r['status'] === 'warning') $warnings++;
   if ($r['status'] === 'error') $errors_count++;
   if ($r['rider_status'] === 'update') $updates++;
   if ($r['club_status'] === 'new' && !empty($r['club_name'])) $new_clubs++;
   }
   ?>

   <div class="grid grid-cols-2 gs-md-grid-cols-4 gap-md mb-lg">
   <div class="stat-card-success">
    <div class="stat-number-success"><?= $ready ?></div>
    <div class="stat-label-success">✓ Redo att spara</div>
   </div>
   <div class="stat-card-info">
    <div class="stat-number-info"><?= $updates ?></div>
    <div class="stat-label-info">⟳ Uppdaterar befintliga</div>
   </div>
   <div class="stat-card-warning">
    <div class="stat-number-warning"><?= $warnings ?></div>
    <div class="stat-label-warning">⚠ Varningar</div>
   </div>
   <div class="stat-card-error">
    <div class="stat-number-error"><?= $errors_count ?></div>
    <div class="stat-label-error">✗ Fel (hoppas över)</div>
   </div>
   </div>

   <?php if ($new_clubs > 0): ?>
   <div class="alert alert--info mb-lg">
    <i data-lucide="plus-circle"></i>
    <strong><?= $new_clubs ?> nya klubbar</strong> kommer skapas automatiskt.
   </div>
   <?php endif; ?>

   <!-- Preview Table -->
   <div class="table-responsive">
   <table class="table">
    <thead>
    <tr>
     <th>Rad</th>
     <th>Namn</th>
     <th>Födelseår</th>
     <th>Klubb</th>
     <th>Licens</th>
     <th>Kategori</th>
     <th>Status</th>
    </tr>
    </thead>
    <tbody>
    <?php foreach (array_slice($preview_data['riders'], 0, 100) as $rider): // Show first 100 ?>
     <tr class="<?=
     $rider['status'] === 'error' ? 'table-row-bg-error' :
     ($rider['status'] === 'warning' ? 'table-row-bg-warning' :
     ($rider['rider_status'] === 'update' ? 'table-row-bg-info' : 'table-row-bg-transparent'))
     ?>">
     <td><?= $rider['line'] ?></td>
     <td>
      <strong><?= h($rider['firstname'] . ' ' . $rider['lastname']) ?></strong>
      <?php if ($rider['gender'] === 'F'): ?>
      <span class="badge badge-xs badge-pink">F</span>
      <?php endif; ?>
     </td>
     <td><?= $rider['birth_year'] ?? '-' ?></td>
     <td>
      <?= h($rider['club_name']) ?>
      <?php if ($rider['club_status'] === 'new'): ?>
      <span class="badge badge-xs badge-success">ny</span>
      <?php endif; ?>
     </td>
     <td>
      <code class="gs-code-xs"><?= h($rider['license_number']) ?></code>
     </td>
     <td>
      <span class="badge badge-xs badge-secondary">
      <?= h($rider['license_type']) ?>
      </span>
     </td>
     <td>
      <?php if ($rider['status'] === 'ready'): ?>
      <?php if ($rider['rider_status'] === 'update'): ?>
       <span class="badge badge-info">⟳ Uppdatera</span>
      <?php else: ?>
       <span class="badge badge-success">✓ Ny</span>
      <?php endif; ?>
      <?php elseif ($rider['status'] === 'warning'): ?>
      <span class="badge badge-warning">⚠ <?= h($rider['message']) ?></span>
      <?php else: ?>
      <span class="badge badge-error">✗ <?= h($rider['message']) ?></span>
      <?php endif; ?>
     </td>
     </tr>
    <?php endforeach; ?>
    </tbody>
   </table>
   </div>

   <?php if (count($preview_data['riders']) > 100): ?>
   <p class="text-secondary text-center mt-md">
    Visar första 100 av <?= count($preview_data['riders']) ?> rader.
    Alla kommer importeras vid bekräftelse.
   </p>
   <?php endif; ?>

   <!-- Action Buttons -->
   <div class="flex gap-md mt-lg">
   <form method="POST" class="gs-form-flex-1">
    <?= csrf_field() ?>
    <input type="hidden" name="confirm_import" value="1">
    <button type="submit" class="btn btn--primary btn-lg w-full">
    <i data-lucide="check"></i>
    Bekräfta och spara till databas
    (<?= $ready + $warnings ?> riders)
    </button>
   </form>
   <a href="?cancel=1" class="btn btn--secondary btn-lg">
    <i data-lucide="x"></i>
    Avbryt
   </a>
   </div>

   <?php if ($errors_count > 0): ?>
   <div class="alert alert--warning mt-lg">
    <i data-lucide="alert-triangle"></i>
    <strong><?= $errors_count ?> rader kommer hoppas över</strong> på grund av fel.
    De övriga <?= $ready + $warnings ?> kommer importeras.
   </div>
   <?php endif; ?>

  </div>
  </div>
 <?php endif; ?>

 <!-- Navigation -->
 <div class="mt-lg">
  <a href="/admin/import-history.php" class="btn btn--secondary">
  <i data-lucide="history"></i>
  Visa importhistorik
  </a>
  <a href="/admin/riders.php" class="btn btn--secondary ml-sm">
  <i data-lucide="users"></i>
  Alla deltagare
  </a>
 </div>

<?php include __DIR__ . '/components/unified-layout-footer.php'; ?>
