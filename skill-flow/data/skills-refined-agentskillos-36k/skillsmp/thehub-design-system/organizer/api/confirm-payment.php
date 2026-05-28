<?php
/**
 * API: Bekräfta betalning
 */

require_once __DIR__ . '/../config.php';

header('Content-Type: application/json');

// Kräv inloggning
if (!isLoggedIn() || !hasRole('promotor')) {
    http_response_code(401);
    echo json_encode(['error' => 'Ej inloggad']);
    exit;
}

// Läs JSON-body
$input = json_decode(file_get_contents('php://input'), true);
$registrationId = (int)($input['registration_id'] ?? 0);

if (!$registrationId) {
    http_response_code(400);
    echo json_encode(['error' => 'Ogiltigt registrerings-ID']);
    exit;
}

try {
    global $pdo;

    // Hämta registreringen för att verifiera tillgång
    $stmt = $pdo->prepare("SELECT event_id FROM event_registrations WHERE id = ?");
    $stmt->execute([$registrationId]);
    $reg = $stmt->fetch(PDO::FETCH_ASSOC);

    if (!$reg) {
        http_response_code(404);
        echo json_encode(['error' => 'Registrering hittades inte']);
        exit;
    }

    // Kontrollera eventtillgång
    if (!canAccessEvent($reg['event_id'])) {
        http_response_code(403);
        echo json_encode(['error' => 'Ingen tillgång till detta event']);
        exit;
    }

    // Uppdatera betalningsstatus
    $stmt = $pdo->prepare("
        UPDATE event_registrations
        SET payment_status = 'paid',
            status = 'confirmed',
            confirmed_date = COALESCE(confirmed_date, NOW())
        WHERE id = ?
    ");
    $stmt->execute([$registrationId]);

    echo json_encode(['success' => true]);

} catch (Exception $e) {
    http_response_code(500);
    echo json_encode(['error' => 'Kunde inte uppdatera: ' . $e->getMessage()]);
}
