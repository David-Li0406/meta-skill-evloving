<?php
/**
 * TheHUB V1.0 - Search API DEBUG PAGE
 * Shows detailed debug information for search queries
 */

// Enable ALL error reporting
error_reporting(E_ALL);
ini_set('display_errors', '1');
ini_set('display_startup_errors', '1');

// Catch fatal errors
register_shutdown_function(function() {
    $error = error_get_last();
    if ($error && in_array($error['type'], [E_ERROR, E_PARSE, E_CORE_ERROR, E_COMPILE_ERROR])) {
        echo '<div class="debug-box error">';
        echo '<strong>❌ FATAL PHP ERROR!</strong><br>';
        echo '<strong>Type:</strong> ' . $error['type'] . '<br>';
        echo '<strong>Message:</strong> ' . htmlspecialchars($error['message']) . '<br>';
        echo '<strong>File:</strong> ' . htmlspecialchars($error['file']) . ':' . $error['line'] . '<br>';
        echo '</div>';
    }
});

$configPath = dirname(__DIR__) . '/config.php';
echo '<div class="debug-box">Config path: ' . htmlspecialchars($configPath) . '<br>';
echo 'Config exists: ' . (file_exists($configPath) ? 'YES' : 'NO') . '<br>';
echo 'Loading config.php...</div>';
flush();

try {
    require_once $configPath;
    echo '<div class="debug-box success">Config loaded successfully!</div>';
    flush();
} catch (Exception $e) {
    die('<div class="debug-box error"><strong>❌ Config load failed!</strong><br>' . htmlspecialchars($e->getMessage()) . '</div>');
}

header('Content-Type: text/html; charset=utf-8');

$query = trim($_GET['q'] ?? '');
$type = $_GET['type'] ?? 'all';
$limit = min(intval($_GET['limit'] ?? 10), 20);

