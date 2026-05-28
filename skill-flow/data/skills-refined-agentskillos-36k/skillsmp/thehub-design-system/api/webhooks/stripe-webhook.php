<?php
/**
 * Stripe Webhook Handler
 * Receives events from Stripe
 *
 * Endpoint: /api/webhooks/stripe-webhook.php
 */

header('Content-Type: application/json');

// Only allow POST
if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    http_response_code(405);
    echo json_encode(['error' => 'Method not allowed']);
    exit;
}

require_once __DIR__ . '/../../config.php';
require_once __DIR__ . '/../../includes/payment/StripeClient.php';

$pdo = $GLOBALS['pdo'];

// Read raw POST data
$payload = file_get_contents('php://input');
$sigHeader = $_SERVER['HTTP_STRIPE_SIGNATURE'] ?? '';

// Get webhook secret from environment
$webhookSecret = getenv('STRIPE_WEBHOOK_SECRET');
if (!$webhookSecret && function_exists('env')) {
    $webhookSecret = env('STRIPE_WEBHOOK_SECRET', '');
}

// Log webhook receipt
try {
    $stmt = $pdo->prepare("
        INSERT INTO webhook_logs
        (gateway_code, webhook_type, payload, signature, received_at)
        VALUES ('stripe', 'webhook', ?, ?, NOW())
    ");
    $stmt->execute([$payload, $sigHeader]);
    $logId = $pdo->lastInsertId();
} catch (Exception $e) {
    error_log("Failed to log webhook: " . $e->getMessage());
    $logId = null;
}

try {
    // Parse event data
    $event = json_decode($payload, true);

    if (!$event) {
        throw new Exception('Invalid JSON payload');
    }

    // Verify webhook signature if secret is configured
    if ($webhookSecret) {
        $stripeApiKey = getenv('STRIPE_SECRET_KEY');
        if (!$stripeApiKey && function_exists('env')) {
            $stripeApiKey = env('STRIPE_SECRET_KEY', '');
        }

        if ($stripeApiKey) {
            $client = new \TheHUB\Payment\StripeClient($stripeApiKey);
            $verification = $client->verifyWebhookSignature($payload, $sigHeader, $webhookSecret);

            if (!$verification['valid']) {
                throw new Exception('Invalid webhook signature: ' . ($verification['error'] ?? 'Unknown error'));
            }
        }
    }

    $type = $event['type'] ?? '';
    $data = $event['data']['object'] ?? [];

    // Update webhook log with type
    if ($logId) {
        $stmt = $pdo->prepare("UPDATE webhook_logs SET webhook_type = ? WHERE id = ?");
        $stmt->execute([$type, $logId]);
    }

    // Handle different event types
    switch ($type) {
        case 'payment_intent.succeeded':
            $paymentIntentId = $data['id'] ?? null;

            if (!$paymentIntentId) {
                throw new Exception('Missing payment_intent ID');
            }

            // Find order by payment intent ID
            $stmt = $pdo->prepare("
                SELECT id, payment_status, order_number
                FROM orders
                WHERE gateway_transaction_id = ? AND gateway_code = 'stripe'
            ");
            $stmt->execute([$paymentIntentId]);
            $order = $stmt->fetch(PDO::FETCH_ASSOC);

            if ($order && $order['payment_status'] === 'pending') {
                $pdo->beginTransaction();

                try {
                    // Mark order as paid
                    $stmt = $pdo->prepare("
                        UPDATE orders
                        SET payment_status = 'paid',
                            payment_reference = ?,
                            paid_at = NOW(),
                            callback_received_at = NOW(),
                            gateway_metadata = JSON_SET(
                                COALESCE(gateway_metadata, '{}'),
                                '$.stripe_event', CAST(? AS JSON)
                            )
                        WHERE id = ?
                    ");
                    $stmt->execute([
                        $data['id'],
                        json_encode(['type' => $type, 'payment_intent' => $data['id']]),
                        $order['id']
                    ]);

                    // Update registrations
                    $stmt = $pdo->prepare("
                        UPDATE event_registrations
                        SET payment_status = 'paid',
                            status = 'confirmed',
                            confirmed_date = NOW()
                        WHERE order_id = ?
                    ");
                    $stmt->execute([$order['id']]);

                    $pdo->commit();

                    // Mark webhook as processed
                    if ($logId) {
                        $stmt = $pdo->prepare("
                            UPDATE webhook_logs
                            SET processed = 1, order_id = ?, processed_at = NOW()
                            WHERE id = ?
                        ");
                        $stmt->execute([$order['id'], $logId]);
                    }

                    $result = [
                        'status' => 'processed',
                        'message' => 'Payment confirmed for order ' . $order['order_number']
                    ];

                } catch (Exception $e) {
                    $pdo->rollBack();
                    throw $e;
                }
            } else {
                $result = [
                    'status' => 'ignored',
                    'message' => $order ? 'Order already processed' : 'Order not found'
                ];
            }
            break;

        case 'payment_intent.payment_failed':
            $paymentIntentId = $data['id'] ?? null;

            if ($paymentIntentId) {
                $stmt = $pdo->prepare("
                    UPDATE orders
                    SET payment_status = 'failed',
                        callback_received_at = NOW(),
                        gateway_metadata = JSON_SET(
                            COALESCE(gateway_metadata, '{}'),
                            '$.stripe_error', ?
                        )
                    WHERE gateway_transaction_id = ? AND gateway_code = 'stripe' AND payment_status = 'pending'
                ");
                $stmt->execute([
                    $data['last_payment_error']['message'] ?? 'Payment failed',
                    $paymentIntentId
                ]);

                $result = ['status' => 'processed', 'message' => 'Payment failure recorded'];
            } else {
                $result = ['status' => 'ignored', 'message' => 'Missing payment_intent ID'];
            }
            break;

        case 'charge.refunded':
            $paymentIntentId = $data['payment_intent'] ?? null;

            if ($paymentIntentId) {
                $stmt = $pdo->prepare("
                    UPDATE orders
                    SET payment_status = 'refunded',
                        refunded_at = NOW(),
                        callback_received_at = NOW()
                    WHERE gateway_transaction_id = ? AND gateway_code = 'stripe'
                ");
                $stmt->execute([$paymentIntentId]);

                $result = ['status' => 'processed', 'message' => 'Refund recorded'];
            } else {
                $result = ['status' => 'ignored', 'message' => 'Missing payment_intent ID'];
            }
            break;

        case 'account.updated':
            // Connected account status update
            $accountId = $data['id'] ?? null;

            if ($accountId) {
                $chargesEnabled = $data['charges_enabled'] ?? false;
                $payoutsEnabled = $data['payouts_enabled'] ?? false;
                $detailsSubmitted = $data['details_submitted'] ?? false;

                $status = 'pending';
                if ($chargesEnabled && $payoutsEnabled) {
                    $status = 'active';
                } elseif (!$detailsSubmitted) {
                    $status = 'pending';
                } else {
                    $status = 'disabled';
                }

                $stmt = $pdo->prepare("
                    UPDATE payment_recipients
                    SET stripe_account_status = ?
                    WHERE stripe_account_id = ?
                ");
                $stmt->execute([$status, $accountId]);

                $result = ['status' => 'processed', 'message' => 'Account status updated to: ' . $status];
            } else {
                $result = ['status' => 'ignored', 'message' => 'Missing account ID'];
            }
            break;

        default:
            // Unhandled event type
            $result = ['status' => 'ignored', 'message' => 'Unhandled event type: ' . $type];
    }

    // Mark webhook as processed if not already done
    if ($logId && !in_array($type, ['payment_intent.succeeded'])) {
        $stmt = $pdo->prepare("
            UPDATE webhook_logs
            SET processed = 1, processed_at = NOW()
            WHERE id = ?
        ");
        $stmt->execute([$logId]);
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

    error_log("Stripe webhook error: " . $e->getMessage());

    http_response_code(400);
    echo json_encode(['error' => $e->getMessage()]);
}
