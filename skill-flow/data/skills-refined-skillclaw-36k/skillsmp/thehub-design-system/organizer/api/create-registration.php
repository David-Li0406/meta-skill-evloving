<?php
/**
 * API: Skapa platsregistrering (DEMO)
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

// Validera
$firstName = trim($input['first_name'] ?? '');
$lastName = trim($input['last_name'] ?? '');

if (!$firstName || !$lastName) {
    http_response_code(400);
    echo json_encode(['error' => 'Saknade obligatoriska fält']);
    exit;
}

// DEMO: Returnera simulerat svar
$demoBibNumber = rand(200, 299);

echo json_encode([
    'success' => true,
    'registration_id' => rand(10000, 99999),
    'bib_number' => $demoBibNumber,
    'demo' => true,
    'message' => 'Demo-registrering skapad (sparas ej i databasen)'
]);
