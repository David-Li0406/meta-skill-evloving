<?php
/**
 * API endpoint to update event series
 */

require_once __DIR__ . '/../../config.php';
require_admin();

header('Content-Type: application/json');

// Get JSON input
$input = json_decode(file_get_contents('php://input'), true);

if (!$input) {
    echo json_encode(['success' => false, 'error' => 'Invalid JSON input']);
    exit;
}

// Verify CSRF token
if (empty($input['csrf_token']) || !verify_csrf_token($input['csrf_token'])) {
    echo json_encode(['success' => false, 'error' => 'Invalid CSRF token']);
    exit;
}

$eventId = isset($input['event_id']) ? intval($input['event_id']) : 0;
$seriesId = isset($input['series_id']) && $input['series_id'] !== '' ? intval($input['series_id']) : null;

if (!$eventId) {
    echo json_encode(['success' => false, 'error' => 'Event ID required']);
    exit;
}

try {
    global $pdo;

    // Update the event using direct PDO
    $stmt = $pdo->prepare("UPDATE events SET series_id = ? WHERE id = ?");
    $stmt->execute([$seriesId, $eventId]);

    echo json_encode(['success' => true]);
} catch (Exception $e) {
    error_log("Series update error: " . $e->getMessage() . " | Event ID: $eventId | Series ID: " . var_export($seriesId, true));
    echo json_encode(['success' => false, 'error' => $e->getMessage()]);
}
