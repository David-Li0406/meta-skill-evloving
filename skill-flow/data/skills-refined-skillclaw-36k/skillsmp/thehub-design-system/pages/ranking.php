<?php
/**
 * V3 Ranking Page - 24 month rolling ranking
 * Matches v2 structure with discipline tabs
 */

// Define page type for sponsor placements
if (!defined('HUB_PAGE_TYPE')) {
    define('HUB_PAGE_TYPE', 'ranking');
}

$db = hub_db();

// Include ranking functions - try multiple paths for V3 routing compatibility
$hasRankingSystem = false;
$possiblePaths = [
    dirname(__DIR__) . '/includes/ranking_functions.php',
    __DIR__ . '/../includes/ranking_functions.php',
    $_SERVER['DOCUMENT_ROOT'] . '/includes/ranking_functions.php',
];

foreach ($possiblePaths as $path) {
    if (file_exists($path)) {
        require_once $path;
        $hasRankingSystem = true;
        break;
    }
}

// Get selected discipline
$discipline = isset($_GET['discipline']) ? strtoupper($_GET['discipline']) : 'GRAVITY';
if (!in_array($discipline, ['ENDURO', 'DH', 'GRAVITY'])) {
    $discipline = 'GRAVITY';
}

// Get view (riders or clubs)
$view = isset($_GET['view']) ? $_GET['view'] : 'riders';
if (!in_array($view, ['riders', 'clubs'])) {
    $view = 'riders';
}

// Pagination - use 'p' to avoid conflict with routing 'page' parameter
$page = isset($_GET['p']) ? max(1, (int)$_GET['p']) : 1;
$perPage = 50;
$offset = ($page - 1) * $perPage;

$ranking = ['riders' => [], 'clubs' => [], 'total' => 0, 'snapshot_date' => null];
$error = null;

try {
    if ($hasRankingSystem && function_exists('rankingTablesExist')) {
        // Use parent getDB function if available, otherwise use hub_db()
        $parentDb = function_exists('getDB') ? getDB() : $db;

        if ($parentDb && rankingTablesExist($parentDb)) {
            if ($view === 'clubs' && function_exists('getCurrentClubRanking')) {
                $ranking = getCurrentClubRanking($parentDb, $discipline, $perPage, $offset);
            } elseif (function_exists('getCurrentRanking')) {
                $ranking = getCurrentRanking($parentDb, $discipline, $perPage, $offset);
            }
        }
    }
} catch (Exception $e) {
    $error = $e->getMessage();
}

$totalPages = max(1, ceil(($ranking['total'] ?? 0) / $perPage));
$disciplineNames = [
    'GRAVITY' => 'Gravity',
    'ENDURO' => 'Enduro',
    'DH' => 'Downhill'
];
?>

<link rel="stylesheet" href="/assets/css/pages/ranking.css?v=<?= file_exists(dirname(__DIR__) . '/assets/css/pages/ranking.css') ? filemtime(dirname(__DIR__) . '/assets/css/pages/ranking.css') : time() ?>">

<div class="page-header">
  <h1 class="page-title">
    <i data-lucide="trending-up" class="page-icon"></i>
    Ranking
  </h1>
  <p class="page-subtitle">
    GravitySeries 24 månaders rullande ranking
    <?php if (!empty($ranking['snapshot_date'])): ?>
      <span class="subtitle-meta">· Uppdaterad <?= date('j F Y', strtotime($ranking['snapshot_date'])) ?></span>
    <?php endif; ?>
  </p>
</div>

<!-- Global Sponsor: Header Banner -->
<?= render_global_sponsors('ranking', 'header_banner', '') ?>

<!-- Global Sponsor: Content Top -->
<?= render_global_sponsors('ranking', 'content_top', '') ?>

<!-- Discipline Tabs -->
<div class="discipline-tabs mb-md">
  <a href="/ranking?discipline=GRAVITY&view=<?= $view ?>"
     class="discipline-tab <?= $discipline === 'GRAVITY' ? 'active' : '' ?>">
    Gravity
  </a>
  <a href="/ranking?discipline=ENDURO&view=<?= $view ?>"
     class="discipline-tab <?= $discipline === 'ENDURO' ? 'active' : '' ?>">
    Enduro
  </a>
  <a href="/ranking?discipline=DH&view=<?= $view ?>"
     class="discipline-tab <?= $discipline === 'DH' ? 'active' : '' ?>">
    Downhill
  </a>
</div>

<!-- View Toggle - matches database page style -->
<div class="tabs-nav tabs-nav--noborder mb-lg">
  <a href="/ranking?discipline=<?= $discipline ?>&view=riders"
     class="tab-pill <?= $view === 'riders' ? 'active' : '' ?>">
    <i data-lucide="users"></i> Åkare
  </a>
  <a href="/ranking?discipline=<?= $discipline ?>&view=clubs"
     class="tab-pill <?= $view === 'clubs' ? 'active' : '' ?>">
    <i data-lucide="shield"></i> Klubbar
  </a>
</div>

