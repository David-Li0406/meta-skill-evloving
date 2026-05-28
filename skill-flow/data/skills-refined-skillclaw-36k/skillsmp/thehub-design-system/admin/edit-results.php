<?php
require_once __DIR__ . '/../config.php';
require_once __DIR__ . '/../includes/point-calculations.php';
require_admin();

$db = getDB();

// Get event ID from URL (accept both 'id', 'event_id', and 'event' for flexibility)
$eventId = isset($_GET['id']) ? (int)$_GET['id'] : (isset($_GET['event_id']) ? (int)$_GET['event_id'] : (isset($_GET['event']) ? (int)$_GET['event'] : 0));

if (!$eventId) {
 header('Location: /admin/results.php');
 exit;
}

// Fetch event details
$event = $db->getRow("SELECT e.*, s.name as series_name FROM events e LEFT JOIN series s ON e.series_id = s.id WHERE e.id = ?", [$eventId]);

if (!$event) {
 header('Location: /admin/results.php');
 exit;
}

// Check if DH event for displaying run times
$eventFormat = $event['event_format'] ?? 'ENDURO';
$isDH = in_array($eventFormat, ['DH_STANDARD', 'DH_SWECUP']);

$message = '';
$messageType = 'info';

// Handle form submission for updating results
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
 checkCsrf();

 $resultId = isset($_POST['result_id']) ? (int)$_POST['result_id'] : 0;
 $action = $_POST['action'] ?? '';

 if ($action === 'set_license') {
 // Set license for a rider
 $riderId = isset($_POST['rider_id']) ? (int)$_POST['rider_id'] : 0;
 $licenseType = trim($_POST['license_type'] ?? '');
 $currentYear = (int)date('Y');

 if ($riderId && in_array($licenseType, ['motionslicens', 'engangslicens', 'baslicens'])) {
  try {
  $db->update('riders', [
   'license_type' => $licenseType,
   'license_year' => $currentYear
  ], 'id = ?', [$riderId]);
  $message = 'Licens uppdaterad till ' . ucfirst($licenseType) . ' för ' . $currentYear . '!';
  $messageType = 'success';
  } catch (Exception $e) {
  $message = 'Fel vid uppdatering av licens: ' . $e->getMessage();
  $messageType = 'error';
  }
 } else {
  $message = 'Ogiltig licenstyp eller åkare.';
  $messageType = 'error';
 }
 } elseif ($action === 'update' && $resultId) {
 // Update result
 $updateData = [
  'position' => !empty($_POST['position']) ? (int)$_POST['position'] : null,
  'bib_number' => trim($_POST['bib_number'] ?? ''),
  'finish_time' => !empty($_POST['finish_time']) ? trim($_POST['finish_time']) : null,
  'points' => !empty($_POST['points']) ? (float)$_POST['points'] : 0,
  'status' => trim($_POST['status'] ?? 'finished'),
 ];

 // Update class if provided
 if (isset($_POST['class_id']) && $_POST['class_id'] !== '') {
  $updateData['class_id'] = (int)$_POST['class_id'];
 }

 // Add DH run times if provided
 if (isset($_POST['run_1_time'])) {
  $updateData['run_1_time'] = !empty($_POST['run_1_time']) ? trim($_POST['run_1_time']) : null;
 }
 if (isset($_POST['run_2_time'])) {
  $updateData['run_2_time'] = !empty($_POST['run_2_time']) ? trim($_POST['run_2_time']) : null;
 }

 try {
  $db->update('results', $updateData, 'id = ?', [$resultId]);
  $message = 'Resultat uppdaterat!';
  $messageType = 'success';
 } catch (Exception $e) {
  $message = 'Fel vid uppdatering: ' . $e->getMessage();
  $messageType = 'error';
 }
 } elseif ($action === 'delete' && $resultId) {
 // Delete result
 try {
  $db->delete('results', 'id = ?', [$resultId]);
  $message = 'Resultat borttaget!';
  $messageType = 'success';
 } catch (Exception $e) {
  $message = 'Fel vid borttagning: ' . $e->getMessage();
  $messageType = 'error';
 }
 } elseif ($action === 'recalculate') {
 // Recalculate points for this event - use appropriate function based on format
 try {
  $eventFormat = $event['event_format'] ?? 'ENDURO';
  $isDH = in_array($eventFormat, ['DH_STANDARD', 'DH_SWECUP']);

  if ($isDH) {
   $useSwecupDh = ($eventFormat === 'DH_SWECUP');
   $stats = recalculateDHEventResults($db, $eventId, null, $useSwecupDh);
   $message = "DH-resultat omräknade! Positioner: {$stats['positions_updated']}, Poäng: {$stats['points_updated']}";
   $messageType = !empty($stats['errors']) ? 'warning' : 'success';
  } else {
   $stats = recalculateEventResults($db, $eventId);
   $message = "Resultat omräknade! Positioner: {$stats['positions_updated']}, Poäng: {$stats['points_updated']}";
   $messageType = !empty($stats['errors']) ? 'warning' : 'success';
  }
 } catch (Exception $e) {
  $message = 'Fel vid omräkning: ' . $e->getMessage();
  $messageType = 'error';
 }
 } elseif ($action === 'move_all_class') {
 // Move all results from one class to another
 $fromClassId = isset($_POST['from_class_id']) ? (int)$_POST['from_class_id'] : 0;
 $toClassId = isset($_POST['to_class_id']) ? (int)$_POST['to_class_id'] : 0;

 if ($fromClassId && $toClassId && $fromClassId !== $toClassId) {
  try {
   // Count affected results
   $count = $db->getRow(
    "SELECT COUNT(*) as cnt FROM results WHERE event_id = ? AND class_id = ?",
    [$eventId, $fromClassId]
   )['cnt'] ?? 0;

   if ($count > 0) {
    // Update all results from source class to target class
    $db->query(
     "UPDATE results SET class_id = ? WHERE event_id = ? AND class_id = ?",
     [$toClassId, $eventId, $fromClassId]
    );

    // Get class names for message
    $fromClass = $db->getRow("SELECT name, display_name FROM classes WHERE id = ?", [$fromClassId]);
    $toClass = $db->getRow("SELECT name, display_name FROM classes WHERE id = ?", [$toClassId]);

    $message = "$count deltagare flyttade från " . ($fromClass['display_name'] ?? $fromClass['name']) . " till " . ($toClass['display_name'] ?? $toClass['name']) . "!";
    $messageType = 'success';
   } else {
    $message = "Inga deltagare att flytta.";
    $messageType = 'warning';
   }
  } catch (Exception $e) {
   $message = 'Fel vid flytt: ' . $e->getMessage();
   $messageType = 'error';
  }
 } else {
  $message = 'Ogiltig käll- eller målklass.';
  $messageType = 'error';
 }
 } elseif ($action === 'save_all' && isset($_POST['results']) && is_array($_POST['results'])) {
 // Save all results at once
 $updated = 0;
 $errors = [];

 foreach ($_POST['results'] as $resId => $data) {
  $resId = (int)$resId;
  if ($resId < 1) continue;

  $updateData = [
   'position' => !empty($data['position']) ? (int)$data['position'] : null,
   'bib_number' => trim($data['bib_number'] ?? ''),
   'finish_time' => !empty($data['finish_time']) ? trim($data['finish_time']) : null,
   'points' => isset($data['points']) ? (float)$data['points'] : 0,
   'status' => trim($data['status'] ?? 'finished'),
  ];

  if (isset($data['class_id']) && $data['class_id'] !== '') {
   $updateData['class_id'] = (int)$data['class_id'];
  }

  if (isset($data['run_1_time'])) {
   $updateData['run_1_time'] = !empty($data['run_1_time']) ? trim($data['run_1_time']) : null;
  }
  if (isset($data['run_2_time'])) {
   $updateData['run_2_time'] = !empty($data['run_2_time']) ? trim($data['run_2_time']) : null;
  }

  try {
   $db->update('results', $updateData, 'id = ?', [$resId]);
   $updated++;
  } catch (Exception $e) {
   $errors[] = "Resultat $resId: " . $e->getMessage();
  }
 }

 if ($updated > 0) {
  $message = "$updated resultat sparade!";
  $messageType = 'success';
  if (!empty($errors)) {
   $message .= " (" . count($errors) . " fel)";
   $messageType = 'warning';
  }
 } else {
  $message = "Inga resultat uppdaterades.";
  $messageType = 'error';
 }
 }
}

