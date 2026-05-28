<?php
/**
 * Class Structure Analysis
 * Analyze how different events structure their classes:
 * - Number of stages per class
 * - Winner times vs average times
 * - Class participation patterns
 *
 * @package TheHUB Analytics
 */
require_once __DIR__ . '/../config.php';
require_once __DIR__ . '/../includes/auth.php';
require_once __DIR__ . '/../analytics/includes/KPICalculator.php';
requireLogin();

global $pdo;

// Get available brands using KPICalculator
$brands = [];
try {
    $kpiCalc = new KPICalculator($pdo);
    $brands = $kpiCalc->getAllBrands();
} catch (Exception $e) {
    error_log("Class Structure brand error: " . $e->getMessage());
}

// Get available years
$availableYears = [];
try {
    $stmt = $pdo->query("SELECT DISTINCT YEAR(date) as year FROM events WHERE date IS NOT NULL ORDER BY year DESC");
    $availableYears = $stmt->fetchAll(PDO::FETCH_COLUMN);
} catch (Exception $e) {}

// Parameters - single brand like analytics-trends.php
$selectedBrand = isset($_GET['brand']) && $_GET['brand'] !== '' ? (int)$_GET['brand'] : null;
$selectedYear = isset($_GET['year']) ? (int)$_GET['year'] : ($availableYears[0] ?? (int)date('Y'));

// Build query for class structure analysis
$classData = [];
$eventSummary = [];

