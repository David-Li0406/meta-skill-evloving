<?php
/**
 * TheHUB Admin - Rebuild Rider Statistics
 *
 * Placera i: /admin/rebuild-stats.php
 */

require_once __DIR__ . '/../config.php';
require_admin();

require_once __DIR__ . '/../includes/rebuild-rider-stats.php';

$db = getDB();
$pdo = $db->getPdo();

$message = null;
$messageType = null;
$results = null;

// Hantera form submissions
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    checkCsrf();

    $action = $_POST['action'] ?? '';

    switch ($action) {
        case 'migrate':
            // Kör databasmigration
            $results = runStatsMigration($pdo);
            $message = 'Migration slutförd!';
            $messageType = 'success';
            break;

        case 'rebuild_single':
            // Bygg om en enskild åkare
            $riderId = (int)$_POST['rider_id'];
            if ($riderId > 0) {
                // First, run debug to see what would be found
                $debugResults = debugRiderAchievements($pdo, $riderId);

                $results = rebuildRiderStats($pdo, $riderId);
                if (isset($results['success']) && $results['success']) {
                    $message = "Statistik uppdaterad för åkare #$riderId ({$results['achievements_added']} achievements)";
                    $messageType = 'success';
                    // Add debug info to results
                    $results['debug'] = $debugResults;
                } else {
                    $message = "Fel: " . implode(', ', $results['errors'] ?? ['Okänt fel']);
                    $messageType = 'error';
                }
            }
            break;

        case 'rebuild_all':
            // Bygg om ALLA åkare (kan ta tid!)
            set_time_limit(300); // 5 minuter
            $results = rebuildAllRiderStats($pdo);
            $message = sprintf(
                'Rebuild klar! %d åkare processade på %.1f sekunder. %d misslyckades.',
                $results['processed'],
                $results['duration_seconds'],
                $results['failed']
            );
            $messageType = $results['failed'] > 0 ? 'warning' : 'success';
            break;

        case 'update_leaders':
            // Uppdatera endast serieledare
            updateCurrentSeriesLeaders($pdo);
            $message = 'Serieledare uppdaterade!';
            $messageType = 'success';
            break;
    }
}

// Hämta statistik för dashboard
$stats = [
    'total_riders' => 0,
    'riders_with_results' => 0,
    'total_achievements' => 0,
    'total_results' => 0,
    'last_rebuild' => null
];

try {
    $stats['total_riders'] = $db->getValue("SELECT COUNT(*) FROM riders") ?: 0;
    $stats['riders_with_results'] = $db->getValue("SELECT COUNT(DISTINCT cyclist_id) FROM results") ?: 0;

    // Check if rider_achievements table exists
    try {
        $stats['total_achievements'] = $db->getValue("SELECT COUNT(*) FROM rider_achievements") ?: 0;
    } catch (Exception $e) {
        $stats['total_achievements'] = 0;
    }

    $stats['total_results'] = $db->getValue("SELECT COUNT(*) FROM results") ?: 0;

    // Check if stats_updated_at column exists
    try {
        $stats['last_rebuild'] = $db->getValue("SELECT MAX(stats_updated_at) FROM riders");
    } catch (Exception $e) {
        $stats['last_rebuild'] = null;
    }
} catch (Exception $e) {
    // Ignore errors
}

/**
 * Kör databasmigration direkt
 */
