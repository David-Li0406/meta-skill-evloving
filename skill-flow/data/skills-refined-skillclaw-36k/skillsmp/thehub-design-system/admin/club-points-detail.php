<?php
/**
 * Admin Club Points Detail
 * Shows detailed breakdown of a club's points in a series
 */
require_once __DIR__ . '/../config.php';
require_once __DIR__ . '/../includes/club-points-system.php';
require_admin();

$db = getDB();

// Get parameters
$clubId = isset($_GET['club_id']) ? (int)$_GET['club_id'] : 0;
$seriesId = isset($_GET['series_id']) ? (int)$_GET['series_id'] : 0;

if (!$clubId || !$seriesId) {
 header('Location: /admin/club-points.php');
 exit;
}

// Get detailed breakdown
$detail = getClubPointsDetail($db, $clubId, $seriesId);

if (!$detail || !$detail['club']) {
 set_flash('error', 'Klubb hittades inte');
 header('Location: /admin/club-points.php');
 exit;
}

$club = $detail['club'];
$standing = $detail['standing'];
$events = $detail['events'];
$riderDetails = $detail['rider_details'];

// Get series info
$series = $db->getRow("SELECT * FROM series WHERE id = ?", [$seriesId]);

$page_title = $club['name'] . ' - Klubbpoäng';
include __DIR__ . '/components/unified-layout.php';
?>

<!-- Back Button -->
<div class="mb-lg">
  <a href="/admin/club-points.php?series_id=<?= $seriesId ?>" class="btn btn--secondary btn--sm">
    <i data-lucide="arrow-left"></i>
    Tillbaka till ranking
  </a>
