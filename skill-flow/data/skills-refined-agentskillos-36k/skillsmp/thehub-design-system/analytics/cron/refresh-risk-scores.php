<?php
/**
 * Cron Job: Refresh Risk Scores
 *
 * Beraknar och cachar risk-scores for alla aktiva riders.
 * Ska koras dagligen eller veckvis.
 *
 * Korning:
 *   php analytics/cron/refresh-risk-scores.php
 *   php analytics/cron/refresh-risk-scores.php --year=2025
 *   php analytics/cron/refresh-risk-scores.php --force
 *
 * Crontab:
 *   0 3 * * * /usr/bin/php /path/to/thehub/analytics/cron/refresh-risk-scores.php
 *
 * @package TheHUB Analytics
 * @version 2.0
 */

$isCli = (php_sapi_name() === 'cli');

if (!$isCli) {
    require_once __DIR__ . '/../../config.php';
    require_once __DIR__ . '/../../includes/auth.php';

    if (!isLoggedIn() || !hasRole('admin')) {
        http_response_code(403);
        die('Atkomst nekad');
    }

    header('Content-Type: text/plain; charset=utf-8');
}

require_once __DIR__ . '/../includes/KPICalculator.php';
require_once __DIR__ . '/../includes/AnalyticsConfig.php';

function output(string $msg): void {
    global $isCli;
    echo $msg . ($isCli ? "\n" : "<br>\n");
    if (!$isCli) {
        ob_flush();
        flush();
    }
}

// Parse arguments
$options = getopt('', ['year:', 'force', 'limit:']);
$year = isset($options['year']) ? (int)$options['year'] : (int)date('Y');
$force = isset($options['force']);
$limit = isset($options['limit']) ? (int)$options['limit'] : null;

output("=== Risk Scores Refresh ===");
output("Ar: $year");
output("Force: " . ($force ? 'Ja' : 'Nej'));
output("");

try {
    if ($isCli) {
        require_once __DIR__ . '/../../config.php';
    }

    global $pdo;

    if (!$pdo) {
        throw new Exception("Ingen databasanslutning");
    }

    // Skapa tabell om den inte finns
    $pdo->exec("
        CREATE TABLE IF NOT EXISTS rider_risk_scores (
            id INT AUTO_INCREMENT PRIMARY KEY,
            rider_id INT NOT NULL,
            season_year SMALLINT NOT NULL,
            risk_score TINYINT NOT NULL DEFAULT 0,
            risk_level VARCHAR(20) GENERATED ALWAYS AS (
                CASE
                    WHEN risk_score >= 70 THEN 'critical'
                    WHEN risk_score >= 50 THEN 'high'
                    WHEN risk_score >= 30 THEN 'medium'
                    ELSE 'low'
                END
            ) STORED,
            factors JSON NULL,
            declining_events TINYINT(1) DEFAULT 0,
            no_recent_activity TINYINT(1) DEFAULT 0,
            class_downgrade TINYINT(1) DEFAULT 0,
            single_series TINYINT(1) DEFAULT 0,
            low_tenure TINYINT(1) DEFAULT 0,
            high_age_in_class TINYINT(1) DEFAULT 0,
            calculation_version VARCHAR(20) DEFAULT 'v2',
            calculated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE KEY unique_rider_year (rider_id, season_year),
            INDEX idx_risk_score (season_year, risk_score DESC)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
    ");

    // Rensa befintlig data for aret om force
    if ($force) {
        $stmt = $pdo->prepare("DELETE FROM rider_risk_scores WHERE season_year = ?");
        $stmt->execute([$year]);
        output("Rensade befintlig data for $year");
    }

    // Hamta aktiva riders for aret
    $sql = "
        SELECT DISTINCT rider_id
        FROM rider_yearly_stats
        WHERE season_year = ?
    ";
    if ($limit) {
        $sql .= " LIMIT $limit";
    }

    $stmt = $pdo->prepare($sql);
    $stmt->execute([$year]);
    $riderIds = $stmt->fetchAll(PDO::FETCH_COLUMN);

    $totalRiders = count($riderIds);
    output("Hittade $totalRiders riders att berakna");
    output("");

    $kpiCalc = new KPICalculator($pdo);

    // Forberedd insert
    $insertStmt = $pdo->prepare("
        INSERT INTO rider_risk_scores
        (rider_id, season_year, risk_score, factors, declining_events, no_recent_activity,
         class_downgrade, single_series, low_tenure, high_age_in_class, calculation_version)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON DUPLICATE KEY UPDATE
            risk_score = VALUES(risk_score),
            factors = VALUES(factors),
            declining_events = VALUES(declining_events),
            no_recent_activity = VALUES(no_recent_activity),
            class_downgrade = VALUES(class_downgrade),
            single_series = VALUES(single_series),
            low_tenure = VALUES(low_tenure),
            high_age_in_class = VALUES(high_age_in_class),
            calculation_version = VALUES(calculation_version),
            calculated_at = CURRENT_TIMESTAMP
    ");

    $processed = 0;
    $errors = 0;
    $startTime = microtime(true);

    foreach ($riderIds as $riderId) {
        try {
            $risk = $kpiCalc->calculateChurnRisk($riderId, $year);

            $insertStmt->execute([
                $riderId,
                $year,
                $risk['risk_score'],
                json_encode($risk['factors']),
                $risk['declining_events'] ? 1 : 0,
                $risk['no_recent_activity'] ? 1 : 0,
                $risk['class_downgrade'] ? 1 : 0,
                $risk['single_series'] ? 1 : 0,
                $risk['low_tenure'] ? 1 : 0,
                $risk['high_age_in_class'] ? 1 : 0,
                AnalyticsConfig::CALCULATION_VERSION
            ]);

            $processed++;

            // Progress
            if ($processed % 100 === 0) {
                $pct = round($processed / $totalRiders * 100);
                output("Progress: $processed / $totalRiders ($pct%)");
            }
        } catch (Exception $e) {
            $errors++;
            if ($errors <= 5) {
                output("Fel for rider $riderId: " . $e->getMessage());
            }
        }
    }

    $duration = round(microtime(true) - $startTime, 2);

    output("");
    output("=== KLART ===");
    output("Beraknade: $processed riders");
    output("Fel: $errors");
    output("Tid: {$duration}s");

    // Visa distribution
    $stmt = $pdo->prepare("
        SELECT risk_level, COUNT(*) as cnt
        FROM rider_risk_scores
        WHERE season_year = ?
        GROUP BY risk_level
    ");
    $stmt->execute([$year]);
    $dist = $stmt->fetchAll(PDO::FETCH_KEY_PAIR);

    output("");
    output("Distribution:");
    output("- Critical: " . ($dist['critical'] ?? 0));
    output("- High: " . ($dist['high'] ?? 0));
    output("- Medium: " . ($dist['medium'] ?? 0));
    output("- Low: " . ($dist['low'] ?? 0));

    // Logga i analytics_logs om tabellen finns
    try {
        $pdo->prepare("
            INSERT INTO analytics_logs (level, message, source, context)
            VALUES ('info', ?, 'refresh-risk-scores', ?)
        ")->execute([
            "Risk scores beraknade for $year: $processed riders",
            json_encode(['year' => $year, 'processed' => $processed, 'errors' => $errors, 'duration' => $duration])
        ]);
    } catch (Exception $e) {}

} catch (Exception $e) {
    output("");
    output("[FEL] " . $e->getMessage());
    exit(1);
}