try {
    // Build brand filter (single brand, like analytics-trends.php)
    $brandFilter = '';
    $brandParams = [];
    if ($selectedBrand !== null) {
        $brandFilter = "AND s.brand_id = ?";
        $brandParams = [$selectedBrand];
    }

    // Get class structure data per event
    $sql = "
        SELECT
            e.id as event_id,
            e.name as event_name,
            e.date as event_date,
            s.name as series_name,
            sb.name as brand_name,
            sb.accent_color as brand_color,
            COALESCE(r.class_id, 0) as class_id,
            COALESCE(cl.display_name, cl.name, CASE WHEN r.class_id IS NULL THEN 'Okand klass' ELSE CONCAT('Klass ', r.class_id) END) as class_name,
            COALESCE(cl.sort_order, 9999) as class_sort_order,
            COUNT(DISTINCT r.cyclist_id) as participants,

            -- Winner time (fastest finished time - exclude DNF/DNS/DQ)
            -- Use custom time parsing to handle MM:SS.ms format
            MIN(CASE WHEN (r.status IS NULL OR LOWER(r.status) NOT IN ('dnf', 'dns', 'dq', 'dsq', 'did not finish', 'did not start', 'disqualified'))
                     AND r.finish_time IS NOT NULL
                     AND r.finish_time != ''
                     AND r.finish_time NOT LIKE '%DNF%'
                     AND r.finish_time NOT LIKE '%DNS%'
                THEN
                    CASE
                        -- HH:MM:SS or HH:MM:SS.ms format
                        WHEN r.finish_time REGEXP '^[0-9]+:[0-9]+:[0-9]' THEN TIME_TO_SEC(r.finish_time)
                        -- MM:SS.ms or MM:SS format (no hours)
                        WHEN r.finish_time REGEXP '^[0-9]+:[0-9]' THEN
                            CAST(SUBSTRING_INDEX(r.finish_time, ':', 1) AS DECIMAL(10,3)) * 60 +
                            CAST(SUBSTRING_INDEX(SUBSTRING_INDEX(r.finish_time, ':', -1), '.', 1) AS DECIMAL(10,3)) +
                            COALESCE(CAST(CONCAT('0.', SUBSTRING_INDEX(r.finish_time, '.', -1)) AS DECIMAL(10,3)), 0)
                        ELSE TIME_TO_SEC(r.finish_time)
                    END
                END) as winner_time_sec,

            -- Average time (finished only - exclude DNF/DNS/DQ)
            AVG(CASE WHEN (r.status IS NULL OR LOWER(r.status) NOT IN ('dnf', 'dns', 'dq', 'dsq', 'did not finish', 'did not start', 'disqualified'))
                     AND r.finish_time IS NOT NULL
                     AND r.finish_time != ''
                     AND r.finish_time NOT LIKE '%DNF%'
                     AND r.finish_time NOT LIKE '%DNS%'
                THEN
                    CASE
                        WHEN r.finish_time REGEXP '^[0-9]+:[0-9]+:[0-9]' THEN TIME_TO_SEC(r.finish_time)
                        WHEN r.finish_time REGEXP '^[0-9]+:[0-9]' THEN
                            CAST(SUBSTRING_INDEX(r.finish_time, ':', 1) AS DECIMAL(10,3)) * 60 +
                            CAST(SUBSTRING_INDEX(SUBSTRING_INDEX(r.finish_time, ':', -1), '.', 1) AS DECIMAL(10,3)) +
                            COALESCE(CAST(CONCAT('0.', SUBSTRING_INDEX(r.finish_time, '.', -1)) AS DECIMAL(10,3)), 0)
                        ELSE TIME_TO_SEC(r.finish_time)
                    END
                END) as avg_time_sec,

            -- Median approximation (simple)
            COUNT(CASE WHEN r.status IS NULL OR LOWER(r.status) NOT IN ('dnf', 'dns', 'dq', 'dsq', 'did not finish', 'did not start', 'disqualified') THEN 1 END) as finished_count,

            -- Count stages used (non-null ss columns)
            MAX(
                (CASE WHEN r.ss1 IS NOT NULL AND r.ss1 != '' AND r.ss1 != '00:00:00' THEN 1 ELSE 0 END) +
                (CASE WHEN r.ss2 IS NOT NULL AND r.ss2 != '' AND r.ss2 != '00:00:00' THEN 1 ELSE 0 END) +
                (CASE WHEN r.ss3 IS NOT NULL AND r.ss3 != '' AND r.ss3 != '00:00:00' THEN 1 ELSE 0 END) +
                (CASE WHEN r.ss4 IS NOT NULL AND r.ss4 != '' AND r.ss4 != '00:00:00' THEN 1 ELSE 0 END) +
                (CASE WHEN r.ss5 IS NOT NULL AND r.ss5 != '' AND r.ss5 != '00:00:00' THEN 1 ELSE 0 END) +
                (CASE WHEN r.ss6 IS NOT NULL AND r.ss6 != '' AND r.ss6 != '00:00:00' THEN 1 ELSE 0 END) +
                (CASE WHEN r.ss7 IS NOT NULL AND r.ss7 != '' AND r.ss7 != '00:00:00' THEN 1 ELSE 0 END) +
                (CASE WHEN r.ss8 IS NOT NULL AND r.ss8 != '' AND r.ss8 != '00:00:00' THEN 1 ELSE 0 END) +
                (CASE WHEN r.ss9 IS NOT NULL AND r.ss9 != '' AND r.ss9 != '00:00:00' THEN 1 ELSE 0 END) +
                (CASE WHEN r.ss10 IS NOT NULL AND r.ss10 != '' AND r.ss10 != '00:00:00' THEN 1 ELSE 0 END) +
                (CASE WHEN r.ss11 IS NOT NULL AND r.ss11 != '' AND r.ss11 != '00:00:00' THEN 1 ELSE 0 END) +
                (CASE WHEN r.ss12 IS NOT NULL AND r.ss12 != '' AND r.ss12 != '00:00:00' THEN 1 ELSE 0 END) +
                (CASE WHEN r.ss13 IS NOT NULL AND r.ss13 != '' AND r.ss13 != '00:00:00' THEN 1 ELSE 0 END) +
                (CASE WHEN r.ss14 IS NOT NULL AND r.ss14 != '' AND r.ss14 != '00:00:00' THEN 1 ELSE 0 END) +
                (CASE WHEN r.ss15 IS NOT NULL AND r.ss15 != '' AND r.ss15 != '00:00:00' THEN 1 ELSE 0 END)
            ) as stage_count,

            -- Which specific stages were used (bitmask style concat)
            CONCAT_WS(',',
                IF(MAX(CASE WHEN r.ss1 IS NOT NULL AND r.ss1 != '' AND r.ss1 != '00:00:00' THEN 1 END) = 1, 'SS1', NULL),
                IF(MAX(CASE WHEN r.ss2 IS NOT NULL AND r.ss2 != '' AND r.ss2 != '00:00:00' THEN 1 END) = 1, 'SS2', NULL),
                IF(MAX(CASE WHEN r.ss3 IS NOT NULL AND r.ss3 != '' AND r.ss3 != '00:00:00' THEN 1 END) = 1, 'SS3', NULL),
                IF(MAX(CASE WHEN r.ss4 IS NOT NULL AND r.ss4 != '' AND r.ss4 != '00:00:00' THEN 1 END) = 1, 'SS4', NULL),
                IF(MAX(CASE WHEN r.ss5 IS NOT NULL AND r.ss5 != '' AND r.ss5 != '00:00:00' THEN 1 END) = 1, 'SS5', NULL),
                IF(MAX(CASE WHEN r.ss6 IS NOT NULL AND r.ss6 != '' AND r.ss6 != '00:00:00' THEN 1 END) = 1, 'SS6', NULL),
                IF(MAX(CASE WHEN r.ss7 IS NOT NULL AND r.ss7 != '' AND r.ss7 != '00:00:00' THEN 1 END) = 1, 'SS7', NULL),
                IF(MAX(CASE WHEN r.ss8 IS NOT NULL AND r.ss8 != '' AND r.ss8 != '00:00:00' THEN 1 END) = 1, 'SS8', NULL),
                IF(MAX(CASE WHEN r.ss9 IS NOT NULL AND r.ss9 != '' AND r.ss9 != '00:00:00' THEN 1 END) = 1, 'SS9', NULL),
                IF(MAX(CASE WHEN r.ss10 IS NOT NULL AND r.ss10 != '' AND r.ss10 != '00:00:00' THEN 1 END) = 1, 'SS10', NULL),
                IF(MAX(CASE WHEN r.ss11 IS NOT NULL AND r.ss11 != '' AND r.ss11 != '00:00:00' THEN 1 END) = 1, 'SS11', NULL),
                IF(MAX(CASE WHEN r.ss12 IS NOT NULL AND r.ss12 != '' AND r.ss12 != '00:00:00' THEN 1 END) = 1, 'SS12', NULL),
                IF(MAX(CASE WHEN r.ss13 IS NOT NULL AND r.ss13 != '' AND r.ss13 != '00:00:00' THEN 1 END) = 1, 'SS13', NULL),
                IF(MAX(CASE WHEN r.ss14 IS NOT NULL AND r.ss14 != '' AND r.ss14 != '00:00:00' THEN 1 END) = 1, 'SS14', NULL),
                IF(MAX(CASE WHEN r.ss15 IS NOT NULL AND r.ss15 != '' AND r.ss15 != '00:00:00' THEN 1 END) = 1, 'SS15', NULL)
            ) as stages_used,

            -- Time spread (difference between slowest and fastest finisher)
            (
                MAX(CASE WHEN (r.status IS NULL OR LOWER(r.status) NOT IN ('dnf', 'dns', 'dq', 'dsq', 'did not finish', 'did not start', 'disqualified'))
                         AND r.finish_time IS NOT NULL AND r.finish_time != ''
                         AND r.finish_time NOT LIKE '%DNF%' AND r.finish_time NOT LIKE '%DNS%'
                    THEN
                        CASE
                            WHEN r.finish_time REGEXP '^[0-9]+:[0-9]+:[0-9]' THEN TIME_TO_SEC(r.finish_time)
                            WHEN r.finish_time REGEXP '^[0-9]+:[0-9]' THEN
                                CAST(SUBSTRING_INDEX(r.finish_time, ':', 1) AS DECIMAL(10,3)) * 60 +
                                CAST(SUBSTRING_INDEX(SUBSTRING_INDEX(r.finish_time, ':', -1), '.', 1) AS DECIMAL(10,3)) +
                                COALESCE(CAST(CONCAT('0.', SUBSTRING_INDEX(r.finish_time, '.', -1)) AS DECIMAL(10,3)), 0)
                            ELSE TIME_TO_SEC(r.finish_time)
                        END
                    END)
                -
                MIN(CASE WHEN (r.status IS NULL OR LOWER(r.status) NOT IN ('dnf', 'dns', 'dq', 'dsq', 'did not finish', 'did not start', 'disqualified'))
                         AND r.finish_time IS NOT NULL AND r.finish_time != ''
                         AND r.finish_time NOT LIKE '%DNF%' AND r.finish_time NOT LIKE '%DNS%'
                    THEN
                        CASE
                            WHEN r.finish_time REGEXP '^[0-9]+:[0-9]+:[0-9]' THEN TIME_TO_SEC(r.finish_time)
                            WHEN r.finish_time REGEXP '^[0-9]+:[0-9]' THEN
                                CAST(SUBSTRING_INDEX(r.finish_time, ':', 1) AS DECIMAL(10,3)) * 60 +
                                CAST(SUBSTRING_INDEX(SUBSTRING_INDEX(r.finish_time, ':', -1), '.', 1) AS DECIMAL(10,3)) +
                                COALESCE(CAST(CONCAT('0.', SUBSTRING_INDEX(r.finish_time, '.', -1)) AS DECIMAL(10,3)), 0)
                            ELSE TIME_TO_SEC(r.finish_time)
                        END
                    END)
            ) as time_spread_sec,

            -- Venue info for tracking min/max locations
            v.name as venue_name

        FROM results r
        JOIN events e ON r.event_id = e.id
        JOIN series_events se ON se.event_id = e.id
        JOIN series s ON se.series_id = s.id
        LEFT JOIN series_brands sb ON s.brand_id = sb.id
        LEFT JOIN classes cl ON r.class_id = cl.id
        LEFT JOIN venues v ON e.venue_id = v.id
        WHERE YEAR(e.date) = ?
        $brandFilter
        GROUP BY e.id, COALESCE(r.class_id, 0)
        ORDER BY e.date DESC, class_sort_order ASC, class_name ASC
    ";

    $params = array_merge([$selectedYear], $brandParams);
    $stmt = $pdo->prepare($sql);
    $stmt->execute($params);
    $classData = $stmt->fetchAll(PDO::FETCH_ASSOC);

    // Group data by event for summary
    foreach ($classData as $row) {
        $eventId = $row['event_id'];
        if (!isset($eventSummary[$eventId])) {
            $eventSummary[$eventId] = [
                'event_name' => $row['event_name'],
                'event_date' => $row['event_date'],
                'series_name' => $row['series_name'],
                'brand_name' => $row['brand_name'],
                'brand_color' => $row['brand_color'],
                'classes' => [],
                'total_participants' => 0,
                'class_count' => 0
            ];
        }
        $eventSummary[$eventId]['classes'][] = $row;
        $eventSummary[$eventId]['total_participants'] += $row['participants'];
        $eventSummary[$eventId]['class_count']++;
    }

} catch (Exception $e) {
    error_log("Class Structure query error: " . $e->getMessage());
}

