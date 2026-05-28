<?php
/**
 * API: Event Participation Analysis Export
 *
 * Exporterar event participation data med valfri brand-filtrering.
 * GDPR-sakrad (minimum 10 per segment).
 *
 * Endpoints:
 *   GET /api/analytics/event-participation-export.php?action=distribution&series_id=X&year=Y
 *   GET /api/analytics/event-participation-export.php?action=unique&series_id=X&year=Y
 *   GET /api/analytics/event-participation-export.php?action=retention&series_id=X&from_year=Y&to_year=Z
 *   GET /api/analytics/event-participation-export.php?action=loyalty&series_id=X
 *   GET /api/analytics/event-participation-export.php?action=event_retention&event_id=X&from_year=Y&to_year=Z
 *   GET /api/analytics/event-participation-export.php?action=available_series&brands=1,2,3
 *   GET /api/analytics/event-participation-export.php?action=available_years&series_id=X
 *
 * @package TheHUB Analytics
 * @version 3.2
 */

header('Content-Type: application/json; charset=utf-8');

require_once __DIR__ . '/../../config/database.php';
require_once __DIR__ . '/../../includes/auth.php';

// Require admin or statistics permission
if (!isAdmin() && !hasPermission('statistics')) {
    http_response_code(403);
    echo json_encode(['success' => false, 'error' => 'Unauthorized']);
    exit;
}

require_once __DIR__ . '/../../analytics/includes/KPICalculator.php';

// Parameters
$action = $_GET['action'] ?? 'distribution';
$seriesId = isset($_GET['series_id']) ? (int)$_GET['series_id'] : null;
$year = isset($_GET['year']) ? (int)$_GET['year'] : null;
$fromYear = isset($_GET['from_year']) ? (int)$_GET['from_year'] : null;
$toYear = isset($_GET['to_year']) ? (int)$_GET['to_year'] : null;
$eventId = isset($_GET['event_id']) ? (int)$_GET['event_id'] : null;
$venueId = isset($_GET['venue_id']) ? (int)$_GET['venue_id'] : null;
$minYears = isset($_GET['min_years']) ? (int)$_GET['min_years'] : 2;
$format = $_GET['format'] ?? 'json';

// Parse brand filter
$brandIds = null;
if (!empty($_GET['brands'])) {
    $brandIds = array_map('intval', explode(',', $_GET['brands']));
    $brandIds = array_filter($brandIds);
    $brandIds = array_slice($brandIds, 0, 12); // Max 12 brands
}

// Validate series_id for most actions
if ($seriesId !== null && ($seriesId < 1 || $seriesId > 999999)) {
    http_response_code(400);
    echo json_encode(['success' => false, 'error' => 'Invalid series_id']);
    exit;
}

// Validate year ranges
if ($year !== null && ($year < 2010 || $year > 2030)) {
    http_response_code(400);
    echo json_encode(['success' => false, 'error' => 'Invalid year']);
    exit;
}

try {
    $pdo = hub_db();
    $kpi = new KPICalculator($pdo);

    $response = [
        'success' => true,
        'action' => $action,
        'timestamp' => date('Y-m-d H:i:s'),
        'gdpr_compliant' => true
    ];

    switch ($action) {
        case 'distribution':
            // Series participation distribution
            if (!$seriesId || !$year) {
                throw new InvalidArgumentException('series_id and year required');
            }
            $response['series_id'] = $seriesId;
            $response['year'] = $year;
            $response['brand_filter'] = $brandIds;
            $response['data'] = $kpi->getSeriesParticipationDistribution($seriesId, $year, $brandIds);
            break;

        case 'unique':
            // Events with unique participants
            if (!$seriesId || !$year) {
                throw new InvalidArgumentException('series_id and year required');
            }
            $response['series_id'] = $seriesId;
            $response['year'] = $year;
            $response['brand_filter'] = $brandIds;
            $response['data'] = $kpi->getEventsWithUniqueParticipants($seriesId, $year, $brandIds);
            break;

        case 'retention':
            // Series event retention comparison
            if (!$seriesId || !$fromYear || !$toYear) {
                throw new InvalidArgumentException('series_id, from_year and to_year required');
            }
            $response['series_id'] = $seriesId;
            $response['from_year'] = $fromYear;
            $response['to_year'] = $toYear;
            $response['brand_filter'] = $brandIds;
            $response['data'] = $kpi->getSeriesEventRetentionComparison($seriesId, $fromYear, $toYear, $brandIds);
            break;

        case 'event_retention':
            // Single event retention
            if (!$eventId || !$fromYear || !$toYear) {
                throw new InvalidArgumentException('event_id, from_year and to_year required');
            }
            $response['event_id'] = $eventId;
            $response['from_year'] = $fromYear;
            $response['to_year'] = $toYear;
            $response['data'] = $kpi->getEventRetention($eventId, $fromYear, $toYear);
            break;

        case 'loyalty':
            // Loyal riders analysis
            if (!$seriesId) {
                throw new InvalidArgumentException('series_id required');
            }
            $response['series_id'] = $seriesId;
            $response['venue_id'] = $venueId;
            $response['min_years'] = $minYears;
            $response['data'] = $kpi->getEventLoyalRiders($seriesId, $venueId, $minYears);
            break;

        case 'available_series':
            // Get available series for analysis
            $response['brand_filter'] = $brandIds;
            $response['data'] = $kpi->getAvailableSeriesForEventAnalysis($brandIds);
            break;

        case 'available_years':
            // Get available years for a series
            if (!$seriesId) {
                throw new InvalidArgumentException('series_id required');
            }
            $response['series_id'] = $seriesId;
            $response['data'] = $kpi->getAvailableYearsForSeries($seriesId);
            break;

        default:
            http_response_code(400);
            echo json_encode([
                'success' => false,
                'error' => 'Unknown action: ' . $action,
                'available_actions' => [
                    'distribution', 'unique', 'retention', 'event_retention',
                    'loyalty', 'available_series', 'available_years'
                ]
            ]);
            exit;
    }

    // Log API access
    logApiAccess($pdo, 'event_participation_' . $action, $seriesId, $year, $brandIds);

    // Output
    if ($format === 'csv' && in_array($action, ['distribution', 'unique', 'retention'])) {
        outputCsv($action, $response['data']);
    } else {
        echo json_encode($response, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE);
    }

} catch (InvalidArgumentException $e) {
    http_response_code(400);
    echo json_encode([
        'success' => false,
        'error' => $e->getMessage()
    ]);

} catch (Exception $e) {
    http_response_code(500);
    echo json_encode([
        'success' => false,
        'error' => 'Internal server error',
        'debug' => (defined('DEBUG') && DEBUG) ? $e->getMessage() : null
    ]);
}

