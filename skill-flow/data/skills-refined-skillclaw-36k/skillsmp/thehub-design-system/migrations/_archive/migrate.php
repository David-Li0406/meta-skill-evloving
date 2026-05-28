<?php
/**
 * Migration Runner
 * Reads and executes SQL migration files from database/migrations folder
 */

require_once __DIR__ . '/../config.php';
require_admin();

// Enable error display for debugging
error_reporting(E_ALL);
ini_set('display_errors', 1);

$db = getDB();
$message = '';
$messageType = '';

// Ensure migrations table exists
try {
 $db->getAll("
 CREATE TABLE IF NOT EXISTS migrations (
 id INT AUTO_INCREMENT PRIMARY KEY,
 filename VARCHAR(255) NOT NULL UNIQUE,
 executed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
 success TINYINT(1) DEFAULT 1,
 error_message TEXT
 )
");
} catch (Exception $e) {
 // Table might already exist
}

// Get migrations directory
$migrationsDir = __DIR__ . '/../database/migrations';
$migrationFiles = [];

if (is_dir($migrationsDir)) {
 $files = scandir($migrationsDir);
 foreach ($files as $file) {
 if (pathinfo($file, PATHINFO_EXTENSION) === 'sql') {
 $migrationFiles[] = $file;
 }
 }
 sort($migrationFiles);
}

// Get executed migrations
$executedMigrations = [];
try {
 $rows = $db->getAll("SELECT filename, executed_at, success, error_message FROM migrations");
 foreach ($rows as $row) {
 $executedMigrations[$row['filename']] = $row;
 }
} catch (Exception $e) {
 // Table might not exist yet
}

// Handle run migration
if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['run_migration'])) {
 checkCsrf();

 $filename = basename($_POST['run_migration']); // Security: only basename
 $filepath = $migrationsDir . '/' . $filename;

 if (file_exists($filepath) && pathinfo($filename, PATHINFO_EXTENSION) === 'sql') {
 $sql = file_get_contents($filepath);

 // Split by semicolons (simple approach - doesn't handle semicolons in strings)
 $statements = array_filter(array_map('trim', explode(';', $sql)));

 $errors = [];
 $successCount = 0;

 foreach ($statements as $statement) {
 // Remove SQL comments (lines starting with --)
 $lines = explode("\n", $statement);
 $cleanLines = [];
 foreach ($lines as $line) {
 $trimmedLine = trim($line);
 if (strpos($trimmedLine, '--') !== 0 && !empty($trimmedLine)) {
  $cleanLines[] = $line;
 }
 }
 $statement = trim(implode("\n", $cleanLines));

 if (empty($statement)) {
 continue;
 }

 try {
 $db->getAll($statement);
 $successCount++;
 } catch (Exception $e) {
 $errorMsg = $e->getMessage();
 // Ignore"already exists" errors
 if (strpos($errorMsg, 'Duplicate column') === false &&
  strpos($errorMsg, 'Duplicate key') === false &&
  strpos($errorMsg, 'already exists') === false) {
  $errors[] = $errorMsg;
 } else {
  $successCount++;
 }
 }
 }

 // Record migration
 $success = empty($errors);
 $errorMessage = implode('; ', $errors);

 try {
 // Check if already recorded
 $existing = $db->getRow("SELECT id FROM migrations WHERE filename = ?", [$filename]);
 if ($existing) {
 $db->update('migrations', [
  'executed_at' => date('Y-m-d H:i:s'),
  'success' => $success ? 1 : 0,
  'error_message' => $errorMessage ?: null
 ], 'filename = ?', [$filename]);
 } else {
 $db->insert('migrations', [
  'filename' => $filename,
  'success' => $success ? 1 : 0,
  'error_message' => $errorMessage ?: null
 ]);
 }
 } catch (Exception $e) {
 // Ignore tracking errors
 }

 if ($success) {
 $message ="Migration '$filename' kördes framgångsrikt ($successCount statements)";
 $messageType = 'success';
 } else {
 $message ="Migration '$filename' kördes med fel:" . $errorMessage;
 $messageType = 'error';
 }

 // Refresh executed migrations
 try {
 $rows = $db->getAll("SELECT filename, executed_at, success, error_message FROM migrations");
 $executedMigrations = [];
 foreach ($rows as $row) {
 $executedMigrations[$row['filename']] = $row;
 }
 } catch (Exception $e) {
 // Ignore
 }
 } else {
 $message = 'Ogiltig migrationsfil';
 $messageType = 'error';
 }
}

