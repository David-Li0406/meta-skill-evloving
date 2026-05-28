<?php
/**
 * Ranking Debug Tool
 * Shows detailed calculation breakdown for ranking points
 */

require_once __DIR__ . '/../config.php';
require_once __DIR__ . '/../includes/ranking_functions.php';
require_admin();

$db = getDB();

// Get parameters
$riderId = isset($_GET['rider_id']) ? (int)$_GET['rider_id'] : null;
$eventId = isset($_GET['event_id']) ? (int)$_GET['event_id'] : null;
$discipline = isset($_GET['discipline']) ? strtoupper($_GET['discipline']) : 'GRAVITY';

$pageTitle = 'Ranking Debug';
$pageType = 'admin';

include __DIR__ . '/../includes/layout-header.php';
?>

<main class="main-content">
 <div class="container">
 <div class="flex items-center justify-between mb-lg">
  <h1 class="text-primary">
  <i data-lucide="bug"></i>
  Ranking Debug
  </h1>
  <a href="/admin/ranking.php" class="btn btn--secondary">
  <i data-lucide="arrow-left"></i>
  Tillbaka
  </a>
 </div>

 <!-- Filter Form -->
 <div class="card mb-lg">
  <div class="card-header">
  <h2 class="text-primary">Filter</h2>
  </div>
  <div class="card-body">
  <form method="GET" class="gs-form">
   <div class="grid grid-cols-3 gap-md">
   <div class="form-group">
    <label for="rider_id" class="label">Rider ID (valfritt)</label>
    <input type="number" id="rider_id" name="rider_id"
     value="<?= $riderId ?? '' ?>"
     class="input"
     placeholder="T.ex. 7476">
   </div>
   <div class="form-group">
    <label for="event_id" class="label">Event ID (valfritt)</label>
    <input type="number" id="event_id" name="event_id"
     value="<?= $eventId ?? '' ?>"
     class="input"
     placeholder="T.ex. 123">
   </div>
   <div class="form-group">
    <label for="discipline" class="label">Disciplin</label>
    <select id="discipline" name="discipline" class="input">
    <option value="GRAVITY" <?= $discipline === 'GRAVITY' ? 'selected' : '' ?>>Gravity</option>
    <option value="ENDURO" <?= $discipline === 'ENDURO' ? 'selected' : '' ?>>Enduro</option>
    <option value="DH" <?= $discipline === 'DH' ? 'selected' : '' ?>>Downhill</option>
    </select>
   </div>
   </div>
   <button type="submit" class="btn btn--primary mt-md">
   <i data-lucide="search"></i>
   Visa beräkning
   </button>
  </form>
  </div>
 </div>

 <?php if ($riderId || $eventId): ?>
  <?php
  // Get settings
  $fieldMultipliers = getRankingFieldMultipliers($db);
  $eventLevelMultipliers = getEventLevelMultipliers($db);
  $timeDecay = getRankingTimeDecay($db);

  $cutoffDate = date('Y-m-d', strtotime('-24 months'));
  $month12Cutoff = date('Y-m-d', strtotime('-12 months'));

  // Build query filters
  $disciplineFilter = '';
  $params = [$cutoffDate];

  if ($discipline !== 'GRAVITY') {
  $disciplineFilter = 'AND e.discipline = ?';
  $params[] = $discipline;
  } else {
  $disciplineFilter ="AND e.discipline IN ('ENDURO', 'DH')";
  }

  // Add rider/event filters
  $extraFilter = '';
  if ($riderId) {
  $extraFilter .= ' AND r.cyclist_id = ?';
  $params[] = $riderId;
  }
  if ($eventId) {
  $extraFilter .= ' AND r.event_id = ?';
  $params[] = $eventId;
  }

  // Get results with detailed info
  $results = $db->getAll("
  SELECT
   r.cyclist_id as rider_id,
   r.event_id,
   r.class_id,
   COALESCE(
   CASE
    WHEN COALESCE(r.run_1_points, 0) > 0 OR COALESCE(r.run_2_points, 0) > 0
    THEN COALESCE(r.run_1_points, 0) + COALESCE(r.run_2_points, 0)
    ELSE r.points
   END,
   r.points
   ) as original_points,
   e.date as event_date,
   e.name as event_name,
   e.discipline,
   COALESCE(e.event_level, 'national') as event_level,
   cl.name as class_name,
   rider.firstname,
   rider.lastname
  FROM results r
  STRAIGHT_JOIN events e ON r.event_id = e.id
  STRAIGHT_JOIN classes cl ON r.class_id = cl.id
  LEFT JOIN riders rider ON r.cyclist_id = rider.id
  WHERE r.status = 'finished'
  AND (r.points > 0 OR COALESCE(r.run_1_points, 0) > 0 OR COALESCE(r.run_2_points, 0) > 0)
  AND e.date >= ?
  {$disciplineFilter}
  {$extraFilter}
  AND COALESCE(cl.series_eligible, 1) = 1
  AND COALESCE(cl.awards_points, 1) = 1
  ORDER BY e.date DESC, r.cyclist_id
 ", $params);

  // Calculate field sizes
  $fieldSizes = [];
  foreach ($results as $result) {
  $key = $result['event_id'] . '_' . $result['class_id'];
  if (!isset($fieldSizes[$key])) {
   $fieldSizes[$key] = 0;
  }
  $fieldSizes[$key]++;
  }
  ?>

  <!-- Settings Info -->
  <div class="card mb-lg">
  <div class="card-header">
   <h2 class="text-primary">
   <i data-lucide="settings"></i>
   Aktuella inställningar
   </h2>
  </div>
  <div class="card-body">
   <div class="grid grid-cols-2 gap-lg">
   <div>
    <h3 class="mb-sm">Eventnivå-multiplikatorer</h3>
    <ul>
    <li><strong>National:</strong> <?= number_format($eventLevelMultipliers['national'], 2) ?> (<?= $eventLevelMultipliers['national'] * 100 ?>%)</li>
    <li><strong>Sportmotion:</strong> <?= number_format($eventLevelMultipliers['sportmotion'], 2) ?> (<?= $eventLevelMultipliers['sportmotion'] * 100 ?>%)</li>
    </ul>
   </div>
   <div>
    <h3 class="mb-sm">Tidsviktning</h3>
    <ul>
    <li><strong>Månad 1-12:</strong> <?= number_format($timeDecay['months_1_12'], 2) ?> (<?= $timeDecay['months_1_12'] * 100 ?>%)</li>
    <li><strong>Månad 13-24:</strong> <?= number_format($timeDecay['months_13_24'], 2) ?> (<?= $timeDecay['months_13_24'] * 100 ?>%)</li>
    </ul>
   </div>
   </div>
  </div>
  </div>

  <!-- Results Table -->
  <div class="card">
  <div class="card-header">
   <h2 class="text-primary">
   <i data-lucide="calculator"></i>
   Beräkningsdetaljer (<?= count($results) ?> resultat)
   </h2>
  </div>
  <div class="card-body">
   <div style="overflow-x: auto;">
   <table class="table">
    <thead>
    <tr>
     <th>Rider</th>
     <th>Event</th>
     <th>Datum</th>
     <th>Klass</th>
     <th>Fält</th>
     <th>Event Nivå</th>
     <th>Original p</th>
     <th>Fält mult</th>
     <th>Event mult</th>
     <th>Tid mult</th>
     <th style="background: #fef3c7;">Ranking p</th>
     <th style="background: #dcfce7;">Viktade p</th>
    </tr>
    </thead>
    <tbody>
    <?php foreach ($results as $result): ?>
     <?php
     $key = $result['event_id'] . '_' . $result['class_id'];
     $fieldSize = $fieldSizes[$key] ?? 1;

     $fieldMult = getFieldMultiplier($fieldSize, $fieldMultipliers);
     $eventLevelMult = $eventLevelMultipliers[$result['event_level']] ?? 1.00;

     // Calculate time decay
     $eventDate = new DateTime($result['event_date']);
     $today = new DateTime();
     $monthsDiff = $eventDate->diff($today)->m + ($eventDate->diff($today)->y * 12);

     $timeMult = 0;
     $timeLabel = '';
     if ($monthsDiff < 12) {
     $timeMult = $timeDecay['months_1_12'];
     $timeLabel = '1-12 mån';
     } elseif ($monthsDiff < 24) {
     $timeMult = $timeDecay['months_13_24'];
     $timeLabel = '13-24 mån';
     } else {
     $timeMult = $timeDecay['months_25_plus'];
     $timeLabel = '25+ mån';
     }

     $rankingPoints = $result['original_points'] * $fieldMult * $eventLevelMult;
     $weightedPoints = $rankingPoints * $timeMult;
     ?>
     <tr>
     <td><?= h($result['firstname'] . ' ' . $result['lastname']) ?></td>
     <td><?= h($result['event_name']) ?></td>
     <td><?= date('Y-m-d', strtotime($result['event_date'])) ?></td>
     <td><?= h($result['class_name']) ?></td>
     <td><?= $fieldSize ?> åkare</td>
     <td>
      <span style="padding: 2px 8px; border-radius: 4px; font-size: 0.75rem;
       <?= $result['event_level'] === 'sportmotion' ? 'background: #fef3c7; color: #92400e;' : 'background: #dbeafe; color: #1e40af;' ?>">
      <?= ucfirst($result['event_level']) ?>
      </span>
     </td>
     <td><?= number_format($result['original_points'], 1) ?></td>
     <td><?= number_format($fieldMult, 2) ?> <small>(<?= $fieldMult * 100 ?>%)</small></td>
     <td><?= number_format($eventLevelMult, 2) ?> <small>(<?= $eventLevelMult * 100 ?>%)</small></td>
     <td><?= number_format($timeMult, 2) ?> <small>(<?= $timeLabel ?>)</small></td>
     <td style="background: #fef3c7; font-weight: 600;"><?= number_format($rankingPoints, 1) ?></td>
     <td style="background: #dcfce7; font-weight: 600;"><?= number_format($weightedPoints, 1) ?></td>
     </tr>
    <?php endforeach; ?>
    </tbody>
   </table>
   </div>

   <?php if (empty($results)): ?>
   <p class="text-secondary text-center py-xl">
    Inga resultat hittades för de valda filtren.
   </p>
   <?php endif; ?>
  </div>
  </div>

  <!-- Calculation Explanation -->
  <div class="card mt-lg">
  <div class="card-header">
   <h2 class="text-primary">
   <i data-lucide="info"></i>
   Förklaring
   </h2>
  </div>
  <div class="card-body">
   <h3 class="mb-sm">Beräkningsformel:</h3>
   <div class="gs-bg-light p-md gs-rounded mb-md" style="font-family: monospace;">
   <strong>Ranking Points</strong> = Original Points × Fält Mult × Event Mult<br>
   <strong>Viktade Points</strong> = Ranking Points × Tid Mult
   </div>

   <h3 class="mb-sm">Exempel (Marie's Capital Enduro #4):</h3>
   <div class="gs-bg-light p-md gs-rounded">
   <strong>Om Sportmotion med 2 åkare:</strong><br>
   Ranking Points = 500 × 0.77 (2 åkare) × 0.50 (sportmotion) = <strong>192.5p</strong><br>
   <br>
   <strong>Om National med 2 åkare:</strong><br>
   Ranking Points = 500 × 0.77 (2 åkare) × 1.00 (national) = <strong>385p</strong><br>
   <br>
   <strong>Om event är från senaste 12 mån:</strong><br>
   Viktade Points = Ranking Points × 1.00 = samma som Ranking Points
   </div>
  </div>
  </div>

 <?php else: ?>
  <div class="card">
  <div class="card-body">
   <p class="text-secondary text-center py-xl">
   Välj Rider ID eller Event ID ovan för att se beräkningsdetaljer.
   </p>
  </div>
  </div>
 <?php endif; ?>

 </div>
</main>

<style>
.table {
 width: 100%;
 font-size: 0.875rem;
}

.table th {
 background: var(--gs-gray-100);
 padding: 0.75rem 0.5rem;
 text-align: left;
 font-weight: 600;
 white-space: nowrap;
}

.table td {
 padding: 0.75rem 0.5rem;
 border-bottom: 1px solid var(--gs-gray-200);
}

.table tbody tr:hover {
 background: var(--gs-gray-50);
}

@media (max-width: 767px) {
 .grid.grid-cols-3 {
 grid-template-columns: 1fr !important;
 }

 .grid.grid-cols-2 {
 grid-template-columns: 1fr !important;
 }
}
</style>

<?php include __DIR__ . '/../includes/layout-footer.php'; ?>
