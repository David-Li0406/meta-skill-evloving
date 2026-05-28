<?php
/**
 * Auto Merge Duplicates Tool
 * Hittar dubbletter där en har UCI-ID och andra har SWE-ID
 * Slår automatiskt ihop dem
 */
require_once __DIR__ . '/../config.php';
require_admin();

$db = getDB();
$message = '';
$messageType = 'info';

// Hitta alla potentiella dubbletter
// Två ryttare med samma förnamn + efternamn + klubb
// Men en har UCI-ID och andra har SWE-ID

$duplicates = [];

try {
 // Strategi 1: Samma förnamn + efternamn + klubb
 // En har UCI-ID (innehåller INTE 'SWE'), andra har SWE-ID
 $results = $db->getAll("
 SELECT 
 r1.id as id1,
 r1.firstname,
 r1.lastname,
 r1.license_number as license1,
 r1.club_id,
 c.name as club_name,
 (SELECT COUNT(*) FROM results WHERE cyclist_id = r1.id) as results1,
 r2.id as id2,
 r2.license_number as license2,
 (SELECT COUNT(*) FROM results WHERE cyclist_id = r2.id) as results2
 FROM riders r1
 LEFT JOIN clubs c ON r1.club_id = c.id
 JOIN riders r2 ON 
 LOWER(r1.firstname) = LOWER(r2.firstname)
 AND LOWER(r1.lastname) = LOWER(r2.lastname)
 AND r1.club_id = r2.club_id
 AND r1.id < r2.id
 WHERE 
 -- En måste ha UCI-ID (ingen SWE)
 ((r1.license_number IS NOT NULL AND r1.license_number != '' AND r1.license_number NOT LIKE 'SWE%')
 OR
 (r2.license_number IS NOT NULL AND r2.license_number != '' AND r2.license_number NOT LIKE 'SWE%'))
 AND
 -- Och andra måste ha SWE-ID eller ingen
 ((r1.license_number IS NULL OR r1.license_number = '' OR r1.license_number LIKE 'SWE%')
 OR
 (r2.license_number IS NULL OR r2.license_number = '' OR r2.license_number LIKE 'SWE%'))
 ORDER BY c.name, r1.lastname, r1.firstname
");
 
 // Organisera resultaten
 $seen = [];
 foreach ($results as $row) {
 $key = $row['id1'] . '-' . $row['id2'];
 if (isset($seen[$key])) continue;
 $seen[$key] = true;
 
 // Bestäm vilken som ska behållas (den med UCI-ID)
 $hasUci1 = !empty($row['license1']) && $row['license1'] !== '' && strpos($row['license1'], 'SWE') === false;
 $hasUci2 = !empty($row['license2']) && $row['license2'] !== '' && strpos($row['license2'], 'SWE') === false;
 
 if ($hasUci1 && !$hasUci2) {
 // r1 har UCI, r2 har SWE/ingen → behål r1
 $duplicates[] = [
 'keep_id' => $row['id1'],
 'keep_name' => $row['firstname'] . ' ' . $row['lastname'],
 'keep_license' => $row['license1'],
 'keep_results' => $row['results1'],
 'merge_id' => $row['id2'],
 'merge_license' => $row['license2'],
 'merge_results' => $row['results2'],
 'club' => $row['club_name'],
 'reason' => 'r1 har UCI-ID'
 ];
 } elseif ($hasUci2 && !$hasUci1) {
 // r2 har UCI, r1 har SWE/ingen → behål r2
 $duplicates[] = [
 'keep_id' => $row['id2'],
 'keep_name' => $row['firstname'] . ' ' . $row['lastname'],
 'keep_license' => $row['license2'],
 'keep_results' => $row['results2'],
 'merge_id' => $row['id1'],
 'merge_license' => $row['license1'],
 'merge_results' => $row['results1'],
 'club' => $row['club_name'],
 'reason' => 'r2 har UCI-ID'
 ];
 }
 }
} catch (Exception $e) {
 $message = 'Fel vid sökning: ' . $e->getMessage();
 $messageType = 'error';
}

// Hantera auto-merge
if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['auto_merge_all'])) {
 checkCsrf();
 
 if (empty($duplicates)) {
 $message = 'Inga dubbletter att slå ihop';
 $messageType = 'info';
 } else {
 try {
 $db->pdo->beginTransaction();
 
 $merged = 0;
 $resultsMoved = 0;
 $resultsDeleted = 0;
 
 foreach ($duplicates as $dup) {
 $keepId = $dup['keep_id'];
 $mergeId = $dup['merge_id'];
 
 // Flytta alla resultat från merge_id till keep_id
 $oldResults = $db->getAll(
 "SELECT id, event_id FROM results WHERE cyclist_id = ?",
  [$mergeId]
 );
 
 foreach ($oldResults as $oldResult) {
  // Kontrollera om keep_id redan har resultat för detta event
  $existing = $db->getRow(
 "SELECT id FROM results WHERE cyclist_id = ? AND event_id = ?",
  [$keepId, $oldResult['event_id']]
  );
  
  if ($existing) {
  // Ta bort duplicerat resultat
  $db->delete('results', 'id = ?', [$oldResult['id']]);
  $resultsDeleted++;
  } else {
  // Flytta resultat
  $db->update('results', ['cyclist_id' => $keepId], 'id = ?', [$oldResult['id']]);
  $resultsMoved++;
  }
 }
 
 // Ta bort duplicerad ryttare
 $db->delete('riders', 'id = ?', [$mergeId]);
 $merged++;
 }
 
 $db->pdo->commit();
 
 $message ="✓ Sammanfogade $merged dubbletter!";
 $message .="$resultsMoved resultat flyttade";
 if ($resultsDeleted > 0) {
 $message .=", $resultsDeleted dubbletter borttagna";
 }
 $messageType = 'success';
 
 // Rensa duplicates för att visa uppdaterad status
 $duplicates = [];
 
 } catch (Exception $e) {
 if ($db->pdo->inTransaction()) {
 $db->pdo->rollBack();
 }
 $message = 'Fel vid sammanslagning: ' . $e->getMessage();
 $messageType = 'error';
 }
 }
}