<!-- Info Banner -->
<div class="info-banner mb-lg">
  <span class="info-icon"><i data-lucide="info"></i></span>
  <span>24 månaders rullande ranking. Poäng viktas efter fältstorlek och eventtyp.</span>
</div>

<?php if ($error): ?>
<div class="card mb-lg">
  <div class="card-title text-error">Fel</div>
  <p><?= htmlspecialchars($error) ?></p>
</div>
<?php endif; ?>

<?php if (!$hasRankingSystem): ?>
<div class="card text-center">
  <div class="empty-state">
    <div class="empty-state-icon"><i data-lucide="settings"></i></div>
    <h3>Rankingsystemet är inte konfigurerat</h3>
    <p class="text-muted">Kontakta administratör.</p>
  </div>
</div>
<?php elseif ($view === 'riders' && empty($ranking['riders'])): ?>
<div class="card text-center">
  <div class="empty-state">
    <div class="empty-state-icon"><i data-lucide="trophy"></i></div>
    <h3>Ingen <?= $disciplineNames[$discipline] ?>-ranking ännu</h3>
    <p class="text-muted">Rankingen uppdateras efter att resultat har registrerats.</p>
  </div>
</div>
<?php elseif ($view === 'clubs' && empty($ranking['clubs'])): ?>
<div class="card text-center">
  <div class="empty-state">
    <div class="empty-state-icon"><i data-lucide="shield"></i></div>
    <h3>Ingen klubbranking ännu</h3>
    <p class="text-muted">Klubbranking beräknas baserat på åkarnas poäng.</p>
  </div>
</div>
<?php else: ?>

<!-- Stats -->
<div class="stats-grid mb-lg">
  <div class="stat-card">
    <span class="stat-value"><?= number_format($ranking['total'] ?? 0) ?></span>
    <span class="stat-label"><?= $view === 'clubs' ? 'Klubbar' : 'Åkare' ?></span>
  </div>
  <div class="stat-card">
    <span class="stat-value">24</span>
    <span class="stat-label">Månader</span>
  </div>
</div>

<?php if ($view === 'riders' && !empty($ranking['riders'])): ?>
<!-- Riders Ranking -->
<section class="card">
  <div class="table-wrapper">
    <table class="table table--striped table--hover">
      <thead>
        <tr>
          <th class="text-center w-60">#</th>
          <th class="col-rider">Åkare</th>
          <th class="table-col-hide-portrait">Klubb</th>
          <th class="text-center table-col-hide-portrait">Events</th>
          <th class="text-right">Poäng</th>
        </tr>
      </thead>
      <tbody>
        <?php foreach ($ranking['riders'] as $rider): ?>
        <tr onclick="window.location='/rider/<?= $rider['rider_id'] ?>'" class="cursor-pointer">
          <td class="text-center">
            <?php if ($rider['ranking_position'] == 1): ?>
              <img src="/assets/icons/medal-1st.svg" alt="1:a" class="medal-icon">
            <?php elseif ($rider['ranking_position'] == 2): ?>
              <img src="/assets/icons/medal-2nd.svg" alt="2:a" class="medal-icon">
            <?php elseif ($rider['ranking_position'] == 3): ?>
              <img src="/assets/icons/medal-3rd.svg" alt="3:e" class="medal-icon">
            <?php else: ?>
              <span class="rank-number"><?= $rider['ranking_position'] ?></span>
            <?php endif; ?>
          </td>
          <td class="col-rider">
            <a href="/rider/<?= $rider['rider_id'] ?>" class="rider-link">
              <?= htmlspecialchars(($rider['firstname'] ?? '') . ' ' . ($rider['lastname'] ?? '')) ?>
            </a>
          </td>
          <td class="table-col-hide-portrait">
            <?php if (!empty($rider['club_id'])): ?>
              <a href="/club/<?= $rider['club_id'] ?>" class="club-link"><?= htmlspecialchars($rider['club_name'] ?? '-') ?></a>
            <?php else: ?>
              <span class="text-muted"><?= htmlspecialchars($rider['club_name'] ?? '-') ?></span>
            <?php endif; ?>
          </td>
          <td class="text-center table-col-hide-portrait">
            <?= $rider['events_count'] ?? 0 ?>
          </td>
          <td class="text-right">
            <span class="points-value"><?= number_format($rider['total_ranking_points'] ?? $rider['total_points'] ?? 0, 1) ?></span>
          </td>
        </tr>
        <?php endforeach; ?>
      </tbody>
    </table>
  </div>

  <!-- Mobile Card View -->
  <div class="result-list">
    <?php foreach ($ranking['riders'] as $rider): ?>
    <a href="/rider/<?= $rider['rider_id'] ?>" class="result-item">
      <div class="result-place <?= $rider['ranking_position'] <= 3 ? 'top-3' : '' ?>">
        <?php if ($rider['ranking_position'] == 1): ?>
          <img src="/assets/icons/medal-1st.svg" alt="1:a" class="medal-icon">
        <?php elseif ($rider['ranking_position'] == 2): ?>
          <img src="/assets/icons/medal-2nd.svg" alt="2:a" class="medal-icon">
        <?php elseif ($rider['ranking_position'] == 3): ?>
          <img src="/assets/icons/medal-3rd.svg" alt="3:e" class="medal-icon">
        <?php else: ?>
          <?= $rider['ranking_position'] ?>
        <?php endif; ?>
      </div>
      <div class="result-info">
        <div class="result-name"><?= htmlspecialchars(($rider['firstname'] ?? '') . ' ' . ($rider['lastname'] ?? '')) ?></div>
        <div class="result-club">
          <?= htmlspecialchars($rider['club_name'] ?? '-') ?>
          <?php if (!empty($rider['events_count'])): ?>
            • <?= $rider['events_count'] ?> events
          <?php endif; ?>
        </div>
      </div>
      <div class="result-points">
        <div class="points-big"><?= number_format($rider['total_ranking_points'] ?? $rider['total_points'] ?? 0, 1) ?></div>
        <div class="points-label">poäng</div>
      </div>
    </a>
    <?php endforeach; ?>
  </div>
