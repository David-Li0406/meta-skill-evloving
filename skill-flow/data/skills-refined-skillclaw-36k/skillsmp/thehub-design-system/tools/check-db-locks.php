<?php
/**
 * Check for database locks and running queries
 */
error_reporting(E_ALL);
ini_set('display_errors', 1);

require_once __DIR__ . '/../config.php';

$db = getDB();

echo "<h1>Database Lock Check</h1>";

// Check for running queries
echo "<h2>Running Processes</h2>";
try {
    $processes = $db->getAll("SHOW PROCESSLIST");

    echo "<table border='1' cellpadding='5'>";
    echo "<tr><th>ID</th><th>User</th><th>DB</th><th>Command</th><th>Time</th><th>State</th><th>Info</th></tr>";

    foreach ($processes as $proc) {
        $bgColor = '';
        if ($proc['Time'] > 5) $bgColor = '#fed7d7'; // Highlight long-running
        if ($proc['Command'] === 'Sleep') $bgColor = '#e0e0e0';

        echo "<tr style='background: $bgColor;'>";
        echo "<td>{$proc['Id']}</td>";
        echo "<td>{$proc['User']}</td>";
        echo "<td>{$proc['db']}</td>";
        echo "<td>{$proc['Command']}</td>";
        echo "<td><strong>{$proc['Time']}s</strong></td>";
        echo "<td>{$proc['State']}</td>";
        echo "<td style='max-width: 300px; overflow: hidden;'>" . htmlspecialchars(substr($proc['Info'] ?? '', 0, 200)) . "</td>";
        echo "</tr>";
    }
    echo "</table>";

} catch (Exception $e) {
    echo "<p style='color: red;'>Error: " . htmlspecialchars($e->getMessage()) . "</p>";
}

// Check table status
echo "<h2>Table Status</h2>";
try {
    $tables = $db->getAll("SHOW TABLE STATUS WHERE Name = 'ranking_settings'");

    if ($tables) {
        foreach ($tables as $table) {
            echo "<p><strong>Table:</strong> {$table['Name']}</p>";
            echo "<p><strong>Engine:</strong> {$table['Engine']}</p>";
            echo "<p><strong>Rows:</strong> {$table['Rows']}</p>";
            echo "<p><strong>Avg Row Length:</strong> {$table['Avg_row_length']}</p>";
            echo "<p><strong>Data Length:</strong> {$table['Data_length']}</p>";
        }
    }
} catch (Exception $e) {
    echo "<p style='color: red;'>Error: " . htmlspecialchars($e->getMessage()) . "</p>";
}

// Try a simple SELECT to see if we can read
echo "<h2>Can We Read?</h2>";
try {
    $result = $db->getRow("SELECT * FROM ranking_settings WHERE setting_key = 'field_multipliers'");
    if ($result) {
        echo "<p style='color: green;'>✅ Can read from ranking_settings</p>";
    }
} catch (Exception $e) {
    echo "<p style='color: red;'>❌ Cannot read: " . htmlspecialchars($e->getMessage()) . "</p>";
}

// Try a simple UPDATE with minimal data
echo "<h2>Can We Write?</h2>";
try {
    $testValue = '{"test":true,"timestamp":' . time() . '}';

    echo "<p>Attempting UPDATE on ranking_settings...</p>";
    flush();

    $result = $db->query("
        UPDATE ranking_settings
        SET description = CONCAT(description, '')
        WHERE setting_key = 'field_multipliers'
    ");

    echo "<p style='color: green;'>✅ Can write to ranking_settings! Affected rows: $result</p>";

} catch (Exception $e) {
    echo "<p style='color: red;'>❌ Cannot write: " . htmlspecialchars($e->getMessage()) . "</p>";
}

echo "<p><a href='/admin/ranking.php'>← Back</a></p>";
