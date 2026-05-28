<?php
/**
 * Series API Endpoint
 * TheHUB V3
 *
 * Handles: update_promotor (limited update for promotors)
 */
header('Content-Type: application/json');

require_once __DIR__ . '/../config.php';

// Get action from query string
$action = $_GET['action'] ?? '';

try {
    switch ($action) {
        case 'update_promotor':
            handleUpdatePromotor();
            break;

        default:
            echo json_encode(['success' => false, 'error' => 'Ogiltig action']);
    }
} catch (Exception $e) {
    error_log("Series API error: " . $e->getMessage());
    echo json_encode(['success' => false, 'error' => 'Serverfel']);
}

/**
 * Handle promotor update of series settings (Swish, banner)
 */
function handleUpdatePromotor() {
    global $pdo;

    // Must be logged in
    if (!function_exists('hasRole') || !hasRole('promotor')) {
        echo json_encode(['success' => false, 'error' => 'Ingen behörighet']);
        return;
    }

    // Get JSON input
    $input = json_decode(file_get_contents('php://input'), true);

    if (!$input || !isset($input['id'])) {
        echo json_encode(['success' => false, 'error' => 'Serie-ID saknas']);
        return;
    }

    $seriesId = (int)$input['id'];
    $userId = $_SESSION['user']['id'] ?? 0;

    // Verify promotor has access to this series
    $accessCheck = $pdo->prepare("
        SELECT 1 FROM promotor_series
        WHERE user_id = ? AND series_id = ?
    ");
    $accessCheck->execute([$userId, $seriesId]);

    if (!$accessCheck->fetch()) {
        echo json_encode(['success' => false, 'error' => 'Du har inte behörighet till denna serie']);
        return;
    }

    // Update series fields that promotors can change
    $swishNumber = $input['swish_number'] ?? null;
    $swishName = $input['swish_name'] ?? null;
    $bannerMediaId = $input['banner_media_id'] ?? null;

    // Sanitize Swish number (remove spaces, keep dashes)
    if ($swishNumber) {
        $swishNumber = preg_replace('/[^\d\-]/', '', $swishNumber);
    }

    try {
        $stmt = $pdo->prepare("
            UPDATE series
            SET swish_number = ?,
                swish_name = ?,
                banner_media_id = ?
            WHERE id = ?
        ");
        $stmt->execute([$swishNumber, $swishName, $bannerMediaId, $seriesId]);

        echo json_encode([
            'success' => true,
            'message' => 'Serien har uppdaterats'
        ]);
    } catch (PDOException $e) {
        error_log("Series update error: " . $e->getMessage());
        echo json_encode(['success' => false, 'error' => 'Databasfel vid uppdatering']);
    }
}
