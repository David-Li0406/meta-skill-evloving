<?php
/**
 * Stripe Connect Gateway
 * Handles card payments via Stripe with Connected Accounts
 *
 * @package TheHUB\Payment\Gateways
 */

namespace TheHUB\Payment\Gateways;

use TheHUB\Payment\GatewayInterface;
use TheHUB\Payment\StripeClient;

class StripeGateway implements GatewayInterface {
    private $pdo;
    private $client;

    public function __construct($pdo) {
        $this->pdo = $pdo;

        // Get Stripe API key from environment or config
        $apiKey = $this->getStripeKey();
        if ($apiKey) {
            $this->client = new StripeClient($apiKey);
        }
    }

    public function getName(): string {
        return 'Stripe (Kort / Apple Pay / Google Pay)';
    }

    public function getCode(): string {
        return 'stripe';
    }

    /**
     * Get Stripe API key from environment
     */
    private function getStripeKey(): ?string {
        // Try environment variable
        $key = getenv('STRIPE_SECRET_KEY');
        if ($key) {
            return $key;
        }

        // Try env() helper if available
        if (function_exists('env')) {
            $key = env('STRIPE_SECRET_KEY');
            if ($key) {
                return $key;
            }
        }

        return null;
    }

    /**
     * Check if gateway is available for a payment recipient
     */
    public function isAvailable(int $paymentRecipientId): bool {
        if (!$this->client) {
            return false;
        }

        $stmt = $this->pdo->prepare("
            SELECT gateway_type, gateway_enabled, stripe_account_id, stripe_account_status
            FROM payment_recipients
            WHERE id = ? AND active = 1
        ");
        $stmt->execute([$paymentRecipientId]);
        $result = $stmt->fetch(\PDO::FETCH_ASSOC);

        // Stripe is available if enabled and has an active connected account
        // OR if no connected account is needed (direct to platform)
        return $result
            && $result['gateway_type'] === 'stripe'
            && $result['gateway_enabled']
            && ($result['stripe_account_status'] === 'active' || !$result['stripe_account_id']);
    }

    public function initiatePayment(array $orderData): array {
        if (!$this->client) {
            return [
                'success' => false,
                'error' => 'Stripe API key not configured'
            ];
        }

        $paymentRecipientId = $orderData['payment_recipient_id'] ?? null;

        // Get Stripe account ID if using Connected Account
        $stripeAccountId = null;
        if ($paymentRecipientId) {
            $stmt = $this->pdo->prepare("
                SELECT stripe_account_id
                FROM payment_recipients
                WHERE id = ? AND stripe_account_status = 'active'
            ");
            $stmt->execute([$paymentRecipientId]);
            $stripeAccountId = $stmt->fetchColumn() ?: null;
        }

        $paymentData = [
            'amount' => (float)$orderData['total_amount'],
            'currency' => 'SEK',
            'description' => $orderData['event_name'] ?? 'TheHUB Registration',
            'email' => $orderData['customer_email'] ?? null,
            'metadata' => [
                'order_id' => $orderData['id'] ?? null,
                'order_number' => $orderData['order_number'] ?? null,
                'event_id' => $orderData['event_id'] ?? null,
                'payment_recipient_id' => $paymentRecipientId
            ]
        ];

        // Add Connected Account if configured
        if ($stripeAccountId) {
            $paymentData['stripe_account_id'] = $stripeAccountId;
            $paymentData['platform_fee_percent'] = 2; // 2% platform fee
        }

        $result = $this->client->createPaymentIntent($paymentData);

        return [
            'success' => $result['success'],
            'transaction_id' => $result['payment_intent_id'] ?? null,
            'client_secret' => $result['client_secret'] ?? null,
            'status' => $result['status'] ?? 'pending',
            'redirect_url' => null, // Frontend will handle with Stripe.js
            'metadata' => [
                'stripe_status' => $result['status'] ?? null,
                'connected_account' => $stripeAccountId
            ],
            'error' => $result['error'] ?? null
        ];
    }

    public function checkStatus(string $transactionId): array {
        if (!$this->client) {
            return ['success' => false, 'error' => 'Stripe not configured'];
        }

        $result = $this->client->getPaymentIntent($transactionId);

        return [
            'success' => $result['success'],
            'status' => $result['status'] ?? 'unknown',
            'paid' => $result['paid'] ?? false,
            'amount' => $result['amount'] ?? 0,
            'payment_reference' => $transactionId,
            'error' => $result['error'] ?? null
        ];
    }

    public function refund(string $transactionId, float $amount): array {
        if (!$this->client) {
            return ['success' => false, 'error' => 'Stripe not configured'];
        }

        return $this->client->createRefund($transactionId, $amount);
    }

    public function cancel(string $transactionId): array {
        if (!$this->client) {
            return ['success' => false, 'error' => 'Stripe not configured'];
        }

        return $this->client->cancelPaymentIntent($transactionId);
    }

    /**
     * Get Stripe client for direct API access
     */
    public function getClient(): ?StripeClient {
        return $this->client;
    }

    /**
     * Create Connected Account for payment recipient
     */
    public function createConnectedAccount(array $data): array {
        if (!$this->client) {
            return ['success' => false, 'error' => 'Stripe not configured'];
        }

        return $this->client->createConnectedAccount($data);
    }

    /**
     * Create Account Link for onboarding
     */
    public function createAccountLink(string $accountId, string $returnUrl, string $refreshUrl): array {
        if (!$this->client) {
            return ['success' => false, 'error' => 'Stripe not configured'];
        }

        return $this->client->createAccountLink($accountId, $returnUrl, $refreshUrl);
    }

    /**
     * Get Connected Account details
     */
    public function getAccount(string $accountId): array {
        if (!$this->client) {
            return ['success' => false, 'error' => 'Stripe not configured'];
        }

        return $this->client->getAccount($accountId);
    }

    /**
     * Verify webhook signature
     */
    public function verifyWebhook(string $payload, string $sigHeader, string $secret): array {
        if (!$this->client) {
            return ['valid' => false, 'error' => 'Stripe not configured'];
        }

        return $this->client->verifyWebhookSignature($payload, $sigHeader, $secret);
    }
}