</div>

 <!-- Header -->
 <div class="flex items-center gap-lg mb-lg">
  <?php if ($club['logo']): ?>
  <img src="<?= h($club['logo']) ?>" alt="" style="width: 64px; height: 64px; object-fit: contain;">
  <?php endif; ?>
  <div>
  <h1 class="text-primary gs-mb-0">
   <?= h($club['name']) ?>
  </h1>
  <?php if ($club['city']): ?>
   <p class="text-secondary gs-mt-xs">
   <i data-lucide="map-pin" class="icon-sm"></i>
   <?= h($club['city']) ?>
   <?php if ($club['region']): ?>, <?= h($club['region']) ?><?php endif; ?>
   </p>
  <?php endif; ?>
  </div>
 </div>

 <!-- Summary Card -->
 <?php if ($standing): ?>
 <div class="card mb-lg">
  <div class="card-header">
  <h2 class="text-primary">
   <i data-lucide="award"></i>
   Sammanfattning - <?= h($series['name']) ?>
  </h2>
  </div>
  <div class="card-body">
  <div class="grid grid-cols-5 gap-lg">
   <div class="text-center">
   <div class="gs-text-3xl font-bold <?= $standing['ranking'] <= 3 ? 'text-warning' : 'text-primary' ?>">
    #<?= $standing['ranking'] ?>
   </div>
   <div class="text-sm text-secondary">Ranking</div>
   </div>
   <div class="text-center">
   <div class="gs-text-3xl font-bold text-primary">
    <?= number_format($standing['total_points']) ?>
   </div>
   <div class="text-sm text-secondary">Totala poäng</div>
   </div>
   <div class="text-center">
   <div class="gs-text-3xl font-bold text-primary">
    <?= $standing['total_participants'] ?>
   </div>
   <div class="text-sm text-secondary">Deltagare</div>
   </div>
   <div class="text-center">
   <div class="gs-text-3xl font-bold text-primary">
    <?= $standing['events_count'] ?>
   </div>
   <div class="text-sm text-secondary">Events</div>
   </div>
   <div class="text-center">
   <div class="gs-text-3xl font-bold text-primary">
    <?= number_format($standing['best_event_points']) ?>
   </div>
   <div class="text-sm text-secondary">Bästa event</div>
   </div>
  </div>
  </div>
 </div>
 <?php endif; ?>

 <!-- Events Breakdown -->
 <div class="card">
  <div class="card-header">
  <h2 class="text-primary">
   <i data-lucide="calendar"></i>
   Poäng per event
  </h2>
  </div>
  <div class="card-body gs-p-0">
  <?php if (empty($events)): ?>
   <div class="text-center py-xl">
   <p class="text-secondary">Inga eventpoäng registrerade.</p>
   </div>
  <?php else: ?>
   <?php foreach ($events as $event): ?>
   <div class="border-b" style="border-color: var(--border);">
    <!-- Event Header -->
    <div class="p-md gs-bg-light flex items-center justify-between">
    <div>
     <strong><?= h($event['event_name']) ?></strong>
     <span class="text-sm text-secondary ml-sm">
     <?= date('Y-m-d', strtotime($event['event_date'])) ?>
     <?php if ($event['location']): ?>
      | <?= h($event['location']) ?>
     <?php endif; ?>
     </span>
    </div>
    <div class="flex items-center gap-lg">
     <span class="text-sm text-secondary">
     <?= $event['participants_count'] ?> deltagare
     </span>
     <span class="font-bold text-primary">
     <?= number_format($event['total_points']) ?> p
     </span>
    </div>
    </div>

    <!-- Rider Details -->
    <?php if (isset($riderDetails[$event['event_id']]) && !empty($riderDetails[$event['event_id']])): ?>
    <table class="table table-sm gs-mb-0">
     <thead>
     <tr>
      <th>Åkare</th>
      <th>Klass</th>
      <th class="text-right">Original</th>
      <th class="text-center">%</th>
      <th class="text-right">Klubbpoäng</th>
     </tr>
     </thead>
     <tbody>
     <?php foreach ($riderDetails[$event['event_id']] as $rider): ?>
      <tr class="<?= $rider['club_points'] == 0 ? 'text-secondary' : '' ?>">
      <td>
       <?= h($rider['firstname']) ?> <?= h($rider['lastname']) ?>
       <?php if ($rider['rider_rank_in_club'] == 1): ?>
       <span class="badge badge-warning badge-sm gs-ml-xs">1:a</span>
       <?php elseif ($rider['rider_rank_in_club'] == 2): ?>
       <span class="badge badge-secondary badge-sm gs-ml-xs">2:a</span>
       <?php endif; ?>
      </td>
      <td><?= h($rider['class_name'] ?? '-') ?></td>
      <td class="text-right"><?= $rider['original_points'] ?></td>
      <td class="text-center">
       <?php if ($rider['percentage_applied'] == 100): ?>
       <span class="badge badge-success badge-sm">100%</span>
       <?php elseif ($rider['percentage_applied'] == 50): ?>
       <span class="badge badge-warning badge-sm">50%</span>
       <?php else: ?>
       <span class="badge badge-secondary badge-sm">0%</span>
       <?php endif; ?>
      </td>
      <td class="text-right font-bold">
       <?= $rider['club_points'] ?>
      </td>
      </tr>
     <?php endforeach; ?>
     </tbody>
    </table>
    <?php endif; ?>
   </div>
   <?php endforeach; ?>
  <?php endif; ?>
  </div>
 </div>

 <!-- Points Summary by Class -->
 <?php
 // Calculate points by class
 $classTotals = [];
 foreach ($riderDetails as $eventId => $riders) {
  foreach ($riders as $rider) {
  $className = $rider['class_name'] ?? 'Okänd';
  if (!isset($classTotals[$className])) {
   $classTotals[$className] = ['points' => 0, 'riders' => 0];
  }
  $classTotals[$className]['points'] += $rider['club_points'];
  if ($rider['club_points'] > 0) {
   $classTotals[$className]['riders']++;
  }
  }
 }
 arsort($classTotals);
 ?>

 <?php if (!empty($classTotals)): ?>
 <div class="card mt-lg">
  <div class="card-header">
  <h2 class="text-primary">
   <i data-lucide="layers"></i>
   Poäng per klass
  </h2>
  </div>
  <div class="card-body gs-p-0">
  <table class="table gs-mb-0">
   <thead>
   <tr>
    <th>Klass</th>
    <th class="text-right">Poänggivande åkare</th>
    <th class="text-right">Totala poäng</th>
   </tr>
   </thead>
   <tbody>
   <?php foreach ($classTotals as $className => $data): ?>
    <tr>
    <td><strong><?= h($className) ?></strong></td>
    <td class="text-right"><?= $data['riders'] ?></td>
    <td class="text-right font-bold"><?= number_format($data['points']) ?></td>
    </tr>
   <?php endforeach; ?>
   </tbody>
  </table>
  </div>
 </div>
<?php endif; ?>

<?php include __DIR__ . '/components/unified-layout-footer.php'; ?>
