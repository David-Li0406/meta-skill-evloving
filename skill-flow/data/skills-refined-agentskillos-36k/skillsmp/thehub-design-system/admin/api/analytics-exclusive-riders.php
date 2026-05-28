<?php
/**
 * API: Get exclusive riders for an event
 * Returns riders who ONLY participated in this specific event within the brand/series
 */
require_once __DIR__ . '/../../config.php';
require_admin();

header('Content-Type: application/json');

global $pdo;

$eventId = isset($_GET['event_id']) ? (int)$_GET['event_id'] : 0;
$year = isset($_GET['year']) ? (int)$_GET['year'] : (int)date('Y');
$brandId = isset($_GET['brand_id']) && $_GET['brand_id'] !== '' ? (int)$_GET['brand_id'] : null;

if (!$eventId) {
    echo json_encode(['error' => 'Event ID saknas']);
    exit;
}

try {
    // Hitta deltagare som ENDAST tävlade på detta event under året (inom vald serie/brand)
    $exclusiveSql = "
        SELECT DISTINCT r.cyclist_id
        FROM results r
        WHERE r.event_id = ?
        AND r.cyclist_id IN (
            SELECT sub_r.cyclist_id
            FROM results sub_r
            JOIN events sub_e ON sub_e.id = sub_r.event_id
            " . ($brandId ? "
                JOIN series_events sub_se ON sub_se.event_id = sub_e.id
                JOIN series sub_s ON sub_s.id = sub_se.series_id
            " : "") . "
            WHERE YEAR(sub_e.date) = ?
            " . ($brandId ? "AND sub_s.brand_id = ?" : "") . "
            GROUP BY sub_r.cyclist_id
            HAVING COUNT(DISTINCT sub_r.event_id) = 1
        )
    ";

    $exclusiveParams = [$eventId, $year];
    if ($brandId) {
        $exclusiveParams[] = $brandId;
    }

    $stmt = $pdo->prepare($exclusiveSql);
    $stmt->execute($exclusiveParams);
    $exclusiveRiderIds = $stmt->fetchAll(PDO::FETCH_COLUMN);

    if (empty($exclusiveRiderIds)) {
        echo json_encode(['riders' => []]);
        exit;
    }

    // Hämta rider-info med klass och kolla om de tävlade i annan serie
    $placeholders = implode(',', array_fill(0, count($exclusiveRiderIds), '?'));

    $riderSql = "
        SELECT
            rid.id,
            CONCAT(rid.firstname, ' ', rid.lastname) as name,
            COALESCE(NULLIF(c.display_name, ''), c.name) as class_name,
            r.position
        FROM results r
        JOIN riders rid ON rid.id = r.cyclist_id
        LEFT JOIN classes c ON c.id = r.class_id
        WHERE r.event_id = ?
        AND r.cyclist_id IN ($placeholders)
        ORDER BY c.display_name, c.name, rid.lastname, rid.firstname
    ";

    $riderParams = array_merge([$eventId], $exclusiveRiderIds);
    $stmt = $pdo->prepare($riderSql);
    $stmt->execute($riderParams);
    $riders = $stmt->fetchAll(PDO::FETCH_ASSOC);

    // Kolla vilka som tävlade i ANNAN serie under samma år
    $otherSeriesMap = [];
    if ($brandId && !empty($exclusiveRiderIds)) {
        $otherSeriesSql = "
            SELECT
                r.cyclist_id,
                GROUP_CONCAT(DISTINCT s.name SEPARATOR ', ') as series_names
            FROM results r
            JOIN events e ON e.id = r.event_id
            JOIN series_events se ON se.event_id = e.id
            JOIN series s ON s.id = se.series_id
            WHERE YEAR(e.date) = ?
            AND r.cyclist_id IN ($placeholders)
            AND s.brand_id != ?
            GROUP BY r.cyclist_id
        ";

        $otherParams = array_merge([$year], $exclusiveRiderIds, [$brandId]);
        $stmt = $pdo->prepare($otherSeriesSql);
        $stmt->execute($otherParams);

        while ($row = $stmt->fetch(PDO::FETCH_ASSOC)) {
            $otherSeriesMap[$row['cyclist_id']] = $row['series_names'];
        }
    }

    // Lägg till other_series info och räkna per klass
    $classCounts = [];
    foreach ($riders as &$rider) {
        $rider['other_series'] = $otherSeriesMap[$rider['id']] ?? null;

        // Räkna per klass
        $className = $rider['class_name'] ?? 'Okänd klass';
        if (!isset($classCounts[$className])) {
            $classCounts[$className] = 0;
        }
        $classCounts[$className]++;
    }

    // Sortera klassräkning efter antal (störst först)
    arsort($classCounts);

    // Konvertera till array för JSON
    $classCountsArray = [];
    foreach ($classCounts as $name => $count) {
        $classCountsArray[] = ['name' => $name, 'count' => $count];
    }

    echo json_encode([
        'riders' => $riders,
        'class_counts' => $classCountsArray,
        'total' => count($riders)
    ]);

} catch (Exception $e) {
    echo json_encode(['error' => 'Databasfel: ' . $e->getMessage()]);
}
