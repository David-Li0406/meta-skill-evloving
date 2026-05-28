<?php
/**
 * Robust SQL Runner for migrations
 * Hanterar kommentarer och strangkonstanter korrekt
 *
 * KRITISKT: Denna fil maste skapas FORST innan andra analytics-filer.
 * Alla setup-scripts anvander dessa funktioner.
 *
 * @package TheHUB Analytics
 * @version 1.0
 */

/**
 * Kor en SQL-fil och returnerar resultat
 * Hanterar:
 * - SQL-kommentarer (-- och block-kommentarer)
 * - Strangkonstanter med ' och "
 * - Flera statements separerade med ;
 *
 * @param PDO $pdo Databasanslutning
 * @param string $path Sokvag till SQL-fil
 * @return array Resultat med success, errors, skipped
 */
function runSqlFile(PDO $pdo, string $path): array {
    $result = ['success' => 0, 'errors' => [], 'skipped' => 0];

    if (!file_exists($path)) {
        $result['errors'][] = "Fil saknas: $path";
        return $result;
    }

    $sql = file_get_contents($path);
    $statements = splitSqlStatements($sql);

    foreach ($statements as $stmt) {
        $stmt = trim($stmt);
        if (empty($stmt)) continue;

        try {
            $pdo->exec($stmt);
            $result['success']++;
        } catch (PDOException $e) {
            // Ignorera "already exists" fel - tabellen/index finns redan
            $msg = $e->getMessage();
            if (strpos($msg, 'already exists') !== false ||
                strpos($msg, 'Duplicate') !== false ||
                strpos($msg, 'SQLSTATE[42S01]') !== false) {
                $result['skipped']++;
            } else {
                $result['errors'][] = $msg . " [SQL: " . substr($stmt, 0, 100) . "...]";
            }
        }
    }

    return $result;
}

/**
 * Splittra SQL pa ; men respektera strangar och kommentarer
 *
 * Anvander en state-machine for att korrekt hantera:
 * - Strangkonstanter ('...' och "...")
 * - Radkommentarer (--)
 * - Blockkommentarer
 * - Escaped quotes (\' och \")
 *
 * @param string $sql SQL-innehall
 * @return array Array av SQL-statements
 */
function splitSqlStatements(string $sql): array {
    $statements = [];
    $current = '';
    $inString = false;
    $stringChar = '';
    $inMultiComment = false;
    $len = strlen($sql);

    for ($i = 0; $i < $len; $i++) {
        $char = $sql[$i];
        $next = ($i + 1 < $len) ? $sql[$i + 1] : '';
        $prev = ($i > 0) ? $sql[$i - 1] : '';

        // Hantera radkommentarer (-- ...)
        // Endast om vi inte ar i en strang eller blockkommentar
        if (!$inString && !$inMultiComment && $char === '-' && $next === '-') {
            // Skippa till slutet av raden
            while ($i < $len && $sql[$i] !== "\n") {
                $i++;
            }
            continue;
        }

        // Hantera blockkommentarer (/* ... */)
        if (!$inString && !$inMultiComment && $char === '/' && $next === '*') {
            $inMultiComment = true;
            $i++; // Hoppa over *
            continue;
        }

        if ($inMultiComment && $char === '*' && $next === '/') {
            $inMultiComment = false;
            $i++; // Hoppa over /
            continue;
        }

        if ($inMultiComment) {
            continue;
        }

        // Hantera strangar - starta
        if (!$inString && ($char === "'" || $char === '"')) {
            $inString = true;
            $stringChar = $char;
            $current .= $char;
            continue;
        }

        // Hantera strangar - avsluta
        if ($inString && $char === $stringChar) {
            // Kolla om det ar en escaped quote
            if ($prev === '\\') {
                // Escaped quote, fortsatt i strang
                $current .= $char;
                continue;
            }
            // Kolla double-quote escape ('' eller "")
            if ($next === $stringChar) {
                $current .= $char . $next;
                $i++;
                continue;
            }
            // Slut pa strang
            $inString = false;
            $stringChar = '';
            $current .= $char;
            continue;
        }

        // Statement delimiter - endast om vi inte ar i strang
        if (!$inString && $char === ';') {
            $trimmed = trim($current);
            if (!empty($trimmed)) {
                $statements[] = $trimmed;
            }
            $current = '';
            continue;
        }

        $current .= $char;
    }

    // Sista statement utan ;
    $trimmed = trim($current);
    if (!empty($trimmed)) {
        $statements[] = $trimmed;
    }

    return $statements;
}

/**
 * Kolla om en kolumn finns i en tabell
 * Anvander INFORMATION_SCHEMA for webhotell-kompatibilitet
 *
 * @param PDO $pdo Databasanslutning
 * @param string $table Tabellnamn
 * @param string $column Kolumnnamn
 * @return bool True om kolumnen finns
 */
