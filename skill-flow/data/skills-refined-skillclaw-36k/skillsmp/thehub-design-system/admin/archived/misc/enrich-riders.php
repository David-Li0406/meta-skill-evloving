<?php
/**
 * Enrich Riders from Registration Data
 * Import data from old registration files to fill in missing rider information
 *
 * Use case: Riders created from results import have SWE ID but missing:
 * - Birth year
 * - Email
 * - License type
 * - Phone
 *
 * This tool matches riders by name and updates missing fields.
 */

require_once __DIR__ . '/../config.php';
require_admin();
require_once __DIR__ . '/../includes/admin-layout.php';

$db = getDB();
$message = '';
$messageType = 'info';
$matches = [];
$previewMode = false;

// Get riders with SWE ID that are missing data
$incompleteRiders = $db->getAll("
 SELECT
 r.id,
 r.firstname,
 r.lastname,
 r.license_number,
 r.birth_year,
 r.email,
 r.license_type,
 r.phone,
 r.gender
 FROM riders r
 WHERE r.license_number LIKE 'SWE%'
 AND (
 r.birth_year IS NULL
 OR r.email IS NULL OR r.email = ''
 OR r.license_type IS NULL OR r.license_type = ''
 )
 ORDER BY r.lastname, r.firstname
");

$incompleteCount = count($incompleteRiders);

// Handle file upload
if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_FILES['csv_file'])) {
 if (!verify_csrf_token($_POST['csrf_token'] ?? '')) {
 $message = 'Ogiltig CSRF-token';
 $messageType = 'error';
 } else {
 $file = $_FILES['csv_file'];

 if ($file['error'] !== UPLOAD_ERR_OK) {
  $message = 'Filuppladdning misslyckades';
  $messageType = 'error';
 } else {
  // Read CSV
  $handle = fopen($file['tmp_name'], 'r');
  if ($handle) {
  // Detect delimiter
  $firstLine = fgets($handle);
  rewind($handle);
  $delimiter = (strpos($firstLine, ';') !== false) ? ';' : ',';

  // Read header
  $header = fgetcsv($handle, 0, $delimiter);
  $header = array_map(function($h) {
   return strtolower(trim($h));
  }, $header);

  // Map columns (flexible mapping)
  $colMap = [
   'firstname' => null,
   'lastname' => null,
   'birth_year' => null,
   'email' => null,
   'license_type' => null,
   'phone' => null,
   'gender' => null,
   'license_number' => null,
  ];

  // Try to find columns
  foreach ($header as $idx => $col) {
   if (in_array($col, ['firstname', 'förnamn', 'first_name', 'first name'])) {
   $colMap['firstname'] = $idx;
   } elseif (in_array($col, ['lastname', 'efternamn', 'last_name', 'last name', 'surname'])) {
   $colMap['lastname'] = $idx;
   } elseif (in_array($col, ['birth_year', 'födelseår', 'birthyear', 'birth year', 'år'])) {
   $colMap['birth_year'] = $idx;
   } elseif (in_array($col, ['email', 'e-post', 'epost', 'mail'])) {
   $colMap['email'] = $idx;
   } elseif (in_array($col, ['license_type', 'licenstyp', 'licens', 'license'])) {
   $colMap['license_type'] = $idx;
   } elseif (in_array($col, ['phone', 'telefon', 'tel', 'mobil', 'mobile'])) {
   $colMap['phone'] = $idx;
   } elseif (in_array($col, ['gender', 'kön', 'sex'])) {
   $colMap['gender'] = $idx;
   } elseif (in_array($col, ['license_number', 'licensnummer', 'uci_id', 'uci id', 'swe_id', 'swe id'])) {
   $colMap['license_number'] = $idx;
   }
  }

  if ($colMap['firstname'] === null || $colMap['lastname'] === null) {
   $message = 'CSV måste innehålla kolumner för förnamn och efternamn';
   $messageType = 'error';
  } else {
   // Read all rows
   $csvData = [];
   while (($row = fgetcsv($handle, 0, $delimiter)) !== false) {
   $csvData[] = $row;
   }

   // Match against incomplete riders
   $matches = [];
   foreach ($incompleteRiders as $rider) {
   $riderName = strtolower(trim($rider['firstname'] . ' ' . $rider['lastname']));
   $riderNameReverse = strtolower(trim($rider['lastname'] . ' ' . $rider['firstname']));

   foreach ($csvData as $csvRow) {
    $csvFirstname = $csvRow[$colMap['firstname']] ?? '';
    $csvLastname = $csvRow[$colMap['lastname']] ?? '';
    $csvName = strtolower(trim($csvFirstname . ' ' . $csvLastname));
    $csvNameReverse = strtolower(trim($csvLastname . ' ' . $csvFirstname));

    // Match by name
    if ($csvName === $riderName || $csvNameReverse === $riderName ||
    $csvName === $riderNameReverse || $csvNameReverse === $riderNameReverse) {

    // Extract data from CSV
    $updates = [];

    if (empty($rider['birth_year']) && $colMap['birth_year'] !== null) {
     $year = $csvRow[$colMap['birth_year']] ?? '';
     if (preg_match('/\d{4}/', $year, $m)) {
     $updates['birth_year'] = (int)$m[0];
     }
    }

    if (empty($rider['email']) && $colMap['email'] !== null) {
     $email = trim($csvRow[$colMap['email']] ?? '');
     if (filter_var($email, FILTER_VALIDATE_EMAIL)) {
     $updates['email'] = $email;
     }
    }

    if (empty($rider['license_type']) && $colMap['license_type'] !== null) {
     $licenseType = trim($csvRow[$colMap['license_type']] ?? '');
     if ($licenseType) {
     $updates['license_type'] = $licenseType;
     }
    }

    if (empty($rider['phone']) && $colMap['phone'] !== null) {
     $phone = trim($csvRow[$colMap['phone']] ?? '');
     if ($phone) {
     $updates['phone'] = $phone;
     }
    }

    if (empty($rider['gender']) && $colMap['gender'] !== null) {
     $gender = strtoupper(trim($csvRow[$colMap['gender']] ?? ''));
     if (in_array($gender, ['M', 'K', 'F', 'MALE', 'FEMALE', 'MAN', 'KVINNA'])) {
     if (in_array($gender, ['F', 'FEMALE', 'KVINNA'])) $gender = 'K';
     if (in_array($gender, ['MALE', 'MAN'])) $gender = 'M';
     $updates['gender'] = $gender;
     }
    }

    // Also update license_number if CSV has a better one (UCI)
    if ($colMap['license_number'] !== null) {
     $csvLicense = trim(preg_replace('/\s+/', '', $csvRow[$colMap['license_number']] ?? ''));
     // If CSV has a UCI ID (10-11 digits starting with 100/101)
     if (preg_match('/^10[01]\d{7,8}$/', $csvLicense)) {
     $updates['license_number'] = $csvRow[$colMap['license_number']]; // Keep original format with spaces
     }
    }

    if (!empty($updates)) {
     $matches[] = [
     'rider' => $rider,
     'csv_name' => $csvFirstname . ' ' . $csvLastname,
     'updates' => $updates
     ];
    }
    break; // Found match, move to next rider
    }
   }
   }

   $previewMode = true;
   $message = 'Hittade ' . count($matches) . ' matchningar av ' . count($incompleteRiders) . ' ofullständiga ryttare';
   $messageType = count($matches) > 0 ? 'success' : 'warning';
  }

  fclose($handle);
  }
 }
 }
}

