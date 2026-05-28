<?php
require_once __DIR__ . '/../config.php';
require_admin();

$db = getDB();

echo "<!DOCTYPE html><html><head><meta charset='UTF-8'><title>Check Series Format</title>";
echo "<style>body{font-family:monospace;padding:20px;background:#f5f5f5;} .success{color:green;} .error{color:red;} .info{color:blue;} table{border-collapse:collapse;} td,th{border:1px solid #ccc;padding:8px;}</style>";
echo "</head><body>";
echo "<h1>Series Format Column Check</h1>";

try {
    // Check if column exists
    echo "<h2>1. Checking if 'format' column exists in series table:</h2>";
    $columns = $db->getAll("SHOW COLUMNS FROM series LIKE 'format'");

    if (empty($columns)) {
        echo "<p class='error'>✗ Column 'format' does NOT exist!</p>";
        echo "<p><strong>Solution:</strong> Run the migration: <a href='/admin/migrations/add_series_format.php'>Add Series Format Migration</a></p>";
    } else {
        echo "<p class='success'>✓ Column 'format' exists!</p>";
        echo "<table><tr><th>Field</th><th>Type</th><th>Null</th><th>Key</th><th>Default</th><th>Extra</th></tr>";
        foreach ($columns as $col) {
            echo "<tr>";
            echo "<td>" . htmlspecialchars($col['Field']) . "</td>";
            echo "<td>" . htmlspecialchars($col['Type']) . "</td>";
            echo "<td>" . htmlspecialchars($col['Null']) . "</td>";
            echo "<td>" . htmlspecialchars($col['Key']) . "</td>";
            echo "<td>" . htmlspecialchars($col['Default']) . "</td>";
            echo "<td>" . htmlspecialchars($col['Extra']) . "</td>";
            echo "</tr>";
        }
        echo "</table>";
    }

    // Show current series data
    echo "<h2>2. Current Series Data:</h2>";
    $series = $db->getAll("SELECT id, name, format FROM series ORDER BY id DESC LIMIT 10");

    if (empty($series)) {
        echo "<p class='info'>No series found in database.</p>";
    } else {
        echo "<table><tr><th>ID</th><th>Name</th><th>Format</th></tr>";
        foreach ($series as $s) {
            echo "<tr>";
            echo "<td>" . htmlspecialchars($s['id']) . "</td>";
            echo "<td>" . htmlspecialchars($s['name']) . "</td>";
            echo "<td>" . htmlspecialchars($s['format'] ?? 'NULL') . "</td>";
            echo "</tr>";
        }
        echo "</table>";
    }

    // Test updating a series
    echo "<h2>3. Test Form (Update a series to Team format):</h2>";
    if (!empty($series)) {
        $testSeries = $series[0];
        echo "<form method='POST'>";
        echo csrf_field();
        echo "<input type='hidden' name='test_update' value='1'>";
        echo "<p>Test updating series: <strong>" . htmlspecialchars($testSeries['name']) . "</strong></p>";
        echo "<p>Current format: <strong>" . htmlspecialchars($testSeries['format'] ?? 'NULL') . "</strong></p>";
        echo "<label>New format: <select name='format'>";
        echo "<option value='Championship'>Championship</option>";
        echo "<option value='Team'>Team</option>";
        echo "</select></label><br><br>";
        echo "<button type='submit'>Test Update</button>";
        echo "</form>";

        // Handle test update
        if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['test_update'])) {
            checkCsrf();
            $newFormat = $_POST['format'] ?? 'Championship';

            echo "<h3>Attempting to update...</h3>";
            echo "<p>New format value from POST: <strong>" . htmlspecialchars($newFormat) . "</strong></p>";

            try {
                $db->update('series', ['format' => $newFormat], 'id = ?', [$testSeries['id']]);
                echo "<p class='success'>✓ Update executed successfully!</p>";

                // Verify update
                $updated = $db->getRow("SELECT format FROM series WHERE id = ?", [$testSeries['id']]);
                echo "<p>Format in database after update: <strong>" . htmlspecialchars($updated['format'] ?? 'NULL') . "</strong></p>";

                if ($updated['format'] === $newFormat) {
                    echo "<p class='success'>✓ Format was saved correctly!</p>";
                } else {
                    echo "<p class='error'>✗ Format was NOT saved correctly! Expected '{$newFormat}', got '" . htmlspecialchars($updated['format'] ?? 'NULL') . "'</p>";
                }
            } catch (Exception $e) {
                echo "<p class='error'>✗ Update failed: " . htmlspecialchars($e->getMessage()) . "</p>";
            }
        }
    }

} catch (Exception $e) {
    echo "<h2 class='error'>✗ Error!</h2>";
    echo "<p class='error'>" . htmlspecialchars($e->getMessage()) . "</p>";
}

echo "<hr><p><a href='/admin/series.php'>← Back to Series</a></p>";
echo "</body></html>";
