<?php
/**
 * Recalculate All Points System
 *
 * This script recalculates ALL points in the system from scratch:
 * 1. Event points (results.points) from events.point_scale_id
 * 2. Ranking points from results with multipliers
 * 3. Club points per series
 * 4. Global club ranking
 *
 * IMPORTANT: This will recalculate EVERYTHING. Make sure you have a backup!
 */

require_once __DIR__ . '/../config.php';
require_once __DIR__ . '/../includes/point-calculations.php';
require_once __DIR__ . '/../includes/ranking_functions.php';
require_once __DIR__ . '/../includes/club-points-system.php';
require_admin();

$db = getDB();

// Configuration
$dryRun = isset($_GET['dry_run']) && $_GET['dry_run'] === '1';
$step = isset($_GET['step']) ? $_GET['step'] : 'summary';

$pageTitle = 'Recalculate All Points';
$pageType = 'admin';
include __DIR__ . '/../includes/layout-header.php';
?>

<main class="main-content">
 <div class="container">
 <div class="card">
  <div class="card-header">
  <h1 class="text-primary">
   <i data-lucide="refresh-cw"></i>
   Recalculate All Points System
  </h1>
  </div>

  <div class="card-body">
  <?php if ($step === 'summary'): ?>
   <!-- Summary Page -->
   <div class="alert alert--info mb-lg">
   <i data-lucide="info"></i>
   <strong>Detta verktyg räknar om ALLA poäng i systemet från start.</strong>
   <p class="mt-sm">Det kommer att:</p>
   <ul class="gs-margin-list">
    <li><strong>Steg 1:</strong> Räkna om alla event-poäng (results.points) baserat på events.point_scale_id</li>
    <li><strong>Steg 2:</strong> Räkna om alla rankingpoäng baserat på results.points med multiplikatorer</li>
    <li><strong>Steg 3:</strong> Räkna om klubbpoäng per serie</li>
    <li><strong>Steg 4:</strong> Räkna om global klubbranking</li>
   </ul>
   </div>

   <?php
   // Get statistics
   $stats = [
   'total_events' => $db->getRow("SELECT COUNT(*) as cnt FROM events WHERE active = 1")['cnt'] ?? 0,
   'total_results' => $db->getRow("SELECT COUNT(*) as cnt FROM results")['cnt'] ?? 0,
   'total_riders' => $db->getRow("SELECT COUNT(DISTINCT cyclist_id) as cnt FROM results")['cnt'] ?? 0,
   'total_series' => $db->getRow("SELECT COUNT(*) as cnt FROM series WHERE active = 1")['cnt'] ?? 0,
   'total_clubs' => $db->getRow("SELECT COUNT(*) as cnt FROM clubs WHERE active = 1")['cnt'] ?? 0,
   ];
   ?>

   <div class="gs-stats-grid mb-lg">
   <div class="stat-card">
    <div class="stat-value"><?= number_format($stats['total_events']) ?></div>
    <div class="stat-label">Active Events</div>
   </div>
   <div class="stat-card">
    <div class="stat-value"><?= number_format($stats['total_results']) ?></div>
    <div class="stat-label">Total Results</div>
   </div>
   <div class="stat-card">
    <div class="stat-value"><?= number_format($stats['total_riders']) ?></div>
    <div class="stat-label">Active Riders</div>
   </div>
   <div class="stat-card">
    <div class="stat-value"><?= number_format($stats['total_series']) ?></div>
    <div class="stat-label">Active Series</div>
   </div>
   <div class="stat-card">
    <div class="stat-value"><?= number_format($stats['total_clubs']) ?></div>
    <div class="stat-label">Active Clubs</div>
   </div>
   </div>

   <div class="alert alert--warning mb-lg">
   <i data-lucide="alert-triangle"></i>
   <strong>Varning!</strong>
   <ul class="gs-margin-list">
    <li>Detta kommer att ändra alla poäng i databasen</li>
    <li>Processen kan ta flera minuter</li>
    <li>Se till att du har en backup av databasen</li>
   </ul>
   </div>

   <div class="flex gap-md mt-lg">
   <a href="?step=1&dry_run=1" class="btn btn--secondary">
    <i data-lucide="eye"></i>
    Dry Run (No Changes)
   </a>
   <a href="?step=1" class="btn btn--primary"
    onclick="return confirm('Är du säker på att du vill räkna om ALLA poäng?\n\nDetta kan inte ångras.');">
    <i data-lucide="refresh-cw"></i>
    Start Recalculation
   </a>
   </div>

  <?php elseif ($step === '1'): ?>
   <!-- Step 1: Recalculate Event Points -->
   <h2 class="mb-md">Steg 1: Räkna om Event-poäng (results.points)</h2>

   <?php if ($dryRun): ?>
   <div class="alert alert--info mb-md">
    <i data-lucide="eye"></i>
    <strong>DRY RUN MODE</strong> - Inga ändringar görs i databasen
   </div>
   <?php endif; ?>

   <div class="gs-progress-log" style="background: #f5f5f5; padding: 1rem; border-radius: 8px; max-height: 600px; overflow-y: auto; font-family: monospace; font-size: 0.9rem;">
   <?php
   $startTime = microtime(true);
   $stats = [
    'events_processed' => 0,
    'results_updated' => 0,
    'points_changed' => 0,
    'errors' => []
   ];

   echo"<p>⏳ Fetching all events...</p>";
   flush();

   // Get all events with results
   $events = $db->getAll("
    SELECT e.id, e.name, e.date, e.point_scale_id, e.event_format,
     COUNT(r.id) as result_count
    FROM events e
    LEFT JOIN results r ON e.id = r.event_id
    WHERE e.active = 1
    GROUP BY e.id
    HAVING result_count > 0
    ORDER BY e.date DESC
   ");

   echo"<p>✅ Found" . count($events) ." events with results</p>";
   echo"<hr>";
   flush();

   foreach ($events as $event) {
    echo"<p><strong>{$event['name']}</strong> ({$event['date']}) - {$event['result_count']} results</p>";
    flush();

    try {
    $eventFormat = $event['event_format'] ?? 'ENDURO';
    $isDH = in_array($eventFormat, ['DH_STANDARD', 'DH_SWECUP']);

    if ($dryRun) {
     echo" → DRY RUN: Would recalculate {$event['result_count']} results<br>";
    } else {
     if ($isDH) {
     $useSweCup = ($eventFormat === 'DH_SWECUP');
     $result = recalculateDHEventResults($db, $event['id'], null, $useSweCup);
     } else {
     $result = recalculateEventResults($db, $event['id'], null);
     }

     $stats['results_updated'] += $result['points_updated'] ?? 0;
     $stats['points_changed'] += $result['points_updated'] ?? 0;

     echo" → ✅ Updated {$result['points_updated']} results<br>";

     if (!empty($result['errors'])) {
     echo" → ⚠️" . count($result['errors']) ." errors<br>";
     $stats['errors'] = array_merge($stats['errors'], $result['errors']);
     }
    }

    $stats['events_processed']++;
    } catch (Exception $e) {
    echo" → ❌ Error:" . $e->getMessage() ."<br>";
    $stats['errors'][] ="Event {$event['id']}:" . $e->getMessage();
    }

    flush();
   }

   $elapsed = round(microtime(true) - $startTime, 2);

   echo"<hr>";
   echo"<p><strong>📊 Summary:</strong></p>";
   echo"<ul>";
   echo"<li>Events processed: {$stats['events_processed']}</li>";
   echo"<li>Results updated: {$stats['results_updated']}</li>";
   echo"<li>Points changed: {$stats['points_changed']}</li>";
   echo"<li>Errors:" . count($stats['errors']) ."</li>";
   echo"<li>Time: {$elapsed}s</li>";
   echo"</ul>";

   if (!empty($stats['errors'])) {
    echo"<p><strong>⚠️ Errors:</strong></p>";
    echo"<ul>";
    foreach (array_slice($stats['errors'], 0, 20) as $error) {
    echo"<li>" . htmlspecialchars($error) ."</li>";
    }
    if (count($stats['errors']) > 20) {
    echo"<li>... and" . (count($stats['errors']) - 20) ." more errors</li>";
    }
    echo"</ul>";
   }
   ?>
   </div>

   <div class="flex gap-md mt-lg">
   <a href="?step=summary" class="btn btn--secondary">
    <i data-lucide="arrow-left"></i>
    Back
   </a>
   <?php if (!$dryRun): ?>
    <a href="?step=2" class="btn btn--primary">
    <i data-lucide="arrow-right"></i>
    Next: Recalculate Ranking Points
    </a>
   <?php endif; ?>
   </div>

  <?php elseif ($step === '2'): ?>
   <!-- Step 2: Recalculate Ranking Points -->
   <h2 class="mb-md">Steg 2: Räkna om Rankingpoäng och Populera ranking_points</h2>

   <div class="alert alert--info mb-md">
   <i data-lucide="info"></i>
   Detta steg kommer att:
   <ul class="gs-margin-list">
    <li>Populera ranking_points tabellen med viktade poäng</li>
    <li>Beräkna fältstorlek, event-nivå och tidsviktning</li>
    <li>Spara alla multipliers för visning</li>
    <li>Uppdatera ranking-snapshots</li>
   </ul>
   </div>

   <div class="gs-progress-log" style="background: #f5f5f5; padding: 1rem; border-radius: 8px; max-height: 600px; overflow-y: auto; font-family: monospace; font-size: 0.9rem;">
   <?php
   $startTime = microtime(true);

   echo"<h3>A) Populera ranking_points tabell</h3>";
   flush();

   try {
    $populateStats = populateRankingPoints($db, true);

    echo"<hr>";
    echo"<h3>B) Uppdatera ranking-snapshots</h3>";
    flush();

    $rankingStats = runFullRankingUpdate($db, true);

    echo"<hr>";
    echo"<p><strong>📊 Ranking Update Summary:</strong></p>";
    echo"<ul>";
    echo"<li>Ranking points populated: {$populateStats['total_inserted']}</li>";
    echo"<li>ENDURO: {$rankingStats['enduro']['riders']} riders, {$rankingStats['enduro']['clubs']} clubs</li>";
    echo"<li>DH: {$rankingStats['dh']['riders']} riders, {$rankingStats['dh']['clubs']} clubs</li>";
    echo"<li>GRAVITY: {$rankingStats['gravity']['riders']} riders, {$rankingStats['gravity']['clubs']} clubs</li>";
    echo"<li>Total time:" . round(microtime(true) - $startTime, 2) ."s</li>";
    echo"</ul>";
   } catch (Exception $e) {
    echo"<p class='error'>❌ Error:" . htmlspecialchars($e->getMessage()) ."</p>";
    echo"<p>Stack trace:</p>";
    echo"<pre style='font-size: 0.8rem; overflow-x: auto;'>" . htmlspecialchars($e->getTraceAsString()) ."</pre>";
   }

   $elapsed = round(microtime(true) - $startTime, 2);
   echo"<p>⏱️ Step completed in {$elapsed}s</p>";
   ?>
   </div>

   <div class="flex gap-md mt-lg">
   <a href="?step=1" class="btn btn--secondary">
    <i data-lucide="arrow-left"></i>
    Back
   </a>
   <a href="?step=3" class="btn btn--primary">
    <i data-lucide="arrow-right"></i>
    Next: Recalculate Club Points
   </a>
   </div>

  <?php elseif ($step === '3'): ?>
   <!-- Step 3: Recalculate Club Points per Series -->
   <h2 class="mb-md">Steg 3: Räkna om Klubbpoäng per Serie</h2>

   <div class="gs-progress-log" style="background: #f5f5f5; padding: 1rem; border-radius: 8px; max-height: 600px; overflow-y: auto; font-family: monospace; font-size: 0.9rem;">
   <?php
   $startTime = microtime(true);

   echo"<p>⏳ Fetching all active series...</p>";
   flush();

   $series = $db->getAll("SELECT id, name FROM series WHERE active = 1 ORDER BY year DESC, name");
   echo"<p>✅ Found" . count($series) ." active series</p>";
   echo"<hr>";
   flush();

   $totalUpdated = 0;

   foreach ($series as $s) {
    echo"<p><strong>{$s['name']}</strong></p>";
    flush();

    try {
    // Clear existing club points for this series
    $db->query("DELETE FROM club_standings_cache WHERE series_id = ?", [$s['id']]);
    $db->query("DELETE FROM club_event_points WHERE series_id = ?", [$s['id']]);
    $db->query("DELETE FROM club_rider_points WHERE series_id = ?", [$s['id']]);

    // Get all events in this series
    $seriesEvents = $db->getAll("
     SELECT DISTINCT e.id
     FROM events e
     LEFT JOIN series_events se ON e.id = se.event_id
     WHERE (e.series_id = ? OR se.series_id = ?)
     AND e.active = 1
    ", [$s['id'], $s['id']]);

    echo" → Found" . count($seriesEvents) ." events in series<br>";

    // Recalculate club points for each event
    foreach ($seriesEvents as $evt) {
     if (function_exists('calculateClubPointsForEvent')) {
     calculateClubPointsForEvent($db, $evt['id'], $s['id']);
     }
    }

    // Update series standings cache
    if (function_exists('updateSeriesStandingsCache')) {
     $updated = updateSeriesStandingsCache($db, $s['id']);
     echo" → ✅ Updated {$updated} club standings<br>";
     $totalUpdated += $updated;
    }

    } catch (Exception $e) {
    echo" → ❌ Error:" . $e->getMessage() ."<br>";
    }

    flush();
   }

   $elapsed = round(microtime(true) - $startTime, 2);
   echo"<hr>";
   echo"<p><strong>📊 Summary:</strong></p>";
   echo"<ul>";
   echo"<li>Series processed:" . count($series) ."</li>";
   echo"<li>Club standings updated: {$totalUpdated}</li>";
   echo"<li>Time: {$elapsed}s</li>";
   echo"</ul>";
   ?>
   </div>

   <div class="flex gap-md mt-lg">
   <a href="?step=2" class="btn btn--secondary">
    <i data-lucide="arrow-left"></i>
    Back
   </a>
   <a href="?step=complete" class="btn btn-success">
    <i data-lucide="check"></i>
    Complete
   </a>
   </div>

  <?php elseif ($step === 'complete'): ?>
   <!-- Completion Page -->
   <div class="alert alert--success mb-lg">
   <i data-lucide="check-circle"></i>
   <strong>✅ All points have been recalculated successfully!</strong>
   </div>

   <h2 class="mb-md">What was updated:</h2>
   <ul class="gs-list">
   <li>✅ All event points (results.points) recalculated from event point scales</li>
   <li>✅ All ranking points recalculated with field and time multipliers</li>
   <li>✅ All club points per series recalculated</li>
   <li>✅ Global club ranking updated</li>
   </ul>

   <div class="flex gap-md mt-lg">
   <a href="/admin/results.php" class="btn btn--secondary">
    <i data-lucide="list"></i>
    View Results
   </a>
   <a href="/ranking/" class="btn btn--secondary">
    <i data-lucide="trophy"></i>
    View Ranking
   </a>
   <a href="/admin/series.php" class="btn btn--secondary">
    <i data-lucide="award"></i>
    View Series
   </a>
   <a href="?step=summary" class="btn btn--primary">
    <i data-lucide="refresh-cw"></i>
    Run Again
   </a>
   </div>

  <?php endif; ?>
  </div>
 </div>
 </div>
</main>

<script src="https://unpkg.com/lucide@latest"></script>
<script>
 lucide.createIcons();

 // Auto-scroll to bottom of log
 const log = document.querySelector('.gs-progress-log');
 if (log) {
 log.scrollTop = log.scrollHeight;
 }
</script>

<?php include __DIR__ . '/../includes/layout-footer.php'; ?>
