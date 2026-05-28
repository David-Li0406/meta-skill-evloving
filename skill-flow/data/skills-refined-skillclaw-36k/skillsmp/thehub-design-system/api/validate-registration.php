<?php
/**
 * API: Validate Registration
 *
 * Validates if a rider can register for a specific class in an event.
 * Returns validation result with errors and warnings.
 *
 * Parameters:
 *   - event_id: Event ID
 *   - rider_id: Rider ID
 *   - class_id: Class ID
 *
 * Or for batch validation:
 *   - event_id: Event ID
 *   - rider_id: Rider ID
 *   - action: 'eligible_classes' to get all eligible classes for a rider
 *
 * Or for admin preview:
 *   - event_id: Event ID
 *   - class_id: Class ID
 *   - action: 'eligible_riders' to get riders eligible for a class
 */

require_once __DIR__ . '/../config.php';
require_once __DIR__ . '/../includes/registration-validator.php';

header('Content-Type: application/json');

// Get parameters
$eventId = filter_input(INPUT_GET, 'event_id', FILTER_VALIDATE_INT);
$riderId = filter_input(INPUT_GET, 'rider_id', FILTER_VALIDATE_INT);
$classId = filter_input(INPUT_GET, 'class_id', FILTER_VALIDATE_INT);
$action = filter_input(INPUT_GET, 'action', FILTER_SANITIZE_SPECIAL_CHARS);

// Validate required parameters
if (!$eventId) {
    http_response_code(400);
    echo json_encode([
        'success' => false,
        'error' => 'Event ID krävs.'
    ]);
    exit;
}

$db = getDB();
$pdo = $db->getPdo();

try {
    // Handle different actions
    switch ($action) {
        case 'eligible_classes':
            // Get all eligible classes for a rider
            if (!$riderId) {
                http_response_code(400);
                echo json_encode([
                    'success' => false,
                    'error' => 'Rider ID krävs för att hämta valbara klasser.'
                ]);
                exit;
            }

            $result = getEligibleClasses($pdo, $eventId, $riderId);
            echo json_encode([
                'success' => true,
                'classes' => $result
            ]);
            break;

        case 'eligible_riders':
            // Get all riders eligible for a class (admin preview)
            if (!$classId) {
                http_response_code(400);
                echo json_encode([
                    'success' => false,
                    'error' => 'Klass ID krävs för att förhandsgranska åkare.'
                ]);
                exit;
            }

            $limit = filter_input(INPUT_GET, 'limit', FILTER_VALIDATE_INT) ?: 50;
            $result = getEligibleRiders($pdo, $eventId, $classId, $limit);

            // Separate eligible and ineligible
            $eligible = array_filter($result, fn($r) => $r['allowed']);
            $ineligible = array_filter($result, fn($r) => !$r['allowed']);

            echo json_encode([
                'success' => true,
                'total' => count($result),
                'eligible_count' => count($eligible),
                'ineligible_count' => count($ineligible),
                'eligible' => array_values($eligible),
                'ineligible' => array_values($ineligible)
            ]);
            break;

        case 'event_info':
            // Get event rule information
            $eventInfo = getEventRuleType($pdo, $eventId);
            $ruleType = getEffectiveRuleType($pdo, $eventId);

            echo json_encode([
                'success' => true,
                'event' => $eventInfo,
                'rule_type' => $ruleType
            ]);
            break;

        default:
            // Standard single registration validation
            if (!$riderId || !$classId) {
                http_response_code(400);
                echo json_encode([
                    'success' => false,
                    'error' => 'Rider ID och Klass ID krävs för validering.'
                ]);
                exit;
            }

            $result = validateRegistration($pdo, $eventId, $riderId, $classId);

            // Log validation for debugging
            logValidation($pdo, $eventId, $riderId, $classId, $result);

            echo json_encode([
                'success' => true,
                'validation' => $result
            ]);
            break;
    }

} catch (Exception $e) {
    error_log("Registration validation error: " . $e->getMessage());

    http_response_code(500);
    echo json_encode([
        'success' => false,
        'error' => 'Ett fel uppstod vid validering. Försök igen senare.'
    ]);
}
