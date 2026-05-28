<?php
/**
 * ImgBB Configuration
 *
 * API key for uploading profile images to ImgBB
 * Get your free API key at: https://api.imgbb.com/
 */

// ImgBB API Key - can be overridden via environment variable
if (!defined('IMGBB_API_KEY')) {
    define('IMGBB_API_KEY', getenv('IMGBB_API_KEY') ?: 'YOUR_API_KEY_HERE');
}

// ImgBB API endpoint
if (!defined('IMGBB_API_URL')) {
    define('IMGBB_API_URL', 'https://api.imgbb.com/1/upload');
}

// Upload settings
if (!defined('AVATAR_MAX_SIZE')) {
    define('AVATAR_MAX_SIZE', 2 * 1024 * 1024); // 2MB max
}

if (!defined('AVATAR_ALLOWED_TYPES')) {
    define('AVATAR_ALLOWED_TYPES', ['image/jpeg', 'image/png', 'image/gif', 'image/webp']);
}
