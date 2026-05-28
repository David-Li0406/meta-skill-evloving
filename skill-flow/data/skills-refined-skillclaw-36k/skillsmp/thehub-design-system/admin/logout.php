<?php
require_once __DIR__ . '/../config.php';

// Prevent caching
header("Cache-Control: no-store, no-cache, must-revalidate, max-age=0");
header("Cache-Control: post-check=0, pre-check=0", false);
header("Pragma: no-cache");

logout();

// Clear any output buffers
if (ob_get_level()) {
    ob_end_clean();
}

redirect('/admin/login.php');
