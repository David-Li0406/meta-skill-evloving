<?php
/**
 * API: User Preferences
 * Spara och hämta användarpreferenser (tema, etc.)
 */

session_start();
require_once __DIR__ . '/../../includes/db.php';

header('Content-Type: application/json');

// Kräv inloggning
if (!isset($_SESSION['rider_id'])) {
    http_response_code(401);
    echo json_encode(['error' => 'Not logged in']);
    exit;
}

$userId = $_SESSION['rider_id'];

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    // Spara preferenser
    $input = json_decode(file_get_contents('php://input'), true);

    if (isset($input['theme'])) {
        $theme = in_array($input['theme'], ['light', 'dark', 'auto']) ? $input['theme'] : 'auto';

        try {
            // Spara i databasen
            $stmt = $pdo->prepare("
                UPDATE riders SET theme_preference = ? WHERE id = ?
            ");
            $stmt->execute([$theme, $userId]);

            echo json_encode(['success' => true, 'theme' => $theme]);
        } catch (PDOException $e) {
            http_response_code(500);
            echo json_encode(['error' => 'Database error']);
        }
    } else {
        http_response_code(400);
        echo json_encode(['error' => 'Missing theme']);
    }
}
elseif ($_SERVER['REQUEST_METHOD'] === 'GET') {
    // Hämta preferenser
    try {
        $stmt = $pdo->prepare("SELECT theme_preference FROM riders WHERE id = ?");
        $stmt->execute([$userId]);
        $theme = $stmt->fetchColumn();

        // Default till 'auto' om ingen preferens finns
        if (!$theme) {
            $theme = 'auto';
        }

        echo json_encode(['theme' => $theme]);
    } catch (PDOException $e) {
        http_response_code(500);
        echo json_encode(['error' => 'Database error']);
    }
}
else {
    http_response_code(405);
    echo json_encode(['error' => 'Method not allowed']);
}
