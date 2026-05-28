<?php
/**
 * TheHUB API - Orders (Multi-Rider Support)
 *
 * Hanterar ordrar med flera deltagare.
 *
 * Endpoints:
 * POST /api/orders.php - Skapa multi-rider order
 * GET /api/orders.php?action=my_riders - Hämta riders användaren kan anmäla
 * GET /api/orders.php?action=event_classes&event_id=X&rider_id=Y - Hämta klasser för rider
 * GET /api/orders.php?action=series_classes&series_id=X&rider_id=Y - Hämta klasser för rider i serie
 * POST /api/orders.php?action=create_rider - Skapa ny rider från flödet
 *
 * @since 2026-01-12
 */

require_once dirname(__DIR__) . '/config.php';
require_once dirname(__DIR__) . '/includes/order-manager.php';

header('Content-Type: application/json');
header('Cache-Control: no-store');

$method = $_SERVER['REQUEST_METHOD'];
$action = $_GET['action'] ?? '';

try {
    // ========================================
    // GET REQUESTS
    // ========================================
    if ($method === 'GET') {

        switch ($action) {

            // Hämta riders som användaren kan anmäla
            case 'my_riders':
                if (!hub_is_logged_in()) {
                    http_response_code(401);
                    echo json_encode(['success' => false, 'error' => 'Du måste vara inloggad']);
                    exit;
                }

                $currentUser = hub_current_user();
                $riders = getRegistrableRiders($currentUser['id']);

                echo json_encode([
                    'success' => true,
                    'riders' => $riders
                ]);
                break;

            // Hämta klasser för en rider i ett event
            case 'event_classes':
                $eventId = intval($_GET['event_id'] ?? 0);
                $riderId = intval($_GET['rider_id'] ?? 0);

                if (!$eventId || !$riderId) {
                    throw new Exception('event_id och rider_id krävs');
                }

                $classes = getEligibleClassesForEvent($eventId, $riderId);

                // Hämta event-info för early bird / late fee status
                $pdo = hub_db();
                $eventStmt = $pdo->prepare("
                    SELECT name, date, early_bird_deadline, late_fee_start
                    FROM events WHERE id = ?
                ");
                $eventStmt->execute([$eventId]);
                $event = $eventStmt->fetch(PDO::FETCH_ASSOC);

                $now = time();
                $isEarlyBird = !empty($event['early_bird_deadline']) && $now < strtotime($event['early_bird_deadline']);
                $isLateFee = !empty($event['late_fee_start']) && $now >= strtotime($event['late_fee_start']);

                // Beräkna aktuellt pris för varje klass
                foreach ($classes as &$class) {
                    if ($isEarlyBird && $class['early_bird_price']) {
                        $class['current_price'] = $class['early_bird_price'];
                        $class['price_type'] = 'early_bird';
                    } elseif ($isLateFee && $class['late_fee']) {
                        $class['current_price'] = $class['base_price'] + $class['late_fee'];
                        $class['price_type'] = 'late_fee';
                    } else {
                        $class['current_price'] = $class['base_price'];
                        $class['price_type'] = 'normal';
                    }
                }

                echo json_encode([
                    'success' => true,
                    'event' => $event,
                    'is_early_bird' => $isEarlyBird,
                    'is_late_fee' => $isLateFee,
                    'classes' => $classes
                ]);
                break;

            // Hämta klasser för en rider i en serie
            case 'series_classes':
                $seriesId = intval($_GET['series_id'] ?? 0);
                $riderId = intval($_GET['rider_id'] ?? 0);

                if (!$seriesId || !$riderId) {
                    throw new Exception('series_id och rider_id krävs');
                }

                $classes = getEligibleClassesForSeries($seriesId, $riderId);

                // Hämta serie-info
                $pdo = hub_db();
                $seriesStmt = $pdo->prepare("
                    SELECT id, name, series_discount_percent,
                           (SELECT COUNT(*) FROM events WHERE series_id = s.id) as event_count
                    FROM series s WHERE s.id = ?
                ");
                $seriesStmt->execute([$seriesId]);
                $series = $seriesStmt->fetch(PDO::FETCH_ASSOC);

                echo json_encode([
                    'success' => true,
                    'series' => $series,
                    'classes' => $classes
                ]);
                break;

            // Hämta klubbar (för skapa rider)
            case 'clubs':
                $pdo = hub_db();
                $clubsStmt = $pdo->query("SELECT id, name, city FROM clubs WHERE active = 1 ORDER BY name");
                $clubs = $clubsStmt->fetchAll(PDO::FETCH_ASSOC);

                echo json_encode([
                    'success' => true,
                    'clubs' => $clubs
                ]);
                break;

            default:
                throw new Exception('Ogiltig action');
        }
    }

    // ========================================
    // POST REQUESTS
    // ========================================
    elseif ($method === 'POST') {
        $data = json_decode(file_get_contents('php://input'), true);

        if (!$data) {
            throw new Exception('Ogiltig JSON-data');
        }

        $action = $data['action'] ?? $_GET['action'] ?? 'create';

        switch ($action) {

            // Skapa multi-rider order
            case 'create':
                if (!hub_is_logged_in()) {
                    http_response_code(401);
                    echo json_encode(['success' => false, 'error' => 'Du måste vara inloggad']);
                    exit;
                }

                $currentUser = hub_current_user();

                // Validera buyer data
                $buyerData = [
                    'user_id' => $currentUser['id'],
                    'name' => $data['buyer']['name'] ?? ($currentUser['firstname'] . ' ' . $currentUser['lastname']),
                    'email' => $data['buyer']['email'] ?? $currentUser['email'],
                    'phone' => $data['buyer']['phone'] ?? null
                ];

                $items = $data['items'] ?? [];

                if (empty($items)) {
                    throw new Exception('Inga deltagare valda');
                }

                // Validera att användaren får anmäla dessa riders
                $allowedRiders = getRegistrableRiders($currentUser['id']);
                $allowedRiderIds = array_column($allowedRiders, 'id');

                foreach ($items as $item) {
                    $riderId = intval($item['rider_id']);
                    if (!in_array($riderId, $allowedRiderIds)) {
                        throw new Exception('Du har inte behörighet att anmäla rider med ID ' . $riderId);
                    }
                }

                // Skapa order
                $result = createMultiRiderOrder($buyerData, $items, $data['discount_code'] ?? null);

                if ($result['success']) {
                    // Beräkna savings
                    $savings = calculateMultiRiderSavings(count($items));
                    $result['savings'] = $savings;
                }

                echo json_encode($result);
                break;

            // Skapa ny rider från anmälningsflödet
            case 'create_rider':
                if (!hub_is_logged_in()) {
                    http_response_code(401);
                    echo json_encode(['success' => false, 'error' => 'Du måste vara inloggad']);
                    exit;
                }

                $currentUser = hub_current_user();
                $riderData = $data['rider'] ?? $data;

                $result = createRiderFromRegistration($riderData, $currentUser['id']);

                echo json_encode($result);
                break;

            default:
                throw new Exception('Ogiltig action');
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
