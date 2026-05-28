<?php
error_reporting(E_ALL);
ini_set('display_errors', 1);

echo "<h1>Database Test</h1>";

try {
    $pdo = new PDO(
        "mysql:host=localhost;dbname=u994733455_thehub;charset=utf8mb4",
        "u994733455_rogerthat",
        "staggerMYnagger987!",
        [PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION]
    );
    echo "<p style='color:green'>✓ Database connected!</p>";

    $stmt = $pdo->query("SELECT COUNT(*) as c FROM riders");
    $r = $stmt->fetch();
    echo "<p>Riders: {$r['c']}</p>";

} catch (Exception $e) {
    echo "<p style='color:red'>✗ Error: " . $e->getMessage() . "</p>";
}
