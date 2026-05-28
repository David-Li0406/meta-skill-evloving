<?php
/**
 * Test script to verify ranking_settings update works
 */
error_reporting(E_ALL);
ini_set('display_errors', 1);

require_once __DIR__ . '/../config.php';
require_once __DIR__ . '/../includes/ranking_functions.php';

$db = getDB();

echo "<h1>Testing Ranking Settings Save</h1>";

// Test 1: Read current value
echo "<h2>Test 1: Reading current last_calculation</h2>";
try {
    $current = $db->getRow("SELECT * FROM ranking_settings WHERE setting_key = 'last_calculation'");
    echo "<pre>";
    print_r($current);
    echo "</pre>";
} catch (Exception $e) {
    echo "<p style='color: red;'>Error: " . htmlspecialchars($e->getMessage()) . "</p>";
}

// Test 2: Try to update
echo "<h2>Test 2: Updating last_calculation</h2>";
try {
    $testData = json_encode([
        'date' => date('Y-m-d H:i:s'),
        'test' => 'This is a test update at ' . time()
    ]);

    echo "<p>Data to save: <code>" . htmlspecialchars($testData) . "</code></p>";

    $result = $db->query("
        INSERT INTO ranking_settings (setting_key, setting_value, description)
        VALUES ('last_calculation', ?, 'Timestamp of last ranking calculation')
        ON DUPLICATE KEY UPDATE setting_value = ?, updated_at = NOW()
    ", [$testData, $testData]);

    echo "<p style='color: green;'>✅ Query executed successfully</p>";
    echo "<p>Affected rows: " . $result . "</p>";
} catch (Exception $e) {
    echo "<p style='color: red;'>❌ Error: " . htmlspecialchars($e->getMessage()) . "</p>";
    echo "<pre>" . htmlspecialchars($e->getTraceAsString()) . "</pre>";
}

// Test 3: Read again to verify
echo "<h2>Test 3: Reading updated value</h2>";
try {
    $updated = $db->getRow("SELECT * FROM ranking_settings WHERE setting_key = 'last_calculation'");
    echo "<pre>";
    print_r($updated);
    echo "</pre>";

    if ($updated && $updated['setting_value']) {
        $decoded = json_decode($updated['setting_value'], true);
        echo "<p>Decoded value:</p>";
        echo "<pre>";
        print_r($decoded);
        echo "</pre>";
    }
} catch (Exception $e) {
    echo "<p style='color: red;'>Error: " . htmlspecialchars($e->getMessage()) . "</p>";
}

echo "<p><a href='/admin/ranking.php'>← Back to Ranking Admin</a></p>";
