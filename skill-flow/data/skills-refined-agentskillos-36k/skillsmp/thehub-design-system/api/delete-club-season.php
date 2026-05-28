<?php
/**
 * API endpoint to delete a rider's club season membership
 * Only accessible by superadmin
 */

require_once __DIR__ . '/../hub-config.php';

header('Content-Type: application/json');

// Check if superadmin
$isSuperAdmin = function_exists('hub_is_super_admin') && hub_is_super_admin();

if (!$isSuperAdmin) {
    http_response_code(403);
    echo json_encode(['success' => false, 'error' => 'Endast superadmin kan radera klubbtillhörighet']);
    exit;
}

// Get JSON input
$input = json_decode(file_get_contents('php://input'), true);

$riderId = intval($input['rider_id'] ?? 0);
$year = intval($input['year'] ?? 0);

if (!$riderId || !$year) {
    http_response_code(400);
    echo json_encode(['success' => false, 'error' => 'Ogiltiga parametrar']);
    exit;
}

try {
    $db = hub_db();

    // Delete the club season entry
    $stmt = $db->prepare("DELETE FROM rider_club_seasons WHERE rider_id = ? AND season_year = ?");
    $stmt->execute([$riderId, $year]);

    $deleted = $stmt->rowCount();

    if ($deleted > 0) {
        echo json_encode(['success' => true, 'message' => "Klubbtillhörighet för $year raderad"]);
    } else {
        echo json_encode(['success' => false, 'error' => 'Ingen klubbtillhörighet hittades']);
    }

} catch (Exception $e) {
    http_response_code(500);
    echo json_encode(['success' => false, 'error' => 'Databasfel: ' . $e->getMessage()]);
}
