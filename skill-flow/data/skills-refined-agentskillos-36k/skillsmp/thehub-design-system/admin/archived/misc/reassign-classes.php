<?php
/**
 * Admin tool to reassign classes based on rider gender and age
 * Useful when riders are in wrong classes after import
 */
require_once __DIR__ . '/../config.php';
require_once __DIR__ . '/../includes/class-calculations.php';
require_admin();

$db = getDB();
$message = '';
$messageType = 'info';

// Get all events with results
$events = $db->getAll("
 SELECT e.id, e.name, e.date, e.discipline,
  COUNT(r.id) as result_count
 FROM events e
 INNER JOIN results r ON e.id = r.event_id
 GROUP BY e.id
 ORDER BY e.date DESC
 LIMIT 100
");

// Handle reassign action
if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['reassign_classes'])) {
 checkCsrf();

 $eventId = (int)$_POST['event_id'];

 if ($eventId) {
 try {
  $db->pdo->beginTransaction();

  // Get event info
  $event = $db->getRow("SELECT date, discipline FROM events WHERE id = ?", [$eventId]);
  if (!$event) {
  throw new Exception("Event hittades inte");
  }

  // Get all results with rider info
  $results = $db->getAll("
  SELECT r.id as result_id, r.cyclist_id, r.class_id,
   c.firstname, c.lastname, c.gender, c.birth_year,
   cls.name as old_class_name, cls.display_name as old_class_display
  FROM results r
  INNER JOIN riders c ON r.cyclist_id = c.id
  LEFT JOIN classes cls ON r.class_id = cls.id
  WHERE r.event_id = ?
 ", [$eventId]);

  $updated = 0;
  $skipped = 0;
  $errors = [];

  foreach ($results as $result) {
  if (!$result['birth_year'] || !$result['gender']) {
   $skipped++;
   continue;
  }

  // Determine correct class
  $correctClassId = determineRiderClass(
   $db,
   $result['birth_year'],
   $result['gender'],
   $event['date'],
   $event['discipline'] ?? 'ENDURO'
  );

  if ($correctClassId && $correctClassId != $result['class_id']) {
   // Update the class
   $db->update('results', ['class_id' => $correctClassId], 'id = ?', [$result['result_id']]);
   $updated++;

   // Log the change
   $newClass = $db->getRow("SELECT display_name FROM classes WHERE id = ?", [$correctClassId]);
   error_log("Reassigned {$result['firstname']} {$result['lastname']} from '{$result['old_class_display']}' to '{$newClass['display_name']}'");
  } else {
   $skipped++;
  }
  }

  $db->pdo->commit();

  $message ="Omtilldelade klasser för" . count($results) ." resultat: $updated uppdaterade, $skipped oförändrade";
  $messageType = 'success';

 } catch (Exception $e) {
  if ($db->pdo->inTransaction()) {
  $db->pdo->rollBack();
  }
  $message ="Fel vid omtilldelning:" . $e->getMessage();
  $messageType = 'error';
 }
 } else {
 $message ="Välj ett event";
 $messageType = 'error';
 }
}

// Handle preview action
$previewResults = [];
$previewEventId = null;
if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['preview_classes'])) {
 checkCsrf();

 $previewEventId = (int)$_POST['event_id'];

 if ($previewEventId) {
 $event = $db->getRow("SELECT date, discipline FROM events WHERE id = ?", [$previewEventId]);

 if ($event) {
  $results = $db->getAll("
  SELECT r.id as result_id, r.cyclist_id, r.class_id,
   c.firstname, c.lastname, c.gender, c.birth_year,
   cls.name as old_class_name, cls.display_name as old_class_display
  FROM results r
  INNER JOIN riders c ON r.cyclist_id = c.id
  LEFT JOIN classes cls ON r.class_id = cls.id
  WHERE r.event_id = ?
  ORDER BY cls.sort_order, c.lastname
 ", [$previewEventId]);

  foreach ($results as $result) {
  $correctClassId = null;
  $correctClassName = null;
  $needsChange = false;

  if ($result['birth_year'] && $result['gender']) {
   $correctClassId = determineRiderClass(
   $db,
   $result['birth_year'],
   $result['gender'],
   $event['date'],
   $event['discipline'] ?? 'ENDURO'
   );

   if ($correctClassId) {
   $correctClass = $db->getRow("SELECT display_name FROM classes WHERE id = ?", [$correctClassId]);
   $correctClassName = $correctClass['display_name'] ?? 'Okänd';
   $needsChange = ($correctClassId != $result['class_id']);
   }
  }

  $previewResults[] = [
   'firstname' => $result['firstname'],
   'lastname' => $result['lastname'],
   'gender' => $result['gender'],
   'birth_year' => $result['birth_year'],
   'old_class' => $result['old_class_display'] ?? 'Ingen',
   'new_class' => $correctClassName ?? 'Kan ej bestämmas',
   'needs_change' => $needsChange
  ];
  }
 }
 }
}

$pageTitle = 'Omtilldela Klasser';
$pageType = 'admin';
include __DIR__ . '/../includes/layout-header.php';
?>

<main class="main-content">
 <div class="container">
 <div class="mb-lg">
  <a href="/admin/system-settings.php?tab=debug" class="btn btn--secondary btn--sm">
  <i data-lucide="arrow-left"></i>
  Tillbaka
  </a>
 </div>

 <h1 class="text-primary mb-lg">
  <i data-lucide="refresh-cw"></i>
  Omtilldela Klasser
 </h1>

 <?php if ($message): ?>
  <div class="alert alert-<?= $messageType ?> mb-lg">
  <i data-lucide="<?= $messageType === 'success' ? 'check-circle' : 'alert-circle' ?>"></i>
  <?= h($message) ?>
  </div>
 <?php endif; ?>

 <!-- Info Box -->
 <div class="alert alert--info mb-lg">
  <i data-lucide="info"></i>
  <div>
  <strong>Om detta verktyg:</strong><br>
  Omtilldelar klasser för alla resultat i ett event baserat på deltagarens kön och ålder.
  Användbart när resultat har importerats med fel klassplacering (t.ex. pojkar i flickklass).
  </div>
 </div>

 <!-- Event Selection Form -->
 <div class="card mb-lg">
  <div class="card-header">
  <h2 class="text-primary">
   <i data-lucide="calendar"></i>
   Välj Event
  </h2>
  </div>
  <div class="card-body">
  <form method="POST">
   <?= csrf_field() ?>
   <div class="form-group mb-md">
   <label class="label">Event med resultat</label>
   <select name="event_id" class="input" required>
    <option value="">Välj event...</option>
    <?php foreach ($events as $event): ?>
    <option value="<?= $event['id'] ?>" <?= $previewEventId == $event['id'] ? 'selected' : '' ?>>
     <?= h($event['name']) ?> (<?= date('Y-m-d', strtotime($event['date'])) ?>) - <?= $event['result_count'] ?> resultat
    </option>
    <?php endforeach; ?>
   </select>
   </div>
   <div class="flex gap-md">
   <button type="submit" name="preview_classes" class="btn btn--secondary">
    <i data-lucide="eye"></i>
    Förhandsgranska
   </button>
   <button type="submit" name="reassign_classes" class="btn btn-warning"
    onclick="return confirm('Omtilldela klasser för alla resultat i valt event?');">
    <i data-lucide="refresh-cw"></i>
    Omtilldela Klasser
   </button>
   </div>
  </form>
  </div>
 </div>

 <!-- Preview Results -->
 <?php if (!empty($previewResults)): ?>
  <div class="card">
  <div class="card-header">
   <h2 class="text-primary">
   <i data-lucide="list"></i>
   Förhandsgranskning (<?= count($previewResults) ?> deltagare)
   </h2>
  </div>
  <div class="card-body gs-p-0">
   <div class="table-responsive">
   <table class="table">
    <thead>
    <tr>
     <th>Namn</th>
     <th>Kön</th>
     <th>Födelseår</th>
     <th>Nuvarande Klass</th>
     <th>Korrekt Klass</th>
     <th>Status</th>
    </tr>
    </thead>
    <tbody>
    <?php foreach ($previewResults as $result): ?>
     <tr class="<?= $result['needs_change'] ? 'gs-bg-warning-light' : '' ?>">
     <td><strong><?= h($result['firstname']) ?> <?= h($result['lastname']) ?></strong></td>
     <td>
      <?php if ($result['gender'] === 'M'): ?>
      <span class="badge badge-primary">Man</span>
      <?php elseif (in_array($result['gender'], ['F', 'K'])): ?>
      <span class="badge badge-accent">Kvinna</span>
      <?php else: ?>
      <span class="badge badge-secondary">-</span>
      <?php endif; ?>
     </td>
     <td><?= $result['birth_year'] ?: '-' ?></td>
     <td><?= h($result['old_class']) ?></td>
     <td><?= h($result['new_class']) ?></td>
     <td>
      <?php if ($result['needs_change']): ?>
      <span class="badge badge-warning">
       <i data-lucide="alert-triangle" class="gs-icon-12"></i>
       Behöver ändras
      </span>
      <?php else: ?>
      <span class="badge badge-success">
       <i data-lucide="check" class="gs-icon-12"></i>
       OK
      </span>
      <?php endif; ?>
     </td>
     </tr>
    <?php endforeach; ?>
    </tbody>
   </table>
   </div>
  </div>
  </div>
 <?php endif; ?>
 </div>
</main>

<?php include __DIR__ . '/../includes/layout-footer.php'; ?>
