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
 $result = importVenuesFromCSV($file['tmp_name'], $db);
 $stats = $result['stats'];
 $errors = $result['errors'];

 if ($stats['failed'] === 0) {
 $message ="Import klar! {$stats['success']} anläggningar importerade.";
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
 * Import venues from CSV file
 */
function importVenuesFromCSV($filePath, $db) {
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

 // Read header with detected delimiter
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
 'bana' => 'name',
 'anläggning' => 'name',
 'anlaggning' => 'name',
 'park' => 'name',
 'bikepark' => 'name',

 'stad' => 'city',
 'city' => 'city',
 'ort' => 'city',

 'region' => 'region',
 'län' => 'region',
 'lan' => 'region',
 'county' => 'region',
 'område' => 'region',
 'omrade' => 'region',

 'land' => 'country',
 'country' => 'country',

 'adress' => 'address',
 'address' => 'address',
 'gatuadress' => 'address',
 'streetaddress' => 'address',

 'koordinater' => 'coordinates',
 'coordinates' => 'coordinates',
 'coords' => 'coordinates',
 'gps' => 'coordinates',
 'latlon' => 'coordinates',
 'latlong' => 'coordinates',

 'beskrivning' => 'description',
 'description' => 'description',
 'beskriv' => 'description',
 'info' => 'description',

 'webbplats' => 'website',
 'website' => 'website',
 'url' => 'website',
 'hemsida' => 'website',
 'web' => 'website',
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

 // Prepare venue data
 $venueData = [
 'name' => trim($data['name']),
 'city' => trim($data['city'] ?? ''),
 'region' => trim($data['region'] ?? ''),
 'country' => trim($data['country'] ?? 'Sverige'),
 'address' => trim($data['address'] ?? ''),
 'coordinates' => trim($data['coordinates'] ?? ''),
 'description' => trim($data['description'] ?? ''),
 'website' => trim($data['website'] ?? ''),
 'active' => 1
 ];

 // Check if venue exists (by name)
 $existing = $db->getRow(
 "SELECT id FROM venues WHERE name = ? LIMIT 1",
 [$venueData['name']]
 );

 if ($existing) {
 // Update existing venue
 $db->update('venues', $venueData, 'id = ?', [$existing['id']]);
 $stats['updated']++;
 error_log("Updated venue: {$venueData['name']}");
 } else {
 // Insert new venue
 $newId = $db->insert('venues', $venueData);
 $stats['success']++;
 error_log("Inserted venue: {$venueData['name']} (ID: {$newId})");
 }

 } catch (Exception $e) {
 $stats['failed']++;
 $errors[] ="Rad {$lineNumber}:" . $e->getMessage();
 error_log("Import error on line {$lineNumber}:" . $e->getMessage());
 }
 }

 fclose($handle);

 // Verification
 $verifyCount = $db->getRow("SELECT COUNT(*) as count FROM venues");
 $totalInDb = $verifyCount['count'] ?? 0;
 error_log("Venue import complete: {$stats['success']} new, {$stats['updated']} updated, {$stats['failed']} failed. Total venues in DB: {$totalInDb}");

 $stats['total_in_db'] = $totalInDb;

 return [
 'stats' => $stats,
 'errors' => $errors
 ];
}

// Page config for unified layout
$page_title = 'Importera Anläggningar';
$breadcrumbs = [
    ['label' => 'Import', 'url' => '/admin/import'],
    ['label' => 'Venues']
];

// Include unified layout
include __DIR__ . '/components/unified-layout.php';
?>

<?php if ($message): ?>
<div class="alert alert-<?= $messageType === 'success' ? 'success' : ($messageType === 'error' ? 'error' : 'warning') ?> mb-lg">
    <i data-lucide="<?= $messageType === 'success' ? 'check-circle' : 'alert-circle' ?>"></i>
    <?= h($message) ?>
</div>
<?php endif; ?>

<?php if (!empty($errors)): ?>
<div class="alert alert-error mb-lg">
    <strong>Fel under import:</strong>
    <ul style="margin-top: var(--space-sm); margin-left: var(--space-lg);">
        <?php foreach ($errors as $error): ?>
        <li><?= h($error) ?></li>
        <?php endforeach; ?>
    </ul>
</div>
<?php endif; ?>

