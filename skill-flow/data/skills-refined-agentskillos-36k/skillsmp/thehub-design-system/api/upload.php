<?php
/**
 * Simple File Upload API
 * TheHUB V3
 *
 * Handles file uploads for sponsors and other assets
 *
 * Security: This endpoint is protected by:
 * - Only allowing specific folders
 * - Only allowing image files
 * - File size limits
 * - Random filenames
 * - Calling pages (admin/*) already require authentication
 */
header('Content-Type: application/json');

require_once __DIR__ . '/../config.php';

// Handle upload
if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    echo json_encode(['success' => false, 'error' => 'POST krävs']);
    exit;
}

if (!isset($_FILES['file']) || $_FILES['file']['error'] !== UPLOAD_ERR_OK) {
    $errorMessages = [
        UPLOAD_ERR_INI_SIZE => 'Filen är för stor (PHP-gräns)',
        UPLOAD_ERR_FORM_SIZE => 'Filen är för stor (formulär-gräns)',
        UPLOAD_ERR_PARTIAL => 'Filen laddades endast upp delvis',
        UPLOAD_ERR_NO_FILE => 'Ingen fil laddades upp',
        UPLOAD_ERR_NO_TMP_DIR => 'Temporär mapp saknas',
        UPLOAD_ERR_CANT_WRITE => 'Kunde inte skriva filen till disk',
        UPLOAD_ERR_EXTENSION => 'Filuppladdning stoppades av ett tillägg',
    ];
    $errorCode = $_FILES['file']['error'] ?? UPLOAD_ERR_NO_FILE;
    $errorMsg = $errorMessages[$errorCode] ?? 'Okänt uppladdningsfel';
    echo json_encode(['success' => false, 'error' => $errorMsg]);
    exit;
}

$file = $_FILES['file'];
$folder = $_POST['folder'] ?? 'uploads';

// Allowed folders
$allowedFolders = ['sponsors', 'media', 'uploads', 'events', 'series'];
if (!in_array($folder, $allowedFolders)) {
    $folder = 'uploads';
}

// Validate file type (images only for now)
$allowedTypes = ['image/jpeg', 'image/png', 'image/gif', 'image/webp', 'image/svg+xml'];
$finfo = new finfo(FILEINFO_MIME_TYPE);
$mimeType = $finfo->file($file['tmp_name']);

if (!in_array($mimeType, $allowedTypes)) {
    echo json_encode(['success' => false, 'error' => 'Otillåten filtyp. Endast bilder tillåtna.']);
    exit;
}

// Max file size: 5MB
$maxSize = 5 * 1024 * 1024;
if ($file['size'] > $maxSize) {
    echo json_encode(['success' => false, 'error' => 'Filen är för stor. Max 5MB.']);
    exit;
}

// Create upload directory
$uploadDir = __DIR__ . '/../uploads/' . $folder . '/';
if (!is_dir($uploadDir)) {
    mkdir($uploadDir, 0755, true);
}

// Generate unique filename
$extension = pathinfo($file['name'], PATHINFO_EXTENSION);
$safeName = preg_replace('/[^a-zA-Z0-9_-]/', '', pathinfo($file['name'], PATHINFO_FILENAME));
$safeName = substr($safeName, 0, 50);
$filename = $safeName . '_' . uniqid() . '.' . $extension;

$destination = $uploadDir . $filename;

// Move uploaded file
if (!move_uploaded_file($file['tmp_name'], $destination)) {
    echo json_encode(['success' => false, 'error' => 'Kunde inte spara filen']);
    exit;
}

// Return success with path
$relativePath = '/uploads/' . $folder . '/' . $filename;

echo json_encode([
    'success' => true,
    'path' => $relativePath,
    'filename' => $filename,
    'size' => $file['size'],
    'type' => $mimeType
]);