// Brand comparison data (shows when no brand is selected, or as overview)
$brandComparison = [];
try {
    $compSql = "
        SELECT
            sb.id as brand_id,
            sb.name as brand_name,
            sb.accent_color as brand_color,
            YEAR(e.date) as event_year,
            COUNT(DISTINCT e.id) as event_count,
            COUNT(DISTINCT r.cyclist_id) as total_participants,

            -- Average winner time across all events (finished only - exclude DNF/DNS/DQ)
            AVG(
                CASE WHEN (r.status IS NULL OR LOWER(r.status) NOT IN ('dnf', 'dns', 'dq', 'dsq', 'did not finish', 'did not start', 'disqualified'))
                     AND r.finish_time IS NOT NULL
                     AND r.finish_time != ''
                     AND r.finish_time NOT LIKE '%DNF%'
                     AND r.finish_time NOT LIKE '%DNS%'
                THEN
                    CASE
                        WHEN r.finish_time REGEXP '^[0-9]+:[0-9]+:[0-9]' THEN TIME_TO_SEC(r.finish_time)
                        WHEN r.finish_time REGEXP '^[0-9]+:[0-9]' THEN
                            CAST(SUBSTRING_INDEX(r.finish_time, ':', 1) AS DECIMAL(10,3)) * 60 +
                            CAST(SUBSTRING_INDEX(SUBSTRING_INDEX(r.finish_time, ':', -1), '.', 1) AS DECIMAL(10,3)) +
                            COALESCE(CAST(CONCAT('0.', SUBSTRING_INDEX(r.finish_time, '.', -1)) AS DECIMAL(10,3)), 0)
                        ELSE TIME_TO_SEC(r.finish_time)
                    END
                END
            ) as avg_winner_time_sec,

            -- Average stage count
            AVG(
                (CASE WHEN r.ss1 IS NOT NULL AND r.ss1 != '' AND r.ss1 != '00:00:00' THEN 1 ELSE 0 END) +
                (CASE WHEN r.ss2 IS NOT NULL AND r.ss2 != '' AND r.ss2 != '00:00:00' THEN 1 ELSE 0 END) +
                (CASE WHEN r.ss3 IS NOT NULL AND r.ss3 != '' AND r.ss3 != '00:00:00' THEN 1 ELSE 0 END) +
                (CASE WHEN r.ss4 IS NOT NULL AND r.ss4 != '' AND r.ss4 != '00:00:00' THEN 1 ELSE 0 END) +
                (CASE WHEN r.ss5 IS NOT NULL AND r.ss5 != '' AND r.ss5 != '00:00:00' THEN 1 ELSE 0 END) +
                (CASE WHEN r.ss6 IS NOT NULL AND r.ss6 != '' AND r.ss6 != '00:00:00' THEN 1 ELSE 0 END) +
                (CASE WHEN r.ss7 IS NOT NULL AND r.ss7 != '' AND r.ss7 != '00:00:00' THEN 1 ELSE 0 END) +
                (CASE WHEN r.ss8 IS NOT NULL AND r.ss8 != '' AND r.ss8 != '00:00:00' THEN 1 ELSE 0 END)
            ) as avg_stages,

            -- Count unique classes used
            COUNT(DISTINCT COALESCE(r.class_id, 0)) as unique_classes

        FROM results r
        JOIN events e ON r.event_id = e.id
        JOIN series_events se ON se.event_id = e.id
        JOIN series s ON se.series_id = s.id
        JOIN series_brands sb ON s.brand_id = sb.id
        WHERE YEAR(e.date) = ?
        GROUP BY sb.id, YEAR(e.date)
        ORDER BY sb.name ASC
    ";

    $stmt = $pdo->prepare($compSql);
    $stmt->execute([$selectedYear]);
    $brandComparison = $stmt->fetchAll(PDO::FETCH_ASSOC);

} catch (Exception $e) {
    error_log("Brand comparison error: " . $e->getMessage());
}

