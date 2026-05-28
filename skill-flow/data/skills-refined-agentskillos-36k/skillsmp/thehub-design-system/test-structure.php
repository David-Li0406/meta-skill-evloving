<?php
error_reporting(E_ALL);
ini_set('display_errors', 1);

echo "<h1>File Structure</h1>";

$files = [
    'config.php',
    'hub-config.php',
    'router.php',
    'index.php',
    'includes/helpers.php',
    'includes/auth.php',
    'components/header.php',
    'components/sidebar.php',
    'components/head.php',
    'components/mobile-nav.php',
    'components/icons.php',
    'pages/welcome.php',
];

foreach ($files as $f) {
    $path = __DIR__ . '/' . $f;
    if (file_exists($path)) {
        echo "<p style='color:green'>✓ {$f} (" . filesize($path) . " bytes)</p>";
    } else {
        echo "<p style='color:red'>✗ {$f} MISSING</p>";
    }
}

echo "<h2>Directory</h2>";
echo "<pre>" . __DIR__ . "</pre>";
