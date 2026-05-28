<?php
/**
 * Rider Ranking Profile Page
 * Detailed ranking information for a specific rider
 */

error_reporting(E_ALL);
ini_set('display_errors', 1);

require_once __DIR__ . '/../config.php';
require_once __DIR__ . '/../includes/ranking_functions.php';

$db = getDB();

// Get rider ID and discipline from URL
$riderId = isset($_GET['id']) ? (int)$_GET['id'] : 0;
$discipline = isset($_GET['discipline']) ? strtoupper($_GET['discipline']) : 'GRAVITY';

if (!in_array($discipline, ['ENDURO', 'DH', 'GRAVITY'])) {
 $discipline = 'GRAVITY';
}

if (!$riderId) {
 header('Location: /ranking/');
 exit;
}

// Get rider information (with club fallback to rider_club_seasons)
$rider = $db->getRow("
 SELECT r.*,
        COALESCE(c.name, c_season.name) as club_name,
        COALESCE(c.id, rcs_latest.club_id) as club_id
 FROM riders r
 LEFT JOIN clubs c ON r.club_id = c.id
 LEFT JOIN (
     SELECT rider_id, club_id
     FROM rider_club_seasons rcs1
     WHERE season_year = (SELECT MAX(season_year) FROM rider_club_seasons rcs2 WHERE rcs2.rider_id = rcs1.rider_id)
 ) rcs_latest ON rcs_latest.rider_id = r.id AND r.club_id IS NULL
 LEFT JOIN clubs c_season ON rcs_latest.club_id = c_season.id
 WHERE r.id = ?
", [$riderId]);

if (!$rider) {
 header('Location: /ranking/');
 exit;
}

// Get rider's ranking data
$riderData = calculateRankingData($db, $discipline, false);
$riderRanking = null;

foreach ($riderData as $data) {
 if ($data['rider_id'] == $riderId) {
 $riderRanking = $data;
 break;
 }
}

// Get rider's recent results (last 24 months)
$cutoffDate = date('Y-m-d', strtotime('-24 months'));
$disciplineFilter = '';
$params = [$riderId, $cutoffDate];

if ($discipline !== 'GRAVITY') {
 $disciplineFilter = 'AND e.discipline = ?';
 $params[] = $discipline;
}

$results = $db->getAll("
 SELECT
 r.points,
 r.run_1_points,
 r.run_2_points,
 e.name as event_name,
 e.date as event_date,
 e.discipline,
 e.event_level,
 cl.name as class_name
 FROM results r
 JOIN events e ON r.event_id = e.id
 JOIN classes cl ON r.class_id = cl.id
 WHERE r.cyclist_id = ?
 AND r.status = 'finished'
 AND (r.points > 0 OR COALESCE(r.run_1_points, 0) > 0 OR COALESCE(r.run_2_points, 0) > 0)
 AND e.date >= ?
 {$disciplineFilter}
 AND COALESCE(cl.series_eligible, 1) = 1
 AND COALESCE(cl.awards_points, 1) = 1
 ORDER BY e.date DESC
", $params);

$pageTitle = $rider['firstname'] . ' ' . $rider['lastname'] . ' - ' . getDisciplineDisplayName($discipline) . ' Ranking';
$pageType = 'public';
include __DIR__ . '/../includes/layout-header.php';
?>

<main class="main-content">
 <div class="container">
 <div class="gs-rider-profile-container">
  <!-- Back Button -->
  <div class="mb-md">
  <a href="/ranking/?discipline=<?= $discipline ?>&view=riders" class="btn btn--secondary btn--sm">
   <i data-lucide="arrow-left"></i> Tillbaka till ranking
  </a>
  </div>

  <!-- Rider Header -->
  <div class="gs-rider-header mb-lg">
  <div class="gs-rider-avatar">
   <i data-lucide="user" style="width: 48px; height: 48px;"></i>
  </div>
  <div class="gs-rider-header-info">
   <h1 class="text-primary gs-mb-xs">
   <?= h($rider['firstname'] . ' ' . $rider['lastname']) ?>
   </h1>
   <?php if ($rider['club_name']): ?>
   <p class="text-secondary gs-mb-xs">
    <i data-lucide="shield" style="width: 16px; height: 16px;"></i>
    <?= h($rider['club_name']) ?>
   </p>
   <?php endif; ?>
   <?php if ($rider['birth_year']): ?>
   <p class="text-secondary text-sm">
    Född <?= $rider['birth_year'] ?>
   </p>
   <?php endif; ?>
  </div>
  </div>

  <!-- Discipline Tabs -->
  <div class="gs-discipline-tabs mb-lg">
  <a href="?id=<?= $riderId ?>&discipline=GRAVITY" class="gs-discipline-tab <?= $discipline === 'GRAVITY' ? 'active' : '' ?>">
   Gravity
  </a>
  <a href="?id=<?= $riderId ?>&discipline=ENDURO" class="gs-discipline-tab <?= $discipline === 'ENDURO' ? 'active' : '' ?>">
   Enduro
  </a>
  <a href="?id=<?= $riderId ?>&discipline=DH" class="gs-discipline-tab <?= $discipline === 'DH' ? 'active' : '' ?>">
   Downhill
  </a>
  </div>

  <?php if ($riderRanking): ?>
  <!-- Ranking Stats Cards -->
  <div class="gs-stats-grid mb-lg">
   <div class="stat-card">
   <div class="gs-stat-icon">
    <i data-lucide="trophy"></i>
   </div>
   <div>
    <div class="stat-value">#<?= $riderRanking['ranking_position'] ?></div>
    <div class="stat-label">Placering</div>
   </div>
   </div>
   <div class="stat-card">
   <div class="gs-stat-icon">
    <i data-lucide="target"></i>
   </div>
   <div>
    <div class="stat-value"><?= number_format($riderRanking['total_ranking_points'], 1) ?></div>
    <div class="stat-label">Totala poäng</div>
   </div>
   </div>
   <div class="stat-card">
   <div class="gs-stat-icon">
    <i data-lucide="calendar"></i>
   </div>
   <div>
    <div class="stat-value"><?= $riderRanking['events_count'] ?></div>
    <div class="stat-label">Events</div>
   </div>
   </div>
  </div>

  <!-- Points Breakdown -->
  <div class="card mb-lg">
   <div class="card-header">
   <h2 class="text-primary">
    <i data-lucide="bar-chart-2"></i>
    Poängfördelning
   </h2>
   </div>
   <div class="card-body">
   <div class="points-breakdown-detail">
    <div class="gs-points-row">
    <span class="points-label">
     <i data-lucide="calendar-check" style="width: 16px; height: 16px;"></i>
     Senaste 12 månader (100%)
    </span>
    <span class="gs-points-value text-success"><?= number_format($riderRanking['points_12'], 1) ?></span>
    </div>
    <div class="gs-points-row">
    <span class="points-label">
     <i data-lucide="calendar" style="width: 16px; height: 16px;"></i>
     Månad 13-24 (50% vikt)
    </span>
    <span class="gs-points-value text-secondary"><?= number_format($riderRanking['points_13_24'], 1) ?></span>
    </div>
    <div class="gs-points-row">
    <span class="points-label font-bold">
     <i data-lucide="award" style="width: 16px; height: 16px;"></i>
     Viktade poäng (bidrar till ranking)
    </span>
    <span class="gs-points-value text-primary font-bold"><?= number_format($riderRanking['points_13_24'] * 0.5, 1) ?></span>
    </div>
    <hr class="gs-my-sm">
    <div class="gs-points-row gs-total">
    <span class="points-label font-bold text-lg">
     <i data-lucide="trophy" style="width: 18px; height: 18px;"></i>
     Totala rankingpoäng
    </span>
    <span class="gs-points-value text-primary font-bold text-xl"><?= number_format($riderRanking['total_ranking_points'], 1) ?></span>
    </div>
   </div>
   </div>
  </div>
  <?php else: ?>
  <div class="card text-center mb-lg">
   <div class="card-body">
   <p class="text-secondary">Ingen ranking för <?= getDisciplineDisplayName($discipline) ?> ännu</p>
   </div>
  </div>
  <?php endif; ?>

  <!-- Recent Results -->
  <div class="card">
  <div class="card-header">
   <h2 class="text-primary">
   <i data-lucide="list"></i>
   Resultat (senaste 24 mån)
   </h2>
  </div>
  <div class="card-body">
   <?php if (empty($results)): ?>
   <p class="text-secondary text-center">Inga resultat för <?= getDisciplineDisplayName($discipline) ?></p>
   <?php else: ?>
   <div class="gs-results-list">
    <?php foreach ($results as $result): ?>
    <?php
    $points = $result['run_1_points'] || $result['run_2_points']
     ? ($result['run_1_points'] + $result['run_2_points'])
     : $result['points'];
    ?>
    <div class="gs-result-item">
     <div class="gs-result-date">
     <?= date('j M Y', strtotime($result['event_date'])) ?>
     </div>
     <div class="gs-result-event">
     <div class="gs-result-event-name"><?= h($result['event_name']) ?></div>
     <div class="gs-result-meta">
      <?= h($result['class_name']) ?>
      <?php if ($result['event_level'] === 'sportmotion'): ?>
      <span class="badge badge-sm">Sportmotion</span>
      <?php endif; ?>
     </div>
     </div>
     <div class="gs-result-points">
     <?= number_format($points, 1) ?> p
     </div>
    </div>
    <?php endforeach; ?>
   </div>
   <?php endif; ?>
  </div>
  </div>
 </div>
 </div>
</main>

<style>
.gs-rider-profile-container {
 max-width: 800px;
 margin: 0 auto;
}

.gs-rider-header {
 display: flex;
 align-items: center;
 gap: var(--gs-space-lg);
 padding: var(--gs-space-lg);
 background: var(--gs-white);
 border-radius: var(--gs-radius-lg);
 box-shadow: var(--gs-shadow-sm);
}

.gs-rider-avatar {
 width: 80px;
 height: 80px;
 display: flex;
 align-items: center;
 justify-content: center;
 background: var(--primary-light);
 border-radius: var(--gs-radius-full);
 color: var(--primary);
 flex-shrink: 0;
}

.gs-rider-header-info {
 flex: 1;
}

.gs-rider-header-info p {
 display: flex;
 align-items: center;
 gap: var(--gs-space-xs);
}

.gs-rider-header-info i {
 flex-shrink: 0;
}

.stat-card {
 display: flex;
 align-items: center;
 gap: var(--space-md);
}

.gs-stat-icon {
 width: 48px;
 height: 48px;
 display: flex;
 align-items: center;
 justify-content: center;
 background: var(--primary-light);
 border-radius: var(--gs-radius-md);
 color: var(--primary);
 flex-shrink: 0;
}

.gs-stat-icon i {
 width: 24px;
 height: 24px;
}

.points-breakdown-detail {
 display: flex;
 flex-direction: column;
 gap: var(--space-sm);
}

.gs-points-row {
 display: flex;
 justify-content: space-between;
 align-items: center;
 padding: var(--space-sm);
 background: var(--gs-light);
 border-radius: var(--gs-radius-sm);
}

.gs-points-row.gs-total {
 background: var(--primary-light);
 padding: var(--space-md);
}

.points-label {
 display: flex;
 align-items: center;
 gap: var(--gs-space-xs);
 font-size: 0.9375rem;
}

.gs-points-value {
 font-size: 1.125rem;
 font-weight: 600;
}

.gs-results-list {
 display: flex;
 flex-direction: column;
 gap: var(--gs-space-xs);
}

.gs-result-item {
 display: grid;
 grid-template-columns: auto 1fr auto;
 gap: var(--space-md);
 align-items: center;
 padding: var(--space-sm) var(--space-md);
 background: var(--gs-light);
 border-radius: var(--gs-radius-sm);
}

.gs-result-date {
 font-size: 0.875rem;
 color: var(--text-secondary);
 white-space: nowrap;
}

.gs-result-event {
 min-width: 0;
}

.gs-result-event-name {
 font-weight: 600;
 font-size: 0.9375rem;
 white-space: nowrap;
 overflow: hidden;
 text-overflow: ellipsis;
}

.gs-result-meta {
 font-size: 0.75rem;
 color: var(--text-secondary);
 display: flex;
 align-items: center;
 gap: var(--gs-space-xs);
}

.gs-result-points {
 font-weight: bold;
 color: var(--primary);
 white-space: nowrap;
}

@media (max-width: 567px) {
 .gs-rider-header {
 flex-direction: column;
 text-align: center;
 }

 .gs-rider-header-info p {
 justify-content: center;
 }

 .gs-result-item {
 grid-template-columns: 1fr;
 gap: var(--gs-space-xs);
 }

 .gs-result-date {
 font-size: 0.75rem;
 }

 .gs-result-points {
 text-align: left;
 }
}
</style>

<?php include __DIR__ . '/../includes/layout-footer.php'; ?>
