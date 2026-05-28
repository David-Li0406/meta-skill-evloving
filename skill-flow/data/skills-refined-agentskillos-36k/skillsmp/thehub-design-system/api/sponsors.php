<?php
/**
 * DEBUG VERSION - sponsors.php
 * Run this instead of sponsors.php to see where it fails
 */

// Enable all errors
error_reporting(E_ALL);
ini_set('display_errors', 1);
ini_set('log_errors', 1);

echo "<!DOCTYPE html><html><head><title>Sponsors Debug</title></head><body>";
echo "<h1>Sponsors.php Debug</h1>";
echo "<pre>";

// Step 1: Check config
echo "STEP 1: Loading config.php...\n";
try {
    require_once __DIR__ . '/../config.php';
    echo "✓ config.php loaded successfully\n";
    echo "  - ROOT_PATH: " . (defined('ROOT_PATH') ? ROOT_PATH : 'NOT DEFINED') . "\n";
    echo "  - DB connected: " . (isset($pdo) ? 'YES' : 'NO') . "\n";
} catch (Exception $e) {
    echo "✗ FAILED: " . $e->getMessage() . "\n";
    die("</pre></body></html>");
}

// Step 2: Check auth
echo "\nSTEP 2: Checking authentication...\n";
try {
    if (!function_exists('require_admin')) {
        echo "✗ require_admin() function NOT FOUND!\n";
        echo "  Looking in includes/auth.php...\n";
        if (file_exists(__DIR__ . '/../includes/auth.php')) {
            echo "  - auth.php EXISTS\n";
            require_once __DIR__ . '/../includes/auth.php';
            echo "  - auth.php loaded\n";
        } else {
            echo "  - auth.php MISSING!\n";
        }
    }
    
    if (function_exists('require_admin')) {
        echo "✓ require_admin() function found\n";
        // Don't actually call it yet
        echo "  (Not calling require_admin() in debug mode)\n";
    } else {
        echo "✗ require_admin() still not found after loading auth.php!\n";
    }
} catch (Exception $e) {
    echo "✗ FAILED: " . $e->getMessage() . "\n";
}

// Step 3: Check sponsor functions
echo "\nSTEP 3: Loading sponsor-functions.php...\n";
try {
    if (file_exists(__DIR__ . '/../includes/sponsor-functions.php')) {
        require_once __DIR__ . '/../includes/sponsor-functions.php';
        echo "✓ sponsor-functions.php loaded\n";
        echo "  - search_sponsors exists: " . (function_exists('search_sponsors') ? 'YES' : 'NO') . "\n";
    } else {
        echo "✗ sponsor-functions.php MISSING!\n";
    }
} catch (Exception $e) {
    echo "✗ FAILED: " . $e->getMessage() . "\n";
}

// Step 4: Check media functions
echo "\nSTEP 4: Loading media-functions.php...\n";
try {
    if (file_exists(__DIR__ . '/../includes/media-functions.php')) {
        require_once __DIR__ . '/../includes/media-functions.php';
        echo "✓ media-functions.php loaded\n";
    } else {
        echo "✗ media-functions.php MISSING!\n";
    }
} catch (Exception $e) {
    echo "✗ FAILED: " . $e->getMessage() . "\n";
}

// Step 5: Check database
echo "\nSTEP 5: Testing database connection...\n";
try {
    global $pdo;
    if (!$pdo) {
        echo "✗ \$pdo not set!\n";
    } else {
        echo "✓ \$pdo is set\n";
        $stmt = $pdo->query("SELECT COUNT(*) as cnt FROM sponsors");
        $result = $stmt->fetch();
        echo "  - Sponsors in database: " . $result['cnt'] . "\n";
    }
} catch (Exception $e) {
    echo "✗ Database query FAILED: " . $e->getMessage() . "\n";
}

// Step 6: Check layout
echo "\nSTEP 6: Checking unified-layout.php...\n";
try {
    if (file_exists(__DIR__ . '/components/unified-layout.php')) {
        echo "✓ unified-layout.php EXISTS\n";
        // Check for errors in layout file
        $layoutContent = file_get_contents(__DIR__ . '/components/unified-layout.php');
        if (strpos($layoutContent, '<?php') !== false) {
            echo "  - File contains PHP code\n";
        }
    } else {
        echo "✗ unified-layout.php MISSING!\n";
    }
} catch (Exception $e) {
    echo "✗ FAILED: " . $e->getMessage() . "\n";
}

// Step 7: Check user role
echo "\nSTEP 7: Checking user role...\n";
try {
    if (function_exists('isRole')) {
        echo "✓ isRole() function exists\n";
        if (function_exists('getCurrentAdmin')) {
            $admin = getCurrentAdmin();
            echo "  - Current admin: " . ($admin ? $admin['username'] : 'NOT LOGGED IN') . "\n";
            if ($admin) {
                echo "  - Is promotor: " . (isRole('promotor') ? 'YES' : 'NO') . "\n";
                echo "  - Is admin: " . (isRole('admin') ? 'YES' : 'NO') . "\n";
            }
        }
    } else {
        echo "✗ isRole() function not found\n";
    }
} catch (Exception $e) {
    echo "✗ FAILED: " . $e->getMessage() . "\n";
}

echo "\n===========================================\n";
echo "DEBUG COMPLETE\n";
echo "===========================================\n";

// Try to load actual sponsors page
echo "\n\nAttempting to load sponsors.php...\n";
try {
    ob_start();
    include __DIR__ . '/sponsors.php';
    $output = ob_get_clean();
    echo "✓ sponsors.php loaded successfully!\n";
    echo "\nOutput preview (first 500 chars):\n";
    echo substr(strip_tags($output), 0, 500) . "...\n";
} catch (Exception $e) {
    echo "✗ sponsors.php FAILED TO LOAD:\n";
    echo "Error: " . $e->getMessage() . "\n";
    echo "File: " . $e->getFile() . "\n";
    echo "Line: " . $e->getLine() . "\n";
    echo "\nStack trace:\n";
    echo $e->getTraceAsString() . "\n";
}

echo "</pre></body></html>";
?>
