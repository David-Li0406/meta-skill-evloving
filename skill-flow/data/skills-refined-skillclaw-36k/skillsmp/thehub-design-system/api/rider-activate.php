<?php
/**
 * API Endpoint: Send activation email to rider
 *
 * Sends a password reset email to a rider who has an email but no password set.
 * Open to all users - email verification ensures only the profile owner can activate.
 */

header('Content-Type: application/json');

require_once __DIR__ . '/../config.php';
require_once __DIR__ . '/../hub-config.php';
require_once __DIR__ . '/../includes/mail.php';

// Only POST allowed
if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    http_response_code(405);
    echo json_encode(['success' => false, 'error' => 'Method not allowed']);
    exit;
}

// Get JSON input
$input = json_decode(file_get_contents('php://input'), true);
$riderId = (int)($input['rider_id'] ?? 0);

if (!$riderId) {
    echo json_encode(['success' => false, 'error' => 'Ogiltig profil']);
    exit;
}

// No authentication required - the activation email is sent to the profile's
// registered email address, so only the rightful owner can complete activation

try {
    global $pdo;

    if (!$pdo) {
        echo json_encode(['success' => false, 'error' => 'Databasanslutning misslyckades']);
        exit;
    }

    // Get rider
    $stmt = $pdo->prepare("SELECT id, email, password, firstname, lastname FROM riders WHERE id = ?");
    $stmt->execute([$riderId]);
    $rider = $stmt->fetch(PDO::FETCH_ASSOC);

    if (!$rider) {
        echo json_encode(['success' => false, 'error' => 'Profilen hittades inte']);
        exit;
    }

    if (empty($rider['email'])) {
        echo json_encode(['success' => false, 'error' => 'Profilen saknar e-postadress']);
        exit;
    }

    if (!empty($rider['password'])) {
        echo json_encode(['success' => false, 'error' => 'Kontot är redan aktiverat']);
        exit;
    }

    // Generate password reset token
    $token = bin2hex(random_bytes(32));
    $expires = date('Y-m-d H:i:s', strtotime('+24 hours'));

    $stmt = $pdo->prepare("UPDATE riders SET password_reset_token = ?, password_reset_expires = ? WHERE id = ?");
    $stmt->execute([$token, $expires, $riderId]);

    // Build reset link and send email
    $baseUrl = 'https://thehub.gravityseries.se';
    $resetLink = $baseUrl . '/reset-password?token=' . $token;
    $riderName = trim($rider['firstname'] . ' ' . $rider['lastname']);

    // Log mail configuration for debugging
    error_log("RIDER_ACTIVATE: Mail config - Driver: " . env('MAIL_DRIVER', 'mail') . ", Host: " . env('MAIL_HOST', 'not set') . ", From: " . env('MAIL_FROM_ADDRESS', 'not set'));
    error_log("RIDER_ACTIVATE: Attempting to send to {$rider['email']} for {$riderName}");

    $emailSent = hub_send_password_reset_email($rider['email'], $riderName, $resetLink);

    // Log the action
    error_log("ADMIN ACTIVATE: Super admin sent activation email to rider {$riderId} ({$riderName}) at {$rider['email']}. Email sent: " . ($emailSent ? 'yes' : 'no'));

    if ($emailSent) {
        echo json_encode([
            'success' => true,
            'message' => 'Aktiveringslänk skickad till ' . $rider['email']
        ]);
    } else {
        echo json_encode([
            'success' => false,
            'error' => 'Kunde inte skicka mail. Kontrollera e-postadressen.'
        ]);
    }

} catch (Exception $e) {
    error_log("Rider activate error: " . $e->getMessage());
    echo json_encode(['success' => false, 'error' => 'Ett fel uppstod. Försök igen senare.']);
}