<?php if ($stats): ?>
<!-- Stats Grid -->
<div class="admin-stats-grid mb-lg">
    <div class="admin-stat-card">
        <div class="admin-stat-icon" style="background: var(--color-info-light); color: var(--color-info);">
            <i data-lucide="file-text"></i>
        </div>
        <div class="admin-stat-content">
            <div class="admin-stat-value"><?= $stats['total'] ?></div>
            <div class="admin-stat-label">Totalt rader</div>
        </div>
    </div>
    <div class="admin-stat-card">
        <div class="admin-stat-icon" style="background: var(--color-success-light); color: var(--color-success);">
            <i data-lucide="plus-circle"></i>
        </div>
        <div class="admin-stat-content">
            <div class="admin-stat-value"><?= $stats['success'] ?></div>
            <div class="admin-stat-label">Nya</div>
        </div>
    </div>
    <div class="admin-stat-card">
        <div class="admin-stat-icon" style="background: var(--color-accent-light); color: var(--color-accent);">
            <i data-lucide="refresh-cw"></i>
        </div>
        <div class="admin-stat-content">
            <div class="admin-stat-value"><?= $stats['updated'] ?></div>
            <div class="admin-stat-label">Uppdaterade</div>
        </div>
    </div>
    <div class="admin-stat-card">
        <div class="admin-stat-icon" style="background: var(--color-error-light, rgba(239, 68, 68, 0.1)); color: var(--color-error);">
            <i data-lucide="x-circle"></i>
        </div>
        <div class="admin-stat-content">
            <div class="admin-stat-value"><?= $stats['failed'] ?></div>
            <div class="admin-stat-label">Misslyckade</div>
        </div>
    </div>
</div>

<div class="admin-card mb-lg">
    <div class="admin-card-body">
        <p><strong>Totalt i databasen:</strong> <?= $stats['total_in_db'] ?> anläggningar</p>
    </div>
</div>
<?php endif; ?>

<!-- Upload Form -->
<div class="admin-card mb-lg">
    <div class="admin-card-header">
        <h2>Bulk-import av anläggningar från CSV-fil</h2>
    </div>
    <div class="admin-card-body">
        <form method="POST" enctype="multipart/form-data">
            <?= csrf_field() ?>

            <div class="alert alert-info mb-lg">
                <i data-lucide="info"></i>
                <strong>CSV-format:</strong> Första raden ska innehålla kolumnnamn.
            </div>

            <div class="admin-form-group">
                <label class="admin-form-label">
                    <i data-lucide="upload"></i>
                    Välj CSV-fil
                </label>
                <input type="file" name="csv_file" accept=".csv" required class="admin-form-input">
                <small class="text-secondary">Max 10 MB. Format: CSV (komma-separerad)</small>
            </div>

            <div class="flex gap-md">
                <button type="submit" class="btn-admin btn-admin-primary">
                    <i data-lucide="upload"></i>
                    Importera Anläggningar
                </button>
                <a href="/admin/venues.php" class="btn-admin btn-admin-secondary">
                    <i data-lucide="arrow-left"></i>
                    Tillbaka
                </a>
                <a href="/templates/import-venues-template.csv" class="btn-admin btn-admin-secondary" download>
                    <i data-lucide="download"></i>
                    Ladda ner mall
                </a>
            </div>
        </form>
    </div>
</div>

<!-- CSV Format Info -->
<div class="admin-card">
    <div class="admin-card-header">
        <h2>CSV-kolumner</h2>
    </div>
    <div class="admin-card-body" style="padding: 0;">
        <div class="admin-table-container">
            <table class="admin-table">
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
                        <td>Anläggningsnamn</td>
                        <td><span class="admin-badge admin-badge-success">Ja</span></td>
                        <td>Åre Bike Park</td>
                    </tr>
                    <tr>
                        <td><code>city</code></td>
                        <td>Ort</td>
                        <td><span class="admin-badge admin-badge-secondary">Nej</span></td>
                        <td>Åre</td>
                    </tr>
                    <tr>
                        <td><code>region</code></td>
                        <td>Region/län</td>
                        <td><span class="admin-badge admin-badge-secondary">Nej</span></td>
                        <td>Jämtland</td>
                    </tr>
                    <tr>
                        <td><code>country</code></td>
                        <td>Land</td>
                        <td><span class="admin-badge admin-badge-secondary">Nej</span></td>
                        <td>Sverige</td>
                    </tr>
                    <tr>
                        <td><code>address</code></td>
                        <td>Adress</td>
                        <td><span class="admin-badge admin-badge-secondary">Nej</span></td>
                        <td>Årevägen 1, 837 52 Åre</td>
                    </tr>
                    <tr>
                        <td><code>coordinates</code></td>
                        <td>Koordinater (lat,lon)</td>
                        <td><span class="admin-badge admin-badge-secondary">Nej</span></td>
                        <td>63.3989,13.0819</td>
                    </tr>
                    <tr>
                        <td><code>description</code></td>
                        <td>Beskrivning</td>
                        <td><span class="admin-badge admin-badge-secondary">Nej</span></td>
                        <td>Sveriges största bike park</td>
                    </tr>
                    <tr>
                        <td><code>website</code></td>
                        <td>Hemsida</td>
                        <td><span class="admin-badge admin-badge-secondary">Nej</span></td>
                        <td>https://skistar.com/arebike</td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>
</div>

<?php include __DIR__ . '/components/unified-layout-footer.php'; ?>
