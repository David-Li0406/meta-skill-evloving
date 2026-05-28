<?php
/**
 * Check ranking multipliers in database
 */
error_reporting(E_ALL);
ini_set('display_errors', 1);

require_once __DIR__ . '/../config.php';
require_once __DIR__ . '/../includes/ranking_functions.php';

$db = getDB();

echo "<h1>Ranking Multipliers Check</h1>";

// Check event_level_multipliers setting
echo "<h2>Event Level Multipliers (from database)</h2>";
$eventLevelSetting = $db->getRow("SELECT * FROM ranking_settings WHERE setting_key = 'event_level_multipliers'");

if ($eventLevelSetting) {
    echo "<p><strong>Raw value:</strong> <code>" . htmlspecialchars($eventLevelSetting['setting_value']) . "</code></p>";

    $decoded = json_decode($eventLevelSetting['setting_value'], true);
    if ($decoded) {
        echo "<table border='1' cellpadding='5'>";
        echo "<tr><th>Event Level</th><th>Multiplier</th></tr>";
        foreach ($decoded as $level => $mult) {
            $bgColor = $level === 'sportmotion' ? '#fed7d7' : '#c6f6d5';
            echo "<tr style='background: $bgColor;'>";
            echo "<td><strong>$level</strong></td>";
            echo "<td><strong>$mult</strong> (" . ($mult * 100) . "%)</td>";
            echo "</tr>";
        }
        echo "</table>";
    }

    echo "<p><strong>Updated at:</strong> {$eventLevelSetting['updated_at']}</p>";
} else {
    echo "<p style='color: red;'>❌ No event_level_multipliers found in database!</p>";
}

// Check what the function returns
echo "<h2>What getEventLevelMultipliers() returns</h2>";
$multipliers = getEventLevelMultipliers($db);
echo "<pre>";
print_r($multipliers);
echo "</pre>";

// Test actual calculation for Marie's result
echo "<h2>Test Calculation for Marie's Capital Enduro #4</h2>";

$marieResult = $db->getRow("
    SELECT r.*, e.name as event_name, e.event_level, e.date, c.name as class_name,
           riders.firstname, riders.lastname
    FROM results r
    JOIN events e ON r.event_id = e.id
    JOIN riders ON r.cyclist_id = riders.id
    LEFT JOIN classes c ON r.class_id = c.id
    WHERE r.event_id = 238
    AND riders.firstname LIKE '%Marie%'
    LIMIT 1
");

if ($marieResult) {
    echo "<p><strong>Event:</strong> {$marieResult['event_name']}</p>";
    echo "<p><strong>Date:</strong> {$marieResult['date']}</p>";
    echo "<p><strong>Rider:</strong> {$marieResult['firstname']} {$marieResult['lastname']}</p>";
    echo "<p><strong>Class:</strong> {$marieResult['class_name']}</p>";
    echo "<p><strong>Original Points:</strong> {$marieResult['points']}</p>";
    echo "<p><strong>Event Level:</strong> <code>{$marieResult['event_level']}</code></p>";

    // Calculate field size
    $fieldSize = $db->getOne("
        SELECT COUNT(*)
        FROM results
        WHERE event_id = ? AND class_id = ? AND status = 'finished'
    ", [$marieResult['event_id'], $marieResult['class_id']]);

    echo "<p><strong>Field Size:</strong> $fieldSize riders</p>";

    // Get multipliers
    $fieldMultipliers = getRankingFieldMultipliers($db);
    $fieldMult = getFieldMultiplier($fieldSize, $fieldMultipliers);

    $eventLevelMult = $multipliers[$marieResult['event_level']] ?? 1.00;

    echo "<h3>Calculation:</h3>";
    echo "<div style='background: #e3f2fd; padding: 15px; border-left: 4px solid #2196f3;'>";
    echo "<p>Original Points: <strong>{$marieResult['points']}</strong></p>";
    echo "<p>× Field Multiplier ($fieldSize riders): <strong>$fieldMult</strong> (" . ($fieldMult * 100) . "%)</p>";
    echo "<p>× Event Level ({$marieResult['event_level']}): <strong>$eventLevelMult</strong> (" . ($eventLevelMult * 100) . "%)</p>";

    $rankingPoints = $marieResult['points'] * $fieldMult * $eventLevelMult;
    echo "<hr>";
    echo "<p style='font-size: 1.2em;'>= <strong>" . number_format($rankingPoints, 1) . " ranking points</strong></p>";
    echo "</div>";

    // Now check what's in the actual ranking
    echo "<h3>What's in the actual ranking?</h3>";
    $riderData = calculateRankingData($db, 'ENDURO', false);

    foreach ($riderData as $data) {
        if ($data['rider_id'] == $marieResult['cyclist_id']) {
            echo "<p><strong>Total Ranking Points:</strong> " . number_format($data['total_points'], 1) . "</p>";
            echo "<p><strong>Events Count:</strong> {$data['events_count']}</p>";
            echo "<p><strong>Points (12 months):</strong> " . number_format($data['points_12'], 1) . "</p>";
            echo "<p><strong>Points (13-24 months):</strong> " . number_format($data['points_13_24'], 1) . "</p>";
            break;
        }
    }
}

echo "<p><a href='/admin/ranking.php'>← Back to Ranking Admin</a></p>";
