<?php
/**
 * Clear PHP OpCache
 */

echo "<!DOCTYPE html><html><head><title>Clear Cache</title></head><body>";
echo "<h1>PHP Cache Clear</h1>";

// Clear opcache if available
if (function_exists('opcache_reset')) {
    if (opcache_reset()) {
        echo "<p style='color: green;'>✅ OpCache cleared successfully!</p>";
    } else {
        echo "<p style='color: red;'>❌ Failed to clear OpCache</p>";
    }
} else {
    echo "<p style='color: orange;'>⚠️ OpCache not available</p>";
}

// Clear realpath cache
clearstatcache(true);
echo "<p style='color: green;'>✅ Stat cache cleared</p>";

// Check rider.php for activation feature
$riderFile = __DIR__ . '/../pages/rider.php';
if (file_exists($riderFile)) {
    $modTime = filemtime($riderFile);
    echo "<p><strong>pages/rider.php modified:</strong> " . date('Y-m-d H:i:s', $modTime) . "</p>";

    // Check for activation feature
    $content = file_get_contents($riderFile);
    $hasActivateModal = strpos($content, 'activateModal') !== false;
    if ($hasActivateModal) {
        echo "<p style='color: green;'>✅ Activation feature found in file!</p>";
    } else {
        echo "<p style='color: red;'>❌ Activation feature NOT found in file!</p>";
        echo "<p>File might not be updated yet. Upload latest pages/rider.php</p>";
    }
} else {
    echo "<p style='color: red;'>❌ pages/rider.php not found!</p>";
}

echo "<p><a href='/admin/check-rider-version.php'>→ Check File Versions</a></p>";
echo "<p><a href='/rider/23988'>→ Test Rider Page</a></p>";
echo "</body></html>";
?>
