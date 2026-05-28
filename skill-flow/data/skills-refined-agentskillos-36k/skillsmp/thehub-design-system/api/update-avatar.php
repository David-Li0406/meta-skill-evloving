<?php
/**
 * TheHUB V1.0 - Avatar Update API
 *
 * Handles profile picture upload to ImgBB and updates rider record
 *
 * Security:
 * - Requires authentication
 * - Only allows updating own avatar or children's avatars
 * - Validates file type and size server-side
 * - CSRF protection (if enabled)
 */

header('Content-Type: application/json');
header('Cache-Control: no-store');

require_once dirname(__DIR__) . '/config.php';
require_once dirname(__DIR__) . '/hub-config.php';
require_once dirname(__DIR__) . '/includes/auth.php';
require_once dirname(__DIR__) . '/includes/upload-avatar.php';

$response = ['success' => false, 'error' => null, 'avatar_url' => null];

try {
    // Check if user is logged in (rider or admin)
    $isRiderLoggedIn = function_exists('hub_is_logged_in') && hub_is_logged_in();
    $isAdminLoggedIn = function_exists('isLoggedIn') && isLoggedIn();

    if (!$isRiderLoggedIn && !$isAdminLoggedIn) {
        http_response_code(401);
        $response['error'] = 'Du måste vara inloggad för att ändra profilbild.';
        echo json_encode($response);
        exit;
    }

    // Get current user info
    $currentUser = null;
    if ($isRiderLoggedIn && function_exists('hub_current_user')) {
        $currentUser = hub_current_user();
    }

    // Only accept POST requests
    if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
        http_response_code(405);
        $response['error'] = 'Endast POST-förfrågningar tillåtna.';
        echo json_encode($response);
        exit;
    }

    // Get rider ID to update
    $riderId = intval($_POST['rider_id'] ?? ($currentUser['id'] ?? 0));

    if ($riderId <= 0) {
        http_response_code(400);
        $response['error'] = 'Ingen åkare angiven.';
        echo json_encode($response);
        exit;
    }

    // Security: Check if user can edit this profile
    // Admins can edit any profile
    if (!$isAdminLoggedIn) {
        // For non-admins, check ownership
        if (!$currentUser || $riderId !== $currentUser['id']) {
            // Check if it's a child profile
            if (!$currentUser || !function_exists('hub_is_parent_of') || !hub_is_parent_of($currentUser['id'], $riderId)) {
                http_response_code(403);
                $response['error'] = 'Du har inte behörighet att ändra denna profil.';
                echo json_encode($response);
                exit;
            }
        }
    }

    // Check if file was uploaded
    if (!isset($_FILES['avatar']) || $_FILES['avatar']['error'] === UPLOAD_ERR_NO_FILE) {
        http_response_code(400);
        $response['error'] = 'Ingen bild valdes.';
        echo json_encode($response);
        exit;
    }

    // Upload to ImgBB
    $uploadResult = upload_avatar_to_imgbb($_FILES['avatar']);

    if (!$uploadResult['success']) {
        http_response_code(400);
        $response['error'] = $uploadResult['error'];
        echo json_encode($response);
        exit;
    }

    $avatarUrl = $uploadResult['url'];

    // Update rider's avatar_url in database
    $pdo = hub_db();
    $stmt = $pdo->prepare("UPDATE riders SET avatar_url = ?, updated_at = NOW() WHERE id = ?");
    $stmt->execute([$avatarUrl, $riderId]);

    if ($stmt->rowCount() === 0) {
        // Rider not found or no change
        error_log("Avatar update: No rows affected for rider ID {$riderId}");
    }

    $response['success'] = true;
    $response['avatar_url'] = $avatarUrl;
    $response['message'] = 'Profilbilden har uppdaterats!';

    // Include thumbnail URL if available
    if (!empty($uploadResult['thumb_url'])) {
        $response['thumb_url'] = $uploadResult['thumb_url'];
    }

    echo json_encode($response);

} catch (PDOException $e) {
    error_log("Avatar update DB error: " . $e->getMessage());
    http_response_code(500);
    $response['error'] = 'Databasfel. Försök igen senare.';
    echo json_encode($response);

} catch (Exception $e) {
    error_log("Avatar update error: " . $e->getMessage());
    http_response_code(500);
    $response['error'] = 'Ett oväntat fel uppstod.';
    echo json_encode($response);
}
