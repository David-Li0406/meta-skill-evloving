<?php
/**
 * TheHUB - Map API
 *
 * REST API for event map data, tracks, segments, and POIs.
 * Supports both public (GET) and admin (POST/PUT/DELETE) operations.
 *
 * @since 2025-12-09
 */

require_once dirname(__DIR__) . '/config.php';
require_once INCLUDES_PATH . '/map_functions.php';

header('Content-Type: application/json');
header('Cache-Control: no-store');
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: GET, POST, PUT, DELETE, OPTIONS');
header('Access-Control-Allow-Headers: Content-Type');

// Handle preflight requests
if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') {
    http_response_code(200);
    exit;
}

global $pdo;

$method = $_SERVER['REQUEST_METHOD'];
$action = $_GET['action'] ?? '';
$eventId = isset($_GET['event_id']) ? (int)$_GET['event_id'] : null;

/**
 * Send JSON response
 */
function sendResponse($data, $statusCode = 200) {
    http_response_code($statusCode);
    echo json_encode($data, JSON_UNESCAPED_UNICODE);
    exit;
}

/**
 * Send error response
 */
function sendError($message, $statusCode = 400) {
    sendResponse(['success' => false, 'error' => $message], $statusCode);
}

/**
 * Require admin authentication for write operations
 */
function requireAdminForApi() {
    if (!isLoggedIn()) {
        sendError('Inloggning kravs', 401);
    }
}

/**
 * Get JSON input data
 */
function getJsonInput() {
    $input = file_get_contents('php://input');
    $data = json_decode($input, true);
    if (json_last_error() !== JSON_ERROR_NONE) {
        sendError('Ogiltig JSON-data');
    }
    return $data;
}