// Historical data by venue (when brand is selected)
// Now fetches class-specific winner times
$venueHistory = [];
if ($selectedBrand !== null) {
    try {
        // Get winner times per class per event per venue
        $histSql = "
            SELECT
                v.id as venue_id,
                v.name as venue_name,
                v.city as venue_city,
                YEAR(e.date) as event_year,
                e.id as event_id,
                e.name as event_name,
                e.date as event_date,
                COALESCE(cl.display_name, cl.name) as class_name,
                COUNT(DISTINCT r.cyclist_id) as class_participants,
                MIN(CASE WHEN (r.status IS NULL OR LOWER(r.status) NOT IN ('dnf', 'dns', 'dq', 'dsq', 'did not finish', 'did not start', 'disqualified'))
                         AND r.finish_time IS NOT NULL
                         AND r.finish_time != ''
                         AND r.finish_time NOT LIKE '%DNF%'
                         AND r.finish_time NOT LIKE '%DNS%'
                    THEN
                        CASE
                            WHEN r.finish_time REGEXP '^[0-9]+:[0-9]+:[0-9]' THEN TIME_TO_SEC(r.finish_time)
                            WHEN r.finish_time REGEXP '^[0-9]+:[0-9]' THEN
                                CAST(SUBSTRING_INDEX(r.finish_time, ':', 1) AS DECIMAL(10,3)) * 60 +
                                CAST(SUBSTRING_INDEX(SUBSTRING_INDEX(r.finish_time, ':', -1), '.', 1) AS DECIMAL(10,3)) +
                                COALESCE(CAST(CONCAT('0.', SUBSTRING_INDEX(r.finish_time, '.', -1)) AS DECIMAL(10,3)), 0)
                            ELSE TIME_TO_SEC(r.finish_time)
                        END
                    END) as winner_time_sec
            FROM results r
            JOIN events e ON r.event_id = e.id
            JOIN series_events se ON se.event_id = e.id
            JOIN series s ON se.series_id = s.id
            LEFT JOIN venues v ON e.venue_id = v.id
            LEFT JOIN classes cl ON r.class_id = cl.id
            WHERE s.brand_id = ?
              AND v.id IS NOT NULL
            GROUP BY v.id, e.id, r.class_id
            ORDER BY v.name ASC, event_year ASC
        ";

        $stmt = $pdo->prepare($histSql);
        $stmt->execute([$selectedBrand]);
        $histData = $stmt->fetchAll(PDO::FETCH_ASSOC);

        // DEBUG: Log all classes found with their winner times
        $debugClasses = [];
        foreach ($histData as $row) {
            $key = $row['event_year'] . ' - ' . $row['class_name'];
            if (!isset($debugClasses[$key])) {
                $debugClasses[$key] = $row['winner_time_sec'];
            }
        }
        error_log("VENUE HISTORY DEBUG - Classes found: " . print_r($debugClasses, true));

        // Define class mappings for display (expanded to match various naming conventions)
        $targetClasses = [
            'h_elit' => ['Herrar Elit', 'H Elit', 'Herrar elit', 'Men Elite', 'Herr Elit', 'H-Elit'],
            'd_elit' => ['Damer Elit', 'D Elit', 'Damer elit', 'Women Elite', 'Dam Elit', 'D-Elit'],
            'p15_16' => ['P15-16', 'Pojkar 15-16', 'Pojkar  15-16', 'P 15-16', 'Pojkar P15-16', 'P15/16', 'Boys 15-16', 'Junior P15-16', 'Pojkar, 15-16', 'Pojkar15-16'],
            'p13_14' => ['P13-14', 'Pojkar 13-14', 'P 13-14', 'Pojkar P13-14', 'P13/14', 'Boys 13-14', 'Junior P13-14', 'Pojkar, 13-14'],
        ];
        // Master classes - average of whichever were run that year
        $masterClasses = [
            'Master Herrar 30+',
            'Master Herrar 35+',
            'Master Herrar 40+',
            'Master Herrar 45+',
            'Master Herrar 50+'
        ];

        // Group by venue and year, then aggregate class times
        $tempData = [];
        foreach ($histData as $row) {
            $venueId = $row['venue_id'];
            $year = $row['event_year'];
            $className = $row['class_name'];

            if (!isset($tempData[$venueId])) {
                $venueName = $row['venue_name'];
                if ($row['venue_city']) {
                    $venueName .= ' (' . $row['venue_city'] . ')';
                }
                $tempData[$venueId] = [
                    'name' => $venueName,
                    'years' => []
                ];
            }

            if (!isset($tempData[$venueId]['years'][$year])) {
                $tempData[$venueId]['years'][$year] = [
                    'event_name' => $row['event_name'],
                    'event_date' => $row['event_date'],
                    'participants' => 0,
                    'h_elit' => null,
                    'd_elit' => null,
                    'p15_16' => null,
                    'p13_14' => null,
                    'master_times' => []
                ];
            }

            $tempData[$venueId]['years'][$year]['participants'] += $row['class_participants'];

            // Match class to target categories
            if ($className && $row['winner_time_sec'] > 0) {
                $classNameTrimmed = trim($className);
                $classLower = strtolower($classNameTrimmed);
                $matched = false;

                // First try exact match (with trim)
                foreach ($targetClasses as $key => $names) {
                    foreach ($names as $name) {
                        if (strcasecmp($classNameTrimmed, trim($name)) === 0) {
                            $tempData[$venueId]['years'][$year][$key] = $row['winner_time_sec'];
                            $matched = true;
                            break 2;
                        }
                    }
                }

                // Fallback: pattern-based matching if no exact match
                if (!$matched) {
                    // P15-16 pattern: contains "15-16" or "15/16", or contains both "15" and "16" with pojk/p prefix
                    // Also match "Ungdom 15-16", "U15-16", etc.
                    if (strpos($classLower, '15-16') !== false || strpos($classLower, '15/16') !== false ||
                        (strpos($classLower, 'u15') !== false && strpos($classLower, '16') !== false) ||
                        ((strpos($classLower, '15') !== false && strpos($classLower, '16') !== false) &&
                         (strpos($classLower, 'pojk') !== false || strpos($classLower, 'p1') !== false ||
                          strpos($classLower, 'p 1') !== false || strpos($classLower, 'ungdom') !== false))) {
                        // But exclude if it's clearly a different age group
                        if (strpos($classLower, '13') === false && strpos($classLower, '17') === false) {
                            $tempData[$venueId]['years'][$year]['p15_16'] = $row['winner_time_sec'];
                            $matched = true;
                        }
                    }
                    // P13-14 pattern
                    if (!$matched && (strpos($classLower, '13-14') !== false || strpos($classLower, '13/14') !== false ||
                            (strpos($classLower, 'u13') !== false && strpos($classLower, '14') !== false) ||
                            ((strpos($classLower, '13') !== false && strpos($classLower, '14') !== false) &&
                             (strpos($classLower, 'pojk') !== false || strpos($classLower, 'p1') !== false ||
                              strpos($classLower, 'p 1') !== false || strpos($classLower, 'ungdom') !== false)))) {
                        if (strpos($classLower, '15') === false) {
                            $tempData[$venueId]['years'][$year]['p13_14'] = $row['winner_time_sec'];
                            $matched = true;
                        }
                    }
                    // Herrar Elit pattern
                    if (!$matched && (strpos($classLower, 'herr') !== false || strpos($classLower, 'h ') === 0 || strpos($classLower, 'h-') === 0) &&
                            strpos($classLower, 'elit') !== false) {
                        $tempData[$venueId]['years'][$year]['h_elit'] = $row['winner_time_sec'];
                        $matched = true;
                    }
                    // Damer Elit pattern
                    if (!$matched && (strpos($classLower, 'dam') !== false || strpos($classLower, 'd ') === 0 || strpos($classLower, 'd-') === 0) &&
                            strpos($classLower, 'elit') !== false) {
                        $tempData[$venueId]['years'][$year]['d_elit'] = $row['winner_time_sec'];
                        $matched = true;
                    }
                }

                // Check for master classes (always check, not mutually exclusive with above)
                foreach ($masterClasses as $masterName) {
                    if (strcasecmp($className, $masterName) === 0) {
                        $tempData[$venueId]['years'][$year]['master_times'][] = $row['winner_time_sec'];
                        break;
                    }
                }
            }
        }

        // Calculate master averages and build final structure
        foreach ($tempData as $venueId => $venueData) {
            $venueHistory[$venueId] = [
                'name' => $venueData['name'],
                'years' => []
            ];
            foreach ($venueData['years'] as $year => $yearData) {
                $masterAvg = null;
                if (!empty($yearData['master_times'])) {
                    $masterAvg = array_sum($yearData['master_times']) / count($yearData['master_times']);
                }
                $venueHistory[$venueId]['years'][$year] = [
                    'event_name' => $yearData['event_name'],
                    'event_date' => $yearData['event_date'],
                    'participants' => $yearData['participants'],
                    'h_elit' => $yearData['h_elit'],
                    'd_elit' => $yearData['d_elit'],
                    'p15_16' => $yearData['p15_16'],
                    'p13_14' => $yearData['p13_14'],
                    'master' => $masterAvg
                ];
            }
        }

        // Sort by number of years (most history first)
        uasort($venueHistory, function($a, $b) {
            return count($b['years']) - count($a['years']);
        });

    } catch (Exception $e) {
        error_log("Venue history error: " . $e->getMessage());
    }
}

