<?php
/**
 * Debug file to test import-results-preview dependencies
 */
error_reporting(E_ALL);
ini_set('display_errors', '1');
ini_set('memory_limit', '256M');
set_time_limit(60);

// Register shutdown function to catch fatal errors
register_shutdown_function(function() {
    $error = error_get_last();
    if ($error !== null && in_array($error['type'], [E_ERROR, E_PARSE, E_CORE_ERROR, E_COMPILE_ERROR])) {
        echo "<br><br><strong style='color:red'>FATAL ERROR:</strong><br>";
        echo "Type: " . $error['type'] . "<br>";
        echo "Message: " . htmlspecialchars($error['message']) . "<br>";
        echo "File: " . htmlspecialchars($error['file']) . "<br>";
        echo "Line: " . $error['line'] . "<br>";
    }
});

echo "Step 1: Loading config.php...<br>";
flush();
require_once __DIR__ . '/../config.php';
echo "OK<br>";

echo "Step 2: Loading import-history.php...<br>";
flush();
require_once __DIR__ . '/../includes/import-history.php';
echo "OK<br>";

echo "Step 3: Loading class-calculations.php...<br>";
flush();
require_once __DIR__ . '/../includes/class-calculations.php';
echo "OK<br>";

echo "Step 4: Loading point-calculations.php...<br>";
flush();
require_once __DIR__ . '/../includes/point-calculations.php';
echo "OK<br>";

echo "Step 5: Loading import-functions.php...<br>";
flush();
require_once __DIR__ . '/../includes/import-functions.php';
echo "OK<br>";

echo "Step 6: Loading series-points.php...<br>";
flush();
try {
    require_once __DIR__ . '/../includes/series-points.php';
    echo "OK<br>";
} catch (Throwable $e) {
    echo "<br><strong style='color:red'>ERROR in series-points.php:</strong><br>";
    echo "Message: " . htmlspecialchars($e->getMessage()) . "<br>";
    echo "File: " . htmlspecialchars($e->getFile()) . "<br>";
    echo "Line: " . $e->getLine() . "<br>";
    die();
}

echo "Step 7: Loading rebuild-rider-stats.php...<br>";
flush();
try {
    require_once __DIR__ . '/../includes/rebuild-rider-stats.php';
    echo "OK<br>";
} catch (Throwable $e) {
    echo "<br><strong style='color:red'>ERROR in rebuild-rider-stats.php:</strong><br>";
    echo "Message: " . htmlspecialchars($e->getMessage()) . "<br>";
    echo "File: " . htmlspecialchars($e->getFile()) . "<br>";
    echo "Line: " . $e->getLine() . "<br>";
    die();
}

echo "Step 8: Checking require_admin...<br>";
flush();
require_admin();
echo "OK - Admin authenticated<br>";

echo "Step 9: Testing getDB()...<br>";
flush();
$db = getDB();
echo "OK - DB type: " . get_class($db) . "<br>";

echo "Step 10: Testing database query...<br>";
flush();
$test = $db->getAll("SELECT COUNT(*) as cnt FROM events");
echo "OK - Events count: " . $test[0]['cnt'] . "<br>";

echo "Step 11: Checking session variables...<br>";
flush();
echo "import_preview_file: " . ($_SESSION['import_preview_file'] ?? 'NOT SET') . "<br>";
echo "import_selected_event: " . ($_SESSION['import_selected_event'] ?? 'NOT SET') . "<br>";

echo "<br><strong style='color:green'>All tests passed!</strong>";
