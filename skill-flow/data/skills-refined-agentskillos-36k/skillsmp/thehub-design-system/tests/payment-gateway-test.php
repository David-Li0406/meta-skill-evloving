<?php
/**
 * Payment Gateway Test Script
 * Tests all gateway implementations
 *
 * Run with: php tests/payment-gateway-test.php
 */

// CLI only
if (php_sapi_name() !== 'cli') {
    die('This script can only be run from command line');
}

require_once __DIR__ . '/../config.php';
require_once __DIR__ . '/../includes/payment/PaymentManager.php';

use TheHUB\Payment\PaymentManager;

echo "\n";
echo "╔══════════════════════════════════════════════════════════════╗\n";
echo "║         TheHUB Payment Gateway Test Suite                     ║\n";
echo "╚══════════════════════════════════════════════════════════════╝\n\n";

$pdo = $GLOBALS['pdo'];
$passed = 0;
$failed = 0;
$skipped = 0;

// Helper function
function test($name, $condition, $message = '') {
    global $passed, $failed;
    if ($condition) {
        echo "  ✓ {$name}\n";
        $passed++;
        return true;
    } else {
        echo "  ✗ {$name}" . ($message ? " - {$message}" : "") . "\n";
        $failed++;
        return false;
    }
}

function skip($name, $reason) {
    global $skipped;
    echo "  ⊘ {$name} (skipped: {$reason})\n";
    $skipped++;
}

// =============================================================================
// Test 1: Database Tables
// =============================================================================
echo "─── Test 1: Database Tables ───\n";

$requiredTables = [
    'payment_recipients',
    'orders',
    'order_items'
];

$optionalTables = [
    'payment_transactions',
    'gateway_certificates',
    'webhook_logs'
];

foreach ($requiredTables as $table) {
    $exists = $pdo->query("SHOW TABLES LIKE '{$table}'")->rowCount() > 0;
    test("Table '{$table}' exists", $exists);
}

foreach ($optionalTables as $table) {
    $exists = $pdo->query("SHOW TABLES LIKE '{$table}'")->rowCount() > 0;
    if ($exists) {
        test("Table '{$table}' exists (optional)", true);
    } else {
        skip("Table '{$table}' (optional)", "Run migration 099");
    }
}

echo "\n";

// =============================================================================
// Test 2: PaymentManager Initialization
// =============================================================================
echo "─── Test 2: PaymentManager ───\n";

try {
    $manager = new PaymentManager($pdo);
    test("PaymentManager created", true);
} catch (Exception $e) {
    test("PaymentManager created", false, $e->getMessage());
    exit(1);
}

// =============================================================================
// Test 3: Gateway Registration
// =============================================================================
echo "─── Test 3: Gateway Registration ───\n";

$gateways = $manager->getAvailableGateways();
test("Gateways registered", count($gateways) > 0, "Found " . count($gateways) . " gateways");

$expectedGateways = ['manual', 'swish_handel', 'stripe'];
foreach ($expectedGateways as $code) {
    $gateway = $manager->getGatewayByCode($code);
    test("Gateway '{$code}' registered", $gateway !== null);
    if ($gateway) {
        test("Gateway '{$code}' has name", !empty($gateway->getName()));
        test("Gateway '{$code}' has code", $gateway->getCode() === $code);
    }
}

echo "\n";

// =============================================================================
// Test 4: Gateway Functionality
// =============================================================================
echo "─── Test 4: Gateway Interface ───\n";

foreach ($gateways as $code => $gateway) {
    echo "  Testing {$code}:\n";

    // Check interface methods exist
    $methods = ['initiatePayment', 'checkStatus', 'refund', 'cancel', 'getName', 'getCode', 'isAvailable'];
    foreach ($methods as $method) {
        $hasMethod = method_exists($gateway, $method);
        if (!$hasMethod) {
            test("    {$method}() exists", false);
        }
    }

    // Test with mock data (no actual API calls)
    $mockOrder = [
        'id' => 999999,
        'order_number' => 'ORD-TEST-' . time(),
        'total_amount' => 100.00,
        'payment_recipient_id' => 1,
        'customer_email' => 'test@example.com',
        'event_name' => 'Test Event'
    ];

    // isAvailable check (should return bool)
    $isAvailable = $gateway->isAvailable(1);
    test("    isAvailable() returns bool", is_bool($isAvailable));
}

echo "\n";

// =============================================================================
// Test 5: Manual Gateway (No dependencies)
// =============================================================================
echo "─── Test 5: Manual Gateway ───\n";

$manualGateway = $manager->getGatewayByCode('manual');

