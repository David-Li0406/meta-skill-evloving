<?php
/**
 * DEBUG: Test merge-logiken och visa resultat/event-data
 */
require_once __DIR__ . '/../config.php';
require_admin();

?>
<!DOCTYPE html>
<html>
<head>
    <title>DEBUG: Merge & Event-data</title>
    <style>
        body { font-family: Arial; margin: 20px; }
        table { border-collapse: collapse; width: 100%; margin-bottom: 30px; }
        th, td { border: 1px solid #ddd; padding: 10px; text-align: left; font-size: 12px; }
        th { background-color: #f2f2f2; }
        h2 { margin-top: 30px; color: #333; }
        .debug-box { background-color: #e7f3ff; border-left: 3px solid #0066cc; padding: 10px; margin: 10px 0; }
        .error { background-color: #ffe7e7; border-left: 3px solid #cc0000; padding: 10px; margin: 10px 0; }
        pre { background-color: #f5f5f5; padding: 10px; overflow-x: auto; font-size: 11px; }
    </style>
</head>
<body>
    <h1>DEBUG: Merge-logik & Event-data för dubbletter</h1>
    
    <?php
    try {
        $db = getDB();
        
        // Hitta Milton-dubletterna
        $milton = $db->getAll("
            SELECT id, firstname, lastname, license_number
            FROM riders
            WHERE (firstname LIKE '%milton%' OR lastname LIKE '%grundberg%')
            AND firstname NOT LIKE '% %'
            ORDER BY id
        ", [], true);
        
        echo '<h2>Milton-ridare hittade: ' . count($milton) . '</h2>';
        
        if (count($milton) >= 2) {
            echo '<table>';
            echo '<tr><th>ID</th><th>Namn</th><th>UCI-ID</th><th>Resultat</th></tr>';
            
            foreach ($milton as $rider) {
                $results = $db->getRow("SELECT COUNT(*) as count FROM results WHERE cyclist_id = ?", [$rider['id']]);
                echo '<tr>';
                echo '<td>' . $rider['id'] . '</td>';
                echo '<td>' . h($rider['firstname'] . ' ' . $rider['lastname']) . '</td>';
                echo '<td>' . ($rider['license_number'] ?: '<em>ingen</em>') . '</td>';
                echo '<td>' . ($results['count'] ?? 0) . '</td>';
                echo '</tr>';
            }
            echo '</table>';
            
            // Visa resultat för båda
            echo '<h2>Resultat för rider ID ' . $milton[0]['id'] . '</h2>';
            $res1 = $db->getAll("
                SELECT r.id, r.time, e.name as event_name, e.date, c.name as class_name
                FROM results r
                JOIN events e ON r.event_id = e.id
                LEFT JOIN classes c ON r.class_id = c.id
                WHERE r.cyclist_id = ?
                LIMIT 10
            ", [$milton[0]['id']]);
            
            if (empty($res1)) {
                echo '<p>Ingen resultat</p>';
            } else {
                echo '<table>';
                echo '<tr><th>Result ID</th><th>Event</th><th>Datum</th><th>Klass</th><th>Tid</th></tr>';
                foreach ($res1 as $r) {
                    echo '<tr><td>' . $r['id'] . '</td><td>' . h($r['event_name']) . '</td><td>' . h($r['date']) . '</td><td>' . h($r['class_name'] ?? '-') . '</td><td>' . h($r['time'] ?? '-') . '</td></tr>';
                }
                echo '</table>';
            }
            
            if (count($milton) > 1) {
                echo '<h2>Resultat för rider ID ' . $milton[1]['id'] . '</h2>';
                $res2 = $db->getAll("
                    SELECT r.id, r.time, e.name as event_name, e.date, c.name as class_name
                    FROM results r
                    JOIN events e ON r.event_id = e.id
                    LEFT JOIN classes c ON r.class_id = c.id
                    WHERE r.cyclist_id = ?
                    LIMIT 10
                ", [$milton[1]['id']]);
                
                if (empty($res2)) {
                    echo '<p>Ingen resultat</p>';
                } else {
                    echo '<table>';
                    echo '<tr><th>Result ID</th><th>Event</th><th>Datum</th><th>Klass</th><th>Tid</th></tr>';
                    foreach ($res2 as $r) {
                        echo '<tr><td>' . $r['id'] . '</td><td>' . h($r['event_name']) . '</td><td>' . h($r['date']) . '</td><td>' . h($r['class_name'] ?? '-') . '</td><td>' . h($r['time'] ?? '-') . '</td></tr>';
                    }
                    echo '</table>';
                }
            }
            
            // Test merge SQL
            echo '<h2>Test: Merge SQL-commands</h2>';
            
            $keepId = $milton[0]['id'];
            $mergeId = $milton[1]['id'];
            
            echo '<p>Scenariot: Behåll ID ' . $keepId . ', slå samman ID ' . $mergeId . ' in i det.</p>';
            
            echo '<h3>SQL som skulle köras:</h3>';
            echo '<pre>';
            echo "-- 1. Hitta resultat för duplicate (ID $mergeId)\n";
            echo "SELECT id, event_id FROM results WHERE cyclist_id = $mergeId;\n\n";
            echo "-- 2. För varje resultat, kontrollera om master redan har det\n";
            echo "SELECT id FROM results WHERE cyclist_id = $keepId AND event_id = [event_id];\n\n";
            echo "-- 3. Om inte, uppdatera resultatet\n";
            echo "UPDATE results SET cyclist_id = $keepId WHERE id = [result_id];\n\n";
            echo "-- 4. Ta bort duplicate-ridaren\n";
            echo "DELETE FROM riders WHERE id = $mergeId;\n";
            echo '</pre>';
            
            // Verifiera struktur
            echo '<h2>Databasstruktur-check</h2>';
            
            $resultsCols = $db->getAll("PRAGMA table_info(results)");
            echo '<h3>results-tabell kolumner:</h3>';
            echo '<table>';
            echo '<tr><th>Namn</th><th>Typ</th></tr>';
            foreach ($resultsCols as $col) {
                echo '<tr><td>' . $col['name'] . '</td><td>' . $col['type'] . '</td></tr>';
            }
            echo '</table>';
            
            $ridersCols = $db->getAll("PRAGMA table_info(riders)");
            echo '<h3>riders-tabell kolumner:</h3>';
            echo '<table>';
            echo '<tr><th>Namn</th><th>Typ</th></tr>';
            foreach ($ridersCols as $col) {
                echo '<tr><td>' . $col['name'] . '</td><td>' . $col['type'] . '</td></tr>';
            }
            echo '</table>';
            
        } else {
            echo '<div class="error">Kunde inte hitta minst 2 Milton-ridare för test</div>';
        }
        
    } catch (Exception $e) {
        echo '<div class="error">';
        echo '<strong>Fel:</strong> ' . h($e->getMessage()) . '<br>';
        echo '<pre>' . h($e->getTraceAsString()) . '</pre>';
        echo '</div>';
    }
    ?>

</body>
</html>
