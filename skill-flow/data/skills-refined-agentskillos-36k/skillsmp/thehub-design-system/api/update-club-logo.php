<?php
/**
 * API endpoint for uploading club logos
 * Uses ImgBB for image hosting (same as rider avatars)
 */
require_once __DIR__ . '/../config.php';
require_once __DIR__ . '/../includes/upload-avatar.php';

header('Content-Type: application/json');

// Check if user is logged in
if (!isLoggedIn()) {
    http_response_code(401);
    echo json_encode(['success' => false, 'error' => 'Inte inloggad']);
    exit;
}

// Get club ID
$clubId = isset($_POST['club_id']) ? intval($_POST['club_id']) : 0;

if (!$clubId) {
    http_response_code(400);
    echo json_encode(['success' => false, 'error' => 'Klubb-ID saknas']);
    exit;
}

// Check permissions - either admin or club admin with logo permission
$canUpload = false;
if (hasRole('admin')) {
    $canUpload = true;
} else {
    $perms = getClubAdminPermissions($clubId);
    if ($perms && $perms['can_upload_logo']) {
        $canUpload = true;
    }
}

if (!$canUpload) {
    http_response_code(403);
    echo json_encode(['success' => false, 'error' => 'Du har inte behörighet att ladda upp logotyp för denna klubb']);
    exit;
}

// Check if file was uploaded
if (!isset($_FILES['logo']) || $_FILES['logo']['error'] === UPLOAD_ERR_NO_FILE) {
    http_response_code(400);
    echo json_encode(['success' => false, 'error' => 'Ingen fil valdes']);
    exit;
}

// Upload to ImgBB using the same function as avatars
$result = upload_avatar_to_imgbb($_FILES['logo']);

if (!$result['success']) {
    http_response_code(400);
    echo json_encode(['success' => false, 'error' => $result['error']]);
    exit;
}

// Update club with new logo URL
$db = getDB();

try {
    $db->update('clubs', ['logo_url' => $result['url']], 'id = ?', [$clubId]);

    echo json_encode([
        'success' => true,
        'logo_url' => $result['url'],
        'thumb_url' => $result['thumb_url'] ?? $result['url']
    ]);
} catch (Exception $e) {
    error_log("Club logo update error: " . $e->getMessage());
    http_response_code(500);
    echo json_encode(['success' => false, 'error' => 'Kunde inte spara logotypen i databasen']);
}
