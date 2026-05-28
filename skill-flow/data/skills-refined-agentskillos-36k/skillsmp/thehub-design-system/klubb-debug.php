<?php
// MINIMAL TEST - klubb-debug.php
error_reporting(E_ALL);
ini_set('display_errors', 1);

echo "<h1>KLUBB DEBUG - Om du ser detta fungerar filen!</h1>";
echo "<p>Tid: " . date('Y-m-d H:i:s') . "</p>";

// Test databas
require_once __DIR__ . '/hub-config.php';
$db = hub_db();
echo "<p>Databas OK!</p>";

// Hämta serier
$series = $db->query("SELECT id, name, year FROM series WHERE active = 1 ORDER BY year DESC LIMIT 5")->fetchAll(PDO::FETCH_ASSOC);
echo "<h2>Serier:</h2><ul>";
foreach ($series as $s) {
    echo "<li>{$s['name']} ({$s['year']}) - ID: {$s['id']}</li>";
}
echo "</ul>";

// Test klubbdata för första serien
if (!empty($series)) {
    $sid = $series[0]['id'];
    echo "<h2>Klubbdata för {$series[0]['name']}:</h2>";

    $data = $db->prepare("
        SELECT COUNT(*) as results, COUNT(DISTINCT rd.club_id) as clubs
        FROM results r
        JOIN riders rd ON r.cyclist_id = rd.id
        JOIN events e ON r.event_id = e.id
        WHERE e.series_id = ? AND r.points > 0 AND rd.club_id IS NOT NULL
    ");
    $data->execute([$sid]);
    $row = $data->fetch(PDO::FETCH_ASSOC);
    echo "<p>Resultat med klubb: {$row['results']} från {$row['clubs']} klubbar</p>";
}
?>
