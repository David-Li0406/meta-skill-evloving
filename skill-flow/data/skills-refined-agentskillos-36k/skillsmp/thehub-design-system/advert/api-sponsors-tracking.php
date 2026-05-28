<?php
/**
 * API Endpoints för Sponsor Tracking
 * /api/sponsors/track-impression
 * /api/sponsors/track-click
 */

header('Content-Type: application/json');

require_once __DIR__ . '/../../includes/db.php';
require_once __DIR__ . '/../../includes/GlobalSponsorManager.php';

$globalSponsors = new GlobalSponsorManager($db);

// Hämta request data
$input = json_decode(file_get_contents('php://input'), true);
$action = $_GET['action'] ?? '';

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

/**
 * Hantera impression tracking
 */
function handleImpression($globalSponsors, $input) {
    if (empty($input['sponsor_id'])) {
        http_response_code(400);
        echo json_encode(['error' => 'Missing sponsor_id']);
        return;
    }
    
    $sponsor_id = $input['sponsor_id'];
    $placement_id = $input['placement_id'] ?? null;
    $page_type = $input['page_type'] ?? 'unknown';
    $page_id = $input['page_id'] ?? null;
    
    try {
        $globalSponsors->trackImpression($sponsor_id, $placement_id, $page_type, $page_id);
        echo json_encode(['success' => true]);
    } catch (Exception $e) {
        http_response_code(500);
        echo json_encode(['error' => $e->getMessage()]);
    }
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
    
    $sponsor_id = $input['sponsor_id'];
    $placement_id = $input['placement_id'] ?? null;
    $page_type = $input['page_type'] ?? 'unknown';
    $page_id = $input['page_id'] ?? null;
    
    try {
        $globalSponsors->trackClick($sponsor_id, $placement_id, $page_type, $page_id);
        echo json_encode(['success' => true]);
    } catch (Exception $e) {
        http_response_code(500);
        echo json_encode(['error' => $e->getMessage()]);
    }
}

/**
 * Hämta statistik
 */
function getStats($globalSponsors, $input) {
    // Kräv admin-behörighet
    session_start();
    if (!isset($_SESSION['admin_id'])) {
        http_response_code(403);
        echo json_encode(['error' => 'Unauthorized']);
        return;
    }
    
    $sponsor_id = $input['sponsor_id'] ?? null;
    $period = $input['period'] ?? 'month';
    
    if (!$sponsor_id) {
        http_response_code(400);
        echo json_encode(['error' => 'Missing sponsor_id']);
        return;
    }
    
    try {
        $report = $globalSponsors->generateReport($sponsor_id, $period);
        $daily_stats = $globalSponsors->getSponsorStats($sponsor_id, 30);
        
        echo json_encode([
            'success' => true,
            'report' => $report,
            'daily_stats' => $daily_stats
        ]);
    } catch (Exception $e) {
        http_response_code(500);
        echo json_encode(['error' => $e->getMessage()]);
    }
}
