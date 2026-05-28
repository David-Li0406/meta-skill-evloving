<?php
/**
 * API: Sök åkare
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
$query = trim($input['query'] ?? '');

if (strlen($query) < 2) {
    echo json_encode(['riders' => []]);
    exit;
}

try {
    $riders = searchRiders($query, 15);

    echo json_encode([
        'success' => true,
        'riders' => $riders
    ]);

} catch (Exception $e) {
    http_response_code(500);
    echo json_encode(['error' => 'Sökfel: ' . $e->getMessage()]);
}
