<?php
/**
 * Swish API Client
 * Handles communication with Swish Commerce API (Handel)
 *
 * @package TheHUB\Payment
 */

namespace TheHUB\Payment;

class SwishClient {
    private $baseUrl;
    private $certPath;
    private $certPassword;
    private $payeeAlias; // Swish merchant number
    private $environment; // 'test' or 'production'

    const TEST_URL = 'https://mss.cpc.getswish.net/swish-cpcapi/api/v2';
    const PROD_URL = 'https://cpc.getswish.net/swish-cpcapi/api/v2';

    public function __construct(array $config) {
        $this->environment = $config['environment'] ?? 'test';
        $this->baseUrl = $this->environment === 'production' ? self::PROD_URL : self::TEST_URL;
        $this->certPath = $config['cert_path'] ?? '';
        $this->certPassword = $config['cert_password'] ?? '';
        $this->payeeAlias = $config['payee_alias'] ?? '';
    }

    /**
     * Create payment request (E-commerce flow - requires payer phone)
     *
     * @param array $data Payment data
     * @return array Result
     */
    public function createPaymentRequest(array $data): array {
        $instructionUUID = $this->generateUUID();

        $payload = [
            'payeePaymentReference' => $data['reference'],
            'callbackUrl' => $data['callback_url'],
            'payerAlias' => $this->formatPhoneNumber($data['payer_phone']),
            'payeeAlias' => $this->payeeAlias,
            'amount' => number_format($data['amount'], 2, '.', ''),
            'currency' => 'SEK',
            'message' => mb_substr($data['message'] ?? '', 0, 50)
        ];

        $response = $this->request('PUT', "/paymentrequests/{$instructionUUID}", $payload);

        return [
            'success' => $response['status'] === 201,
            'instruction_uuid' => $instructionUUID,
            'status' => $response['status'],
            'location' => $response['headers']['Location'] ?? null,
            'error' => $response['error'] ?? null
        ];
    }

    /**
     * Create M-commerce payment (QR code flow - no phone required)
     *
     * @param array $data Payment data
     * @return array Result with QR code data
     */
    public function createMCommercePayment(array $data): array {
        $instructionUUID = $this->generateUUID();

        $payload = [
            'payeePaymentReference' => $data['reference'],
            'callbackUrl' => $data['callback_url'],
            'payeeAlias' => $this->payeeAlias,
            'amount' => number_format($data['amount'], 2, '.', ''),
            'currency' => 'SEK',
            'message' => mb_substr($data['message'] ?? '', 0, 50)
        ];

        $response = $this->request('PUT', "/paymentrequests/{$instructionUUID}", $payload);

        // Generate QR code data
        $qrData = $this->generateQRCode($instructionUUID, $data['amount'], $data['message'] ?? '');

        return [
            'success' => $response['status'] === 201,
            'instruction_uuid' => $instructionUUID,
            'qr_code_data' => $qrData,
            'status' => $response['status'],
            'location' => $response['headers']['Location'] ?? null,
            'error' => $response['error'] ?? null
        ];
    }

    /**
     * Check payment status
     *
     * @param string $instructionUUID Payment instruction UUID
     * @return array Status result
     */
    public function getPaymentStatus(string $instructionUUID): array {
        $response = $this->request('GET', "/paymentrequests/{$instructionUUID}");

        if ($response['status'] !== 200) {
            return [
                'success' => false,
                'status' => 'ERROR',
                'error' => $response['error'] ?? 'Unknown error'
            ];
        }

        $data = $response['data'] ?? [];

        return [
            'success' => true,
            'status' => $data['status'] ?? 'PENDING',
            'paid' => ($data['status'] ?? '') === 'PAID',
            'payment_reference' => $data['paymentReference'] ?? null,
            'error_code' => $data['errorCode'] ?? null,
            'error_message' => $data['errorMessage'] ?? null
        ];
    }

    /**
     * Create refund
     *
     * @param string $originalPaymentReference Original payment reference from Swish
     * @param float $amount Amount to refund
     * @param string $message Refund message
     * @return array Refund result
     */
    public function createRefund(string $originalPaymentReference, float $amount, string $message): array {
        $instructionUUID = $this->generateUUID();

        $siteUrl = defined('SITE_URL') ? SITE_URL : 'https://thehub.gravityseries.se';
        $callbackUrl = $siteUrl . '/api/webhooks/swish-callback.php';

        $payload = [
            'originalPaymentReference' => $originalPaymentReference,
            'payerAlias' => $this->payeeAlias, // Merchant becomes payer for refund
            'amount' => number_format($amount, 2, '.', ''),
            'currency' => 'SEK',
            'message' => mb_substr($message, 0, 50),
            'callbackUrl' => $callbackUrl
        ];

        $response = $this->request('PUT', "/refunds/{$instructionUUID}", $payload);

        return [
            'success' => $response['status'] === 201,
            'refund_uuid' => $instructionUUID,
            'status' => $response['status'],
            'error' => $response['error'] ?? null
        ];
    }