?>
<!DOCTYPE html>
<html lang="sv">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Search Debug - TheHUB</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background: #f5f5f5;
        }
        h1 { color: #2563EB; }
        h2 {
            color: #1e40af;
            margin-top: 30px;
            padding: 10px;
            background: #dbeafe;
            border-left: 4px solid #2563EB;
        }
        .debug-box {
            background: white;
            padding: 20px;
            margin: 15px 0;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .success {
            border-left: 4px solid #10b981;
            background: #d1fae5;
        }
        .error {
            border-left: 4px solid #ef4444;
            background: #fee2e2;
        }
        .warning {
            border-left: 4px solid #f59e0b;
            background: #fef3c7;
        }
        pre {
            background: #1e293b;
            color: #e2e8f0;
            padding: 15px;
            border-radius: 5px;
            overflow-x: auto;
            font-size: 13px;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin: 10px 0;
        }
        th, td {
            text-align: left;
            padding: 8px;
            border-bottom: 1px solid #e5e7eb;
        }
        th {
            background: #f3f4f6;
            font-weight: 600;
        }
        .input-form {
            background: white;
            padding: 20px;
            border-radius: 8px;
            margin-bottom: 20px;
        }
        input, select {
            padding: 10px;
            font-size: 14px;
            border: 1px solid #d1d5db;
            border-radius: 5px;
            margin-right: 10px;
        }
        button {
            padding: 10px 20px;
            background: #2563EB;
            color: white;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-size: 14px;
        }
        button:hover {
            background: #1e40af;
        }
    </style>
</head>
<body>
    <h1>🔍 Search Debug Page - TheHUB</h1>

    <div class="input-form">
        <form method="GET">
            <input type="text" name="q" value="<?= htmlspecialchars($query) ?>" placeholder="Sökfråga..." required>
            <select name="type">
                <option value="all" <?= $type === 'all' ? 'selected' : '' ?>>All</option>
                <option value="riders" <?= $type === 'riders' ? 'selected' : '' ?>>Riders</option>
                <option value="clubs" <?= $type === 'clubs' ? 'selected' : '' ?>>Clubs</option>
            </select>
            <input type="number" name="limit" value="<?= $limit ?>" min="1" max="20" style="width: 80px;">
            <button type="submit">🔍 Sök</button>
        </form>
    </div>

    <?php if (strlen($query) >= 2): ?>

    <h2>📊 Input Parameters</h2>
    <div class="debug-box">
        <table>
            <tr><th>Parameter</th><th>Value</th></tr>
            <tr><td>Query</td><td><strong><?= htmlspecialchars($query) ?></strong></td></tr>
            <tr><td>Type</td><td><?= htmlspecialchars($type) ?></td></tr>
            <tr><td>Limit</td><td><?= $limit ?></td></tr>
            <tr><td>Query Length</td><td><?= strlen($query) ?> characters</td></tr>
        </table>
    </div>

    <h2>🔌 Database Connection</h2>
    <?php
    $pdo = null;
    try {
        echo '<div class="debug-box">';
        echo 'Checking $GLOBALS[\'pdo\'] state...<br>';
        echo 'isset($GLOBALS[\'pdo\']): ' . (isset($GLOBALS['pdo']) ? 'YES' : 'NO') . '<br>';
        if (isset($GLOBALS['pdo'])) {
            echo 'is PDO instance: ' . ($GLOBALS['pdo'] instanceof PDO ? 'YES' : 'NO') . '<br>';
            echo 'PDO type: ' . gettype($GLOBALS['pdo']) . '<br>';
        }
        echo 'Attempting to connect via hub_db()...<br>';
        flush();

        $pdo = hub_db();

        echo '</div>';
        echo '<div class="debug-box success">';
        echo '<strong>✅ Database connected successfully!</strong><br>';
        echo 'Driver: ' . $pdo->getAttribute(PDO::ATTR_DRIVER_NAME) . '<br>';
        echo 'Server: ' . $pdo->getAttribute(PDO::ATTR_SERVER_INFO) . '<br>';
        echo '</div>';
    } catch (Exception $e) {
        echo '<div class="debug-box error">';
        echo '<strong>❌ Database connection failed!</strong><br>';
        echo 'Error: ' . htmlspecialchars($e->getMessage()) . '<br>';
        echo 'Type: ' . get_class($e) . '<br>';
        echo 'Code: ' . $e->getCode() . '<br>';
        echo '</div>';
        exit;
    } catch (Throwable $e) {
        echo '<div class="debug-box error">';
        echo '<strong>❌ Fatal error during database connection!</strong><br>';
        echo 'Error: ' . htmlspecialchars($e->getMessage()) . '<br>';
        echo 'Type: ' . get_class($e) . '<br>';
        echo '</div>';
        exit;
    }

    if (!$pdo) {
        echo '<div class="debug-box error">❌ PDO is null after connection attempt!</div>';
        exit;
    }
    ?>

    <h2>👥 Riders Search</h2>
    <?php
    echo '<div class="debug-box">Starting riders search section...</div>';
    flush();

    if ($type === 'all' || $type === 'riders') {
        try {
            echo '<div class="debug-box">Preparing riders query...</div>';
            flush();
            $sql = "
                SELECT r.id, r.firstname, r.lastname, c.name as club_name
                FROM riders r
                LEFT JOIN clubs c ON r.club_id = c.id
                WHERE CONCAT(r.firstname, ' ', r.lastname) LIKE ?
                   OR r.firstname LIKE ?
                   OR r.lastname LIKE ?
                ORDER BY
                    CASE
                        WHEN CONCAT(r.firstname, ' ', r.lastname) LIKE ? THEN 1
                        WHEN r.firstname LIKE ? THEN 2
                        ELSE 3
                    END,
                    r.lastname, r.firstname
                LIMIT ?
            ";

            echo '<div class="debug-box">';
            echo '<h3>SQL Query:</h3>';
            echo '<pre>' . htmlspecialchars($sql) . '</pre>';
            echo '</div>';

            $searchPattern = "%{$query}%";
            $startPattern = "{$query}%";

            echo '<div class="debug-box">';
            echo '<h3>Parameters:</h3>';
            echo '<pre>';
            echo "searchPattern: " . htmlspecialchars($searchPattern) . "\n";
            echo "startPattern: " . htmlspecialchars($startPattern) . "\n";
            echo "limit: " . $limit;
            echo '</pre>';
            echo '</div>';

            $stmt = $pdo->prepare($sql);
            $stmt->execute([$searchPattern, $searchPattern, $searchPattern, $startPattern, $startPattern, $limit]);

            $results = $stmt->fetchAll(PDO::FETCH_ASSOC);

            echo '<div class="debug-box success">';
            echo '<strong>✅ Query executed successfully!</strong><br>';
            echo 'Found ' . count($results) . ' riders<br>';
            echo '</div>';

            if (!empty($results)) {
                echo '<div class="debug-box">';
                echo '<h3>Results:</h3>';
                echo '<table>';
                echo '<tr><th>ID</th><th>First Name</th><th>Last Name</th><th>Club</th></tr>';
                foreach ($results as $row) {
                    echo '<tr>';
                    echo '<td>' . htmlspecialchars($row['id']) . '</td>';
                    echo '<td>' . htmlspecialchars($row['firstname']) . '</td>';
                    echo '<td>' . htmlspecialchars($row['lastname']) . '</td>';
                    echo '<td>' . htmlspecialchars($row['club_name'] ?? '-') . '</td>';
                    echo '</tr>';
                }
                echo '</table>';
                echo '</div>';
            }

        } catch (Exception $e) {
            echo '<div class="debug-box error">';
            echo '<strong>❌ Riders search failed!</strong><br>';
            echo '<strong>Error:</strong> ' . htmlspecialchars($e->getMessage()) . '<br>';
            echo '<strong>Code:</strong> ' . $e->getCode() . '<br>';
            echo '<strong>File:</strong> ' . $e->getFile() . ':' . $e->getLine() . '<br>';
            echo '<h3>Stack Trace:</h3>';
            echo '<pre>' . htmlspecialchars($e->getTraceAsString()) . '</pre>';
            echo '</div>';
        }
    } else {
        echo '<div class="debug-box warning">⏭️ Skipped (type filter)</div>';
    }
    ?>

    <h2>🛡️ Clubs Search</h2>
    <?php
    if ($type === 'all' || $type === 'clubs') {
        try {
            $remainingLimit = $limit - (isset($results) ? count($results) : 0);

            echo '<div class="debug-box">';
            echo '<strong>Remaining limit:</strong> ' . $remainingLimit . '<br>';
            echo '</div>';

            if ($remainingLimit > 0) {
                $sql = "
                    SELECT c.id, c.name, COUNT(r.id) as member_count
                    FROM clubs c
                    LEFT JOIN riders r ON c.id = r.club_id
                    WHERE c.name LIKE ?
                    GROUP BY c.id
                    ORDER BY
                        CASE WHEN c.name LIKE ? THEN 1 ELSE 2 END,
                        c.name
                    LIMIT ?
                ";

                echo '<div class="debug-box">';
                echo '<h3>SQL Query:</h3>';
                echo '<pre>' . htmlspecialchars($sql) . '</pre>';
                echo '</div>';

                $searchPattern = "%{$query}%";
                $startPattern = "{$query}%";

                echo '<div class="debug-box">';
                echo '<h3>Parameters:</h3>';
                echo '<pre>';
                echo "searchPattern: " . htmlspecialchars($searchPattern) . "\n";
                echo "startPattern: " . htmlspecialchars($startPattern) . "\n";
                echo "limit: " . $remainingLimit;
                echo '</pre>';
                echo '</div>';

                $stmt = $pdo->prepare($sql);
                $stmt->execute([$searchPattern, $startPattern, $remainingLimit]);

                $clubResults = $stmt->fetchAll(PDO::FETCH_ASSOC);

                echo '<div class="debug-box success">';
                echo '<strong>✅ Query executed successfully!</strong><br>';
                echo 'Found ' . count($clubResults) . ' clubs<br>';
                echo '</div>';

                if (!empty($clubResults)) {
                    echo '<div class="debug-box">';
                    echo '<h3>Results:</h3>';
                    echo '<table>';
                    echo '<tr><th>ID</th><th>Name</th><th>Members</th></tr>';
                    foreach ($clubResults as $row) {
                        echo '<tr>';
                        echo '<td>' . htmlspecialchars($row['id']) . '</td>';
                        echo '<td>' . htmlspecialchars($row['name']) . '</td>';
                        echo '<td>' . htmlspecialchars($row['member_count']) . '</td>';
                        echo '</tr>';
                    }
                    echo '</table>';
                    echo '</div>';
                }
            } else {
                echo '<div class="debug-box warning">⏭️ Skipped (limit reached)</div>';
            }

        } catch (Exception $e) {
            echo '<div class="debug-box error">';
            echo '<strong>❌ Clubs search failed!</strong><br>';
            echo '<strong>Error:</strong> ' . htmlspecialchars($e->getMessage()) . '<br>';
            echo '<strong>Code:</strong> ' . $e->getCode() . '<br>';
            echo '<strong>File:</strong> ' . $e->getFile() . ':' . $e->getLine() . '<br>';
            echo '<h3>Stack Trace:</h3>';
            echo '<pre>' . htmlspecialchars($e->getTraceAsString()) . '</pre>';
            echo '</div>';
        }
    } else {
        echo '<div class="debug-box warning">⏭️ Skipped (type filter)</div>';
    }
    ?>

    <?php else: ?>
    <div class="debug-box warning">
        <strong>⚠️ Query too short</strong><br>
        Please enter at least 2 characters to search.
    </div>
    <?php endif; ?>

</body>
</html>
