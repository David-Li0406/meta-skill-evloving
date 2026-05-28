<?php
/**
 * ImgBB Avatar Upload Functions
 *
 * Handles uploading profile pictures to ImgBB external service
 */

// Load ImgBB configuration
$imgbbConfig = __DIR__ . '/../config/imgbb.php';
if (file_exists($imgbbConfig)) {
    require_once $imgbbConfig;
}

/**
 * Upload avatar image to ImgBB
 *
 * @param array $file The $_FILES['avatar'] array
 * @return array ['success' => bool, 'url' => string|null, 'error' => string|null]
 */
function upload_avatar_to_imgbb($file) {
    // Check if API key is configured
    if (!defined('IMGBB_API_KEY') || IMGBB_API_KEY === 'YOUR_API_KEY_HERE') {
        error_log('ImgBB: API key not configured');
        return [
            'success' => false,
            'url' => null,
            'error' => 'Bilduppladdning är inte konfigurerad. Kontakta administratören.'
        ];
    }

    // Check for upload errors
    if ($file['error'] !== UPLOAD_ERR_OK) {
        $errorMessages = [
            UPLOAD_ERR_INI_SIZE => 'Filen är för stor (serverinställning)',
            UPLOAD_ERR_FORM_SIZE => 'Filen är för stor (formulärgräns)',
            UPLOAD_ERR_PARTIAL => 'Filen laddades endast upp delvis',
            UPLOAD_ERR_NO_FILE => 'Ingen fil valdes',
            UPLOAD_ERR_NO_TMP_DIR => 'Temporär mapp saknas på servern',
            UPLOAD_ERR_CANT_WRITE => 'Kunde inte skriva filen till disk',
            UPLOAD_ERR_EXTENSION => 'Uppladdning stoppades av ett tillägg',
        ];
        $errorMsg = $errorMessages[$file['error']] ?? 'Okänt uppladdningsfel';
        error_log('ImgBB: Upload error - ' . $errorMsg);
        return [
            'success' => false,
            'url' => null,
            'error' => $errorMsg
        ];
    }

    // Validate file size
    $maxSize = defined('AVATAR_MAX_SIZE') ? AVATAR_MAX_SIZE : 2 * 1024 * 1024;
    if ($file['size'] > $maxSize) {
        $maxMB = $maxSize / 1024 / 1024;
        return [
            'success' => false,
            'url' => null,
            'error' => "Filen är för stor. Max {$maxMB}MB tillåten."
        ];
    }

    // Validate file type using finfo
    $finfo = new finfo(FILEINFO_MIME_TYPE);
    $mimeType = $finfo->file($file['tmp_name']);

    $allowedTypes = defined('AVATAR_ALLOWED_TYPES')
        ? AVATAR_ALLOWED_TYPES
        : ['image/jpeg', 'image/png', 'image/gif', 'image/webp'];

    if (!in_array($mimeType, $allowedTypes)) {
        return [
            'success' => false,
            'url' => null,
            'error' => 'Otillåten filtyp. Endast JPG, PNG, GIF och WebP är tillåtna.'
        ];
    }

    // Read file and convert to base64
    $imageData = file_get_contents($file['tmp_name']);
    if ($imageData === false) {
        error_log('ImgBB: Could not read uploaded file');
        return [
            'success' => false,
            'url' => null,
            'error' => 'Kunde inte läsa den uppladdade filen.'
        ];
    }

    $base64Image = base64_encode($imageData);

    // Prepare API request
    $apiUrl = defined('IMGBB_API_URL') ? IMGBB_API_URL : 'https://api.imgbb.com/1/upload';
    $apiKey = IMGBB_API_KEY;

    $postData = [
        'key' => $apiKey,
        'image' => $base64Image,
        'name' => 'avatar_' . time() . '_' . bin2hex(random_bytes(4))
    ];

    // Make cURL request to ImgBB
    $ch = curl_init();
    curl_setopt_array($ch, [
        CURLOPT_URL => $apiUrl,
        CURLOPT_POST => true,
        CURLOPT_POSTFIELDS => $postData,
        CURLOPT_RETURNTRANSFER => true,
        CURLOPT_TIMEOUT => 30,
        CURLOPT_SSL_VERIFYPEER => true,
        CURLOPT_USERAGENT => 'TheHUB/1.0'
    ]);

    $response = curl_exec($ch);
    $httpCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
    $curlError = curl_error($ch);
    curl_close($ch);

    // Handle cURL errors
    if ($response === false) {
        error_log('ImgBB: cURL error - ' . $curlError);
        return [
            'success' => false,
            'url' => null,
            'error' => 'Kunde inte ansluta till bildtjänsten. Försök igen senare.'
        ];
    }

    // Parse response
    $result = json_decode($response, true);

    if ($httpCode !== 200 || !isset($result['success']) || !$result['success']) {
        $errorMsg = $result['error']['message'] ?? 'Okänt fel från bildtjänsten';
        error_log('ImgBB: API error - ' . $errorMsg . ' (HTTP ' . $httpCode . ')');
        return [
            'success' => false,
            'url' => null,
            'error' => 'Bilduppladdning misslyckades: ' . $errorMsg
        ];
    }

    // Get the image URL
    $imageUrl = $result['data']['url'] ?? null;

    if (!$imageUrl) {
        error_log('ImgBB: No URL in response');
        return [
            'success' => false,
            'url' => null,
            'error' => 'Fick inget svar från bildtjänsten.'
        ];
    }

    error_log('ImgBB: Successfully uploaded image - ' . $imageUrl);

    return [
        'success' => true,
        'url' => $imageUrl,
        'error' => null,
        'delete_url' => $result['data']['delete_url'] ?? null,
        'thumb_url' => $result['data']['thumb']['url'] ?? $imageUrl,
        'medium_url' => $result['data']['medium']['url'] ?? $imageUrl
    ];
}

/**
 * Validate avatar file before upload
 *
 * @param array $file The $_FILES['avatar'] array
 * @return array ['valid' => bool, 'error' => string|null]
 */
function validate_avatar_file($file) {
    // Check if file exists
    if (!isset($file) || $file['error'] === UPLOAD_ERR_NO_FILE) {
        return ['valid' => false, 'error' => 'Ingen fil valdes'];
    }

    // Check for errors
    if ($file['error'] !== UPLOAD_ERR_OK) {
        return ['valid' => false, 'error' => 'Fel vid uppladdning'];
    }

    // Check file size
    $maxSize = defined('AVATAR_MAX_SIZE') ? AVATAR_MAX_SIZE : 2 * 1024 * 1024;
    if ($file['size'] > $maxSize) {
        $maxMB = $maxSize / 1024 / 1024;
        return ['valid' => false, 'error' => "Filen är för stor (max {$maxMB}MB)"];
    }

    // Check mime type
    $finfo = new finfo(FILEINFO_MIME_TYPE);
    $mimeType = $finfo->file($file['tmp_name']);

    $allowedTypes = defined('AVATAR_ALLOWED_TYPES')
        ? AVATAR_ALLOWED_TYPES
        : ['image/jpeg', 'image/png', 'image/gif', 'image/webp'];

    if (!in_array($mimeType, $allowedTypes)) {
        return ['valid' => false, 'error' => 'Otillåten filtyp'];
    }

    return ['valid' => true, 'error' => null];
}
