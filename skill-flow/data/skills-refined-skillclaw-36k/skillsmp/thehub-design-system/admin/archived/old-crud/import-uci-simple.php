<?php
/**
 * UCI License Import - SIMPLIFIED & ROBUST
 * Properly detects CSV separator and encoding
 */

error_reporting(E_ALL);
ini_set('display_errors', 1);

require_once '../config.php';
require_admin();
require_once __DIR__ . '/../includes/admin-layout.php';

$db = getDB();
$pdo = $db->getConnection();

if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_FILES['csv_file'])) {
 try {
 $file = $_FILES['csv_file']['tmp_name'];

 if (!file_exists($file)) {
 throw new Exception("Uppladdad fil hittades inte");
 }

 // Convert encoding if needed
 $original_encoding = convertFileEncoding($file);
 error_log("File encoding: $original_encoding");

 // Detect separator
 $separator = detectCsvSeparator($file);
 $sep_display = $separator ==="\t" ? 'TAB' : $separator;
 error_log("Detected separator: $sep_display");

 // Open file
 $handle = fopen($file, 'r');

 // Read first line to check if it's a header
 $first_line = fgets($handle);
 $is_header = !preg_match('/^\d{8}-\d{4}/', $first_line);

 if (!$is_header) {
 // Not a header, rewind
 rewind($handle);
 }

 error_log("First line is header:" . ($is_header ? 'YES' : 'NO'));
 error_log("First line preview:" . substr($first_line, 0, 200));

 $imported = 0;
 $updated = 0;
 $errors = [];
 $line_number = $is_header ? 1 : 0;

 while (($line = fgets($handle)) !== false) {
 $line_number++;

 // Skip empty lines
 if (trim($line) === '') continue;

 try {
 // Parse CSV
 $row = str_getcsv($line, $separator);

 // Ensure minimum columns
 if (count($row) < 11) {
  error_log("Row $line_number: Only" . count($row) ." columns, expected 11");
  $errors[] ="Rad $line_number: För få kolumner (" . count($row) ." hittade, 11 krävs)";
  continue;
 }

 // Trim ALL values
 $row = array_map('trim', $row);

 // UCI FORMAT MAPPING (based on user's actual file):
 // 0: Födelsedatum (YYYYMMDD-XXXX)
 // 1: Förnamn
 // 2: Efternamn
 // 3: Land
 // 4: Epostadress
 // 5: Huvudförening (Club)
 // 6: Gren (Discipline)
 // 7: Kategori (Gender: Men/Women)
 // 8: Licenstyp (License Category: Master Men, Elite Men, etc)
 // 9: LicensÅr (Year: 2025)
 // 10: UCIKod (with spaces: 101 637 581 11)

 $personnummer = $row[0];
 $first_name = $row[1];
 $last_name = $row[2];
 $country = $row[3];
 $email = $row[4];
 $club_name = $row[5];
 $discipline = $row[6];
 $gender_raw = $row[7];
 $license_category = $row[8];
 $license_year = $row[9];
 $uci_code = $row[10];

 // VALIDATION: Check names
 if (empty($first_name) || empty($last_name)) {
  $errors[] ="Rad $line_number: Saknar namn på cyklist (Förnamn: '$first_name', Efternamn: '$last_name')";
  continue;
 }

 // Parse birth year
 $birth_year = parsePersonnummer($personnummer);
 if (!$birth_year) {
  $errors[] ="Rad $line_number: Ogiltigt personnummer '$personnummer'";
  continue;
 }

 // Convert gender: Men/Women → male/female
 $gender = strtolower(trim($gender_raw));
 if ($gender === 'men' || $gender === 'man' || $gender === 'm') {
  $gender = 'male';
 } elseif ($gender === 'women' || $gender === 'woman' || $gender === 'f') {
  $gender = 'female';
 } else {
  $gender = 'other';
 }

 // Clean UCI ID: Remove spaces, add SWE prefix if missing
 $uci_id = preg_replace('/\s+/', '', $uci_code);
 if (!empty($uci_id) && !str_starts_with($uci_id, 'SWE')) {
  $uci_id = 'SWE' . $uci_id;
 }

 // Extract license_type from license_category
 $license_type = 'Base';
 if (str_contains($license_category, 'Master')) {
  $license_type = 'Master';
 } elseif (str_contains($license_category, 'Elite')) {
  $license_type = 'Elite';
 } elseif (str_contains($license_category, 'Youth') || str_contains($license_category, 'Under')) {
  $license_type = 'Youth';
 } elseif (str_contains($license_category, 'Team Manager')) {
  $license_type = 'Team Manager';
 }

 // License valid until: year → YYYY-12-31
 $license_valid_until = $license_year . '-12-31';

 // Category = license_category
 $category = $license_category;

 // Find or create club
 $club_id = null;
 if (!empty($club_name)) {
  $stmt = $pdo->prepare("SELECT id FROM clubs WHERE name = ?");
  $stmt->execute([$club_name]);
  $club = $stmt->fetch();

  if (!$club) {
  $stmt = $pdo->prepare("INSERT INTO clubs (name, active) VALUES (?, 1)");
  $stmt->execute([$club_name]);
  $club_id = $pdo->lastInsertId();
  } else {
  $club_id = $club['id'];
  }
 }

 // Check if rider exists (by UCI ID or by name+birth_year)
 $existing = null;
 if (!empty($uci_id)) {
  $stmt = $pdo->prepare("SELECT id FROM riders WHERE license_number = ?");
  $stmt->execute([$uci_id]);
  $existing = $stmt->fetch();
 }

 if (!$existing) {
  // Try by name and birth year
  $stmt = $pdo->prepare("SELECT id FROM riders WHERE firstname = ? AND lastname = ? AND birth_year = ?");
  $stmt->execute([$first_name, $last_name, $birth_year]);
  $existing = $stmt->fetch();
 }

 if ($existing) {
  // Update existing
  $stmt = $pdo->prepare("
  UPDATE riders SET
  firstname = ?,
  lastname = ?,
  birth_year = ?,
  club_id = ?,
  gender = ?,
  license_type = ?,
  license_category = ?,
  discipline = ?,
  license_valid_until = ?,
  license_number = ?,
  email = ?
  WHERE id = ?
 ");

  $stmt->execute([
  $first_name,
  $last_name,
  $birth_year,
  $club_id,
  $gender,
  $license_type,
  $license_category,
  $discipline,
  $license_valid_until,
  $uci_id,
  $email,
  $existing['id']
  ]);

  $updated++;
 } else {
  // Insert new - use license_number field for UCI ID
  $stmt = $pdo->prepare("
  INSERT INTO riders (
  firstname, lastname, birth_year, license_number,
  club_id, gender, license_type, license_category,
  discipline, license_valid_until, email, active
  ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 1)
 ");

  $stmt->execute([
  $first_name,
  $last_name,
  $birth_year,
  $uci_id,
  $club_id,
  $gender,
  $license_type,
  $license_category,
  $discipline,
  $license_valid_until,
  $email
  ]);

  $imported++;
 }

 } catch (Exception $e) {
 error_log("Row $line_number ERROR:" . $e->getMessage());
 $errors[] ="Rad $line_number:" . $e->getMessage();
 }
 }

 fclose($handle);

 $_SESSION['import_result'] = [
 'imported' => $imported,
 'updated' => $updated,
 'errors' => $errors,
 'separator' => $sep_display,
 'encoding' => $original_encoding
 ];

 redirect('/admin/import-uci-simple.php?success=1');

 } catch (Exception $e) {
 error_log("FATAL ERROR:" . $e->getMessage());
 $_SESSION['import_error'] = $e->getMessage();
 redirect('/admin/import-uci-simple.php?error=1');
 }
}

$pageTitle = 'UCI Import (Simple)';
$pageType = 'admin';
include '../includes/layout-header.php';
?>

<main class="main-content">
 <div class="container">
 <?php render_admin_header('Import & Data'); ?>

 <?php if (isset($_GET['error'])): ?>
 <div class="alert alert--error mb-lg">
 <h3>❌ Import misslyckades</h3>
 <p><strong>Fel:</strong> <?= htmlspecialchars($_SESSION['import_error'] ?? 'Okänt fel') ?></p>
 <?php unset($_SESSION['import_error']); ?>
 </div>
 <?php endif; ?>

 <?php if (isset($_GET['success'])): ?>
 <?php $result = $_SESSION['import_result']; unset($_SESSION['import_result']); ?>
 <div class="alert alert--success mb-lg">
 <h3>✅ Import klar!</h3>
 <p><strong><?= $result['imported'] ?></strong> nya cyklister importerade</p>
 <p><strong><?= $result['updated'] ?></strong> cyklister uppdaterade</p>
 <p><small>Separator: <code><?= $result['separator'] ?></code> | Encoding: <code><?= $result['encoding'] ?></code></small></p>

 <?php if (!empty($result['errors'])): ?>
  <details class="mt-md">
  <summary class="gs-summary-pointer">
  <?= count($result['errors']) ?> fel/varningar
  </summary>
  <ul class="gs-scroll-list-300">
  <?php foreach ($result['errors'] as $error): ?>
  <li><?= htmlspecialchars($error) ?></li>
  <?php endforeach; ?>
  </ul>
  </details>
 <?php endif; ?>
 </div>
 <?php endif; ?>

 <div class="card mb-lg">
 <div class="card-header">
 <h3 class="">Format-krav</h3>
 </div>
 <div class="card-body">
 <p>Denna import hanterar CSV direkt från UCI Licensregister.</p>
 <h4 class="mt-md">Kolumner (11 st, ingen header krävs):</h4>
 <ol class="text-sm-lh16">
  <li><strong>Födelsedatum</strong> (YYYYMMDD-XXXX)</li>
  <li><strong>Förnamn</strong></li>
  <li><strong>Efternamn</strong></li>
  <li>Land</li>
  <li>Epostadress</li>
  <li><strong>Huvudförening</strong> (Klubb)</li>
  <li><strong>Gren</strong> (MTB, Road, etc)</li>
  <li>Kategori (Men/Women)</li>
  <li><strong>Licenstyp</strong> (Master Men, Elite Men, etc)</li>
  <li>LicensÅr (2025)</li>
  <li>UCIKod</li>
 </ol>
 <p class="mt-md"><strong>Separator:</strong> Detekteras automatiskt (komma, semikolon, tab, pipe)</p>
 <p><strong>Encoding:</strong> Konverteras automatiskt till UTF-8</p>
 </div>
 </div>

 <div class="card">
 <div class="card-header">
 <h3 class="">Ladda upp UCI-fil</h3>
 </div>
 <div class="card-body">
 <form method="POST" enctype="multipart/form-data">
  <?= csrf_field() ?>
  <div class="form-group">
  <label class="label">CSV-fil från UCI</label>
  <input type="file" name="csv_file" accept=".csv,.txt" class="input" required>
  </div>

  <button type="submit" class="btn btn--primary btn-lg">
  <i data-lucide="upload"></i>
  Importera cyklister
  </button>
 </form>
 </div>
 </div>
 </div>
 <?php render_admin_footer(); ?>
</main>

<?php include '../includes/layout-footer.php'; ?>
