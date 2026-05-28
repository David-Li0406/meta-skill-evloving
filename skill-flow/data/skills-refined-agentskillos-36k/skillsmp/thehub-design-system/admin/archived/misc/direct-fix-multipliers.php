<?php
/**
 * Direct database update to fix multipliers
 */
error_reporting(E_ALL);
ini_set('display_errors', 1);

require_once __DIR__ . '/../config.php';

$db = getDB();

echo "<h1>Direct Multiplier Fix</h1>";

// The correct 15-item scale
$newMultipliers = [
    1 => 0.75, 2 => 0.77, 3 => 0.79, 4 => 0.81, 5 => 0.83,
    6 => 0.85, 7 => 0.87, 8 => 0.89, 9 => 0.91, 10 => 0.93,
    11 => 0.95, 12 => 0.97, 13 => 0.98, 14 => 0.99, 15 => 1.00
];

$json = json_encode($newMultipliers);

echo "<h2>New Multipliers JSON:</h2>";
echo "<pre>" . htmlspecialchars($json) . "</pre>";

// Direct UPDATE query (simpler than INSERT ON DUPLICATE)
try {
    echo "<p>Updating database...</p>";
    flush();

    $result = $db->query("
        UPDATE ranking_settings
        SET setting_value = ?, updated_at = NOW()
        WHERE setting_key = 'field_multipliers'
    ", [$json]);

    echo "<p style='color: green; font-weight: bold; font-size: 1.2em;'>✅ SUCCESS!</p>";
    echo "<p>Affected rows: $result</p>";

} catch (Exception $e) {
    echo "<p style='color: red; font-weight: bold;'>❌ ERROR:</p>";
    echo "<pre>" . htmlspecialchars($e->getMessage()) . "</pre>";
}

// Verify it worked
echo "<h2>Verification</h2>";
$verify = $db->getRow("SELECT setting_value FROM ranking_settings WHERE setting_key = 'field_multipliers'");

if ($verify) {
    $decoded = json_decode($verify['setting_value'], true);
    echo "<p><strong>Items in database:</strong> " . count($decoded) . "</p>";

    if (count($decoded) === 15) {
        echo "<p style='color: green; font-size: 1.2em;'>✅ Correct! 15 items saved.</p>";

        echo "<table border='1' cellpadding='5'>";
        echo "<tr><th>Pos</th><th>Value</th><th>Expected</th><th>Match?</th></tr>";
        foreach ($newMultipliers as $pos => $expected) {
            $actual = $decoded[$pos] ?? 'MISSING';
            $match = ($actual == $expected) ? '✅' : '❌';
            echo "<tr>";
            echo "<td>" . ($pos === 15 ? "15+" : $pos) . "</td>";
            echo "<td>$actual</td>";
            echo "<td>$expected</td>";
            echo "<td>$match</td>";
            echo "</tr>";
        }
        echo "</table>";
    } else {
        echo "<p style='color: red;'>Still has " . count($decoded) . " items</p>";
    }
}

echo "<hr>";
echo "<h2 style='color: green;'>✅ All Done!</h2>";
echo "<p><a href='/admin/ranking.php' style='font-size: 1.2em;'>→ Go to Ranking Admin and verify the multipliers show correctly</a></p>";
