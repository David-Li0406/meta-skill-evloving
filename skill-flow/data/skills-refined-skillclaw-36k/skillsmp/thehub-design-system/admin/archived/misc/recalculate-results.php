<?php
require_once __DIR__ . '/../config.php';
require_once __DIR__ . '/../includes/point-calculations.php';
require_admin();

$db = getDB();
$message = '';
$messageType = 'info';

// Handle recalculate request
if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['event_id'])) {
 checkCsrf();

 $eventId = (int)$_POST['event_id'];
 $newScaleId = !empty($_POST['point_scale_id']) ? (int)$_POST['point_scale_id'] : null;
 $useSweCupDH = isset($_POST['use_swecup_dh']) && $_POST['use_swecup_dh'] === '1';

 // Get event info
 $event = $db->getRow("SELECT name FROM events WHERE id = ?", [$eventId]);

 if (!$event) {
 $message = 'Event hittades inte';
 $messageType = 'error';
 } else {
 // Get event format to determine calculation method
 $eventFormatRow = $db->getRow("SELECT event_format FROM events WHERE id = ?", [$eventId]);
 $eventFormat = $eventFormatRow['event_format'] ?? 'ENDURO';

 // Recalculate based on event format
 $isDHEvent = in_array($eventFormat, ['DH_STANDARD', 'DH_SWECUP']);

 if ($isDHEvent) {
 // For DH events, use SweCUP format if specified OR if checkbox is checked
 $useSweCupFormat = ($eventFormat === 'DH_SWECUP') || $useSweCupDH;
 $stats = recalculateDHEventResults($db, $eventId, $newScaleId, $useSweCupFormat);
 $eventType = $useSweCupFormat ? 'DH (SweCUP-format)' : 'DH (standard)';
 } else {
 $stats = recalculateEventResults($db, $eventId, $newScaleId);
 $eventType = ucfirst(strtolower($eventFormat));
 }

 $classesFixed = $stats['classes_fixed'] ?? 0;
 $classesMsg = $classesFixed > 0 ?", {$classesFixed} klassplaceringar korrigerade" :"";

 if (!empty($stats['errors'])) {
 $message ="Omräkning klar med fel ({$eventType}): {$stats['positions_updated']} placeringar uppdaterade, {$stats['points_updated']} poäng uppdaterade{$classesMsg}." . count($stats['errors']) ." fel uppstod.";
 $messageType = 'warning';
 } else {
 $message ="Omräkning klar ({$eventType})! {$stats['positions_updated']} placeringar och {$stats['points_updated']} poäng uppdaterade{$classesMsg} för '{$event['name']}'.";
 $messageType = 'success';
 }
 }

 // Redirect back with message
 $_SESSION['recalc_message'] = $message;
 $_SESSION['recalc_type'] = $messageType;
 header('Location: /admin/results.php');
 exit;
}

// Get event ID from query string
$eventId = isset($_GET['event_id']) ? (int)$_GET['event_id'] : 0;

if (!$eventId) {
 header('Location: /admin/results.php');
 exit;
}

