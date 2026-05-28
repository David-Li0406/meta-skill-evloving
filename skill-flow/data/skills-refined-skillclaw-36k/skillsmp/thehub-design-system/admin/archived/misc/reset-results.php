<?php
/**
 * Reset Results and Import History Script
 * Deletes all results and clears import history
 *
 * IMPORTANT: Run this only once to clear all results!
 */

require_once __DIR__ . '/../config.php';
require_admin();

$db = getDB();
$current_admin = get_current_admin();

$message = '';
$messageType = 'info';
$stats = [
 'results_deleted' => 0,
 'import_history_deleted' => 0,
 'import_records_deleted' => 0,
 'errors' => []
];

// Handle form submission
if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['confirm_reset'])) {
 checkCsrf();

 try {
 // Start transaction
 $db->query("START TRANSACTION");

 // Count existing records before deletion
 $resultsCount = $db->getOne("SELECT COUNT(*) FROM results");
 $importHistoryCount = $db->getOne("SELECT COUNT(*) FROM import_history");
 $importRecordsCount = $db->getOne("SELECT COUNT(*) FROM import_records");

 // Delete all results
 $db->query("DELETE FROM results");
 $stats['results_deleted'] = $resultsCount;
 error_log("Deleted {$resultsCount} results");

 // Delete all import records (tracking data)
 $db->query("DELETE FROM import_records");
 $stats['import_records_deleted'] = $importRecordsCount;
 error_log("Deleted {$importRecordsCount} import records");

 // Delete all import history
 $db->query("DELETE FROM import_history");
 $stats['import_history_deleted'] = $importHistoryCount;
 error_log("Deleted {$importHistoryCount} import history entries");

 // Commit transaction
 $db->query("COMMIT");

 $message ="Alla resultat och importhistorik raderade! {$stats['results_deleted']} resultat, {$stats['import_history_deleted']} importhistorik.";
 $messageType = 'success';

 } catch (Exception $e) {
 $db->query("ROLLBACK");
 $message = 'Fel vid radering: ' . $e->getMessage();
 $messageType = 'error';
 $stats['errors'][] = $e->getMessage();
 }
}

// Get current counts
$currentResultsCount = $db->getOne("SELECT COUNT(*) FROM results");
$currentImportHistoryCount = $db->getOne("SELECT COUNT(*) FROM import_history");
$currentImportRecordsCount = $db->getOne("SELECT COUNT(*) FROM import_records");

$pageTitle = 'Återställ Resultat & Importhistorik';
$pageType = 'admin';
include __DIR__ . '/../includes/layout-header.php';
?>

