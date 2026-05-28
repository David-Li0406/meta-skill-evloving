<?php
error_reporting(E_ALL);
ini_set('display_errors', 1);

require_once __DIR__ . '/../config.php';
require_admin();

$db = getDB();

$pageTitle = 'Database Setup';
$pageType = 'admin';

$message = '';
$messageType = 'info';

// Handle setup execution
if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['action'])) {
 checkCsrf();

 $action = $_POST['action'];

 if ($action === 'run_schema') {
 try {
  // Read schema file
  $schemaFile = __DIR__ . '/../database/schema.sql';

  if (!file_exists($schemaFile)) {
  throw new Exception('Schema file not found: ' . $schemaFile);
  }

  $sql = file_get_contents($schemaFile);

  if ($sql === false) {
  throw new Exception('Failed to read schema file');
  }

  // Get PDO connection from Database class
  $pdo = $db->getConnection();
  if (!$pdo || !$pdo instanceof PDO) {
  throw new Exception('Database connection not available. Please check config.php database settings.');
  }

  // Execute schema (split by statement)
  $statements = array_filter(
  array_map('trim', explode(';', $sql)),
  function($stmt) {
   return !empty($stmt) && !preg_match('/^--/', $stmt);
  }
  );

  $executed = 0;
  $errors = [];

  foreach ($statements as $statement) {
  try {
   $pdo->exec($statement);
   $executed++;
  } catch (PDOException $e) {
   // Ignore errors for DROP/CREATE OR REPLACE (table might not exist)
   if (stripos($statement, 'DROP') === false &&
   stripos($statement, 'CREATE OR REPLACE') === false) {
   $errors[] = $e->getMessage();
   }
   $executed++;
  }
  }

  if (empty($errors)) {
  $message ="Database schema setup complete! Executed {$executed} SQL statements.";
  $messageType = 'success';
  } else {
  $message ="Setup completed with some warnings. Executed {$executed} statements.";
  $messageType = 'warning';
  }

 } catch (Exception $e) {
  $message = 'Setup failed: ' . $e->getMessage();
  $messageType = 'error';
 }
 }
}

// Check database status
$dbStatus = [];
try {
 $pdo = $db->getConnection();
 if ($pdo && $pdo instanceof PDO) {
 $dbStatus['connected'] = true;

 // Get current database name
 $stmt = $pdo->query("SELECT DATABASE() as db_name");
 $result = $stmt->fetch();
 $dbStatus['database'] = $result['db_name'] ?? 'Unknown';

 // Check which tables exist
 $stmt = $pdo->query("SHOW TABLES");
 $dbStatus['tables'] = $stmt->fetchAll(PDO::FETCH_COLUMN);
 $dbStatus['table_count'] = count($dbStatus['tables']);

 // Required tables
 $requiredTables = ['riders', 'clubs', 'events', 'series', 'results', 'admin_users', 'categories', 'import_logs'];
 $dbStatus['missing_tables'] = array_diff($requiredTables, $dbStatus['tables']);

 // Count records in existing tables
 $dbStatus['record_counts'] = [];
 foreach (['riders', 'clubs', 'events', 'series', 'results'] as $table) {
  if (in_array($table, $dbStatus['tables'])) {
  $stmt = $pdo->query("SELECT COUNT(*) FROM $table");
  $dbStatus['record_counts'][$table] = $stmt->fetchColumn();
  }
 }

 } else {
 $dbStatus['connected'] = false;
 $dbStatus['error'] = 'PDO connection not available';
 }
} catch (Exception $e) {
 $dbStatus['connected'] = false;
 $dbStatus['error'] = $e->getMessage();
}

include __DIR__ . '/../includes/layout-header.php';
?>

