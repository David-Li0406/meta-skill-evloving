<?php
/**
 * Apply Discount Code to Order API
 * TheHUB - Applies a discount code to a pending order
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

// Only accept POST
if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    http_response_code(405);
    echo json_encode(['success' => false, 'error' => 'Endast POST tillåtet']);
    exit;
}

// Get parameters
$orderId = intval($_POST['order_id'] ?? 0);
$code = trim($_POST['code'] ?? '');

if (!$orderId) {
    echo json_encode(['success' => false, 'error' => 'Order-ID saknas']);
    exit;
}

if (!$code) {
    echo json_encode(['success' => false, 'error' => 'Rabattkod saknas']);
    exit;
}

// Verify user owns this order
$order = getOrder($orderId);
if (!$order) {
    echo json_encode(['success' => false, 'error' => 'Order hittades inte']);
    exit;
}

if ($order['rider_id'] != $currentUser['id'] && !hub_is_admin()) {
    echo json_encode(['success' => false, 'error' => 'Du har inte behörighet för denna order']);
    exit;
}

// Apply the discount
$result = applyDiscountToOrder($orderId, $code, $currentUser['id']);

if ($result['success']) {
    // Also regenerate Swish URLs with new amount
    $swishUrl = null;
    $swishQr = null;

    if (!empty($order['swish_number'])) {
        $swishUrl = generateSwishUrl(
            $order['swish_number'],
            $result['new_total'],
            $order['swish_message']
        );
        $swishQr = generateSwishQR(
            $order['swish_number'],
            $result['new_total'],
            $order['swish_message']
        );
    }

    echo json_encode([
        'success' => true,
        'discount_amount' => $result['discount_amount'],
        'new_discount' => $result['new_discount'],
        'new_total' => $result['new_total'],
        'swish_url' => $swishUrl,
        'swish_qr' => $swishQr,
        'message' => 'Rabattkod tillämpad!'
    ]);
} else {
    echo json_encode($result);
}
