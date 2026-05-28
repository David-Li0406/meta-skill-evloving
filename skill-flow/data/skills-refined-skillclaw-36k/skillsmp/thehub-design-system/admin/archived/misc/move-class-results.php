<?php
/**
 * Admin tool to move results from one class to another
 * Useful when a class was created incorrectly during import
 */
require_once __DIR__ . '/../config.php';
require_admin();

$db = getDB();
$message = '';
$messageType = 'info';

// Check for message from redirect
if (isset($_SESSION['move_message'])) {
 $message = $_SESSION['move_message'];
 $messageType = $_SESSION['move_message_type'] ?? 'info';
 unset($_SESSION['move_message'], $_SESSION['move_message_type']);
}

// Handle move action
if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['move_results'])) {
 checkCsrf();

 $fromClassId = (int)$_POST['from_class_id'];
 $toClassId = (int)$_POST['to_class_id'];
 $eventId = !empty($_POST['event_id']) ? (int)$_POST['event_id'] : null;

 if ($fromClassId && $toClassId && $fromClassId !== $toClassId) {
 try {
  $db->pdo->beginTransaction();

  // Build the update query
  $params = [$toClassId, $fromClassId];
  $whereClause ="class_id = ?";

  if ($eventId) {
  $whereClause .=" AND event_id = ?";
  $params[] = $eventId;
  }

  // Get count before moving
  $countParams = [$fromClassId];
  $countWhere ="class_id = ?";
  if ($eventId) {
  $countWhere .=" AND event_id = ?";
  $countParams[] = $eventId;
  }
  $count = $db->getRow("SELECT COUNT(*) as c FROM results WHERE $countWhere", $countParams)['c'];

  // Move results
  $db->query("UPDATE results SET class_id = ? WHERE $whereClause", $params);

  // Get class names for message
  $fromClass = $db->getRow("SELECT display_name FROM classes WHERE id = ?", [$fromClassId]);
  $toClass = $db->getRow("SELECT display_name FROM classes WHERE id = ?", [$toClassId]);

  $db->pdo->commit();

  $eventText = $eventId ?" (för valt event)" :"";
  $_SESSION['move_message'] ="Flyttade $count resultat från" . ($fromClass['display_name'] ??"Klass $fromClassId") .
  " till" . ($toClass['display_name'] ??"Klass $toClassId") . $eventText;
  $_SESSION['move_message_type'] = 'success';

 } catch (Exception $e) {
  if ($db->pdo->inTransaction()) {
  $db->pdo->rollBack();
  }
  $_SESSION['move_message'] ="Fel vid flytt:" . $e->getMessage();
  $_SESSION['move_message_type'] = 'error';
 }
 } else {
 $_SESSION['move_message'] ="Välj två olika klasser (from: $fromClassId, to: $toClassId)";
 $_SESSION['move_message_type'] = 'error';
 }

 header('Location: /admin/move-class-results.php');
 exit;
}

// Handle delete class action
if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['delete_class'])) {
 checkCsrf();

 $classId = (int)$_POST['class_id'];

 if ($classId) {
 try {
  // Check if class has results
  $resultCount = $db->getRow("SELECT COUNT(*) as c FROM results WHERE class_id = ?", [$classId])['c'];

  if ($resultCount > 0) {
  $_SESSION['move_message'] ="Kan inte ta bort klass med $resultCount resultat. Flytta resultaten först.";
  $_SESSION['move_message_type'] = 'error';
  } else {
  $className = $db->getRow("SELECT display_name FROM classes WHERE id = ?", [$classId]);
  $db->query("DELETE FROM classes WHERE id = ?", [$classId]);
  $_SESSION['move_message'] ="Tog bort klass:" . ($className['display_name'] ??"ID $classId");
  $_SESSION['move_message_type'] = 'success';
  }
 } catch (Exception $e) {
  $_SESSION['move_message'] ="Fel vid borttagning:" . $e->getMessage();
  $_SESSION['move_message_type'] = 'error';
 }
 }

 header('Location: /admin/move-class-results.php');
 exit;
}

