<?php
/**
 * Check which events have sportmotion level set
 */
error_reporting(E_ALL);
ini_set('display_errors', 1);

require_once __DIR__ . '/../config.php';

$db = getDB();

echo "<h1>Sportmotion Events Check</h1>";

// Check events marked as sportmotion
$sportmotionEvents = $db->getAll("
    SELECT id, name, date, event_level
    FROM events
    WHERE event_level = 'sportmotion'
    ORDER BY date DESC
    LIMIT 20
");

echo "<h2>Events marked as Sportmotion</h2>";
if (empty($sportmotionEvents)) {
    echo "<p style='color: red; font-weight: bold;'>❌ NO EVENTS are marked as sportmotion!</p>";
    echo "<p>This is why the 50% multiplier isn't working.</p>";
} else {
    echo "<table border='1' cellpadding='5'>";
    echo "<tr><th>ID</th><th>Namn</th><th>Datum</th><th>Event Level</th></tr>";
    foreach ($sportmotionEvents as $event) {
        echo "<tr>";
        echo "<td>{$event['id']}</td>";
        echo "<td>" . htmlspecialchars($event['name']) . "</td>";
        echo "<td>{$event['date']}</td>";
        echo "<td><strong>{$event['event_level']}</strong></td>";
        echo "</tr>";
    }
    echo "</table>";
}

// Check Capital Enduro #4 specifically
echo "<h2>Capital Enduro #4 - Väsjön (the event user mentioned)</h2>";
$capitalEvent = $db->getRow("
    SELECT id, name, date, event_level, discipline
    FROM events
    WHERE name LIKE '%Capital Enduro%4%'
    OR (name LIKE '%Capital%' AND name LIKE '%Väsjön%')
    ORDER BY date DESC
    LIMIT 1
");

if ($capitalEvent) {
    echo "<table border='1' cellpadding='5'>";
    echo "<tr><th>Field</th><th>Value</th></tr>";
    echo "<tr><td>ID</td><td>{$capitalEvent['id']}</td></tr>";
    echo "<tr><td>Namn</td><td>" . htmlspecialchars($capitalEvent['name']) . "</td></tr>";
    echo "<tr><td>Datum</td><td>{$capitalEvent['date']}</td></tr>";
    echo "<tr><td>Discipline</td><td>{$capitalEvent['discipline']}</td></tr>";
    echo "<tr><td><strong>Event Level</strong></td><td style='background: " .
        ($capitalEvent['event_level'] === 'sportmotion' ? '#c6f6d5' : '#fed7d7') .
        "; font-weight: bold;'>{$capitalEvent['event_level']}</td></tr>";
    echo "</table>";

    // Check Marie's result in this event
    echo "<h3>Marie's Result in this Event</h3>";
    $marieResult = $db->getRow("
        SELECT r.*, riders.firstname, riders.lastname, c.name as class_name
        FROM results r
        JOIN riders ON r.cyclist_id = riders.id
        LEFT JOIN classes c ON r.class_id = c.id
        WHERE r.event_id = ?
        AND riders.firstname LIKE '%Marie%'
        ORDER BY r.points DESC
        LIMIT 1
    ", [$capitalEvent['id']]);

    if ($marieResult) {
        echo "<p><strong>Rider:</strong> {$marieResult['firstname']} {$marieResult['lastname']}</p>";
        echo "<p><strong>Class:</strong> {$marieResult['class_name']}</p>";
        echo "<p><strong>Points:</strong> {$marieResult['points']}</p>";
        echo "<p><strong>Event Level:</strong> {$capitalEvent['event_level']}</p>";

        $expectedPoints = $marieResult['points'] * 0.77 * 0.50;
        echo "<p style='background: #e3f2fd; padding: 10px;'>";
        echo "<strong>Expected ranking points:</strong><br>";
        echo "Original: {$marieResult['points']}p<br>";
        echo "× Field multiplier (2 riders): 0.77<br>";
        echo "× Event level (sportmotion): 0.50<br>";
        echo "= <strong>" . number_format($expectedPoints, 1) . "p</strong>";
        echo "</p>";
    }
} else {
    echo "<p>Event not found</p>";
}

// Check all events and their levels
echo "<h2>All Recent Events (last 20)</h2>";
$allEvents = $db->getAll("
    SELECT id, name, date, event_level
    FROM events
    ORDER BY date DESC
    LIMIT 20
");

echo "<table border='1' cellpadding='5'>";
echo "<tr><th>ID</th><th>Namn</th><th>Datum</th><th>Event Level</th></tr>";
foreach ($allEvents as $event) {
    $bgColor = $event['event_level'] === 'sportmotion' ? '#c6f6d5' : '#fff';
    echo "<tr style='background: $bgColor;'>";
    echo "<td>{$event['id']}</td>";
    echo "<td>" . htmlspecialchars($event['name']) . "</td>";
    echo "<td>{$event['date']}</td>";
    echo "<td>{$event['event_level']}</td>";
    echo "</tr>";
}
echo "</table>";

echo "<p><a href='/admin/ranking.php'>← Back to Ranking Admin</a></p>";
