<?php
require_once __DIR__ . '/../config.php';
require_admin();

$db = getDB();
$pdo = $GLOBALS['pdo'];

$messages = [];

// Migration 1: Add DH support columns
try {
 $columns = $db->getAll("SHOW COLUMNS FROM results LIKE 'run_1_time'");
 if (empty($columns)) {
 $db->query("ALTER TABLE results ADD COLUMN run_1_time TIME NULL AFTER finish_time");
 $messages[] = ['type' => 'success', 'text' => '✅ Added run_1_time column'];
 } else {
 $messages[] = ['type' => 'info', 'text' => 'ℹ️ run_1_time column already exists'];
 }
} catch (Exception $e) {
 $messages[] = ['type' => 'error', 'text' => '❌ Failed to add run_1_time: ' . $e->getMessage()];
}

try {
 $columns = $db->getAll("SHOW COLUMNS FROM results LIKE 'run_2_time'");
 if (empty($columns)) {
 $db->query("ALTER TABLE results ADD COLUMN run_2_time TIME NULL AFTER run_1_time");
 $messages[] = ['type' => 'success', 'text' => '✅ Added run_2_time column'];
 } else {
 $messages[] = ['type' => 'info', 'text' => 'ℹ️ run_2_time column already exists'];
 }
} catch (Exception $e) {
 $messages[] = ['type' => 'error', 'text' => '❌ Failed to add run_2_time: ' . $e->getMessage()];
}

try {
 $columns = $db->getAll("SHOW COLUMNS FROM results LIKE 'run_1_points'");
 if (empty($columns)) {
 $db->query("ALTER TABLE results ADD COLUMN run_1_points INT DEFAULT 0 AFTER points");
 $messages[] = ['type' => 'success', 'text' => '✅ Added run_1_points column'];
 } else {
 $messages[] = ['type' => 'info', 'text' => 'ℹ️ run_1_points column already exists'];
 }
} catch (Exception $e) {
 $messages[] = ['type' => 'error', 'text' => '❌ Failed to add run_1_points: ' . $e->getMessage()];
}

try {
 $columns = $db->getAll("SHOW COLUMNS FROM results LIKE 'run_2_points'");
 if (empty($columns)) {
 $db->query("ALTER TABLE results ADD COLUMN run_2_points INT DEFAULT 0 AFTER run_1_points");
 $messages[] = ['type' => 'success', 'text' => '✅ Added run_2_points column'];
 } else {
 $messages[] = ['type' => 'info', 'text' => 'ℹ️ run_2_points column already exists'];
 }
} catch (Exception $e) {
 $messages[] = ['type' => 'error', 'text' => '❌ Failed to add run_2_points: ' . $e->getMessage()];
}

// Migration 2: Add event_format column
try {
 $columns = $db->getAll("SHOW COLUMNS FROM events LIKE 'event_format'");
 if (empty($columns)) {
 $db->query("ALTER TABLE events ADD COLUMN event_format VARCHAR(20) DEFAULT 'ENDURO' AFTER discipline");
 $messages[] = ['type' => 'success', 'text' => '✅ Added event_format column'];

 try {
 $db->query("CREATE INDEX idx_event_format ON events(event_format)");
 $messages[] = ['type' => 'success', 'text' => '✅ Created index on event_format'];
 } catch (Exception $e) {
 $messages[] = ['type' => 'warning', 'text' => '⚠️ Could not create index: ' . $e->getMessage()];
 }
 } else {
 $messages[] = ['type' => 'info', 'text' => 'ℹ️ event_format column already exists'];
 }
} catch (Exception $e) {
 $messages[] = ['type' => 'error', 'text' => '❌ Failed to add event_format: ' . $e->getMessage()];
}

$pageTitle = 'Kör Migrationer';
$pageType = 'admin';
include __DIR__ . '/../includes/layout-header.php';
?>

<main class="main-content">
 <div class="container" class="gs-max-w-800">
 <div class="card">
 <div class="card-header">
 <h1 class="text-primary">
  <i data-lucide="database"></i>
  Databas-migrationer
 </h1>
 </div>
 <div class="card-body">
 <div class="alert alert--info mb-lg">
  <i data-lucide="info"></i>
  Dessa migrationer lägger till stöd för DH-resultat och event-format.
 </div>

 <?php foreach ($messages as $msg): ?>
  <div class="alert alert-<?= $msg['type'] ?> mb-sm">
  <?= htmlspecialchars($msg['text']) ?>
  </div>
 <?php endforeach; ?>

 <?php
 $hasErrors = false;
 foreach ($messages as $msg) {
  if ($msg['type'] === 'error') {
  $hasErrors = true;
  break;
  }
 }
 ?>

 <?php if (!$hasErrors): ?>
  <div class="alert alert--success mt-lg">
  <i data-lucide="check-circle"></i>
  <strong>Migrationer klara!</strong> Du kan nu skapa och redigera events med DH-format.
  </div>
 <?php endif; ?>

 <div class="flex gap-md mt-lg">
  <a href="/admin/events.php" class="btn btn--primary">
  <i data-lucide="arrow-left"></i>
  Tillbaka till Events
  </a>
  <a href="/admin/run-migrations.php" class="btn btn--secondary">
  <i data-lucide="refresh-cw"></i>
  Kör igen
  </a>
 </div>
 </div>
 </div>
 </div>
</main>

<?php include __DIR__ . '/../includes/layout-footer.php'; ?>