// Handle run all pending
if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['run_all_pending'])) {
 checkCsrf();

 $ranCount = 0;
 $errorCount = 0;

 foreach ($migrationFiles as $filename) {
 if (isset($executedMigrations[$filename]) && $executedMigrations[$filename]['success']) {
 continue; // Skip already successful
 }

 $filepath = $migrationsDir . '/' . $filename;
 $sql = file_get_contents($filepath);
 $statements = array_filter(array_map('trim', explode(';', $sql)));

 $errors = [];
 $successCount = 0;

 foreach ($statements as $statement) {
 // Remove SQL comments (lines starting with --)
 $lines = explode("\n", $statement);
 $cleanLines = [];
 foreach ($lines as $line) {
 $trimmedLine = trim($line);
 if (strpos($trimmedLine, '--') !== 0 && !empty($trimmedLine)) {
  $cleanLines[] = $line;
 }
 }
 $statement = trim(implode("\n", $cleanLines));

 if (empty($statement)) {
 continue;
 }

 try {
 $db->getAll($statement);
 $successCount++;
 } catch (Exception $e) {
 $errorMsg = $e->getMessage();
 if (strpos($errorMsg, 'Duplicate column') === false &&
  strpos($errorMsg, 'Duplicate key') === false &&
  strpos($errorMsg, 'already exists') === false) {
  $errors[] = $errorMsg;
 } else {
  $successCount++;
 }
 }
 }

 $success = empty($errors);
 $errorMessage = implode('; ', $errors);

 try {
 $existing = $db->getRow("SELECT id FROM migrations WHERE filename = ?", [$filename]);
 if ($existing) {
 $db->update('migrations', [
  'executed_at' => date('Y-m-d H:i:s'),
  'success' => $success ? 1 : 0,
  'error_message' => $errorMessage ?: null
 ], 'filename = ?', [$filename]);
 } else {
 $db->insert('migrations', [
  'filename' => $filename,
  'success' => $success ? 1 : 0,
  'error_message' => $errorMessage ?: null
 ]);
 }
 } catch (Exception $e) {
 // Ignore
 }

 if ($success) {
 $ranCount++;
 } else {
 $errorCount++;
 }
 }

 if ($errorCount > 0) {
 $message ="Körde $ranCount migrationer, $errorCount misslyckades";
 $messageType = 'warning';
 } else {
 $message ="Körde $ranCount nya migrationer framgångsrikt";
 $messageType = 'success';
 }

 // Refresh
 try {
 $rows = $db->getAll("SELECT filename, executed_at, success, error_message FROM migrations");
 $executedMigrations = [];
 foreach ($rows as $row) {
 $executedMigrations[$row['filename']] = $row;
 }
 } catch (Exception $e) {
 // Ignore
 }
}

$pageTitle = 'Kör Migrationer';
$pageType = 'admin';
include __DIR__ . '/../includes/layout-header.php';
?>

