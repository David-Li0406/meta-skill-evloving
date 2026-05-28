<?php
/**
 * Check License Numbers
 * Find riders with potentially incorrect license_number formats
 *
 * Valid formats:
 * - UCI ID: Starts with 100 or 101 (any length, with or without spaces)
 * - SWE ID: Starts with"SWE" followed by digits (e.g., SWE2512345)
 *
 * Invalid (not UCI, not SWE) → Convert to SWE ID format: SWE25XXXXX
 */

require_once __DIR__ . '/../config.php';
require_admin();
require_once __DIR__ . '/../includes/admin-layout.php';

$db = getDB();
$message = '';
$messageType = 'info';

// Helper function to check if license_number is valid UCI
function isValidUCI($licenseNumber) {
 if (empty($licenseNumber)) return false;
 // Remove spaces and check if starts with 100 or 101 (any length)
 $cleaned = preg_replace('/\s+/', '', $licenseNumber);
 return preg_match('/^10[01]\d+$/', $cleaned);
}

// Helper function to check if license_number is valid SWE
function isValidSWE($licenseNumber) {
 if (empty($licenseNumber)) return false;
 return preg_match('/^SWE/i', $licenseNumber);
}

// Get next SWE ID number
function getNextSweId($db) {
 $year = date('y'); // 25 for 2025
 $prefix ="SWE{$year}";

 // Find highest existing SWE ID for this year
 $highest = $db->getRow("
 SELECT license_number
 FROM riders
 WHERE license_number LIKE ?
 ORDER BY license_number DESC
 LIMIT 1
", [$prefix . '%']);

 if ($highest && preg_match('/SWE\d{2}(\d+)/', $highest['license_number'], $matches)) {
 $nextNum = (int)$matches[1] + 1;
 } else {
 $nextNum = 10001; // Start from 10001
 }

 return $prefix . $nextNum;
}

// Handle convert single action
if (isset($_GET['action']) && $_GET['action'] === 'convert' && isset($_GET['id'])) {
 $riderId = (int)$_GET['id'];
 $newSweId = getNextSweId($db);
 $db->update('riders', ['license_number' => $newSweId], 'id = ?', [$riderId]);
 $message ="Ryttare ID {$riderId} fick nytt SWE ID: {$newSweId}";
 $messageType = 'success';
}

// Handle bulk convert action
if (isset($_GET['action']) && $_GET['action'] === 'convert_all_invalid') {
 $year = date('y');
 $prefix ="SWE{$year}";

 // Get all invalid riders
 $invalidRiders = $db->getAll("
 SELECT id, license_number
 FROM riders
 WHERE license_number IS NOT NULL
 AND license_number != ''
 AND license_number NOT REGEXP '^SWE'
 AND REPLACE(REPLACE(license_number, ' ', ''), '-', '') NOT REGEXP '^10[01][0-9]+$'
 ORDER BY id
");

 // Find starting number
 $highest = $db->getRow("
 SELECT license_number
 FROM riders
 WHERE license_number LIKE ?
 ORDER BY license_number DESC
 LIMIT 1
", [$prefix . '%']);

 if ($highest && preg_match('/SWE\d{2}(\d+)/', $highest['license_number'], $matches)) {
 $nextNum = (int)$matches[1] + 1;
 } else {
 $nextNum = 10001;
 }

 $converted = 0;
 foreach ($invalidRiders as $rider) {
 $newSweId = $prefix . $nextNum;
 $db->update('riders', ['license_number' => $newSweId], 'id = ?', [$rider['id']]);
 $nextNum++;
 $converted++;
 }

 $message ="Konverterade {$converted} ryttare till SWE ID format";
 $messageType = 'success';
}

// Query for invalid riders - UCI can have spaces
// Remove spaces before checking the pattern
$invalidRiders = $db->getAll("
 SELECT
 r.id,
 r.firstname,
 r.lastname,
 r.license_number,
 r.license_type,
 r.license_year,
 r.birth_year,
 c.name as club_name,
 LENGTH(r.license_number) as license_length
 FROM riders r
 LEFT JOIN clubs c ON r.club_id = c.id
 WHERE r.license_number IS NOT NULL
 AND r.license_number != ''
 AND r.license_number NOT REGEXP '^SWE'
 AND REPLACE(REPLACE(r.license_number, ' ', ''), '-', '') NOT REGEXP '^10[01][0-9]+$'
 ORDER BY r.id DESC
 LIMIT 200
");

// Count total invalid
$invalidCount = $db->getRow("
 SELECT COUNT(*) as count
 FROM riders
 WHERE license_number IS NOT NULL
 AND license_number != ''
 AND license_number NOT REGEXP '^SWE'
 AND REPLACE(REPLACE(license_number, ' ', ''), '-', '') NOT REGEXP '^10[01][0-9]+$'
")['count'];

// Count by format type
$formatCounts = $db->getAll("
 SELECT
 CASE
  WHEN license_number REGEXP '^SWE' THEN 'SWE ID (korrekt)'
  WHEN REPLACE(REPLACE(license_number, ' ', ''), '-', '') REGEXP '^10[01][0-9]+$' THEN 'UCI ID (korrekt)'
  ELSE 'Ogiltigt format (bör konverteras till SWE ID)'
 END as format_type,
 COUNT(*) as count
 FROM riders
 WHERE license_number IS NOT NULL AND license_number != ''
 GROUP BY format_type
 ORDER BY count DESC
");

$pageTitle = 'Kontrollera License Numbers';
$pageType = 'admin';
include __DIR__ . '/../includes/layout-header.php';
?>

<main class="main-content">
 <div class="container">
 <?php render_admin_header('Kontrollera License Numbers', 'settings'); ?>

 <?php if ($message): ?>
  <div class="alert alert-<?= $messageType ?> mb-lg">
  <i data-lucide="<?= $messageType === 'success' ? 'check-circle' : 'info' ?>"></i>
  <?= h($message) ?>
  </div>
 <?php endif; ?>

 <!-- Format explanation -->
 <div class="alert alert--info mb-lg">
  <i data-lucide="info"></i>
  <div>
  <strong>Giltiga format:</strong><br>
  - <strong>UCI ID:</strong> Börjar med 100 eller 101 (valfri längd, med eller utan mellanslag)<br>
   &nbsp;&nbsp;Exempel: <code>10048820303</code>, <code>100 683 277 90</code>, <code>1006832</code><br>
  - <strong>SWE ID:</strong> Börjar med"SWE" följt av år och nummer<br>
   &nbsp;&nbsp;Exempel: <code>SWE2512345</code><br><br>
  <strong>Ogiltiga:</strong> Konverteras till SWE ID format (SWE25XXXXX)
  </div>
 </div>

 <!-- Format Statistics -->
 <div class="card mb-lg">
  <div class="card-header">
  <h2 class="text-primary">
   <i data-lucide="bar-chart"></i>
   License Number Statistik
  </h2>
  </div>
  <div class="card-body">
  <table class="table">
   <thead>
   <tr>
    <th>Format</th>
    <th>Antal</th>
   </tr>
   </thead>
   <tbody>
   <?php foreach ($formatCounts as $format): ?>
   <tr class="<?= strpos($format['format_type'], 'Ogiltigt') !== false ? 'gs-bg-warning-light' : '' ?>">
    <td>
    <?php if (strpos($format['format_type'], 'Ogiltigt') !== false): ?>
     <i data-lucide="alert-triangle" class="text-warning"></i>
    <?php else: ?>
     <i data-lucide="check-circle" class="text-success"></i>
    <?php endif; ?>
    <?= h($format['format_type']) ?>
    </td>
    <td><?= number_format($format['count']) ?></td>
   </tr>
   <?php endforeach; ?>
   </tbody>
  </table>
  </div>
 </div>

 <!-- Invalid Riders -->
 <div class="card">
  <div class="card-header flex justify-between items-center">
  <h2 class="text-warning">
   <i data-lucide="alert-triangle"></i>
   Ryttare med ogiltigt license_number (<?= number_format($invalidCount) ?> totalt)
  </h2>
  <?php if ($invalidCount > 0): ?>
  <a href="?action=convert_all_invalid"
   class="btn btn--primary"
   onclick="return confirm('Är du säker? Detta konverterar alla <?= $invalidCount ?> ryttare till SWE ID format (SWE25XXXXX).')">
   <i data-lucide="refresh-cw"></i>
   Konvertera alla till SWE ID (<?= $invalidCount ?>)
  </a>
  <?php endif; ?>
  </div>
  <div class="card-body">
  <?php if (empty($invalidRiders)): ?>
   <div class="text-center py-lg">
   <i data-lucide="check-circle" style="width: 48px; height: 48px; color: var(--gs-success);"></i>
   <p class="text-success mt-md">Inga ryttare med ogiltigt format!</p>
   </div>
  <?php else: ?>
   <p class="text-secondary mb-md">
   Visar <?= count($invalidRiders) ?> av <?= number_format($invalidCount) ?> ryttare.
   Dessa license_number är varken giltiga UCI ID eller SWE ID och bör konverteras.
   </p>
   <div class="table-responsive">
   <table class="table">
    <thead>
    <tr>
     <th>ID</th>
     <th>Namn</th>
     <th>Nuvarande License Number</th>
     <th>Licenstyp</th>
     <th>Åtgärd</th>
    </tr>
    </thead>
    <tbody>
    <?php foreach ($invalidRiders as $rider): ?>
    <tr>
     <td><?= $rider['id'] ?></td>
     <td>
     <a href="/rider.php?id=<?= $rider['id'] ?>" target="_blank">
      <?= h($rider['firstname'] . ' ' . $rider['lastname']) ?>
     </a>
     </td>
     <td><code class="text-warning"><?= h($rider['license_number']) ?></code></td>
     <td><?= h($rider['license_type'] ?? '-') ?></td>
     <td>
     <a href="?action=convert&id=<?= $rider['id'] ?>"
      class="btn btn--sm btn--primary"
      onclick="return confirm('Konvertera till SWE ID?')">
      <i data-lucide="refresh-cw"></i>
      Till SWE ID
     </a>
     </td>
    </tr>
    <?php endforeach; ?>
    </tbody>
   </table>
   </div>
  <?php endif; ?>
  </div>
 </div>

 <?php render_admin_footer(); ?>
 </div>
</main>

<style>
.gs-bg-warning-light {
 background-color: rgba(255, 193, 7, 0.1);
}
</style>

<?php include __DIR__ . '/../includes/layout-footer.php'; ?>
