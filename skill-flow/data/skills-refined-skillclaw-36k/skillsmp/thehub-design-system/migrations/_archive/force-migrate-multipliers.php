<?php
/**
 * Force migrate field multipliers to new 15-item scale
 */
error_reporting(E_ALL);
ini_set('display_errors', 1);

require_once __DIR__ . '/../config.php';
require_once __DIR__ . '/../includes/ranking_functions.php';

$db = getDB();

echo "<h1>Force Migrate Field Multipliers</h1>";

// Check current state
echo "<h2>Current State</h2>";
$current = $db->getRow("SELECT * FROM ranking_settings WHERE setting_key = 'field_multipliers'");

if ($current) {
    echo "<p><strong>Current raw value:</strong></p>";
    echo "<pre>" . htmlspecialchars($current['setting_value']) . "</pre>";

    $decoded = json_decode($current['setting_value'], true);
    echo "<p><strong>Number of items:</strong> " . count($decoded) . "</p>";

    if (count($decoded) > 15) {
        echo "<p style='color: red;'>❌ Old scale detected (" . count($decoded) . " items)</p>";
    } else {
        echo "<p style='color: green;'>✅ New scale (" . count($decoded) . " items)</p>";
    }
}

// Get the defaults
echo "<h2>Default 15-item Scale</h2>";
$defaults = getDefaultFieldMultipliers();
echo "<table border='1' cellpadding='5'>";
echo "<tr><th>Position</th><th>Multiplier</th><th>Percentage</th></tr>";
foreach ($defaults as $pos => $mult) {
    echo "<tr>";
    echo "<td>" . ($pos === 15 ? "15+" : $pos) . "</td>";
    echo "<td>" . number_format($mult, 2) . "</td>";
    echo "<td>" . ($mult * 100) . "%</td>";
    echo "</tr>";
}
echo "</table>";

// Force save
echo "<h2>Forcing Migration</h2>";
try {
    saveFieldMultipliers($db, $defaults);
    echo "<p style='color: green; font-weight: bold;'>✅ Successfully saved new 15-item scale!</p>";
} catch (Exception $e) {
    echo "<p style='color: red; font-weight: bold;'>❌ Error: " . htmlspecialchars($e->getMessage()) . "</p>";
}

// Verify
echo "<h2>Verification</h2>";
$after = $db->getRow("SELECT * FROM ranking_settings WHERE setting_key = 'field_multipliers'");

if ($after) {
    echo "<p><strong>New raw value:</strong></p>";
    echo "<pre>" . htmlspecialchars($after['setting_value']) . "</pre>";

    $decoded = json_decode($after['setting_value'], true);
    echo "<p><strong>Number of items:</strong> " . count($decoded) . "</p>";

    if (count($decoded) === 15) {
        echo "<p style='color: green; font-weight: bold;'>✅ Migration successful! Now showing 15 items.</p>";
    } else {
        echo "<p style='color: red; font-weight: bold;'>❌ Still showing " . count($decoded) . " items</p>";
    }

    // Show first few values
    echo "<h3>Values:</h3>";
    echo "<ul>";
    foreach (array_slice($decoded, 0, 5, true) as $key => $val) {
        echo "<li>Position $key: $val</li>";
    }
    echo "<li>...</li>";
    echo "<li>Position 15: {$decoded[15]}</li>";
    echo "</ul>";
}

echo "<p><strong>✅ Done! Now reload the admin ranking page.</strong></p>";
echo "<p><a href='/admin/ranking.php'>Go to Ranking Admin →</a></p>";
