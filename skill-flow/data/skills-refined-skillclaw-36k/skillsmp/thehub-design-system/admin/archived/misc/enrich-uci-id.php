<?php
/**
 * Berika UCI-ID Tool för TheHUB
 * Söker upp saknade UCI-ID från databasen innan import
 */
require_once __DIR__ . '/../config.php';
require_admin();

$db = getDB();
$current_admin = get_current_admin();

$message = '';
$messageType = 'info';
$riders_with_missing_uci = [];
$csv_data = [];
$upload_step = true;

// Steg 1: CSV upload och parsing
if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_FILES['csv_file'])) {
 checkCsrf();

 $file = $_FILES['csv_file'];
 $selectedEventId = !empty($_POST['event_id']) ? (int)$_POST['event_id'] : null;

 // Validera event
 if (!$selectedEventId) {
 $message = 'Du måste välja ett event';
 $messageType = 'error';
 } elseif ($file['error'] !== UPLOAD_ERR_OK) {
 $message = 'Filuppladdning misslyckades';
 $messageType = 'error';
 } else {
 // Läs CSV - använd samma logik som import-results.php
 $csv_rows = [];
 if (($handle = fopen($file['tmp_name'], 'r')) !== FALSE) {
 $headers = null;
 $row_num = 0;

 while (($row = fgetcsv($handle)) !== FALSE) {
 $row_num++;

 if (!$headers) {
  $headers = $row;
  continue;
 }

 // Associera värdena med headers
 $record = array_combine($headers, $row);
 $csv_rows[] = [
  'row_num' => $row_num,
  'data' => $record
 ];
 }
 fclose($handle);
 }

 // Hitta ryttare som saknar UCI-ID
 if (!empty($csv_rows)) {
 foreach ($csv_rows as $csv_row) {
 $data = $csv_row['data'];
 
 // Försök flera kolumnnamn (svenska och engelska)
 $uci_id = trim($data['UCI-ID'] ?? $data['UCI'] ?? $data['uci_id'] ?? $data['UCI_ID'] ?? '');
 $first_name = trim($data['FirstName'] ?? $data['Förnamn'] ?? $data['firstname'] ?? '');
 $last_name = trim($data['LastName'] ?? $data['Efternamn'] ?? $data['lastname'] ?? '');
 $club = trim($data['Club'] ?? $data['Klubb'] ?? $data['club'] ?? '');

 // Om UCI-ID saknas, sök i databasen
 if (empty($uci_id) && !empty($last_name)) {
  // Sök matchande ryttare i databasen
  $potential_matches = findRiderMatches($db, $first_name, $last_name, $club);

  if (!empty($potential_matches)) {
  $riders_with_missing_uci[] = [
  'row_num' => $csv_row['row_num'],
  'csv_data' => $data,
  'potential_matches' => $potential_matches
  ];
  }
 }
 }

 $csv_data = $csv_rows;
 $upload_step = false;

 if (!empty($riders_with_missing_uci)) {
 $_SESSION['enrich_csv_data'] = $csv_rows;
 $_SESSION['enrich_event_id'] = $selectedEventId;
 $message = 'Hittade ' . count($riders_with_missing_uci) . ' ryttare utan UCI-ID. Välj rätt matchning nedan.';
 $messageType = 'warning';
 } else {
 $message = 'Alla ryttare i filen har UCI-ID eller kunde inte matchas i databasen. Klar för import!';
 $messageType = 'success';
 }
 }
 }
}

// Steg 2: Spara UCI-ID val och skapa berikad CSV
if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['save_matches'])) {
 checkCsrf();

 if (empty($_SESSION['enrich_csv_data'])) {
 $message = 'Sessionen har utgått. Ladda upp filen igen.';
 $messageType = 'error';
 } else {
 $csv_rows = $_SESSION['enrich_csv_data'];
 $updated_rows = [];

 // Uppdatera UCI-ID baserat på admin-val
 foreach ($csv_rows as $idx => $row) {
 $row_copy = $row;
 $row_num = $row['row_num'];
 
 $choice_key = 'uci_choice_row_' . $row_num;
 if (!empty($_POST[$choice_key])) {
 $rider_id = (int)$_POST[$choice_key];

 if ($rider_id > 0) {
  // Hämta UCI-ID från vald ryttare
  $rider = $db->getRow("SELECT license_number FROM riders WHERE id = ?", [$rider_id]);
  
  if ($rider && !empty($rider['license_number'])) {
  // Uppdatera CSV-datan - försök flera kolumnnamn
  if (isset($row['data']['UCI-ID'])) {
  $row_copy['data']['UCI-ID'] = $rider['license_number'];
  } elseif (isset($row['data']['UCI'])) {
  $row_copy['data']['UCI'] = $rider['license_number'];
  } elseif (isset($row['data']['uci_id'])) {
  $row_copy['data']['uci_id'] = $rider['license_number'];
  } else {
  // Lägg till ny kolumn om den inte finns
  $row_copy['data']['UCI-ID'] = $rider['license_number'];
  }
  }
 }
 }
 
 $updated_rows[] = $row_copy;
 }

 // Generera ny CSV-fil
 $output_filename = 'enriched_' . time() . '.csv';
 $output_path = UPLOADS_PATH . '/' . $output_filename;

 if (generate_enriched_csv($output_path, $updated_rows)) {
 // Spara till session för preview
 $_SESSION['import_preview_file'] = $output_path;
 $_SESSION['import_preview_filename'] = $output_filename;
 $_SESSION['import_selected_event'] = $_SESSION['enrich_event_id'];
 $_SESSION['import_format'] = $_POST['import_format'] ?? 'enduro';

 // Rensa enrich-session
 unset($_SESSION['enrich_csv_data']);
 unset($_SESSION['enrich_event_id']);

 header('Location: /admin/import-results-preview.php');
 exit;
 } else {
 $message = 'Kunde inte generera berikad CSV-fil';
 $messageType = 'error';
 }
 }
}

