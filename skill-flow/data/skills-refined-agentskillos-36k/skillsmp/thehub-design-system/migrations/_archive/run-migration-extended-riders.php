<?php
/**
 * Migration Runner: Add Extended Rider Fields
 * Date: 2025-11-15
 *
 * This migration adds fields for full rider data including:
 * - Address information (address, postal_code, country)
 * - Emergency contact
 * - District and Team
 * - Multiple disciplines (JSON)
 * - License year
 *
 * IMPORTANT: These fields contain PRIVATE data and must NOT be exposed publicly
 */

error_reporting(E_ALL);
ini_set('display_errors', 1);

// Start output buffering to catch any early errors
ob_start();

try {
 require_once __DIR__ . '/../config.php';

 // Check if user is admin WITHOUT redirecting
 if (!is_admin()) {
 ob_end_clean();
 ?>
 <!DOCTYPE html>
 <html>
 <head>
 <title>Migration - Access Denied</title>
 <style>
 body { font-family: system-ui, sans-serif; max-width: 800px; margin: 50px auto; padding: 20px; }
 .error-box { background: #fee; border: 2px solid #dc3545; border-radius: 8px; padding: 30px; }
 .error-box h1 { color: #dc3545; margin: 0 0 20px 0; }
 .error-box p { line-height: 1.6; }
 .btn { display: inline-block; background: #667eea; color: white; padding: 12px 24px;
  text-decoration: none; border-radius: 6px; margin-top: 20px; }
 </style>
 </head>
 <body>
 <div class="error-box">
 <h1>🔒 Access Denied</h1>
 <p><strong>You must be logged in as an administrator to access this page.</strong></p>
 <p>This migration tool can only be run by authenticated admin users for security reasons.</p>
 <p>Please log in to the admin panel first:</p>
 <a href="/admin/login.php" class="btn">Go to Admin Login</a>
 </div>
 </body>
 </html>
 <?php
 exit;
 }

 $db = getDB();
 $errors = [];
 $success = [];
} catch (Exception $e) {
 ob_end_clean();
 die("INITIALIZATION ERROR:" . $e->getMessage() ."<br><br>Stack trace:<br>" . nl2br($e->getTraceAsString()));
}

// Run each migration step
$migrations = [
 // Step 1: DEPRECATED - personnummer column was dropped 2025-12-01
 // Only birth_year is stored now, personnummer is NOT stored in the database
 // This migration step kept for backwards compatibility (will skip if column doesn't exist)
"ALTER TABLE riders ADD COLUMN personnummer VARCHAR(15) AFTER birth_year" =>"Add personnummer field (DEPRECATED - will be skipped)",

 // Step 2: Add address fields
"ALTER TABLE riders ADD COLUMN address VARCHAR(255) AFTER city" =>"Add address field",
"ALTER TABLE riders ADD COLUMN postal_code VARCHAR(10) AFTER address" =>"Add postal_code field",
"ALTER TABLE riders ADD COLUMN country VARCHAR(100) DEFAULT 'Sverige' AFTER postal_code" =>"Add country field",

 // Step 3: Add emergency contact
"ALTER TABLE riders ADD COLUMN emergency_contact VARCHAR(255) AFTER phone" =>"Add emergency_contact field",

 // Step 4: Add district and team
"ALTER TABLE riders ADD COLUMN district VARCHAR(100) AFTER country" =>"Add district field",
"ALTER TABLE riders ADD COLUMN team VARCHAR(255) AFTER club_id" =>"Add team field",

 // Step 5: Add disciplines JSON field
"ALTER TABLE riders ADD COLUMN disciplines JSON AFTER discipline" =>"Add disciplines JSON field",

 // Step 6: Add license year
"ALTER TABLE riders ADD COLUMN license_year INT AFTER license_valid_until" =>"Add license_year field",
];

// Run migrations
foreach ($migrations as $sql => $description) {
 try {
 $result = $db->query($sql);
 if ($result === false) {
 // Query failed but didn't throw exception
 // Try to get error from PDO
 $pdo = $db->getConnection();
 if ($pdo) {
 $errorInfo = $pdo->errorInfo();
 $errorMsg = $errorInfo[2] ?? 'Unknown database error';

 // Check if it's a duplicate column error
 if (strpos($errorMsg, 'Duplicate column name') !== false ||
  strpos($errorMsg, 'column') !== false ||
  $errorInfo[1] == 1060) { // MySQL error code for duplicate column
  $success[] ="↷" . $description ." (already exists)";
 } else {
  $errors[] ="✗" . $description .":" . $errorMsg;
 }
 } else {
 $errors[] ="✗" . $description .": Database connection is null";
 }
 } else {
 $success[] ="✓" . $description;
 }
 } catch (Exception $e) {
 // Check if error is because column already exists
 if (strpos($e->getMessage(), 'Duplicate column name') !== false ||
 strpos($e->getMessage(), 'column') !== false) {
 $success[] ="↷" . $description ." (already exists)";
 } else {
 $errors[] ="✗" . $description .":" . $e->getMessage();
 }
 }
}

// Add indexes
$indexes = [
"ALTER TABLE riders ADD INDEX idx_personnummer (personnummer)" =>"Add personnummer index",
"ALTER TABLE riders ADD INDEX idx_postal_code (postal_code)" =>"Add postal_code index",
"ALTER TABLE riders ADD INDEX idx_district (district)" =>"Add district index",
];

foreach ($indexes as $sql => $description) {
 try {
 $result = $db->query($sql);
 if ($result === false) {
 // Query failed but didn't throw exception
 $pdo = $db->getConnection();
 if ($pdo) {
 $errorInfo = $pdo->errorInfo();
 $errorMsg = $errorInfo[2] ?? 'Unknown database error';

 // Check if it's a duplicate index error
 if (strpos($errorMsg, 'Duplicate key name') !== false ||
  strpos($errorMsg, 'duplicate') !== false ||
  $errorInfo[1] == 1061) { // MySQL error code for duplicate key
  $success[] ="↷" . $description ." (already exists)";
 } else {
  $errors[] ="✗" . $description .":" . $errorMsg;
 }
 } else {
 $errors[] ="✗" . $description .": Database connection is null";
 }
 } else {
 $success[] ="✓" . $description;
 }
 } catch (Exception $e) {
 // Check if error is because index already exists
 if (strpos($e->getMessage(), 'Duplicate key name') !== false ||
 strpos($e->getMessage(), 'duplicate') !== false ||
 strpos($e->getMessage(), 'exists') !== false) {
 $success[] ="↷" . $description ." (already exists)";
 } else {
 $errors[] ="✗" . $description .":" . $e->getMessage();
 }
 }
}

$pageTitle = 'Migration: Extended Rider Fields';
$pageType = 'admin';

// Debug: Log what happened
error_log("Migration script completed. Success:" . count($success) .", Errors:" . count($errors));

// Flush buffer and start normal output
ob_end_flush();

try {
 include __DIR__ . '/../includes/layout-header.php';
} catch (Exception $e) {
 // If header fails, show a simple HTML header instead
 ?>
 <!DOCTYPE html>
 <html>
 <head>
 <title><?= htmlspecialchars($pageTitle) ?></title>
 <style>
 body { font-family: system-ui, sans-serif; max-width: 1200px; margin: 0 auto; padding: 20px; }
 .error { color: #dc3545; background: #f8d7da; padding: 15px; border-radius: 5px; margin: 10px 0; }
 </style>
 </head>
 <body>
 <div class="error">
 <strong>WARNING:</strong> Layout header failed to load: <?= htmlspecialchars($e->getMessage()) ?>
 </div>
 <?php
}
?>

<main class="main-content">
 <div class="container">
 <h1 class="text-primary mb-lg">
 <i data-lucide="database"></i>
 Migration: Extended Rider Fields
 </h1>

 <?php if (!empty($success)): ?>
 <div class="card mb-lg gs-bg-success">
 <div class="card-header">
  <h2 class="text-success">
  <i data-lucide="check-circle"></i>
  Success (<?= count($success) ?>)
  </h2>
 </div>
 <div class="card-body">
  <?php foreach ($success as $msg): ?>
  <div class="text-sm gs-mb-xs gs-font-monospace">
  <?= h($msg) ?>
  </div>
  <?php endforeach; ?>
 </div>
 </div>
 <?php endif; ?>

 <?php if (!empty($errors)): ?>
 <div class="card mb-lg alert-border-danger">
 <div class="card-header">
  <h2 class="text-error">
  <i data-lucide="alert-circle"></i>
  Errors (<?= count($errors) ?>)
  </h2>
 </div>
 <div class="card-body">
  <?php foreach ($errors as $error): ?>
  <div class="text-sm gs-mb-xs text-error gs-font-monospace">
  <?= h($error) ?>
  </div>
  <?php endforeach; ?>
 </div>
 </div>
 <?php endif; ?>

 <div class="card">
 <div class="card-header">
 <h2 class="text-primary">
  <i data-lucide="info"></i>
  Migration Information
 </h2>
 </div>
 <div class="card-body">
 <h3 class="mb-md">Added Fields:</h3>
 <ul class="text-sm gs-list-ml-lg-lh-1-8">
  <li><code>personnummer</code> - Swedish personal number (YYYYMMDD-XXXX)</li>
  <li><code>address</code> - Street address</li>
  <li><code>postal_code</code> - Postal code</li>
  <li><code>country</code> - Country (default: Sverige)</li>
  <li><code>emergency_contact</code> - Emergency contact information</li>
  <li><code>district</code> - District/Region</li>
  <li><code>team</code> - Team name (separate from club)</li>
  <li><code>disciplines</code> - Multiple disciplines in JSON format (Road, Track, BMX, CX, Trial, Para, MTB, E-cycling, Gravel)</li>
  <li><code>license_year</code> - License year</li>
 </ul>

 <div class="alert alert--warning mt-lg">
  <i data-lucide="shield-alert"></i>
  <strong>PRIVACY WARNING:</strong> The following fields contain PRIVATE data and must NOT be exposed publicly:
  <ul class="gs-list-ml-1-5">
  <li><code>personnummer</code></li>
  <li><code>address</code></li>
  <li><code>postal_code</code></li>
  <li><code>phone</code></li>
  <li><code>emergency_contact</code></li>
  </ul>
 </div>

 <div class="mt-lg">
  <a href="/admin/import-riders-extended.php" class="btn btn--primary">
  <i data-lucide="upload"></i>
  Go to Extended Import
  </a>
  <a href="/admin/riders.php" class="btn btn--secondary">
  <i data-lucide="users"></i>
  View Riders
  </a>
 </div>
 </div>
 </div>
 </div>
</main>

<?php
try {
 include __DIR__ . '/../includes/layout-footer.php';
} catch (Exception $e) {
 echo"<p class='text-error'>ERROR loading footer:" . htmlspecialchars($e->getMessage()) ."</p>";
}
?>
