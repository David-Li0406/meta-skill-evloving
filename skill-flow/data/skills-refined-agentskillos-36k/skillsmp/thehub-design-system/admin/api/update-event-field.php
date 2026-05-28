<?php
/**
 * Generic API endpoint to update a single event field
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
$field = isset($input['field']) ? trim($input['field']) : '';
$value = isset($input['value']) ? $input['value'] : '';

if (!$eventId) {
    echo json_encode(['success' => false, 'error' => 'Event ID required']);
    exit;
}

if (!$field) {
    echo json_encode(['success' => false, 'error' => 'Field name required']);
    exit;
}

// Whitelist of allowed fields
$allowedFields = ['event_level', 'event_format', 'point_scale_id', 'pricing_template_id', 'advent_id', 'venue_id'];

if (!in_array($field, $allowedFields)) {
    echo json_encode(['success' => false, 'error' => 'Invalid field name: ' . $field]);
    exit;
}

// Validate field-specific values
$validEventLevels = ['', 'national', 'sportmotion'];
$validEventFormats = ['', 'ENDURO', 'DH_STANDARD', 'DH_SWECUP', 'DUAL_SLALOM'];

switch ($field) {
    case 'event_level':
        if (!in_array($value, $validEventLevels)) {
            echo json_encode(['success' => false, 'error' => 'Invalid event level value']);
            exit;
        }
        $value = $value ?: null;
        break;

    case 'event_format':
        if (!in_array($value, $validEventFormats)) {
            echo json_encode(['success' => false, 'error' => 'Invalid event format value']);
            exit;
        }
        $value = $value ?: null;
        break;

    case 'point_scale_id':
        $value = ($value !== '' && $value !== null) ? intval($value) : null;
        break;

    case 'pricing_template_id':
        $value = ($value !== '' && $value !== null) ? intval($value) : null;
        break;

    case 'advent_id':
        $value = trim($value);
        break;

    case 'venue_id':
        $value = ($value !== '' && $value !== null) ? intval($value) : null;
        break;
}

try {
    global $pdo;

    // Update the event
    $stmt = $pdo->prepare("UPDATE events SET $field = ? WHERE id = ?");
    $stmt->execute([$value, $eventId]);

    echo json_encode(['success' => true]);
} catch (Exception $e) {
    error_log("Field update error: " . $e->getMessage() . " | Event ID: $eventId | Field: $field");
    echo json_encode(['success' => false, 'error' => $e->getMessage()]);
}
