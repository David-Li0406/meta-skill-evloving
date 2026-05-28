<?php
/**
 * Visa Riders Table Structure - Web Version
 * Kör i webbläsaren: https://thehub.gravityseries.se/show_riders_web.php
 */

// Ladda .env
function loadEnv($path) {
    if (!file_exists($path)) {
        die("Error: .env file not found at $path");
    }
    
    $lines = file($path, FILE_IGNORE_NEW_LINES | FILE_SKIP_EMPTY_LINES);
    $env = [];
    
    foreach ($lines as $line) {
        if (strpos(trim($line), '#') === 0) continue;
        if (strpos($line, '=') === false) continue;
        
        list($key, $value) = explode('=', $line, 2);
        $env[trim($key)] = trim($value, '"\'');
    }
    
    return $env;
}

$env = loadEnv(__DIR__ . '/.env');

// Anslut till databasen
try {
    $pdo = new PDO(
        "mysql:host=" . $env['DB_HOST'] . ";dbname=" . $env['DB_NAME'] . ";charset=utf8mb4",
        $env['DB_USER'],
        $env['DB_PASS'],
        [
            PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION,
            PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC,
            PDO::ATTR_EMULATE_PREPARES => false
        ]
    );
} catch (PDOException $e) {
    die("Connection failed: " . $e->getMessage());
}

