<?php
/**
 * SMTP Test - Temporary debug page
 * DELETE THIS FILE AFTER TESTING
 */
require_once __DIR__ . '/../config.php';
require_once __DIR__ . '/../includes/mail.php';

// Only allow admin access
if (!isset($_SESSION['admin_logged_in']) || !$_SESSION['admin_logged_in']) {
    die('Admin access required');
}

echo "<h1>SMTP Test</h1>";
echo "<pre>";

// Show current settings
echo "=== Current Mail Settings ===\n";
echo "MAIL_DRIVER: " . env('MAIL_DRIVER', 'NOT SET') . "\n";
echo "MAIL_HOST: " . env('MAIL_HOST', 'NOT SET') . "\n";
echo "MAIL_PORT: " . env('MAIL_PORT', 'NOT SET') . "\n";
echo "MAIL_ENCRYPTION: " . env('MAIL_ENCRYPTION', 'NOT SET') . "\n";
echo "MAIL_USERNAME: " . env('MAIL_USERNAME', 'NOT SET') . "\n";
echo "MAIL_PASSWORD: " . (env('MAIL_PASSWORD') ? '***SET***' : 'NOT SET') . "\n";
echo "MAIL_FROM_ADDRESS: " . env('MAIL_FROM_ADDRESS', 'NOT SET') . "\n";
echo "MAIL_FROM_NAME: " . env('MAIL_FROM_NAME', 'NOT SET') . "\n";
echo "\n";

// Test multiple SMTP hosts
echo "=== Testing SMTP Connections ===\n";

$hosts = [
    ['host' => 'mail.hostinger.com', 'port' => 465, 'enc' => 'ssl'],
    ['host' => 'smtp.hostinger.com', 'port' => 465, 'enc' => 'ssl'],
    ['host' => 'smtp.hostinger.com', 'port' => 587, 'enc' => 'tls'],
    ['host' => 'localhost', 'port' => 25, 'enc' => ''],
];

foreach ($hosts as $config) {
    $host = $config['host'];
    $port = $config['port'];
    $encryption = $config['enc'];

    $protocol = ($encryption === 'ssl') ? 'ssl://' : '';
    $address = "{$protocol}{$host}:{$port}";
    echo "Testing: {$address} ... ";

    $context = stream_context_create([
        'ssl' => [
            'verify_peer' => false,
            'verify_peer_name' => false,
            'allow_self_signed' => true
        ]
    ]);

    $socket = @stream_socket_client(
        $address,
        $errno,
        $errstr,
        5, // 5 second timeout for testing
        STREAM_CLIENT_CONNECT,
        $context
    );

    if (!$socket) {
        echo "FAILED ({$errstr})\n";
    } else {
        $greeting = fgets($socket, 515);
        echo "OK! Server: " . trim($greeting) . "\n";
        fclose($socket);
    }
}

echo "\n";

// Test PHP mail() function
echo "=== Testing PHP mail() ===\n";
if (isset($_POST['test_php_mail'])) {
    $testEmail = $_POST['test_php_mail'];
    echo "Sending via PHP mail() to: {$testEmail}\n";

    $headers = "From: TheHUB <info@gravityseries.se>\r\n";
    $headers .= "Content-Type: text/html; charset=UTF-8\r\n";

    $result = @mail($testEmail, 'TheHUB Test (PHP mail)', '<p>Test from PHP mail()</p>', $headers);
    echo "Result: " . ($result ? 'SENT (check inbox/spam)' : 'FAILED') . "\n";
}

echo "\n=== Send Test via SMTP ===\n";
if (isset($_POST['test_smtp'])) {
    $testEmail = $_POST['test_smtp'];
    echo "Sending via SMTP to: {$testEmail}\n";

    $result = hub_send_email(
        $testEmail,
        'TheHUB Test Email (SMTP)',
        '<h1>Test</h1><p>This is a test email from TheHUB via SMTP.</p>',
        []
    );

    echo "Result: " . ($result ? 'SUCCESS' : 'FAILED') . "\n";
}

echo "</pre>";
?>

<h3>Test PHP mail() (fallback)</h3>
<form method="POST">
    <input type="email" name="test_php_mail" placeholder="your@email.com" required>
    <button type="submit">Send via PHP mail()</button>
</form>

<h3>Test SMTP</h3>
<form method="POST">
    <input type="email" name="test_smtp" placeholder="your@email.com" required>
    <button type="submit">Send via SMTP</button>
</form>

<p style="color: red;"><strong>DELETE THIS FILE AFTER TESTING!</strong></p>