function columnExists(PDO $pdo, string $table, string $column): bool {
    $stmt = $pdo->prepare("
        SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS
        WHERE TABLE_SCHEMA = DATABASE()
        AND TABLE_NAME = ?
        AND COLUMN_NAME = ?
    ");
    $stmt->execute([$table, $column]);
    return (int)$stmt->fetchColumn() > 0;
}

/**
 * Kolla om ett index finns i en tabell
 *
 * @param PDO $pdo Databasanslutning
 * @param string $table Tabellnamn
 * @param string $indexName Indexnamn
 * @return bool True om indexet finns
 */
function indexExists(PDO $pdo, string $table, string $indexName): bool {
    $stmt = $pdo->prepare("
        SELECT COUNT(*) FROM INFORMATION_SCHEMA.STATISTICS
        WHERE TABLE_SCHEMA = DATABASE()
        AND TABLE_NAME = ?
        AND INDEX_NAME = ?
    ");
    $stmt->execute([$table, $indexName]);
    return (int)$stmt->fetchColumn() > 0;
}

/**
 * Kolla om en tabell finns
 *
 * @param PDO $pdo Databasanslutning
 * @param string $table Tabellnamn
 * @return bool True om tabellen finns
 */
function tableExists(PDO $pdo, string $table): bool {
    $stmt = $pdo->prepare("
        SELECT COUNT(*) FROM INFORMATION_SCHEMA.TABLES
        WHERE TABLE_SCHEMA = DATABASE()
        AND TABLE_NAME = ?
    ");
    $stmt->execute([$table]);
    return (int)$stmt->fetchColumn() > 0;
}

/**
 * Lagg till kolumn om den inte finns
 * Saker metod for webhotell som inte stoder IF NOT EXISTS
 *
 * @param PDO $pdo Databasanslutning
 * @param string $table Tabellnamn
 * @param string $column Kolumnnamn
 * @param string $definition Kolumndefinition (t.ex. "VARCHAR(100) NULL")
 * @return bool True om kolumnen lades till, false om den redan finns
 */
function addColumnIfNotExists(PDO $pdo, string $table, string $column, string $definition): bool {
    if (columnExists($pdo, $table, $column)) {
        return false; // Redan finns
    }

    $pdo->exec("ALTER TABLE `$table` ADD COLUMN `$column` $definition");
    return true;
}

/**
 * Lagg till index om det inte finns
 *
 * @param PDO $pdo Databasanslutning
 * @param string $table Tabellnamn
 * @param string $indexName Indexnamn
 * @param string $columns Kolumner att indexera (t.ex. "column1, column2")
 * @return bool True om indexet lades till, false om det redan finns
 */
function addIndexIfNotExists(PDO $pdo, string $table, string $indexName, string $columns): bool {
    if (indexExists($pdo, $table, $indexName)) {
        return false;
    }

    $pdo->exec("ALTER TABLE `$table` ADD INDEX `$indexName` ($columns)");
    return true;
}

/**
 * Logga ett meddelande till analytics_logs tabellen
 * Skapas for CLI-scripts som behover logga utan session
 *
 * @param PDO $pdo Databasanslutning
 * @param string $level Log level (debug, info, warn, error, critical)
 * @param string $message Meddelande
 * @param string|null $jobName Jobb/script-namn
 * @param array $context Extra kontext
 * @return bool True om loggning lyckades
 */
function logAnalytics(PDO $pdo, string $level, string $message, ?string $jobName = null, array $context = []): bool {
    // Kolla om analytics_logs tabellen finns
    if (!tableExists($pdo, 'analytics_logs')) {
        error_log("[Analytics] $level: $message (tabell saknas)");
        return false;
    }

    try {
        $stmt = $pdo->prepare("
            INSERT INTO analytics_logs (level, job_name, message, context)
            VALUES (?, ?, ?, ?)
        ");
        $stmt->execute([
            $level,
            $jobName,
            substr($message, 0, 500), // Max 500 tecken
            json_encode($context, JSON_UNESCAPED_UNICODE)
        ]);
        return true;
    } catch (PDOException $e) {
        error_log("[Analytics] Loggningsfel: " . $e->getMessage());
        return false;
    }
}

/**
 * Formatera resultat for CLI-output
 *
 * @param array $result Resultat fran runSqlFile
 * @return string Formaterad output
 */
function formatMigrationResult(array $result): string {
    $output = '';

    if ($result['success'] > 0) {
        $output .= "[OK] {$result['success']} statements korda\n";
    }

    if ($result['skipped'] > 0) {
        $output .= "[SKIP] {$result['skipped']} skippade (redan finns)\n";
    }

    if (!empty($result['errors'])) {
        $output .= "[FEL] " . count($result['errors']) . " fel:\n";
        foreach ($result['errors'] as $err) {
            $output .= "   - " . $err . "\n";
        }
    }

    return $output;
}
