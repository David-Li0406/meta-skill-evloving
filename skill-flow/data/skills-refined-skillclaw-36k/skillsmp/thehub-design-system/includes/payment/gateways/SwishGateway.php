<?php
/**
 * Swish Handel Gateway
 * Handles automated Swish payments via Swish Commerce API
 *
 * @package TheHUB\Payment\Gateways
 */

namespace TheHUB\Payment\Gateways;

use TheHUB\Payment\GatewayInterface;
use TheHUB\Payment\SwishClient;

class SwishGateway implements GatewayInterface {
    private $pdo;
    private $clients = [];

    public function __construct($pdo) {
        $this->pdo = $pdo;
    }

    public function getName(): string {
        return 'Swish Handel';
    }

    public function getCode(): string {
        return 'swish_handel';
    }

    /**
     * Check if gateway is available for a payment recipient
     */
    public function isAvailable(int $paymentRecipientId): bool {
        $stmt = $this->pdo->prepare("
            SELECT pr.gateway_type, pr.gateway_enabled, gc.id as cert_id
            FROM payment_recipients pr
            LEFT JOIN gateway_certificates gc ON pr.id = gc.payment_recipient_id
                AND gc.active = 1 AND gc.cert_type IN ('swish_test', 'swish_production')
            WHERE pr.id = ? AND pr.active = 1
        ");
        $stmt->execute([$paymentRecipientId]);
        $result = $stmt->fetch(\PDO::FETCH_ASSOC);

        return $result
            && $result['gateway_type'] === 'swish_handel'
            && $result['gateway_enabled']
            && $result['cert_id'];
    }

    /**
     * Get or create Swish client for payment recipient
     */
    private function getClient(int $paymentRecipientId): ?SwishClient {
        if (isset($this->clients[$paymentRecipientId])) {
            return $this->clients[$paymentRecipientId];
        }

        $stmt = $this->pdo->prepare("
            SELECT pr.gateway_config, gc.cert_data, gc.cert_password, gc.cert_type
            FROM payment_recipients pr
            LEFT JOIN gateway_certificates gc ON pr.id = gc.payment_recipient_id
                AND gc.active = 1
            WHERE pr.id = ?
            ORDER BY FIELD(gc.cert_type, 'swish_production', 'swish_test')
            LIMIT 1
        ");
        $stmt->execute([$paymentRecipientId]);
        $config = $stmt->fetch(\PDO::FETCH_ASSOC);

        if (!$config || !$config['cert_data']) {
            return null;
        }

        $gatewayConfig = json_decode($config['gateway_config'] ?? '{}', true);

        // Write certificate to temp file
        $certPath = sys_get_temp_dir() . '/swish_cert_' . $paymentRecipientId . '_' . md5($config['cert_data']) . '.p12';
        if (!file_exists($certPath)) {
            file_put_contents($certPath, $config['cert_data']);
            chmod($certPath, 0600);
        }

        // Determine environment from cert type or config
        $environment = 'production';
        if ($config['cert_type'] === 'swish_test') {
            $environment = 'test';
        } elseif (isset($gatewayConfig['environment'])) {
            $environment = $gatewayConfig['environment'];
        }

        $client = new SwishClient([
            'environment' => $environment,
            'cert_path' => $certPath,
            'cert_password' => $config['cert_password'] ?? '',
            'payee_alias' => $gatewayConfig['payee_alias'] ?? ''
        ]);

        $this->clients[$paymentRecipientId] = $client;
        return $client;
    }

    public function initiatePayment(array $orderData): array {
        $paymentRecipientId = $orderData['payment_recipient_id'] ?? null;

        if (!$paymentRecipientId) {
            return [
                'success' => false,
                'error' => 'Payment recipient not specified'
            ];
        }

        $client = $this->getClient($paymentRecipientId);

        if (!$client) {
            return [
                'success' => false,
                'error' => 'Swish certificate not configured for this payment recipient'
            ];
        }

        $callbackUrl = $client->getCallbackUrl();
        $message = mb_substr($orderData['order_number'] ?? '', 0, 50);

        // Use shorter message if order number is long
        if (strlen($message) > 50) {
            $message = substr($orderData['order_number'], -20);
        }

        $paymentData = [
            'reference' => $orderData['order_number'] ?? $orderData['id'],
            'callback_url' => $callbackUrl,
            'amount' => (float)$orderData['total_amount'],
            'message' => $message
        ];

        // Use E-commerce if phone provided, M-commerce if not
        if (!empty($orderData['payer_phone'])) {
            $paymentData['payer_phone'] = $orderData['payer_phone'];
            $result = $client->createPaymentRequest($paymentData);
        } else {
            $result = $client->createMCommercePayment($paymentData);
        }

        return [
            'success' => $result['success'],
            'transaction_id' => $result['instruction_uuid'] ?? null,
            'qr_code_data' => $result['qr_code_data'] ?? null,
            'status' => 'pending',
            'metadata' => [
                'swish_status' => 'CREATED',
                'location' => $result['location'] ?? null,
                'environment' => $client->getCallbackUrl()
            ],
            'error' => $result['error'] ?? null
        ];
    }

    public function checkStatus(string $transactionId): array {
        // Get payment recipient from transaction
        $stmt = $this->pdo->prepare("
            SELECT e.payment_recipient_id
            FROM orders o
            JOIN events e ON o.event_id = e.id
            WHERE o.gateway_transaction_id = ?
        ");
        $stmt->execute([$transactionId]);
        $recipientId = $stmt->fetchColumn();

        if (!$recipientId) {
            return ['success' => false, 'error' => 'Order not found'];
        }

        $client = $this->getClient($recipientId);

        if (!$client) {
            return ['success' => false, 'error' => 'Swish not configured'];
        }

        return $client->getPaymentStatus($transactionId);
    }

    public function refund(string $transactionId, float $amount): array {
        $stmt = $this->pdo->prepare("
            SELECT e.payment_recipient_id, o.payment_reference
            FROM orders o
            JOIN events e ON o.event_id = e.id
            WHERE o.gateway_transaction_id = ?
        ");
        $stmt->execute([$transactionId]);
        $order = $stmt->fetch(\PDO::FETCH_ASSOC);

        if (!$order) {
            return ['success' => false, 'error' => 'Order not found'];
        }

        if (!$order['payment_reference']) {
            return ['success' => false, 'error' => 'No payment reference available for refund'];
        }

        $client = $this->getClient($order['payment_recipient_id']);

        if (!$client) {
            return ['success' => false, 'error' => 'Swish not configured'];
        }

        return $client->createRefund(
            $order['payment_reference'],
            $amount,
            'Refund'
        );
    }

    public function cancel(string $transactionId): array {
        // Swish doesn't support cancellation after creation
        return [
            'success' => false,
            'error' => 'Swish payments cannot be cancelled, only refunded after payment'
        ];
    }
}