// Get all classes with result counts
$classes = $db->getAll("
 SELECT c.id, c.name, c.display_name, c.sort_order,
  COUNT(r.id) as result_count
 FROM classes c
 LEFT JOIN results r ON c.id = r.class_id
 GROUP BY c.id
 ORDER BY c.sort_order, c.display_name
");

// Get all events for filtering
$events = $db->getAll("
 SELECT id, name, date
 FROM events
 ORDER BY date DESC
 LIMIT 100
");

$pageTitle = 'Flytta klassresultat';
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
  <i data-lucide="move"></i>
  Flytta klassresultat
 </h1>

 <?php if ($message): ?>
  <div class="alert alert-<?= $messageType ?> mb-lg">
  <i data-lucide="<?= $messageType === 'success' ? 'check-circle' : 'alert-circle' ?>"></i>
  <?= h($message) ?>
  </div>
 <?php endif; ?>

 <!-- Move Results Form -->
 <div class="card mb-lg">
  <div class="card-header">
  <h2 class="text-primary">
   <i data-lucide="arrow-right-left"></i>
   Flytta resultat mellan klasser
  </h2>
  </div>
  <div class="card-body">
  <form method="POST">
   <?= csrf_field() ?>
   <div class="grid grid-cols-1 md-grid-cols-3 gap-md">
   <div class="form-group">
    <label class="label">Från klass *</label>
    <select name="from_class_id" class="input" required>
    <option value="">Välj klass...</option>
    <?php foreach ($classes as $class): ?>
     <option value="<?= $class['id'] ?>">
     <?= h($class['display_name']) ?> (<?= $class['result_count'] ?> resultat)
     </option>
    <?php endforeach; ?>
    </select>
   </div>
   <div class="form-group">
    <label class="label">Till klass *</label>
    <select name="to_class_id" class="input" required>
    <option value="">Välj klass...</option>
    <?php foreach ($classes as $class): ?>
     <option value="<?= $class['id'] ?>">
     <?= h($class['display_name']) ?> (<?= $class['result_count'] ?> resultat)
     </option>
    <?php endforeach; ?>
    </select>
   </div>
   <div class="form-group">
    <label class="label">Begränsa till event (valfritt)</label>
    <select name="event_id" class="input">
    <option value="">Alla event</option>
    <?php foreach ($events as $event): ?>
     <option value="<?= $event['id'] ?>">
     <?= h($event['name']) ?> (<?= date('Y-m-d', strtotime($event['date'])) ?>)
     </option>
    <?php endforeach; ?>
    </select>
   </div>
   </div>
   <div class="mt-md">
   <button type="submit" name="move_results" class="btn btn-warning"
    onclick="return confirm('Flytta alla resultat från vald klass till den nya klassen?');">
    <i data-lucide="move"></i>
    Flytta resultat
   </button>
   </div>
  </form>
  </div>
 </div>

 <!-- Classes List -->
 <div class="card">
  <div class="card-header">
  <h2 class="text-primary">
   <i data-lucide="layers"></i>
   Alla klasser (<?= count($classes) ?>)
  </h2>
  </div>
  <div class="card-body gs-p-0">
  <div class="table-responsive">
   <table class="table">
   <thead>
    <tr>
    <th>ID</th>
    <th>Visningsnamn</th>
    <th>Namn</th>
    <th>Resultat</th>
    <th>Sort</th>
    <th>Åtgärd</th>
    </tr>
   </thead>
   <tbody>
    <?php foreach ($classes as $class): ?>
    <tr>
     <td><?= $class['id'] ?></td>
     <td><strong><?= h($class['display_name']) ?></strong></td>
     <td><?= h($class['name']) ?></td>
     <td>
     <span class="badge <?= $class['result_count'] > 0 ? 'badge-primary' : 'badge-secondary' ?>">
      <?= $class['result_count'] ?>
     </span>
     </td>
     <td><?= $class['sort_order'] ?></td>
     <td>
     <?php if ($class['result_count'] == 0): ?>
      <form method="POST" style="display: inline;"
       onsubmit="return confirm('Ta bort denna klass?');">
      <?= csrf_field() ?>
      <input type="hidden" name="class_id" value="<?= $class['id'] ?>">
      <button type="submit" name="delete_class" class="btn btn--sm btn-danger">
       <i data-lucide="trash-2"></i>
       Ta bort
      </button>
      </form>
     <?php else: ?>
      <span class="text-xs text-secondary">Har resultat</span>
     <?php endif; ?>
     </td>
    </tr>
    <?php endforeach; ?>
   </tbody>
   </table>
  </div>
  </div>
 </div>
 </div>
</main>

<?php include __DIR__ . '/../includes/layout-footer.php'; ?>
