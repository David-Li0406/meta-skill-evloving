<?php
/**
 * TheHUB Analytics - Unified Migration Runner
 *
 * Kor alla migrations i ratt ordning:
 * 1. Governance-tabeller (Steg 0)
 * 2. Analytics-tabeller (Steg 1)
 * 3. Series extensions (Steg 1)
 * 4. Series level seed (Steg 1)
 *
 * Kan koras fran CLI eller web.
 * CLI: php run-migrations.php [--force]
 *
 * @package TheHUB Analytics
 * @version 1.0
 */

// Okning av tidsgrans
set_time_limit(300);

// Bestam om vi kor i CLI eller web
$isCli = (php_sapi_name() === 'cli');

if (!$isCli) {
    // Web-mode: Krav autentisering
    require_once __DIR__ . '/../../config.php';
    require_once __DIR__ . '/../../includes/auth.php';

    if (!isLoggedIn() || !hasRole('admin')) {
        http_response_code(403);
        die('Atkomst nekad: Endast admin kan kora migrations');
    }

    header('Content-Type: text/plain; charset=utf-8');
    ob_implicit_flush(true);
}

// Ladda sql-runner
require_once __DIR__ . '/../../analytics/includes/sql-runner.php';

// Ladda series extensions
require_once __DIR__ . '/002_series_extensions.php';

function output(string $message): void {
    global $isCli;
    $timestamp = date('H:i:s');
    echo "[$timestamp] $message\n";
    if (!$isCli) {
        ob_flush();
        flush();
    }
}

output("╔════════════════════════════════════════════════════════════╗");
output("║        TheHUB Analytics - Migration Runner                 ║");
output("╚════════════════════════════════════════════════════════════╝");
output("");

try {
    // Hamta databasanslutning
    if ($isCli) {
        require_once __DIR__ . '/../../config.php';
    }

    global $pdo;

    if (!$pdo) {
        throw new Exception("Ingen databasanslutning tillganglig");
    }

    output("Ansluten till databas: " . DB_NAME);
    output("");

    $totalSuccess = 0;
    $totalSkipped = 0;
    $totalErrors = 0;

    // =========================================================================
    // STEG 0: Governance Core
    // =========================================================================
    output("═══ STEG 0: Governance Core ═══");
    output("");

    $file = __DIR__ . '/000_governance_core.sql';
    if (file_exists($file)) {
        output("Kor: 000_governance_core.sql");
        $result = runSqlFile($pdo, $file);
        output("   [OK] {$result['success']} statements");
        if ($result['skipped'] > 0) {
            output("   [SKIP] {$result['skipped']} (redan finns)");
        }
        if (!empty($result['errors'])) {
            foreach ($result['errors'] as $err) {
                output("   [FEL] $err");
            }
        }
        $totalSuccess += $result['success'];
        $totalSkipped += $result['skipped'];
        $totalErrors += count($result['errors']);
    } else {
        output("   [SKIP] Fil saknas: $file");
    }
    output("");

    // =========================================================================
    // STEG 1: Analytics Tables
    // =========================================================================
    output("═══ STEG 1: Analytics Tables ═══");
    output("");

    $file = __DIR__ . '/001_analytics_tables.sql';
    if (file_exists($file)) {
        output("Kor: 001_analytics_tables.sql");
        $result = runSqlFile($pdo, $file);
        output("   [OK] {$result['success']} statements");
        if ($result['skipped'] > 0) {
            output("   [SKIP] {$result['skipped']} (redan finns)");
        }
        if (!empty($result['errors'])) {
            foreach ($result['errors'] as $err) {
                output("   [FEL] $err");
            }
        }
        $totalSuccess += $result['success'];
        $totalSkipped += $result['skipped'];
        $totalErrors += count($result['errors']);
    }
    output("");

    // Series Extensions (PHP)
    output("Kor: 002_series_extensions.php");
    $extResult = runSeriesExtensions($pdo);
    if (!empty($extResult['added'])) {
        output("   [OK] Lade till: " . implode(', ', $extResult['added']));
    }
    if (!empty($extResult['skipped'])) {
        output("   [SKIP] Finns redan: " . implode(', ', $extResult['skipped']));
    }
    if (!empty($extResult['errors'])) {
        foreach ($extResult['errors'] as $err) {
            output("   [FEL] $err");
        }
    }
    output("");

    // Series Level Seed
    $file = __DIR__ . '/003_seed_series_levels.sql';
    if (file_exists($file)) {
        output("Kor: 003_seed_series_levels.sql");
        $result = runSqlFile($pdo, $file);
        output("   [OK] {$result['success']} statements");
        $totalSuccess += $result['success'];
    }
    output("");

    // =========================================================================
    // VERIFIERING
    // =========================================================================
    output("═══ VERIFIERING ═══");
    output("");

    // Governance-tabeller
    $govTables = ['rider_merge_map', 'rider_identity_audit', 'rider_affiliations',
                  'analytics_cron_runs', 'analytics_logs'];
    output("Governance-tabeller:");
    foreach ($govTables as $table) {
        $exists = tableExists($pdo, $table);
        output("   " . ($exists ? '[OK]' : '[FEL]') . " $table");
    }

    // VIEW
    $viewCheck = $pdo->query("
        SELECT COUNT(*) FROM INFORMATION_SCHEMA.VIEWS
        WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'v_canonical_riders'
    ")->fetchColumn();
    output("   " . ($viewCheck ? '[OK]' : '[FEL]') . " v_canonical_riders (VIEW)");
    output("");

    // Analytics-tabeller
    $analyticsTables = ['rider_yearly_stats', 'series_participation', 'series_crossover',
                        'club_yearly_stats', 'venue_yearly_stats', 'analytics_snapshots'];
    output("Analytics-tabeller:");
    foreach ($analyticsTables as $table) {
        $exists = tableExists($pdo, $table);
        output("   " . ($exists ? '[OK]' : '[FEL]') . " $table");
    }
    output("");

    // Series extensions
    output("Series-utokningar:");
    $seriesCols = ['series_level', 'parent_series_id', 'region', 'analytics_enabled'];
    foreach ($seriesCols as $col) {
        $exists = columnExists($pdo, 'series', $col);
        output("   " . ($exists ? '[OK]' : '[FEL]') . " series.$col");
    }
    output("");

    // Series level stats
    output("Seriekategorisering:");
    $levels = $pdo->query("
        SELECT COALESCE(series_level, 'null') as level, COUNT(*) as cnt
        FROM series
        GROUP BY series_level
    ")->fetchAll();
    foreach ($levels as $l) {
        output("   - {$l['level']}: {$l['cnt']} serier");
    }
    output("");

    // =========================================================================
    // SAMMANFATTNING
    // =========================================================================
    output("═══ SAMMANFATTNING ═══");
    output("");
    output("Statements korda: $totalSuccess");
    output("Skippade: $totalSkipped");
    output("Fel: $totalErrors");
    output("");
    output("╔════════════════════════════════════════════════════════════╗");
    output("║                  MIGRATIONS KLAR!                          ║");
    output("╚════════════════════════════════════════════════════════════╝");
    output("");
    output("Nasta steg:");
    output("  php analytics/populate-historical.php");
    output("");

} catch (Exception $e) {
    output("");
    output("[KRITISKT FEL] " . $e->getMessage());
    exit(1);
}
