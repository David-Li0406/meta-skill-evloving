<?php
/**
 * Setup Governance Tables
 * Kor detta FORE Steg 1
 *
 * Skapar:
 * - rider_merge_map (dubblett-hantering)
 * - rider_identity_audit (andringslogg)
 * - rider_affiliations (klubbhistorik)
 * - analytics_cron_runs (cron-korningar)
 * - analytics_logs (generell loggning)
 * - v_canonical_riders (VIEW for canonical lookup)
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

output("=== TheHUB Analytics: Governance Setup ===");
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

    // Kor migrations
    output("1. Skapar governance-tabeller...");
    $migrationFile = __DIR__ . '/migrations/000_governance_core.sql';

    if (!file_exists($migrationFile)) {
        throw new Exception("Migration-fil saknas: $migrationFile");
    }

    $result = runSqlFile($pdo, $migrationFile);

    output(formatMigrationResult($result));

    // Verifiera att tabellerna skapades
    output("");
    output("2. Verifierar tabeller...");

    $tables = [
        'rider_merge_map',
        'rider_identity_audit',
        'rider_affiliations',
        'analytics_cron_runs',
        'analytics_logs'
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

    // Verifiera VIEW
    output("");
    output("3. Verifierar VIEW...");

    $viewCheck = $pdo->query("
        SELECT COUNT(*) as cnt
        FROM INFORMATION_SCHEMA.VIEWS
        WHERE TABLE_SCHEMA = DATABASE()
        AND TABLE_NAME = 'v_canonical_riders'
    ")->fetch();

    if ($viewCheck && $viewCheck['cnt'] > 0) {
        output("   [OK] v_canonical_riders");

        // Testa att VIEW fungerar
        $testResult = $pdo->query("SELECT COUNT(*) as cnt FROM v_canonical_riders")->fetch();
        output("   [OK] VIEW innehaller {$testResult['cnt']} rader");
    } else {
        output("   [FEL] v_canonical_riders saknas!");
        $allOk = false;
    }

    // Logga framgang
    if (tableExists($pdo, 'analytics_logs')) {
        logAnalytics($pdo, 'info', 'Governance setup slutford', 'setup-governance', [
            'tables_created' => $result['success'],
            'skipped' => $result['skipped'],
            'errors' => count($result['errors'])
        ]);
    }

    output("");
    output("=== Governance Setup " . ($allOk ? "KLAR" : "MED FEL") . " ===");

    if (!$allOk) {
        exit(1);
    }

} catch (Exception $e) {
    output("");
    output("[KRITISKT FEL] " . $e->getMessage());
    output("");
    output("Kontrollera:");
    output("  - Att databasanslutningen fungerar");
    output("  - Att .env eller config/database.php ar korrekt");
    output("  - Att migrationsfilerna finns");

    if (isset($pdo) && tableExists($pdo, 'analytics_logs')) {
        logAnalytics($pdo, 'critical', 'Governance setup misslyckades: ' . $e->getMessage(), 'setup-governance');
    }

    exit(1);
}