// Calculate aggregated stats per class across all events
$classAggregates = [];
foreach ($classData as $row) {
    $className = $row['class_name'];
    if (!isset($classAggregates[$className])) {
        $classAggregates[$className] = [
            'sort_order' => $row['class_sort_order'],
            'event_count' => 0,
            'total_participants' => 0,
            'avg_participants' => 0,
            'total_stages' => 0,
            'avg_winner_time' => 0,
            'winner_times' => [],
            'stage_counts' => [],
            'time_venues' => [] // Track venue for each time
        ];
    }
    $classAggregates[$className]['event_count']++;
    $classAggregates[$className]['total_participants'] += $row['participants'];
    if ($row['stage_count'] > 0) {
        $classAggregates[$className]['stage_counts'][] = $row['stage_count'];
    }
    if ($row['winner_time_sec'] > 0) {
        $classAggregates[$className]['winner_times'][] = $row['winner_time_sec'];
        $classAggregates[$className]['time_venues'][$row['winner_time_sec']] = $row['venue_name'] ?: $row['event_name'];
    }
}

// Calculate averages
foreach ($classAggregates as $className => &$agg) {
    $agg['avg_participants'] = $agg['event_count'] > 0
        ? round($agg['total_participants'] / $agg['event_count'], 1)
        : 0;
    $agg['avg_stages'] = !empty($agg['stage_counts'])
        ? round(array_sum($agg['stage_counts']) / count($agg['stage_counts']), 1)
        : 0;
    $agg['avg_winner_time'] = !empty($agg['winner_times'])
        ? array_sum($agg['winner_times']) / count($agg['winner_times'])
        : 0;
    $agg['min_winner_time'] = !empty($agg['winner_times'])
        ? min($agg['winner_times'])
        : 0;
    $agg['max_winner_time'] = !empty($agg['winner_times'])
        ? max($agg['winner_times'])
        : 0;
    // Get venue names for min/max times
    $agg['min_venue'] = $agg['min_winner_time'] > 0 && isset($agg['time_venues'][$agg['min_winner_time']])
        ? $agg['time_venues'][$agg['min_winner_time']]
        : '';
    $agg['max_venue'] = $agg['max_winner_time'] > 0 && isset($agg['time_venues'][$agg['max_winner_time']])
        ? $agg['time_venues'][$agg['max_winner_time']]
        : '';
}
unset($agg);

// Sort by class sort_order (same as classes.php)
uasort($classAggregates, function($a, $b) {
    return $a['sort_order'] - $b['sort_order'];
});

// Helper function to format time
function formatTime($seconds) {
    if (!$seconds || $seconds <= 0) return '-';
    $seconds = (int) $seconds; // Cast to int to avoid float warnings
    $hours = floor($seconds / 3600);
    $minutes = floor(($seconds % 3600) / 60);
    $secs = $seconds % 60;
    if ($hours > 0) {
        return sprintf('%d:%02d:%02d', $hours, $minutes, $secs);
    }
    return sprintf('%d:%02d', $minutes, $secs);
}

// Page config
$page_title = 'Klassanalys';
$breadcrumbs = [
    ['label' => 'Analytics', 'url' => '/admin/analytics-dashboard.php'],
    ['label' => 'Klassanalys']
];

$page_actions = '';

include __DIR__ . '/components/unified-layout.php';
?>

<style>
.stats-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
    gap: var(--space-md);
    margin-bottom: var(--space-xl);
}
.stat-card {
    background: var(--color-bg-surface);
    border: 1px solid var(--color-border);
    border-radius: var(--radius-md);
    padding: var(--space-lg);
    text-align: center;
}
.stat-value {
    font-size: 1.75rem;
    font-weight: 700;
    color: var(--color-accent);
}
.stat-label {
    font-size: 0.8rem;
    color: var(--color-text-muted);
    margin-top: var(--space-xs);
}

.event-card {
    background: var(--color-bg-surface);
    border: 1px solid var(--color-border);
    border-radius: var(--radius-md);
    margin-bottom: var(--space-md);
    overflow: hidden;
}
.event-header {
    padding: var(--space-md) var(--space-lg);
    background: var(--color-bg-page);
    border-bottom: 1px solid var(--color-border);
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
    gap: var(--space-sm);
}
.event-title {
    font-weight: 600;
    color: var(--color-text-primary);
}
.event-meta {
    display: flex;
    gap: var(--space-md);
    font-size: 0.85rem;
    color: var(--color-text-muted);
}
.event-meta span {
    display: flex;
    align-items: center;
    gap: var(--space-xs);
}
.brand-tag {
    padding: 2px 8px;
    border-radius: var(--radius-full);
    font-size: 0.7rem;
    font-weight: 600;
    color: white;
}

