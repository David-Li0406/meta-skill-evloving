<?php
/**
 * Admin Refund Requests Management
 * Review and process ticket refund requests
 */

require_once __DIR__ . '/../config.php';
require_admin();

$db = getDB();

// Initialize message
$message = '';
$messageType = 'info';

// Handle actions
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
 checkCsrf();

 $action = $_POST['action'] ?? '';
 $requestId = intval($_POST['request_id'] ?? 0);

 if ($requestId > 0) {
 $request = $db->getRow("
 SELECT err.*, et.ticket_number, et.paid_price
 FROM event_refund_requests err
 JOIN event_tickets et ON err.ticket_id = et.id
 WHERE err.id = ?
", [$requestId]);

 if ($request) {
 if ($action === 'approve') {
 // Approve refund
 $db->execute("
  UPDATE event_refund_requests
  SET status = 'approved', processed_at = NOW(), admin_notes = ?
  WHERE id = ?
 ", [$_POST['admin_notes'] ?? '', $requestId]);

 // Update ticket status
 $db->execute("
  UPDATE event_tickets
  SET status = 'refunded'
  WHERE id = ?
 ", [$request['ticket_id']]);

 $message = 'Återbetalning godkänd för ' . $request['ticket_number'];
 $messageType = 'success';

 } elseif ($action === 'deny') {
 // Deny refund
 $db->execute("
  UPDATE event_refund_requests
  SET status = 'denied', processed_at = NOW(), admin_notes = ?
  WHERE id = ?
 ", [$_POST['admin_notes'] ?? '', $requestId]);

 $message = 'Återbetalning nekad för ' . $request['ticket_number'];
 $messageType = 'warning';
 }
 }
 }
}

// Fetch pending requests
$pendingRequests = $db->getAll("
 SELECT
 err.*,
 et.ticket_number,
 et.paid_price,
 e.name as event_name,
 e.date as event_date,
 r.firstname,
 r.lastname,
 r.email as rider_email
 FROM event_refund_requests err
 JOIN event_tickets et ON err.ticket_id = et.id
 JOIN events e ON et.event_id = e.id
 JOIN riders r ON err.rider_id = r.id
 WHERE err.status = 'pending'
 ORDER BY err.created_at ASC
");

// Fetch processed requests (last 50)
$processedRequests = $db->getAll("
 SELECT
 err.*,
 et.ticket_number,
 et.paid_price,
 e.name as event_name,
 r.firstname,
 r.lastname
 FROM event_refund_requests err
 JOIN event_tickets et ON err.ticket_id = et.id
 JOIN events e ON et.event_id = e.id
 JOIN riders r ON err.rider_id = r.id
 WHERE err.status IN ('approved', 'denied')
 ORDER BY err.processed_at DESC
 LIMIT 50
");

$pageTitle = 'Återbetalningar';
$pageType = 'admin';
include __DIR__ . '/../includes/layout-header.php';
?>

<main class="main-content">
 <div class="container">
 <!-- Header -->
 <div class="card mb-lg">
 <div class="card-body">
 <h1 class="text-primary mb-sm">
  <i data-lucide="rotate-ccw" class="icon-lg"></i>
  Återbetalningar
 </h1>
 <p class="text-secondary">
  Hantera återbetalningsbegäran från deltagare
 </p>
 </div>
 </div>

 <?php if ($message): ?>
 <div class="alert alert-<?= $messageType ?> mb-lg">
 <?= h($message) ?>
 </div>
 <?php endif; ?>

 <!-- Pending Requests -->
 <div class="card mb-lg">
 <div class="card-header">
 <h2 class="text-primary">
  <i data-lucide="clock" class="icon-md"></i>
  Väntande begäran
  <?php if (count($pendingRequests) > 0): ?>
  <span class="badge badge-warning ml-sm"><?= count($pendingRequests) ?></span>
  <?php endif; ?>
 </h2>
 </div>
 <div class="card-body">
 <?php if (empty($pendingRequests)): ?>
  <div class="text-secondary text-center py-lg">
  <i data-lucide="check-circle" class="gs-icon-xl text-success"></i>
  <p class="mt-md">Inga väntande begäran</p>
  </div>
 <?php else: ?>
  <div class="table-responsive">
  <table class="table">
  <thead>
  <tr>
   <th>Datum</th>
   <th>Deltagare</th>
   <th>Event</th>
   <th>Biljett</th>
   <th>Belopp</th>
   <th>Anledning</th>
   <th>Åtgärder</th>
  </tr>
  </thead>
  <tbody>
  <?php foreach ($pendingRequests as $request): ?>
   <?php
   $eventDate = new DateTime($request['event_date']);
   $daysUntilEvent = (new DateTime())->diff($eventDate)->days;
   $isPastEvent = $eventDate < new DateTime();
   ?>
   <tr>
   <td>
   <span class="text-sm">
   <?= date('d M', strtotime($request['created_at'])) ?>
   </span>
   </td>
   <td>
   <strong><?= h($request['firstname'] . ' ' . $request['lastname']) ?></strong>
   <br>
   <span class="text-xs text-secondary">
   <?= h($request['rider_email']) ?>
   </span>
   </td>
   <td>
   <?= h($request['event_name']) ?>
   <br>
   <span class="text-xs text-secondary">
   <?= date('d M Y', strtotime($request['event_date'])) ?>
   <?php if ($isPastEvent): ?>
    <span class="badge badge-error badge-sm">Passerat</span>
   <?php else: ?>
    (<?= $daysUntilEvent ?> dagar kvar)
   <?php endif; ?>
   </span>
   </td>
   <td>
   <code><?= h($request['ticket_number']) ?></code>
   </td>
   <td>
   <strong><?= number_format($request['refund_amount'], 0) ?> kr</strong>
   <br>
   <span class="text-xs text-secondary">
   av <?= number_format($request['paid_price'], 0) ?> kr
   </span>
   </td>
   <td>
   <?php if ($request['reason']): ?>
   <span class="text-sm" title="<?= h($request['reason']) ?>">
    <?= h(substr($request['reason'], 0, 50)) ?>
    <?= strlen($request['reason']) > 50 ? '...' : '' ?>
   </span>
   <?php else: ?>
   <span class="text-secondary text-sm">-</span>
   <?php endif; ?>
   </td>
   <td>
   <div class="flex gap-sm">
   <form method="POST" style="display: inline;">
    <?= csrfField() ?>
    <input type="hidden" name="action" value="approve">
    <input type="hidden" name="request_id" value="<?= $request['id'] ?>">
    <button type="submit"
    class="btn btn-success btn--sm"
    onclick="return confirm('Godkänna återbetalning på <?= $request['refund_amount'] ?> kr?')">
    <i data-lucide="check" class="gs-icon-xs"></i>
    </button>
   </form>
   <form method="POST" style="display: inline;">
    <?= csrfField() ?>
    <input type="hidden" name="action" value="deny">
    <input type="hidden" name="request_id" value="<?= $request['id'] ?>">
    <button type="submit"
    class="btn btn-error btn--sm"
    onclick="return confirm('Neka återbetalning?')">
    <i data-lucide="x" class="gs-icon-xs"></i>
    </button>
   </form>
   </div>
   </td>
   </tr>
  <?php endforeach; ?>
  </tbody>
  </table>
  </div>
 <?php endif; ?>
 </div>
 </div>

 <!-- Processed Requests -->
 <div class="card">
 <div class="card-header">
 <h2 class="text-secondary">
  <i data-lucide="history" class="icon-md"></i>
  Behandlade begäran
 </h2>
 </div>
 <div class="card-body">
 <?php if (empty($processedRequests)): ?>
  <p class="text-secondary">Inga behandlade begäran ännu.</p>
 <?php else: ?>
  <div class="table-responsive">
  <table class="table">
  <thead>
  <tr>
   <th>Datum</th>
   <th>Deltagare</th>
   <th>Event</th>
   <th>Belopp</th>
   <th>Status</th>
  </tr>
  </thead>
  <tbody>
  <?php foreach ($processedRequests as $request): ?>
   <tr>
   <td>
   <?= date('d M Y', strtotime($request['processed_at'])) ?>
   </td>
   <td>
   <?= h($request['firstname'] . ' ' . $request['lastname']) ?>
   </td>
   <td>
   <?= h($request['event_name']) ?>
   </td>
   <td>
   <?= number_format($request['refund_amount'], 0) ?> kr
   </td>
   <td>
   <?php if ($request['status'] === 'approved'): ?>
   <span class="badge badge-success">Godkänd</span>
   <?php else: ?>
   <span class="badge badge-error">Nekad</span>
   <?php endif; ?>
   </td>
   </tr>
  <?php endforeach; ?>
  </tbody>
  </table>
  </div>
 <?php endif; ?>
 </div>
 </div>
 </div>
</main>

<?php include __DIR__ . '/../includes/layout-footer.php'; ?>
