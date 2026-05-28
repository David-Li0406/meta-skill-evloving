<?php
/**
 * Quick migration runner - runs pending SQL migrations directly
 */
require_once __DIR__ . '/../config.php';
require_admin();

$db = getDB();
$pdo = $GLOBALS['pdo'];

echo "<!DOCTYPE html><html><head><meta charset='UTF-8'><title>Kör väntande migrationer</title>";
echo "<style>
    body { font-family: system-ui, sans-serif; padding: 20px; background: #0b131e; color: #f8f2f0; max-width: 900px; margin: 0 auto; }
    .success { color: #10b981; }
    .error { color: #ef4444; }
    .info { color: #38bdf8; }
    .warning { color: #fbbf24; }
    .box { background: #0e1621; padding: 20px; border-radius: 10px; margin: 15px 0; border: 1px solid rgba(55, 212, 214, 0.2); }
    h1 { color: #37d4d6; }
    pre { background: #0b131e; padding: 10px; border-radius: 6px; overflow-x: auto; font-size: 12px; }
    .btn { display: inline-block; padding: 10px 20px; background: #37d4d6; color: #0b131e; text-decoration: none; border-radius: 6px; font-weight: 600; margin-top: 10px; margin-right: 10px; }
</style>";
echo "</head><body>";
echo "<h1>Kör väntande migrationer</h1>";

// List of migrations to check/run
$migrations = [
    '105_add_series_registration_settings.sql',
    '106_add_championship_fee_to_pricing.sql',
    '108_update_registration_rule_types.sql',
    '109_add_event_license_class_to_series.sql',
    '110_add_youtube_to_race_reports.sql'
];

$migrationsDir = __DIR__ . '/migrations/';

// Get already executed migrations
$executedMigrations = [];
try {
    $stmt = $pdo->query("SELECT migration_file FROM migrations_log");
    $executedMigrations = $stmt->fetchAll(PDO::FETCH_COLUMN);
} catch (Exception $e) {
    echo "<p class='warning'>Kunde inte läsa migrations_log: " . $e->getMessage() . "</p>";
}

$pending = [];
foreach ($migrations as $file) {
    if (!in_array($file, $executedMigrations)) {
        $pending[] = $file;
    }
}

if (empty($pending)) {
    echo "<div class='box'>";
    echo "<p class='success'>Alla migrationer är redan körda!</p>";
    echo "</div>";
} else {
    echo "<div class='box'>";
    echo "<h3>Väntande migrationer: " . count($pending) . "</h3>";

    foreach ($pending as $file) {
        echo "<h4>" . htmlspecialchars($file) . "</h4>";
        $fullPath = $migrationsDir . $file;

        if (!file_exists($fullPath)) {
            echo "<p class='error'>Fil hittades inte: $fullPath</p>";
            continue;
        }

        $sql = file_get_contents($fullPath);

        // Remove comment lines
        $sqlLines = explode("\n", $sql);
        $sqlLines = array_filter($sqlLines, fn($line) => !preg_match('/^\s*--/', $line));
        $sql = implode("\n", $sqlLines);

        // Split into statements
        $statements = array_filter(
            array_map('trim', explode(';', $sql)),
            fn($s) => !empty($s)
        );

        $successCount = 0;
        $skipCount = 0;
        $errorCount = 0;

        foreach ($statements as $statement) {
            if (empty(trim($statement))) continue;

            try {
                $pdo->exec($statement);
                $successCount++;
                echo "<p class='success'>✓ " . htmlspecialchars(substr($statement, 0, 80)) . "...</p>";
            } catch (Exception $e) {
                $errMsg = $e->getMessage();

                // Check for ignorable errors
                $ignorable = ['Duplicate', 'already exists', 'Unknown column', "Can't DROP"];
                $isIgnorable = false;
                foreach ($ignorable as $pattern) {
                    if (stripos($errMsg, $pattern) !== false) {
                        $isIgnorable = true;
                        break;
                    }
                }

                if ($isIgnorable) {
                    $skipCount++;
                    echo "<p class='warning'>⚠ Redan utförd: " . htmlspecialchars(substr($statement, 0, 60)) . "...</p>";
                } else {
                    $errorCount++;
                    echo "<p class='error'>✗ Fel: " . htmlspecialchars($errMsg) . "</p>";
                }
            }
        }

        // Log migration if no errors
        if ($errorCount === 0) {
            try {
                $logStmt = $pdo->prepare("INSERT IGNORE INTO migrations_log (migration_file) VALUES (?)");
                $logStmt->execute([$file]);
                echo "<p class='info'>Loggad som körd</p>";
            } catch (Exception $e) {
                echo "<p class='warning'>Kunde inte logga migration: " . $e->getMessage() . "</p>";
            }
        }

        echo "<p>Resultat: $successCount OK, $skipCount redan utförda, $errorCount fel</p>";
        echo "<hr>";
    }

    echo "</div>";
}

echo "<a href='/admin/run-migrations.php' class='btn'>Tillbaka till migrationer</a>";
echo "<a href='/admin/license-class-matrix.php' class='btn'>Licens-Klass Matris</a>";
echo "<a href='/admin/registration-rules.php' class='btn'>Registreringsregler</a>";

echo "</body></html>";