// Get event details
$event = $db->getRow("
 SELECT e.*,
 COUNT(r.id) as result_count,
 ps.name as current_scale_name
 FROM events e
 LEFT JOIN results r ON e.id = r.event_id
 LEFT JOIN point_scales ps ON e.point_scale_id = ps.id
 WHERE e.id = ?
 GROUP BY e.id
", [$eventId]);

if (!$event) {
 header('Location: /admin/results.php');
 exit;
}

// Check event format
$eventFormat = $event['event_format'] ?? 'ENDURO';
$isDHEvent = in_array($eventFormat, ['DH_STANDARD', 'DH_SWECUP']);

// Get all point scales
$pointScales = getPointScales($db, null, true);

$pageTitle = 'Räkna om resultat - ' . $event['name'];
$pageType = 'admin';
include __DIR__ . '/../includes/layout-header.php';
?>

<main class="main-content">
 <div class="container container-max-800-center">
 <div class="card">
 <div class="card-header">
 <div class="flex justify-between items-center">
  <h1 class="text-primary">
  <i data-lucide="refresh-cw"></i>
  Räkna om resultat
  </h1>
  <a href="/admin/results.php" class="btn btn--secondary btn--sm">
  <i data-lucide="arrow-left"></i>
  Tillbaka
  </a>
 </div>
 </div>

 <div class="card-body">
 <!-- Event Info -->
 <div class="mb-lg gs-bg-info-box">
  <h2 class="mb-sm"><?= h($event['name']) ?></h2>
  <div class="flex gap-md text-sm text-secondary">
  <span>
  <i data-lucide="calendar" class="icon-sm"></i>
  <?= date('Y-m-d', strtotime($event['date'])) ?>
  </span>
  <span>
  <i data-lucide="users" class="icon-sm"></i>
  <?= $event['result_count'] ?> resultat
  </span>
  <?php if ($event['current_scale_name']): ?>
  <span>
  <i data-lucide="award" class="icon-sm"></i>
  <?= h($event['current_scale_name']) ?>
  </span>
  <?php endif; ?>
  </div>
 </div>

 <!-- Warning Alert -->
 <?php if ($isDHEvent): ?>
  <div class="alert alert--info mb-md">
  <i data-lucide="info"></i>
  <strong>DH-resultat detekterat!</strong> Detta event innehåller DH två-åk resultat.
  </div>
 <?php endif; ?>

 <div class="alert alert--warning mb-lg">
  <i data-lucide="alert-triangle"></i>
  <strong>Varning!</strong> Detta kommer att:
  <ul class="gs-margin-list">
  <li><strong>Korrigera klassplaceringar</strong> baserat på deltagarens kön och födelseår</li>
  <?php if ($isDHEvent): ?>
  <li>Räkna om placeringar för varje åk separat</li>
  <li>Räkna om total placering baserat på snabbaste åket</li>
  <li>Räkna om poäng (standard DH: snabbaste räknas, SweCUP DH: båda räknas)</li>
  <?php else: ?>
  <li>Räkna om alla placeringar inom varje klass baserat på tid</li>
  <li>Räkna om alla poäng baserat på nya placeringar</li>
  <?php endif; ?>
  <li>Kan ändra poängmall om du väljer en annan nedan</li>
  </ul>
 </div>

 <!-- Recalculate Form -->
 <form method="POST">
  <?= csrf_field() ?>
  <input type="hidden" name="event_id" value="<?= $eventId ?>">

  <div class="form-group">
  <label class="label">
  <i data-lucide="target"></i>
  Poängmall (valfritt)
  </label>
  <select name="point_scale_id" class="input">
  <option value="">Behåll nuvarande (<?= h($event['current_scale_name'] ?: 'Ingen') ?>)</option>
  <?php foreach ($pointScales as $scale): ?>
  <option value="<?= $scale['id'] ?>" <?= $event['point_scale_id'] == $scale['id'] ? 'selected' : '' ?>>
   <?= h($scale['name']) ?>
   <?php if ($scale['discipline'] !== 'ALL'): ?>
   (<?= h($scale['discipline']) ?>)
   <?php endif; ?>
   <?php if ($scale['is_default']): ?>
   ⭐ Standard
   <?php endif; ?>
  </option>
  <?php endforeach; ?>
  </select>
  <small class="text-sm text-secondary">
  Välj en poängmall om du vill ändra från nuvarande. Lämna tom för att behålla nuvarande mall.
  </small>
  </div>

  <?php if ($isDHEvent): ?>
  <div class="form-group">
  <label class="checkbox-label">
  <input type="checkbox" name="use_swecup_dh" value="1" class="checkbox">
  <span>
   <strong>SweCUP DH-format</strong>
   <span class="text-sm text-secondary gs-block-mt-qtr">
   Båda åken ger poäng separat (run_1_points + run_2_points).
   Lämna avmarkerad för standard DH där endast snabbaste åket räknas.
   </span>
  </span>
  </label>
  </div>
  <?php endif; ?>

  <div class="flex gs-justify-end gap-md mt-lg">
  <a href="/admin/results.php" class="btn btn--secondary">
  <i data-lucide="x"></i>
  Avbryt
  </a>
  <button type="submit" class="btn btn--primary btn-lg"
  onclick="return confirm('Är du säker på att du vill räkna om alla resultat för detta event?\n\nDetta kan inte ångras.');">
  <i data-lucide="refresh-cw"></i>
  Räkna om resultat
  </button>
  </div>
 </form>
 </div>
 </div>
 </div>
</main>

<script src="https://unpkg.com/lucide@latest"></script>
<script>
 lucide.createIcons();
</script>

<?php include __DIR__ . '/../includes/layout-footer.php'; ?>
