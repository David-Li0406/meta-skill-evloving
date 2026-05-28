<?php
/**
 * SCF License API - Enkel Datatest
 * Bara visar vad API:et returnerar
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
$API_KEY = $env['SCF_API_KEY'] ?? null;
$API_URL = $env['SCF_API_URL'] ?? 'https://licens.scf.se/api/1.0';

if (!$API_KEY) {
    die("❌ Error: SCF_API_KEY not found in .env");
}

// Testa med några vanliga svenska cyklisters namn
$testCases = [
    ['firstname' => 'Erik', 'lastname' => 'Andersson', 'gender' => 'M'],
    ['firstname' => 'Anna', 'lastname' => 'Larsson', 'gender' => 'F'],
    ['firstname' => 'Johan', 'lastname' => 'Svensson', 'gender' => 'M'],
];

?>
<!DOCTYPE html>
<html lang="sv">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SCF License Data Test</title>
    <style>
        body {
            font-family: 'Inter', -apple-system, sans-serif;
            max-width: 1200px;
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
        .info {
            background: #f0f9ff;
            border-left: 4px solid #004a98;
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
        .warning {
            background: #fef2f2;
            border-left: 4px solid #ef4444;
            padding: 15px;
            margin: 20px 0;
            border-radius: 5px;
        }
        pre {
            background: #1e1e1e;
            color: #d4d4d4;
            padding: 20px;
            border-radius: 5px;
            overflow-x: auto;
            font-size: 13px;
            line-height: 1.5;
        }
        .test-result {
            margin: 20px 0;
            padding: 20px;
            border: 2px solid #e0e0e0;
            border-radius: 5px;
        }
        .test-result.success {
            border-color: #61CE70;
            background: #f0fdf4;
        }
        .field-highlight {
            background: #fffbeb;
            padding: 2px 6px;
            border-radius: 3px;
            font-family: 'Courier New', monospace;
            color: #171717;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin: 15px 0;
        }
        th {
            background: #171717;
            color: #61CE70;
            padding: 10px;
            text-align: left;
            font-size: 13px;
        }
        td {
            padding: 8px 10px;
            border-bottom: 1px solid #e0e0e0;
            font-size: 13px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🔍 SCF License API - Datatest</h1>
        
        <div class="info">
            <strong>Test:</strong> Hämtar några licenser från SCF för att se datastrukturen<br>
            <strong>API:</strong> <?php echo htmlspecialchars($API_URL); ?><br>
            <strong>Year:</strong> 2026
        </div>

        <?php
        $foundLicense = false;
        
        foreach ($testCases as $idx => $test) {
            $params = [
                'year' => 2026,
                'firstname' => $test['firstname'],
                'lastname' => $test['lastname'],
                'gender' => $test['gender']
            ];
            
            $url = "$API_URL/licenselookup?" . http_build_query($params);
            
            echo "<div class='test-result'>";
            echo "<h3>Test " . ($idx + 1) . ": {$test['firstname']} {$test['lastname']} ({$test['gender']})</h3>";
            echo "<p><small>URL: <code>" . htmlspecialchars($url) . "</code></small></p>";
            
            $ch = curl_init();
            curl_setopt($ch, CURLOPT_URL, $url);
            curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
            curl_setopt($ch, CURLOPT_HTTPHEADER, [
                'Authorization: Bearer ' . $API_KEY
            ]);
            
            $response = curl_exec($ch);
            $httpCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
            curl_close($ch);
            
            if ($httpCode !== 200) {
                echo "<div class='warning'>HTTP $httpCode</div>";
                continue;
            }
            
            $data = json_decode($response, true);
            
            if (json_last_error() !== JSON_ERROR_NONE) {
                echo "<div class='warning'>JSON parse error</div>";
                continue;
            }
            
            $licenses = $data['results'] ?? [];
            
            if (!empty($licenses)) {
                $foundLicense = true;
                echo "<div class='success'>✓ Hittade " . count($licenses) . " licens(er)!</div>";
                
                foreach ($licenses as $licIdx => $license) {
                    echo "<h4>Licens #" . ($licIdx + 1) . ":</h4>";
                    echo "<table>";
                    echo "<thead><tr><th>Fält</th><th>Värde</th></tr></thead>";
                    echo "<tbody>";
                    
                    foreach ($license as $field => $value) {
                        echo "<tr>";
                        echo "<td><strong>" . htmlspecialchars($field) . "</strong></td>";
                        echo "<td><span class='field-highlight'>" . htmlspecialchars($value) . "</span></td>";
                        echo "</tr>";
                    }
                    
                    echo "</tbody></table>";
                }
                
                echo "</div>";
                break; // Sluta söka när vi hittat en
            } else {
                echo "<p>Ingen licens hittad för detta namn.</p>";
                echo "</div>";
            }
        }
        
        if (!$foundLicense) {
            echo "<div class='warning'>";
            echo "<h3>⚠️ Inga licenser hittades i testerna</h3>";
            echo "<p>Testa med ett riktigt namn från din databas:</p>";
            echo "<form method='GET'>";
            echo "<p><input type='text' name='fn' placeholder='Förnamn' style='padding: 8px; margin: 5px;'></p>";
            echo "<p><input type='text' name='ln' placeholder='Efternamn' style='padding: 8px; margin: 5px;'></p>";
            echo "<p><select name='g' style='padding: 8px; margin: 5px;'>";
            echo "<option value='M'>Man</option>";
            echo "<option value='F'>Kvinna</option>";
            echo "</select></p>";
            echo "<p><button type='submit' style='padding: 10px 20px; background: #61CE70; color: white; border: none; border-radius: 5px; cursor: pointer;'>Sök</button></p>";
            echo "</form>";
            echo "</div>";
            
            // Om form submitted
            if (isset($_GET['fn']) && isset($_GET['ln']) && isset($_GET['g'])) {
                $params = [
                    'year' => 2026,
                    'firstname' => $_GET['fn'],
                    'lastname' => $_GET['ln'],
                    'gender' => $_GET['g']
                ];
                
                $url = "$API_URL/licenselookup?" . http_build_query($params);
                
                echo "<div class='test-result'>";
                echo "<h3>Sökresultat för {$_GET['fn']} {$_GET['ln']}</h3>";
                echo "<p><small>URL: <code>" . htmlspecialchars($url) . "</code></small></p>";
                
                $ch = curl_init();
                curl_setopt($ch, CURLOPT_URL, $url);
                curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
                curl_setopt($ch, CURLOPT_HTTPHEADER, [
                    'Authorization: Bearer ' . $API_KEY
                ]);
                
                $response = curl_exec($ch);
                $httpCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
                curl_close($ch);
                
                echo "<h4>Raw Response (HTTP $httpCode):</h4>";
                echo "<pre>" . htmlspecialchars($response) . "</pre>";
                
                $data = json_decode($response, true);
                if ($data && !empty($data['results'])) {
                    echo "<div class='success'>✓ Licens hittad!</div>";
                    
                    foreach ($data['results'] as $license) {
                        echo "<table>";
                        echo "<thead><tr><th>Fält</th><th>Värde</th></tr></thead>";
                        echo "<tbody>";
                        
                        foreach ($license as $field => $value) {
                            echo "<tr>";
                            echo "<td><strong>" . htmlspecialchars($field) . "</strong></td>";
                            echo "<td><span class='field-highlight'>" . htmlspecialchars($value) . "</span></td>";
                            echo "</tr>";
                        }
                        
                        echo "</tbody></table>";
                    }
                }
                echo "</div>";
            }
        } else {
            echo "<div class='success'>";
            echo "<h3>✅ API fungerar!</h3>";
            echo "<p>Vi kan hämta licensdata från SCF. Nu behöver vi:</p>";
            echo "<ol>";
            echo "<li>Kolla din riders-tabell struktur (kör show_riders_web.php)</li>";
            echo "<li>Mappa fälten från API:et till dina databas-kolumner</li>";
            echo "<li>Bygg sync-skriptet</li>";
            echo "</ol>";
            echo "</div>";
        }
        ?>
    </div>
</body>
</html>
