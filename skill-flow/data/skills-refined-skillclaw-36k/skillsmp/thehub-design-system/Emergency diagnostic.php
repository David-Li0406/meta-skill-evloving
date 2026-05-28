<?php
/**
 * EMERGENCY DIAGNOSTIC SCRIPT
 * Upload this to your server root and access it via browser
 * URL: https://thehub.gravityseries.se/EMERGENCY-DIAGNOSTIC.php
 */

error_reporting(E_ALL);
ini_set('display_errors', 1);

echo "<h1>🚨 EMERGENCY DIAGNOSTIC</h1>";
echo "<style>body{font-family:monospace;background:#1a1a1a;color:#0f0;padding:20px;}h2{color:#ff0;border-bottom:2px solid #ff0;}</style>";

// 1. PHP VERSION
echo "<h2>1. PHP VERSION</h2>";
echo "PHP Version: " . phpversion() . "<br>";
echo "Date: " . date('Y-m-d H:i:s') . "<br><br>";

// 2. DATABASE CONNECTION
echo "<h2>2. DATABASE CONNECTION</h2>";
try {
    require_once __DIR__ . '/config.php';
    echo "✅ config.php loaded<br>";
    
    if (isset($db)) {
        echo "✅ \$db object exists<br>";
        
        // Test query
        $test = $db->getValue("SELECT COUNT(*) FROM riders");
        echo "✅ Database connection works - {$test} riders found<br>";
    } else {
        echo "❌ \$db object not found<br>";
    }
} catch (Exception $e) {
    echo "❌ ERROR: " . $e->getMessage() . "<br>";
}
echo "<br>";

// 3. CRITICAL FILES
echo "<h2>3. CRITICAL FILES</h2>";
$files = [
    'config.php',
    'includes/db.php',
    'includes/ranking_functions.php',
    'pages/rider.php',
    'pages/ranking.php'
];

foreach ($files as $file) {
    if (file_exists(__DIR__ . '/' . $file)) {
        $size = filesize(__DIR__ . '/' . $file);
        $modified = date('Y-m-d H:i:s', filemtime(__DIR__ . '/' . $file));
        echo "✅ {$file} (Size: {$size} bytes, Modified: {$modified})<br>";
    } else {
        echo "❌ {$file} - MISSING!<br>";
    }
}
echo "<br>";

// 4. DATABASE TABLES
echo "<h2>4. DATABASE TABLES</h2>";
try {
    $tables = $db->getAll("SHOW TABLES");
    echo "Found " . count($tables) . " tables:<br>";
    
    $critical = ['riders', 'results', 'events', 'ranking_points', 'ranking_snapshots'];
    
    foreach ($critical as $table) {
        $exists = false;
        foreach ($tables as $t) {
            if (in_array($table, $t)) {
                $exists = true;
                break;
            }
        }
        
        if ($exists) {
            $count = $db->getValue("SELECT COUNT(*) FROM {$table}");
            echo "✅ {$table} ({$count} rows)<br>";
        } else {
            echo "❌ {$table} - MISSING!<br>";
        }
    }
} catch (Exception $e) {
    echo "❌ ERROR checking tables: " . $e->getMessage() . "<br>";
}
echo "<br>";

// 5. RANKING SYSTEM
echo "<h2>5. RANKING SYSTEM</h2>";
try {
    // Check if ranking_functions exists
    if (file_exists(__DIR__ . '/includes/ranking_functions.php')) {
        require_once __DIR__ . '/includes/ranking_functions.php';
        echo "✅ ranking_functions.php loaded<br>";
        
        // Check for critical functions
        $functions = ['calculate_rider_ranking', 'get_ranking_data', 'update_ranking'];
        foreach ($functions as $func) {
            if (function_exists($func)) {
                echo "✅ Function {$func}() exists<br>";
            } else {
                echo "⚠️ Function {$func}() NOT FOUND<br>";
            }
        }
    } else {
        echo "❌ ranking_functions.php NOT FOUND<br>";
    }
    
    // Test ranking query
    $rankingTest = $db->getRow("
        SELECT * FROM ranking_points 
        WHERE rider_id = 7701 
        LIMIT 1
    ");
    
    if ($rankingTest) {
        echo "✅ Can query ranking_points table<br>";
        echo "Sample data: <pre>" . print_r($rankingTest, true) . "</pre>";
    } else {
        echo "⚠️ No ranking data found for rider 7701<br>";
    }
    
} catch (Exception $e) {
    echo "❌ ERROR: " . $e->getMessage() . "<br>";
}
echo "<br>";

// 6. TEST RIDER PAGE
echo "<h2>6. TEST RIDER PAGE</h2>";
try {
    $rider = $db->getRow("SELECT * FROM riders WHERE id = 7701");
    
    if ($rider) {
        echo "✅ Rider 7701 exists: " . $rider['name'] . "<br>";
        
        // Check results
        $results = $db->getAll("
            SELECT COUNT(*) as count 
            FROM results 
            WHERE rider_id = 7701
        ");
        echo "✅ Rider has " . $results[0]['count'] . " results<br>";
    } else {
        echo "❌ Rider 7701 NOT FOUND<br>";
    }
} catch (Exception $e) {
    echo "❌ ERROR: " . $e->getMessage() . "<br>";
}
echo "<br>";

// 7. RECENT ERRORS
echo "<h2>7. RECENT PHP ERRORS</h2>";
$error_log = __DIR__ . '/error_log';
if (file_exists($error_log)) {
    echo "✅ error_log found<br>";
    $errors = file($error_log);
    $recent = array_slice($errors, -20); // Last 20 lines
    echo "<pre style='background:#000;color:#f00;padding:10px;overflow:auto;max-height:300px;'>";
    echo implode("", $recent);
    echo "</pre>";
} else {
    echo "⚠️ No error_log file found<br>";
}
echo "<br>";

// 8. PERMISSIONS
echo "<h2>8. FILE PERMISSIONS</h2>";
$dirs = ['uploads', 'uploads/media', 'includes', 'pages'];
foreach ($dirs as $dir) {
    if (is_dir(__DIR__ . '/' . $dir)) {
        $perms = substr(sprintf('%o', fileperms(__DIR__ . '/' . $dir)), -4);
        $writable = is_writable(__DIR__ . '/' . $dir) ? '✅ Writable' : '❌ Not writable';
        echo "{$dir}: {$perms} - {$writable}<br>";
    } else {
        echo "❌ {$dir} - DOES NOT EXIST<br>";
    }
}

echo "<br><hr>";
echo "<h2>🎯 NEXT STEPS:</h2>";
echo "<ol>";
echo "<li>Screenshot this entire page</li>";
echo "<li>Share the output with Claude</li>";
echo "<li>Delete this file after diagnosis (security risk)</li>";
echo "</ol>";
?>Emergency diagnostic 
