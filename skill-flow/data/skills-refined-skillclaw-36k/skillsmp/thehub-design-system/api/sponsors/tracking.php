<?php
/**
 * API Endpoints för Sponsor Tracking
 * /api/sponsors/tracking.php
 *
 * Actions:
 * - track-impression: Tracka visning av sponsor
 * - track-click: Tracka klick på sponsor
 * - get-stats: Hämta statistik (kräver admin)
 */

header('Content-Type: application/json');

require_once __DIR__ . '/../../config.php';
require_once __DIR__ . '/../../includes/GlobalSponsorManager.php';

$globalSponsors = new GlobalSponsorManager($pdo);

// Hämta request data
$input = json_decode(file_get_contents('php://input'), true) ?? [];
$action = $_GET['action'] ?? $_POST['action'] ?? '';

try {
    switch ($action) {
        case 'track-impression':
            handleImpression($globalSponsors, $input);
            break;

        case 'track-click':
            handleClick($globalSponsors, $input);
            break;

        case 'get-stats':
            getStats($globalSponsors, $input);
            break;

        default:
            http_response_code(400);
            echo json_encode(['error' => 'Invalid action']);
    }
} catch (Exception $e) {
    http_response_code(500);
    echo json_encode(['error' => 'Server error']);
    error_log("Sponsor tracking API error: " . $e->getMessage());
}

/**
 * Hantera impression tracking
 */
function handleImpression($globalSponsors, $input) {
    if (empty($input['sponsor_id'])) {
        http_response_code(400);
        echo json_encode(['error' => 'Missing sponsor_id']);
        return;
    }

    $sponsor_id = (int)$input['sponsor_id'];
    $placement_id = isset($input['placement_id']) ? (int)$input['placement_id'] : null;
    $page_type = $input['page_type'] ?? 'unknown';
    $page_id = isset($input['page_id']) ? (int)$input['page_id'] : null;

    $globalSponsors->trackImpression($sponsor_id, $placement_id, $page_type, $page_id);
    echo json_encode(['success' => true]);
}

/**
 * Hantera click tracking
 */
function handleClick($globalSponsors, $input) {
    if (empty($input['sponsor_id'])) {
        http_response_code(400);
        echo json_encode(['error' => 'Missing sponsor_id']);
        return;
    }

    $sponsor_id = (int)$input['sponsor_id'];
    $placement_id = isset($input['placement_id']) ? (int)$input['placement_id'] : null;
    $page_type = $input['page_type'] ?? 'unknown';
    $page_id = isset($input['page_id']) ? (int)$input['page_id'] : null;

    $globalSponsors->trackClick($sponsor_id, $placement_id, $page_type, $page_id);
    echo json_encode(['success' => true]);
}

/**
 * Hämta statistik
 */
function getStats($globalSponsors, $input) {
    // Kräv admin-behörighet
    if (!isset($_SESSION['admin_id'])) {
        http_response_code(403);
        echo json_encode(['error' => 'Unauthorized']);
        return;
    }

    $sponsor_id = isset($input['sponsor_id']) ? (int)$input['sponsor_id'] : null;
    $period = $input['period'] ?? 'month';

    if (!$sponsor_id) {
        http_response_code(400);
        echo json_encode(['error' => 'Missing sponsor_id']);
        return;
    }

    $report = $globalSponsors->generateReport($sponsor_id, $period);
    $daily_stats = $globalSponsors->getSponsorStats($sponsor_id, 30);

    echo json_encode([
        'success' => true,
        'report' => $report,
        'daily_stats' => $daily_stats
    ]);
}
