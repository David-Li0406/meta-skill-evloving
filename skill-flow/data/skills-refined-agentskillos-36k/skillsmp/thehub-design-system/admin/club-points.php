<?php
/**
 * Admin Club Points Standings
 * Shows club rankings per series with filtering and statistics
 */
require_once __DIR__ . '/../config.php';
require_once __DIR__ . '/../includes/club-points-system.php';
require_admin();

$db = getDB();
$current_admin = get_current_admin();

$message = '';
$messageType = 'info';

// Check if tables exist
if (!clubPointsTablesExist($db)) {
    $message = 'Klubbpoängtabeller saknas. <a href="/admin/run-migration.php?file=071_club_points_system.sql">Kör migration 071</a> för att skapa dem.';
    $messageType = 'warning';
}

// Get all series for filter
$seriesList = $db->getAll("
 SELECT id, name, year, discipline
 FROM series
 WHERE active = 1
 ORDER BY year DESC, name ASC
");

// Get selected series (default to first or most recent)
$selectedSeriesId = isset($_GET['series_id']) ? (int)$_GET['series_id'] : 0;
if (!$selectedSeriesId && !empty($seriesList)) {
 $selectedSeriesId = $seriesList[0]['id'];
}

// Handle recalculate action
if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['recalculate'])) {
    checkCsrf();

    $seriesIdToRecalc = (int)$_POST['series_id'];
    if ($seriesIdToRecalc) {
        $stats = recalculateSeriesClubPoints($db, $seriesIdToRecalc);
        $message = "Omräkning klar! {$stats['events_processed']} events, {$stats['total_clubs']} klubbar, {$stats['total_points']} poäng.";
        $messageType = 'success';
        $selectedSeriesId = $seriesIdToRecalc;
    }
}

// Handle recalculate ALL series
if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['recalculate_all'])) {
    checkCsrf();

    $totalStats = ['series' => 0, 'events' => 0, 'clubs' => 0, 'points' => 0];

    foreach ($seriesList as $series) {
        $stats = recalculateSeriesClubPoints($db, $series['id']);
        $totalStats['series']++;
        $totalStats['events'] += $stats['events_processed'];
        $totalStats['clubs'] += $stats['total_clubs'];
        $totalStats['points'] += $stats['total_points'];
    }

    $message = "ALLA serier omräknade! {$totalStats['series']} serier, {$totalStats['events']} events, {$totalStats['clubs']} klubbar totalt.";
    $messageType = 'success';
}

// Get standings for selected series
$standings = [];
$seriesInfo = null;
if ($selectedSeriesId) {
 $standings = getClubStandings($db, $selectedSeriesId);
 $seriesInfo = $db->getRow("SELECT * FROM series WHERE id = ?", [$selectedSeriesId]);
}

// Calculate summary stats
$totalClubs = count($standings);
$totalPoints = array_sum(array_column($standings, 'total_points'));
$totalParticipants = array_sum(array_column($standings, 'total_participants'));

$page_title = 'Klubbpoäng';
include __DIR__ . '/components/unified-layout.php';
?>