// Handle apply updates
if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['action']) && $_POST['action'] === 'apply') {
 if (!verify_csrf_token($_POST['csrf_token'] ?? '')) {
 $message = 'Ogiltig CSRF-token';
 $messageType = 'error';
 } else {
 $updateData = json_decode($_POST['update_data'] ?? '[]', true);
 $updated = 0;

 foreach ($updateData as $item) {
  $riderId = (int)$item['rider_id'];
  $updates = $item['updates'];

  if ($riderId > 0 && !empty($updates)) {
  $db->update('riders', $updates, 'id = ?', [$riderId]);
  $updated++;
  }
 }

 $message ="Uppdaterade {$updated} ryttare";
 $messageType = 'success';

 // Refresh incomplete riders list
 $incompleteRiders = $db->getAll("
  SELECT
  r.id,
  r.firstname,
  r.lastname,
  r.license_number,
  r.birth_year,
  r.email,
  r.license_type,
  r.phone,
  r.gender
  FROM riders r
  WHERE r.license_number LIKE 'SWE%'
  AND (
  r.birth_year IS NULL
  OR r.email IS NULL OR r.email = ''
  OR r.license_type IS NULL OR r.license_type = ''
  )
  ORDER BY r.lastname, r.firstname
 ");
 $incompleteCount = count($incompleteRiders);
 }
}

$pageTitle = 'Berika Ryttardata';
$pageType = 'admin';
include __DIR__ . '/../includes/layout-header.php';
?>

<main class="main-content">
 <div class="container">
 <?php render_admin_header('Berika Ryttardata', 'settings'); ?>

 <?php if ($message): ?>
  <div class="alert alert-<?= $messageType ?> mb-lg">
  <i data-lucide="<?= $messageType === 'success' ? 'check-circle' : ($messageType === 'error' ? 'alert-circle' : 'alert-triangle') ?>"></i>
  <?= h($message) ?>
  </div>
 <?php endif; ?>

 <!-- Info -->
 <div class="alert alert--info mb-lg">
  <i data-lucide="info"></i>
  <div>
  <strong>Berika ryttare med SWE ID</strong><br>
  Ryttare skapade från resultatimport saknar ofta födelseår, e-post och licenstyp.<br>
  Ladda upp en CSV från gamla anmälningar för att fylla i saknad data.<br><br>
  <strong>CSV-kolumner som stöds:</strong> förnamn/firstname, efternamn/lastname, födelseår/birth_year, e-post/email, licenstyp/license_type, telefon/phone, kön/gender, licensnummer/license_number
  </div>
 </div>

 <!-- Stats -->
 <div class="card mb-lg">
  <div class="card-header">
  <h2 class="text-primary">
   <i data-lucide="users"></i>
   Ryttare med SWE ID som saknar data
  </h2>
  </div>
  <div class="card-body">
  <div class="text-center">
   <span class="gs-text-4xl font-bold text-warning"><?= $incompleteCount ?></span>
   <span class="text-secondary"> ryttare</span>
  </div>
  </div>
 </div>

 <?php if (!$previewMode || empty($matches)): ?>
 <!-- Upload Form -->
 <div class="card mb-lg">
  <div class="card-header">
  <h2 class="text-primary">
   <i data-lucide="upload"></i>
   Ladda upp anmälningsdata (CSV)
  </h2>
  </div>
  <div class="card-body">
  <form method="POST" enctype="multipart/form-data">
   <?= csrf_field() ?>
   <div class="form-group">
   <label class="label">Välj CSV-fil</label>
   <input type="file" name="csv_file" accept=".csv,.txt" class="input" required>
   <small class="text-secondary">CSV med semikolon (;) eller komma (,) som separator</small>
   </div>
   <button type="submit" class="btn btn--primary">
   <i data-lucide="search"></i>
   Sök matchningar
   </button>
  </form>
  </div>
 </div>
 <?php endif; ?>

 <?php if ($previewMode && !empty($matches)): ?>
 <!-- Preview Matches -->
 <div class="card mb-lg">
  <div class="card-header flex justify-between items-center">
  <h2 class="text-success">
   <i data-lucide="check-circle"></i>
   Förhandsgranska uppdateringar (<?= count($matches) ?>)
  </h2>
  <form method="POST" style="display: inline;">
   <?= csrf_field() ?>
   <input type="hidden" name="action" value="apply">
   <input type="hidden" name="update_data" value="<?= h(json_encode(array_map(function($m) {
   return ['rider_id' => $m['rider']['id'], 'updates' => $m['updates']];
   }, $matches))) ?>">
   <button type="submit" class="btn btn-success" onclick="return confirm('Tillämpa alla <?= count($matches) ?> uppdateringar?')">
   <i data-lucide="check"></i>
   Tillämpa alla uppdateringar
   </button>
  </form>
  </div>
  <div class="card-body">
  <div class="table-responsive">
   <table class="table">
   <thead>
    <tr>
    <th>Ryttare</th>
    <th>Nuvarande SWE ID</th>
    <th>Uppdateringar</th>
    </tr>
   </thead>
   <tbody>
    <?php foreach ($matches as $match): ?>
    <tr>
    <td>
     <a href="/rider.php?id=<?= $match['rider']['id'] ?>" target="_blank">
     <?= h($match['rider']['firstname'] . ' ' . $match['rider']['lastname']) ?>
     </a>
    </td>
    <td><code><?= h($match['rider']['license_number']) ?></code></td>
    <td>
     <?php foreach ($match['updates'] as $field => $value): ?>
     <span class="badge badge-success gs-mr-xs">
      <?= h($field) ?>: <?= h($value) ?>
     </span>
     <?php endforeach; ?>
    </td>
    </tr>
    <?php endforeach; ?>
   </tbody>
   </table>
  </div>
  </div>
 </div>

 <!-- Upload new file button -->
 <div class="text-center">
  <a href="?" class="btn btn--secondary">
  <i data-lucide="upload"></i>
  Ladda upp ny fil
  </a>
 </div>
 <?php endif; ?>

 <!-- List of incomplete riders -->
 <?php if (!$previewMode && $incompleteCount > 0): ?>
 <div class="card">
  <div class="card-header">
  <h2 class="text-warning">
   <i data-lucide="alert-triangle"></i>
   Ofullständiga SWE ID-ryttare (visar max 50)
  </h2>
  </div>
  <div class="card-body">
  <div class="table-responsive">
   <table class="table">
   <thead>
    <tr>
    <th>Namn</th>
    <th>SWE ID</th>
    <th>Födelseår</th>
    <th>E-post</th>
    <th>Licenstyp</th>
    </tr>
   </thead>
   <tbody>
    <?php foreach (array_slice($incompleteRiders, 0, 50) as $rider): ?>
    <tr>
    <td>
     <a href="/rider.php?id=<?= $rider['id'] ?>" target="_blank">
     <?= h($rider['firstname'] . ' ' . $rider['lastname']) ?>
     </a>
    </td>
    <td><code><?= h($rider['license_number']) ?></code></td>
    <td class="<?= empty($rider['birth_year']) ? 'text-error' : '' ?>">
     <?= $rider['birth_year'] ?: '❌ Saknas' ?>
    </td>
    <td class="<?= empty($rider['email']) ? 'text-error' : '' ?>">
     <?= $rider['email'] ?: '❌ Saknas' ?>
    </td>
    <td class="<?= empty($rider['license_type']) ? 'text-error' : '' ?>">
     <?= $rider['license_type'] ?: '❌ Saknas' ?>
    </td>
    </tr>
    <?php endforeach; ?>
   </tbody>
   </table>
  </div>
  </div>
 </div>
 <?php endif; ?>

 <?php render_admin_footer(); ?>
 </div>
</main>

<?php include __DIR__ . '/../includes/layout-footer.php'; ?>
