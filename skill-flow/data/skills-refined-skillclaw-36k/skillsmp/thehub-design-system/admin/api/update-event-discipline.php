<?php
/**
 * API endpoint to update event discipline
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
$discipline = isset($input['discipline']) ? trim($input['discipline']) : '';

if (!$eventId) {
    echo json_encode(['success' => false, 'error' => 'Event ID required']);
    exit;
}

// Validate discipline value
$validDisciplines = ['', 'ENDURO', 'DH', 'XC', 'XCO', 'XCM', 'DUAL_SLALOM', 'PUMPTRACK', 'GRAVEL', 'E-MTB'];
if (!in_array($discipline, $validDisciplines)) {
    echo json_encode(['success' => false, 'error' => 'Invalid discipline value']);
    exit;
}

try {
    global $pdo;

    // Update the event using direct PDO
    $stmt = $pdo->prepare("UPDATE events SET discipline = ? WHERE id = ?");
    $stmt->execute([$discipline ?: null, $eventId]);

    echo json_encode(['success' => true]);
} catch (Exception $e) {
    error_log("Discipline update error: " . $e->getMessage() . " | Event ID: $eventId");
    echo json_encode(['success' => false, 'error' => $e->getMessage()]);
}
