<?php
require_once __DIR__ . '/../config.php';
require_once __DIR__ . '/../includes/series-points.php'; // Series-specific points (separate from ranking)
require_admin();

$db = getDB();
$current_admin = get_current_admin();

// Get series ID
$seriesId = isset($_GET['series_id']) && is_numeric($_GET['series_id']) ? intval($_GET['series_id']) : null;

if (!$seriesId) {
 redirect('/admin/series.php');
}

// Get series info
$series = $db->getRow("SELECT * FROM series WHERE id = ?", [$seriesId]);

if (!$series) {
 redirect('/admin/series.php');
}

// AUTO-SYNC: Add events locked to this series (events.series_id) to series_events table
// This ensures events with series_id set always appear in the series
// Note: We don't filter by active - admin should see ALL events in the series
$lockedEvents = $db->getAll("
    SELECT e.id, e.date
    FROM events e
    WHERE e.series_id = ?
    AND e.id NOT IN (SELECT event_id FROM series_events WHERE series_id = ?)
", [$seriesId, $seriesId]);

foreach ($lockedEvents as $ev) {
    // Get sort order based on date (to maintain chronological order)
    $existingCount = $db->getRow("SELECT COUNT(*) as cnt FROM series_events WHERE series_id = ?", [$seriesId]);
    $db->insert('series_events', [
        'series_id' => $seriesId,
        'event_id' => $ev['id'],
        'template_id' => null,
        'sort_order' => ($existingCount['cnt'] ?? 0) + 1
    ]);
}

// Re-sort all events by date
if (!empty($lockedEvents)) {
    $allSeriesEvents = $db->getAll("
        SELECT se.id, e.date
        FROM series_events se
        JOIN events e ON se.event_id = e.id
        WHERE se.series_id = ?
        ORDER BY e.date ASC
    ", [$seriesId]);

    $sortOrder = 1;
    foreach ($allSeriesEvents as $se) {
        $db->update('series_events', ['sort_order' => $sortOrder], 'id = ?', [$se['id']]);
        $sortOrder++;
    }
}

$message = '';
$messageType = 'info';

// Handle form submissions
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
 checkCsrf();

 $action = $_POST['action'] ?? '';

 if ($action === 'add_event') {
 $eventId = intval($_POST['event_id']);
 $templateId = !empty($_POST['template_id']) ? intval($_POST['template_id']) : null;

 // Check if already exists
 $existing = $db->getRow(
"SELECT id FROM series_events WHERE series_id = ? AND event_id = ?",
 [$seriesId, $eventId]
 );

 if ($existing) {
 $message = 'Detta event finns redan i serien';
 $messageType = 'error';
 } else {
 // Get max sort order
 $maxOrder = $db->getRow(
 "SELECT MAX(sort_order) as max_order FROM series_events WHERE series_id = ?",
 [$seriesId]
 );
 $sortOrder = ($maxOrder['max_order'] ?? 0) + 1;

 $db->insert('series_events', [
 'series_id' => $seriesId,
 'event_id' => $eventId,
 'template_id' => $templateId,
 'sort_order' => $sortOrder
 ]);

 // Only set events.series_id if event doesn't already have a primary series
 // This allows events to be in multiple series without losing their main series
 $event = $db->getRow("SELECT series_id FROM events WHERE id = ?", [$eventId]);
 if (empty($event['series_id'])) {
 $db->update('events', ['series_id' => $seriesId], 'id = ?', [$eventId]);
 }

 // If a template was specified, calculate series points
 // NOTE: This only affects series_results, NOT results.points (ranking)
 if ($templateId) {
 $stats = recalculateSeriesEventPoints($db, $seriesId, $eventId);
 $message ="Event tillagt i serien! {$stats['inserted']} seriepoäng beräknade.";
 } else {
 $message = 'Event tillagt i serien! (ingen poängmall vald)';
 }
 $messageType = 'success';
 }
 } elseif ($action === 'update_template') {
 $seriesEventId = intval($_POST['series_event_id']);
 $templateId = !empty($_POST['template_id']) ? intval($_POST['template_id']) : null;

 // Get the event_id for this series_event
 $seriesEvent = $db->getRow(
"SELECT event_id FROM series_events WHERE id = ? AND series_id = ?",
 [$seriesEventId, $seriesId]
 );

 if ($seriesEvent) {
 $eventId = $seriesEvent['event_id'];

 // Update series_events template
 $db->update('series_events', [
 'template_id' => $templateId
 ], 'id = ? AND series_id = ?', [$seriesEventId, $seriesId]);

 // Recalculate series points using new template
 // NOTE: This only affects series_results, NOT results.points (ranking stays unchanged!)
 $stats = recalculateSeriesEventPoints($db, $seriesId, $eventId);

 $totalChanged = $stats['inserted'] + $stats['updated'];
 $message ="Poängmall uppdaterad! {$totalChanged} seriepoäng omräknade.";
 $messageType = 'success';
 } else {
 $message = 'Kunde inte hitta eventet';
 $messageType = 'error';
 }
 } elseif ($action === 'bulk_update_templates') {
 $seriesEventIds = $_POST['series_event_ids'] ?? [];
 $templateId = !empty($_POST['bulk_template_id']) ? intval($_POST['bulk_template_id']) : null;

 if (empty($seriesEventIds)) {
  $message = 'Inga event valda';
  $messageType = 'error';
 } else {
  $updatedCount = 0;
  $recalculatedCount = 0;

  foreach ($seriesEventIds as $seriesEventId) {
   $seriesEventId = intval($seriesEventId);

   // Get the event_id for this series_event
   $seriesEvent = $db->getRow(
    "SELECT event_id FROM series_events WHERE id = ? AND series_id = ?",
    [$seriesEventId, $seriesId]
   );

   if ($seriesEvent) {
    $eventId = $seriesEvent['event_id'];

    // Update series_events template
    $db->update('series_events', [
     'template_id' => $templateId
    ], 'id = ? AND series_id = ?', [$seriesEventId, $seriesId]);

    $updatedCount++;

    // Recalculate series points using new template
    if ($templateId) {
     $stats = recalculateSeriesEventPoints($db, $seriesId, $eventId);
     $recalculatedCount += $stats['inserted'] + $stats['updated'];
    }
   }
  }

  $message = "{$updatedCount} event uppdaterade! {$recalculatedCount} seriepoäng omräknade.";
  $messageType = 'success';
 }
 } elseif ($action === 'remove_event') {
 $seriesEventId = intval($_POST['series_event_id']);

 // Get event_id before deleting
 $seriesEvent = $db->getRow(
     "SELECT event_id FROM series_events WHERE id = ? AND series_id = ?",
     [$seriesEventId, $seriesId]
 );

 $db->delete('series_events', 'id = ? AND series_id = ?', [$seriesEventId, $seriesId]);

 // Also clear events.series_id if it points to this series
 if ($seriesEvent) {
     $db->query(
         "UPDATE events SET series_id = NULL WHERE id = ? AND series_id = ?",
         [$seriesEvent['event_id'], $seriesId]
     );
 }

 $message = 'Event borttaget från serien!';
 $messageType = 'success';
 } elseif ($action === 'update_order') {
 $orders = $_POST['orders'] ?? [];

 foreach ($orders as $seriesEventId => $sortOrder) {
 $db->update('series_events', [
 'sort_order' => intval($sortOrder)
 ], 'id = ? AND series_id = ?', [intval($seriesEventId), $seriesId]);
 }

 $message = 'Ordning uppdaterad!';
 $messageType = 'success';
 } elseif ($action === 'update_count_best') {
 $countBest = $_POST['count_best_results'];
 $countBestValue = ($countBest === '' || $countBest === 'null') ? null : intval($countBest);

 try {
 $db->update('series', [
 'count_best_results' => $countBestValue
 ], 'id = ?', [$seriesId]);

 // Refresh series data
 $series = $db->getRow("SELECT * FROM series WHERE id = ?", [$seriesId]);

 if ($countBestValue === null) {
 $message = 'Alla resultat räknas nu';
 } else {
 $message ="Räknar nu de {$countBestValue} bästa resultaten";
 }
 $messageType = 'success';
 } catch (Exception $e) {
 // Show actual error for debugging
 $message = 'Fel: ' . $e->getMessage() . ' - Kör migration 018_add_count_best_results.sql';
 $messageType = 'error';
 }
 } elseif ($action === 'recalculate_all') {
 // Recalculate all series points
 $totalStats = recalculateAllSeriesPoints($db, $seriesId);
 $totalChanged = $totalStats['inserted'] + $totalStats['updated'];
 $message = "Alla poäng omräknade! {$totalStats['events']} events, {$totalChanged} resultat uppdaterade.";
 $messageType = 'success';

} elseif ($action === 'move_up' || $action === 'move_down') {
 $seriesEventId = intval($_POST['series_event_id']);

 // Get current event and all events sorted
 $allEvents = $db->getAll("
 SELECT id, sort_order FROM series_events
 WHERE series_id = ?
 ORDER BY sort_order ASC
", [$seriesId]);

 // Find current position
 $currentIndex = -1;
 foreach ($allEvents as $index => $event) {
 if ($event['id'] == $seriesEventId) {
 $currentIndex = $index;
 break;
 }
 }

 if ($currentIndex >= 0) {
 $swapIndex = $action === 'move_up' ? $currentIndex - 1 : $currentIndex + 1;

 if ($swapIndex >= 0 && $swapIndex < count($allEvents)) {
 // Swap sort_order values
 $currentOrder = $allEvents[$currentIndex]['sort_order'];
 $swapOrder = $allEvents[$swapIndex]['sort_order'];

 $db->update('series_events', ['sort_order' => $swapOrder], 'id = ?', [$seriesEventId]);
 $db->update('series_events', ['sort_order' => $currentOrder], 'id = ?', [$allEvents[$swapIndex]['id']]);

 $message = 'Ordning uppdaterad!';
 $messageType = 'success';
 }
 }
 }
}

// Get events in this series - sorted by event date (chronological order)
// Events with series_id = this series are auto-synced and marked as "locked"
// Uses point_scales for templates (same as ranking system, but points stored separately in series_results)
$seriesEvents = $db->getAll("
 SELECT se.*, e.name as event_name, e.date as event_date, e.location, e.discipline,
 e.series_id as event_series_id,
 ps.name as template_name
 FROM series_events se
 JOIN events e ON se.event_id = e.id
 LEFT JOIN point_scales ps ON se.template_id = ps.id
 WHERE se.series_id = ?
 ORDER BY e.date ASC
", [$seriesId]);

// Get series year for matching
$seriesYear = $series['year'] ?? null;

// Get all events not in this series, with year matching indicator
$eventsNotInSeries = $db->getAll("
 SELECT e.id, e.name, e.date, e.location, e.discipline, YEAR(e.date) as event_year
 FROM events e
 WHERE e.id NOT IN (
 SELECT event_id FROM series_events WHERE series_id = ?
 )
 AND e.active = 1
 ORDER BY e.date DESC
", [$seriesId]);

// Separate events by year match for better UX
$matchingYearEvents = [];
$otherYearEvents = [];
foreach ($eventsNotInSeries as $ev) {
    if ($seriesYear && $ev['event_year'] == $seriesYear) {
        $matchingYearEvents[] = $ev;
    } else {
        $otherYearEvents[] = $ev;
    }
}

// Get all point scales (same templates used for both series and ranking)
$templates = $db->getAll("SELECT id, name FROM point_scales WHERE active = 1 ORDER BY name");

$pageTitle = 'Hantera Events - ' . $series['name'];
$pageType = 'admin';
include __DIR__ . '/components/unified-layout.php';
?>

<!-- Content starts here (unified-layout already opened <main>) -->
<style>
/* Mobile responsiveness for series-events page */
@media (max-width: 900px) {
    /* Header - stack vertically */
    .page-header-flex {
        flex-direction: column !important;
        align-items: stretch !important;
        gap: 16px !important;
    }

    .page-header-flex > .flex.gap-sm {
        flex-direction: column !important;
        width: 100% !important;
    }

    .page-header-flex .btn {
        width: 100% !important;
        justify-content: center !important;
        display: flex !important;
    }

    /* Grid - single column */
    .grid.gs-lg-grid-cols-3 {
        display: block !important;
    }

    .grid.gs-lg-grid-cols-3 > div {
        margin-bottom: 16px !important;
    }

    /* Cards full width */
    .card {
        width: 100% !important;
    }

    /* Bulk edit box */
    .alert.alert--info .flex.items-center {
        flex-direction: column !important;
        align-items: stretch !important;
        gap: 12px !important;
    }

    .alert.alert--info select,
    .alert.alert--info .input {
        width: 100% !important;
        min-width: unset !important;
    }

    .alert.alert--info .btn {
        width: 100% !important;
    }

    .alert.alert--info label {
        text-align: center;
    }

    /* Table wrapper - horizontal scroll */
    .table-responsive {
        overflow-x: auto !important;
        -webkit-overflow-scrolling: touch;
        margin-left: -16px !important;
        margin-right: -16px !important;
        padding-left: 16px !important;
        padding-right: 16px !important;
    }

    .table {
        min-width: 650px !important;
        font-size: 12px !important;
    }

    .table th,
    .table td {
        padding: 8px 6px !important;
        white-space: nowrap !important;
    }

    /* Hide location column */
    .table th:nth-child(5),
    .table td:nth-child(5) {
        display: none !important;
    }

    /* Smaller buttons */
    .table .btn {
        padding: 4px 8px !important;
        font-size: 11px !important;
    }

    .table .btn i,
    .table .btn svg {
        width: 12px !important;
        height: 12px !important;
    }

    /* Template dropdown in table */
    .template-form {
        min-width: 120px !important;
    }

    .template-form select {
        min-width: 100px !important;
        font-size: 11px !important;
        padding: 4px !important;
    }

    /* Order column compact */
    .table td:nth-child(2) .flex {
        gap: 2px !important;
    }

    .table td:nth-child(2) .btn {
        padding: 2px 4px !important;
    }
}

@media (max-width: 480px) {
    .table {
        font-size: 10px !important;
    }

    .table th,
    .table td {
        padding: 6px 4px !important;
    }

    .badge {
        font-size: 9px !important;
        padding: 2px 4px !important;
    }

    /* Hide date column too */
    .table th:nth-child(4),
    .table td:nth-child(4) {
        display: none !important;
    }

    .template-form select {
        min-width: 80px !important;
    }
}
</style>

<div class="container">
 <!-- Header -->
 <div class="flex items-center justify-between mb-lg page-header-flex">
 <div>
 <h1 class="">
  <i data-lucide="calendar"></i>
  <?= h($series['name']) ?>
 </h1>
 <p class="text-secondary">Hantera events och poängmallar</p>
 </div>
 <div class="flex gap-sm flex-wrap">
  <a href="/admin/stage-bonus-points.php?series=<?= $seriesId ?>" class="btn btn--primary">
   <i data-lucide="trophy"></i>
   Sträckbonus
  </a>
  <form method="POST" class="inline">
   <?= csrf_field() ?>
   <input type="hidden" name="action" value="recalculate_all">
   <button type="submit" class="btn btn--primary" onclick="return confirm('Beräkna om alla seriepoäng för alla events?')">
    <i data-lucide="refresh-cw"></i>
    Beräkna om poäng
   </button>
  </form>
  <a href="/admin/series/edit/<?= $seriesId ?>" class="btn btn--secondary">
   <i data-lucide="settings"></i>
   Inställningar
  </a>
  <a href="/admin/series.php" class="btn btn--secondary">
   <i data-lucide="arrow-left"></i>
   Tillbaka
  </a>
 </div>
 </div>

 <!-- Messages -->
 <?php if ($message): ?>
 <div class="alert alert-<?= $messageType ?> mb-lg">
 <i data-lucide="<?= $messageType === 'success' ? 'check-circle' : ($messageType === 'error' ? 'alert-circle' : 'info') ?>"></i>
 <?= h($message) ?>
 </div>
 <?php endif; ?>

 <div class="grid grid-cols-1 gs-lg-grid-cols-3 gap-lg">
 <!-- Settings Column -->
 <div>
 <!-- Count Best Results Card -->
 <div class="card mb-lg">
  <div class="card-header">
  <h2 class="">
  <i data-lucide="calculator"></i>
  Poängräkning
  </h2>
  </div>
  <div class="card-body">
  <form method="POST">
  <?= csrf_field() ?>
  <input type="hidden" name="action" value="update_count_best">

  <div class="form-group">
  <label for="count_best_results" class="label">Räkna bästa resultat</label>
  <select name="count_best_results" id="count_best_results" class="input" onchange="this.form.submit()">
   <option value="null" <?= $series['count_best_results'] === null ? 'selected' : '' ?>>Alla resultat</option>
   <?php for ($i = 1; $i <= 10; $i++): ?>
   <option value="<?= $i ?>" <?= $series['count_best_results'] == $i ? 'selected' : '' ?>>
   Bästa <?= $i ?> av <?= count($seriesEvents) ?>
   </option>
   <?php endfor; ?>
  </select>
  <small class="text-xs text-secondary">
   Övriga resultat visas med överstrykning och räknas inte i totalen
  </small>
  </div>
  </form>
  </div>
 </div>

 <!-- Add Event Card -->
 <div class="card gs-gradient-brand">
  <div class="card-header">
  <h2 class="">
  <i data-lucide="plus"></i>
  Lägg till Event
  </h2>
  </div>
 <div class="card-body">
  <?php if (empty($eventsNotInSeries)): ?>
  <p class="text-sm text-secondary">Alla events är redan tillagda i serien.</p>
  <?php else: ?>
  <?php if ($seriesYear): ?>
  <div class="alert alert--success mb-md" style="padding: 8px 12px; font-size: 0.85rem;">
   <i data-lucide="calendar-check" style="width: 14px; height: 14px;"></i>
   Serie-år: <strong><?= $seriesYear ?></strong>
   <?php if (!empty($matchingYearEvents)): ?>
   - <?= count($matchingYearEvents) ?> event matchar
   <?php endif; ?>
  </div>
  <?php endif; ?>
  <form method="POST">
  <?= csrf_field() ?>
  <input type="hidden" name="action" value="add_event">

  <div class="form-group">
  <label for="event_id" class="label">Välj event</label>
  <select name="event_id" id="event_id" class="input" required>
   <option value="">-- Välj event --</option>
   <?php if (!empty($matchingYearEvents)): ?>
   <optgroup label="✓ Matchar serieåret (<?= $seriesYear ?>)">
   <?php foreach ($matchingYearEvents as $event): ?>
   <option value="<?= $event['id'] ?>" style="font-weight: bold;">
   <?= h($event['name']) ?>
   <?php if ($event['date']): ?>
   (<?= date('Y-m-d', strtotime($event['date'])) ?>)
   <?php endif; ?>
   </option>
   <?php endforeach; ?>
   </optgroup>
   <?php endif; ?>
   <?php if (!empty($otherYearEvents)): ?>
   <optgroup label="Andra år">
   <?php foreach ($otherYearEvents as $event): ?>
   <option value="<?= $event['id'] ?>">
   <?= h($event['name']) ?>
   <?php if ($event['date']): ?>
   (<?= date('Y-m-d', strtotime($event['date'])) ?>)
   <?php endif; ?>
   </option>
   <?php endforeach; ?>
   </optgroup>
   <?php endif; ?>
  </select>
  <small class="text-xs text-secondary">
   Events som matchar serieåret (<?= $seriesYear ?>) visas först
  </small>
  </div>

  <div class="form-group">
  <label for="template_id" class="label">Poängmall (valfritt)</label>
  <select name="template_id" id="template_id" class="input">
   <option value="">-- Ingen mall --</option>
   <?php foreach ($templates as $template): ?>
   <option value="<?= $template['id'] ?>">
   <?= h($template['name']) ?>
   </option>
   <?php endforeach; ?>
  </select>
  <small class="text-xs text-secondary">
   Du kan ändra detta senare
  </small>
  </div>

  <button type="submit" class="btn btn--primary w-full">
  <i data-lucide="plus"></i>
  Lägg till
  </button>
  </form>

  <?php endif; ?>
 </div>
 </div>
 </div> <!-- Close Settings Column -->

 <!-- Events List -->
 <div class="gs-lg-col-span-2">
 <div class="card">
  <div class="card-header">
  <h2 class="">
  <i data-lucide="list"></i>
  Events i serien (<?= count($seriesEvents) ?>)
  </h2>
  <p class="text-sm text-secondary" style="margin-top: 4px;">Sorteras automatiskt efter datum. Events med huvudserie markeras med <span class="badge badge-success badge-sm">Låst</span></p>
  </div>
  <div class="card-body">
  <?php if (empty($seriesEvents)): ?>
  <div class="alert alert--warning">
  <p>Inga events har lagts till i denna serie än.</p>
  </div>
  <?php else: ?>
  <!-- Bulk Edit Form -->
  <div class="alert alert--info mb-md">
   <form method="POST" id="bulkForm">
    <?= csrf_field() ?>
    <input type="hidden" name="action" value="bulk_update_templates">
    <div class="flex items-center gap-md">
     <label class="font-semibold">Bulk-redigera valda event:</label>
     <select name="bulk_template_id" class="input input-sm" style="min-width: 200px;">
      <option value="">-- Välj poängmall --</option>
      <?php foreach ($templates as $template): ?>
       <option value="<?= $template['id'] ?>"><?= h($template['name']) ?></option>
      <?php endforeach; ?>
     </select>
     <button type="submit" class="btn btn-sm btn--primary" id="bulkSubmit" disabled>
      <i data-lucide="check-square"></i>
      Uppdatera valda
     </button>
     <span class="text-sm text-secondary" id="selectedCount">0 valda</span>
    </div>
   </form>
  </div>

  <div class="table-responsive">
  <table class="table">
   <thead>
   <tr>
   <th class="table-col-w-60">
    <input type="checkbox" id="selectAll" title="Markera alla">
   </th>
   <th class="table-col-w-60 text-center">#</th>
   <th>Event</th>
   <th>Datum</th>
   <th>Plats</th>
   <th>Poängmall</th>
   <th class="table-col-w-100">Åtgärder</th>
   </tr>
   </thead>
   <tbody>
   <?php $eventNumber = 1; $totalEvents = count($seriesEvents); ?>
   <?php foreach ($seriesEvents as $se): ?>
   <tr>
   <td>
    <input type="checkbox" class="event-checkbox" name="series_event_ids[]" value="<?= $se['id'] ?>" form="bulkForm">
   </td>
   <td class="text-center">
    <span class="badge badge-primary badge-sm">#<?= $eventNumber ?></span>
   </td>
   <td>
    <strong><?= h($se['event_name']) ?></strong>
    <?php if ($se['event_series_id'] == $seriesId): ?>
    <span class="badge badge-success badge-sm" title="Huvudserie - låst till denna serie"><i data-lucide="lock" style="width:10px;height:10px;"></i> Låst</span>
    <?php endif; ?>
    <?php if ($se['discipline']): ?>
    <br><span class="text-xs text-secondary"><?= h($se['discipline']) ?></span>
    <?php endif; ?>
   </td>
   <td><?= $se['event_date'] ? date('Y-m-d', strtotime($se['event_date'])) : '-' ?></td>
   <td><?= h($se['location'] ?? '-') ?></td>
   <td>
    <form method="POST" class="template-form" style="display: inline-block;">
    <?= csrf_field() ?>
    <input type="hidden" name="action" value="update_template">
    <input type="hidden" name="series_event_id" value="<?= $se['id'] ?>">
    <div style="display: flex; align-items: center; gap: 4px;">
     <select name="template_id" class="input input-sm" style="min-width: 150px;">
      <option value="">-- Ingen mall --</option>
      <?php foreach ($templates as $template): ?>
       <option value="<?= $template['id'] ?>" <?= $se['template_id'] == $template['id'] ? 'selected' : '' ?>>
        <?= h($template['name']) ?>
       </option>
      <?php endforeach; ?>
     </select>
     <button type="submit" class="btn btn-xs btn--primary" title="Spara">
      <i data-lucide="save" style="width: 14px; height: 14px;"></i>
     </button>
    </div>
    </form>
   </td>
   <td>
    <form method="POST" class="gs-display-inline" onsubmit="return confirm('Är du säker?');">
    <?= csrf_field() ?>
    <input type="hidden" name="action" value="remove_event">
    <input type="hidden" name="series_event_id" value="<?= $se['id'] ?>">
    <button type="submit" class="btn btn--sm btn--secondary btn-danger">
    <i data-lucide="trash-2"></i>
    </button>
    </form>
   </td>
   </tr>
   <?php $eventNumber++; ?>
   <?php endforeach; ?>
   </tbody>
  </table>
  </div>
  <?php endif; ?>
  </div>
 </div>
 </div>
 </div>
</div>
<!-- End container (unified-layout-footer will close <main>) -->

<script>
// Bulk edit functionality
document.addEventListener('DOMContentLoaded', function() {
 const selectAll = document.getElementById('selectAll');
 const checkboxes = document.querySelectorAll('.event-checkbox');
 const bulkSubmit = document.getElementById('bulkSubmit');
 const selectedCount = document.getElementById('selectedCount');

 if (!selectAll || !bulkSubmit || !selectedCount) return;

 // Update selected count and button state
 function updateBulkState() {
  const checkedCount = document.querySelectorAll('.event-checkbox:checked').length;
  selectedCount.textContent = checkedCount + ' valda';
  bulkSubmit.disabled = checkedCount === 0;
 }

 // Select all checkbox
 selectAll.addEventListener('change', function() {
  checkboxes.forEach(cb => cb.checked = this.checked);
  updateBulkState();
 });

 // Individual checkboxes
 checkboxes.forEach(cb => {
  cb.addEventListener('change', function() {
   // Update select all state
   selectAll.checked = document.querySelectorAll('.event-checkbox:checked').length === checkboxes.length;
   updateBulkState();
  });
 });

 // Form submission confirmation
 document.getElementById('bulkForm').addEventListener('submit', function(e) {
  const checkedCount = document.querySelectorAll('.event-checkbox:checked').length;
  const templateSelect = document.querySelector('select[name="bulk_template_id"]');
  const templateName = templateSelect.options[templateSelect.selectedIndex].text;

  if (!templateSelect.value) {
   e.preventDefault();
   alert('Välj en poängmall först!');
   return false;
  }

  if (!confirm(`Är du säker på att du vill uppdatera ${checkedCount} event med poängmallen "${templateName}"?\n\nDetta kommer omberäkna seriepoängen för alla valda event.`)) {
   e.preventDefault();
   return false;
  }
 });
});
</script>

<?php include __DIR__ . '/components/unified-layout-footer.php'; ?>