$pageTitle = 'Auto-merge Dubbletter (UCI vs SWE)';
$pageType = 'admin';
include __DIR__ . '/../includes/layout-header.php';
?>

<main class="main-content">
 <div class="container">
 <h1 class="text-primary mb-lg">
 <i data-lucide="git-merge"></i>
 Auto-merge Dubbletter
 </h1>

 <p class="text-secondary mb-lg">
 Hittar automatiskt ryttare som är dubbletter där en har UCI-ID och andra har SWE-ID.
 <br>Slår ihop dem och behåller UCI-ID:n.
 </p>

 <?php if ($message): ?>
 <div class="alert alert-<?= $messageType ?> mb-lg">
 <i data-lucide="<?= $messageType === 'success' ? 'check-circle' : ($messageType === 'error' ? 'alert-circle' : 'info') ?>"></i>
 <?= h($message) ?>
 </div>
 <?php endif; ?>

 <!-- Duplicates Found -->
 <?php if (!empty($duplicates)): ?>
 <div class="card mb-lg">
 <div class="card-header">
  <h2 class="text-primary">
  <i data-lucide="alert-triangle"></i>
  Hittade <?= count($duplicates) ?> dubbletter
  </h2>
 </div>
 <div class="card-body">
  <div class="gs-overflow-x-auto mb-lg">
  <table class="table">
  <thead>
  <tr>
   <th>Klubb</th>
   <th>Namn</th>
   <th>Behål (UCI)</th>
   <th>Ta bort (SWE)</th>
   <th>Resultat</th>
  </tr>
  </thead>
  <tbody>
  <?php foreach ($duplicates as $dup): ?>
   <tr>
   <td>
   <strong><?= h($dup['club']) ?></strong>
   </td>
   <td>
   <strong><?= h($dup['keep_name']) ?></strong>
   <br><span class="text-xs text-secondary">(ID: <?= $dup['keep_id'] ?>, <?= $dup['merge_id'] ?>)</span>
   </td>
   <td>
   <code class="text-success"><?= h($dup['keep_license']) ?></code>
   <br><span class="text-xs"><?= $dup['keep_results'] ?> res.</span>
   </td>
   <td>
   <code class="text-secondary"><?= h($dup['merge_license'] ?: 'ingen') ?></code>
   <br><span class="text-xs"><?= $dup['merge_results'] ?> res.</span>
   </td>
   <td>
   <?= ($dup['keep_results'] + $dup['merge_results']) ?> totalt
   </td>
   </tr>
  <?php endforeach; ?>
  </tbody>
  </table>
  </div>

  <form method="POST" onsubmit="return confirm('Slå ihop alla <?= count($duplicates) ?> dubbletter? Detta kan inte ångras!');">
  <?= csrf_field() ?>
  <button type="submit" name="auto_merge_all" class="btn btn--primary btn-lg">
  <i data-lucide="git-merge"></i>
  Slå ihop alla dubbletter
  </button>
  </form>
 </div>
 </div>
 <?php else: ?>
 <div class="card">
 <div class="card-header">
  <h2 class="text-primary">Status</h2>
 </div>
 <div class="card-body">
  <div class="alert alert--success">
  <i data-lucide="check-circle"></i>
  Inga dubbletter hittades! Databasen är ren.
  </div>
 </div>
 </div>
 <?php endif; ?>

 <div class="mt-lg">
 <a href="/admin/" class="btn btn--secondary">
 <i data-lucide="arrow-left"></i>
 Tillbaka
 </a>
 </div>
 </div>
</main>

<?php include __DIR__ . '/../includes/layout-footer.php'; ?>
