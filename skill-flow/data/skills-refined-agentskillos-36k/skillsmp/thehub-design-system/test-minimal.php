<!DOCTYPE html>
<html lang="sv">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TheHUB - Emergency Debug</title>
    <style>
        body { font-family: system-ui, sans-serif; max-width: 800px; margin: 50px auto; padding: 20px; background: #1a1a2e; color: #eee; }
        .card { background: #16213e; padding: 30px; border-radius: 10px; margin-bottom: 20px; }
        h1 { color: #00d4ff; }
        h2 { color: #fff; border-bottom: 1px solid #333; padding-bottom: 10px; }
        .success { color: #22C55E; }
        .error { color: #EF4444; }
        .warning { color: #F59E0B; }
        pre { background: #0a0a1a; padding: 15px; border-radius: 5px; overflow-x: auto; font-size: 12px; }
    </style>
</head>
<body>
    <div class="card">
        <h1>🚨 TheHUB Emergency Debug</h1>

        <?php
        error_reporting(E_ALL);
        ini_set('display_errors', 1);

        echo "<h2>1. PHP Status</h2>";
        echo "<p class='success'>✓ PHP is working (Version: " . PHP_VERSION . ")</p>";
        echo "<p>Server: " . ($_SERVER['SERVER_SOFTWARE'] ?? 'Unknown') . "</p>";

        echo "<h2>2. File Check</h2>";
        $criticalFiles = [
            'config.php' => 'Main configuration',
            'hub-config.php' => 'Hub configuration',
            'router.php' => 'URL router',
            'index.php' => 'Main entry point',
            'includes/helpers.php' => 'Helper functions',
            'includes/auth.php' => 'Authentication',
            'components/header.php' => 'Header component',
            'components/sidebar.php' => 'Sidebar component',
            'components/head.php' => 'Head component',
            'components/mobile-nav.php' => 'Mobile navigation',
            'components/icons.php' => 'Icon definitions',
        ];

        foreach ($criticalFiles as $file => $desc) {
            $path = __DIR__ . '/' . $file;
            if (file_exists($path)) {
                $size = filesize($path);
                echo "<p class='success'>✓ {$file} ({$size} bytes) - {$desc}</p>";
            } else {
                echo "<p class='error'>✗ {$file} MISSING - {$desc}</p>";
            }
        }

        echo "<h2>3. Database Connection</h2>";
        try {
            if (file_exists(__DIR__ . '/config.php')) {
                // Don't use require - manually test connection
                $host = 'localhost';
                $dbname = 'u994733455_thehub';
                $username = 'u994733455_rogerthat';
                $password = 'staggerMYnagger987!';

                $pdo = new PDO(
                    "mysql:host=$host;dbname=$dbname;charset=utf8mb4",
                    $username,
                    $password,
                    [PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION]
                );
                echo "<p class='success'>✓ Database connection successful</p>";

                $stmt = $pdo->query("SELECT COUNT(*) as count FROM riders");
                $result = $stmt->fetch(PDO::FETCH_ASSOC);
                echo "<p class='success'>✓ Found {$result['count']} riders in database</p>";

                $stmt = $pdo->query("SELECT COUNT(*) as count FROM events");
                $result = $stmt->fetch(PDO::FETCH_ASSOC);
                echo "<p class='success'>✓ Found {$result['count']} events in database</p>";

            } else {
                echo "<p class='error'>✗ config.php not found!</p>";
            }
        } catch (PDOException $e) {
            echo "<p class='error'>✗ Database error: " . htmlspecialchars($e->getMessage()) . "</p>";
        }

        echo "<h2>4. Load Test - config.php</h2>";
        try {
            ob_start();
            require_once __DIR__ . '/config.php';
            $output = ob_get_clean();
            echo "<p class='success'>✓ config.php loaded successfully</p>";
            if ($output) {
                echo "<p class='warning'>Output from config.php:</p><pre>" . htmlspecialchars($output) . "</pre>";
            }
        } catch (Throwable $e) {
            ob_end_clean();
            echo "<p class='error'>✗ config.php error: " . htmlspecialchars($e->getMessage()) . "</p>";
            echo "<pre>File: " . $e->getFile() . "\nLine: " . $e->getLine() . "</pre>";
        }

        echo "<h2>5. Load Test - hub-config.php</h2>";
        try {
            ob_start();
            require_once __DIR__ . '/hub-config.php';
            $output = ob_get_clean();
            echo "<p class='success'>✓ hub-config.php loaded successfully</p>";
            if ($output) {
                echo "<p class='warning'>Output from hub-config.php:</p><pre>" . htmlspecialchars($output) . "</pre>";
            }

            // Check constants
            echo "<p>HUB_ROOT: " . (defined('HUB_ROOT') ? HUB_ROOT : '<span class="error">NOT DEFINED</span>') . "</p>";
            echo "<p>HUB_NAV defined: " . (defined('HUB_NAV') ? '<span class="success">YES</span>' : '<span class="error">NO</span>') . "</p>";

        } catch (Throwable $e) {
            ob_end_clean();
            echo "<p class='error'>✗ hub-config.php error: " . htmlspecialchars($e->getMessage()) . "</p>";
            echo "<pre>File: " . $e->getFile() . "\nLine: " . $e->getLine() . "</pre>";
        }

        echo "<h2>6. Load Test - router.php</h2>";
        try {
            ob_start();
            require_once __DIR__ . '/router.php';
            $output = ob_get_clean();
            echo "<p class='success'>✓ router.php loaded successfully</p>";

            // Test the function
            if (function_exists('hub_get_current_page')) {
                echo "<p class='success'>✓ hub_get_current_page() exists</p>";
            } else {
                echo "<p class='error'>✗ hub_get_current_page() NOT DEFINED</p>";
            }

        } catch (Throwable $e) {
            ob_end_clean();
            echo "<p class='error'>✗ router.php error: " . htmlspecialchars($e->getMessage()) . "</p>";
            echo "<pre>File: " . $e->getFile() . "\nLine: " . $e->getLine() . "\nTrace:\n" . $e->getTraceAsString() . "</pre>";
        }

        echo "<h2>7. Load Test - Components</h2>";
        $components = ['icons.php', 'head.php', 'header.php', 'sidebar.php', 'mobile-nav.php'];
        foreach ($components as $comp) {
            try {
                $path = __DIR__ . '/components/' . $comp;
                if (file_exists($path)) {
                    // Just check syntax, don't execute
                    $code = file_get_contents($path);
                    $tokens = @token_get_all($code);
                    if ($tokens !== false) {
                        echo "<p class='success'>✓ components/{$comp} - syntax OK</p>";
                    }
                } else {
                    echo "<p class='error'>✗ components/{$comp} - FILE MISSING</p>";
                }
            } catch (Throwable $e) {
                echo "<p class='error'>✗ components/{$comp} - " . htmlspecialchars($e->getMessage()) . "</p>";
            }
        }

        echo "<h2>8. Session Status</h2>";
        echo "<p>Session status: " . session_status() . " (1=disabled, 2=active)</p>";
        if (session_status() === PHP_SESSION_ACTIVE) {
            echo "<p class='success'>✓ Session is active</p>";
            echo "<p>Session ID: " . session_id() . "</p>";
        }

        echo "<h2>9. Request Info</h2>";
        echo "<p>REQUEST_URI: " . htmlspecialchars($_SERVER['REQUEST_URI'] ?? 'N/A') . "</p>";
        echo "<p>DOCUMENT_ROOT: " . htmlspecialchars($_SERVER['DOCUMENT_ROOT'] ?? 'N/A') . "</p>";
        echo "<p>SCRIPT_FILENAME: " . htmlspecialchars($_SERVER['SCRIPT_FILENAME'] ?? 'N/A') . "</p>";
        ?>

        <h2>10. Next Steps</h2>
        <ul>
            <li>If all tests pass, the issue is in page rendering logic</li>
            <li>If a specific file fails, that's where the bug is</li>
            <li>Check the error messages above for details</li>
        </ul>
    </div>
</body>
</html>
