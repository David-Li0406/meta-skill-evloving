<?php
/**
 * Lagg till analytics-kolumner pa series-tabellen
 * Anvander helper-funktioner for webhotell-kompatibilitet
 *
 * OBS: ALTER TABLE ... ADD COLUMN IF NOT EXISTS fungerar inte pa alla MySQL/MariaDB
 * Darfor anvands INFORMATION_SCHEMA for att kolla forst.
 *
 * @package TheHUB Analytics
 * @version 1.0
 */

// Ladda sql-runner om det inte redan ar laddat
if (!function_exists('addColumnIfNotExists')) {
    require_once __DIR__ . '/../includes/sql-runner.php';
}

/**
 * Kor series-utokningarna
 *
 * @param PDO $pdo Databasanslutning
 * @return array Resultat med 'added' och 'skipped' arrayer
 */
function runSeriesExtensions(PDO $pdo): array {
    $result = ['added' => [], 'skipped' => [], 'errors' => []];

    // Lagg till series_level - kategoriserar serier som national/regional/local/championship
    try {
        if (addColumnIfNotExists($pdo, 'series', 'series_level',
            "ENUM('national', 'regional', 'local', 'championship') DEFAULT 'regional' COMMENT 'Seriens niva'")) {
            $result['added'][] = 'series_level';
        } else {
            $result['skipped'][] = 'series_level';
        }
    } catch (PDOException $e) {
        $result['errors'][] = "series_level: " . $e->getMessage();
    }

    // Lagg till parent_series_id - for hierarkiska serier (t.ex. regional -> national)
    try {
        if (addColumnIfNotExists($pdo, 'series', 'parent_series_id',
            "INT NULL COMMENT 'Overordnad serie (for feeder-analys)'")) {
            $result['added'][] = 'parent_series_id';
        } else {
            $result['skipped'][] = 'parent_series_id';
        }
    } catch (PDOException $e) {
        $result['errors'][] = "parent_series_id: " . $e->getMessage();
    }

    // Lagg till region - geografisk kategorisering
    try {
        if (addColumnIfNotExists($pdo, 'series', 'region',
            "VARCHAR(100) NULL COMMENT 'Geografisk region (t.ex. Stockholm, Vastkusten)'")) {
            $result['added'][] = 'region';
        } else {
            $result['skipped'][] = 'region';
        }
    } catch (PDOException $e) {
        $result['errors'][] = "region: " . $e->getMessage();
    }

    // Lagg till analytics_enabled - flagga for om serien ska inkluderas i analytics
    try {
        if (addColumnIfNotExists($pdo, 'series', 'analytics_enabled',
            "TINYINT(1) DEFAULT 1 COMMENT '1 = inkludera i analytics'")) {
            $result['added'][] = 'analytics_enabled';
        } else {
            $result['skipped'][] = 'analytics_enabled';
        }
    } catch (PDOException $e) {
        $result['errors'][] = "analytics_enabled: " . $e->getMessage();
    }

    // Lagg till index for series_level
    try {
        if (addIndexIfNotExists($pdo, 'series', 'idx_series_level', 'series_level')) {
            $result['added'][] = 'idx_series_level (index)';
        } else {
            $result['skipped'][] = 'idx_series_level (index)';
        }
    } catch (PDOException $e) {
        $result['errors'][] = "idx_series_level: " . $e->getMessage();
    }

    // Lagg till index for parent_series_id
    try {
        if (addIndexIfNotExists($pdo, 'series', 'idx_parent_series', 'parent_series_id')) {
            $result['added'][] = 'idx_parent_series (index)';
        } else {
            $result['skipped'][] = 'idx_parent_series (index)';
        }
    } catch (PDOException $e) {
        $result['errors'][] = "idx_parent_series: " . $e->getMessage();
    }

    // Lagg till index for region
    try {
        if (addIndexIfNotExists($pdo, 'series', 'idx_region', 'region')) {
            $result['added'][] = 'idx_region (index)';
        } else {
            $result['skipped'][] = 'idx_region (index)';
        }
    } catch (PDOException $e) {
        $result['errors'][] = "idx_region: " . $e->getMessage();
    }

    return $result;
}

/**
 * Aterga till ursprungligt series-schema (for rollback)
 *
 * @param PDO $pdo Databasanslutning
 * @return array Resultat
 */
function rollbackSeriesExtensions(PDO $pdo): array {
    $result = ['removed' => [], 'errors' => []];

    $columns = ['series_level', 'parent_series_id', 'region', 'analytics_enabled'];
    $indexes = ['idx_series_level', 'idx_parent_series', 'idx_region'];

    // Ta bort index forst
    foreach ($indexes as $index) {
        try {
            if (indexExists($pdo, 'series', $index)) {
                $pdo->exec("ALTER TABLE series DROP INDEX $index");
                $result['removed'][] = "$index (index)";
            }
        } catch (PDOException $e) {
            $result['errors'][] = "$index: " . $e->getMessage();
        }
    }

    // Ta bort kolumner
    foreach ($columns as $column) {
        try {
            if (columnExists($pdo, 'series', $column)) {
                $pdo->exec("ALTER TABLE series DROP COLUMN $column");
                $result['removed'][] = $column;
            }
        } catch (PDOException $e) {
            $result['errors'][] = "$column: " . $e->getMessage();
        }
    }

    return $result;
}
