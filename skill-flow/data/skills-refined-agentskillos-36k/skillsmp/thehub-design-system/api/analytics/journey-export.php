<?php
/**
 * API: Journey Analysis Export
 *
 * Exporterar First Season Journey och Longitudinal Journey data
 * med valfri brand-filtrering. GDPR-sakrad (minimum 10 per segment).
 *
 * Endpoints:
 *   GET /api/analytics/journey-export.php?action=summary&cohort=2023
 *   GET /api/analytics/journey-export.php?action=longitudinal&cohort=2023
 *   GET /api/analytics/journey-export.php?action=patterns&cohort=2023
 *   GET /api/analytics/journey-export.php?action=brands&cohort=2023&brands=1,2,3
 *   GET /api/analytics/journey-export.php?action=full&cohort=2023&format=csv
 *   GET /api/analytics/journey-export.php?action=available
 *
 * @package TheHUB Analytics
 * @version 3.1
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
$action = $_GET['action'] ?? 'summary';
$cohort = isset($_GET['cohort']) ? (int)$_GET['cohort'] : null;
$format = $_GET['format'] ?? 'json';

// Parse brand filter
$brandIds = null;
if (!empty($_GET['brands'])) {
    $brandIds = array_map('intval', explode(',', $_GET['brands']));
    $brandIds = array_filter($brandIds);
    $brandIds = array_slice($brandIds, 0, 12); // Max 12 brands
}

// Validate cohort year
if ($cohort !== null && ($cohort < 2010 || $cohort > 2030)) {
    http_response_code(400);
    echo json_encode(['success' => false, 'error' => 'Invalid cohort year']);
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
        case 'summary':
            // First Season Journey summary
            if (!$cohort) {
                throw new InvalidArgumentException('Cohort year required');
            }
            $response['cohort'] = $cohort;
            $response['brand_filter'] = $brandIds;
            $response['data'] = $kpi->getFirstSeasonJourneySummary($cohort, $brandIds);
            break;

        case 'longitudinal':
            // Longitudinal retention funnel
            if (!$cohort) {
                throw new InvalidArgumentException('Cohort year required');
            }
            $response['cohort'] = $cohort;
            $response['brand_filter'] = $brandIds;
            $response['data'] = $kpi->getCohortLongitudinalOverview($cohort, $brandIds);
            break;

        case 'patterns':
            // Journey pattern distribution
            if (!$cohort) {
                throw new InvalidArgumentException('Cohort year required');
            }
            $response['cohort'] = $cohort;
            $response['brand_filter'] = $brandIds;
            $response['data'] = $kpi->getJourneyTypeDistribution($cohort, $brandIds);
            break;

        case 'retention_starts':
            // Retention by first season start count
            if (!$cohort) {
                throw new InvalidArgumentException('Cohort year required');
            }
            $response['cohort'] = $cohort;
            $response['brand_filter'] = $brandIds;
            $response['data'] = $kpi->getRetentionByStartCount($cohort, $brandIds);
            break;

        case 'brands':
            // Multi-brand comparison
            if (!$cohort) {
                throw new InvalidArgumentException('Cohort year required');
            }
            if (empty($brandIds) || count($brandIds) < 2) {
                throw new InvalidArgumentException('At least 2 brand IDs required for comparison');
            }
            $response['cohort'] = $cohort;
            $response['data'] = $kpi->getBrandJourneyComparison($cohort, $brandIds);
            break;

        case 'brand_funnel':
            // Single brand retention funnel
            if (!$cohort) {
                throw new InvalidArgumentException('Cohort year required');
            }
            $brandId = isset($_GET['brand_id']) ? (int)$_GET['brand_id'] : null;
            if (!$brandId) {
                throw new InvalidArgumentException('brand_id parameter required');
            }
            $response['cohort'] = $cohort;
            $response['brand_id'] = $brandId;
            $response['data'] = $kpi->getBrandRetentionFunnel($brandId, $cohort);
            break;

        case 'brand_patterns':
            // Journey patterns per brand
            if (!$cohort) {
                throw new InvalidArgumentException('Cohort year required');
            }
            if (empty($brandIds)) {
                throw new InvalidArgumentException('Brand IDs required');
            }
            $response['cohort'] = $cohort;
            $response['data'] = $kpi->getJourneyPatternsByBrand($cohort, $brandIds);
            break;

        case 'full':
            // Full export (CSV or JSON)
            if (!$cohort) {
                throw new InvalidArgumentException('Cohort year required');
            }
            $exportData = $kpi->exportJourneyData($cohort, $brandIds, $format);

            if ($format === 'csv') {
                // Output CSV file
                header('Content-Type: text/csv; charset=utf-8');
                header('Content-Disposition: attachment; filename="' . $exportData['filename'] . '"');
                echo "\xEF\xBB\xBF"; // UTF-8 BOM
                echo $exportData['data'];

                // Log export
                logExport($pdo, 'journey_full_csv', $cohort, $brandIds);
                exit;
            }

            $response['cohort'] = $cohort;
            $response['brand_filter'] = $brandIds;
            $response['data'] = $exportData['data'];
            break;

        case 'available':
            // Get available cohorts and brands
            $response['cohorts'] = $kpi->getAvailableCohortYears($brandIds);
            $response['brands'] = $kpi->getAvailableBrandsForJourney($cohort);
            break;

        default:
            http_response_code(400);
            echo json_encode([
                'success' => false,
                'error' => 'Unknown action: ' . $action,
                'available_actions' => [
                    'summary', 'longitudinal', 'patterns', 'retention_starts',
                    'brands', 'brand_funnel', 'brand_patterns', 'full', 'available'
                ]
            ]);
            exit;
    }

    // Log API access
    logExport($pdo, 'journey_api_' . $action, $cohort, $brandIds);

    echo json_encode($response, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE);

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
 * Log export/API access
 */
function logExport(PDO $pdo, string $type, ?int $cohort, ?array $brandIds): void {
    try {
        $stmt = $pdo->prepare("
            INSERT INTO analytics_exports
            (export_type, export_params, exported_by, ip_address)
            VALUES (?, ?, ?, ?)
        ");
        $stmt->execute([
            $type,
            json_encode(['cohort' => $cohort, 'brands' => $brandIds]),
            $_SESSION['user_id'] ?? null,
            $_SERVER['REMOTE_ADDR'] ?? null
        ]);
    } catch (Exception $e) {
        // Ignore logging errors
    }
}
