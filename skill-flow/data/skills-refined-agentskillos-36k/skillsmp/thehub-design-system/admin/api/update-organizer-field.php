<?php
/**
 * API endpoint to update organizer/contact fields for an event
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

// Whitelist of allowed organizer fields
$allowedFields = ['organizer_club_id', 'website', 'contact_email', 'contact_phone', 'registration_deadline', 'registration_deadline_time'];

if (!in_array($field, $allowedFields)) {
    echo json_encode(['success' => false, 'error' => 'Invalid field name']);
    exit;
}

// Process value based on field type
switch ($field) {
    case 'organizer_club_id':
        $value = ($value !== '' && $value !== null) ? intval($value) : null;
        break;

    case 'website':
    case 'contact_email':
    case 'contact_phone':
        $value = trim($value);
        break;

    case 'registration_deadline':
        // Validate date format
        if ($value && !preg_match('/^\d{4}-\d{2}-\d{2}$/', $value)) {
            echo json_encode(['success' => false, 'error' => 'Invalid date format']);
            exit;
        }
        break;

    case 'registration_deadline_time':
        // Validate time format or use default
        if (!$value || $value === '') {
            $value = '23:59';
        } elseif (!preg_match('/^\d{2}:\d{2}(:\d{2})?$/', $value)) {
            echo json_encode(['success' => false, 'error' => 'Invalid time format']);
            exit;
        }
        break;
}

try {
    global $pdo;

    // Update the event
    $stmt = $pdo->prepare("UPDATE events SET $field = ? WHERE id = ?");
    $stmt->execute([$value, $eventId]);

    echo json_encode(['success' => true]);
} catch (Exception $e) {
    error_log("Organizer field update error: " . $e->getMessage() . " | Event ID: $eventId | Field: $field");
    echo json_encode(['success' => false, 'error' => $e->getMessage()]);
}
