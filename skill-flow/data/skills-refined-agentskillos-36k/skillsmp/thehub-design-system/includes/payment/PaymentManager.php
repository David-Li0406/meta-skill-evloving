<?php
/**
 * Payment Manager - Central hub for all payment operations
 * Handles gateway selection, payment initiation, and status tracking
 *
 * @package TheHUB\Payment
 */

namespace TheHUB\Payment;

require_once __DIR__ . '/GatewayInterface.php';
require_once __DIR__ . '/SwishClient.php';
require_once __DIR__ . '/StripeClient.php';
require_once __DIR__ . '/gateways/SwishGateway.php';
require_once __DIR__ . '/gateways/StripeGateway.php';
require_once __DIR__ . '/gateways/ManualGateway.php';

class PaymentManager {
    private $pdo;
    private $gateways = [];

    public function __construct($pdo) {
        $this->pdo = $pdo;
        $this->registerGateways();
    }

    /**
     * Register all available gateways
     */
    private function registerGateways() {
        $this->gateways['manual'] = new Gateways\ManualGateway($this->pdo);
        $this->gateways['swish_handel'] = new Gateways\SwishGateway($this->pdo);
        $this->gateways['stripe'] = new Gateways\StripeGateway($this->pdo);
    }

    /**
     * Get appropriate gateway for a payment recipient
     *
     * @param int $paymentRecipientId Payment recipient ID
     * @return GatewayInterface Gateway instance
     */
    public function getGateway(int $paymentRecipientId): GatewayInterface {
        $stmt = $this->pdo->prepare("
            SELECT gateway_type, gateway_enabled
            FROM payment_recipients
            WHERE id = ? AND active = 1
        ");
        $stmt->execute([$paymentRecipientId]);
        $recipient = $stmt->fetch(\PDO::FETCH_ASSOC);

        if (!$recipient || !$recipient['gateway_enabled']) {
            return $this->gateways['manual'];
        }

        $gatewayType = $recipient['gateway_type'];

        // Check if the gateway is available for this recipient
        $gateway = $this->gateways[$gatewayType] ?? $this->gateways['manual'];

        if ($gateway->isAvailable($paymentRecipientId)) {
            return $gateway;
        }

        // Fallback to manual if gateway is not properly configured
        return $this->gateways['manual'];
    }

    /**
     * Get gateway by code
     *
     * @param string $gatewayCode Gateway code
     * @return GatewayInterface|null Gateway instance or null
     */
    public function getGatewayByCode(string $gatewayCode): ?GatewayInterface {
        return $this->gateways[$gatewayCode] ?? null;
    }

    /**
     * Initiate payment for an order
     *
     * @param int $orderId Order ID
     * @return array Result with payment info
     */
    public function initiatePayment(int $orderId): array {
        // Get order details
        $stmt = $this->pdo->prepare("
            SELECT o.*, e.name as event_name, e.payment_recipient_id,
                   pr.gateway_type, pr.gateway_config, pr.swish_number
            FROM orders o
            JOIN events e ON o.event_id = e.id
            LEFT JOIN payment_recipients pr ON e.payment_recipient_id = pr.id
            WHERE o.id = ?
        ");
        $stmt->execute([$orderId]);
        $order = $stmt->fetch(\PDO::FETCH_ASSOC);

        if (!$order) {
            return ['success' => false, 'error' => 'Order not found'];
        }

        if (!$order['payment_recipient_id']) {
            return ['success' => false, 'error' => 'No payment recipient configured for this event'];
        }

        // Get appropriate gateway
        $gateway = $this->getGateway($order['payment_recipient_id']);

        // Prepare order data for gateway
        $orderData = [
            'id' => $order['id'],
            'order_number' => $order['order_number'],
            'total_amount' => $order['total_amount'],
            'payment_recipient_id' => $order['payment_recipient_id'],
            'payer_phone' => $order['payer_phone'] ?? null,
            'customer_email' => $order['customer_email'],
            'customer_name' => $order['customer_name'],
            'event_id' => $order['event_id'],
            'event_name' => $order['event_name']
        ];

        // Initiate payment through gateway
        $result = $gateway->initiatePayment($orderData);

        // Log transaction
        $this->logTransaction($orderId, $gateway->getCode(), 'payment', null, $result);

        // Update order with gateway info
        if ($result['success']) {
            $stmt = $this->pdo->prepare("
                UPDATE orders
                SET gateway_code = ?,
                    gateway_transaction_id = ?,
                    gateway_metadata = ?
                WHERE id = ?
            ");
            $stmt->execute([
                $gateway->getCode(),
                $result['transaction_id'] ?? null,
                json_encode($result['metadata'] ?? []),
                $orderId
            ]);
        }

        return $result;
    }

    /**
     * Check payment status
     *
     * @param int $orderId Order ID
     * @return array Status result
     */
    public function checkPaymentStatus(int $orderId): array {
        $stmt = $this->pdo->prepare("
            SELECT gateway_code, gateway_transaction_id, payment_status
            FROM orders
            WHERE id = ?
        ");
        $stmt->execute([$orderId]);
        $order = $stmt->fetch(\PDO::FETCH_ASSOC);

        if (!$order) {
            return ['success' => false, 'error' => 'Order not found'];
        }

        // If already paid, return immediately
        if ($order['payment_status'] === 'paid') {
            return ['success' => true, 'status' => 'paid', 'paid' => true];
        }

        // If no gateway transaction, can't check
        if (!$order['gateway_transaction_id']) {
            return ['success' => true, 'status' => $order['payment_status'], 'paid' => false];
        }

        // Check with gateway
        $gateway = $this->gateways[$order['gateway_code']] ?? $this->gateways['manual'];
        $result = $gateway->checkStatus($order['gateway_transaction_id']);

        // Log transaction
        $this->logTransaction($orderId, $order['gateway_code'], 'status_check', null, $result);

        // Update order if status changed
        if ($result['paid'] ?? false) {
            $this->markOrderPaid($orderId, $result['payment_reference'] ?? $order['gateway_transaction_id']);
        }

        return $result;
    }

    /**
     * Process refund for an order
     *
     * @param int $orderId Order ID
     * @param float|null $amount Amount to refund (null for full)
     * @return array Refund result
     */
    public function refund(int $orderId, ?float $amount = null): array {
        $stmt = $this->pdo->prepare("
            SELECT gateway_code, gateway_transaction_id, payment_status, total_amount
            FROM orders
            WHERE id = ?
        ");
        $stmt->execute([$orderId]);
        $order = $stmt->fetch(\PDO::FETCH_ASSOC);

        if (!$order) {
            return ['success' => false, 'error' => 'Order not found'];
        }

        if ($order['payment_status'] !== 'paid') {
            return ['success' => false, 'error' => 'Order is not paid'];
        }

        $refundAmount = $amount ?? $order['total_amount'];
        $gateway = $this->gateways[$order['gateway_code']] ?? $this->gateways['manual'];

        $result = $gateway->refund($order['gateway_transaction_id'], $refundAmount);

        // Log transaction
        $this->logTransaction($orderId, $order['gateway_code'], 'refund', ['amount' => $refundAmount], $result);

        // Update order status if successful
        if ($result['success']) {
            $stmt = $this->pdo->prepare("
                UPDATE orders
                SET payment_status = 'refunded',
                    refunded_at = NOW()
                WHERE id = ?
            ");
            $stmt->execute([$orderId]);
        }

        return $result;
    }

    /**
     * Cancel payment for an order
     *
     * @param int $orderId Order ID
     * @return array Cancel result
     */
    public function cancel(int $orderId): array {
        $stmt = $this->pdo->prepare("
            SELECT gateway_code, gateway_transaction_id, payment_status
            FROM orders
            WHERE id = ?
        ");
        $stmt->execute([$orderId]);
        $order = $stmt->fetch(\PDO::FETCH_ASSOC);

        if (!$order) {
            return ['success' => false, 'error' => 'Order not found'];
        }

        if ($order['payment_status'] === 'paid') {
            return ['success' => false, 'error' => 'Cannot cancel paid order, use refund instead'];
        }

        $gateway = $this->gateways[$order['gateway_code']] ?? $this->gateways['manual'];

        $result = $gateway->cancel($order['gateway_transaction_id']);

        // Log transaction
        $this->logTransaction($orderId, $order['gateway_code'], 'cancel', null, $result);

        // Update order status
        $stmt = $this->pdo->prepare("
            UPDATE orders
            SET payment_status = 'cancelled',
                cancelled_at = NOW()
            WHERE id = ?
        ");
        $stmt->execute([$orderId]);

        return $result;
    }

    /**
     * Mark order as paid
     *
     * @param int $orderId Order ID
     * @param string $paymentReference Payment reference
     * @return bool Success
     */
    public function markOrderPaid(int $orderId, string $paymentReference = ''): bool {
        $this->pdo->beginTransaction();

        try {
            // Update order
            $stmt = $this->pdo->prepare("
                UPDATE orders
                SET payment_status = 'paid',
                    payment_reference = ?,
                    paid_at = NOW()
                WHERE id = ? AND payment_status = 'pending'
            ");
            $stmt->execute([$paymentReference, $orderId]);

            if ($stmt->rowCount() === 0) {
                $this->pdo->rollBack();
                return false;
            }

            // Update linked registrations
            $stmt = $this->pdo->prepare("
                UPDATE event_registrations
                SET payment_status = 'paid',
                    status = 'confirmed',
                    confirmed_date = NOW()
                WHERE order_id = ?
            ");
            $stmt->execute([$orderId]);

            $this->pdo->commit();
            return true;

        } catch (\Exception $e) {
            $this->pdo->rollBack();
            throw $e;
        }
    }

    /**
     * Log payment transaction
     *
     * @param int $orderId Order ID
     * @param string $gatewayCode Gateway code
     * @param string $type Transaction type
     * @param array|null $requestData Request data
     * @param array $responseData Response data
     */
    private function logTransaction(int $orderId, string $gatewayCode, string $type, ?array $requestData, array $responseData) {
        try {
            $stmt = $this->pdo->prepare("
                INSERT INTO payment_transactions
                (order_id, gateway_code, transaction_type, request_data, response_data, status, created_at, completed_at)
                VALUES (?, ?, ?, ?, ?, ?, NOW(), NOW())
            ");

            $status = ($responseData['success'] ?? false) ? 'success' : 'failed';

            $stmt->execute([
                $orderId,
                $gatewayCode,
                $type,
                $requestData ? json_encode($requestData) : null,
                json_encode($responseData),
                $status
            ]);
        } catch (\Exception $e) {
            // Log error but don't fail the main operation
            error_log("Failed to log payment transaction: " . $e->getMessage());
        }
    }

    /**
     * Get all available gateways
     *
     * @return array Gateways
     */
    public function getAvailableGateways(): array {
        return $this->gateways;
    }

    /**
     * Get order with payment details
     *
     * @param int $orderId Order ID
     * @return array|null Order data
     */
    public function getOrder(int $orderId): ?array {
        $stmt = $this->pdo->prepare("
            SELECT o.*, e.name as event_name, e.date as event_date,
                   pr.name as recipient_name, pr.swish_number, pr.swish_name,
                   pr.gateway_type, pr.gateway_enabled
            FROM orders o
            LEFT JOIN events e ON o.event_id = e.id
            LEFT JOIN payment_recipients pr ON e.payment_recipient_id = pr.id
            WHERE o.id = ?
        ");
        $stmt->execute([$orderId]);
        $order = $stmt->fetch(\PDO::FETCH_ASSOC);

        if (!$order) {
            return null;
        }

        // Get order items
        $stmt = $this->pdo->prepare("
            SELECT * FROM order_items WHERE order_id = ?
        ");
        $stmt->execute([$orderId]);
        $order['items'] = $stmt->fetchAll(\PDO::FETCH_ASSOC);

        // Get payment transactions
        $stmt = $this->pdo->prepare("
            SELECT * FROM payment_transactions
            WHERE order_id = ?
            ORDER BY created_at DESC
        ");
        $stmt->execute([$orderId]);
        $order['transactions'] = $stmt->fetchAll(\PDO::FETCH_ASSOC);

        return $order;
    }

    /**
     * Handle webhook callback
     *
     * @param string $gatewayCode Gateway code
     * @param array $data Webhook data
     * @return array Processing result
     */
    public function handleWebhook(string $gatewayCode, array $data): array {
        // This is typically handled by the webhook endpoints directly
        // This method is for programmatic webhook simulation/testing
        return ['success' => true, 'message' => 'Webhook processing delegated to gateway-specific handler'];
    }
}