<main class="main-content">
 <div class="container">
 <!-- Header -->
 <div class="flex items-center justify-between mb-lg">
 <div>
 <h1 class="">
  <i data-lucide="database"></i>
  Kör Migrationer
 </h1>
 <p class="text-secondary">
  Kör databasmigrationer från /database/migrations
 </p>
 </div>
 <a href="/admin/system-settings.php?tab=debug" class="btn btn--secondary">
 <i data-lucide="arrow-left"></i>
 Tillbaka
 </a>
 </div>

 <?php if ($message): ?>
 <div class="alert alert-<?= h($messageType) ?> mb-lg">
 <i data-lucide="<?= $messageType === 'success' ? 'check-circle' : ($messageType === 'error' ? 'alert-circle' : 'alert-triangle') ?>"></i>
 <?= h($message) ?>
 </div>
 <?php endif; ?>

 <!-- Stats -->
 <?php
 $successCount = 0;
 foreach ($executedMigrations as $m) {
 if ($m['success']) $successCount++;
 }
 $pendingCount = count($migrationFiles) - $successCount;
 ?>
 <div class="grid grid-cols-3 gap-md mb-lg">
 <div class="card">
 <div class="card-body text-center">
  <div class="text-2xl text-primary"><?= count($migrationFiles) ?></div>
  <div class="text-sm text-secondary">Totalt filer</div>
 </div>
 </div>
 <div class="card">
 <div class="card-body text-center">
  <div class="text-2xl text-success"><?= $successCount ?></div>
  <div class="text-sm text-secondary">Körda</div>
 </div>
 </div>
 <div class="card">
 <div class="card-body text-center">
  <div class="text-2xl text-warning"><?= $pendingCount ?></div>
  <div class="text-sm text-secondary">Väntande</div>
 </div>
 </div>
 </div>

 <?php if ($pendingCount > 0): ?>
 <div class="card mb-lg">
 <div class="card-body">
  <form method="POST">
  <?= csrf_field() ?>
  <button type="submit" name="run_all_pending" value="1" class="btn btn--primary"
  onclick="return confirm('Kör alla <?= $pendingCount ?> väntande migrationer?')">
  <i data-lucide="play"></i>
  Kör alla väntande migrationer
  </button>
  </form>
 </div>
 </div>
 <?php endif; ?>

 <!-- Migration List -->
 <div class="card">
 <div class="card-header">
 <h2 class="">
  <i data-lucide="list"></i>
  Migrationer (<?= count($migrationFiles) ?>)
 </h2>
 </div>
 <div class="card-body gs-p-0">
 <?php if (empty($migrationFiles)): ?>
  <div class="p-lg text-center">
  <i data-lucide="inbox" class="text-secondary" style="width: 48px; height: 48px;"></i>
  <p class="text-secondary mt-md">Inga migrationsfiler hittades i /database/migrations</p>
  </div>
 <?php else: ?>
  <!-- Mobile View: Cards -->
  <div class="migration-cards p-sm">
  <?php foreach ($migrationFiles as $file):
  $executed = $executedMigrations[$file] ?? null;
  $isSuccess = $executed && $executed['success'];
  $isFailed = $executed && !$executed['success'];
  ?>
  <div class="migration-card <?= $isSuccess ? 'success' : ($isFailed ? 'failed' : 'pending') ?>">
  <div class="migration-card-header">
   <div class="migration-filename"><?= h($file) ?></div>
   <div class="migration-status">
   <?php if ($isSuccess): ?>
   <span class="badge badge-success">✓ Körd</span>
   <?php elseif ($isFailed): ?>
   <span class="badge badge-danger">✗ Misslyckad</span>
   <?php else: ?>
   <span class="badge badge-warning">⏳ Väntande</span>
   <?php endif; ?>
   </div>
  </div>
  <?php if ($executed): ?>
   <div class="migration-date">
   Körd: <?= date('Y-m-d H:i', strtotime($executed['executed_at'])) ?>
   </div>
  <?php endif; ?>
  <?php if ($isFailed && $executed['error_message']): ?>
   <div class="migration-error">
   <?= h($executed['error_message']) ?>
   </div>
  <?php endif; ?>
  <div class="migration-action">
   <form method="POST">
   <?= csrf_field() ?>
   <button type="submit" name="run_migration" value="<?= h($file) ?>"
   class="btn btn-block <?= $isSuccess ? 'btn--secondary' : 'btn--primary' ?>"
   onclick="return confirm('Kör migration <?= h($file) ?>?')">
   <i data-lucide="play"></i>
   <?= $isSuccess ? 'Kör igen' : 'Kör migration' ?>
   </button>
   </form>
  </div>
  </div>
  <?php endforeach; ?>
  </div>

  <!-- Desktop View: Table -->
  <div class="migration-table">
  <table class="table">
  <thead>
  <tr>
   <th>Fil</th>
   <th>Status</th>
   <th>Körd</th>
   <th class="text-right">Åtgärd</th>
  </tr>
  </thead>
  <tbody>
  <?php foreach ($migrationFiles as $file):
   $executed = $executedMigrations[$file] ?? null;
   $isSuccess = $executed && $executed['success'];
   $isFailed = $executed && !$executed['success'];
  ?>
   <tr>
   <td>
   <strong><?= h($file) ?></strong>
   <?php if ($isFailed && $executed['error_message']): ?>
   <br><small class="text-error"><?= h($executed['error_message']) ?></small>
   <?php endif; ?>
   </td>
   <td>
   <?php if ($isSuccess): ?>
   <span class="badge badge-success">Körd</span>
   <?php elseif ($isFailed): ?>
   <span class="badge badge-danger">Misslyckad</span>
   <?php else: ?>
   <span class="badge badge-warning">Väntande</span>
   <?php endif; ?>
   </td>
   <td>
   <?php if ($executed): ?>
   <?= date('Y-m-d H:i', strtotime($executed['executed_at'])) ?>
   <?php else: ?>
   -
   <?php endif; ?>
   </td>
   <td class="text-right">
   <form method="POST" style="display: inline;">
   <?= csrf_field() ?>
   <button type="submit" name="run_migration" value="<?= h($file) ?>"
    class="btn btn--sm <?= $isSuccess ? 'btn--secondary' : 'btn--primary' ?>"
    onclick="return confirm('Kör migration <?= h($file) ?>?')">
    <i data-lucide="play"></i>
    <?= $isSuccess ? 'Kör igen' : 'Kör' ?>
   </button>
   </form>
   </td>
   </tr>
  <?php endforeach; ?>
  </tbody>
  </table>
  </div>
 <?php endif; ?>
 </div>
 </div>
 </div>
