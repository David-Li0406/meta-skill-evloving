<?php
/**
 * Setup Ranking System
 *
 * This script:
 * 1. Creates ranking_points table if it doesn't exist
 * 2. Populates it with weighted points from results
 * 3. Shows status and diagnostics
 */

require_once __DIR__ . '/../config.php';
require_once __DIR__ . '/../includes/ranking_functions.php';
require_admin();

$db = getDB();
$step = $_GET['step'] ?? 'check';

$pageTitle = 'Setup Ranking System';
$pageType = 'admin';
include __DIR__ . '/../includes/layout-header.php';
?>

<main class="main-content">
 <div class="container">
 <div class="card">
  <div class="card-header">
  <h1 class="text-primary">
   <i data-lucide="settings"></i>
   Setup Ranking System
  </h1>
  </div>

  <div class="card-body">
  <?php if ($step === 'check'): ?>
   <!-- Step 1: Check Status -->
   <h2 class="mb-md">Status Check</h2>

   <?php
   // Check if ranking_points table exists
   $tableExists = false;
   try {
   $db->getRow("SELECT 1 FROM ranking_points LIMIT 1");
   $tableExists = true;
   } catch (Exception $e) {
   $tableExists = false;
   }

   // Check if it has data
   $recordCount = 0;
   if ($tableExists) {
   $result = $db->getRow("SELECT COUNT(*) as cnt FROM ranking_points");
   $recordCount = $result['cnt'] ?? 0;
   }

   // Check events with event_level set
   $eventsTotal = $db->getRow("SELECT COUNT(*) as cnt FROM events WHERE discipline IN ('ENDURO', 'DH')")['cnt'] ?? 0;
   $eventsWithLevel = $db->getRow("SELECT COUNT(*) as cnt FROM events WHERE discipline IN ('ENDURO', 'DH') AND event_level IS NOT NULL")['cnt'] ?? 0;

   // Check results count
   $resultsCount = $db->getRow("
   SELECT COUNT(*) as cnt
   FROM results r
   JOIN events e ON r.event_id = e.id
   WHERE r.status = 'finished'
   AND r.points > 0
   AND e.date >= DATE_SUB(NOW(), INTERVAL 24 MONTH)
   AND e.discipline IN ('ENDURO', 'DH')
  ")['cnt'] ?? 0;
   ?>

   <div class="gs-stats-grid mb-lg">
   <div class="stat-card <?= $tableExists ? 'gs-bg-success' : 'gs-bg-danger' ?>">
    <div class="stat-value"><?= $tableExists ? '✅' : '❌' ?></div>
    <div class="stat-label">ranking_points tabell</div>
   </div>
   <div class="stat-card <?= $recordCount > 0 ? 'gs-bg-success' : 'gs-bg-warning' ?>">
    <div class="stat-value"><?= number_format($recordCount) ?></div>
    <div class="stat-label">Ranking points records</div>
   </div>
   <div class="stat-card <?= $eventsWithLevel == $eventsTotal ? 'gs-bg-success' : 'gs-bg-warning' ?>">
    <div class="stat-value"><?= $eventsWithLevel ?> / <?= $eventsTotal ?></div>
    <div class="stat-label">Events med event_level</div>
   </div>
   <div class="stat-card">
    <div class="stat-value"><?= number_format($resultsCount) ?></div>
    <div class="stat-label">Results (24 månader)</div>
   </div>
   </div>

   <?php if (!$tableExists): ?>
   <div class="alert alert-danger mb-lg">
    <i data-lucide="alert-circle"></i>
    <strong>Tabellen ranking_points finns inte!</strong>
    <p class="mt-sm">Du måste köra migrationen för att skapa tabellen.</p>
   </div>

   <h3 class="mb-md">Steg 1: Skapa tabell</h3>
   <p class="mb-md">Kör följande SQL-migration:</p>
   <pre class="gs-code-block" style="background: #f5f5f5; padding: 1rem; border-radius: 4px; overflow-x: auto;">mysql -u username -p database_name &lt; database/migrations/034_restore_ranking_points_table.sql</pre>

   <p class="mb-md"><strong>Eller</strong> kör den direkt här:</p>
   <a href="?step=create_table" class="btn btn--primary"
    onclick="return confirm('Skapa ranking_points tabell nu?');">
    <i data-lucide="database"></i>
    Skapa ranking_points tabell
   </a>

   <?php elseif ($eventsWithLevel < $eventsTotal): ?>
   <div class="alert alert--warning mb-lg">
    <i data-lucide="alert-triangle"></i>
    <strong>Vissa events saknar event_level!</strong>
    <p class="mt-sm"><?= $eventsTotal - $eventsWithLevel ?> events behöver få event_level satt (national eller sportmotion).</p>
   </div>

   <h3 class="mb-md">Steg 2: Sätt event_level på events</h3>
   <p class="mb-md">Du kan sätta event_level automatiskt baserat på event-namn:</p>

   <a href="?step=set_event_levels" class="btn btn--primary"
    onclick="return confirm('Sätta event_level automatiskt baserat på namn?');">
    <i data-lucide="tag"></i>
    Sätt event_level automatiskt
   </a>

   <?php elseif ($recordCount == 0): ?>
   <div class="alert alert--warning mb-lg">
    <i data-lucide="alert-triangle"></i>
    <strong>ranking_points tabellen är tom!</strong>
    <p class="mt-sm">Du måste populera tabellen med viktade poäng från results.</p>
   </div>

   <h3 class="mb-md">Steg 3: Populera ranking_points</h3>
   <p class="mb-md">Detta kommer att beräkna viktade poäng för alla results från senaste 24 månaderna.</p>

   <a href="?step=populate" class="btn btn--primary"
    onclick="return confirm('Populera ranking_points nu?\n\nDetta kan ta några minuter.');">
    <i data-lucide="refresh-cw"></i>
    Populera ranking_points
   </a>

   <?php else: ?>
   <div class="alert alert--success mb-lg">
    <i data-lucide="check-circle"></i>
    <strong>✅ Ranking-systemet är konfigurerat!</strong>
    <p class="mt-sm">Allt ser bra ut. Viktade poäng visas nu på rider-profiler.</p>
   </div>

   <h3 class="mb-md">Underhåll</h3>
   <p class="mb-md">För att räkna om alla ranking-poäng (t.ex. efter import av nya results):</p>

   <a href="?step=populate" class="btn btn--secondary">
    <i data-lucide="refresh-cw"></i>
    Räkna om ranking_points
   </a>
   <?php endif; ?>

  <?php elseif ($step === 'create_table'): ?>
   <!-- Step: Create Table -->
   <h2 class="mb-md">Skapa ranking_points tabell</h2>

   <div class="gs-progress-log" style="background: #f5f5f5; padding: 1rem; border-radius: 8px; max-height: 400px; overflow-y: auto; font-family: monospace; font-size: 0.9rem;">
   <?php
   try {
    echo"<p>📦 Läser migration-fil...</p>";
    $migrationFile = __DIR__ . '/../database/migrations/034_restore_ranking_points_table.sql';

    if (!file_exists($migrationFile)) {
    throw new Exception("Migration-filen finns inte: {$migrationFile}");
    }

    $sql = file_get_contents($migrationFile);

    echo"<p>⏳ Kör migration...</p>";
    flush();

    // Split by semicolons and execute each statement
    $statements = array_filter(array_map('trim', explode(';', $sql)));

    foreach ($statements as $statement) {
    if (empty($statement) || strpos($statement, '--') === 0) {
     continue;
    }
    $db->query($statement);
    }

    echo"<p style='color: green;'>✅ Tabell skapad!</p>";
    echo"<p><a href='?step=check' class='btn btn--primary'>Fortsätt →</a></p>";

   } catch (Exception $e) {
    echo"<p style='color: red;'>❌ Fel:" . htmlspecialchars($e->getMessage()) ."</p>";
    echo"<p><a href='?step=check' class='btn btn--secondary'>← Tillbaka</a></p>";
   }
   ?>
   </div>

  <?php elseif ($step === 'set_event_levels'): ?>
   <!-- Step: Set Event Levels -->
   <h2 class="mb-md">Sätt event_level på events</h2>

   <div class="gs-progress-log" style="background: #f5f5f5; padding: 1rem; border-radius: 8px; max-height: 400px; overflow-y: auto; font-family: monospace; font-size: 0.9rem;">
   <?php
   try {
    echo"<p>⏳ Sätter event_level baserat på namn...</p>";
    flush();

    // Set SweCup and GravitySeries to national
    $national = $db->query("
    UPDATE events
    SET event_level = 'national'
    WHERE (name LIKE '%SweCup%' OR name LIKE '%GravitySeries%')
    AND discipline IN ('ENDURO', 'DH')
   ");

    echo"<p>✅ Satte 'national' på SweCup och GravitySeries events</p>";

    // Set others to sportmotion (or national - adjust based on policy)
    $sportmotion = $db->query("
    UPDATE events
    SET event_level = 'national'
    WHERE event_level IS NULL
    AND discipline IN ('ENDURO', 'DH')
   ");

    echo"<p>✅ Satte 'national' på övriga events (ändra till sportmotion om nödvändigt)</p>";
    echo"<hr>";
    echo"<p style='color: green;'><strong>✅ Klart!</strong></p>";
    echo"<p><a href='?step=check' class='btn btn--primary'>Fortsätt →</a></p>";

   } catch (Exception $e) {
    echo"<p style='color: red;'>❌ Fel:" . htmlspecialchars($e->getMessage()) ."</p>";
    echo"<p><a href='?step=check' class='btn btn--secondary'>← Tillbaka</a></p>";
   }
   ?>
   </div>

  <?php elseif ($step === 'populate'): ?>
   <!-- Step: Populate ranking_points -->
   <h2 class="mb-md">Populera ranking_points</h2>

   <div class="gs-progress-log" style="background: #f5f5f5; padding: 1rem; border-radius: 8px; max-height: 600px; overflow-y: auto; font-family: monospace; font-size: 0.9rem;">
   <?php
   try {
    $stats = populateRankingPoints($db, true);

    echo"<hr>";
    echo"<p style='color: green;'><strong>✅ Klart!</strong></p>";
    echo"<ul>";
    echo"<li>Results processed: {$stats['total_processed']}</li>";
    echo"<li>Records inserted: {$stats['total_inserted']}</li>";
    echo"<li>Errors:" . count($stats['errors']) ."</li>";
    echo"<li>Time: {$stats['elapsed_time']}s</li>";
    echo"</ul>";

    if (!empty($stats['errors'])) {
    echo"<p><strong>⚠️ Errors:</strong></p>";
    echo"<ul>";
    foreach (array_slice($stats['errors'], 0, 10) as $error) {
     echo"<li>" . htmlspecialchars($error) ."</li>";
    }
    if (count($stats['errors']) > 10) {
     echo"<li>... and" . (count($stats['errors']) - 10) ." more</li>";
    }
    echo"</ul>";
    }

    echo"<p class='mt-lg'><a href='?step=check' class='btn btn-success'>Klar! Visa status →</a></p>";

   } catch (Exception $e) {
    echo"<p style='color: red;'>❌ Fel:" . htmlspecialchars($e->getMessage()) ."</p>";
    echo"<pre>" . htmlspecialchars($e->getTraceAsString()) ."</pre>";
    echo"<p><a href='?step=check' class='btn btn--secondary'>← Tillbaka</a></p>";
   }
   ?>
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
 setInterval(() => {
  log.scrollTop = log.scrollHeight;
 }, 500);
 }
</script>

<?php include __DIR__ . '/../includes/layout-footer.php'; ?>