</section>

<?php elseif ($view === 'clubs' && !empty($ranking['clubs'])): ?>
<!-- Clubs Ranking -->
<section class="card">
  <div class="table-wrapper">
    <table class="table table--striped table--hover">
      <thead>
        <tr>
          <th class="text-center w-60">#</th>
          <th class="col-club">Klubb</th>
          <th class="text-center table-col-hide-portrait">Åkare</th>
          <th class="text-right">Poäng</th>
        </tr>
      </thead>
      <tbody>
        <?php foreach ($ranking['clubs'] as $club): ?>
        <tr onclick="window.location='/club/<?= $club['club_id'] ?>'" class="cursor-pointer">
          <td class="text-center">
            <?php if ($club['ranking_position'] == 1): ?>
              <img src="/assets/icons/medal-1st.svg" alt="1:a" class="medal-icon">
            <?php elseif ($club['ranking_position'] == 2): ?>
              <img src="/assets/icons/medal-2nd.svg" alt="2:a" class="medal-icon">
            <?php elseif ($club['ranking_position'] == 3): ?>
              <img src="/assets/icons/medal-3rd.svg" alt="3:e" class="medal-icon">
            <?php else: ?>
              <span class="rank-number"><?= $club['ranking_position'] ?></span>
            <?php endif; ?>
          </td>
          <td class="col-club">
            <a href="/club/<?= $club['club_id'] ?>" class="club-link">
              <?= htmlspecialchars($club['club_name'] ?? '') ?>
            </a>
          </td>
          <td class="text-center table-col-hide-portrait">
            <?= $club['riders_count'] ?? 0 ?>
          </td>
          <td class="text-right">
            <span class="points-value"><?= number_format($club['total_ranking_points'] ?? 0, 1) ?></span>
          </td>
        </tr>
        <?php endforeach; ?>
      </tbody>
    </table>
  </div>

  <!-- Mobile Card View -->
  <div class="result-list">
    <?php foreach ($ranking['clubs'] as $club): ?>
    <a href="/club/<?= $club['club_id'] ?>" class="result-item">
      <div class="result-place <?= $club['ranking_position'] <= 3 ? 'top-3' : '' ?>">
        <?php if ($club['ranking_position'] == 1): ?>
          <img src="/assets/icons/medal-1st.svg" alt="1:a" class="medal-icon">
        <?php elseif ($club['ranking_position'] == 2): ?>
          <img src="/assets/icons/medal-2nd.svg" alt="2:a" class="medal-icon">
        <?php elseif ($club['ranking_position'] == 3): ?>
          <img src="/assets/icons/medal-3rd.svg" alt="3:e" class="medal-icon">
        <?php else: ?>
          <?= $club['ranking_position'] ?>
        <?php endif; ?>
      </div>
      <div class="result-info">
        <div class="result-name"><?= htmlspecialchars($club['club_name'] ?? '') ?></div>
        <div class="result-club"><?= $club['riders_count'] ?? 0 ?> åkare</div>
      </div>
      <div class="result-points">
        <div class="points-big"><?= number_format($club['total_ranking_points'] ?? 0, 1) ?></div>
        <div class="points-label">poäng</div>
      </div>
    </a>
    <?php endforeach; ?>
  </div>
</section>
<?php endif; ?>

<!-- Pagination -->
<?php if ($totalPages > 1): ?>
<nav class="pagination mt-lg" aria-label="Sidnavigering">
  <?php if ($page > 1): ?>
    <a href="/ranking?discipline=<?= $discipline ?>&view=<?= $view ?>&p=<?= $page - 1 ?>" class="btn btn--ghost">← Föregående</a>
  <?php endif; ?>

  <span class="pagination-info">Sida <?= $page ?> av <?= $totalPages ?></span>

  <?php if ($page < $totalPages): ?>
    <a href="/ranking?discipline=<?= $discipline ?>&view=<?= $view ?>&p=<?= $page + 1 ?>" class="btn btn--ghost">Nästa →</a>
  <?php endif; ?>
</nav>
<?php endif; ?>

<!-- Global Sponsor: Content Bottom -->
<?= render_global_sponsors('ranking', 'content_bottom', 'Tack till våra partners') ?>

<?php endif; ?>