try {
    switch ($action) {

        // =====================================================
        // PUBLIC ENDPOINTS (GET)
        // =====================================================

        /**
         * GET map data for event
         * GET /api/map.php?action=get_map&event_id=123
         */
        case 'get_map':
            if (!$eventId) {
                sendError('event_id kravs');
            }
            $data = getEventMapData($pdo, $eventId);
            if (!$data) {
                sendResponse([
                    'success' => true,
                    'data' => null,
                    'message' => 'Ingen karta tillganglig for detta event'
                ]);
            }
            sendResponse(['success' => true, 'data' => $data]);
            break;

        /**
         * GET POIs for event
         * GET /api/map.php?action=get_pois&event_id=123
         */
        case 'get_pois':
            if (!$eventId) {
                sendError('event_id kravs');
            }
            $pois = getEventPois($pdo, $eventId);
            sendResponse(['success' => true, 'pois' => $pois]);
            break;

        /**
         * GET segments for event
         * GET /api/map.php?action=get_segments&event_id=123
         */
        case 'get_segments':
            if (!$eventId) {
                sendError('event_id kravs');
            }
            $track = getEventTrack($pdo, $eventId);
            if (!$track) {
                sendResponse(['success' => true, 'segments' => []]);
            }
            sendResponse(['success' => true, 'segments' => $track['segments']]);
            break;

        /**
         * GET POI types configuration
         * GET /api/map.php?action=get_poi_types
         */
        case 'get_poi_types':
            sendResponse(['success' => true, 'poi_types' => POI_TYPES]);
            break;

        /**
         * Check if event has map
         * GET /api/map.php?action=has_map&event_id=123
         */
        case 'has_map':
            if (!$eventId) {
                sendError('event_id kravs');
            }
            $hasMap = eventHasMap($pdo, $eventId);
            sendResponse(['success' => true, 'has_map' => $hasMap]);
            break;

        // =====================================================
        // ADMIN ENDPOINTS (POST/PUT/DELETE)
        // =====================================================

        /**
         * POST add POI
         * POST /api/map.php?action=add_poi&event_id=123
         * Body: { poi_type, lat, lng, label?, description?, sequence_number? }
         */
        case 'add_poi':
            requireAdminForApi();
            if ($method !== 'POST') {
                sendError('POST method kravs', 405);
            }
            if (!$eventId) {
                sendError('event_id kravs');
            }

            $data = getJsonInput();
            if (empty($data['poi_type']) || !isset($data['lat']) || !isset($data['lng'])) {
                sendError('poi_type, lat och lng kravs');
            }

            // Validate POI type
            if (!getPoiType($data['poi_type'])) {
                sendError('Ogiltig POI-typ');
            }

            $poiId = addEventPoi($pdo, $eventId, $data);
            sendResponse([
                'success' => true,
                'message' => 'POI tillagd',
                'poi_id' => $poiId
            ]);
            break;

        /**
         * PUT update POI
         * PUT /api/map.php?action=update_poi&poi_id=456
         * Body: { poi_type, lat, lng, label?, description? }
         */
        case 'update_poi':
            requireAdminForApi();
            if ($method !== 'PUT') {
                sendError('PUT method kravs', 405);
            }

            $poiId = isset($_GET['poi_id']) ? (int)$_GET['poi_id'] : null;
            if (!$poiId) {
                sendError('poi_id kravs');
            }

            $data = getJsonInput();
            if (empty($data['poi_type']) || !isset($data['lat']) || !isset($data['lng'])) {
                sendError('poi_type, lat och lng kravs');
            }

            updateEventPoi($pdo, $poiId, $data);
            sendResponse(['success' => true, 'message' => 'POI uppdaterad']);
            break;

        /**
         * DELETE POI
         * DELETE /api/map.php?action=delete_poi&poi_id=456
         */
        case 'delete_poi':
            requireAdminForApi();
            if ($method !== 'DELETE') {
                sendError('DELETE method kravs', 405);
            }

            $poiId = isset($_GET['poi_id']) ? (int)$_GET['poi_id'] : null;
            if (!$poiId) {
                sendError('poi_id kravs');
            }

            deleteEventPoi($pdo, $poiId);
            sendResponse(['success' => true, 'message' => 'POI borttagen']);
            break;

        /**
         * PUT update segment
         * PUT /api/map.php?action=update_segment&segment_id=789
         * Body: { type, name, timing_id? }
         */
        case 'update_segment':
            requireAdminForApi();
            if ($method !== 'PUT') {
                sendError('PUT method kravs', 405);
            }

            $segmentId = isset($_GET['segment_id']) ? (int)$_GET['segment_id'] : null;
            if (!$segmentId) {
                sendError('segment_id kravs');
            }

            $data = getJsonInput();
            if (empty($data['type']) || !isset($data['name'])) {
                sendError('type och name kravs');
            }

            if (!in_array($data['type'], ['stage', 'liaison'])) {
                sendError('type maste vara "stage" eller "liaison"');
            }

            updateSegmentClassification(
                $pdo,
                $segmentId,
                $data['type'],
                $data['name'],
                $data['timing_id'] ?? null
            );
            sendResponse(['success' => true, 'message' => 'Segment uppdaterat']);
            break;

        /**
         * PUT reorder segments
         * PUT /api/map.php?action=reorder_segments&track_id=123
         * Body: { order: [segment_id, segment_id, ...] }
         */
        case 'reorder_segments':
            requireAdminForApi();
            if ($method !== 'PUT') {
                sendError('PUT method kravs', 405);
            }

            $trackId = isset($_GET['track_id']) ? (int)$_GET['track_id'] : null;
            if (!$trackId) {
                sendError('track_id kravs');
            }

            $data = getJsonInput();
            if (!isset($data['order']) || !is_array($data['order'])) {
                sendError('order-array kravs');
            }

            reorderSegments($pdo, $trackId, $data['order']);
            sendResponse(['success' => true, 'message' => 'Ordning uppdaterad']);
            break;

        /**
         * DELETE track (and all segments)
         * DELETE /api/map.php?action=delete_track&track_id=123
         */
        case 'delete_track':
            requireAdminForApi();
            if ($method !== 'DELETE') {
                sendError('DELETE method kravs', 405);
            }

            $trackId = isset($_GET['track_id']) ? (int)$_GET['track_id'] : null;
            if (!$trackId) {
                sendError('track_id kravs');
            }

            deleteEventTrack($pdo, $trackId);
            sendResponse(['success' => true, 'message' => 'Bana borttagen']);
            break;

        /**
         * POST toggle POI visibility
         * POST /api/map.php?action=toggle_poi_visibility&poi_id=456
         */
        case 'toggle_poi_visibility':
            requireAdminForApi();
            if ($method !== 'POST') {
                sendError('POST method kravs', 405);
            }

            $poiId = isset($_GET['poi_id']) ? (int)$_GET['poi_id'] : null;
            if (!$poiId) {
                sendError('poi_id kravs');
            }

            togglePoiVisibility($pdo, $poiId);
            sendResponse(['success' => true, 'message' => 'Synlighet andrad']);
            break;

        // =====================================================
        // DEFAULT
        // =====================================================

        default:
            sendError('Okand action: ' . htmlspecialchars($action), 400);
    }

} catch (PDOException $e) {
    error_log("Map API database error: " . $e->getMessage());
    sendError('Databasfel', 500);

} catch (Exception $e) {
    error_log("Map API error: " . $e->getMessage());
    sendError($e->getMessage(), 400);
}