</main>

<style>
/* Mobile-first migration styles */
.migration-cards {
 display: flex;
 flex-direction: column;
 gap: var(--space-sm);
}

.migration-table {
 display: none;
}

.migration-card {
 background: var(--gs-white);
 border: 1px solid var(--border);
 border-radius: var(--gs-radius-md);
 padding: var(--space-md);
 transition: all 0.2s;
}

.migration-card:hover {
 box-shadow: var(--gs-shadow-sm);
}

.migration-card.success {
 border-left: 4px solid var(--gs-success);
}

.migration-card.failed {
 border-left: 4px solid var(--gs-danger);
}

.migration-card.pending {
 border-left: 4px solid var(--gs-warning);
}

.migration-card-header {
 display: flex;
 flex-direction: column;
 gap: var(--space-sm);
 margin-bottom: var(--space-sm);
}

.migration-filename {
 font-weight: 600;
 font-size: 0.875rem;
 word-break: break-all;
 line-height: 1.4;
}

.migration-status {
 display: flex;
 align-items: center;
}

.migration-date {
 font-size: 0.75rem;
 color: var(--text-secondary);
 margin-bottom: var(--space-sm);
}

.migration-error {
 background: #fee;
 border: 1px solid #fcc;
 border-radius: var(--gs-radius-sm);
 padding: var(--gs-space-xs);
 font-size: 0.75rem;
 color: var(--gs-danger);
 margin-bottom: var(--space-sm);
 word-break: break-word;
}

.migration-action {
 margin-top: var(--space-sm);
}

/* Desktop view: Show table, hide cards */
@media (min-width: 768px) {
 .migration-cards {
 display: none;
 }

 .migration-table {
 display: block;
 }
}

/* Improve button spacing on mobile */
.btn-block {
 width: 100%;
 justify-content: center;
}

/* Better touch targets on mobile */
@media (max-width: 767px) {
 .btn {
 padding: 0.75rem 1rem;
 font-size: 1rem;
 }
}
</style>

<?php include __DIR__ . '/../includes/layout-footer.php'; ?>