.class-table {
    width: 100%;
    border-collapse: collapse;
}
.class-table th,
.class-table td {
    padding: var(--space-sm) var(--space-md);
    text-align: left;
    border-bottom: 1px solid var(--color-border);
}
.class-table th {
    background: var(--color-bg-page);
    font-size: 0.75rem;
    font-weight: 600;
    color: var(--color-text-muted);
    text-transform: uppercase;
}
.class-table td {
    font-size: 0.875rem;
}
.class-table tr:last-child td {
    border-bottom: none;
}
.class-name {
    font-weight: 500;
    color: var(--color-text-primary);
}
.time-cell {
    font-family: monospace;
    color: var(--color-accent);
}
.stage-badge {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    min-width: 28px;
    height: 28px;
    padding: 0 var(--space-xs);
    background: var(--color-accent-light);
    color: var(--color-accent);
    border-radius: var(--radius-full);
    font-weight: 600;
    font-size: 0.85rem;
}
.stages-list {
    display: flex;
    align-items: center;
    gap: var(--space-sm);
    flex-wrap: wrap;
}
.stages-detail {
    font-size: 0.75rem;
    color: var(--color-text-muted);
    font-family: monospace;
}

.aggregate-section {
    margin-top: var(--space-2xl);
}
.aggregate-table {
    width: 100%;
    border-collapse: collapse;
    background: var(--color-bg-surface);
    border: 1px solid var(--color-border);
    border-radius: var(--radius-md);
    overflow: hidden;
}
.aggregate-table th,
.aggregate-table td {
    padding: var(--space-md);
    text-align: left;
    border-bottom: 1px solid var(--color-border);
}
.aggregate-table th {
    background: var(--color-bg-page);
    font-size: 0.75rem;
    font-weight: 600;
    color: var(--color-text-muted);
    text-transform: uppercase;
}
.aggregate-table tr:last-child td {
    border-bottom: none;
}

.no-data {
    text-align: center;
    padding: var(--space-2xl);
    color: var(--color-text-muted);
}

/* Historical trends section */
.location-section {
    margin-bottom: var(--space-xl);
}
.location-header {
    display: flex;
    align-items: center;
    gap: var(--space-sm);
    margin-bottom: var(--space-md);
}
.location-header h3 {
    margin: 0;
    font-size: 1.1rem;
    color: var(--color-text-primary);
}
.location-header .year-count {
    font-size: 0.8rem;
    color: var(--color-text-muted);
    background: var(--color-bg-page);
    padding: 2px 8px;
    border-radius: var(--radius-full);
}
.history-table {
    width: 100%;
    border-collapse: collapse;
}
.history-table th,
.history-table td {
    padding: var(--space-sm) var(--space-md);
    text-align: left;
    border-bottom: 1px solid var(--color-border);
}
.history-table th {
    background: var(--color-bg-page);
    font-size: 0.75rem;
    font-weight: 600;
    color: var(--color-text-muted);
    text-transform: uppercase;
}
.history-table td {
    font-size: 0.875rem;
}
.history-table tr:last-child td {
    border-bottom: none;
}
.trend-arrow {
    font-size: 0.75rem;
    margin-left: var(--space-xs);
}
.trend-up { color: var(--color-success); }
.trend-down { color: var(--color-error); }
.trend-same { color: var(--color-text-muted); }

/* Brand comparison */
.brand-comparison-table {
    width: 100%;
    border-collapse: collapse;
}
.brand-comparison-table th,
.brand-comparison-table td {
    padding: var(--space-md);
    text-align: left;
    border-bottom: 1px solid var(--color-border);
}
.brand-comparison-table th {
    background: var(--color-bg-page);
    font-size: 0.75rem;
    font-weight: 600;
    color: var(--color-text-muted);
    text-transform: uppercase;
}
.brand-comparison-table tr:last-child td {
    border-bottom: none;
}
.brand-comparison-table tr:hover {
    background: var(--color-bg-hover);
}
.brand-name-cell {
    display: flex;
    align-items: center;
    gap: var(--space-sm);
}
.brand-color-dot {
    width: 12px;
    height: 12px;
    border-radius: 50%;
    flex-shrink: 0;
}
.bar-container {
    width: 100%;
    max-width: 120px;
    height: 8px;
    background: var(--color-bg-page);
    border-radius: var(--radius-full);
    overflow: hidden;
}
.bar-fill {
    height: 100%;
    border-radius: var(--radius-full);
    transition: width 0.3s ease;
}

/* Mobile */
@media (max-width: 767px) {
    .event-card,
    .stat-card {
        margin-left: -16px;
        margin-right: -16px;
        border-radius: 0;
        border-left: none;
        border-right: none;
    }
    .stats-grid {
        grid-template-columns: repeat(2, 1fr);
    }
    .class-table {
        font-size: 0.8rem;
    }
    .class-table th,
    .class-table td {
        padding: var(--space-xs) var(--space-sm);
    }
    .event-header {
        flex-direction: column;
        align-items: flex-start;
    }
}
</style>

<!-- Filter Bar (same pattern as analytics-trends.php) -->
<div class="filter-bar">
    <form method="get" class="filter-form">
        <?php if (!empty($brands)): ?>
        <div class="filter-group">
            <label class="filter-label">Varumarke</label>
            <select name="brand" class="form-select" onchange="this.form.submit()">
                <option value="">Alla varumarken</option>
                <?php foreach ($brands as $brand): ?>
                    <option value="<?= $brand['id'] ?>" <?= $selectedBrand == $brand['id'] ? 'selected' : '' ?>
                        <?php if (!empty($brand['accent_color'])): ?>style="border-left: 3px solid <?= htmlspecialchars($brand['accent_color']) ?>"<?php endif; ?>>
                        <?= htmlspecialchars($brand['name']) ?>
                    </option>
                <?php endforeach; ?>
            </select>
        </div>
        <?php endif; ?>

        <div class="filter-group">
            <label class="filter-label">Sasong</label>
            <select name="year" class="form-select" onchange="this.form.submit()">
                <?php foreach ($availableYears as $y): ?>
                    <option value="<?= $y ?>" <?= $y == $selectedYear ? 'selected' : '' ?>><?= $y ?></option>
                <?php endforeach; ?>
            </select>
        </div>
    </form>
</div>

<!-- Stats Overview -->
<div class="stats-grid">
    <div class="stat-card">
        <div class="stat-value"><?= count($eventSummary) ?></div>
        <div class="stat-label">Events</div>
    </div>
    <div class="stat-card">
        <div class="stat-value"><?= count($classAggregates) ?></div>
        <div class="stat-label">Unika klasser</div>
    </div>
    <div class="stat-card">
        <div class="stat-value"><?= array_sum(array_column($classData, 'participants')) ?></div>
        <div class="stat-label">Totalt deltagare</div>
    </div>
    <div class="stat-card">
        <div class="stat-value">
            <?php
            $stageCounts = array_filter(array_column($classData, 'stage_count'));
            echo !empty($stageCounts) ? round(array_sum($stageCounts) / count($stageCounts), 1) : '-';
            ?>
        </div>
        <div class="stat-label">Snitt sträckor</div>
    </div>