function runStatsMigration($pdo) {
    $migrations = [
        // Achievements tabell
        "CREATE TABLE IF NOT EXISTS rider_achievements (
            id INT AUTO_INCREMENT PRIMARY KEY,
            rider_id INT NOT NULL,
            achievement_type VARCHAR(50) NOT NULL,
            achievement_value VARCHAR(100) DEFAULT NULL,
            series_id INT DEFAULT NULL,
            season_year INT DEFAULT NULL,
            earned_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            INDEX idx_rider (rider_id),
            INDEX idx_type (achievement_type),
            INDEX idx_season (season_year)
        )",

        // Sociala profiler
        "ALTER TABLE riders ADD COLUMN social_instagram VARCHAR(100) DEFAULT NULL",
        "ALTER TABLE riders ADD COLUMN social_facebook VARCHAR(255) DEFAULT NULL",
        "ALTER TABLE riders ADD COLUMN social_strava VARCHAR(50) DEFAULT NULL",
        "ALTER TABLE riders ADD COLUMN social_youtube VARCHAR(100) DEFAULT NULL",
        "ALTER TABLE riders ADD COLUMN social_tiktok VARCHAR(100) DEFAULT NULL",

        // Cached stats
        "ALTER TABLE riders ADD COLUMN stats_total_starts INT DEFAULT 0",
        "ALTER TABLE riders ADD COLUMN stats_total_finished INT DEFAULT 0",
        "ALTER TABLE riders ADD COLUMN stats_total_wins INT DEFAULT 0",
        "ALTER TABLE riders ADD COLUMN stats_total_podiums INT DEFAULT 0",
        "ALTER TABLE riders ADD COLUMN stats_total_points INT DEFAULT 0",
        "ALTER TABLE riders ADD COLUMN stats_updated_at DATETIME DEFAULT NULL",

        // Experience
        "ALTER TABLE riders ADD COLUMN first_season INT DEFAULT NULL",
        "ALTER TABLE riders ADD COLUMN experience_level INT DEFAULT 1"
    ];

    $results = [];
    foreach ($migrations as $sql) {
        try {
            $pdo->exec($sql);
            $results[] = ['sql' => substr($sql, 0, 60) . '...', 'status' => 'OK'];
        } catch (PDOException $e) {
            // Ignorera "column already exists" fel
            if (strpos($e->getMessage(), 'Duplicate column') === false &&
                strpos($e->getMessage(), 'already exists') === false) {
                $results[] = ['sql' => substr($sql, 0, 60) . '...', 'status' => 'ERROR: ' . $e->getMessage()];
            } else {
                $results[] = ['sql' => substr($sql, 0, 60) . '...', 'status' => 'SKIPPED (exists)'];
            }
        }
    }

    return $results;
}

/**
 * Debug function to show what achievements would be found for a rider
 */
