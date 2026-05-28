<?php
/**
 * Populate Historical Analytics Data
 *
 * Genererar all historisk analytics-data for tidigare ar.
 * Kor detta EFTER setup-governance.php och setup-tables.php.
 *
 * Vad scriptet gor:
 * 1. Hittar alla ar med data i events-tabellen
 * 2. For varje ar, kor alla berakningar via AnalyticsEngine
 * 3. Loggar progress och resultat
 *
 * Kan koras bade fran CLI och web.
 * CLI: php populate-historical.php [start_year] [end_year]
 *
 * @package TheHUB Analytics
 * @version 1.0
 */

// Okning av tidsgrans for langa korningar
set_time_limit(1800); // 30 minuter (stora ar tar lang tid)
ini_set('memory_limit', '512M');

// Bestam om vi kor i CLI eller web
$isCli = (php_sapi_name() === 'cli');

if (!$isCli) {
    // Web-mode: Krav autentisering
    require_once __DIR__ . '/../config.php';
    require_once __DIR__ . '/../includes/auth.php';

    // Endast admin far kora
    if (!isLoggedIn() || !hasRole('admin')) {
        http_response_code(403);
        die('Atkomst nekad: Endast admin kan kora populate');
    }

    // Disable all output buffering for real-time output
    while (ob_get_level()) {
        ob_end_flush();
    }

    header('Content-Type: text/plain; charset=utf-8');
    header('X-Accel-Buffering: no'); // Disable nginx buffering
    header('Cache-Control: no-cache');
    ob_implicit_flush(true);

    // Disable PHP output buffering
    ini_set('output_buffering', 'off');
    ini_set('zlib.output_compression', false);
}

// Ladda beroenden
require_once __DIR__ . '/includes/AnalyticsEngine.php';
require_once __DIR__ . '/includes/KPICalculator.php';

// Skapa output-funktion
function output(string $message, bool $newline = true): void {
    global $isCli;
    $timestamp = date('H:i:s');
    $line = "[$timestamp] $message";

    if ($isCli) {
        echo $line . ($newline ? "\n" : "\r");
    } else {
        echo $line . ($newline ? "\n" : "                    \r");
        @ob_flush();
        flush();
    }
}

// Progress callback for long operations
function createProgressCallback(string $operation): callable {
    return function(int $current, int $total) use ($operation) {
        $pct = $total > 0 ? round(($current / $total) * 100) : 0;
        output("      [$pct%] $operation: $current / $total", false);
    };
}

output("=== TheHUB Analytics: Populate Historical Data ===");
output("");

