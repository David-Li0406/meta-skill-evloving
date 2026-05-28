<?php
/**
 * Swish Callback Handler
 * Receives payment status updates from Swish Commerce API
 *
 * Endpoint: /api/webhooks/swish-callback.php
 */

// Allow Swish to make POST requests
header('Content-Type: application/json');
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: POST, OPTIONS');
header('Access-Control-Allow-Headers: Content-Type');

// Handle preflight
if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') {
    http_response_code(200);
    exit;
}

// Only allow POST
if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    http_response_code(405);
    echo json_encode(['error' => 'Method not allowed']);
    exit;
}

require_once __DIR__ . '/../../config.php';

$pdo = $GLOBALS['pdo'];

// Read raw POST data
$payload = file_get_contents('php://input');
$data = json_decode($payload, true);

// Get request headers
$headers = getallheaders();

// Log webhook receipt
try {
    $stmt = $pdo->prepare("
        INSERT INTO webhook_logs
        (gateway_code, webhook_type, payload, headers, received_at)
        VALUES ('swish_handel', 'callback', ?, ?, NOW())
    ");
    $stmt->execute([
        $payload,
        json_encode($headers)
    ]);
    $logId = $pdo->lastInsertId();
} catch (Exception $e) {
    error_log("Failed to log webhook: " . $e->getMessage());
    $logId = null;
}

try {
    // Validate webhook data
    if (empty($data)) {
        throw new Exception('Empty or invalid JSON payload');
    }

    // Swish sends different callback formats
    // Payment callbacks have 'id' and 'status'
    // Refund callbacks have similar structure

    $instructionUUID = $data['id'] ?? null;
    $status = $data['status'] ?? null;

    if (!$instructionUUID) {
        throw new Exception('Missing instruction UUID in callback');
    }

    // Find order by instruction UUID
    $stmt = $pdo->prepare("
        SELECT id, payment_status, order_number
        FROM orders
        WHERE gateway_transaction_id = ? AND gateway_code = 'swish_handel'
    ");
    $stmt->execute([$instructionUUID]);
    $order = $stmt->fetch(PDO::FETCH_ASSOC);

    if (!$order) {
        // Might be a refund callback or unknown transaction
        $result = ['status' => 'ignored', 'message' => 'Order not found for UUID: ' . $instructionUUID];

        // Update log
        if ($logId) {
            $stmt = $pdo->prepare("
                UPDATE webhook_logs
                SET processed = 1, error_message = ?, processed_at = NOW()
                WHERE id = ?
            ");
            $stmt->execute([$result['message'], $logId]);
        }

        echo json_encode($result);
        exit;
    }

    // Process based on status
    switch ($status) {
        case 'PAID':
            // Payment successful
            $pdo->beginTransaction();

            try {
                // Update order
                $stmt = $pdo->prepare("
                    UPDATE orders
                    SET payment_status = 'paid',
                        payment_reference = ?,
                        paid_at = NOW(),
                        callback_received_at = NOW(),
                        gateway_metadata = JSON_SET(
                            COALESCE(gateway_metadata, '{}'),
                            '$.swish_callback', CAST(? AS JSON),
                            '$.swish_payment_reference', ?
                        )
                    WHERE id = ? AND payment_status = 'pending'
                ");
                $stmt->execute([
                    $data['paymentReference'] ?? null,
                    json_encode($data),
                    $data['paymentReference'] ?? null,
                    $order['id']
                ]);

                $rowsAffected = $stmt->rowCount();

                // Update registrations if order was updated
                if ($rowsAffected > 0) {
                    $stmt = $pdo->prepare("
                        UPDATE event_registrations
                        SET payment_status = 'paid',
                            status = 'confirmed',
                            confirmed_date = NOW()
                        WHERE order_id = ?
                    ");
                    $stmt->execute([$order['id']]);
                }

                $pdo->commit();

                $result = [
                    'status' => 'processed',
                    'message' => 'Payment confirmed for order ' . $order['order_number'],
                    'rows_affected' => $rowsAffected
                ];

            } catch (Exception $e) {
                $pdo->rollBack();
                throw $e;
            }
            break;

        case 'DECLINED':
        case 'ERROR':
        case 'CANCELLED':
            // Payment failed
            $stmt = $pdo->prepare("
                UPDATE orders
                SET payment_status = 'failed',
                    callback_received_at = NOW(),
                    gateway_metadata = JSON_SET(
                        COALESCE(gateway_metadata, '{}'),
                        '$.swish_callback', CAST(? AS JSON),
                        '$.error_code', ?,
                        '$.error_message', ?
                    )
                WHERE id = ?
            ");
            $stmt->execute([
                json_encode($data),
                $data['errorCode'] ?? $status,
                $data['errorMessage'] ?? 'Payment ' . strtolower($status),
                $order['id']
            ]);

            $result = [
                'status' => 'processed',
                'message' => 'Payment failed for order ' . $order['order_number'] . ': ' . $status
            ];
            break;

        case 'CREATED':
        case 'PENDING':
            // Still processing, no action needed
            $result = [
                'status' => 'acknowledged',
                'message' => 'Payment pending for order ' . $order['order_number']
            ];
            break;

        default:
            $result = [
                'status' => 'ignored',
                'message' => 'Unknown status: ' . $status
            ];
    }

    // Mark webhook as processed
    if ($logId) {
        $stmt = $pdo->prepare("
            UPDATE webhook_logs
            SET processed = 1, order_id = ?, webhook_type = ?, processed_at = NOW()
            WHERE id = ?
        ");
        $stmt->execute([$order['id'], $status, $logId]);
    }

    // Log payment transaction
    try {
        $stmt = $pdo->prepare("
            INSERT INTO payment_transactions
            (order_id, gateway_code, transaction_type, response_data, status, created_at, completed_at)
            VALUES (?, 'swish_handel', 'payment', ?, ?, NOW(), NOW())
        ");
        $txStatus = ($status === 'PAID') ? 'success' : (in_array($status, ['DECLINED', 'ERROR', 'CANCELLED']) ? 'failed' : 'pending');
        $stmt->execute([$order['id'], json_encode($data), $txStatus]);
    } catch (Exception $e) {
        // Non-critical, continue
        error_log("Failed to log payment transaction: " . $e->getMessage());
    }

    echo json_encode($result);

} catch (Exception $e) {
    // Log error
    if ($logId) {
        $stmt = $pdo->prepare("
            UPDATE webhook_logs
            SET error_message = ?
            WHERE id = ?
        ");
        $stmt->execute([$e->getMessage(), $logId]);
    }

    error_log("Swish callback error: " . $e->getMessage());

    http_response_code(500);
    echo json_encode(['error' => $e->getMessage()]);
}
