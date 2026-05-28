<?php
/**
 * Discount Code Validation API
 * TheHUB - AJAX endpoint for validating discount codes
 */

require_once __DIR__ . '/../hub-config.php';
require_once __DIR__ . '/../includes/payment.php';

header('Content-Type: application/json');

// Require login
if (!hub_is_logged_in()) {
    http_response_code(401);
    echo json_encode(['success' => false, 'error' => 'Ej inloggad']);
    exit;
}

$currentUser = hub_current_user();

// Get request parameters
$code = $_GET['code'] ?? $_POST['code'] ?? '';
$eventId = intval($_GET['event_id'] ?? $_POST['event_id'] ?? 0);
$subtotal = floatval($_GET['subtotal'] ?? $_POST['subtotal'] ?? 0);

if (!$code) {
    echo json_encode(['success' => false, 'error' => 'Ingen rabattkod angiven']);
    exit;
}

if (!$eventId) {
    echo json_encode(['success' => false, 'error' => 'Event saknas']);
    exit;
}

// Validate the discount code
$validation = validateDiscountCode($code, $eventId, $currentUser['id'], $subtotal);

if ($validation['valid']) {
    $discount = $validation['discount'];
    $discountAmount = calculateDiscountAmount($discount, $subtotal);

    echo json_encode([
        'success' => true,
        'valid' => true,
        'code' => $discount['code'],
        'description' => $discount['description'],
        'discount_type' => $discount['discount_type'],
        'discount_value' => floatval($discount['discount_value']),
        'discount_amount' => $discountAmount,
        'label' => $discount['discount_type'] === 'percentage'
            ? $discount['discount_value'] . '%'
            : number_format($discount['discount_value'], 0) . ' kr'
    ]);
} else {
    echo json_encode([
        'success' => false,
        'valid' => false,
        'error' => $validation['error']
    ]);
}
