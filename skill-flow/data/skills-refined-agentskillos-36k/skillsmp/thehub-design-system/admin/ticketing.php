<?php
/**
 * Ticketing Dashboard
 * Main hub for managing event ticketing, pricing, and sales
 */

require_once __DIR__ . '/../config.php';
require_admin();

$db = getDB();

// Get upcoming events with basic info
$events = $db->getAll("
 SELECT
 e.id,
 e.name,
 e.date,
 e.location
 FROM events e
 WHERE e.date >= DATE_SUB(CURDATE(), INTERVAL 30 DAY)
 ORDER BY e.date ASC
");

// Separate upcoming and past events
$upcomingEvents = [];
$pastEvents = [];
$today = date('Y-m-d');

foreach ($events as $event) {
 if ($event['date'] >= $today) {
 $upcomingEvents[] = $event;
 } else {
 $pastEvents[] = $event;
 }
}

$page_title = 'Biljetter';
include __DIR__ . '/components/unified-layout.php';
?>

<div class="alert alert--info mb-lg">
 <i data-lucide="info"></i>
 <strong>Info:</strong> Ticketing-funktioner kräver att databasmigreringarna körs för att aktivera kolumner som ticketing_enabled, woo_product_id, etc.
 </div>

 <!-- Upcoming Events -->
 <div class="card mb-lg">
 <div class="card-header">
 <h2 class="">
  <i data-lucide="calendar"></i>
  Kommande events (<?= count($upcomingEvents) ?>)
 </h2>
 </div>
 <div class="card-body">
 <?php if (empty($upcomingEvents)): ?>
  <p class="text-secondary">Inga kommande events</p>
 <?php else: ?>
  <div class="table-scrollable">
  <table class="table">
  <thead>
  <tr>
   <th>Event</th>
   <th class="col-landscape">Datum</th>
   <th class="col-tablet">Plats</th>
   <th class="gs-actions-col">Åtgärder</th>
  </tr>
  </thead>
  <tbody>
  <?php foreach ($upcomingEvents as $event): ?>
   <tr>
   <td><strong><?= htmlspecialchars($event['name']) ?></strong></td>
   <td class="col-landscape"><?= date('d M Y', strtotime($event['date'])) ?></td>
   <td class="col-tablet"><?= htmlspecialchars($event['location'] ?? '-') ?></td>
   <td class="gs-actions-col">
   <a href="/admin/event-ticketing.php?id=<?= $event['id'] ?>" class="btn btn--sm btn--primary">
   <i data-lucide="settings"></i>
   <span class="col-landscape">Konfigurera</span>
   </a>
   </td>
   </tr>
  <?php endforeach; ?>
  </tbody>
  </table>
  </div>
 <?php endif; ?>
 </div>
 </div>

 <!-- Past Events -->
 <?php if (!empty($pastEvents)): ?>
 <div class="card">
 <div class="card-header">
 <h2 class="text-secondary">
  <i data-lucide="history"></i>
  Tidigare events (<?= count($pastEvents) ?>)
 </h2>
 </div>
 <div class="card-body">
 <div class="table-scrollable">
  <table class="table">
  <thead>
  <tr>
  <th>Event</th>
  <th class="col-landscape">Datum</th>
  <th class="col-tablet">Plats</th>
  </tr>
  </thead>
  <tbody>
  <?php foreach ($pastEvents as $event): ?>
  <tr>
   <td><?= htmlspecialchars($event['name']) ?></td>
   <td class="col-landscape"><?= date('d M Y', strtotime($event['date'])) ?></td>
   <td class="col-tablet"><?= htmlspecialchars($event['location'] ?? '-') ?></td>
  </tr>
  <?php endforeach; ?>
  </tbody>
  </table>
 </div>
 </div>
 </div>
 <?php endif; ?>

<?php include __DIR__ . '/components/unified-layout-footer.php'; ?>
