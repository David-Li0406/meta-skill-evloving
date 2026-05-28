<?php
/**
 * Setup Analytics Tables
 * Kor EFTER setup-governance.php
 *
 * Skapar:
 * - rider_yearly_stats
 * - series_participation
 * - series_crossover
 * - club_yearly_stats
 * - venue_yearly_stats
 * - analytics_snapshots
 *
 * Samt utokar series-tabellen med analytics-kolumner.
 *
 * Kan koras bade fran CLI och web.
 *
 * @package TheHUB Analytics
 * @version 1.0
 */

// Bestam om vi kor i CLI eller web
$isCli = (php_sapi_name() === 'cli');

if (!$isCli) {
    // Web-mode: Krav autentisering
    require_once __DIR__ . '/../config.php';
    require_once __DIR__ . '/../includes/auth.php';

    // Endast admin far kora setup
    if (!isLoggedIn() || !hasRole('admin')) {
        http_response_code(403);
        die('Atkomst nekad: Endast admin kan kora setup');
    }

    header('Content-Type: text/plain; charset=utf-8');
}

// Ladda beroenden
require_once __DIR__ . '/includes/sql-runner.php';
require_once __DIR__ . '/migrations/002_series_extensions.php';

// Skapa output-funktion som fungerar bade i CLI och web
function output(string $message): void {
    global $isCli;
    if ($isCli) {
        echo $message . "\n";
    } else {
        echo $message . "\n";
        ob_flush();
        flush();
    }
}

output("=== TheHUB Analytics: Tables Setup ===");
output("");

try {
    // Hamta databasanslutning
    if ($isCli) {
        // CLI: Ladda config manuellt
        require_once __DIR__ . '/../config.php';
    }

    // Anvand global $pdo fran config.php
    global $pdo;

    if (!$pdo) {
        throw new Exception("Ingen databasanslutning tillganglig");
    }

    output("Ansluten till databas: " . DB_NAME);
    output("");

    // Kolla att governance-tabeller finns
    if (!tableExists($pdo, 'analytics_logs')) {
        output("[VARNING] Governance-tabeller saknas!");
        output("          Kor forst: php analytics/setup-governance.php");
        output("");
    }

    // 1. Kor huvudtabeller
    output("1. Skapar analytics-tabeller...");
    $migrationFile = __DIR__ . '/migrations/001_analytics_tables.sql';

    if (!file_exists($migrationFile)) {
        throw new Exception("Migration-fil saknas: $migrationFile");
    }

    $result = runSqlFile($pdo, $migrationFile);
    output(formatMigrationResult($result));

    // 2. Kor series extensions (via PHP for kompatibilitet)
    output("2. Utokar series-tabellen...");
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

    // 3. Kor series level seed
    output("");
    output("3. Kategoriserar serier (series_level)...");
    $seedFile = __DIR__ . '/migrations/003_seed_series_levels.sql';

    if (file_exists($seedFile)) {
        $seedResult = runSqlFile($pdo, $seedFile);
        output("   [OK] {$seedResult['success']} statements korda");
    } else {
        output("   [SKIP] Seed-fil saknas: $seedFile");
    }

    // Visa series_level statistik
    output("");
    output("   Seriekategorisering:");
    $levelStats = $pdo->query("
        SELECT series_level, COUNT(*) as cnt
        FROM series
        WHERE series_level IS NOT NULL AND series_level != ''
        GROUP BY series_level
        ORDER BY
            CASE series_level
                WHEN 'national' THEN 1
                WHEN 'championship' THEN 2
                WHEN 'regional' THEN 3
                WHEN 'local' THEN 4
            END
    ")->fetchAll();

    foreach ($levelStats as $stat) {
        output("   - {$stat['series_level']}: {$stat['cnt']} serier");
    }

    // Verifiera att analytics-tabellerna skapades
    output("");
    output("4. Verifierar tabeller...");

    $tables = [
        'rider_yearly_stats',
        'series_participation',
        'series_crossover',
        'club_yearly_stats',
        'venue_yearly_stats',
        'analytics_snapshots'
    ];

    $allOk = true;
    foreach ($tables as $table) {
        if (tableExists($pdo, $table)) {
            output("   [OK] $table");
        } else {
            output("   [FEL] $table saknas!");
            $allOk = false;
        }
    }

    // Verifiera series-kolumner
    output("");
    output("5. Verifierar series-utokningar...");

    $seriesColumns = ['series_level', 'parent_series_id', 'region', 'analytics_enabled'];
    foreach ($seriesColumns as $col) {
        if (columnExists($pdo, 'series', $col)) {
            output("   [OK] series.$col");
        } else {
            output("   [FEL] series.$col saknas!");
            $allOk = false;
        }
    }

    // Logga framgang
    if (tableExists($pdo, 'analytics_logs')) {
        logAnalytics($pdo, 'info', 'Tables setup slutford', 'setup-tables', [
            'tables_created' => $result['success'],
            'series_extensions' => $extResult,
            'all_ok' => $allOk
        ]);
    }

    output("");
    output("=== Tables Setup " . ($allOk ? "KLAR" : "MED FEL") . " ===");

    if (!$allOk) {
        exit(1);
    }

} catch (Exception $e) {
    output("");
    output("[KRITISKT FEL] " . $e->getMessage());
    output("");
    output("Kontrollera:");
    output("  - Att setup-governance.php har korts forst");
    output("  - Att databasanslutningen fungerar");
    output("  - Att migrationsfilerna finns");

    if (isset($pdo) && function_exists('tableExists') && tableExists($pdo, 'analytics_logs')) {
        logAnalytics($pdo, 'critical', 'Tables setup misslyckades: ' . $e->getMessage(), 'setup-tables');
    }

    exit(1);
}