try {
    // Hamta databasanslutning
    if ($isCli) {
        require_once __DIR__ . '/../config.php';
    }

    global $pdo;

    if (!$pdo) {
        throw new Exception("Ingen databasanslutning tillganglig");
    }

    // Kolla att tabeller finns
    $requiredTables = [
        'rider_yearly_stats',
        'series_participation',
        'series_crossover',
        'club_yearly_stats',
        'venue_yearly_stats',
        'v_canonical_riders' // VIEW
    ];

    output("Kontrollerar tabeller...");
    foreach ($requiredTables as $table) {
        $check = $pdo->query("SHOW TABLES LIKE '$table'")->fetch();
        if (!$check) {
            throw new Exception("Tabell '$table' saknas! Kor forst setup-tables.php");
        }
    }
    output("   Alla tabeller finns [OK]");
    output("");

    // Skapa engine
    $engine = new AnalyticsEngine($pdo);

    // Aktivera icke-blockerande lage - forhindrar att analytics lasar tabeller
    // och blockerar resten av sidan under berakning
    $engine->enableNonBlockingMode();
    output("Icke-blockerande lage aktiverat (READ UNCOMMITTED)");

    // Bestam ar att bearbeta
    $availableYears = $engine->getAvailableYears();

    if (empty($availableYears)) {
        throw new Exception("Inga ar med data hittades i events-tabellen");
    }

    // CLI-argument for specifika ar och force-flagga
    // Anvandning: php populate-historical.php [start_year] [end_year] [--force]
    $forceRerun = false;
    $startYear = min($availableYears);
    $endYear = max($availableYears);

    if ($isCli) {
        foreach ($argv as $i => $arg) {
            if ($arg === '--force' || $arg === '-f') {
                $forceRerun = true;
            } elseif ($i === 1 && is_numeric($arg)) {
                $startYear = (int)$arg;
            } elseif ($i === 2 && is_numeric($arg)) {
                $endYear = (int)$arg;
            }
        }
    }

    // Web-mode: kolla for force-parameter
    if (!$isCli && isset($_GET['force'])) {
        $forceRerun = true;
    }

    // Spara force-flaggan i engine for att kunna anvanda den
    $engine->setForceRerun($forceRerun);

    if ($forceRerun) {
        output("FORCE-LAGE: Alla jobb kors om oavsett tidigare status");
    } else {
        output("NORMAL LAGE: Redan klara jobb hoppas over (anvand --force for att kora om)");
    }

    // Filtrera ar
    $yearsToProcess = array_filter($availableYears, function($y) use ($startYear, $endYear) {
        return $y >= $startYear && $y <= $endYear;
    });

    sort($yearsToProcess);

    output("Tillgangliga ar: " . implode(', ', $availableYears));
    output("Bearbetar ar: " . implode(', ', $yearsToProcess));
    output("");

    $totalStats = [
        'years_processed' => 0,
        'yearly_stats' => 0,
        'series_participation' => 0,
        'series_crossover' => 0,
        'club_stats' => 0,
        'venue_stats' => 0,
        'errors' => []
    ];

    $startTime = microtime(true);

    foreach ($yearsToProcess as $year) {
        output("--- Ar $year ---");

        try {
            $yearSkipped = true;

            // 1. Yearly Stats
            output("  1/5 rider_yearly_stats...");
            $progressCallback = createProgressCallback("riders");
            $count = $engine->calculateYearlyStats($year, $progressCallback);
            if ($count > 0) {
                output(""); // Clear progress line
                output("      $count riders bearbetade");
                $totalStats['yearly_stats'] += $count;
                $yearSkipped = false;
            } else {
                output("      [HOPPAS OVER - redan klar]");
            }

            // 2. Series Participation
            output("  2/5 series_participation...");
            $progressCallback = createProgressCallback("participations");
            $count = $engine->calculateSeriesParticipation($year, $progressCallback);
            if ($count > 0) {
                output(""); // Clear progress line
                output("      $count participations skapade");
                $totalStats['series_participation'] += $count;
                $yearSkipped = false;
            } else {
                output("      [HOPPAS OVER - redan klar]");
            }

            // 3. Series Crossover
            output("  3/5 series_crossover...");
            $count = $engine->calculateSeriesCrossover($year);
            if ($count > 0) {
                output("      $count crossovers skapade");
                $totalStats['series_crossover'] += $count;
                $yearSkipped = false;
            } else {
                output("      [HOPPAS OVER - redan klar]");
            }

            // 4. Club Stats
            output("  4/5 club_yearly_stats...");
            $progressCallback = createProgressCallback("klubbar");
            $count = $engine->calculateClubStats($year, $progressCallback);
            if ($count > 0) {
                output(""); // Clear progress line
                output("      $count klubbar bearbetade");
                $totalStats['club_stats'] += $count;
                $yearSkipped = false;
            } else {
                output("      [HOPPAS OVER - redan klar]");
            }

            // 5. Venue Stats
            output("  5/5 venue_yearly_stats...");
            $count = $engine->calculateVenueStats($year);
            if ($count > 0) {
                output("      $count venues bearbetade");
                $totalStats['venue_stats'] += $count;
                $yearSkipped = false;
            } else {
                output("      [HOPPAS OVER - redan klar]");
            }

            if ($yearSkipped) {
                output("  [HOPPAS OVER] Ar $year redan beraknat");
                $totalStats['years_skipped'] = ($totalStats['years_skipped'] ?? 0) + 1;
            } else {
                $totalStats['years_processed']++;
                output("  [OK] Ar $year klart");
            }
            output("");

        } catch (Exception $e) {
            $totalStats['errors'][] = "$year: " . $e->getMessage();
            output("  [FEL] " . $e->getMessage());
            output("");
        }
    }

    $endTime = microtime(true);
    $duration = round($endTime - $startTime, 2);

    // Sammanfattning
    output("=== SAMMANFATTNING ===");
    output("");
    output("Tid: {$duration}s");
    output("Ar bearbetade: {$totalStats['years_processed']}");
    $skipped = $totalStats['years_skipped'] ?? 0;
    if ($skipped > 0) {
        output("Ar hoppade over (redan klara): $skipped");
    }
    output("");
    output("Rader skapade/uppdaterade:");
    output("  - rider_yearly_stats: {$totalStats['yearly_stats']}");
    output("  - series_participation: {$totalStats['series_participation']}");
    output("  - series_crossover: {$totalStats['series_crossover']}");
    output("  - club_yearly_stats: {$totalStats['club_stats']}");
    output("  - venue_yearly_stats: {$totalStats['venue_stats']}");

    if (!empty($totalStats['errors'])) {
        output("");
        output("FEL:");
        foreach ($totalStats['errors'] as $err) {
            output("  - $err");
        }
    }

    output("");

    // Visa nagra KPIs for senaste aret
    if ($totalStats['years_processed'] > 0) {
        $latestYear = max($yearsToProcess);
        $kpi = new KPICalculator($pdo);

        output("=== KPI VERIFIERING ($latestYear) ===");
        output("");
        output("Totalt aktiva riders: " . $kpi->getTotalActiveRiders($latestYear));
        output("Nya riders (rookies): " . $kpi->getNewRidersCount($latestYear));
        output("Retention rate: " . $kpi->getRetentionRate($latestYear) . "%");
        output("Cross-participation: " . $kpi->getCrossParticipationRate($latestYear) . "%");
        output("Genomsnittsalder: " . $kpi->getAverageAge($latestYear) . " ar");

        $gender = $kpi->getGenderDistribution($latestYear);
        output("Konsfordelning: M={$gender['M']}, F={$gender['F']}, Okand={$gender['unknown']}");
    }

    output("");
    output("=== Populate Historical Data KLAR ===");

    // Logga till analytics_logs
    if (function_exists('tableExists') && tableExists($pdo, 'analytics_logs')) {
        $stmt = $pdo->prepare("
            INSERT INTO analytics_logs (level, job_name, message, context)
            VALUES ('info', 'populate-historical', 'Historisk data genererad', ?)
        ");
        $stmt->execute([json_encode($totalStats, JSON_UNESCAPED_UNICODE)]);
    }

} catch (Exception $e) {
    output("");
    output("[KRITISKT FEL] " . $e->getMessage());
    output("");
    output("Kontrollera:");
    output("  - Att setup-governance.php har korts");
    output("  - Att setup-tables.php har korts");
    output("  - Att det finns data i events och results");
    exit(1);
}
