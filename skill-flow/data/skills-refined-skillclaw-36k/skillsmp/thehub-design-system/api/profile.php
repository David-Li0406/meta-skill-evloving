<?php
/**
 * TheHUB V1.0 - Profile API
 *
 * Handles profile management:
 * - Link/unlink children
 * - Update profile
 */

require_once dirname(__DIR__) . '/config.php';

header('Content-Type: application/json');
header('Cache-Control: no-store');

$pdo = hub_db();
$action = $_GET['action'] ?? '';

// Require login for all actions
if (!hub_is_logged_in()) {
    http_response_code(401);
    echo json_encode(['success' => false, 'error' => 'Du måste vara inloggad']);
    exit;
}

$currentUser = hub_current_user();

try {
    switch ($action) {
        case 'link_child':
            $childId = intval($_GET['child_id'] ?? 0);

            if (!$childId) {
                throw new Exception('child_id krävs');
            }

            // Check child exists and is different from current user
            $stmt = $pdo->prepare("SELECT id, first_name, birth_year FROM riders WHERE id = ?");
            $stmt->execute([$childId]);
            $child = $stmt->fetch(PDO::FETCH_ASSOC);

            if (!$child) {
                throw new Exception('Åkare hittades inte');
            }

            if ($childId === $currentUser['id']) {
                throw new Exception('Du kan inte koppla dig själv');
            }

            // Check not already linked
            $checkStmt = $pdo->prepare("
                SELECT id FROM rider_parents
                WHERE parent_rider_id = ? AND child_rider_id = ?
            ");
            $checkStmt->execute([$currentUser['id'], $childId]);
            if ($checkStmt->fetch()) {
                throw new Exception('Redan kopplad');
            }

            // Create link
            $insertStmt = $pdo->prepare("
                INSERT INTO rider_parents (parent_rider_id, child_rider_id, relationship, can_register, can_edit_profile)
                VALUES (?, ?, 'parent', 1, 1)
            ");
            $insertStmt->execute([$currentUser['id'], $childId]);

            // Redirect back
            header('Location: /profile/children?msg=added');
            exit;

        case 'unlink_child':
            $childId = intval($_GET['child_id'] ?? 0);

            if (!$childId) {
                throw new Exception('child_id krävs');
            }

            // Remove link
            $stmt = $pdo->prepare("
                DELETE FROM rider_parents
                WHERE parent_rider_id = ? AND child_rider_id = ?
            ");
            $stmt->execute([$currentUser['id'], $childId]);

            // Redirect back
            header('Location: /profile/children?msg=removed');
            exit;

        case 'get_children':
            $children = hub_get_linked_children($currentUser['id']);

            echo json_encode([
                'success' => true,
                'children' => $children
            ]);
            break;

        case 'get_admin_clubs':
            $clubs = hub_get_admin_clubs($currentUser['id']);

            echo json_encode([
                'success' => true,
                'clubs' => $clubs
            ]);
            break;

        default:
            throw new Exception('Ogiltig action');
    }

} catch (Exception $e) {
    http_response_code(400);
    echo json_encode([
        'success' => false,
        'error' => $e->getMessage()
    ]);
}
