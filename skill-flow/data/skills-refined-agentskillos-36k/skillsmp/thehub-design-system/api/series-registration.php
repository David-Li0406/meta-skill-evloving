<?php
/**
 * TheHUB - Series Registration API
 *
 * Handles series (season pass) registration flow:
 * - Get series info with pricing
 * - Get eligible classes for rider
 * - Validate registration
 * - Create series registration
 * - Get rider's series registrations (my tickets)
 *
 * @since 2026-01-11
 */

require_once dirname(__DIR__) . '/config.php';
require_once HUB_ROOT . '/includes/series-registration.php';

header('Content-Type: application/json');
header('Cache-Control: no-store');

// Enable CORS for frontend
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: GET, POST, OPTIONS');
header('Access-Control-Allow-Headers: Content-Type');

if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') {
    exit(0);
}

$pdo = hub_db();
$method = $_SERVER['REQUEST_METHOD'];
$action = $_GET['action'] ?? '';

try {
    // =========================================
    // GET REQUESTS
    // =========================================
    if ($method === 'GET') {
        switch ($action) {

            // Get series info with pricing for a specific class
            case 'series_info':
                $seriesId = intval($_GET['series_id'] ?? 0);
                $classId = intval($_GET['class_id'] ?? 0);

                if (!$seriesId) {
                    throw new Exception('series_id krävs');
                }

                // Get series details
                $stmt = $pdo->prepare("
                    SELECT s.*,
                           sb.name AS brand_name,
                           sb.logo AS brand_logo
                    FROM series s
                    LEFT JOIN series_brands sb ON s.brand_id = sb.id
                    WHERE s.id = ?
                ");
                $stmt->execute([$seriesId]);
                $series = $stmt->fetch(PDO::FETCH_ASSOC);

                if (!$series) {
                    throw new Exception('Serien hittades inte');
                }

                // Get event count
                $eventCount = getSeriesEventCount($pdo, $seriesId);

                // Get pricing if class specified
                $pricing = null;
                if ($classId) {
                    $pricing = calculateSeriesPrice($pdo, $seriesId, $classId);
                }

                // Check registration status
                $registrationOpen = true;
                $registrationMessage = null;

                if (!$series['allow_series_registration']) {
                    $registrationOpen = false;
                    $registrationMessage = 'Serieanmälan är inte aktiverad';
                } elseif ($series['registration_opens']) {
                    $opens = new DateTime($series['registration_opens']);
                    if (new DateTime() < $opens) {
                        $registrationOpen = false;
                        $registrationMessage = 'Anmälan öppnar ' . $opens->format('j M Y');
                    }
                }

                if ($series['registration_closes']) {
                    $closes = new DateTime($series['registration_closes']);
                    if (new DateTime() > $closes) {
                        $registrationOpen = false;
                        $registrationMessage = 'Anmälan stängde ' . $closes->format('j M Y');
                    }
                }

                echo json_encode([
                    'success' => true,
                    'series' => [
                        'id' => $series['id'],
                        'name' => $series['name'],
                        'year' => $series['year'],
                        'description' => $series['description'],
                        'logo' => $series['logo'],
                        'brand_name' => $series['brand_name'],
                        'brand_logo' => $series['brand_logo'],
                        'event_count' => $eventCount,
                        'registration_open' => $registrationOpen,
                        'registration_message' => $registrationMessage,
                        'registration_opens' => $series['registration_opens'],
                        'registration_closes' => $series['registration_closes'],
                        'discount_percent' => $series['series_discount_percent']
                    ],
                    'pricing' => $pricing
                ]);
                break;

            // Get eligible classes for rider in series
            case 'eligible_classes':
                $seriesId = intval($_GET['series_id'] ?? 0);
                $riderId = intval($_GET['rider_id'] ?? 0);

                if (!$seriesId || !$riderId) {
                    throw new Exception('series_id och rider_id krävs');
                }

                $classes = getEligibleSeriesClasses($pdo, $seriesId, $riderId);

                echo json_encode([
                    'success' => true,
                    'classes' => $classes
                ]);
                break;

            // Get events in a series with prices
            case 'series_events':
                $seriesId = intval($_GET['series_id'] ?? 0);
                $classId = intval($_GET['class_id'] ?? 0);

                if (!$seriesId) {
                    throw new Exception('series_id krävs');
                }

                // Default class to first active one if not specified
                if (!$classId) {
                    $stmt = $pdo->prepare("SELECT id FROM classes WHERE active = 1 ORDER BY sort_order LIMIT 1");
                    $stmt->execute();
                    $classId = $stmt->fetchColumn() ?: 1;
                }

                $events = getSeriesEventsWithPrices($pdo, $seriesId, $classId);

                echo json_encode([
                    'success' => true,
                    'events' => $events
                ]);
                break;

            // Validate series registration
            case 'validate':
                $seriesId = intval($_GET['series_id'] ?? 0);
                $riderId = intval($_GET['rider_id'] ?? 0);
                $classId = intval($_GET['class_id'] ?? 0);

                if (!$seriesId || !$riderId || !$classId) {
                    throw new Exception('series_id, rider_id och class_id krävs');
                }

                $validation = validateSeriesRegistration($pdo, $riderId, $seriesId, $classId);
                $pricing = calculateSeriesPrice($pdo, $seriesId, $classId);

                echo json_encode([
                    'success' => true,
                    'validation' => $validation,
                    'pricing' => $pricing
                ]);
                break;

            // Get rider's series registrations (my tickets)
            case 'my_registrations':
                if (!hub_is_logged_in()) {
                    http_response_code(401);
                    echo json_encode(['success' => false, 'error' => 'Du måste vara inloggad']);
                    exit;
                }

                $currentUser = hub_current_user();
                $riderId = intval($_GET['rider_id'] ?? $currentUser['id']);

                // Verify permission
                if ($riderId !== $currentUser['id'] && !hub_is_admin()) {
                    http_response_code(403);
                    echo json_encode(['success' => false, 'error' => 'Ingen behörighet']);
                    exit;
                }

                $registrations = getRiderSeriesRegistrations($pdo, $riderId);

                // Add events for each registration
                foreach ($registrations as &$reg) {
                    $reg['events'] = getSeriesRegistrationEvents($pdo, $reg['id']);
                }

                echo json_encode([
                    'success' => true,
                    'registrations' => $registrations
                ]);
                break;

            // Get single registration details
            case 'registration':
                $registrationId = intval($_GET['id'] ?? 0);

                if (!$registrationId) {
                    throw new Exception('id krävs');
                }

                // Get registration
                $stmt = $pdo->prepare("
                    SELECT sr.*,
                           s.name AS series_name,
                           s.year AS series_year,
                           s.logo AS series_logo,
                           c.name AS class_name,
                           c.display_name AS class_display_name,
                           CONCAT(r.firstname, ' ', r.lastname) AS rider_name,
                           r.email AS rider_email
                    FROM series_registrations sr
                    JOIN series s ON sr.series_id = s.id
                    JOIN classes c ON sr.class_id = c.id
                    JOIN riders r ON sr.rider_id = r.id
                    WHERE sr.id = ?
                ");
                $stmt->execute([$registrationId]);
                $registration = $stmt->fetch(PDO::FETCH_ASSOC);

                if (!$registration) {
                    throw new Exception('Registrering hittades inte');
                }

                // Verify permission
                if (hub_is_logged_in()) {
                    $currentUser = hub_current_user();
                    if ($registration['rider_id'] !== $currentUser['id'] && !hub_is_admin()) {
                        http_response_code(403);
                        echo json_encode(['success' => false, 'error' => 'Ingen behörighet']);
                        exit;
                    }
                }

                // Get events
                $events = getSeriesRegistrationEvents($pdo, $registrationId);

                echo json_encode([
                    'success' => true,
                    'registration' => $registration,
                    'events' => $events
                ]);
                break;

            // Get all classes for series (no rider filter)
            case 'all_classes':
                $seriesId = intval($_GET['series_id'] ?? 0);

                if (!$seriesId) {
                    throw new Exception('series_id krävs');
                }

                $stmt = $pdo->prepare("
                    SELECT c.id, c.name, c.display_name, c.gender, c.min_age, c.max_age
                    FROM classes c
                    WHERE c.active = 1
                    ORDER BY c.sort_order ASC, c.name ASC
                ");
                $stmt->execute();
                $classes = $stmt->fetchAll(PDO::FETCH_ASSOC);

                // Add pricing for each class
                foreach ($classes as &$class) {
                    $pricing = calculateSeriesPrice($pdo, $seriesId, $class['id']);
                    $class['price'] = $pricing['final_price'] ?? 0;
                    $class['original_price'] = $pricing['base_price'] ?? 0;
                    $class['discount'] = $pricing['discount_amount'] ?? 0;
                }

                echo json_encode([
                    'success' => true,
                    'classes' => $classes
                ]);
                break;

            default:
                throw new Exception('Ogiltig action: ' . $action);
        }
    }

    // =========================================
    // POST REQUESTS
    // =========================================
    elseif ($method === 'POST') {
        $data = json_decode(file_get_contents('php://input'), true);

        if (!$data) {
            throw new Exception('Ogiltig JSON-data');
        }

        $action = $data['action'] ?? $action;

        switch ($action) {

            // Create series registration
            case 'register':
                // Must be logged in
                if (!hub_is_logged_in()) {
                    http_response_code(401);
                    echo json_encode(['success' => false, 'error' => 'Du måste vara inloggad']);
                    exit;
                }

                $currentUser = hub_current_user();

                $seriesId = intval($data['series_id'] ?? 0);
                $riderId = intval($data['rider_id'] ?? $currentUser['id']);
                $classId = intval($data['class_id'] ?? 0);

                if (!$seriesId || !$classId) {
                    throw new Exception('series_id och class_id krävs');
                }

                // Verify permission to register this rider
                if ($riderId !== $currentUser['id'] && !hub_is_parent_of($currentUser['id'], $riderId) && !hub_is_admin()) {
                    http_response_code(403);
                    echo json_encode(['success' => false, 'error' => 'Du har inte behörighet att anmäla denna åkare']);
                    exit;
                }

                // Create registration
                $result = createSeriesRegistration($pdo, $riderId, $seriesId, $classId, 'web');

                if ($result['success']) {
                    // Return checkout URL
                    $checkoutUrl = '/checkout.php?type=series&id=' . $result['registration_id'];

                    echo json_encode([
                        'success' => true,
                        'registration_id' => $result['registration_id'],
                        'events_created' => $result['events_created'],
                        'pricing' => $result['pricing'],
                        'checkout_url' => $checkoutUrl,
                        'warnings' => $result['warnings']
                    ]);
                } else {
                    http_response_code(400);
                    echo json_encode([
                        'success' => false,
                        'errors' => $result['errors']
                    ]);
                }
                break;

            // Mark registration as paid (for admin/webhook)
            case 'mark_paid':
                // Admin only
                if (!hub_is_admin()) {
                    http_response_code(403);
                    echo json_encode(['success' => false, 'error' => 'Admin-åtkomst krävs']);
                    exit;
                }

                $registrationId = intval($data['registration_id'] ?? 0);
                $paymentMethod = $data['payment_method'] ?? 'manual';
                $paymentReference = $data['payment_reference'] ?? null;

                if (!$registrationId) {
                    throw new Exception('registration_id krävs');
                }

                $success = markSeriesRegistrationPaid($pdo, $registrationId, $paymentMethod, $paymentReference);

                echo json_encode([
                    'success' => $success,
                    'message' => $success ? 'Betalning registrerad' : 'Kunde inte uppdatera betalning'
                ]);
                break;

            // Cancel registration
            case 'cancel':
                if (!hub_is_logged_in()) {
                    http_response_code(401);
                    echo json_encode(['success' => false, 'error' => 'Du måste vara inloggad']);
                    exit;
                }

                $currentUser = hub_current_user();
                $registrationId = intval($data['registration_id'] ?? 0);
                $reason = $data['reason'] ?? null;

                if (!$registrationId) {
                    throw new Exception('registration_id krävs');
                }

                // Get registration to check permission
                $stmt = $pdo->prepare("SELECT rider_id FROM series_registrations WHERE id = ?");
                $stmt->execute([$registrationId]);
                $reg = $stmt->fetch(PDO::FETCH_ASSOC);

                if (!$reg) {
                    throw new Exception('Registrering hittades inte');
                }

                // Check permission
                if ($reg['rider_id'] !== $currentUser['id'] && !hub_is_admin()) {
                    http_response_code(403);
                    echo json_encode(['success' => false, 'error' => 'Ingen behörighet']);
                    exit;
                }

                $success = cancelSeriesRegistration($pdo, $registrationId, $reason);

                echo json_encode([
                    'success' => $success,
                    'message' => $success ? 'Registrering avbokad' : 'Kunde inte avboka'
                ]);
                break;

            default:
                throw new Exception('Ogiltig action: ' . $action);
        }
    }

    else {
        throw new Exception('Metod stöds ej: ' . $method);
    }

} catch (Exception $e) {
    http_response_code(400);
    echo json_encode([
        'success' => false,
        'error' => $e->getMessage()
    ]);
}
