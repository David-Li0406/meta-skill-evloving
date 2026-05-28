<?php
require_once __DIR__ . '/../config.php';
require_admin();

// Only accept POST requests
if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    http_response_code(405);
    die('Method not allowed');
}

// Validate CSRF token
checkCsrf();

$db = getDB();

// Get rider ID
$id = isset($_POST['id']) && is_numeric($_POST['id']) ? intval($_POST['id']) : null;

if (!$id) {
    http_response_code(400);
    echo json_encode(['success' => false, 'message' => 'Ogiltigt ID']);
    exit;
}

try {
    // Check if rider exists
    $rider = $db->getRow("SELECT id, firstname, lastname FROM riders WHERE id = ?", [$id]);

    if (!$rider) {
        http_response_code(404);
        echo json_encode(['success' => false, 'message' => 'Deltagare hittades inte']);
        exit;
    }

    // Delete rider
    $db->delete('riders', 'id = ?', [$id]);

    // Redirect back to riders list
    header('Location: /admin/riders.php?message=' . urlencode('Deltagare borttagen'));
    exit;

} catch (Exception $e) {
    http_response_code(500);
    echo json_encode(['success' => false, 'message' => 'Ett fel uppstod: ' . $e->getMessage()]);
    exit;
}
