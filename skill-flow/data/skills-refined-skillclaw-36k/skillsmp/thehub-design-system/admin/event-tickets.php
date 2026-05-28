<?php
/**
 * Admin Event Tickets Management
 * Generate and manage tickets for events
 */

require_once __DIR__ . '/../config.php';
require_admin();

$db = getDB();

// Get event ID
$eventId = isset($_GET['id']) ? intval($_GET['id']) : 0;

if ($eventId <= 0) {
 $_SESSION['message'] = 'Ogiltigt event-ID';
 $_SESSION['messageType'] = 'error';
 header('Location: /admin/events.php');
 exit;
}

// Fetch event data
$event = $db->getRow("SELECT * FROM events WHERE id = ?", [$eventId]);

if (!$event) {
 $_SESSION['message'] = 'Event hittades inte';
 $_SESSION['messageType'] = 'error';
 header('Location: /admin/events.php');
 exit;
}

// Initialize message variables
$message = '';
$messageType = 'info';

// Handle form submission
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
 checkCsrf();

 $action = $_POST['action'] ?? '';

 if ($action === 'generate_tickets') {
 $classId = intval($_POST['class_id'] ?? 0);
 $quantity = intval($_POST['quantity'] ?? 0);

 if ($classId <= 0 || $quantity <= 0) {
  $message = 'Välj klass och ange antal biljetter';
  $messageType = 'error';
 } else {
  // Generate tickets
  $existingCount = $db->getValue("
  SELECT COUNT(*) FROM event_tickets
  WHERE event_id = ? AND class_id = ?
 ", [$eventId, $classId]);

  $inserted = 0;
  $wooProductId = $event['woo_product_id'] ?? null;

  for ($i = 1; $i <= $quantity; $i++) {
  $ticketNum = $existingCount + $i;
  $ticketNumber = sprintf('E%d-C%d-%05d', $eventId, $classId, $ticketNum);

  $result = $db->execute("
   INSERT INTO event_tickets
   (event_id, ticket_number, class_id, status, woo_product_id, created_at)
   VALUES (?, ?, ?, 'available', ?, NOW())
  ", [$eventId, $ticketNumber, $classId, $wooProductId]);

  if ($result) {
   $inserted++;
  }
  }

  $message ="Skapade $inserted biljetter";
  $messageType = 'success';
 }
 } elseif ($action === 'delete_available') {
 // Delete all available tickets for a class
 $classId = intval($_POST['class_id'] ?? 0);

 if ($classId > 0) {
  $deleted = $db->execute("
  DELETE FROM event_tickets
  WHERE event_id = ? AND class_id = ? AND status = 'available'
 ", [$eventId, $classId]);

  $message = 'Raderade tillgängliga biljetter';
  $messageType = 'success';
 }
 }
}

// Fetch classes with pricing
$classes = $db->getAll("
 SELECT
 c.id,
 c.name,
 c.display_name,
 c.sort_order,
 epr.base_price
 FROM classes c
 LEFT JOIN event_pricing_rules epr ON c.id = epr.class_id AND epr.event_id = ?
 ORDER BY c.sort_order ASC
", [$eventId]);

// Fetch ticket statistics per class
$ticketStats = $db->getAll("
 SELECT
 class_id,
 COUNT(*) as total,
 SUM(CASE WHEN status = 'available' THEN 1 ELSE 0 END) as available,
 SUM(CASE WHEN status = 'sold' THEN 1 ELSE 0 END) as sold,
 SUM(CASE WHEN status = 'refunded' THEN 1 ELSE 0 END) as refunded
 FROM event_tickets
 WHERE event_id = ?
 GROUP BY class_id
", [$eventId]);

// Create stats map
$statsMap = [];
foreach ($ticketStats as $stat) {
 $statsMap[$stat['class_id']] = $stat;
}

// Total stats
$totalStats = $db->getRow("
 SELECT
 COUNT(*) as total,
 SUM(CASE WHEN status = 'available' THEN 1 ELSE 0 END) as available,
 SUM(CASE WHEN status = 'sold' THEN 1 ELSE 0 END) as sold,
 SUM(CASE WHEN status = 'refunded' THEN 1 ELSE 0 END) as refunded
 FROM event_tickets
 WHERE event_id = ?
", [$eventId]);

$pageTitle = 'Biljetter - ' . $event['name'];
$pageType = 'admin';
include __DIR__ . '/../includes/layout-header.php';
?>

<main class="main-content">
 <div class="container">
 <!-- Header -->
 <div class="card mb-lg">
  <div class="card-body">
  <div class="mb-md">
   <a href="/admin/event-pricing.php?id=<?= $eventId ?>" class="btn btn--secondary btn--sm">
   <i data-lucide="arrow-left" class="icon-md"></i>
   Tillbaka till prissättning
   </a>
  </div>

  <h1 class="text-primary mb-sm">
   <i data-lucide="ticket" class="icon-lg"></i>
   Biljetthantering
  </h1>
  <p class="text-secondary">
   <strong><?= h($event['name']) ?></strong> - <?= date('d M Y', strtotime($event['date'])) ?>
  </p>
  </div>
 </div>

 <?php if ($message): ?>
  <div class="alert alert-<?= $messageType ?> mb-lg">
  <?= h($message) ?>
  </div>
 <?php endif; ?>

 <!-- Total Statistics -->
 <div class="card mb-lg">
  <div class="card-header">
  <h2 class="text-primary">
   <i data-lucide="bar-chart-2" class="icon-md"></i>
   Total statistik
  </h2>
  </div>
  <div class="card-body">
  <div class="grid grid-cols-2 gs-md-grid-cols-4 gap-md">
   <div class="stat-card">
   <div class="stat-value"><?= $totalStats['total'] ?? 0 ?></div>
   <div class="stat-label">Totalt skapade</div>
   </div>
   <div class="stat-card">
   <div class="stat-value text-success"><?= $totalStats['available'] ?? 0 ?></div>
   <div class="stat-label">Tillgängliga</div>
   </div>
   <div class="stat-card">
   <div class="stat-value text-primary"><?= $totalStats['sold'] ?? 0 ?></div>
   <div class="stat-label">Sålda</div>
   </div>
   <div class="stat-card">
   <div class="stat-value text-warning"><?= $totalStats['refunded'] ?? 0 ?></div>
   <div class="stat-label">Återbetalade</div>
   </div>
  </div>
  </div>
 </div>

 <!-- Generate Tickets -->
 <div class="card mb-lg">
  <div class="card-header">
  <h2 class="text-primary">
   <i data-lucide="plus-circle" class="icon-md"></i>
   Generera biljetter
  </h2>
  </div>
  <div class="card-body">
  <form method="POST" class="flex gap-md gs-items-end flex-wrap">
   <?= csrfField() ?>
   <input type="hidden" name="action" value="generate_tickets">

   <div class="form-group">
   <label class="label">Klass</label>
   <select name="class_id" class="gs-select" required>
    <option value="">Välj klass...</option>
    <?php foreach ($classes as $class): ?>
    <?php if ($class['base_price'] > 0): ?>
     <option value="<?= $class['id'] ?>">
     <?= h($class['display_name']) ?> (<?= $class['base_price'] ?> kr)
     </option>
    <?php endif; ?>
    <?php endforeach; ?>
   </select>
   </div>

   <div class="form-group">
   <label class="label">Antal biljetter</label>
   <input type="number"
    name="quantity"
    class="input"
    value="50"
    min="1"
    max="1000"
    required
    style="width: 100px;">
   </div>

   <button type="submit" class="btn btn--primary">
   <i data-lucide="plus" class="icon-sm"></i>
   Generera
   </button>
  </form>
  </div>
 </div>

 <!-- Tickets per Class -->
 <div class="card">
  <div class="card-header">
  <h2 class="text-primary">
   <i data-lucide="layers" class="icon-md"></i>
   Biljetter per klass
  </h2>
  </div>
  <div class="card-body">
  <div class="table-responsive">
   <table class="table">
   <thead>
    <tr>
    <th>Klass</th>
    <th>Pris</th>
    <th class="table-center">Totalt</th>
    <th class="table-center">Tillgängliga</th>
    <th class="table-center">Sålda</th>
    <th>Fyllning</th>
    <th>Åtgärder</th>
    </tr>
   </thead>
   <tbody>
    <?php foreach ($classes as $class): ?>
    <?php
    $stats = $statsMap[$class['id']] ?? null;
    $total = $stats['total'] ?? 0;
    $available = $stats['available'] ?? 0;
    $sold = $stats['sold'] ?? 0;
    $fillPercent = $total > 0 ? round(($sold / $total) * 100) : 0;
    ?>
    <tr>
     <td>
     <strong><?= h($class['display_name']) ?></strong>
     </td>
     <td>
     <?php if ($class['base_price'] > 0): ?>
      <?= number_format($class['base_price'], 0) ?> kr
     <?php else: ?>
      <span class="text-secondary">Ej satt</span>
     <?php endif; ?>
     </td>
     <td class="table-center"><?= $total ?></td>
     <td class="table-center">
     <?php if ($available > 0): ?>
      <span class="badge badge-success"><?= $available ?></span>
     <?php else: ?>
      <span class="text-secondary">0</span>
     <?php endif; ?>
     </td>
     <td class="table-center">
     <?php if ($sold > 0): ?>
      <span class="badge badge-primary"><?= $sold ?></span>
     <?php else: ?>
      <span class="text-secondary">0</span>
     <?php endif; ?>
     </td>
     <td>
     <?php if ($total > 0): ?>
      <div style="width: 100px; height: 8px; background: var(--gs-bg-tertiary); border-radius: 4px; overflow: hidden;">
      <div style="width: <?= $fillPercent ?>%; height: 100%; background: var(--primary);"></div>
      </div>
      <span class="text-xs text-secondary"><?= $fillPercent ?>%</span>
     <?php else: ?>
      <span class="text-secondary text-sm">-</span>
     <?php endif; ?>
     </td>
     <td>
     <?php if ($available > 0): ?>
      <form method="POST" style="display: inline;"
       onsubmit="return confirm('Radera <?= $available ?> tillgängliga biljetter?');">
      <?= csrfField() ?>
      <input type="hidden" name="action" value="delete_available">
      <input type="hidden" name="class_id" value="<?= $class['id'] ?>">
      <button type="submit" class="btn btn-error btn--sm">
       <i data-lucide="trash-2" class="gs-icon-xs"></i>
      </button>
      </form>
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