/**
 * Log API access
 */
function logApiAccess(PDO $pdo, string $type, ?int $seriesId, ?int $year, ?array $brandIds): void {
    try {
        $stmt = $pdo->prepare("
            INSERT INTO analytics_exports
            (export_type, export_params, exported_by, ip_address)
            VALUES (?, ?, ?, ?)
        ");
        $stmt->execute([
            $type,
            json_encode(['series_id' => $seriesId, 'year' => $year, 'brands' => $brandIds]),
            $_SESSION['user_id'] ?? null,
            $_SERVER['REMOTE_ADDR'] ?? null
        ]);
    } catch (Exception $e) {
        // Ignore logging errors
    }
}

/**
 * Output data as CSV
 */
function outputCsv(string $action, array $data): void {
    header('Content-Type: text/csv; charset=utf-8');
    header('Content-Disposition: attachment; filename="event_participation_' . $action . '_' . date('Y-m-d') . '.csv"');

    echo "\xEF\xBB\xBF"; // UTF-8 BOM

    if (isset($data['suppressed'])) {
        echo "Error: Data suppressed for GDPR compliance\n";
        echo "Reason: " . ($data['reason'] ?? 'Unknown') . "\n";
        exit;
    }

    switch ($action) {
        case 'distribution':
            echo "Events Attended,Count,Percentage\n";
            if (!empty($data['distribution'])) {
                foreach ($data['distribution'] as $d) {
                    echo "{$d['events']},{$d['count']},{$d['percentage']}\n";
                }
            }
            echo "\n";
            echo "Summary\n";
            echo "Total Participants," . ($data['total_participants'] ?? '') . "\n";
            echo "Total Events in Series," . ($data['total_events_in_series'] ?? '') . "\n";
            echo "Avg Events per Rider," . ($data['avg_events_per_rider'] ?? '') . "\n";
            echo "Single Event %," . ($data['single_event_pct'] ?? '') . "\n";
            echo "Full Series %," . ($data['full_series_pct'] ?? '') . "\n";
            break;

        case 'unique':
            echo "Event ID,Event Name,Event Date,Venue,Total Participants,Unique Count,Unique %\n";
            if (!empty($data['events'])) {
                foreach ($data['events'] as $e) {
                    $name = str_replace('"', '""', $e['event_name'] ?? '');
                    $venue = str_replace('"', '""', $e['venue_name'] ?? '');
                    echo "{$e['event_id']},\"{$name}\",{$e['event_date']},\"{$venue}\",{$e['total_participants']}," .
                         ($e['unique_count'] ?? 0) . "," . ($e['unique_pct'] ?? 0) . "\n";
                }
            }
            break;

        case 'retention':
            echo "Event ID,Event Name,Venue,Participants,Returned Same Event,Returned Series,Retention %\n";
            if (!empty($data['events'])) {
                foreach ($data['events'] as $e) {
                    $name = str_replace('"', '""', $e['name'] ?? '');
                    $venue = str_replace('"', '""', $e['venue_name'] ?? '');
                    $r = $e['retention'] ?? [];
                    echo "{$e['id']},\"{$name}\",\"{$venue}\"," .
                         ($r['participants_from_year'] ?? 0) . "," .
                         ($r['returned_same_event'] ?? 0) . "," .
                         ($r['returned_same_series'] ?? 0) . "," .
                         ($r['same_event_retention_rate'] ?? 0) . "\n";
                }
            }
            break;
    }

    exit;
}
