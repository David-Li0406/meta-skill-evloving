<?php
/**
 * Stripe Client - Handles Stripe Connect payments
 *
 * @package TheHUB\Payment
 */

namespace TheHUB\Payment;

class StripeClient {
    private $apiKey;
    private $baseUrl = 'https://api.stripe.com/v1';

    public function __construct(string $apiKey) {
        $this->apiKey = $apiKey;
    }

    /**
     * Create Payment Intent
     *
     * @param array $data Payment data
     * @return array Result
     */
    public function createPaymentIntent(array $data): array {
        $params = [
            'amount' => (int)($data['amount'] * 100), // Convert to cents/ore
            'currency' => strtolower($data['currency'] ?? 'sek'),
            'description' => $data['description'] ?? '',
            'metadata' => $data['metadata'] ?? []
        ];

        // Add receipt email if provided
        if (!empty($data['email'])) {
            $params['receipt_email'] = $data['email'];
        }

        // If using Connected Account (Stripe Connect)
        if (!empty($data['stripe_account_id'])) {
            $params['transfer_data'] = [
                'destination' => $data['stripe_account_id']
            ];

            // Platform fee (e.g., 2%)
            if (!empty($data['platform_fee_percent'])) {
                $feeAmount = (int)($params['amount'] * $data['platform_fee_percent'] / 100);
                $params['application_fee_amount'] = $feeAmount;
            }
        }

        $response = $this->request('POST', '/payment_intents', $params);

        return [
            'success' => !isset($response['error']),
            'payment_intent_id' => $response['id'] ?? null,
            'client_secret' => $response['client_secret'] ?? null,
            'status' => $response['status'] ?? null,
            'error' => $response['error']['message'] ?? null
        ];
    }

    /**
     * Get Payment Intent status
     *
     * @param string $paymentIntentId Payment Intent ID
     * @return array Status result
     */
    public function getPaymentIntent(string $paymentIntentId): array {
        $response = $this->request('GET', "/payment_intents/{$paymentIntentId}");

        return [
            'success' => !isset($response['error']),
            'id' => $response['id'] ?? null,
            'status' => $response['status'] ?? null,
            'paid' => ($response['status'] ?? '') === 'succeeded',
            'amount' => isset($response['amount']) ? $response['amount'] / 100 : 0,
            'currency' => $response['currency'] ?? 'sek',
            'payment_method' => $response['payment_method'] ?? null,
            'error' => $response['error']['message'] ?? null
        ];
    }

    /**
     * Create refund
     *
     * @param string $paymentIntentId Payment Intent ID
     * @param float|null $amount Amount to refund (null for full refund)
     * @return array Refund result
     */
    public function createRefund(string $paymentIntentId, ?float $amount = null): array {
        $params = [
            'payment_intent' => $paymentIntentId
        ];

        if ($amount !== null) {
            $params['amount'] = (int)($amount * 100);
        }

        $response = $this->request('POST', '/refunds', $params);

        return [
            'success' => !isset($response['error']),
            'refund_id' => $response['id'] ?? null,
            'status' => $response['status'] ?? null,
            'amount' => isset($response['amount']) ? $response['amount'] / 100 : 0,
            'error' => $response['error']['message'] ?? null
        ];
    }

    /**
     * Cancel Payment Intent
     *
     * @param string $paymentIntentId Payment Intent ID
     * @return array Cancel result
     */
    public function cancelPaymentIntent(string $paymentIntentId): array {
        $response = $this->request('POST', "/payment_intents/{$paymentIntentId}/cancel");

        return [
            'success' => !isset($response['error']),
            'status' => $response['status'] ?? null,
            'error' => $response['error']['message'] ?? null
        ];
    }

    /**
     * Create Connected Account (Express)
     *
     * @param array $data Account data
     * @return array Result
     */
    public function createConnectedAccount(array $data): array {
        $params = [
            'type' => 'express',
            'country' => $data['country'] ?? 'SE',
            'email' => $data['email'] ?? null,
            'capabilities' => [
                'card_payments' => ['requested' => true],
                'transfers' => ['requested' => true]
            ],
            'business_type' => $data['business_type'] ?? 'individual',
            'metadata' => $data['metadata'] ?? []
        ];

        $response = $this->request('POST', '/accounts', $params);

        return [
            'success' => !isset($response['error']),
            'account_id' => $response['id'] ?? null,
            'error' => $response['error']['message'] ?? null
        ];
    }