</div>

<!-- Brand Comparison (always shown) -->
<?php if (!empty($brandComparison)): ?>
<div class="admin-card" style="margin-bottom: var(--space-xl);">
    <div class="admin-card-header">
        <h2><i data-lucide="git-compare"></i> Jamfor varumarken (<?= $selectedYear ?>)</h2>
    </div>
    <div class="admin-card-body" style="padding:0;">
        <div class="table-responsive">
            <?php
            // Calculate max values for bar charts
            $maxParticipants = max(array_column($brandComparison, 'total_participants'));
            $maxStages = max(array_column($brandComparison, 'avg_stages'));
            $maxTime = max(array_filter(array_column($brandComparison, 'avg_winner_time_sec')));
            ?>
            <table class="brand-comparison-table">
                <thead>
                    <tr>
                        <th>Varumarke</th>
                        <th>Events</th>
                        <th>Deltagare</th>
                        <th>Klasser</th>
                        <th>Snitt strackor</th>
                        <th>Snitt vinnartid</th>
                    </tr>
                </thead>
                <tbody>
                    <?php foreach ($brandComparison as $brand): ?>
                    <tr>
                        <td>
                            <div class="brand-name-cell">
                                <span class="brand-color-dot" style="background: <?= htmlspecialchars($brand['brand_color'] ?: 'var(--color-accent)') ?>"></span>
                                <strong><?= htmlspecialchars($brand['brand_name']) ?></strong>
                            </div>
                        </td>
                        <td><?= $brand['event_count'] ?></td>
                        <td>
                            <div style="display:flex;align-items:center;gap:var(--space-sm);">
                                <span><?= $brand['total_participants'] ?></span>
                                <div class="bar-container">
                                    <div class="bar-fill" style="width: <?= $maxParticipants > 0 ? round($brand['total_participants'] / $maxParticipants * 100) : 0 ?>%; background: <?= htmlspecialchars($brand['brand_color'] ?: 'var(--color-accent)') ?>"></div>
                                </div>
                            </div>
                        </td>
                        <td><?= $brand['unique_classes'] ?></td>
                        <td>
                            <?php if ($brand['avg_stages'] > 0): ?>
                            <span class="stage-badge"><?= round($brand['avg_stages'], 1) ?></span>
                            <?php else: ?>
                            -
                            <?php endif; ?>
                        </td>
                        <td class="time-cell"><?= formatTime($brand['avg_winner_time_sec']) ?></td>
                    </tr>
                    <?php endforeach; ?>
                </tbody>
            </table>
        </div>
    </div>
</div>
<?php endif; ?>

<?php if (empty($eventSummary)): ?>
<div class="admin-card">
    <div class="no-data">
        <i data-lucide="inbox" style="width:48px;height:48px;margin-bottom:var(--space-md);opacity:0.5;"></i>
        <p>Ingen data hittades for valda filter.</p>
        <p style="font-size:0.85rem;">Prova att valja en annan sasong eller varumarke.</p>
        <?php if ($selectedBrand === null): ?>
        <p style="font-size:0.85rem; margin-top: var(--space-md);">
            <strong>Tips:</strong> Valj ett varumarke for att se historik per anlaggning.
        </p>
        <?php endif; ?>
    </div>
</div>
<?php else: ?>

<!-- Event Details -->
<div class="admin-card">
    <div class="admin-card-header">
        <h2><i data-lucide="calendar"></i> Events per klass (<?= $selectedYear ?>)</h2>
    </div>
    <div class="admin-card-body" style="padding:0;">
        <?php foreach ($eventSummary as $eventId => $event): ?>
        <div class="event-card" style="margin:var(--space-md);margin-bottom:var(--space-sm);">
            <div class="event-header">
                <div>
                    <span class="event-title"><?= htmlspecialchars($event['event_name']) ?></span>
                    <?php if ($event['brand_color']): ?>
                    <span class="brand-tag" style="background:<?= htmlspecialchars($event['brand_color']) ?>;">
                        <?= htmlspecialchars($event['brand_name']) ?>
                    </span>
                    <?php endif; ?>
                </div>
                <div class="event-meta">
                    <span><i data-lucide="calendar"></i> <?= date('Y-m-d', strtotime($event['event_date'])) ?></span>
                    <span><i data-lucide="users"></i> <?= $event['total_participants'] ?> deltagare</span>
                    <span><i data-lucide="layers"></i> <?= $event['class_count'] ?> klasser</span>
                </div>
            </div>
            <table class="class-table">
                <thead>
                    <tr>
                        <th>Klass</th>
                        <th>Deltagare</th>
                        <th>Sträckor</th>
                        <th>Vinnartid</th>
                        <th>Snitttid</th>
                        <th>Tidsspridning</th>
                    </tr>
                </thead>
                <tbody>
                    <?php foreach ($event['classes'] as $class): ?>
                    <tr>
                        <td class="class-name"><?= htmlspecialchars($class['class_name']) ?></td>
                        <td><?= $class['participants'] ?></td>
                        <td>
                            <?php if (!empty($class['stages_used'])): ?>
                            <div class="stages-list">
                                <span class="stage-badge"><?= $class['stage_count'] ?></span>
                                <span class="stages-detail"><?= htmlspecialchars($class['stages_used']) ?></span>
                            </div>
                            <?php else: ?>
                            <span style="color:var(--color-text-muted);">-</span>
                            <?php endif; ?>
                        </td>
                        <td class="time-cell"><?= formatTime($class['winner_time_sec']) ?></td>
                        <td class="time-cell"><?= formatTime($class['avg_time_sec']) ?></td>
                        <td class="time-cell">
                            <?php if (isset($class['time_spread_sec']) && $class['time_spread_sec'] > 0): ?>
                            +<?= formatTime($class['time_spread_sec']) ?>
                            <?php else: ?>
                            -
                            <?php endif; ?>
                        </td>
                    </tr>
                    <?php endforeach; ?>
                </tbody>
            </table>
        </div>
        <?php endforeach; ?>
        <div style="padding:var(--space-sm);"></div>
    </div>
</div>

