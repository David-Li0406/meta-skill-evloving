<?php
/**
 * Fix Event Levels
 *
 * This script corrects event_level on events to ensure proper ranking point multipliers:
 * - SweCup events = national (1.0 multiplier)
 * - GravitySeries events = national (1.0 multiplier)
 * - Capital Enduro events = sportmotion (0.5 multiplier)
 * - Other regional events = sportmotion (0.5 multiplier)
 */

require_once __DIR__ . '/../config.php';
require_admin();

$db = getDB();

$pageTitle = 'Fix Event Levels';
$pageType = 'admin';
include __DIR__ . '/../includes/layout-header.php';
?>

<main class="main-content">
 <div class="container">
 <div class="card">
 <div class="card-header">
 <h1 class="text-primary">
  <i data-lucide="tag"></i>
  Fix Event Levels
 </h1>
 </div>

 <div class="card-body">
 <div class="alert alert--info mb-lg">
  <i data-lucide="info"></i>
  Detta verktyg korrigerar event_level på events för att säkerställa rätt rankingpoäng-multiplikatorer.
 </div>

 <?php
 // Show current distribution
 $current = $db->getAll("
  SELECT
  event_level,
  COUNT(*) as count
  FROM events
  WHERE discipline IN ('ENDURO', 'DH')
  GROUP BY event_level
 ");

 echo"<h3 class=' mb-md'>Nuvarande fördelning:</h3>";
 echo"<div class='gs-stats-grid mb-lg'>";
 foreach ($current as $row) {
  $level = $row['event_level'] ?? 'NULL';
  $count = $row['count'];
  echo"<div class='stat-card'>";
  echo"<div class='stat-value'>{$count}</div>";
  echo"<div class='stat-label'>{$level}</div>";
  echo"</div>";
 }
 echo"</div>";

 if (isset($_POST['fix'])) {
  echo"<h3 class=' mb-md'>Korrigerar event_level...</h3>";
  echo"<div style='background: #f5f5f5; padding: 1rem; border-radius: 8px; max-height: 400px; overflow-y: auto; font-family: monospace; font-size: 0.9rem;'>";

  // Set SweCup to national
  $swecup = $db->query("
  UPDATE events
  SET event_level = 'national'
  WHERE name LIKE '%SweCup%'
  AND discipline IN ('ENDURO', 'DH')
 ");
  echo"<p>✅ SweCup events → national</p>";
  flush();

  // Set GravitySeries to national
  $gravityseries = $db->query("
  UPDATE events
  SET event_level = 'national'
  WHERE name LIKE '%GravitySeries%'
  AND discipline IN ('ENDURO', 'DH')
 ");
  echo"<p>✅ GravitySeries events → national</p>";
  flush();

  // Set Capital Enduro to sportmotion
  $capital = $db->query("
  UPDATE events
  SET event_level = 'sportmotion'
  WHERE name LIKE '%Capital Enduro%'
  AND discipline IN ('ENDURO', 'DH')
 ");
  echo"<p>✅ Capital Enduro events → sportmotion</p>";
  flush();

  // Show updated distribution
  $updated = $db->getAll("
  SELECT
  event_level,
  COUNT(*) as count
  FROM events
  WHERE discipline IN ('ENDURO', 'DH')
  GROUP BY event_level
 ");

  echo"<hr>";
  echo"<p><strong>📊 Uppdaterad fördelning:</strong></p>";
  echo"<ul>";
  foreach ($updated as $row) {
  $level = $row['event_level'] ?? 'NULL';
  $count = $row['count'];
  echo"<li>{$level}: {$count} events</li>";
  }
  echo"</ul>";

  echo"<hr>";
  echo"<p style='color: green;'><strong>✅ Klart!</strong></p>";
  echo"<p>Nu behöver du köra om rankingpoäng-beräkningen för att uppdatera poängen:</p>";
  echo"<a href='/admin/recalculate-all-points.php?step=2' class='btn btn--primary'>Räkna om rankingpoäng →</a>";
  echo"</div>";

 } else {
  // Show what will be changed
  echo"<h3 class=' mb-md'>Föreslagna ändringar:</h3>";

  echo"<div class='mb-lg'>";
  echo"<h4 class=''>SweCup events (→ national):</h4>";
  $swecup = $db->getAll("
  SELECT id, name, date, event_level
  FROM events
  WHERE name LIKE '%SweCup%'
  AND discipline IN ('ENDURO', 'DH')
  ORDER BY date DESC
  LIMIT 10
 ");
  if (!empty($swecup)) {
  echo"<ul class='gs-list text-sm'>";
  foreach ($swecup as $event) {
  $current_level = $event['event_level'] ?? 'NULL';
  $arrow = $current_level === 'national' ? '✅' : '→ national';
  echo"<li>{$event['name']} ({$event['date']}) - {$current_level} {$arrow}</li>";
  }
  echo"</ul>";
  } else {
  echo"<p class='text-secondary'>Inga SweCup events hittades</p>";
  }
  echo"</div>";

  echo"<div class='mb-lg'>";
  echo"<h4 class=''>GravitySeries events (→ national):</h4>";
  $gs = $db->getAll("
  SELECT id, name, date, event_level
  FROM events
  WHERE name LIKE '%GravitySeries%'
  AND discipline IN ('ENDURO', 'DH')
  ORDER BY date DESC
  LIMIT 10
 ");
  if (!empty($gs)) {
  echo"<ul class='gs-list text-sm'>";
  foreach ($gs as $event) {
  $current_level = $event['event_level'] ?? 'NULL';
  $arrow = $current_level === 'national' ? '✅' : '→ national';
  echo"<li>{$event['name']} ({$event['date']}) - {$current_level} {$arrow}</li>";
  }
  echo"</ul>";
  } else {
  echo"<p class='text-secondary'>Inga GravitySeries events hittades</p>";
  }
  echo"</div>";

  echo"<div class='mb-lg'>";
  echo"<h4 class=''>Capital Enduro events (→ sportmotion):</h4>";
  $capital = $db->getAll("
  SELECT id, name, date, event_level
  FROM events
  WHERE name LIKE '%Capital Enduro%'
  AND discipline IN ('ENDURO', 'DH')
  ORDER BY date DESC
  LIMIT 10
 ");
  if (!empty($capital)) {
  echo"<ul class='gs-list text-sm'>";
  foreach ($capital as $event) {
  $current_level = $event['event_level'] ?? 'NULL';
  $arrow = $current_level === 'sportmotion' ? '✅' : '→ sportmotion';
  echo"<li>{$event['name']} ({$event['date']}) - {$current_level} {$arrow}</li>";
  }
  echo"</ul>";
  } else {
  echo"<p class='text-secondary'>Inga Capital Enduro events hittades</p>";
  }
  echo"</div>";

  echo"<div class='alert alert--warning mb-lg'>";
  echo"<i data-lucide='alert-triangle'></i>";
  echo"<strong>Viktigt:</strong> Efter att ha korrigerat event_level måste du räkna om rankingpoängen för att ändringarna ska få effekt.";
  echo"</div>";

  echo"<form method='POST'>";
  echo csrf_field();
  echo"<button type='submit' name='fix' class='btn btn--primary' onclick=\"return confirm('Korrigera event_level på alla events?')\">";
  echo"<i data-lucide='check'></i> Korrigera event_level";
  echo"</button>";
  echo"</form>";
 }
 ?>
 </div>
 </div>
 </div>
</main>

<script src="https://unpkg.com/lucide@latest"></script>
<script>
 lucide.createIcons();
</script>

<?php include __DIR__ . '/../includes/layout-footer.php'; ?>
