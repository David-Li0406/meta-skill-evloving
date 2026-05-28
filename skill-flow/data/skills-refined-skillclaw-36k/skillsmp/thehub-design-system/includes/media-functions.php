<?php
/**
 * Media Library Functions
 * TheHUB V3 - Media & Sponsor System
 */

/**
 * Get media statistics by folder
 */
function get_media_stats() {
    global $pdo;
    
    try {
        $stmt = $pdo->query("
            SELECT 
                folder,
                COUNT(*) as count,
                SUM(size) as total_size
            FROM media
            GROUP BY folder
        ");
        return $stmt->fetchAll(PDO::FETCH_ASSOC);
    } catch (PDOException $e) {
        error_log("get_media_stats error: " . $e->getMessage());
        return [];
    }
}

/**
 * Get media files by folder
 * Supports subfolders with LIKE matching (e.g., "sponsors" matches "sponsors/mysponsor")
 */
function get_media_by_folder($folder = null, $limit = 50, $offset = 0, $includeSubfolders = false) {
    global $pdo;

    try {
        $sql = "SELECT * FROM media";
        $params = [];

        if ($folder) {
            if ($includeSubfolders) {
                // Match folder and all subfolders
                $sql .= " WHERE (folder = ? OR folder LIKE ?)";
                $params[] = $folder;
                $params[] = $folder . '/%';
            } else {
                $sql .= " WHERE folder = ?";
                $params[] = $folder;
            }
        }

        $sql .= " ORDER BY uploaded_at DESC LIMIT ? OFFSET ?";
        $params[] = (int)$limit;
        $params[] = (int)$offset;

        $stmt = $pdo->prepare($sql);
        $stmt->execute($params);
        return $stmt->fetchAll(PDO::FETCH_ASSOC);
    } catch (PDOException $e) {
        error_log("get_media_by_folder error: " . $e->getMessage());
        return [];
    }
}

/**
 * Get subfolders within a parent folder
 */
function get_media_subfolders($parentFolder) {
    global $pdo;

    try {
        $stmt = $pdo->prepare("
            SELECT
                folder,
                COUNT(*) as count,
                SUM(size) as total_size
            FROM media
            WHERE folder LIKE ?
            GROUP BY folder
            ORDER BY folder
        ");
        $stmt->execute([$parentFolder . '/%']);
        $results = $stmt->fetchAll(PDO::FETCH_ASSOC);

        // Extract subfolder names
        $subfolders = [];
        foreach ($results as $row) {
            // Get the subfolder name (part after parent/)
            $subPath = substr($row['folder'], strlen($parentFolder) + 1);
            // Only include direct subfolders (not nested)
            if (strpos($subPath, '/') === false) {
                $subfolders[] = [
                    'name' => $subPath,
                    'path' => $row['folder'],
                    'count' => (int)$row['count'],
                    'size' => (int)$row['total_size']
                ];
            }
        }

        return $subfolders;
    } catch (PDOException $e) {
        error_log("get_media_subfolders error: " . $e->getMessage());
        return [];
    }
}

/**
 * Create a media subfolder for a sponsor
 * Returns the folder path
 */
function create_sponsor_media_folder($sponsorName) {
    // Generate slug from sponsor name
    $slug = strtolower(trim($sponsorName));
    $slug = preg_replace('/[åä]/u', 'a', $slug);
    $slug = preg_replace('/[ö]/u', 'o', $slug);
    $slug = preg_replace('/[^a-z0-9]+/', '-', $slug);
    $slug = trim($slug, '-');

    return 'sponsors/' . $slug;
}

/**
 * Search media files
 * Supports searching in subfolders with LIKE matching
 */
function search_media($query, $folder = null, $limit = 50, $includeSubfolders = true) {
    global $pdo;

    try {
        $sql = "SELECT * FROM media WHERE (original_filename LIKE ? OR alt_text LIKE ? OR caption LIKE ?)";
        $searchTerm = "%{$query}%";
        $params = [$searchTerm, $searchTerm, $searchTerm];

        if ($folder) {
            if ($includeSubfolders) {
                $sql .= " AND (folder = ? OR folder LIKE ?)";
                $params[] = $folder;
                $params[] = $folder . '/%';
            } else {
                $sql .= " AND folder = ?";
                $params[] = $folder;
            }
        }

        $sql .= " ORDER BY uploaded_at DESC LIMIT ?";
        $params[] = (int)$limit;

        $stmt = $pdo->prepare($sql);
        $stmt->execute($params);
        return $stmt->fetchAll(PDO::FETCH_ASSOC);
    } catch (PDOException $e) {
        error_log("search_media error: " . $e->getMessage());
        return [];
    }
}

/**
 * Get single media file by ID
 */
function get_media($id) {
    global $pdo;
    
    try {
        $stmt = $pdo->prepare("SELECT * FROM media WHERE id = ?");
        $stmt->execute([$id]);
        return $stmt->fetch(PDO::FETCH_ASSOC);
    } catch (PDOException $e) {
        error_log("get_media error: " . $e->getMessage());
        return null;
    }
}

/**
 * Get media URL
 */
function get_media_url($id) {
    $media = get_media($id);
    if ($media && isset($media['filepath'])) {
        return '/' . ltrim($media['filepath'], '/');
    }
    return null;
}

/**
 * Upload media file
 */
function upload_media($file, $folder = 'general', $uploadedBy = null) {
    global $pdo;
    
    $allowedTypes = ['image/jpeg', 'image/png', 'image/gif', 'image/webp', 'image/svg+xml', 'application/pdf'];
    $maxSize = 10 * 1024 * 1024; // 10MB
    
    // Validate file
    if (!isset($file['tmp_name']) || !is_uploaded_file($file['tmp_name'])) {
        return ['success' => false, 'error' => 'Ingen fil uppladdad'];
    }
    
    if ($file['size'] > $maxSize) {
        return ['success' => false, 'error' => 'Filen är för stor (max 10MB)'];
    }
    
    $mimeType = mime_content_type($file['tmp_name']);
    if (!in_array($mimeType, $allowedTypes)) {
        return ['success' => false, 'error' => 'Filtypen stöds inte'];
    }
    
    // Generate filename
    $ext = pathinfo($file['name'], PATHINFO_EXTENSION);
    $filename = uniqid() . '_' . time() . '.' . strtolower($ext);
    $relativeFilepath = "uploads/media/{$folder}/{$filename}";

    // Use absolute path for file operations
    $rootPath = defined('ROOT_PATH') ? ROOT_PATH : dirname(__DIR__);
    $absoluteFilepath = $rootPath . '/' . $relativeFilepath;

    // Create directory if needed
    $dir = dirname($absoluteFilepath);
    if (!is_dir($dir)) {
        mkdir($dir, 0755, true);
    }

    // Move file
    if (!move_uploaded_file($file['tmp_name'], $absoluteFilepath)) {
        return ['success' => false, 'error' => 'Kunde inte spara filen'];
    }

    // Get image dimensions if applicable
    $width = null;
    $height = null;
    if (strpos($mimeType, 'image/') === 0 && $mimeType !== 'image/svg+xml') {
        $dimensions = getimagesize($absoluteFilepath);
        if ($dimensions) {
            $width = $dimensions[0];
            $height = $dimensions[1];
        }
    }
    
    // Save to database (store relative path)
    try {
        $stmt = $pdo->prepare("
            INSERT INTO media (filename, original_filename, filepath, mime_type, size, width, height, folder, uploaded_by, uploaded_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, NOW())
        ");
        $stmt->execute([
            $filename,
            $file['name'],
            $relativeFilepath,
            $mimeType,
            $file['size'],
            $width,
            $height,
            $folder,
            $uploadedBy
        ]);

        $mediaId = $pdo->lastInsertId();

        return [
            'success' => true,
            'id' => $mediaId,
            'url' => '/' . $relativeFilepath,
            'filename' => $filename
        ];
    } catch (PDOException $e) {
        error_log("upload_media error: " . $e->getMessage());
        // Clean up file on database error
        @unlink($absoluteFilepath);
        return ['success' => false, 'error' => 'Databasfel'];
    }
}

/**
 * Update media metadata
 */
function update_media($id, $data) {
    global $pdo;
    
    try {
        $allowedFields = ['folder', 'alt_text', 'caption'];
        $updates = [];
        $params = [];
        
        foreach ($allowedFields as $field) {
            if (isset($data[$field])) {
                $updates[] = "{$field} = ?";
                $params[] = $data[$field];
            }
        }
        
        if (empty($updates)) {
            return ['success' => false, 'error' => 'Inget att uppdatera'];
        }
        
        $params[] = $id;
        $sql = "UPDATE media SET " . implode(', ', $updates) . " WHERE id = ?";
        
        $stmt = $pdo->prepare($sql);
        $stmt->execute($params);
        
        return ['success' => true];
    } catch (PDOException $e) {
        error_log("update_media error: " . $e->getMessage());
        return ['success' => false, 'error' => 'Kunde inte uppdatera'];
    }
}

/**
 * Delete media file
 */
function delete_media($id) {
    global $pdo;
    
    try {
        // Get file info first
        $media = get_media($id);
        if (!$media) {
            return ['success' => false, 'error' => 'Media hittades inte'];
        }
        
        // Check if media is in use
        $usage = get_media_usage($id);
        if (!empty($usage)) {
            return ['success' => false, 'error' => 'Filen används och kan inte raderas'];
        }
        
        // Delete from database
        $stmt = $pdo->prepare("DELETE FROM media WHERE id = ?");
        $stmt->execute([$id]);
        
        // Delete file (use absolute path)
        $rootPath = defined('ROOT_PATH') ? ROOT_PATH : dirname(__DIR__);
        $absolutePath = $rootPath . '/' . ltrim($media['filepath'], '/');
        if (file_exists($absolutePath)) {
            @unlink($absolutePath);
        }

        return ['success' => true];
    } catch (PDOException $e) {
        error_log("delete_media error: " . $e->getMessage());
        return ['success' => false, 'error' => 'Kunde inte radera'];
    }
}

/**
 * Get media usage (where it's used)
 */
function get_media_usage($mediaId) {
    global $pdo;
    $usage = [];
    
    try {
        // Check sponsors
        $stmt = $pdo->prepare("SELECT id, name FROM sponsors WHERE logo_media_id = ?");
        $stmt->execute([$mediaId]);
        foreach ($stmt->fetchAll(PDO::FETCH_ASSOC) as $row) {
            $usage[] = [
                'entity_type' => 'Sponsor',
                'entity_id' => $row['id'],
                'entity_name' => $row['name'],
                'field' => 'logo'
            ];
        }
        
        // Check series (if columns exist)
        try {
            $stmt = $pdo->prepare("SELECT id, name FROM series WHERE logo_light_media_id = ? OR logo_dark_media_id = ?");
            $stmt->execute([$mediaId, $mediaId]);
            foreach ($stmt->fetchAll(PDO::FETCH_ASSOC) as $row) {
                $usage[] = [
                    'entity_type' => 'Serie',
                    'entity_id' => $row['id'],
                    'entity_name' => $row['name'],
                    'field' => 'logo'
                ];
            }
        } catch (PDOException $e) {
            // Columns might not exist yet
        }
        
        // Check ad_placements
        try {
            $stmt = $pdo->prepare("SELECT id, name FROM ad_placements WHERE media_id = ?");
            $stmt->execute([$mediaId]);
            foreach ($stmt->fetchAll(PDO::FETCH_ASSOC) as $row) {
                $usage[] = [
                    'entity_type' => 'Annons',
                    'entity_id' => $row['id'],
                    'entity_name' => $row['name'],
                    'field' => 'bild'
                ];
            }
        } catch (PDOException $e) {
            // Table might not exist yet
        }
        
    } catch (PDOException $e) {
        error_log("get_media_usage error: " . $e->getMessage());
    }
    
    return $usage;
}

/**
 * Format file size for display
 */
function format_file_size($bytes) {
    if ($bytes === null || $bytes === 0) return '0 B';
    
    $units = ['B', 'KB', 'MB', 'GB'];
    $unitIndex = 0;
    $size = (float)$bytes;
    
    while ($size >= 1024 && $unitIndex < count($units) - 1) {
        $size /= 1024;
        $unitIndex++;
    }
    
    return round($size, 1) . ' ' . $units[$unitIndex];
}

/**
 * Check if media exists
 */
function media_exists($id) {
    global $pdo;

    try {
        $stmt = $pdo->prepare("SELECT COUNT(*) FROM media WHERE id = ?");
        $stmt->execute([$id]);
        return $stmt->fetchColumn() > 0;
    } catch (PDOException $e) {
        return false;
    }
}

/**
 * Get media thumbnail URL
 * For now returns the same URL, but can be extended to generate actual thumbnails
 */
function get_media_thumbnail($id, $size = 'medium') {
    $media = get_media($id);
    if ($media && isset($media['filepath'])) {
        return '/' . ltrim($media['filepath'], '/');
    }
    return '/assets/images/placeholder.png';
}

/**
 * Resize an image to specific dimensions
 * Maintains aspect ratio and pads with transparent background if needed
 *
 * @param string $sourcePath Path to source image
 * @param string $destPath Path to save resized image
 * @param int $targetWidth Target width in pixels
 * @param int $targetHeight Target height in pixels
 * @param bool $fitInside If true, image fits inside dimensions (may have padding). If false, fills dimensions (may crop)
 * @return bool Success
 */
function resize_image($sourcePath, $destPath, $targetWidth, $targetHeight, $fitInside = true) {
    if (!file_exists($sourcePath)) {
        return false;
    }

    $imageInfo = getimagesize($sourcePath);
    if (!$imageInfo) {
        return false;
    }

    $mimeType = $imageInfo['mime'];
    $origWidth = $imageInfo[0];
    $origHeight = $imageInfo[1];

    // Create source image
    switch ($mimeType) {
        case 'image/jpeg':
            $srcImage = imagecreatefromjpeg($sourcePath);
            break;
        case 'image/png':
            $srcImage = imagecreatefrompng($sourcePath);
            break;
        case 'image/gif':
            $srcImage = imagecreatefromgif($sourcePath);
            break;
        case 'image/webp':
            $srcImage = imagecreatefromwebp($sourcePath);
            break;
        default:
            return false;
    }

    if (!$srcImage) {
        return false;
    }

    // Calculate new dimensions maintaining aspect ratio
    $origRatio = $origWidth / $origHeight;
    $targetRatio = $targetWidth / $targetHeight;

    if ($fitInside) {
        // Fit inside: image fits completely inside target dimensions
        if ($origRatio > $targetRatio) {
            $newWidth = $targetWidth;
            $newHeight = (int)($targetWidth / $origRatio);
        } else {
            $newHeight = $targetHeight;
            $newWidth = (int)($targetHeight * $origRatio);
        }
    } else {
        // Fill: image fills target dimensions (may crop)
        if ($origRatio > $targetRatio) {
            $newHeight = $targetHeight;
            $newWidth = (int)($targetHeight * $origRatio);
        } else {
            $newWidth = $targetWidth;
            $newHeight = (int)($targetWidth / $origRatio);
        }
    }

    // Create destination image with transparent background
    $dstImage = imagecreatetruecolor($targetWidth, $targetHeight);

    // For PNG/WebP: preserve transparency
    if (in_array($mimeType, ['image/png', 'image/webp', 'image/gif'])) {
        imagealphablending($dstImage, false);
        imagesavealpha($dstImage, true);
        $transparent = imagecolorallocatealpha($dstImage, 255, 255, 255, 127);
        imagefilledrectangle($dstImage, 0, 0, $targetWidth, $targetHeight, $transparent);
    } else {
        // For JPEG: white background
        $white = imagecolorallocate($dstImage, 255, 255, 255);
        imagefilledrectangle($dstImage, 0, 0, $targetWidth, $targetHeight, $white);
    }

    // Center the image
    $x = (int)(($targetWidth - $newWidth) / 2);
    $y = (int)(($targetHeight - $newHeight) / 2);

    // Resize and copy
    imagecopyresampled($dstImage, $srcImage, $x, $y, 0, 0, $newWidth, $newHeight, $origWidth, $origHeight);

    // Save based on destination extension
    $ext = strtolower(pathinfo($destPath, PATHINFO_EXTENSION));
    $success = false;

    switch ($ext) {
        case 'jpg':
        case 'jpeg':
            $success = imagejpeg($dstImage, $destPath, 90);
            break;
        case 'png':
            $success = imagepng($dstImage, $destPath, 9);
            break;
        case 'gif':
            $success = imagegif($dstImage, $destPath);
            break;
        case 'webp':
            $success = imagewebp($dstImage, $destPath, 90);
            break;
    }

    // Clean up
    imagedestroy($srcImage);
    imagedestroy($dstImage);

    return $success;
}

/**
 * Upload a sponsor logo with automatic resizing to 400x120px
 *
 * @param array $file $_FILES array element
 * @param string $folder Folder path (e.g., 'sponsors/gravity-series/jarvsofjellet')
 * @param int|null $uploadedBy User ID who uploaded
 * @return array Result with success, id, url, etc.
 */
function upload_sponsor_logo($file, $folder, $uploadedBy = null) {
    global $pdo;

    $allowedTypes = ['image/jpeg', 'image/png', 'image/gif', 'image/webp'];
    $maxSize = 10 * 1024 * 1024; // 10MB

    // Sponsor logo - store larger original, scale via CSS
    // Max width 800px, maintain aspect ratio (no fixed height)
    $maxWidth = 800;

    // Validate file
    if (!isset($file['tmp_name']) || !is_uploaded_file($file['tmp_name'])) {
        return ['success' => false, 'error' => 'Ingen fil uppladdad'];
    }

    if ($file['size'] > $maxSize) {
        return ['success' => false, 'error' => 'Filen är för stor (max 10MB)'];
    }

    $mimeType = mime_content_type($file['tmp_name']);
    if (!in_array($mimeType, $allowedTypes)) {
        return ['success' => false, 'error' => 'Filtypen stöds inte. Använd JPG, PNG, GIF eller WebP.'];
    }

    // Generate filename - prefer PNG for transparency support
    $originalExt = strtolower(pathinfo($file['name'], PATHINFO_EXTENSION));
    $ext = in_array($originalExt, ['png', 'webp']) ? $originalExt : 'png';
    $filename = uniqid('sponsor_') . '_' . time() . '.' . $ext;
    $relativeFilepath = "uploads/media/{$folder}/{$filename}";

    // Use absolute path for file operations
    $rootPath = defined('ROOT_PATH') ? ROOT_PATH : dirname(__DIR__);
    $absoluteFilepath = $rootPath . '/' . $relativeFilepath;

    // Create directory if needed
    $dir = dirname($absoluteFilepath);
    if (!is_dir($dir)) {
        mkdir($dir, 0755, true);
    }

    // Get original dimensions
    $imageInfo = getimagesize($file['tmp_name']);
    if (!$imageInfo) {
        return ['success' => false, 'error' => 'Kunde inte läsa bilden'];
    }
    $origWidth = $imageInfo[0];
    $origHeight = $imageInfo[1];

    // Only resize if wider than max, keep aspect ratio
    $finalWidth = $origWidth;
    $finalHeight = $origHeight;

    if ($origWidth > $maxWidth) {
        $finalWidth = $maxWidth;
        $finalHeight = (int) round($origHeight * ($maxWidth / $origWidth));
        // Resize maintaining aspect ratio
        if (!resize_image($file['tmp_name'], $absoluteFilepath, $finalWidth, $finalHeight, true)) {
            return ['success' => false, 'error' => 'Kunde inte bearbeta bilden'];
        }
    } else {
        // Just copy the original
        if (!move_uploaded_file($file['tmp_name'], $absoluteFilepath)) {
            // Try copy if move fails (e.g., already moved)
            if (!copy($file['tmp_name'], $absoluteFilepath)) {
                return ['success' => false, 'error' => 'Kunde inte spara bilden'];
            }
        }
    }

    // Get final file size
    $finalSize = filesize($absoluteFilepath);

    // Save to database
    try {
        $stmt = $pdo->prepare("
            INSERT INTO media (filename, original_filename, filepath, mime_type, size, width, height, folder, uploaded_by, uploaded_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, NOW())
        ");
        $stmt->execute([
            $filename,
            $file['name'],
            $relativeFilepath,
            'image/' . $ext,
            $finalSize,
            $finalWidth,
            $finalHeight,
            $folder,
            $uploadedBy
        ]);

        $mediaId = $pdo->lastInsertId();

        return [
            'success' => true,
            'id' => $mediaId,
            'url' => '/' . $relativeFilepath,
            'filename' => $filename,
            'width' => $targetWidth,
            'height' => $targetHeight
        ];
    } catch (PDOException $e) {
        error_log("upload_sponsor_logo error: " . $e->getMessage());
        @unlink($absoluteFilepath);
        return ['success' => false, 'error' => 'Databasfel'];
    }
}

/**
 * Create a media folder path for event-specific sponsor logos
 *
 * @param string $seriesName Name of the series
 * @param string $eventName Name of the event
 * @return string Folder path like 'sponsors/gravity-series/jarvsofjellet'
 */
function create_event_sponsor_folder($seriesName, $eventName) {
    $seriesSlug = slugify($seriesName);
    $eventSlug = slugify($eventName);

    return "sponsors/{$seriesSlug}/{$eventSlug}";
}

/**
 * Create URL-safe slug from string
 */
function slugify($text) {
    // Convert Swedish characters
    $text = str_replace(['å', 'ä', 'Å', 'Ä'], 'a', $text);
    $text = str_replace(['ö', 'Ö'], 'o', $text);

    // Lowercase and replace non-alphanumeric with hyphens
    $text = strtolower(trim($text));
    $text = preg_replace('/[^a-z0-9]+/', '-', $text);
    $text = trim($text, '-');

    return $text ?: 'unknown';
}

/**
 * Get event sponsor folder path
 * Uses series name if available, otherwise 'events'
 */
function get_event_sponsor_folder($eventId) {
    global $pdo;

    try {
        $stmt = $pdo->prepare("
            SELECT e.name as event_name, s.name as series_name
            FROM events e
            LEFT JOIN series s ON e.series_id = s.id
            WHERE e.id = ?
        ");
        $stmt->execute([$eventId]);
        $result = $stmt->fetch(PDO::FETCH_ASSOC);

        if ($result) {
            $seriesName = $result['series_name'] ?: 'events';
            $eventName = $result['event_name'];
            return create_event_sponsor_folder($seriesName, $eventName);
        }
    } catch (PDOException $e) {
        error_log("get_event_sponsor_folder error: " . $e->getMessage());
    }

    return 'sponsors/events';
}