<main class="main-content">
 <div class="container">
 <h1 class="mb-lg">
  <i data-lucide="database"></i>
  Database Setup
 </h1>

 <?php if ($message): ?>
  <div class="alert alert-<?= h($messageType) ?> mb-lg">
  <i data-lucide="<?= $messageType === 'success' ? 'check-circle' : 'alert-circle' ?>"></i>
  <?= h($message) ?>
  </div>
 <?php endif; ?>

 <!-- Database Status -->
 <div class="card mb-lg">
  <div class="card-header">
  <h2 class="">Database Status</h2>
  </div>
  <div class="card-body">
  <?php if ($dbStatus['connected']): ?>
   <p class="mb-md">
   <span class="badge badge-success">✅ Connected</span>
   <strong>Database:</strong> <?= h($dbStatus['database']) ?>
   </p>

   <div class="mb-lg">
   <h3 class="mb-sm">Tables (<?= $dbStatus['table_count'] ?>)</h3>
   <?php if (empty($dbStatus['tables'])): ?>
    <div class="alert alert--warning">
    ⚠️ <strong>No tables found!</strong> You need to run the database setup.
    </div>
   <?php else: ?>
    <div class="grid grid-cols-2 gap-md">
    <div>
     <h4 class="mb-sm">Existing Tables:</h4>
     <ul class="gs-list">
     <?php foreach ($dbStatus['tables'] as $table): ?>
      <li>
      ✅ <code><?= h($table) ?></code>
      <?php if (isset($dbStatus['record_counts'][$table])): ?>
       <span class="text-secondary">
       (<?= number_format($dbStatus['record_counts'][$table]) ?> records)
       </span>
      <?php endif; ?>
      </li>
     <?php endforeach; ?>
     </ul>
    </div>
    <?php if (!empty($dbStatus['missing_tables'])): ?>
     <div>
     <h4 class="mb-sm">Missing Tables:</h4>
     <ul class="gs-list">
      <?php foreach ($dbStatus['missing_tables'] as $table): ?>
      <li class="text-error">❌ <code><?= h($table) ?></code></li>
      <?php endforeach; ?>
     </ul>
     </div>
    <?php endif; ?>
    </div>
   <?php endif; ?>
   </div>

   <!-- Record Counts -->
   <?php if (!empty($dbStatus['record_counts'])): ?>
   <div class="mb-md">
    <h3 class="mb-sm">Data Summary:</h3>
    <div class="grid grid-cols-5 gap-md">
    <?php foreach ($dbStatus['record_counts'] as $table => $count): ?>
     <div class="text-center" class="gs-stat-display-lg">
     <div class="gs-stat-display-number">
      <?= number_format($count) ?>
     </div>
     <div class="text-sm text-secondary"><?= h(ucfirst($table)) ?></div>
     </div>
    <?php endforeach; ?>
    </div>
   </div>
   <?php endif; ?>

  <?php else: ?>
   <div class="alert alert-danger">
   <strong>❌ Database not connected</strong>
   <?php if (isset($dbStatus['error'])): ?>
    <p class="mt-sm">Error: <?= h($dbStatus['error']) ?></p>
   <?php endif; ?>
   </div>
  <?php endif; ?>
  </div>
 </div>

 <!-- Setup Actions -->
 <div class="card">
  <div class="card-header">
  <h2 class="">Setup Actions</h2>
  </div>
  <div class="card-body">
  <form method="POST" onsubmit="return confirm('This will create/update database tables. Continue?');">
   <?= csrf_field() ?>
   <input type="hidden" name="action" value="run_schema">

   <div class="alert alert--info mb-md">
   <p class="gs-m-0">
    <strong>ℹ️ This will:</strong>
   </p>
   <ul class="gs-margin-list">
    <li>Create all required tables (riders, clubs, events, series, results, etc.)</li>
    <li>Add default categories (Elite, Junior, Veteran, etc.)</li>
    <li>Create default admin user (username: <code>admin</code>, password: <code>changeme123</code>)</li>
    <li>Safe to run multiple times (uses IF NOT EXISTS)</li>
   </ul>
   </div>

   <button type="submit" class="btn btn--primary btn-lg">
   <i data-lucide="play-circle"></i>
   Run Database Setup
   </button>
  </form>

  <div class="mt-lg flex gap-md">
   <a href="/admin/debug-database.php" class="btn btn--secondary">
   <i data-lucide="search"></i>
   Debug Database
   </a>
   <a href="/admin/riders.php" class="btn btn--secondary">
   <i data-lucide="users"></i>
   View Riders
   </a>
   <a href="/admin/import-riders.php" class="btn btn--secondary">
   <i data-lucide="upload"></i>
   Import Riders
   </a>
  </div>
  </div>
 </div>

 </div>
</main>

<?php include __DIR__ . '/../includes/layout-footer.php'; ?>
