<?php
/**
 * API endpoint to bulk update events
 * Handles multiple event updates in a single request
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

$changes = isset($input['changes']) ? $input['changes'] : [];

if (empty($changes)) {
    echo json_encode(['success' => false, 'error' => 'No changes provided']);
    exit;
}

// Valid field values
$validDisciplines = ['', 'ENDURO', 'DH', 'XC', 'XCO', 'XCM', 'DUAL_SLALOM', 'PUMPTRACK', 'GRAVEL', 'E-MTB'];
$validEventLevels = ['', 'national', 'sportmotion'];
$validEventFormats = ['', 'ENDURO', 'DH_STANDARD', 'DH_SWECUP', 'DUAL_SLALOM'];

try {
    global $pdo;

    error_log("=== BULK UPDATE START ===");
    error_log("Changes received: " . json_encode($changes));

    $pdo->beginTransaction();
    error_log("Transaction started");

    $updateCount = 0;
    $errors = [];

    foreach ($changes as $eventId => $fields) {
        $eventId = intval($eventId);
        error_log("Processing event ID: $eventId");

        if ($eventId <= 0) {
            $errors[] = "Invalid event ID: $eventId";
            continue;
        }

        foreach ($fields as $fieldName => $value) {
            error_log("  Updating field $fieldName to: " . var_export($value, true));
            try {
                switch ($fieldName) {
                    case 'series_id':
                        $seriesId = ($value !== '' && $value !== null) ? intval($value) : null;
                        $stmt = $pdo->prepare("UPDATE events SET series_id = ? WHERE id = ?");
                        $stmt->execute([$seriesId, $eventId]);
                        $updateCount++;
                        break;

                    case 'discipline':
                        if (!in_array($value, $validDisciplines)) {
                            $errors[] = "Invalid discipline value for event $eventId: $value";
                            continue 2;
                        }
                        $discipline = $value ?: null;
                        $stmt = $pdo->prepare("UPDATE events SET discipline = ? WHERE id = ?");
                        $stmt->execute([$discipline, $eventId]);
                        $updateCount++;
                        break;

                    case 'event_level':
                        if (!in_array($value, $validEventLevels)) {
                            $errors[] = "Invalid event_level value for event $eventId: $value";
                            continue 2;
                        }
                        $eventLevel = $value ?: null;
                        $stmt = $pdo->prepare("UPDATE events SET event_level = ? WHERE id = ?");
                        $stmt->execute([$eventLevel, $eventId]);
                        $updateCount++;
                        break;

                    case 'event_format':
                        if (!in_array($value, $validEventFormats)) {
                            $errors[] = "Invalid event_format value for event $eventId: $value";
                            continue 2;
                        }
                        $eventFormat = $value ?: null;
                        $stmt = $pdo->prepare("UPDATE events SET event_format = ? WHERE id = ?");
                        $stmt->execute([$eventFormat, $eventId]);
                        $updateCount++;
                        break;

                    case 'pricing_template_id':
                        $pricingTemplateId = ($value !== '' && $value !== null) ? intval($value) : null;
                        $stmt = $pdo->prepare("UPDATE events SET pricing_template_id = ? WHERE id = ?");
                        $stmt->execute([$pricingTemplateId, $eventId]);
                        $updateCount++;
                        break;

                    case 'advent_id':
                        $adventId = trim($value);
                        $stmt = $pdo->prepare("UPDATE events SET advent_id = ? WHERE id = ?");
                        $stmt->execute([$adventId, $eventId]);
                        $updateCount++;
                        break;

                    case 'point_scale_id':
                        $pointScaleId = ($value !== '' && $value !== null) ? intval($value) : null;
                        $stmt = $pdo->prepare("UPDATE events SET point_scale_id = ? WHERE id = ?");
                        $stmt->execute([$pointScaleId, $eventId]);
                        $updateCount++;
                        break;

                    case 'venue_id':
                        $venueId = ($value !== '' && $value !== null) ? intval($value) : null;
                        $stmt = $pdo->prepare("UPDATE events SET venue_id = ? WHERE id = ?");
                        $stmt->execute([$venueId, $eventId]);
                        $updateCount++;
                        break;

                    case 'organizer_club_id':
                        $organizerClubId = ($value !== '' && $value !== null) ? intval($value) : null;
                        $stmt = $pdo->prepare("UPDATE events SET organizer_club_id = ? WHERE id = ?");
                        $stmt->execute([$organizerClubId, $eventId]);
                        $updateCount++;
                        break;

                    case 'website':
                        $website = trim($value);
                        $stmt = $pdo->prepare("UPDATE events SET website = ? WHERE id = ?");
                        $stmt->execute([$website, $eventId]);
                        $updateCount++;
                        break;

                    case 'contact_email':
                        $contactEmail = trim($value);
                        $stmt = $pdo->prepare("UPDATE events SET contact_email = ? WHERE id = ?");
                        $stmt->execute([$contactEmail, $eventId]);
                        $updateCount++;
                        break;

                    case 'contact_phone':
                        $contactPhone = trim($value);
                        $stmt = $pdo->prepare("UPDATE events SET contact_phone = ? WHERE id = ?");
                        $stmt->execute([$contactPhone, $eventId]);
                        $updateCount++;
                        break;

                    case 'registration_deadline':
                        // Validate date format
                        if ($value && !preg_match('/^\d{4}-\d{2}-\d{2}$/', $value)) {
                            $errors[] = "Invalid date format for event $eventId";
                            continue 2;
                        }
                        $stmt = $pdo->prepare("UPDATE events SET registration_deadline = ? WHERE id = ?");
                        $stmt->execute([$value, $eventId]);
                        $updateCount++;
                        break;

                    case 'registration_deadline_time':
                        // Validate time format or use default
                        $time = $value;
                        if (!$time || $time === '') {
                            $time = '23:59';
                        } elseif (!preg_match('/^\d{2}:\d{2}(:\d{2})?$/', $time)) {
                            $errors[] = "Invalid time format for event $eventId";
                            continue 2;
                        }
                        $stmt = $pdo->prepare("UPDATE events SET registration_deadline_time = ? WHERE id = ?");
                        $stmt->execute([$time, $eventId]);
                        $updateCount++;
                        break;

                    default:
                        $errors[] = "Unknown field: $fieldName for event $eventId";
                }
            } catch (Exception $e) {
                $errors[] = "Error updating event $eventId field $fieldName: " . $e->getMessage();
            }
        }
    }

    if (!empty($errors)) {
        error_log("Rolling back due to errors: " . json_encode($errors));
        $pdo->rollBack();
        echo json_encode([
            'success' => false,
            'error' => 'Some updates failed: ' . implode(', ', $errors),
            'errors' => $errors
        ]);
        exit;
    }

    error_log("Committing transaction with $updateCount updates");
    $pdo->commit();
    error_log("Transaction committed successfully");

    // VERIFY: Check if changes were actually saved
    foreach ($changes as $eventId => $fields) {
        $eventId = intval($eventId);
        $stmt = $pdo->prepare("SELECT * FROM events WHERE id = ?");
        $stmt->execute([$eventId]);
        $event = $stmt->fetch(PDO::FETCH_ASSOC);
        error_log("VERIFY Event $eventId after commit: " . json_encode($event));
    }

    echo json_encode([
        'success' => true,
        'updated' => $updateCount,
        'message' => "$updateCount updates applied successfully"
    ]);

} catch (Exception $e) {
    if ($pdo->inTransaction()) {
        $pdo->rollBack();
    }
    error_log("Bulk update error: " . $e->getMessage());
    echo json_encode(['success' => false, 'error' => $e->getMessage()]);
}
