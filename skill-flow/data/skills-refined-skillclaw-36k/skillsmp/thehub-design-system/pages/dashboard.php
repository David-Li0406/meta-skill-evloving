<?php
/**
 * V3 Dashboard - Overview with real data
 */

// Load filter setting from admin configuration
$publicSettings = @include(HUB_ROOT . '/config/public_settings.php');
$filter = $publicSettings['public_riders_display'] ?? 'all';

try {
    $db = hub_db();

    // Get overall stats - respects admin filter setting
    if ($filter === 'with_results') {
        $stats = [
            'total_riders' => $db->query("
                SELECT COUNT(DISTINCT r.id)
                FROM riders r
                INNER JOIN results res ON r.id = res.cyclist_id
            ")->fetchColumn() ?: 0,
            'total_clubs' => $db->query("
                SELECT COUNT(DISTINCT c.id)
                FROM clubs c
                INNER JOIN riders r ON c.id = r.club_id
                INNER JOIN results res ON r.id = res.cyclist_id
            ")->fetchColumn() ?: 0,
            'total_events' => $db->query("SELECT COUNT(DISTINCT event_id) FROM results")->fetchColumn() ?: 0,
            'total_results' => $db->query("SELECT COUNT(*) FROM results")->fetchColumn() ?: 0,
        ];
    } else {
        $stats = [
            'total_riders' => $db->query("SELECT COUNT(*) FROM riders WHERE active = 1")->fetchColumn() ?: 0,
            'total_clubs' => $db->query("SELECT COUNT(*) FROM clubs WHERE active = 1")->fetchColumn() ?: 0,
            'total_events' => $db->query("SELECT COUNT(*) FROM events")->fetchColumn() ?: 0,
            'total_results' => $db->query("SELECT COUNT(*) FROM results")->fetchColumn() ?: 0,
        ];
    }

    // Get active series
    $activeSeries = $db->query("
        SELECT s.id, s.name, s.year, COUNT(DISTINCT e.id) as event_count
        FROM series s
        LEFT JOIN events e ON s.id = e.series_id
        WHERE s.status = 'active'
        GROUP BY s.id
        ORDER BY s.year DESC
        LIMIT 5
    ")->fetchAll(PDO::FETCH_ASSOC) ?: [];

    // Get top riders
    $topRiders = $db->query("
        SELECT c.id, c.firstname, c.lastname, COUNT(r.id) as race_count
        FROM riders c
        INNER JOIN results r ON c.id = r.cyclist_id
        WHERE c.active = 1
        GROUP BY c.id
        ORDER BY race_count DESC
        LIMIT 5
    ")->fetchAll(PDO::FETCH_ASSOC) ?: [];

} catch (Exception $e) {
    $stats = ['total_riders' => 0, 'total_clubs' => 0, 'total_events' => 0, 'total_results' => 0];
    $activeSeries = [];
    $topRiders = [];
    $error = $e->getMessage();
}
?>

<h1 class="text-2xl font-bold mb-lg">Dashboard</h1>

<?php if (isset($error)): ?>
<div class="card mb-lg bg-error">
  <p class="text-error">Databasfel: <?= htmlspecialchars($error) ?></p>
</div>
<?php endif; ?>

<div class="page-grid">
  <!-- Quick Navigation -->
  <section class="card grid-full">
    <h2 class="card-title mb-md">Snabblänkar</h2>
    <div class="flex flex-wrap gap-sm">
      <a href="/riders" class="btn btn--primary"><i data-lucide="users" class="icon-sm"></i> Åkare</a>
      <a href="/clubs" class="btn btn--primary"><i data-lucide="shield" class="icon-sm"></i> Klubbar</a>
      <a href="/results" class="btn btn--primary"><i data-lucide="flag" class="icon-sm"></i> Resultat</a>
      <a href="/series" class="btn btn--primary"><i data-lucide="trophy" class="icon-sm"></i> Serier</a>
    </div>
  </section>

  <!-- Stats Overview -->
  <section class="card grid-full" aria-labelledby="stats-title">
    <h2 id="stats-title" class="card-title mb-md">Översikt</h2>
    <div class="stats-row">
      <div class="stat-block">
        <div class="stat-value"><?= number_format($stats['total_riders']) ?></div>
        <div class="stat-label">Åkare</div>
      </div>
      <div class="stat-block">
        <div class="stat-value"><?= number_format($stats['total_clubs']) ?></div>
        <div class="stat-label">Klubbar</div>
      </div>
      <div class="stat-block">
        <div class="stat-value"><?= number_format($stats['total_events']) ?></div>
        <div class="stat-label">Event</div>
      </div>
      <div class="stat-block">
        <div class="stat-value"><?= number_format($stats['total_results']) ?></div>
        <div class="stat-label">Resultat</div>
      </div>
    </div>
  </section>

  <!-- Active Series -->
  <section class="card" aria-labelledby="series-title">
    <div class="card-header">
      <h2 id="series-title" class="card-title">Aktiva serier</h2>
      <a href="/series" class="btn btn--ghost text-sm">Alla →</a>
    </div>
    <?php if (empty($activeSeries)): ?>
    <p class="text-muted p-md">Inga aktiva serier</p>
    <?php else: ?>
    <div class="table-wrapper">
      <table class="table table--compact">
        <thead>
          <tr>
            <th scope="col">Serie</th>
            <th scope="col" class="text-right">År</th>
            <th scope="col" class="text-right">Event</th>
          </tr>
        </thead>
        <tbody>
          <?php foreach ($activeSeries as $series): ?>
          <tr>
            <td><?= htmlspecialchars($series['name']) ?></td>
            <td class="text-right"><?= $series['year'] ?></td>
            <td class="text-right"><?= $series['event_count'] ?></td>
          </tr>
          <?php endforeach; ?>
        </tbody>
      </table>
    </div>
    <?php endif; ?>
  </section>

  <!-- Top Riders -->
  <section class="card" aria-labelledby="riders-title">
    <div class="card-header">
      <h2 id="riders-title" class="card-title">Mest aktiva åkare</h2>
      <a href="/riders" class="btn btn--ghost text-sm">Alla →</a>
    </div>
    <?php if (empty($topRiders)): ?>
    <p class="text-muted p-md">Inga åkare med resultat</p>
    <?php else: ?>
    <div class="table-wrapper">
      <table class="table table--compact table--clickable">
        <thead>
          <tr>
            <th scope="col">Åkare</th>
            <th scope="col" class="text-right">Starter</th>
          </tr>
        </thead>
        <tbody>
          <?php foreach ($topRiders as $rider): ?>
          <tr data-href="/rider/<?= $rider['id'] ?>">
            <td><?= htmlspecialchars($rider['firstname'] . ' ' . $rider['lastname']) ?></td>
            <td class="text-right"><?= $rider['race_count'] ?></td>
          </tr>
          <?php endforeach; ?>
        </tbody>
      </table>
    </div>
    <?php endif; ?>
  </section>
</div>