<!-- DEBUG: Show all classes found in venue history data -->
<?php if (!empty($debugClasses)): ?>
<div class="alert alert-info mb-lg">
    <strong>DEBUG - Klasser funna i venue history (2024):</strong><br>
    <?php foreach ($debugClasses as $key => $time): ?>
        <?php if (strpos($key, '2024') !== false): ?>
            <?= htmlspecialchars($key) ?>: <?= $time ? round($time, 2) . 's' : 'NULL' ?><br>
        <?php endif; ?>
    <?php endforeach; ?>
</div>
<?php endif; ?>

<!-- Historical trends by venue (when brand selected) -->
<?php if (!empty($venueHistory)): ?>
<div class="admin-card" style="margin-bottom: var(--space-xl);">
    <div class="admin-card-header">
        <h2><i data-lucide="mountain"></i> Historik per anlaggning</h2>
    </div>
    <div class="admin-card-body">
        <?php foreach ($venueHistory as $venueId => $data): ?>
        <?php if (count($data['years']) > 1): ?>
        <div class="location-section">
            <div class="location-header">
                <i data-lucide="mountain"></i>
                <h3><?= htmlspecialchars($data['name']) ?></h3>
                <span class="year-count"><?= count($data['years']) ?> ar</span>
            </div>
            <div class="table-responsive">
                <table class="history-table">
                    <thead>
                        <tr>
                            <th>Ar</th>
                            <th>Delt.</th>
                            <th>H Elit</th>
                            <th>D Elit</th>
                            <th>P15-16</th>
                            <th>P13-14</th>
                            <th>Master</th>
                        </tr>
                    </thead>
                    <tbody>
                        <?php
                        $prevParticipants = null;
                        $prevHElit = null;
                        ksort($data['years']); // Sort by year ascending
                        foreach ($data['years'] as $year => $yearData):
                            // Calculate trend arrows for participants
                            $partTrend = '';
                            if ($prevParticipants !== null) {
                                if ($yearData['participants'] > $prevParticipants) {
                                    $partTrend = '<span class="trend-arrow trend-up">+' . ($yearData['participants'] - $prevParticipants) . '</span>';
                                } elseif ($yearData['participants'] < $prevParticipants) {
                                    $partTrend = '<span class="trend-arrow trend-down">' . ($yearData['participants'] - $prevParticipants) . '</span>';
                                }
                            }
                            $prevParticipants = $yearData['participants'];

                            // Time trend for H Elit (lower is better)
                            $hElitTrend = '';
                            if ($prevHElit !== null && $yearData['h_elit'] > 0) {
                                $diff = $yearData['h_elit'] - $prevHElit;
                                if ($diff < -5) {
                                    $hElitTrend = '<span class="trend-arrow trend-up" title="Snabbare"></span>';
                                } elseif ($diff > 5) {
                                    $hElitTrend = '<span class="trend-arrow trend-down" title="Langsammare"></span>';
                                }
                            }
                            if ($yearData['h_elit'] > 0) {
                                $prevHElit = $yearData['h_elit'];
                            }
                        ?>
                        <tr>
                            <td><strong><?= $year ?></strong></td>
                            <td><?= $yearData['participants'] ?><?= $partTrend ?></td>
                            <td class="time-cell"><?= formatTime($yearData['h_elit']) ?><?= $hElitTrend ?></td>
                            <td class="time-cell"><?= formatTime($yearData['d_elit']) ?></td>
                            <td class="time-cell"><?= formatTime($yearData['p15_16']) ?></td>
                            <td class="time-cell"><?= formatTime($yearData['p13_14']) ?></td>
                            <td class="time-cell" title="Snitt H30-H50"><?= formatTime($yearData['master']) ?></td>
                        </tr>
                        <?php endforeach; ?>
                    </tbody>
                </table>
            </div>
        </div>
        <?php endif; ?>
        <?php endforeach; ?>

        <?php
        // Check if any venues had only 1 year
        $singleYearVenues = array_filter($venueHistory, function($d) { return count($d['years']) === 1; });
        if (!empty($singleYearVenues)):
        ?>
        <p style="color: var(--color-text-muted); font-size: 0.85rem; margin-top: var(--space-lg);">
            <i data-lucide="info" style="width:14px;height:14px;vertical-align:middle;"></i>
            <?= count($singleYearVenues) ?> anlaggningar med endast ett ar visas inte.
        </p>
        <?php endif; ?>
    </div>
</div>
<?php endif; ?>

<!-- Aggregate by Class -->
<div class="aggregate-section">
    <div class="admin-card">
        <div class="admin-card-header">
            <h2><i data-lucide="bar-chart-3"></i> Sammanfattning per klass</h2>
        </div>
        <div class="admin-card-body" style="padding:0;">
            <div class="table-responsive">
                <table class="aggregate-table">
                    <thead>
                        <tr>
                            <th>Klass</th>
                            <th>Antal events</th>
                            <th>Snitt deltagare</th>
                            <th>Snitt strackor</th>
                            <th>Kortast</th>
                            <th>Snitt vinnartid</th>
                            <th>Langst</th>
                        </tr>
                    </thead>
                    <tbody>
                        <?php foreach ($classAggregates as $className => $agg): ?>
                        <tr>
                            <td class="class-name"><?= htmlspecialchars($className) ?></td>
                            <td><?= $agg['event_count'] ?></td>
                            <td><?= $agg['avg_participants'] ?></td>
                            <td>
                                <?php if ($agg['avg_stages'] > 0): ?>
                                <span class="stage-badge"><?= $agg['avg_stages'] ?></span>
                                <?php else: ?>
                                -
                                <?php endif; ?>
                            </td>
                            <td class="time-cell" style="color: var(--color-success);">
                                <?= formatTime($agg['min_winner_time']) ?>
                                <?php if (!empty($agg['min_venue'])): ?>
                                <span style="color: var(--color-text-muted); font-size: 0.75rem; display: block;">(<?= htmlspecialchars($agg['min_venue']) ?>)</span>
                                <?php endif; ?>
                            </td>
                            <td class="time-cell"><?= formatTime($agg['avg_winner_time']) ?></td>
                            <td class="time-cell" style="color: var(--color-warning);">
                                <?= formatTime($agg['max_winner_time']) ?>
                                <?php if (!empty($agg['max_venue'])): ?>
                                <span style="color: var(--color-text-muted); font-size: 0.75rem; display: block;">(<?= htmlspecialchars($agg['max_venue']) ?>)</span>
                                <?php endif; ?>
                            </td>
                        </tr>
                        <?php endforeach; ?>
                    </tbody>
                </table>
            </div>
        </div>
    </div>
</div>

<?php endif; ?>

<script>
// Initialize Lucide icons
if (typeof lucide !== 'undefined') {
    lucide.createIcons();
}
</script>

<?php include __DIR__ . '/components/unified-layout-footer.php'; ?>