<main class="main-content">
 <div class="container">
 <!-- Header -->
 <div class="flex items-center justify-between mb-lg">
  <div>
  <h1 class="text-primary">
   <i data-lucide="trash-2"></i>
   Återställ Resultat & Importhistorik
  </h1>
  <p class="text-secondary mt-sm">
   Radera alla resultat och importhistorik
  </p>
  </div>
  <a href="/admin/results.php" class="btn btn--secondary">
  <i data-lucide="arrow-left"></i>
  Tillbaka
  </a>
 </div>

 <!-- Message -->
 <?php if ($message): ?>
  <div class="alert alert-<?= h($messageType) ?> mb-lg">
  <i data-lucide="<?= $messageType === 'success' ? 'check-circle' : 'alert-circle' ?>"></i>
  <?= h($message) ?>
  </div>
 <?php endif; ?>

 <!-- Stats -->
 <?php if ($stats['results_deleted'] > 0 || $stats['import_history_deleted'] > 0): ?>
  <div class="card mb-lg">
  <div class="card-header">
   <h2 class="">Statistik</h2>
  </div>
  <div class="card-body">
   <div class="grid grid-cols-3 gap-md">
   <div>
    <div class="text-sm text-secondary">Raderade resultat</div>
    <div class="text-error"><?= number_format($stats['results_deleted']) ?></div>
   </div>
   <div>
    <div class="text-sm text-secondary">Raderad importhistorik</div>
    <div class="text-error"><?= number_format($stats['import_history_deleted']) ?></div>
   </div>
   <div>
    <div class="text-sm text-secondary">Raderade spårningsposter</div>
    <div class="text-error"><?= number_format($stats['import_records_deleted']) ?></div>
   </div>
   </div>
  </div>
  </div>
 <?php endif; ?>

 <!-- Current Status -->
 <div class="card mb-lg">
  <div class="card-header">
  <h2 class="">Nuvarande status</h2>
  </div>
  <div class="card-body">
  <div class="grid grid-cols-3 gap-md">
   <div>
   <div class="text-sm text-secondary">Resultat i databasen</div>
   <div class="<?= $currentResultsCount > 0 ? 'text-accent' : 'text-secondary' ?>">
    <?= number_format($currentResultsCount) ?>
   </div>
   </div>
   <div>
   <div class="text-sm text-secondary">Importhistorik</div>
   <div class="<?= $currentImportHistoryCount > 0 ? 'text-accent' : 'text-secondary' ?>">
    <?= number_format($currentImportHistoryCount) ?>
   </div>
   </div>
   <div>
   <div class="text-sm text-secondary">Spårningsposter</div>
   <div class="<?= $currentImportRecordsCount > 0 ? 'text-accent' : 'text-secondary' ?>">
    <?= number_format($currentImportRecordsCount) ?>
   </div>
   </div>
  </div>
  </div>
 </div>

 <!-- Warning Card -->
 <div class="card mb-lg">
  <div class="card-header">
  <h2 class="text-error">
   <i data-lucide="alert-triangle"></i>
   VARNING - Läs detta först!
  </h2>
  </div>
  <div class="card-body">
  <p class="text-error mb-md">
   <strong>Detta script kommer att:</strong>
  </p>
  <ul class="text-secondary" class="gs-list-ml-lg-lh-1-8">
   <li>Radera <strong>ALLA resultat</strong> från results-tabellen</li>
   <li>Radera <strong>ALLA importhistorik</strong> från import_history-tabellen</li>
   <li>Radera <strong>ALLA spårningsposter</strong> från import_records-tabellen</li>
   <li>Tömma rollback-menyn helt</li>
  </ul>
  <p class="text-error mt-md">
   <strong>Detta går INTE att ångra!</strong>
  </p>
  <p class="text-secondary mt-md">
   <strong>OBS:</strong> Deltagare (riders), tävlingar (events), serier, klubbar och venues påverkas INTE.
   Endast resultat och importhistorik raderas.
  </p>
  </div>
 </div>

 <!-- What happens after -->
 <div class="card mb-lg">
  <div class="card-header">
  <h2 class="">
   <i data-lucide="info"></i>
   Vad händer efter radering?
  </h2>
  </div>
  <div class="card-body">
  <ul class="text-secondary" class="gs-list-ml-lg-lh-1-8">
   <li>Rollback-menyn blir tom (inga importer att rulla tillbaka)</li>
   <li>Framtida importer kommer att spåras korrekt</li>
   <li>Du kan importera resultat på nytt</li>
   <li>Rollback kommer fungera korrekt för nya importer</li>
   <li>Importhistoriken försvinner när den rullas tillbaka (som förväntat)</li>
  </ul>
  </div>
 </div>

 <!-- Confirm Form -->
 <?php if ($currentResultsCount > 0 || $currentImportHistoryCount > 0): ?>
  <div class="card">
  <div class="card-body">
   <form method="POST" onsubmit="return confirm('Är du ABSOLUT säker på att du vill radera alla resultat och importhistorik? Detta går inte att ångra!');">
   <?= csrf_field() ?>

   <div class="form-group">
    <label class="checkbox-label">
    <input type="checkbox" required>
    <span>Jag förstår att detta kommer radera alla <?= number_format($currentResultsCount) ?> resultat</span>
    </label>
   </div>

   <div class="form-group">
    <label class="checkbox-label">
    <input type="checkbox" required>
    <span>Jag förstår att all importhistorik kommer raderas</span>
    </label>
   </div>

   <div class="form-group">
    <label class="checkbox-label">
    <input type="checkbox" required>
    <span>Jag förstår att detta inte går att ångra</span>
    </label>
   </div>

   <div class="flex gap-md mt-lg">
    <button type="submit" name="confirm_reset" class="btn btn-danger">
    <i data-lucide="trash-2"></i>
    Radera Allt
    </button>
    <a href="/admin/results.php" class="btn btn--secondary">
    <i data-lucide="x"></i>
    Avbryt
    </a>
   </div>
   </form>
  </div>
  </div>
 <?php else: ?>
  <div class="card">
  <div class="card-body">
   <div class="text-center">
   <i data-lucide="check-circle" class="gs-icon-success-center"></i>
   <h3 class="text-success mb-sm">Databasen är redan tom</h3>
   <p class="text-secondary">Det finns inga resultat eller importhistorik att radera.</p>
   <a href="/admin/results.php" class="btn btn--primary mt-lg">
    <i data-lucide="arrow-left"></i>
    Tillbaka till Resultat
   </a>
   </div>
  </div>
  </div>
 <?php endif; ?>
 </div>
</main>

<?php include __DIR__ . '/../includes/layout-footer.php'; ?>
