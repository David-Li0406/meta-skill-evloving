<?php
/**
 * Simple Migration: Add format column to series table
 * Minimal version with direct SQL
 */

error_reporting(E_ALL);
ini_set('display_errors', 1);
set_time_limit(120);

?>
<!DOCTYPE html>
<html>
<head>
    <meta charset='UTF-8'>
    <title>Simple Migration: Add Series Format</title>
    <style>
        body{font-family:monospace;padding:20px;background:#f5f5f5;}
        .success{color:green;font-weight:bold;}
        .error{color:red;font-weight:bold;}
        .info{color:blue;}
        pre{background:#fff;padding:10px;border:1px solid #ccc;overflow:auto;}
        .step{background:white;padding:15px;margin:10px 0;border-left:4px solid #667eea;}
    </style>
</head>
<body>
    <h1>Simple Migration: Add Format Column</h1>

<?php

try {
    // Load config
    require_once __DIR__ . '/../../config.php';

    echo "<div class='step'>";
    echo "<p class='info'>Step 1: Loading configuration...</p>";
    echo "<p>DB_HOST: " . htmlspecialchars(DB_HOST) . "</p>";
    echo "<p>DB_NAME: " . htmlspecialchars(DB_NAME) . "</p>";
    echo "<p class='success'>✓ Config loaded</p>";
    echo "</div>";
    flush();

    // Create direct PDO connection
    echo "<div class='step'>";
    echo "<p class='info'>Step 2: Creating database connection...</p>";

    $dsn = "mysql:host=" . DB_HOST . ";dbname=" . DB_NAME . ";charset=utf8mb4";
    $pdo = new PDO($dsn, DB_USER, DB_PASS, [
        PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION,
        PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC
    ]);

    echo "<p class='success'>✓ Connected to database</p>";
    echo "</div>";
    flush();

    // Check if column exists
    echo "<div class='step'>";
    echo "<p class='info'>Step 3: Checking if 'format' column exists...</p>";

    $stmt = $pdo->query("SHOW COLUMNS FROM series LIKE 'format'");
    $columns = $stmt->fetchAll();

    if (empty($columns)) {
        echo "<p class='info'>Column does not exist - will add it.</p>";
        echo "</div>";
        flush();

        // Add column
        echo "<div class='step'>";
        echo "<p class='info'>Step 4: Adding 'format' column...</p>";
        echo "<p>SQL: <code>ALTER TABLE series ADD COLUMN format VARCHAR(50) DEFAULT 'Championship' AFTER type</code></p>";
        flush();

        $sql = "ALTER TABLE series ADD COLUMN format VARCHAR(50) DEFAULT 'Championship' AFTER type";
        $result = $pdo->exec($sql);

        echo "<p class='success'>✓ ALTER TABLE executed (affected rows: " . var_export($result, true) . ")</p>";
        echo "</div>";
        flush();

        // Verify
        echo "<div class='step'>";
        echo "<p class='info'>Step 5: Verifying column was added...</p>";

        $stmt = $pdo->query("SHOW COLUMNS FROM series LIKE 'format'");
        $verify = $stmt->fetchAll();

        if (!empty($verify)) {
            echo "<p class='success'>✓ Column 'format' verified!</p>";
        } else {
            throw new Exception("Column was not added!");
        }
        echo "</div>";

    } else {
        echo "<p class='info'>Column 'format' already exists!</p>";
        echo "</div>";
    }

    // Success
    echo "<hr>";
    echo "<h2 class='success'>✅ Migration completed successfully!</h2>";
    echo "<p><a href='/admin/series.php' style='color:green;font-weight:bold;font-size:18px;'>→ Go to Series Page</a></p>";
    echo "<p><a href='/admin/check-series-format.php' style='color:blue;'>→ Verify with Diagnostic Tool</a></p>";

} catch (PDOException $e) {
    echo "<hr>";
    echo "<h2 class='error'>✗ Database Error!</h2>";
    echo "<p class='error'>Error: " . htmlspecialchars($e->getMessage()) . "</p>";
    echo "<p>Error Code: " . htmlspecialchars($e->getCode()) . "</p>";
    echo "<h3>Stack Trace:</h3>";
    echo "<pre>" . htmlspecialchars($e->getTraceAsString()) . "</pre>";

} catch (Exception $e) {
    echo "<hr>";
    echo "<h2 class='error'>✗ Error!</h2>";
    echo "<p class='error'>Error: " . htmlspecialchars($e->getMessage()) . "</p>";
    echo "<h3>Stack Trace:</h3>";
    echo "<pre>" . htmlspecialchars($e->getTraceAsString()) . "</pre>";
}

?>

</body>
</html>
