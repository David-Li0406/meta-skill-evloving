<?php
/**
 * API endpoint to create a quick sponsor for an event
 * Handles logo upload with automatic resize to 400x120px
 *
 * POST parameters:
 * - event_id: The event this sponsor is for
 * - name: Sponsor name (required)
 * - website: Sponsor website (optional)
 * - logo: File upload (required, PNG/JPG/WebP, will be resized to 400x120px)
 * - csrf_token: CSRF token
 */

require_once __DIR__ . '/../../config.php';
require_once __DIR__ . '/../../includes/media-functions.php';
require_once __DIR__ . '/../../includes/sponsor-functions.php';

require_admin();

header('Content-Type: application/json');

// Verify CSRF token
$csrfToken = $_POST['csrf_token'] ?? '';
if (!verify_csrf_token($csrfToken)) {
    echo json_encode(['success' => false, 'error' => 'Ogiltig CSRF-token. Ladda om sidan.']);
    exit;
}

// Get parameters
$eventId = (int)($_POST['event_id'] ?? 0);
$name = trim($_POST['name'] ?? '');
$website = trim($_POST['website'] ?? '');

// Validate required fields
if ($eventId <= 0) {
    echo json_encode(['success' => false, 'error' => 'Event-ID saknas']);
    exit;
}

if (empty($name)) {
    echo json_encode(['success' => false, 'error' => 'Sponsorns namn krävs']);
    exit;
}

// Check if file was uploaded
if (!isset($_FILES['logo']) || $_FILES['logo']['error'] === UPLOAD_ERR_NO_FILE) {
    echo json_encode(['success' => false, 'error' => 'Logotyp krävs. Ladda upp en PNG eller JPG-bild.']);
    exit;
}

if ($_FILES['logo']['error'] !== UPLOAD_ERR_OK) {
    $errorMessages = [
        UPLOAD_ERR_INI_SIZE => 'Filen är för stor (serverinställning)',
        UPLOAD_ERR_FORM_SIZE => 'Filen är för stor',
        UPLOAD_ERR_PARTIAL => 'Filen laddades bara upp delvis',
        UPLOAD_ERR_NO_TMP_DIR => 'Tillfällig mapp saknas',
        UPLOAD_ERR_CANT_WRITE => 'Kunde inte skriva filen',
        UPLOAD_ERR_EXTENSION => 'Uppladdning stoppades av ett tillägg'
    ];
    $errorMsg = $errorMessages[$_FILES['logo']['error']] ?? 'Okänt fel vid uppladdning';
    echo json_encode(['success' => false, 'error' => $errorMsg]);
    exit;
}

// Validate file type
$allowedTypes = ['image/png', 'image/jpeg', 'image/webp'];
$finfo = finfo_open(FILEINFO_MIME_TYPE);
$mimeType = finfo_file($finfo, $_FILES['logo']['tmp_name']);
finfo_close($finfo);

if (!in_array($mimeType, $allowedTypes)) {
    echo json_encode(['success' => false, 'error' => 'Ogiltigt bildformat. Använd PNG, JPG eller WebP.']);
    exit;
}

global $pdo;

try {
    // Get event and series info for folder structure
    $stmt = $pdo->prepare("
        SELECT e.name as event_name, s.name as series_name, s.short_name as series_short
        FROM events e
        LEFT JOIN series s ON e.series_id = s.id
        WHERE e.id = ?
    ");
    $stmt->execute([$eventId]);
    $eventInfo = $stmt->fetch(PDO::FETCH_ASSOC);

    if (!$eventInfo) {
        echo json_encode(['success' => false, 'error' => 'Eventet hittades inte']);
        exit;
    }

    // Create folder path: sponsors/{series}/{event}
    $seriesSlug = slugify($eventInfo['series_short'] ?: $eventInfo['series_name'] ?: 'general');
    $eventSlug = slugify($eventInfo['event_name']);
    $folder = "sponsors/{$seriesSlug}/{$eventSlug}";

    // Get current user ID
    $currentUser = get_admin_user();
    $uploadedBy = $currentUser ? $currentUser['id'] : null;

    // Upload and resize logo to 400x120px
    $uploadResult = upload_sponsor_logo($_FILES['logo'], $folder, $uploadedBy);

    if (!$uploadResult['success']) {
        echo json_encode(['success' => false, 'error' => 'Kunde inte ladda upp logotypen: ' . ($uploadResult['error'] ?? 'Okänt fel')]);
        exit;
    }

    $pdo->beginTransaction();

    // Create the sponsor
    $sponsorData = [
        'name' => $name,
        'website' => $website ?: null,
        'tier' => 'bronze', // Default tier for quick sponsors
        'active' => 1,
        'logo_media_id' => $uploadResult['id'],
        'display_order' => 999 // Put at end
    ];

    $sponsorId = create_sponsor($sponsorData);

    if (!$sponsorId) {
        throw new Exception('Kunde inte skapa sponsor i databasen');
    }

    // Link sponsor to this event as partner
    $stmt = $pdo->prepare("
        SELECT COALESCE(MAX(display_order), 0) + 1 as next_order
        FROM event_sponsors
        WHERE event_id = ? AND placement = 'partner'
    ");
    $stmt->execute([$eventId]);
    $nextOrder = $stmt->fetchColumn();

    $stmt = $pdo->prepare("
        INSERT INTO event_sponsors (event_id, sponsor_id, placement, display_order)
        VALUES (?, ?, 'partner', ?)
    ");
    $stmt->execute([$eventId, $sponsorId, $nextOrder]);

    $pdo->commit();

    echo json_encode([
        'success' => true,
        'sponsor' => [
            'id' => $sponsorId,
            'name' => $name,
            'logo_url' => $uploadResult['url']
        ],
        'message' => 'Sponsor skapad och tillagd!'
    ]);

} catch (Exception $e) {
    if ($pdo->inTransaction()) {
        $pdo->rollBack();
    }
    error_log("Create event sponsor error: " . $e->getMessage());
    echo json_encode(['success' => false, 'error' => 'Ett fel uppstod: ' . $e->getMessage()]);
}
