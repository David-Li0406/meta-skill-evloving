<?php
/**
 * Media API Endpoint
 * TheHUB V3 - Media & Sponsor System
 * 
 * Handles: upload, get, update, delete
 */
header('Content-Type: application/json');

require_once __DIR__ . '/../config.php';
require_once __DIR__ . '/../includes/media-functions.php';

// Get action from query string
$action = $_GET['action'] ?? '';

try {
    switch ($action) {
        case 'upload':
            handleUpload();
            break;
            
        case 'get':
            handleGet();
            break;
            
        case 'update':
            handleUpdate();
            break;
            
        case 'delete':
            handleDelete();
            break;
            
        case 'list':
            handleList();
            break;

        case 'create_folder':
            handleCreateFolder();
            break;

        default:
            echo json_encode(['success' => false, 'error' => 'Ogiltig action']);
    }
} catch (Exception $e) {
    error_log("Media API error: " . $e->getMessage());
    echo json_encode(['success' => false, 'error' => 'Serverfel']);
}

/**
 * Handle file upload
 */
function handleUpload() {
    if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
        echo json_encode(['success' => false, 'error' => 'POST krävs']);
        return;
    }
    
    if (!isset($_FILES['file'])) {
        echo json_encode(['success' => false, 'error' => 'Ingen fil bifogad']);
        return;
    }
    
    $folder = $_POST['folder'] ?? 'general';
    $uploadedBy = $_SESSION['user']['id'] ?? null;
    
    $result = upload_media($_FILES['file'], $folder, $uploadedBy);
    echo json_encode($result);
}

/**
 * Get single media item
 */
function handleGet() {
    $id = $_GET['id'] ?? null;
    
    if (!$id) {
        echo json_encode(['success' => false, 'error' => 'ID saknas']);
        return;
    }
    
    $media = get_media($id);
    
    if (!$media) {
        echo json_encode(['success' => false, 'error' => 'Media hittades inte']);
        return;
    }
    
    // Add URL and usage info
    $media['url'] = '/' . ltrim($media['filepath'], '/');
    $media['thumbnail'] = $media['url']; // For now, same as main URL
    $media['usage'] = get_media_usage($id);
    
    echo json_encode(['success' => true, 'data' => $media]);
}

/**
 * Update media metadata
 */
function handleUpdate() {
    if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
        echo json_encode(['success' => false, 'error' => 'POST krävs']);
        return;
    }
    
    $input = json_decode(file_get_contents('php://input'), true);
    
    if (!$input || !isset($input['id'])) {
        echo json_encode(['success' => false, 'error' => 'ID saknas']);
        return;
    }
    
    $result = update_media($input['id'], $input);
    echo json_encode($result);
}

/**
 * Delete media
 */
function handleDelete() {
    $id = $_GET['id'] ?? null;

    if (!$id) {
        echo json_encode(['success' => false, 'error' => 'ID saknas']);
        return;
    }

    // Check if promotor - they can only delete files in their event folders
    $isPromotorOnly = function_exists('isRole') && isRole('promotor');
    if ($isPromotorOnly) {
        global $pdo;
        $media = get_media($id);
        if (!$media) {
            echo json_encode(['success' => false, 'error' => 'Media hittades inte']);
            return;
        }

        // Get promotor's allowed folders
        $promotorAllowedFolders = [];
        if (function_exists('getPromotorEvents')) {
            $promotorEvents = getPromotorEvents();
            foreach ($promotorEvents as $event) {
                $eventInfo = $pdo->prepare("
                    SELECT e.name as event_name, s.short_name as series_short, s.name as series_name
                    FROM events e
                    LEFT JOIN series s ON e.series_id = s.id
                    WHERE e.id = ?
                ");
                $eventInfo->execute([$event['id']]);
                $info = $eventInfo->fetch(PDO::FETCH_ASSOC);
                if ($info) {
                    $seriesSlug = slugify($info['series_short'] ?: $info['series_name'] ?: 'general');
                    $eventSlug = slugify($info['event_name']);
                    $promotorAllowedFolders[] = "sponsors/{$seriesSlug}/{$eventSlug}";
                }
            }
        }

        // Check if file is in an allowed folder
        $hasAccess = false;
        foreach ($promotorAllowedFolders as $allowed) {
            if (strpos($media['folder'], $allowed) === 0 || $media['folder'] === $allowed) {
                $hasAccess = true;
                break;
            }
        }

        if (!$hasAccess) {
            echo json_encode(['success' => false, 'error' => 'Du har inte behörighet att radera denna fil']);
            return;
        }
    }

    $result = delete_media($id);
    echo json_encode($result);
}

/**
 * List media with filters
 */
function handleList() {
    $folder = $_GET['folder'] ?? null;
    $search = $_GET['search'] ?? '';
    $limit = min((int)($_GET['limit'] ?? 50), 200);
    $offset = (int)($_GET['offset'] ?? 0);
    
    if ($search) {
        $files = search_media($search, $folder, $limit);
    } else {
        $files = get_media_by_folder($folder, $limit, $offset);
    }
    
    // Add URLs
    foreach ($files as &$file) {
        $file['url'] = '/' . ltrim($file['filepath'], '/');
        $file['thumbnail'] = $file['url'];
    }
    
    echo json_encode([
        'success' => true,
        'data' => $files,
        'count' => count($files)
    ]);
}

/**
 * Create a new folder
 */
function handleCreateFolder() {
    if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
        echo json_encode(['success' => false, 'error' => 'POST krävs']);
        return;
    }

    // Get JSON input
    $input = json_decode(file_get_contents('php://input'), true);
    $folderPath = $input['folder'] ?? '';

    if (empty($folderPath)) {
        echo json_encode(['success' => false, 'error' => 'Mappnamn saknas']);
        return;
    }

    // Sanitize folder path
    $folderPath = preg_replace('/[^a-z0-9\-\/]/', '', strtolower($folderPath));
    $folderPath = trim($folderPath, '/');

    if (empty($folderPath)) {
        echo json_encode(['success' => false, 'error' => 'Ogiltigt mappnamn']);
        return;
    }

    // Create the physical folder
    $uploadDir = __DIR__ . '/../uploads/media/' . $folderPath;

    if (is_dir($uploadDir)) {
        // Folder already exists - that's fine
        echo json_encode([
            'success' => true,
            'message' => 'Mappen finns redan',
            'folder' => $folderPath
        ]);
        return;
    }

    if (!mkdir($uploadDir, 0755, true)) {
        echo json_encode(['success' => false, 'error' => 'Kunde inte skapa mappen']);
        return;
    }

    echo json_encode([
        'success' => true,
        'message' => 'Mappen skapades',
        'folder' => $folderPath
    ]);
}