    /**
     * Make HTTP request to Swish API
     *
     * @param string $method HTTP method
     * @param string $endpoint API endpoint
     * @param array|null $data Request data
     * @return array Response
     */
    private function request(string $method, string $endpoint, ?array $data = null): array {
        $url = $this->baseUrl . $endpoint;

        $ch = curl_init($url);

        curl_setopt_array($ch, [
            CURLOPT_CUSTOMREQUEST => $method,
            CURLOPT_RETURNTRANSFER => true,
            CURLOPT_HEADER => true,
            CURLOPT_SSLCERT => $this->certPath,
            CURLOPT_SSLCERTPASSWD => $this->certPassword,
            CURLOPT_SSL_VERIFYPEER => true,
            CURLOPT_SSL_VERIFYHOST => 2,
            CURLOPT_TIMEOUT => 30,
            CURLOPT_HTTPHEADER => [
                'Content-Type: application/json',
                'Accept: application/json'
            ]
        ]);

        if ($data !== null) {
            curl_setopt($ch, CURLOPT_POSTFIELDS, json_encode($data));
        }

        $response = curl_exec($ch);
        $httpCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
        $headerSize = curl_getinfo($ch, CURLINFO_HEADER_SIZE);

        if (curl_errno($ch)) {
            $error = curl_error($ch);
            curl_close($ch);
            return [
                'status' => 0,
                'error' => 'CURL Error: ' . $error
            ];
        }

        $headers = $this->parseHeaders(substr($response, 0, $headerSize));
        $body = substr($response, $headerSize);

        curl_close($ch);

        return [
            'status' => $httpCode,
            'headers' => $headers,
            'data' => json_decode($body, true),
            'error' => $httpCode >= 400 ? ($body ?: 'HTTP Error ' . $httpCode) : null
        ];
    }

    /**
     * Parse response headers
     *
     * @param string $headerText Raw header text
     * @return array Parsed headers
     */
    private function parseHeaders(string $headerText): array {
        $headers = [];
        foreach (explode("\r\n", $headerText) as $line) {
            if (strpos($line, ':') !== false) {
                list($key, $value) = explode(':', $line, 2);
                $headers[trim($key)] = trim($value);
            }
        }
        return $headers;
    }

    /**
     * Generate UUID v4
     *
     * @return string UUID string
     */
    private function generateUUID(): string {
        return sprintf(
            '%04x%04x-%04x-%04x-%04x-%04x%04x%04x',
            mt_rand(0, 0xffff), mt_rand(0, 0xffff),
            mt_rand(0, 0xffff),
            mt_rand(0, 0x0fff) | 0x4000,
            mt_rand(0, 0x3fff) | 0x8000,
            mt_rand(0, 0xffff), mt_rand(0, 0xffff), mt_rand(0, 0xffff)
        );
    }

    /**
     * Format phone number for Swish (46XXXXXXXXX)
     *
     * @param string $phone Phone number
     * @return string Formatted phone number
     */
    private function formatPhoneNumber(string $phone): string {
        $clean = preg_replace('/[^0-9]/', '', $phone);
        if (substr($clean, 0, 1) === '0') {
            return '46' . substr($clean, 1);
        }
        if (substr($clean, 0, 2) !== '46') {
            return '46' . $clean;
        }
        return $clean;
    }

    /**
     * Generate QR code data for M-commerce
     *
     * @param string $token Payment token/UUID
     * @param float $amount Amount
     * @param string $message Message
     * @return string QR code content
     */
    private function generateQRCode(string $token, float $amount, string $message): string {
        // Swish M-commerce QR format
        $amountOre = (int)($amount * 100);
        return "C{$this->payeeAlias};{$amountOre};{$message};{$token}";
    }

    /**
     * Get callback URL
     *
     * @return string Callback URL
     */
    public function getCallbackUrl(): string {
        $siteUrl = defined('SITE_URL') ? SITE_URL : 'https://thehub.gravityseries.se';
        return $siteUrl . '/api/webhooks/swish-callback.php';
    }
}