// Ladda event för dropdown
$events = $db->getAll("
 SELECT id, name, date, location
 FROM events
 ORDER BY date DESC
 LIMIT 100
");

$pageTitle = 'Berika UCI-ID';
$pageType = 'admin';
include __DIR__ . '/../includes/layout-header.php';
?>

<main class="main-content">
 <div class="container">
 <!-- Header -->
 <div class="flex items-center justify-between mb-lg">
 <h1 class="text-primary">
 <i data-lucide="search"></i>
 Berika UCI-ID i Resultatfil
 </h1>
 <a href="/admin/import-results.php" class="btn btn--secondary">
 <i data-lucide="arrow-left"></i>
 Tillbaka till import
 </a>
 </div>

 <!-- Messages -->
 <?php if ($message): ?>
 <div class="alert alert-<?= $messageType ?> mb-lg">
 <i data-lucide="<?= $messageType === 'success' ? 'check-circle' : ($messageType === 'error' ? 'alert-circle' : 'alert-triangle') ?>"></i>
 <?= h($message) ?>
 </div>
 <?php endif; ?>

 <!-- Steg 1: Upload -->
 <?php if ($upload_step): ?>
 <div class="card">
 <div class="card-header">
 <h2 class="text-primary">
  <i data-lucide="upload"></i>
  Ladda upp resultatfil
 </h2>
 </div>
 <div class="card-body">
 <form method="POST" enctype="multipart/form-data" class="gs-form">
  <?= csrf_field() ?>

  <div class="form-group mb-lg">
  <label for="event_id" class="label label-lg">
  <span class="badge badge-primary mr-sm">1</span>
  Välj event
  </label>
  <select id="event_id" name="event_id" class="input input-lg" required>
  <option value="">-- Välj ett event --</option>
  <?php foreach ($events as $event): ?>
  <option value="<?= $event['id'] ?>">
   <?= h($event['name']) ?> (<?= date('Y-m-d', strtotime($event['date'])) ?>)
   <?php if ($event['location']): ?>
   - <?= h($event['location']) ?>
   <?php endif; ?>
  </option>
  <?php endforeach; ?>
  </select>
  </div>

  <div class="form-group mb-lg">
  <label for="csv_file" class="label label-lg">
  <span class="badge badge-primary mr-sm">2</span>
  CSV-fil
  </label>
  <input type="file" id="csv_file" name="csv_file" class="input input-lg" accept=".csv" required>
  <p class="text-sm text-secondary mt-sm">
  Systemet söker automatiskt efter saknade UCI-ID i databasen
  </p>
  </div>

  <button type="submit" class="btn btn--primary btn-lg w-full">
  <i data-lucide="search"></i>
  Sök saknade UCI-ID
  </button>
 </form>
 </div>
 </div>

 <!-- Info -->
 <div class="card mt-lg">
 <div class="card-header">
 <h3 class="text-primary">
  <i data-lucide="info"></i>
  Hur fungerar det?
 </h3>
 </div>
 <div class="card-body text-sm">
 <p class="mb-md">Det här verktyget hjälper dig att fylla i saknade UCI-ID innan du importerar resultat:</p>
 <ol class="ml-md">
  <li>Ladda upp din resultatfil (CSV)</li>
  <li>Systemet söker automatiskt efter ryttare i databasen baserat på namn och klubb</li>
  <li>Du väljer rätt matchning för varje ryttare</li>
  <li>En berikad CSV-fil skapas och förs vidare till import-preview</li>
 </ol>
 </div>
 </div>

 <?php else: ?>

 <!-- Steg 2: Matcha UCI-ID -->
 <form method="POST" class="gs-form">
 <?= csrf_field() ?>
 <input type="hidden" name="save_matches" value="1">
 <input type="hidden" name="import_format" value="<?= h($_POST['import_format'] ?? 'enduro') ?>">

 <?php foreach ($riders_with_missing_uci as $item): ?>
 <div class="card mb-lg">
 <div class="card-header">
  <h3 class="text-primary">
  Rad <?= $item['row_num'] ?>: <?= h($item['csv_data']['FirstName'] ?? $item['csv_data']['Förnamn'] ?? '') ?> <?= h($item['csv_data']['LastName'] ?? $item['csv_data']['Efternamn'] ?? '') ?>
  </h3>
 </div>
 <div class="card-body">
  <div class="mb-md">
  <p class="text-sm text-secondary mb-sm">
  <strong>CSV-data:</strong><br>
  Klubb: <?= h($item['csv_data']['Club'] ?? $item['csv_data']['Klubb'] ?? 'Okänd') ?><br>
  Kategori: <?= h($item['csv_data']['Category'] ?? $item['csv_data']['Klass'] ?? 'Okänd') ?>
  </p>
  </div>

  <div class="form-group">
  <label class="label">
  Välj rätt ryttare:
  </label>
  <select name="uci_choice_row_<?= $item['row_num'] ?>" class="input">
  <option value="">-- Ingen match --</option>
  <?php foreach ($item['potential_matches'] as $match): ?>
  <option value="<?= $match['id'] ?>">
   <?= h($match['firstname'] . ' ' . $match['lastname']) ?>
   (Licens: <?= h($match['license_number']) ?>, Klubb: <?= h($match['club_name']) ?>)
  </option>
  <?php endforeach; ?>
  </select>
  </div>
 </div>
 </div>
 <?php endforeach; ?>

 <div class="flex gap-md">
 <button type="submit" class="btn btn--primary btn-lg flex-1">
  <i data-lucide="check"></i>
  Spara & Gå till Preview
 </button>
 <a href="/admin/enrich-uci-id.php" class="btn btn--secondary btn-lg flex-1">
  <i data-lucide="x"></i>
  Avbryt
 </a>
 </div>
 </form>

 <?php endif; ?>
 </div>
</main>

<?php include __DIR__ . '/../includes/layout-footer.php'; ?>

<?php
/**
 * Hitta matchande ryttare i databasen
 */
function findRiderMatches($db, $first_name, $last_name, $club) {
 $matches = [];
 
 // Normalisera för sökning
 $search_lastname = strtolower(trim($last_name));
 $search_club = strtolower(trim($club));
 
 // Strategi 1: Exakt namn + klubb-matchning
 if (!empty($club)) {
 $results = $db->getAll("
 SELECT r.id, r.firstname, r.lastname, r.license_number, c.name as club_name
 FROM riders r
 LEFT JOIN clubs c ON r.club_id = c.id
 WHERE LOWER(r.lastname) = ?
 AND LOWER(c.name) LIKE ?
 AND r.license_number IS NOT NULL
 AND r.license_number != ''
 LIMIT 5
", [$search_lastname, '%' . $search_club . '%']);
 
 if (!empty($results)) {
 return $results;
 }
 }
 
 // Strategi 2: Exakt namn (utan klubb-krav)
 $results = $db->getAll("
 SELECT r.id, r.firstname, r.lastname, r.license_number, c.name as club_name
 FROM riders r
 LEFT JOIN clubs c ON r.club_id = c.id
 WHERE LOWER(r.lastname) = ?
 AND r.license_number IS NOT NULL
 AND r.license_number != ''
 ORDER BY r.license_year DESC
 LIMIT 5
", [$search_lastname]);
 
 if (!empty($results)) {
 return $results;
 }
 
 // Strategi 3: Fuzzy match på första 3 bokstäverna
 if (strlen($search_lastname) >= 3) {
 $search_prefix = substr($search_lastname, 0, 3);
 $results = $db->getAll("
 SELECT r.id, r.firstname, r.lastname, r.license_number, c.name as club_name
 FROM riders r
 LEFT JOIN clubs c ON r.club_id = c.id
 WHERE LOWER(r.lastname) LIKE ?
 AND r.license_number IS NOT NULL
 AND r.license_number != ''
 ORDER BY r.license_year DESC
 LIMIT 5
", [$search_prefix . '%']);
 
 if (!empty($results)) {
 return $results;
 }
 }
 
 return [];
}

/**
 * Generera berikad CSV-fil med uppdaterade UCI-ID
 */
function generate_enriched_csv($output_path, $updated_rows) {
 $handle = fopen($output_path, 'w');
 if (!$handle) return false;

 if (!empty($updated_rows)) {
 // Skriv headers från första raden
 $headers = array_keys($updated_rows[0]['data']);
 fputcsv($handle, $headers);

 // Skriv data
 foreach ($updated_rows as $row) {
 fputcsv($handle, array_values($row['data']));
 }
 }

 fclose($handle);
 return true;
}
?>