    /**
     * Create Account Link for onboarding
     *
     * @param string $accountId Stripe Account ID
     * @param string $returnUrl Return URL after onboarding
     * @param string $refreshUrl Refresh URL if link expires
     * @return array Result with onboarding URL
     */
    public function createAccountLink(string $accountId, string $returnUrl, string $refreshUrl): array {
        $params = [
            'account' => $accountId,
            'return_url' => $returnUrl,
            'refresh_url' => $refreshUrl,
            'type' => 'account_onboarding'
        ];

        $response = $this->request('POST', '/account_links', $params);

        return [
            'success' => !isset($response['error']),
            'url' => $response['url'] ?? null,
            'expires_at' => $response['expires_at'] ?? null,
            'error' => $response['error']['message'] ?? null
        ];
    }

    /**
     * Get Connected Account details
     *
     * @param string $accountId Stripe Account ID
     * @return array Account details
     */
    public function getAccount(string $accountId): array {
        $response = $this->request('GET', "/accounts/{$accountId}");

        return [
            'success' => !isset($response['error']),
            'id' => $response['id'] ?? null,
            'email' => $response['email'] ?? null,
            'charges_enabled' => $response['charges_enabled'] ?? false,
            'payouts_enabled' => $response['payouts_enabled'] ?? false,
            'details_submitted' => $response['details_submitted'] ?? false,
            'error' => $response['error']['message'] ?? null
        ];
    }

    /**
     * Verify webhook signature
     *
     * @param string $payload Raw request body
     * @param string $sigHeader Stripe-Signature header
     * @param string $secret Webhook secret
     * @return array Verification result
     */
    public function verifyWebhookSignature(string $payload, string $sigHeader, string $secret): array {
        $elements = [];
        foreach (explode(',', $sigHeader) as $element) {
            $parts = explode('=', $element, 2);
            if (count($parts) === 2) {
                $elements[$parts[0]] = $parts[1];
            }
        }

        if (!isset($elements['t']) || !isset($elements['v1'])) {
            return ['valid' => false, 'error' => 'Invalid signature header format'];
        }

        $timestamp = $elements['t'];
        $signature = $elements['v1'];

        // Check timestamp tolerance (5 minutes)
        if (abs(time() - $timestamp) > 300) {
            return ['valid' => false, 'error' => 'Timestamp outside tolerance'];
        }

        // Compute expected signature
        $signedPayload = $timestamp . '.' . $payload;
        $expectedSignature = hash_hmac('sha256', $signedPayload, $secret);

        if (!hash_equals($expectedSignature, $signature)) {
            return ['valid' => false, 'error' => 'Signature mismatch'];
        }

        return ['valid' => true, 'event' => json_decode($payload, true)];
    }

    /**
     * Make API request to Stripe
     *
     * @param string $method HTTP method
     * @param string $endpoint API endpoint
     * @param array|null $data Request data
     * @return array Response
     */
    public function request(string $method, string $endpoint, ?array $data = null): array {
        $url = $this->baseUrl . $endpoint;

        $ch = curl_init($url);

        $headers = [
            'Authorization: Bearer ' . $this->apiKey,
            'Content-Type: application/x-www-form-urlencoded',
            'Stripe-Version: 2023-10-16'
        ];

        curl_setopt_array($ch, [
            CURLOPT_CUSTOMREQUEST => $method,
            CURLOPT_RETURNTRANSFER => true,
            CURLOPT_HTTPHEADER => $headers,
            CURLOPT_TIMEOUT => 30
        ]);

        if ($data !== null && $method !== 'GET') {
            curl_setopt($ch, CURLOPT_POSTFIELDS, $this->buildQuery($data));
        }

        $response = curl_exec($ch);
        $httpCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);

        if (curl_errno($ch)) {
            $error = curl_error($ch);
            curl_close($ch);
            return ['error' => ['message' => 'CURL Error: ' . $error]];
        }

        curl_close($ch);

        return json_decode($response, true) ?? [];
    }

    /**
     * Build query string from nested array (Stripe format)
     *
     * @param array $data Data to encode
     * @param string $prefix Prefix for nested keys
     * @return string Query string
     */
    private function buildQuery(array $data, string $prefix = ''): string {
        $result = [];

        foreach ($data as $key => $value) {
            $fullKey = $prefix ? $prefix . '[' . $key . ']' : $key;

            if (is_array($value)) {
                $result[] = $this->buildQuery($value, $fullKey);
            } else {
                $result[] = urlencode($fullKey) . '=' . urlencode($value);
            }
        }

        return implode('&', $result);
    }
}
