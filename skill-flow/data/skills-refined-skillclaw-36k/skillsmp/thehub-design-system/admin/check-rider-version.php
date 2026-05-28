<?php
require_once __DIR__ . '/../config.php';

header('Content-Type: text/html; charset=utf-8');

// Check if pages/rider.php has the activation modal
$riderPhpPath = __DIR__ . '/../pages/rider.php';
$riderPhpContent = file_get_contents($riderPhpPath);

$hasActivateModal = strpos($riderPhpContent, 'activateModal') !== false;
$hasCanActivateProfile = strpos($riderPhpContent, 'canActivateProfile') !== false;
$hasSendActivationEmail = strpos($riderPhpContent, 'sendActivationEmail') !== false;

$fileModified = date('Y-m-d H:i:s', filemtime($riderPhpPath));
$fileSize = filesize($riderPhpPath);

echo "<h1>Rider.php Diagnostic</h1>";

echo "<h2>File Info:</h2>";
echo "Path: " . $riderPhpPath . "<br>";
echo "Modified: " . $fileModified . "<br>";
echo "Size: " . number_format($fileSize) . " bytes<br>";

echo "<h2>Feature Check:</h2>";
echo "✓ Contains 'activateModal': " . ($hasActivateModal ? '✅ YES' : '❌ NO') . "<br>";
echo "✓ Contains 'canActivateProfile': " . ($hasCanActivateProfile ? '✅ YES' : '❌ NO') . "<br>";
echo "✓ Contains 'sendActivationEmail': " . ($hasSendActivationEmail ? '✅ YES' : '❌ NO') . "<br>";

echo "<h2>Expected:</h2>";
echo "All three should be YES for activation feature to work.<br>";

if (!$hasActivateModal || !$hasCanActivateProfile || !$hasSendActivationEmail) {
    echo "<br><strong style='color: red;'>❌ PROBLEM: pages/rider.php is outdated!</strong><br>";
    echo "You need to upload the latest version from Git.";
} else {
    echo "<br><strong style='color: green;'>✅ File looks good!</strong><br>";
    echo "If button still doesn't show, check PHP opcache.";
}

// Check opcache
echo "<h2>PHP Cache:</h2>";
if (function_exists('opcache_get_status')) {
    $status = opcache_get_status();
    echo "OPcache enabled: " . ($status['opcache_enabled'] ? 'YES' : 'NO') . "<br>";
    if ($status['opcache_enabled']) {
        echo "<a href='/admin/clear-cache.php'>Clear Cache</a>";
    }
} else {
    echo "OPcache not available<br>";
}
?>
