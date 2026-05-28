<?php
/**
 * SCF License API Test Script
 * Testar API-anrop och visar vad som returneras
 */

// Ladda .env
function loadEnv($path) {
    if (!file_exists($path)) {
        die("Error: .env file not found at $path\n");
    }
    
    $lines = file($path, FILE_IGNORE_NEW_LINES | FILE_SKIP_EMPTY_LINES);
    $env = [];
    
    foreach ($lines as $line) {
        if (strpos(trim($line), '#') === 0) continue;
        list($key, $value) = explode('=', $line, 2);
        $env[trim($key)] = trim($value, '"\'');
    }
    
    return $env;
}

$env = loadEnv(__DIR__ . '/.env');
$API_KEY = $env['SCF_LICENSE_API_KEY'] ?? null;

if (!$API_KEY) {
    die("Error: SCF_LICENSE_API_KEY not found in .env\n");
}

echo "=== SCF License API Test ===\n\n";

// Test 1: Hämta via UCI ID
echo "Test 1: Lookup by UCI ID\n";
echo "Enter UCI ID to test (or press enter to skip): ";
$uciId = trim(fgets(STDIN));

if (!empty($uciId)) {
    $url = "https://licens.scf.se/api/1.0/ucilicenselookup?year=2026&uciids=" . urlencode($uciId);
    
    $ch = curl_init();
    curl_setopt($ch, CURLOPT_URL, $url);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_HTTPHEADER, [
        'Authorization: Bearer ' . $API_KEY
    ]);
    
    $response = curl_exec($ch);
    $httpCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
    curl_close($ch);
    
    echo "\nHTTP Status: $httpCode\n";
    echo "Response:\n";
    echo $response . "\n\n";
    
    $data = json_decode($response, true);
    if ($data) {
        echo "Parsed data:\n";
        print_r($data);
    }
}

// Test 2: Hämta via namn
echo "\n\nTest 2: Lookup by Name\n";
echo "Enter first name (or press enter to skip): ";
$firstName = trim(fgets(STDIN));

if (!empty($firstName)) {
    echo "Enter last name: ";
    $lastName = trim(fgets(STDIN));
    echo "Enter gender (M/F): ";
    $gender = trim(fgets(STDIN));
    
    $params = [
        'year' => 2026,
        'firstname' => $firstName,
        'lastname' => $lastName,
        'gender' => $gender
    ];
    
    $url = "https://licens.scf.se/api/1.0/licenselookup?" . http_build_query($params);
    
    $ch = curl_init();
    curl_setopt($ch, CURLOPT_URL, $url);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_HTTPHEADER, [
        'Authorization: Bearer ' . $API_KEY
    ]);
    
    $response = curl_exec($ch);
    $httpCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
    curl_close($ch);
    
    echo "\nHTTP Status: $httpCode\n";
    echo "Response:\n";
    echo $response . "\n\n";
    
    $data = json_decode($response, true);
    if ($data) {
        echo "Parsed data:\n";
        print_r($data);
    }
}

echo "\n=== Test Complete ===\n";
?>
