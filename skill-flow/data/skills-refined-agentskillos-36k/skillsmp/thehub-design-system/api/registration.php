<?php
/**
 * TheHUB V1.0 - Registration API
 *
 * Handles event registration flow including:
 * - Get rider info for registration
 * - Validate registration eligibility
 * - Create registration (pending payment)
 * - Get checkout URL for WooCommerce
 *
 * Uses V2's registration-validator for validation logic
 */

require_once dirname(__DIR__) . '/config.php';
require_once HUB_ROOT . '/includes/registration-validator.php';

header('Content-Type: application/json');
header('Cache-Control: no-store');

$pdo = hub_db();
$method = $_SERVER['REQUEST_METHOD'];
$action = $_GET['action'] ?? '';

try {
    // GET requests
    if ($method === 'GET') {
        switch ($action) {
            case 'get_rider':
                // Get rider info for registration form
                $riderId = intval($_GET['rider_id'] ?? 0);
                $eventId = intval($_GET['event_id'] ?? 0);

                if (!$riderId || !$eventId) {
                    throw new Exception('rider_id och event_id krävs');
                }

                // Get rider
                $stmt = $pdo->prepare("
                    SELECT r.id, r.firstname, r.lastname, r.birth_year, r.gender,
                           r.license_number, r.license_type, c.name as club_name
                    FROM riders r
                    LEFT JOIN clubs c ON r.club_id = c.id
                    WHERE r.id = ?
                ");
                $stmt->execute([$riderId]);
                $rider = $stmt->fetch(PDO::FETCH_ASSOC);

                if (!$rider) {
                    throw new Exception('Åkare hittades inte');
                }

                // Get eligible classes for this rider in this event
                $eligibleClasses = getEligibleClasses($pdo, $eventId, $riderId);

                // Get suggested class (first eligible)
                $suggested = !empty($eligibleClasses) ? $eligibleClasses[0] : null;

                // Get price for suggested class
                $price = 0;
                if ($suggested) {
                    $priceStmt = $pdo->prepare("
                        SELECT ptr.base_price
                        FROM events e
                        JOIN pricing_template_rules ptr ON e.pricing_template_id = ptr.template_id
                        WHERE e.id = ? AND ptr.class_id = ?
                    ");
                    $priceStmt->execute([$eventId, $suggested['class_id']]);
                    $priceRow = $priceStmt->fetch(PDO::FETCH_ASSOC);
                    $price = $priceRow['base_price'] ?? 0;
                }

                echo json_encode([
                    'success' => true,
                    'rider' => $rider,
                    'name' => $rider['firstname'] . ' ' . $rider['lastname'],
                    'eligible_classes' => $eligibleClasses,
                    'suggested_class_id' => $suggested['class_id'] ?? null,
                    'suggested_class_name' => $suggested['class_name'] ?? 'Välj klass',
                    'price' => $price
                ]);
                break;

            case 'validate':
                // Validate single registration
                $eventId = intval($_GET['event_id'] ?? 0);
                $riderId = intval($_GET['rider_id'] ?? 0);
                $classId = intval($_GET['class_id'] ?? 0);

                if (!$eventId || !$riderId || !$classId) {
                    throw new Exception('event_id, rider_id och class_id krävs');
                }

                $result = validateRegistration($pdo, $eventId, $riderId, $classId);

                echo json_encode([
                    'success' => true,
                    'validation' => $result
                ]);
                break;

            case 'eligible_classes':
                // Get eligible classes for rider
                $eventId = intval($_GET['event_id'] ?? 0);
                $riderId = intval($_GET['rider_id'] ?? 0);

                if (!$eventId || !$riderId) {
                    throw new Exception('event_id och rider_id krävs');
                }

                $classes = getEligibleClasses($pdo, $eventId, $riderId);

                echo json_encode([
                    'success' => true,
                    'classes' => $classes
                ]);
                break;

            case 'event_classes':
                // Get all classes for an event with pricing
                $eventId = intval($_GET['event_id'] ?? 0);

                if (!$eventId) {
                    throw new Exception('event_id krävs');
                }

                $stmt = $pdo->prepare("
                    SELECT epr.id, epr.class_id, c.name, c.display_name, c.gender,
                           c.min_age, c.max_age,
                           epr.base_price as price
                    FROM event_pricing_rules epr
                    JOIN classes c ON epr.class_id = c.id
                    WHERE epr.event_id = ?
                    ORDER BY c.sort_order, c.name
                ");
                $stmt->execute([$eventId]);
                $classes = $stmt->fetchAll(PDO::FETCH_ASSOC);

                echo json_encode([
                    'success' => true,
                    'classes' => $classes
                ]);
                break;

            default:
                throw new Exception('Ogiltig action');
        }
    }

    // POST requests - Create registration
    elseif ($method === 'POST') {
        $data = json_decode(file_get_contents('php://input'), true);

        if (!$data) {
            throw new Exception('Ogiltig JSON-data');
        }

        $eventId = intval($data['event_id'] ?? 0);
        $participants = $data['participants'] ?? [];

        if (!$eventId || empty($participants)) {
            throw new Exception('event_id och participants krävs');
        }

        // Verify user is logged in
        if (!hub_is_logged_in()) {
            http_response_code(401);
            echo json_encode(['success' => false, 'error' => 'Du måste vara inloggad']);
            exit;
        }

        $currentUser = hub_current_user();

        // Validate all participants
        $errors = [];
        $validRegistrations = [];

        foreach ($participants as $index => $p) {
            $riderId = intval($p['rider_id'] ?? 0);
            $classId = intval($p['class_id'] ?? 0);

            if (!$riderId || !$classId) {
                $errors[] = "Deltagare " . ($index + 1) . ": Saknar rider_id eller class_id";
                continue;
            }

            // Check permission to register this rider
            if ($riderId !== $currentUser['id'] && !hub_is_parent_of($currentUser['id'], $riderId)) {
                $errors[] = "Deltagare " . ($index + 1) . ": Du har inte behörighet att anmäla denna åkare";
                continue;
            }

            // Validate registration
            $validation = validateRegistration($pdo, $eventId, $riderId, $classId);

            if (!$validation['allowed']) {
                $errors[] = "Deltagare " . ($index + 1) . ": " . implode(', ', $validation['errors']);
                continue;
            }

            // Check not already registered
            $checkStmt = $pdo->prepare("
                SELECT id FROM event_registrations
                WHERE event_id = ? AND rider_id = ? AND status != 'cancelled'
            ");
            $checkStmt->execute([$eventId, $riderId]);
            if ($checkStmt->fetch()) {
                $errors[] = "Deltagare " . ($index + 1) . ": Redan anmäld till detta event";
                continue;
            }

            $validRegistrations[] = [
                'rider_id' => $riderId,
                'class_id' => $classId,
                'price' => $p['price'] ?? 0
            ];
        }

        if (!empty($errors)) {
            echo json_encode([
                'success' => false,
                'errors' => $errors
            ]);
            exit;
        }

        // Create registrations
        $pdo->beginTransaction();

        try {
            $registrationIds = [];

            foreach ($validRegistrations as $reg) {
                // Get rider info
                $riderStmt = $pdo->prepare("
                    SELECT firstname, lastname, email, birth_year, gender, club_id
                    FROM riders WHERE id = ?
                ");
                $riderStmt->execute([$reg['rider_id']]);
                $rider = $riderStmt->fetch(PDO::FETCH_ASSOC);

                // Get club name
                $clubName = '';
                if ($rider['club_id']) {
                    $clubStmt = $pdo->prepare("SELECT name FROM clubs WHERE id = ?");
                    $clubStmt->execute([$rider['club_id']]);
                    $clubName = $clubStmt->fetchColumn() ?: '';
                }

                // Get class name
                $classStmt = $pdo->prepare("SELECT name FROM classes WHERE id = ?");
                $classStmt->execute([$reg['class_id']]);
                $className = $classStmt->fetchColumn();

                // Insert registration
                $insertStmt = $pdo->prepare("
                    INSERT INTO event_registrations
                    (event_id, rider_id, first_name, last_name, email, birth_year, gender,
                     club_name, category, status, payment_status, registration_date, registered_by)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 'pending', 'unpaid', NOW(), ?)
                ");
                $insertStmt->execute([
                    $eventId,
                    $reg['rider_id'],
                    $rider['firstname'],
                    $rider['lastname'],
                    $rider['email'],
                    $rider['birth_year'],
                    $rider['gender'],
                    $clubName,
                    $className,
                    $currentUser['id']
                ]);

                $registrationIds[] = $pdo->lastInsertId();
            }

            $pdo->commit();

            // Generate checkout URL
            $checkoutUrl = WC_CHECKOUT_URL . '?registration=' . implode(',', $registrationIds);

            echo json_encode([
                'success' => true,
                'registration_ids' => $registrationIds,
                'checkout_url' => $checkoutUrl,
                'total' => array_sum(array_column($validRegistrations, 'price'))
            ]);

        } catch (Exception $e) {
            $pdo->rollBack();
            throw $e;
        }
    }

    else {
        throw new Exception('Metod stöds ej');
    }

} catch (Exception $e) {
    http_response_code(400);
    echo json_encode([
        'success' => false,
        'error' => $e->getMessage()
    ]);
}
