<?php
/**
 * Manual Gateway - For manual Swish confirmation
 * Generates Swish deep links and QR codes for manual payment
 *
 * @package TheHUB\Payment\Gateways
 */

namespace TheHUB\Payment\Gateways;

use TheHUB\Payment\GatewayInterface;

class ManualGateway implements GatewayInterface {
    private $pdo;

    public function __construct($pdo) {
        $this->pdo = $pdo;
    }

    public function getName(): string {
        return 'Manuell Swish';
    }

    public function getCode(): string {
        return 'manual';
    }

    /**
     * Check if gateway is available for a payment recipient
     */
    public function isAvailable(int $paymentRecipientId): bool {
        $stmt = $this->pdo->prepare("
            SELECT swish_number
            FROM payment_recipients
            WHERE id = ? AND active = 1 AND swish_number IS NOT NULL AND swish_number != ''
        ");
        $stmt->execute([$paymentRecipientId]);
        return (bool)$stmt->fetchColumn();
    }

    public function initiatePayment(array $orderData): array {
        $paymentRecipientId = $orderData['payment_recipient_id'] ?? null;

        $swishNumber = null;
        $swishName = null;

        if ($paymentRecipientId) {
            $stmt = $this->pdo->prepare("
                SELECT swish_number, swish_name
                FROM payment_recipients
                WHERE id = ? AND active = 1
            ");
            $stmt->execute([$paymentRecipientId]);
            $recipient = $stmt->fetch(\PDO::FETCH_ASSOC);

            if ($recipient) {
                $swishNumber = $recipient['swish_number'];
                $swishName = $recipient['swish_name'];
            }
        }

        if (!$swishNumber) {
            return [
                'success' => false,
                'error' => 'No Swish number configured for this payment recipient'
            ];
        }

        // Generate Swish message (short reference)
        $message = $this->generateSwishMessage($orderData['order_number'] ?? '');
        $amount = (float)$orderData['total_amount'];

        // Generate unique transaction ID for tracking
        $transactionId = 'manual_' . uniqid() . '_' . time();

        return [
            'success' => true,
            'transaction_id' => $transactionId,
            'swish_url' => $this->generateSwishUrl($swishNumber, $amount, $message),
            'swish_qr' => $this->generateSwishQR($swishNumber, $amount, $message),
            'swish_number' => $swishNumber,
            'swish_name' => $swishName,
            'swish_message' => $message,
            'status' => 'pending',
            'requires_manual_confirmation' => true,
            'metadata' => [
                'manual_gateway' => true,
                'swish_number' => $swishNumber,
                'message' => $message
            ]
        ];
    }

    public function checkStatus(string $transactionId): array {
        // Manual gateway requires admin confirmation
        // Check database for payment status
        $stmt = $this->pdo->prepare("
            SELECT payment_status
            FROM orders
            WHERE gateway_transaction_id = ?
        ");
        $stmt->execute([$transactionId]);
        $status = $stmt->fetchColumn();

        return [
            'success' => true,
            'status' => $status ?: 'pending',
            'paid' => $status === 'paid',
            'requires_manual_confirmation' => true
        ];
    }

    public function refund(string $transactionId, float $amount): array {
        return [
            'success' => true,
            'message' => 'Manual refund required - contact customer directly via Swish',
            'requires_manual_action' => true
        ];
    }

    public function cancel(string $transactionId): array {
        return [
            'success' => true,
            'message' => 'Order cancelled - inform customer if needed',
            'requires_manual_action' => true
        ];
    }

    /**
     * Generate Swish message from order number
     */
    private function generateSwishMessage(string $orderNumber): string {
        // Remove ORD- prefix and shorten if needed
        $message = preg_replace('/^ORD-/', '', $orderNumber);

        // Swish message limit is 50 chars
        return mb_substr($message, 0, 50);
    }

    /**
     * Generate Swish payment URL (opens Swish app)
     */
    private function generateSwishUrl(string $recipientNumber, float $amount, string $message): string {
        // Clean phone number
        $cleanNumber = preg_replace('/[^0-9]/', '', $recipientNumber);

        // Convert 07... to 467...
        if (substr($cleanNumber, 0, 1) === '0') {
            $cleanNumber = '46' . substr($cleanNumber, 1);
        }

        $params = [
            'sw' => $cleanNumber,
            'amt' => number_format($amount, 0, '', ''),
            'msg' => $message
        ];

        return 'https://app.swish.nu/1/p/sw/?' . http_build_query($params);
    }

    /**
     * Generate Swish QR code URL
     */
    private function generateSwishQR(string $recipientNumber, float $amount, string $message): string {
        // Clean phone number
        $cleanNumber = preg_replace('/[^0-9]/', '', $recipientNumber);
        if (substr($cleanNumber, 0, 1) === '0') {
            $cleanNumber = '46' . substr($cleanNumber, 1);
        }

        // Swish QR payload format
        $amountOre = (int)($amount * 100);
        $message = mb_substr($message, 0, 50);
        $payload = "C{$cleanNumber};{$amountOre};{$message}";

        // Use Google Charts API for QR generation
        $size = 200;
        $qrUrl = 'https://chart.googleapis.com/chart?' . http_build_query([
            'cht' => 'qr',
            'chs' => "{$size}x{$size}",
            'chl' => $payload,
            'choe' => 'UTF-8'
        ]);

        return $qrUrl;
    }

    /**
     * Format Swish number for display
     */
    public function formatSwishNumber(string $number): string {
        $clean = preg_replace('/[^0-9]/', '', $number);

        // Mobile number format: 070-123 45 67
        if (strlen($clean) === 10 && substr($clean, 0, 1) === '0') {
            return substr($clean, 0, 3) . '-' .
                   substr($clean, 3, 3) . ' ' .
                   substr($clean, 6, 2) . ' ' .
                   substr($clean, 8, 2);
        }

        // Company number format: 123-XXX XX XX
        if (strlen($clean) >= 7) {
            return substr($clean, 0, 3) . '-' .
                   substr($clean, 3, 3) . ' ' .
                   substr($clean, 6, 2) . ' ' .
                   substr($clean, 8);
        }

        return $number;
    }
}
