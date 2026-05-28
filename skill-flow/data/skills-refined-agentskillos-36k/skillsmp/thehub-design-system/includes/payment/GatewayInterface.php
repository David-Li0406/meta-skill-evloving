<?php
/**
 * Payment Gateway Interface
 * All payment gateways must implement this interface
 *
 * @package TheHUB\Payment
 */

namespace TheHUB\Payment;

interface GatewayInterface {
    /**
     * Initialize payment
     *
     * @param array $orderData Order information including:
     *   - id: Order ID
     *   - order_number: Order number (e.g., ORD-2026-000001)
     *   - total_amount: Amount to charge
     *   - payment_recipient_id: Payment recipient ID
     *   - payer_phone: Payer's phone number (for Swish)
     *   - customer_email: Customer email
     *   - event_name: Event name for description
     * @return array Result array with:
     *   - success: bool
     *   - transaction_id: string Gateway transaction ID
     *   - redirect_url: string|null URL to redirect user
     *   - qr_code_data: string|null QR code data for mobile payments
     *   - client_secret: string|null For Stripe frontend integration
     *   - metadata: array Additional gateway-specific data
     *   - error: string|null Error message if failed
     */
    public function initiatePayment(array $orderData): array;

    /**
     * Check payment status
     *
     * @param string $transactionId Gateway transaction ID
     * @return array Result array with:
     *   - success: bool
     *   - status: string (pending, paid, failed, cancelled)
     *   - paid: bool True if payment confirmed
     *   - payment_reference: string|null External reference
     *   - error: string|null Error message if failed
     */
    public function checkStatus(string $transactionId): array;

    /**
     * Process refund
     *
     * @param string $transactionId Original transaction ID
     * @param float $amount Amount to refund (null for full refund)
     * @return array Result array with:
     *   - success: bool
     *   - refund_id: string|null Refund transaction ID
     *   - status: string Refund status
     *   - error: string|null Error message if failed
     */
    public function refund(string $transactionId, float $amount): array;

    /**
     * Cancel payment
     *
     * @param string $transactionId Transaction to cancel
     * @return array Result array with:
     *   - success: bool
     *   - error: string|null Error message if failed
     */
    public function cancel(string $transactionId): array;

    /**
     * Get gateway display name
     *
     * @return string Human-readable gateway name
     */
    public function getName(): string;

    /**
     * Get gateway code (e.g., 'swish_handel', 'stripe', 'manual')
     *
     * @return string Gateway identifier code
     */
    public function getCode(): string;

    /**
     * Check if gateway is available/configured
     *
     * @param int $paymentRecipientId Payment recipient to check
     * @return bool True if gateway can be used
     */
    public function isAvailable(int $paymentRecipientId): bool;
}
