<?php
/**
 * EMERGENCY ROLLBACK - RANKING SYSTEM
 * This will restore basic ranking functionality
 * Upload to server root and run ONCE
 */

error_reporting(E_ALL);
ini_set('display_errors', 1);

require_once __DIR__ . '/config.php';

echo "<h1>🔧 EMERGENCY RANKING ROLLBACK</h1>";
echo "<style>body{font-family:monospace;background:#1a1a1a;color:#0f0;padding:20px;}</style>";

// STEP 1: Check if tables exist
echo "<h2>Step 1: Checking tables...</h2>";

$tables_needed = [
    'ranking_points' => "
        CREATE TABLE IF NOT EXISTS ranking_points (
            id INT PRIMARY KEY AUTO_INCREMENT,
            rider_id INT NOT NULL,
            event_id INT NOT NULL,
            discipline VARCHAR(50) DEFAULT 'enduro',
            base_points DECIMAL(10,2) DEFAULT 0,
            field_size_multiplier DECIMAL(5,2) DEFAULT 1.0,
            time_decay_multiplier DECIMAL(5,2) DEFAULT 1.0,
            event_level_multiplier DECIMAL(5,2) DEFAULT 1.0,
            final_points DECIMAL(10,2) DEFAULT 0,
            calculated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (rider_id) REFERENCES riders(id) ON DELETE CASCADE,
            FOREIGN KEY (event_id) REFERENCES events(id) ON DELETE CASCADE,
            INDEX idx_rider (rider_id),
            INDEX idx_event (event_id),
            INDEX idx_discipline (discipline)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
    ",
    'ranking_snapshots' => "
        CREATE TABLE IF NOT EXISTS ranking_snapshots (
            id INT PRIMARY KEY AUTO_INCREMENT,
            rider_id INT NOT NULL,
            discipline VARCHAR(50) DEFAULT 'enduro',
            position INT,
            total_points DECIMAL(10,2),
            events_counted INT,
            snapshot_date DATE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (rider_id) REFERENCES riders(id) ON DELETE CASCADE,
            INDEX idx_rider_disc (rider_id, discipline),
            INDEX idx_snapshot (snapshot_date)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
    "
];

foreach ($tables_needed as $table => $sql) {
    try {
        $db->query($sql);
        echo "✅ Table {$table} OK<br>";
    } catch (Exception $e) {
        echo "❌ Error with {$table}: " . $e->getMessage() . "<br>";
    }
}

// STEP 2: Simple ranking calculation
echo "<h2>Step 2: Recalculating rankings (simple method)...</h2>";

try {
    // Clear old data
    $db->query("TRUNCATE ranking_points");
    $db->query("TRUNCATE ranking_snapshots");
    echo "✅ Cleared old ranking data<br>";
    
    // Get all results from last 24 months
    $results = $db->getAll("
        SELECT 
            r.id as result_id,
            r.rider_id,
            r.event_id,
            r.position,
            r.points,
            e.date as event_date,
            e.discipline,
            (SELECT COUNT(*) FROM results r2 WHERE r2.event_id = r.event_id) as field_size
        FROM results r
        INNER JOIN events e ON r.event_id = e.id
        WHERE e.date >= DATE_SUB(CURDATE(), INTERVAL 24 MONTH)
          AND r.position > 0
        ORDER BY e.date DESC
    ");
    
    echo "Found " . count($results) . " results to process<br>";
    
    // Calculate points for each result
    foreach ($results as $result) {
        // Simple base points
        $base_points = $result['points'] ?? 100;
        
        // Field size multiplier
        $field_size = $result['field_size'];
        if ($field_size <= 10) {
            $field_multiplier = 0.8;
        } elseif ($field_size <= 20) {
            $field_multiplier = 0.9;
        } elseif ($field_size <= 30) {
            $field_multiplier = 1.0;
        } elseif ($field_size <= 50) {
            $field_multiplier = 1.1;
        } else {
            $field_multiplier = 1.2;
        }
        
        // Time decay
        $months_ago = (strtotime('now') - strtotime($result['event_date'])) / (30 * 24 * 60 * 60);
        if ($months_ago <= 6) {
            $time_multiplier = 1.0;
        } elseif ($months_ago <= 12) {
            $time_multiplier = 0.9;
        } elseif ($months_ago <= 18) {
            $time_multiplier = 0.7;
        } else {
            $time_multiplier = 0.5;
        }
        
        $final_points = $base_points * $field_multiplier * $time_multiplier;
        
        // Insert into ranking_points
        $db->insert('ranking_points', [
            'rider_id' => $result['rider_id'],
            'event_id' => $result['event_id'],
            'discipline' => $result['discipline'] ?? 'enduro',
            'base_points' => $base_points,
            'field_size_multiplier' => $field_multiplier,
            'time_decay_multiplier' => $time_multiplier,
            'event_level_multiplier' => 1.0,
            'final_points' => $final_points
        ]);
    }
    
    echo "✅ Calculated " . count($results) . " ranking points<br>";
    
    // Create snapshots
    $disciplines = ['enduro', 'downhill'];
    
    foreach ($disciplines as $discipline) {
        $rankings = $db->getAll("
            SELECT 
                rider_id,
                SUM(final_points) as total_points,
                COUNT(DISTINCT event_id) as events_counted
            FROM ranking_points
            WHERE discipline = ?
            GROUP BY rider_id
            ORDER BY total_points DESC
        ", [$discipline]);
        
        $position = 1;
        foreach ($rankings as $ranking) {
            $db->insert('ranking_snapshots', [
                'rider_id' => $ranking['rider_id'],
                'discipline' => $discipline,
                'position' => $position,
                'total_points' => $ranking['total_points'],
                'events_counted' => $ranking['events_counted'],
                'snapshot_date' => date('Y-m-d')
            ]);
            $position++;
        }
        
        echo "✅ Created {$position} snapshots for {$discipline}<br>";
    }
    
    echo "<br><h2>✅ RANKING SYSTEM RESTORED!</h2>";
    echo "<p>Test it at: <a href='/ranking'>https://thehub.gravityseries.se/ranking</a></p>";
    echo "<p>Test rider: <a href='/rider/7701'>https://thehub.gravityseries.se/rider/7701</a></p>";
    
} catch (Exception $e) {
    echo "❌ ERROR: " . $e->getMessage() . "<br>";
    echo "<pre>" . $e->getTraceAsString() . "</pre>";
}

echo "<br><hr>";
echo "<p><strong>⚠️ DELETE THIS FILE AFTER SUCCESS!</strong></p>";
?>