function debugRiderAchievements($pdo, $rider_id) {
    $debug = [
        'series_championships' => [],
        'swedish_championships' => [],
        'series_data' => [],
        'podiums' => ['gold' => 0, 'silver' => 0, 'bronze' => 0]
    ];

    $currentYear = (int)date('Y');

    // Check if series_events junction table exists
    $stmt = $pdo->query("SHOW TABLES LIKE 'series_events'");
    $useSeriesEvents = $stmt->fetch() !== false;

    // Check what series data exists for this rider
    if ($useSeriesEvents) {
        $stmt = $pdo->prepare("
            SELECT
                s.id,
                s.name,
                s.year as series_year,
                s.status,
                s.end_date,
                YEAR(e.date) as event_year,
                COUNT(r.id) as result_count,
                SUM(r.points) as total_points
            FROM results r
            JOIN events e ON r.event_id = e.id
            JOIN series_events se ON se.event_id = e.id
            JOIN series s ON se.series_id = s.id
            WHERE r.cyclist_id = ?
              AND r.status = 'finished'
            GROUP BY s.id, COALESCE(s.year, YEAR(e.date))
            ORDER BY event_year DESC, s.name
        ");
    } else {
        $stmt = $pdo->prepare("
            SELECT
                s.id,
                s.name,
                s.year as series_year,
                s.status,
                s.end_date,
                YEAR(e.date) as event_year,
                COUNT(r.id) as result_count,
                SUM(r.points) as total_points
            FROM results r
            JOIN events e ON r.event_id = e.id
            JOIN series s ON e.series_id = s.id
            WHERE r.cyclist_id = ?
              AND r.status = 'finished'
            GROUP BY s.id, COALESCE(s.year, YEAR(e.date))
            ORDER BY event_year DESC, s.name
        ");
    }
    $stmt->execute([$rider_id]);
    $debug['series_data'] = $stmt->fetchAll(PDO::FETCH_ASSOC);

    // Check series championships calculation
    // Series qualifies if: status='completed' OR end_date < today OR events from previous year
    if ($useSeriesEvents) {
        $stmt = $pdo->prepare("
            SELECT
                s.id as series_id,
                s.name as series_name,
                s.year as series_year,
                s.status as series_status,
                s.end_date,
                COALESCE(s.year, YEAR(e.date)) as effective_year,
                r.class_id,
                SUM(r.points) as total_points
            FROM results r
            JOIN events e ON r.event_id = e.id
            JOIN series_events se ON se.event_id = e.id
            JOIN series s ON se.series_id = s.id
            WHERE r.cyclist_id = ?
              AND r.status = 'finished'
              AND (
                  s.status = 'completed'
                  OR (s.end_date IS NOT NULL AND s.end_date < CURDATE())
                  OR YEAR(e.date) < ?
              )
            GROUP BY s.id, COALESCE(s.year, YEAR(e.date)), r.class_id
        ");
    } else {
        $stmt = $pdo->prepare("
            SELECT
                s.id as series_id,
                s.name as series_name,
                s.year as series_year,
                s.status as series_status,
                s.end_date,
                COALESCE(s.year, YEAR(e.date)) as effective_year,
                r.class_id,
                SUM(r.points) as total_points
            FROM results r
            JOIN events e ON r.event_id = e.id
            JOIN series s ON e.series_id = s.id
            WHERE r.cyclist_id = ?
              AND r.status = 'finished'
              AND (
                  s.status = 'completed'
                  OR (s.end_date IS NOT NULL AND s.end_date < CURDATE())
                  OR YEAR(e.date) < ?
              )
            GROUP BY s.id, COALESCE(s.year, YEAR(e.date)), r.class_id
        ");
    }
    $stmt->execute([$rider_id, $currentYear]);
    $riderSeasons = $stmt->fetchAll(PDO::FETCH_ASSOC);

    foreach ($riderSeasons as $season) {
        $year = (int)($season['effective_year']);
        $seriesId = $season['series_id'];
        $classId = $season['class_id'];

        // Find max points for this series/class/year
        if ($useSeriesEvents) {
            $stmt = $pdo->prepare("
                SELECT MAX(total) as max_points FROM (
                    SELECT r.cyclist_id, SUM(r.points) as total
                    FROM results r
                    JOIN events e ON r.event_id = e.id
                    JOIN series_events se ON se.event_id = e.id
                    JOIN series s ON se.series_id = s.id
                    WHERE se.series_id = ?
                      AND r.class_id = ?
                      AND COALESCE(s.year, YEAR(e.date)) = ?
                      AND r.status = 'finished'
                    GROUP BY r.cyclist_id
                ) as subq
            ");
        } else {
            $stmt = $pdo->prepare("
                SELECT MAX(total) as max_points FROM (
                    SELECT r.cyclist_id, SUM(r.points) as total
                    FROM results r
                    JOIN events e ON r.event_id = e.id
                    JOIN series s ON e.series_id = s.id
                    WHERE e.series_id = ?
                      AND r.class_id = ?
                      AND COALESCE(s.year, YEAR(e.date)) = ?
                      AND r.status = 'finished'
                    GROUP BY r.cyclist_id
                ) as subq
            ");
        }
        $stmt->execute([$seriesId, $classId, $year]);
        $maxPoints = $stmt->fetchColumn();

        $isChampion = ($season['total_points'] == $maxPoints && $maxPoints > 0);

        $debug['series_championships'][] = [
            'series' => $season['series_name'],
            'year' => $year,
            'series_year' => $season['series_year'],
            'series_status' => $season['series_status'],
            'end_date' => $season['end_date'] ?? null,
            'class_id' => $classId,
            'rider_points' => $season['total_points'],
            'max_points' => $maxPoints,
            'is_champion' => $isChampion
        ];
    }

    // Check Swedish championships
    $stmt = $pdo->prepare("
        SELECT
            e.name as event_name,
            YEAR(e.date) as year,
            e.is_championship,
            r.position
        FROM results r
        JOIN events e ON r.event_id = e.id
        WHERE r.cyclist_id = ?
          AND r.position = 1
          AND r.status = 'finished'
          AND e.is_championship = 1
    ");
    $stmt->execute([$rider_id]);
    $debug['swedish_championships'] = $stmt->fetchAll(PDO::FETCH_ASSOC);

    // Count podiums
    $stmt = $pdo->prepare("
        SELECT
            SUM(CASE WHEN position = 1 THEN 1 ELSE 0 END) as gold,
            SUM(CASE WHEN position = 2 THEN 1 ELSE 0 END) as silver,
            SUM(CASE WHEN position = 3 THEN 1 ELSE 0 END) as bronze
        FROM results
        WHERE cyclist_id = ? AND status = 'finished'
    ");
    $stmt->execute([$rider_id]);
    $podiums = $stmt->fetch(PDO::FETCH_ASSOC);
    $debug['podiums'] = $podiums ?: ['gold' => 0, 'silver' => 0, 'bronze' => 0];

    return $debug;
}

$page_title = 'Rebuild Rider Stats';
$breadcrumbs = [
    ['label' => 'Inställningar', 'url' => '/admin/tools.php'],
    ['label' => 'Rebuild Stats']
];
include __DIR__ . '/components/unified-layout.php';
?>

        <!-- Header -->
        <div class="flex items-center justify-between mb-lg">
            <div>
                <h1>
                    <i data-lucide="refresh-cw"></i>
                    Rebuild Rider Statistics
                </h1>
                <p class="text-secondary">
                    Räkna om statistik och achievements efter resultatimport
                </p>
            </div>
            <a href="/admin/tools.php" class="btn btn--secondary">
                <i data-lucide="arrow-left"></i>
                Tillbaka
            </a>
        </div>

        <?php if ($message): ?>
        <div class="alert alert-<?= h($messageType) ?> mb-lg">
            <i data-lucide="<?= $messageType === 'success' ? 'check-circle' : ($messageType === 'error' ? 'alert-circle' : 'alert-triangle') ?>"></i>
            <?= h($message) ?>
        </div>
        <?php endif; ?>

        <!-- Current Stats -->
        <div class="card mb-lg">
            <div class="card-header">
                <h2><i data-lucide="bar-chart-2"></i> Nuvarande status</h2>
            </div>
            <div class="card-body">
                <div class="grid grid-cols-4 gap-md">
                    <div class="stat-box">
                        <div class="stat-value"><?= number_format($stats['total_riders']) ?></div>
                        <div class="stat-label">Åkare totalt</div>
                    </div>
                    <div class="stat-box">
                        <div class="stat-value"><?= number_format($stats['riders_with_results']) ?></div>
                        <div class="stat-label">Med resultat</div>
                    </div>
                    <div class="stat-box">
                        <div class="stat-value"><?= number_format($stats['total_results']) ?></div>
                        <div class="stat-label">Resultat</div>
                    </div>
                    <div class="stat-box">
                        <div class="stat-value"><?= number_format($stats['total_achievements']) ?></div>
                        <div class="stat-label">Achievements</div>
                    </div>
                </div>
                <p class="text-secondary mt-md" style="font-size: 0.85rem;">
                    Senaste rebuild: <?= $stats['last_rebuild'] ? date('Y-m-d H:i', strtotime($stats['last_rebuild'])) : 'Aldrig' ?>
                </p>
            </div>
        </div>

        <!-- Migration -->
        <div class="card mb-lg">
            <div class="card-header">
                <h2><i data-lucide="database"></i> Steg 1: Databasmigration</h2>
            </div>
            <div class="card-body">
                <p class="text-secondary mb-md">
                    Kör detta FÖRST för att skapa nya tabeller och kolumner. Säkert att köra flera gånger.
                </p>
                <form method="POST">
                    <?= csrf_field() ?>
                    <input type="hidden" name="action" value="migrate">
                    <button type="submit" class="btn btn--secondary">
                        <i data-lucide="play"></i>
                        Kör Migration
                    </button>
                </form>

                <?php if ($results && isset($results[0]['sql'])): ?>
                <div class="mt-md">
                    <table class="table table--striped">
                        <thead>
                            <tr>
                                <th>Query</th>
                                <th>Status</th>
                            </tr>
                        </thead>
                        <tbody>
                            <?php foreach ($results as $r): ?>
                            <tr>
                                <td><code style="font-size: 0.75rem;"><?= h($r['sql']) ?></code></td>
                                <td class="<?= strpos($r['status'], 'OK') !== false ? 'text-success' : (strpos($r['status'], 'ERROR') !== false ? 'text-error' : 'text-secondary') ?>">
                                    <?= h($r['status']) ?>
                                </td>
                            </tr>
                            <?php endforeach; ?>
                        </tbody>
                    </table>
                </div>
                <?php endif; ?>
            </div>
        </div>

        <!-- Single Rider Rebuild -->
        <div class="card mb-lg">
            <div class="card-header">
                <h2><i data-lucide="user"></i> Steg 2a: Rebuild enskild åkare</h2>
            </div>
            <div class="card-body">
                <p class="text-secondary mb-md">
                    Testa på en åkare först för att verifiera att allt fungerar.
                </p>
                <form method="POST" class="flex gap-sm">
                    <?= csrf_field() ?>
                    <input type="hidden" name="action" value="rebuild_single">
                    <input type="number" name="rider_id" placeholder="Rider ID (t.ex. 7701)" required min="1" class="form-control" style="max-width: 200px;">
                    <button type="submit" class="btn btn--primary">
                        <i data-lucide="refresh-cw"></i>
                        Rebuild åkare
                    </button>
                </form>

                <?php if (isset($results['debug'])): ?>
                <div class="debug-output mt-lg">
                    <h4>🔍 Debug Information</h4>

                    <!-- Podiums -->
                    <div class="debug-section">
                        <strong>Pallplatser:</strong>
                        Guld: <?= $results['debug']['podiums']['gold'] ?? 0 ?>,
                        Silver: <?= $results['debug']['podiums']['silver'] ?? 0 ?>,
                        Brons: <?= $results['debug']['podiums']['bronze'] ?? 0 ?>
                    </div>

                    <!-- Series Data -->
                    <?php if (!empty($results['debug']['series_data'])): ?>
                    <div class="debug-section">
                        <strong>Serie-deltaganden:</strong>
                        <table class="table table--striped table--sm mt-sm">
                            <thead>
                                <tr>
                                    <th>Serie</th>
                                    <th>År (serie)</th>
                                    <th>År (event)</th>
                                    <th>Status</th>
                                    <th>Resultat</th>
                                    <th>Poäng</th>
                                </tr>
                            </thead>
                            <tbody>
                                <?php foreach ($results['debug']['series_data'] as $sd): ?>
                                <tr>
                                    <td><?= h($sd['name']) ?></td>
                                    <td><?= $sd['series_year'] ?? '<span class="text-warning">NULL</span>' ?></td>
                                    <td><?= $sd['event_year'] ?></td>
                                    <td><?= $sd['status'] ?? 'N/A' ?></td>
                                    <td><?= $sd['result_count'] ?></td>
                                    <td><?= $sd['total_points'] ?></td>
                                </tr>
                                <?php endforeach; ?>
                            </tbody>
                        </table>
                    </div>
                    <?php endif; ?>

                    <!-- Series Championships -->
                    <div class="debug-section">
                        <strong>Seriemästare-beräkning:</strong>
                        <?php if (empty($results['debug']['series_championships'])): ?>
                            <p class="text-warning">Inga kvalificerande serier hittades (kräver end_date passerat, status='completed', eller events från tidigare år)</p>
                        <?php else: ?>
                        <table class="table table--striped table--sm mt-sm">
                            <thead>
                                <tr>
                                    <th>Serie</th>
                                    <th>År</th>
                                    <th>End Date</th>
                                    <th>Status</th>
                                    <th>Åkarens poäng</th>
                                    <th>Max poäng</th>
                                    <th>Mästare?</th>
                                </tr>
                            </thead>
                            <tbody>
                                <?php foreach ($results['debug']['series_championships'] as $sc): ?>
                                <tr class="<?= $sc['is_champion'] ? 'bg-success-light' : '' ?>">
                                    <td><?= h($sc['series']) ?></td>
                                    <td><?= $sc['year'] ?></td>
                                    <td><?= $sc['end_date'] ?? '<span class="text-secondary">-</span>' ?></td>
                                    <td><?= $sc['series_status'] ?? 'N/A' ?></td>
                                    <td><?= $sc['rider_points'] ?></td>
                                    <td><?= $sc['max_points'] ?></td>
                                    <td><?= $sc['is_champion'] ? '✅ JA' : '❌ Nej' ?></td>
                                </tr>
                                <?php endforeach; ?>
                            </tbody>
                        </table>
                        <?php endif; ?>
                    </div>

                    <!-- Swedish Championships -->
                    <div class="debug-section">
                        <strong>SM-titlar:</strong>
                        <?php if (empty($results['debug']['swedish_championships'])): ?>
                            <p class="text-secondary">Inga SM-segrar (kräver is_championship=1 på event och position=1)</p>
                        <?php else: ?>
                        <ul>
                            <?php foreach ($results['debug']['swedish_championships'] as $sm): ?>
                            <li>🥇 <?= h($sm['event_name']) ?> (<?= $sm['year'] ?>)</li>
                            <?php endforeach; ?>
                        </ul>
                        <?php endif; ?>
                    </div>
                </div>
                <?php endif; ?>
            </div>
        </div>

        <!-- Full Rebuild -->
        <div class="card mb-lg">
            <div class="card-header">
                <h2><i data-lucide="users"></i> Steg 2b: Rebuild ALLA åkare</h2>
            </div>
            <div class="card-body">
                <div class="alert alert-warning mb-md">
                    <i data-lucide="alert-triangle"></i>
                    <strong>Varning:</strong> Detta kan ta flera minuter beroende på antal åkare och resultat.
                    Stäng inte webbläsaren medan processen körs.
                </div>
                <form method="POST" onsubmit="return confirm('Är du säker? Detta kommer räkna om statistik för ALLA åkare.');">
                    <?= csrf_field() ?>
                    <input type="hidden" name="action" value="rebuild_all">
                    <button type="submit" class="btn btn--danger">
                        <i data-lucide="zap"></i>
                        Rebuild alla åkare
                    </button>
                </form>
            </div>
        </div>

        <!-- Update Leaders Only -->
        <div class="card mb-lg">
            <div class="card-header">
                <h2><i data-lucide="trophy"></i> Uppdatera serieledare</h2>
            </div>
            <div class="card-body">
                <p class="text-secondary mb-md">
                    Snabb uppdatering av endast "Serieledare"-achievements för pågående säsong.
                </p>
                <form method="POST">
                    <?= csrf_field() ?>
                    <input type="hidden" name="action" value="update_leaders">
                    <button type="submit" class="btn btn--primary">
                        <i data-lucide="crown"></i>
                        Uppdatera ledare
                    </button>
                </form>
            </div>
        </div>

        <!-- Usage Info -->
        <div class="card">
            <div class="card-header">
                <h2><i data-lucide="book-open"></i> Användning</h2>
            </div>
            <div class="card-body">
                <ol class="usage-list">
                    <li>Kör <strong>Migration</strong> första gången (skapar nya tabeller)</li>
                    <li>Importera resultat som vanligt (CSV-import etc.)</li>
                    <li>Kör <strong>Rebuild enskild åkare</strong> för att testa</li>
                    <li>Kör <strong>Rebuild alla åkare</strong> efter stora importer</li>
                    <li>Kör <strong>Uppdatera ledare</strong> efter varje nytt event-resultat</li>
                </ol>
            </div>
        </div>

<style>
/* Mobile first - base styles */
.stat-box {
    text-align: center;
    padding: var(--space-md);
    background: var(--color-star-fade);
    border-radius: var(--radius-md);
}

.stat-value {
    font-size: 1.25rem;
    font-weight: 700;
    color: var(--color-primary);
    line-height: 1;
}

.stat-label {
    font-size: 0.7rem;
    color: var(--color-text);
    text-transform: uppercase;
    letter-spacing: 0.5px;
    margin-top: var(--space-xs);
}

.usage-list {
    margin-left: var(--space-lg);
    color: var(--color-text);
}

.usage-list li {
    margin-bottom: var(--space-sm);
}

.usage-list strong {
    color: var(--color-primary);
}

.form-control {
    padding: var(--space-sm) var(--space-md);
    border: 1px solid var(--color-border);
    border-radius: var(--radius-md);
    background: var(--color-star);
    color: var(--color-primary);
    width: 100%;
}

.form-control:focus {
    outline: none;
    border-color: var(--color-accent);
}

/* Grid - mobile first (2 columns) */
.grid {
    display: grid;
}

.grid-cols-4 {
    grid-template-columns: repeat(2, 1fr);
}

.gap-md {
    gap: var(--space-md);
}

/* Page header - mobile: stack vertically */
.main-content .container > .flex:first-child {
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    gap: var(--space-md);
}

/* Form with input + button - mobile: stack */
form.flex {
    display: flex;
    flex-direction: column;
    gap: var(--space-sm);
}

form.flex .form-control {
    width: 100%;
}

/* Cards full width on mobile */
.card {
    overflow-x: auto;
}

/* Tablet (600px+) */
@media (min-width: 600px) {
    .stat-value {
        font-size: 1.5rem;
    }

    .stat-label {
        font-size: 0.75rem;
    }

    form.flex {
        flex-direction: row;
        align-items: center;
    }

    form.flex .form-control {
        width: auto;
        max-width: 200px;
    }
}

/* Desktop (900px+) */
@media (min-width: 900px) {
    .grid-cols-4 {
        grid-template-columns: repeat(4, 1fr);
    }

    .stat-value {
        font-size: 1.75rem;
    }

    .main-content .container > .flex:first-child {
        flex-direction: row;
        align-items: center;
        justify-content: space-between;
    }
}

/* Debug output styling */
.debug-output {
    background: var(--color-star-fade);
    border: 1px solid var(--color-border);
    border-radius: var(--radius-md);
    padding: var(--space-md);
}

.debug-output h4 {
    margin: 0 0 var(--space-md) 0;
    color: var(--color-primary);
    font-size: 1rem;
}

.debug-section {
    margin-bottom: var(--space-md);
    padding-bottom: var(--space-md);
    border-bottom: 1px solid var(--color-border);
}

.debug-section:last-child {
    margin-bottom: 0;
    padding-bottom: 0;
    border-bottom: none;
}

.debug-section strong {
    display: block;
    margin-bottom: var(--space-xs);
    color: var(--color-primary);
}

.debug-section ul {
    margin: var(--space-sm) 0 0 var(--space-lg);
    padding: 0;
}

.debug-section li {
    margin-bottom: var(--space-xs);
}

.table--sm th,
.table--sm td {
    padding: var(--space-xs) var(--space-sm);
    font-size: 0.8rem;
}

.bg-success-light {
    background: rgba(97, 206, 112, 0.15);
}

.text-warning {
    color: var(--color-warning);
}
</style>

<?php include __DIR__ . '/components/unified-layout-footer.php'; ?>