<div class="mb-lg">
 <a href="/clubs/leaderboard.php<?= $selectedSeriesId ? '?series_id=' . $selectedSeriesId : '' ?>" class="btn btn--secondary" target="_blank">
 <i data-lucide="external-link"></i>
 Publik vy
 </a>
 </div>

 <!-- Messages -->
 <?php if ($message): ?>
 <div class="alert alert-<?= $messageType ?> mb-lg">
 <i data-lucide="<?= $messageType === 'success' ? 'check-circle' : ($messageType === 'error' ? 'alert-circle' : 'info') ?>"></i>
 <?= h($message) ?>
 </div>
 <?php endif; ?>

 <!-- Filters and Actions -->
 <div class="card mb-lg">
 <div class="card-body">
 <div class="flex gs-items-end gap-lg flex-wrap">
  <!-- Series Filter -->
  <div class="form-group gs-mb-0" style="flex: 1; min-width: 200px;">
  <label for="series_filter" class="label">Välj serie</label>
  <select id="series_filter" class="input" onchange="window.location.href='?series_id=' + this.value">
  <option value="">-- Välj serie --</option>
  <?php foreach ($seriesList as $series): ?>
  <option value="<?= $series['id'] ?>" <?= $series['id'] == $selectedSeriesId ? 'selected' : '' ?>>
   <?= h($series['name']) ?> (<?= $series['year'] ?>)
  </option>
  <?php endforeach; ?>
  </select>
  </div>

  <!-- Recalculate Button -->
  <?php if ($selectedSeriesId): ?>
  <form method="POST" class="gs-mb-0" style="display: inline;">
  <?= csrf_field() ?>
  <input type="hidden" name="series_id" value="<?= $selectedSeriesId ?>">
  <button type="submit" name="recalculate" class="btn btn--secondary"
  onclick="return confirm('Räkna om alla klubbpoäng för denna serie?')">
  <i data-lucide="refresh-cw"></i>
  Räkna om
  </button>
  </form>
  <?php endif; ?>

  <!-- Recalculate ALL Button -->
  <form method="POST" class="gs-mb-0" style="display: inline; margin-left: 0.5rem;">
  <?= csrf_field() ?>
  <button type="submit" name="recalculate_all" class="btn btn--primary"
  onclick="return confirm('Räkna om klubbpoäng för ALLA serier?\n\nDetta kan ta några sekunder.')">
  <i data-lucide="refresh-cw"></i>
  Räkna alla serier
  </button>
  </form>
 </div>
 </div>
 </div>

 <?php if ($selectedSeriesId && $seriesInfo): ?>
 <!-- Summary Stats -->
 <div class="grid grid-cols-4 gap-md mb-lg">
 <div class="card text-center">
  <div class="card-body">
  <div class="gs-text-3xl font-bold text-primary"><?= $totalClubs ?></div>
  <div class="text-sm text-secondary">Klubbar</div>
  </div>
 </div>
 <div class="card text-center">
  <div class="card-body">
  <div class="gs-text-3xl font-bold text-primary"><?= number_format($totalPoints) ?></div>
  <div class="text-sm text-secondary">Totala poäng</div>
  </div>
 </div>
 <div class="card text-center">
  <div class="card-body">
  <div class="gs-text-3xl font-bold text-primary"><?= $totalParticipants ?></div>
  <div class="text-sm text-secondary">Deltagare</div>
  </div>
 </div>
 <div class="card text-center">
  <div class="card-body">
  <div class="gs-text-3xl font-bold text-primary">
  <?= !empty($standings) ? $standings[0]['events_count'] : 0 ?>
  </div>
  <div class="text-sm text-secondary">Events</div>
  </div>
 </div>
 </div>

 <!-- Standings Table -->
 <div class="card">
 <div class="card-header">
  <h2 class="text-primary">
  <i data-lucide="list-ordered"></i>
  Klubbranking - <?= h($seriesInfo['name']) ?>
  </h2>
 </div>
 <div class="card-body gs-p-0">
  <?php if (empty($standings)): ?>
  <div class="text-center py-xl">
  <i data-lucide="info" class="icon-lg text-secondary mb-md"></i>
  <p class="text-secondary">Inga klubbpoäng har beräknats för denna serie ännu.</p>
  <p class="text-sm text-secondary mt-sm">
  Klicka på"Räkna om" för att beräkna klubbpoäng baserat på resultat.
  </p>
  </div>
  <?php else: ?>
  <div class="table-responsive">
  <table class="table">
  <thead>
   <tr>
   <th style="width: 60px;">Rank</th>
   <th>Klubb</th>
   <th>Ort</th>
   <th class="text-right">Poäng</th>
   <th class="text-right">Deltagare</th>
   <th class="text-right">Events</th>
   <th class="text-right">Bästa event</th>
   <th style="width: 80px;"></th>
   </tr>
  </thead>
  <tbody>
   <?php foreach ($standings as $index => $club): ?>
   <tr>
   <td>
   <?php if ($club['ranking'] <= 3): ?>
    <span class="badge badge-<?= $club['ranking'] == 1 ? 'warning' : ($club['ranking'] == 2 ? 'secondary' : 'primary') ?>">
    <?= $club['ranking'] ?>
    </span>
   <?php else: ?>
    <?= $club['ranking'] ?>
   <?php endif; ?>
   </td>
   <td>
   <div class="flex items-center gap-sm">
    <?php if ($club['logo']): ?>
    <img src="<?= h($club['logo']) ?>" alt="" style="width: 24px; height: 24px; object-fit: contain;">
    <?php endif; ?>
    <strong><?= h($club['club_name']) ?></strong>
    <?php if ($club['short_name']): ?>
    <span class="text-xs text-secondary">(<?= h($club['short_name']) ?>)</span>
    <?php endif; ?>
   </div>
   </td>
   <td class="text-secondary"><?= h($club['city'] ?? '-') ?></td>
   <td class="text-right font-bold"><?= number_format($club['total_points']) ?></td>
   <td class="text-right"><?= $club['total_participants'] ?></td>
   <td class="text-right"><?= $club['events_count'] ?></td>
   <td class="text-right"><?= number_format($club['best_event_points']) ?></td>
   <td>
   <a href="/admin/club-points-detail.php?club_id=<?= $club['club_id'] ?>&series_id=<?= $selectedSeriesId ?>"
    class="btn btn--sm btn--secondary">
    <i data-lucide="eye"></i>
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

 <?php else: ?>
 <!-- No series selected -->
 <div class="card">
 <div class="card-body text-center py-xl">
  <i data-lucide="award" class="icon-lg text-secondary mb-md"></i>
  <h3 class="mb-sm">Välj en serie</h3>
  <p class="text-secondary">
  Välj en serie ovan för att se klubbranking.
  </p>
 </div>
 </div>
 <?php endif; ?>

 <!-- Info Card -->
 <div class="card mt-lg">
 <div class="card-header">
 <h3 class="text-secondary">
  <i data-lucide="info"></i>
  Om klubbpoäng
 </h3>
 </div>
 <div class="card-body">
 <ul class="text-sm text-secondary" style="margin: 0; padding-left: 1.5rem;">
  <li>Bästa åkare från varje klubb per klass får 100% av sina poäng</li>
  <li>Näst bästa åkare från samma klubb/klass får 50%</li>
  <li>Övriga åkare från klubben i samma klass får 0%</li>
  <li>Poängen ackumuleras över alla events i serien</li>
 </ul>
 </div>
 </div>

<?php include __DIR__ . '/components/unified-layout-footer.php'; ?>
