<?php
/**
 * Diagnostic Tool: Rider Points Breakdown
 * Shows exactly how points are calculated for a rider across all systems
 */

require_once __DIR__ . '/../config.php';
require_admin();

$db = getDB();
$riderId = isset($_GET['rider_id']) ? (int)$_GET['rider_id'] : 0;

$pageTitle = 'Diagnose Rider Points';
include __DIR__ . '/../includes/layout-header.php';
?>

<div class="container">
 <h1 class="mb-lg">🔍 Rider Points Diagnostic</h1>

 <form method="GET" class="mb-lg">
 <div style="display: flex; gap: 1rem;">
  <input type="number" name="rider_id" value="<?= $riderId ?>"
   placeholder="Rider ID" class="input" style="width: 200px;">
  <button type="submit" class="btn btn--primary">Diagnose</button>
 </div>
 </form>

 <?php if ($riderId): ?>
 <?php
 // Get rider info
 $rider = $db->getRow("SELECT * FROM riders WHERE id = ?", [$riderId]);
 if (!$rider) {
  echo"<div class='alert alert--error'>Rider ID $riderId not found</div>";
 } else {
  ?>
  <div class="card mb-lg">
  <div class="card-header">
   <h2 class="">👤 Rider: <?= h($rider['firstname'] . ' ' . $rider['lastname']) ?></h2>
  </div>
  </div>

  <!-- GravitySeries Total Diagnostic -->
  <div class="card mb-lg">
  <div class="card-header">
   <h3 class="">🏆 GravitySeries Total (Individual Championship)</h3>
  </div>
  <div class="card-body">
   <?php
   // Find GravitySeries Total series
   $totalSeries = $db->getRow("
   SELECT id, name FROM series
   WHERE id = 8 OR (
    active = 1 AND (
    name LIKE '%Total%'
    OR (name LIKE '%GravitySeries%'
     AND name NOT LIKE '%Capital%'
     AND name NOT LIKE '%Götaland%'
     AND name NOT LIKE '%Jämtland%')
    )
   )
   ORDER BY (id = 8) DESC, year DESC LIMIT 1
  ");

   if ($totalSeries) {
   echo"<p><strong>Serie:</strong> {$totalSeries['name']} (ID: {$totalSeries['id']})</p>";

   // Method 1: Via series_events
   $method1 = $db->getAll("
    SELECT
    e.id as event_id,
    e.name as event_name,
    e.date as event_date,
    r.points,
    r.status,
    'series_events' as method
    FROM results r
    JOIN events e ON r.event_id = e.id
    JOIN series_events se ON e.id = se.event_id
    WHERE se.series_id = ? AND r.cyclist_id = ?
    ORDER BY e.date DESC
   ", [$totalSeries['id'], $riderId]);

   // Method 2: Via events.series_id
   $method2 = $db->getAll("
    SELECT
    e.id as event_id,
    e.name as event_name,
    e.date as event_date,
    r.points,
    r.status,
    'events.series_id' as method
    FROM results r
    JOIN events e ON r.event_id = e.id
    WHERE e.series_id = ? AND r.cyclist_id = ?
    AND e.series_id IS NOT NULL
    ORDER BY e.date DESC
   ", [$totalSeries['id'], $riderId]);

   // Combined (what the UNION should give)
   $combined = $db->getAll("
    SELECT DISTINCT
    e.id as event_id,
    e.name as event_name,
    e.date as event_date,
    r.points,
    r.status
    FROM results r
    JOIN events e ON r.event_id = e.id
    WHERE r.cyclist_id = ?
    AND (
    e.id IN (SELECT event_id FROM series_events WHERE series_id = ?)
    OR e.series_id = ?
    )
    ORDER BY e.date DESC
   ", [$riderId, $totalSeries['id'], $totalSeries['id']]);

   ?>
   <h4 class="mt-lg">Method 1: Via series_events junction table</h4>
   <table class="table">
    <thead>
    <tr>
     <th>Date</th>
     <th>Event</th>
     <th>Status</th>
     <th>Points</th>
    </tr>
    </thead>
    <tbody>
    <?php
    $method1Total = 0;
    foreach ($method1 as $r):
     if ($r['status'] === 'finished' && $r['points'] > 0) {
     $method1Total += $r['points'];
     }
    ?>
     <tr>
     <td><?= $r['event_date'] ?></td>
     <td><?= h($r['event_name']) ?></td>
     <td><?= $r['status'] ?></td>
     <td><?= $r['points'] ?></td>
     </tr>
    <?php endforeach; ?>
    <tr class="table-footer">
     <td colspan="3">Total (finished + points > 0):</td>
     <td><strong><?= $method1Total ?></strong></td>
    </tr>
    </tbody>
   </table>

   <h4 class="mt-lg">Method 2: Via events.series_id direct link</h4>
   <table class="table">
    <thead>
    <tr>
     <th>Date</th>
     <th>Event</th>
     <th>Status</th>
     <th>Points</th>
    </tr>
    </thead>
    <tbody>
    <?php
    $method2Total = 0;
    foreach ($method2 as $r):
     if ($r['status'] === 'finished' && $r['points'] > 0) {
     $method2Total += $r['points'];
     }
    ?>
     <tr>
     <td><?= $r['event_date'] ?></td>
     <td><?= h($r['event_name']) ?></td>
     <td><?= $r['status'] ?></td>
     <td><?= $r['points'] ?></td>
     </tr>
    <?php endforeach; ?>
    <tr class="table-footer">
     <td colspan="3">Total (finished + points > 0):</td>
     <td><strong><?= $method2Total ?></strong></td>
    </tr>
    </tbody>
   </table>

   <h4 class="mt-lg">✅ Combined (UNION - What rider.php uses)</h4>
   <table class="table">
    <thead>
    <tr>
     <th>Date</th>
     <th>Event</th>
     <th>Status</th>
     <th>Points</th>
    </tr>
    </thead>
    <tbody>
    <?php
    $combinedTotal = 0;
    foreach ($combined as $r):
     if ($r['status'] === 'finished' && $r['points'] > 0) {
     $combinedTotal += $r['points'];
     }
    ?>
     <tr>
     <td><?= $r['event_date'] ?></td>
     <td><?= h($r['event_name']) ?></td>
     <td><?= $r['status'] ?></td>
     <td><?= $r['points'] ?></td>
     </tr>
    <?php endforeach; ?>
    <tr class="table-footer">
     <td colspan="3">Total (finished + points > 0):</td>
     <td><strong><?= $combinedTotal ?></strong></td>
    </tr>
    </tbody>
   </table>

   <div class="alert alert--info mt-lg">
    <strong>Summary:</strong><br>
    Method 1 (series_events): <?= $method1Total ?> points<br>
    Method 2 (events.series_id): <?= $method2Total ?> points<br>
    <strong>Combined UNION: <?= $combinedTotal ?> points</strong><br>
    <br>
    <?php if ($method1Total + $method2Total > $combinedTotal): ?>
    ⚠️ There is overlap! Some events are in BOTH methods.
    <?php else: ?>
    ✅ No overlap - methods are exclusive.
    <?php endif; ?>
   </div>
   <?php
   } else {
   echo"<p>No GravitySeries Total series found</p>";
   }
   ?>
  </div>
  </div>

  <!-- GravitySeries Team Diagnostic -->
  <?php if ($rider['club_id']): ?>
  <div class="card mb-lg">
  <div class="card-header">
   <h3 class="">👥 GravitySeries Team (Club Points)</h3>
  </div>
  <div class="card-body">
   <?php
   if ($totalSeries) {
   $teamPoints = $db->getAll("
    SELECT
    e.name as event_name,
    e.date as event_date,
    crp.original_points,
    crp.club_points,
    crp.percentage_applied
    FROM club_rider_points crp
    JOIN events e ON crp.event_id = e.id
    WHERE crp.rider_id = ?
    AND crp.club_id = ?
    AND crp.series_id = ?
    ORDER BY e.date DESC
   ", [$riderId, $rider['club_id'], $totalSeries['id']]);

   ?>
   <table class="table">
    <thead>
    <tr>
     <th>Date</th>
     <th>Event</th>
     <th>Original Points</th>
     <th>Percentage</th>
     <th>Club Points</th>
    </tr>
    </thead>
    <tbody>
    <?php
    $teamTotal = 0;
    foreach ($teamPoints as $tp):
     $teamTotal += $tp['club_points'];
    ?>
     <tr>
     <td><?= $tp['event_date'] ?></td>
     <td><?= h($tp['event_name']) ?></td>
     <td><?= $tp['original_points'] ?></td>
     <td><?= $tp['percentage_applied'] ?>%</td>
     <td><?= number_format($tp['club_points'], 1) ?></td>
     </tr>
    <?php endforeach; ?>
    <tr class="table-footer">
     <td colspan="4">Total:</td>
     <td><strong><?= number_format($teamTotal, 1) ?></strong></td>
    </tr>
    </tbody>
   </table>
   <?php
   }
   ?>
  </div>
  </div>
  <?php endif; ?>

  <!-- Ranking Diagnostic -->
  <div class="card mb-lg">
  <div class="card-header">
   <h3 class="">📊 Ranking Points (24-month rolling)</h3>
  </div>
  <div class="card-body">
   <?php
   $rankingCount = $db->getRow("
   SELECT COUNT(*) as cnt
   FROM ranking_points
   WHERE rider_id = ?
  ", [$riderId]);

   if ($rankingCount['cnt'] == 0) {
   echo"<div class='alert alert--warning'>";
   echo"⚠️ No ranking data found. Run ranking update at <a href='/admin/ranking.php'>/admin/ranking.php</a>";
   echo"</div>";
   } else {
   foreach (['ENDURO', 'DH', 'GRAVITY'] as $disc) {
    $rankingData = $db->getAll("
    SELECT
     e.name as event_name,
     e.date as event_date,
     rp.original_points,
     rp.field_multiplier,
     rp.event_level_multiplier,
     rp.ranking_points
    FROM ranking_points rp
    JOIN events e ON rp.event_id = e.id
    WHERE rp.rider_id = ? AND rp.discipline = ?
    AND e.date >= DATE_SUB(NOW(), INTERVAL 24 MONTH)
    ORDER BY e.date DESC
   ", [$riderId, $disc]);

    if (!empty($rankingData)) {
    echo"<h4 class=' mt-lg'>" . $disc ."</h4>";
    ?>
    <table class="table">
     <thead>
     <tr>
      <th>Date</th>
      <th>Event</th>
      <th>Original</th>
      <th>Field Multi</th>
      <th>Level Multi</th>
      <th>Ranking Points</th>
     </tr>
     </thead>
     <tbody>
     <?php
     $rankingTotal = 0;
     foreach ($rankingData as $rd):
      $rankingTotal += $rd['ranking_points'];
     ?>
      <tr>
      <td><?= $rd['event_date'] ?></td>
      <td><?= h($rd['event_name']) ?></td>
      <td><?= $rd['original_points'] ?></td>
      <td><?= $rd['field_multiplier'] ?></td>
      <td><?= $rd['event_level_multiplier'] ?></td>
      <td><?= number_format($rd['ranking_points'], 1) ?></td>
      </tr>
     <?php endforeach; ?>
     <tr class="table-footer">
      <td colspan="5">Total:</td>
      <td><strong><?= number_format($rankingTotal, 1) ?></strong></td>
     </tr>
     </tbody>
    </table>
    <?php
    }
   }
   }
   ?>
  </div>
  </div>
 <?php } ?>
 <?php endif; ?>
</div>

<?php include __DIR__ . '/../includes/layout-footer.php'; ?>