// Fetch all results for this event
$currentYear = (int)date('Y');
$results = $db->getAll("
 SELECT
 res.*,
 r.id as rider_id,
 r.firstname,
 r.lastname,
 r.gender,
 r.birth_year,
 r.license_type,
 r.license_year,
 r.license_number,
 CASE
  WHEN r.license_year = ? AND r.license_type IS NOT NULL AND r.license_type != ''
  AND r.license_type NOT IN ('engangslicens', 'Engångslicens', 'sweid', 'SWE ID')
  THEN 1
  ELSE 0
 END as has_active_license,
 c.name as club_name,
 cls.name as class_name,
 cls.display_name as class_display_name,
 cls.sort_order as class_sort_order
 FROM results res
 INNER JOIN riders r ON res.cyclist_id = r.id
 LEFT JOIN clubs c ON r.club_id = c.id
 LEFT JOIN classes cls ON res.class_id = cls.id
 WHERE res.event_id = ?
 ORDER BY
 cls.sort_order ASC,
 COALESCE(cls.name, 'Oklassificerad'),
 CASE WHEN res.status = 'finished' THEN res.class_position ELSE 999 END,
 res.finish_time
", [$currentYear, $eventId]);

// Group results by class
$resultsByClass = [];
foreach ($results as $result) {
 $className = $result['class_name'] ?? 'Oklassificerad';
 if (!isset($resultsByClass[$className])) {
 $resultsByClass[$className] = [
  'display_name' => $result['class_display_name'] ?? $className,
  'sort_order' => $result['class_sort_order'] ?? 999,
  'results' => []
 ];
 }
 $resultsByClass[$className]['results'][] = $result;
}

// Sort by sort_order
uksort($resultsByClass, function($a, $b) use ($resultsByClass) {
 return $resultsByClass[$a]['sort_order'] - $resultsByClass[$b]['sort_order'];
});

// Get all classes for dropdown
$classes = $db->getAll("SELECT id, name, display_name FROM classes WHERE active = 1 ORDER BY sort_order, name");

// Page config for unified layout
$page_title = 'Editera Resultat - ' . $event['name'];
$breadcrumbs = [
    ['label' => 'Resultat', 'url' => '/admin/results.php'],
    ['label' => $event['name']]
];
$page_actions = '<form method="POST" style="display: inline;">
    ' . csrf_field() . '
    <input type="hidden" name="action" value="recalculate">
    <button type="submit" class="btn-admin btn-admin-secondary" onclick="return confirm(\'Räkna om poäng för alla resultat i detta event?\')">
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="16" height="16"><rect width="16" height="20" x="4" y="2" rx="2"/><line x1="8" x2="16" y1="6" y2="6"/><line x1="8" x2="16" y1="10" y2="10"/><line x1="8" x2="16" y1="14" y2="14"/><line x1="8" x2="16" y1="18" y2="18"/></svg>
        Räkna om poäng
    </button>
</form>
<a href="/admin/results.php" class="btn-admin btn-admin-secondary">
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="16" height="16"><path d="m12 19-7-7 7-7"/><path d="M19 12H5"/></svg>
    Tillbaka
</a>';

include __DIR__ . '/components/unified-layout.php';
?>

<!-- Message -->
 <?php if ($message): ?>
  <div class="alert alert-<?= h($messageType) ?> mb-lg">
  <i data-lucide="<?= $messageType === 'success' ? 'check-circle' : 'alert-circle' ?>"></i>
  <?= h($message) ?>
  </div>
 <?php endif; ?>

 <?php if (empty($results)): ?>
  <div class="card">
  <div class="card-body">
   <div class="alert alert--warning">
   <p>Inga resultat hittades för detta event.</p>
   </div>
  </div>
  </div>
 <?php else: ?>
  <!-- Save All Button -->
  <form method="POST" id="save-all-form">
   <?= csrf_field() ?>
   <input type="hidden" name="action" value="save_all">

   <div class="mb-md">
    <button type="submit" class="btn btn--primary btn--lg">
     <i data-lucide="save"></i>
     Spara alla ändringar
    </button>
   </div>

  <!-- Results by Class -->
  <?php foreach ($resultsByClass as $className => $classData):
   // Get class_id from first result in this class
   $currentClassId = $classData['results'][0]['class_id'] ?? 0;
  ?>
  <div class="card mb-lg">
   <div class="card-header">
   <div class="flex items-center justify-between flex-wrap gap-sm">
    <h3 class="text-primary gs-mb-0">
     <i data-lucide="users"></i>
     <?= h($classData['display_name']) ?>
     <span class="badge badge-primary badge-sm gs-ml-xs">
     <?= h($className) ?>
     </span>
     <span class="badge badge-secondary ml-sm">
     <?= count($classData['results']) ?> deltagare
     </span>
    </h3>
    <!-- Move All Control -->
    <div class="flex items-center gap-xs">
     <select id="move-target-<?= $currentClassId ?>" class="input input-xs" style="min-width: 150px;">
      <option value="">Flytta alla till...</option>
      <?php foreach ($classes as $class): ?>
       <?php if ($class['id'] != $currentClassId): ?>
       <option value="<?= $class['id'] ?>"><?= h($class['display_name'] ?? $class['name']) ?></option>
       <?php endif; ?>
      <?php endforeach; ?>
     </select>
     <button type="button"
      class="btn btn--secondary btn--sm move-all-btn"
      data-from-class="<?= $currentClassId ?>"
      data-class-name="<?= h($classData['display_name']) ?>"
      title="Flytta alla deltagare">
      <i data-lucide="arrow-right-left"></i>
      Flytta
     </button>
    </div>
   </div>
   </div>
   <div class="card-body gs-p-0 table-scrollable">
   <table class="table table-sm">
    <thead>
    <tr>
     <th class="table-th-w60">Plac.</th>
     <th>Namn</th>
     <th class="table-th-w140">Klass</th>
     <th class="table-th-w120">Licens</th>
     <th class="table-th-w150">Klubb</th>
     <th class="table-th-w100">Startnr</th>
     <?php if ($isDH): ?>
     <th class="table-th-w100"><?= $eventFormat === 'DH_SWECUP' ? 'Kval' : 'Åk 1' ?></th>
     <th class="table-th-w100"><?= $eventFormat === 'DH_SWECUP' ? 'Final' : 'Åk 2' ?></th>
     <?php endif; ?>
     <th class="table-th-w120"><?= $isDH ? 'Bästa' : 'Tid' ?></th>
     <th class="table-th-w80">Poäng</th>
     <th class="table-th-w120">Status</th>
     <th class="table-th-w120">Åtgärder</th>
    </tr>
    </thead>
    <tbody>
    <?php foreach ($classData['results'] as $result): ?>
     <tr id="result-row-<?= $result['id'] ?>" data-result-id="<?= $result['id'] ?>">
      <!-- Position -->
      <td class="text-center">
      <input type="number"
       name="results[<?= $result['id'] ?>][position]"
       value="<?= h($result['position']) ?>"
       class="input input-w60"
       min="1">
      </td>

      <!-- Name (read-only) -->
      <td>
      <strong><?= h($result['firstname']) ?> <?= h($result['lastname']) ?></strong>
      <div class="gs-rider-meta-text">
       <?php if ($result['birth_year']): ?>
       <?= calculateAge($result['birth_year']) ?> år
       <?php endif; ?>
       <?php if ($result['gender']): ?>
       • <?= $result['gender'] == 'M' ? 'Herr' : ($result['gender'] == 'F' ? 'Dam' : '') ?>
       <?php endif; ?>
      </div>
      </td>

      <!-- Class -->
      <td>
      <select name="results[<?= $result['id'] ?>][class_id]" class="input input-xs">
       <?php foreach ($classes as $class): ?>
       <option value="<?= $class['id'] ?>" <?= $result['class_id'] == $class['id'] ? 'selected' : '' ?>>
        <?= h($class['display_name'] ?? $class['name']) ?>
       </option>
       <?php endforeach; ?>
      </select>
      </td>

      <!-- License -->
      <td>
      <?php if ($result['has_active_license']): ?>
       <span class="badge badge-success badge-sm">
       <?= h($result['license_type']) ?>
       </span>
      <?php elseif ($result['license_number']): ?>
       <!-- Has SWE ID but no active license - allow setting -->
       <div class="flex gap-xs items-center">
       <span class="badge badge-warning badge-sm" title="SWE ID utan aktiv licens">
        SWE ID
       </span>
       <button type="button"
        class="btn btn--secondary btn-xs set-license-btn"
        data-rider-id="<?= $result['rider_id'] ?>"
        data-rider-name="<?= h($result['firstname'] . ' ' . $result['lastname']) ?>"
        title="Tilldela licens">
        <i data-lucide="id-card" class="gs-icon-12"></i>
       </button>
       </div>
      <?php else: ?>
       <span class="text-secondary text-xs">-</span>
      <?php endif; ?>
      </td>

      <!-- Club (read-only) -->
      <td>
      <?php if ($result['club_name']): ?>
       <span class="badge badge-secondary badge-sm">
       <?= h($result['club_name']) ?>
       </span>
      <?php else: ?>
       <span class="text-secondary">-</span>
      <?php endif; ?>
      </td>

      <!-- Bib Number -->
      <td class="text-center">
      <input type="text"
       name="results[<?= $result['id'] ?>][bib_number]"
       value="<?= h($result['bib_number']) ?>"
       class="input input-w80">
      </td>

      <!-- DH Run Times -->
      <?php if ($isDH): ?>
      <td class="text-center">
      <input type="text"
       name="results[<?= $result['id'] ?>][run_1_time]"
       value="<?= h($result['run_1_time'] ?? '') ?>"
       class="input input-w100-mono"
       placeholder="M:SS.mm">
      </td>
      <td class="text-center">
      <input type="text"
       name="results[<?= $result['id'] ?>][run_2_time]"
       value="<?= h($result['run_2_time'] ?? '') ?>"
       class="input input-w100-mono"
       placeholder="M:SS.mm">
      </td>
      <?php endif; ?>

      <!-- Finish Time -->
      <td class="text-center">
      <input type="text"
       name="results[<?= $result['id'] ?>][finish_time]"
       value="<?= h($result['finish_time']) ?>"
       class="input input-w100-mono"
       placeholder="<?= $isDH ? 'Auto' : 'HH:MM:SS' ?>"
       <?= $isDH ? 'readonly style="background: var(--color-star-fade);"' : '' ?>>
      </td>

      <!-- Points -->
      <td class="text-center">
      <input type="number"
       name="results[<?= $result['id'] ?>][points]"
       value="<?= h($result['points']) ?>"
       class="input input-w70"
       step="1"
       min="0">
      </td>

      <!-- Status -->
      <td class="text-center">
      <select name="results[<?= $result['id'] ?>][status]" class="input input-xs">
       <option value="finished" <?= $result['status'] === 'finished' ? 'selected' : '' ?>>Slutförd</option>
       <option value="dnf" <?= $result['status'] === 'dnf' ? 'selected' : '' ?>>DNF</option>
       <option value="dns" <?= $result['status'] === 'dns' ? 'selected' : '' ?>>DNS</option>
       <option value="dq" <?= $result['status'] === 'dq' ? 'selected' : '' ?>>DQ</option>
      </select>
      </td>

      <!-- Actions -->
      <td class="text-center">
       <button type="button"
        class="btn btn-danger btn--sm delete-result"
        data-result-id="<?= $result['id'] ?>"
        data-rider-name="<?= h($result['firstname'] . ' ' . $result['lastname']) ?>"
        title="Ta bort">
       <i data-lucide="trash-2" class="icon-sm"></i>
       </button>
      </td>
     </tr>
    <?php endforeach; ?>
    </tbody>
   </table>
   </div>
  </div>
  <?php endforeach; ?>

   <!-- Save All Button Bottom -->
   <div class="mt-md">
    <button type="submit" class="btn btn--primary btn--lg">
     <i data-lucide="save"></i>
     Spara alla ändringar
    </button>
   </div>
  </form>
 <?php endif; ?>

<!-- License Assignment Modal -->
<div id="license-modal" class="gs-modal hidden">
 <div class="gs-modal-backdrop"></div>
 <div class="gs-modal-content" style="max-width: 400px;">
 <div class="gs-modal-header">
  <h3 class="">
  <i data-lucide="id-card"></i>
  Tilldela licens
  </h3>
  <button type="button" class="btn btn-ghost btn--sm close-modal">
  <i data-lucide="x"></i>
  </button>
 </div>
 <form method="POST" id="license-form">
  <?= csrf_field() ?>
  <input type="hidden" name="action" value="set_license">
  <input type="hidden" name="rider_id" id="modal-rider-id" value="">

  <div class="gs-modal-body">
  <p class="mb-md">
   Tilldela licens till <strong id="modal-rider-name"></strong> för <?= date('Y') ?>:
  </p>

  <div class="grid gap-sm">
   <label class="card p-md" style="cursor: pointer; border: 2px solid var(--border);">
   <div class="flex items-center gap-md">
    <input type="radio" name="license_type" value="motionslicens" required>
    <div>
    <strong>Motionslicens</strong>
    <p class="text-sm text-secondary gs-mb-0">För motionslopp och breddtävlingar</p>
    </div>
   </div>
   </label>

   <label class="card p-md" style="cursor: pointer; border: 2px solid var(--border);">
   <div class="flex items-center gap-md">
    <input type="radio" name="license_type" value="baslicens">
    <div>
    <strong>Baslicens</strong>
    <p class="text-sm text-secondary gs-mb-0">Grundläggande licens</p>
    </div>
   </div>
   </label>

   <label class="card p-md" style="cursor: pointer; border: 2px solid var(--border);">
   <div class="flex items-center gap-md">
    <input type="radio" name="license_type" value="engangslicens">
    <div>
    <strong>Engångslicens</strong>
    <p class="text-sm text-secondary gs-mb-0">Engångslicens för enstaka tävling</p>
    </div>
   </div>
   </label>
  </div>
  </div>

  <div class="gs-modal-footer">
  <button type="button" class="btn btn--secondary close-modal">Avbryt</button>
  <button type="submit" class="btn btn--primary">
   <i data-lucide="check"></i>
   Tilldela licens
  </button>
  </div>
 </form>
 </div>
</div>

<script src="https://unpkg.com/lucide@latest"></script>
<script>
 lucide.createIcons();

 // Delete result confirmation
 document.querySelectorAll('.delete-result').forEach(btn => {
 btn.addEventListener('click', function() {
  const resultId = this.dataset.resultId;
  const riderName = this.dataset.riderName;

  if (confirm('Är du säker på att du vill ta bort resultatet för ' + riderName + '?')) {
  const form = document.createElement('form');
  form.method = 'POST';
  form.innerHTML = `
   <?= csrf_field() ?>
   <input type="hidden" name="result_id" value="${resultId}">
   <input type="hidden" name="action" value="delete">
  `;
  document.body.appendChild(form);
  form.submit();
  }
 });
 });

 // License assignment modal
 const modal = document.getElementById('license-modal');

 document.querySelectorAll('.set-license-btn').forEach(btn => {
 btn.addEventListener('click', function() {
  const riderId = this.dataset.riderId;
  const riderName = this.dataset.riderName;

  document.getElementById('modal-rider-id').value = riderId;
  document.getElementById('modal-rider-name').textContent = riderName;

  // Reset radio buttons
  document.querySelectorAll('#license-form input[type="radio"]').forEach(r => r.checked = false);

  modal.style.display = 'flex';
  lucide.createIcons();
 });
 });

 // Close modal
 document.querySelectorAll('.close-modal, .gs-modal-backdrop').forEach(el => {
 el.addEventListener('click', function() {
  modal.style.display = 'none';
 });
 });

 // Highlight selected license card
 document.querySelectorAll('#license-form input[type="radio"]').forEach(radio => {
 radio.addEventListener('change', function() {
  document.querySelectorAll('#license-form label.card').forEach(card => {
  card.style.borderColor = 'var(--border)';
  card.style.backgroundColor = '';
  });
  if (this.checked) {
  const card = this.closest('label');
  card.style.borderColor = 'var(--primary)';
  card.style.backgroundColor = 'var(--primary-light, rgba(var(--primary-rgb), 0.1))';
  }
 });
 });

 // Move all participants from one class to another
 document.querySelectorAll('.move-all-btn').forEach(btn => {
 btn.addEventListener('click', function() {
  const fromClassId = this.dataset.fromClass;
  const className = this.dataset.className;
  const selectEl = document.getElementById('move-target-' + fromClassId);
  const toClassId = selectEl.value;

  if (!toClassId) {
  alert('Välj en målklass först.');
  return;
  }

  const targetClassName = selectEl.options[selectEl.selectedIndex].text;

  if (confirm('Flytta ALLA deltagare från "' + className + '" till "' + targetClassName + '"?\n\nDetta påverkar alla deltagare i klassen.')) {
  const form = document.createElement('form');
  form.method = 'POST';
  form.innerHTML = `
   <?= csrf_field() ?>
   <input type="hidden" name="action" value="move_all_class">
   <input type="hidden" name="from_class_id" value="${fromClassId}">
   <input type="hidden" name="to_class_id" value="${toClassId}">
  `;
  document.body.appendChild(form);
  form.submit();
  }
 });
 });
</script>

<?php include __DIR__ . '/components/unified-layout-footer.php'; ?>