// Test with a mock payment recipient
$stmt = $pdo->query("SELECT id FROM payment_recipients WHERE active = 1 AND swish_number IS NOT NULL LIMIT 1");
$recipient = $stmt->fetch(PDO::FETCH_ASSOC);

if ($recipient) {
    $mockOrder = [
        'id' => 999999,
        'order_number' => 'ORD-TEST-' . time(),
        'total_amount' => 199.00,
        'payment_recipient_id' => $recipient['id'],
        'customer_email' => 'test@example.com'
    ];

    $result = $manualGateway->initiatePayment($mockOrder);

    test("Manual gateway initiatePayment()", isset($result['success']));
    test("Manual gateway returns transaction_id", isset($result['transaction_id']));
    test("Manual gateway returns swish_url", isset($result['swish_url']));
    test("Manual gateway returns swish_qr", isset($result['swish_qr']));

    if ($result['success'] && $result['transaction_id']) {
        $status = $manualGateway->checkStatus($result['transaction_id']);
        test("Manual gateway checkStatus()", isset($status['success']));
        test("Manual gateway requires_manual_confirmation", $status['requires_manual_confirmation'] ?? false);
    }
} else {
    skip("Manual gateway tests", "No active payment recipients with swish_number");
}

echo "\n";

// =============================================================================
// Test 6: Swish Handel Gateway (Structure only)
// =============================================================================
echo "─── Test 6: Swish Handel Gateway ───\n";

$swishGateway = $manager->getGatewayByCode('swish_handel');

test("SwishGateway exists", $swishGateway !== null);
test("SwishGateway code is 'swish_handel'", $swishGateway->getCode() === 'swish_handel');
test("SwishGateway name is set", !empty($swishGateway->getName()));

// Check if SwishClient is loadable
try {
    require_once __DIR__ . '/../includes/payment/SwishClient.php';
    test("SwishClient class loadable", class_exists('TheHUB\Payment\SwishClient'));
} catch (Exception $e) {
    test("SwishClient class loadable", false, $e->getMessage());
}

echo "\n";

// =============================================================================
// Test 7: Stripe Gateway (Structure only)
// =============================================================================
echo "─── Test 7: Stripe Gateway ───\n";

$stripeGateway = $manager->getGatewayByCode('stripe');

test("StripeGateway exists", $stripeGateway !== null);
test("StripeGateway code is 'stripe'", $stripeGateway->getCode() === 'stripe');
test("StripeGateway name is set", !empty($stripeGateway->getName()));

// Check if StripeClient is loadable
try {
    require_once __DIR__ . '/../includes/payment/StripeClient.php';
    test("StripeClient class loadable", class_exists('TheHUB\Payment\StripeClient'));
} catch (Exception $e) {
    test("StripeClient class loadable", false, $e->getMessage());
}

// Check if Stripe API key is configured
$stripeKey = getenv('STRIPE_SECRET_KEY');
if (!$stripeKey && function_exists('env')) {
    $stripeKey = env('STRIPE_SECRET_KEY');
}
if ($stripeKey) {
    test("Stripe API key configured", true);
} else {
    skip("Stripe API key", "Not configured in environment");
}

echo "\n";

// =============================================================================
// Test 8: Webhook Files
// =============================================================================
echo "─── Test 8: Webhook Endpoints ───\n";

$webhookFiles = [
    '/api/webhooks/swish-callback.php',
    '/api/webhooks/stripe-webhook.php'
];

foreach ($webhookFiles as $file) {
    $path = __DIR__ . '/..' . $file;
    test("Webhook file exists: {$file}", file_exists($path));
}

echo "\n";

// =============================================================================
// Test 9: Admin Pages
// =============================================================================
echo "─── Test 9: Admin Pages ───\n";

$adminFiles = [
    '/admin/gateway-settings.php',
    '/admin/certificates.php',
    '/admin/payment-recipients.php'
];

foreach ($adminFiles as $file) {
    $path = __DIR__ . '/..' . $file;
    test("Admin file exists: {$file}", file_exists($path));
}

echo "\n";

// =============================================================================
// Test Summary
// =============================================================================
echo "══════════════════════════════════════════════════════════════\n";
echo "                        Test Summary                           \n";
echo "══════════════════════════════════════════════════════════════\n";
echo "  Passed:  {$passed}\n";
echo "  Failed:  {$failed}\n";
echo "  Skipped: {$skipped}\n";
echo "══════════════════════════════════════════════════════════════\n";

if ($failed > 0) {
    echo "\n⚠ Some tests failed. Check the output above.\n";
    exit(1);
} else {
    echo "\n✓ All tests passed!\n";
    exit(0);
}