?>
<!DOCTYPE html>
<html lang="sv">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Riders Table Structure</title>
    <style>
        body {
            font-family: 'Inter', -apple-system, sans-serif;
            max-width: 1400px;
            margin: 40px auto;
            padding: 20px;
            background: #f5f5f5;
        }
        .container {
            background: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        h1 {
            color: #171717;
            border-bottom: 3px solid #61CE70;
            padding-bottom: 10px;
        }
        h2 {
            color: #171717;
            margin-top: 30px;
        }
        .stats {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin: 20px 0;
        }
        .stat-card {
            background: #f0f9ff;
            border-left: 4px solid #004a98;
            padding: 20px;
            border-radius: 5px;
        }
        .stat-number {
            font-size: 32px;
            font-weight: 700;
            color: #171717;
        }
        .stat-label {
            color: #7A7A7A;
            font-size: 14px;
            margin-top: 5px;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
            background: white;
        }
        th {
            background: #171717;
            color: #61CE70;
            padding: 12px;
            text-align: left;
            font-weight: 600;
        }
        td {
            padding: 10px 12px;
            border-bottom: 1px solid #e0e0e0;
        }
        tr:hover {
            background: #f9f9f9;
        }
        .license-col {
            background: #fff7ed;
        }
        code {
            background: #1e1e1e;
            color: #61CE70;
            padding: 2px 6px;
            border-radius: 3px;
            font-size: 13px;
        }
        .example-data {
            background: #fafafa;
            padding: 15px;
            border-radius: 5px;
            margin: 10px 0;
            max-height: 400px;
            overflow-y: auto;
        }
        .field-row {
            padding: 8px 0;
            border-bottom: 1px solid #e0e0e0;
            display: grid;
            grid-template-columns: 200px 1fr;
            gap: 20px;
        }
        .field-row:last-child {
            border-bottom: none;
        }
        .field-name {
            font-weight: 600;
            color: #004a98;
        }
        .field-value {
            font-family: 'Courier New', monospace;
            color: #171717;
        }
        .warning {
            background: #fef2f2;
            border-left: 4px solid #ef4444;
            padding: 15px;
            margin: 20px 0;
            border-radius: 5px;
        }
        .success {
            background: #f0fdf4;
            border-left: 4px solid #61CE70;
            padding: 15px;
            margin: 20px 0;
            border-radius: 5px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🗄️ Riders Table Structure</h1>
        
        <?php
        // Hämta statistik
        try {
            $stmt = $pdo->query("SELECT COUNT(*) as total FROM riders");
            $totalCount = $stmt->fetch()['total'];
            
            $stmt = $pdo->query("SELECT COUNT(*) as total FROM riders WHERE uci_id IS NOT NULL AND uci_id != ''");
            $uciCount = $stmt->fetch()['total'];
            
            $stmt = $pdo->query("SELECT COUNT(*) as total FROM riders WHERE uci_id IS NULL OR uci_id = ''");
            $noUciCount = $stmt->fetch()['total'];
            
            echo "<div class='stats'>";
            echo "<div class='stat-card'>";
            echo "<div class='stat-number'>$totalCount</div>";
            echo "<div class='stat-label'>Total Riders</div>";
            echo "</div>";
            
            echo "<div class='stat-card'>";
            echo "<div class='stat-number'>$uciCount</div>";
            echo "<div class='stat-label'>Riders med UCI ID</div>";
            echo "</div>";
            
            echo "<div class='stat-card'>";
            echo "<div class='stat-number'>$noUciCount</div>";
            echo "<div class='stat-label'>Riders utan UCI ID</div>";
            echo "</div>";
            echo "</div>";
            
            // Visa kolumner
            echo "<h2>📋 Table Columns</h2>";
            $stmt = $pdo->query("DESCRIBE riders");
            $columns = $stmt->fetchAll();
            
            echo "<table>";
            echo "<thead><tr><th>Field</th><th>Type</th><th>Null</th><th>Key</th><th>Default</th><th>Extra</th></tr></thead>";
            echo "<tbody>";
            
            foreach ($columns as $col) {
                $isLicense = (stripos($col['Field'], 'license') !== false || stripos($col['Field'], 'licens') !== false);
                $rowClass = $isLicense ? 'license-col' : '';
                
                echo "<tr class='$rowClass'>";
                echo "<td><code>" . htmlspecialchars($col['Field']) . "</code></td>";
                echo "<td>" . htmlspecialchars($col['Type']) . "</td>";
                echo "<td>" . htmlspecialchars($col['Null']) . "</td>";
                echo "<td>" . htmlspecialchars($col['Key']) . "</td>";
                echo "<td>" . htmlspecialchars($col['Default'] ?? 'NULL') . "</td>";
                echo "<td>" . htmlspecialchars($col['Extra']) . "</td>";
                echo "</tr>";
            }
            
            echo "</tbody></table>";
            
            // Kolla om license-kolumner finns
            $licenseColumns = array_filter($columns, function($col) {
                return stripos($col['Field'], 'license') !== false || stripos($col['Field'], 'licens') !== false;
            });
            
            if (empty($licenseColumns)) {
                echo "<div class='warning'>";
                echo "<strong>⚠️ Inga license-kolumner hittades!</strong><br>";
                echo "Du behöver troligen lägga till kolumner för att lagra licensinformation, t.ex:<br>";
                echo "<code>license_2026</code>, <code>license_type</code>, <code>license_valid</code>, <code>license_updated</code>";
                echo "</div>";
            } else {
                echo "<div class='success'>";
                echo "<strong>✓ License-kolumner hittade:</strong><br>";
                foreach ($licenseColumns as $col) {
                    echo "<code>" . htmlspecialchars($col['Field']) . "</code> ";
                }
                echo "</div>";
            }
            
            // Visa exempel
            echo "<h2>📄 Example Rider Data</h2>";
            $stmt = $pdo->query("SELECT * FROM riders WHERE uci_id IS NOT NULL AND uci_id != '' LIMIT 1");
            $example = $stmt->fetch();
            
            if ($example) {
                echo "<div class='example-data'>";
                foreach ($example as $key => $value) {
                    if (!is_numeric($key)) {
                        $isLicense = (stripos($key, 'license') !== false || stripos($key, 'licens') !== false);
                        $highlightClass = $isLicense ? 'license-col' : '';
                        
                        echo "<div class='field-row $highlightClass'>";
                        echo "<div class='field-name'>$key:</div>";
                        echo "<div class='field-value'>" . htmlspecialchars($value ?? 'NULL') . "</div>";
                        echo "</div>";
                    }
                }
                echo "</div>";
            } else {
                echo "<div class='warning'>Inga riders med UCI ID hittades för att visa exempel.</div>";
            }
            
        } catch (Exception $e) {
            echo "<div class='warning'><strong>Error:</strong> " . htmlspecialchars($e->getMessage()) . "</div>";
        }
        ?>
        
        <div style="margin-top: 40px; padding-top: 20px; border-top: 2px solid #e0e0e0;">
            <h3>📋 Next Steps</h3>
            <ol>
                <li>Notera vilka license-kolumner du har (markerade i orange ovan)</li>
                <li>Kör <code>test_scf_api_web.php</code> för att se vilka fält SCF API returnerar</li>
                <li>Berätta för Claude hur fälten ska mappas mellan API och databas</li>
            </ol>
        </div>
    </div>
</body>
</html>
