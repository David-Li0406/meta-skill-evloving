<?php
/**
 * Visa struktur på riders-tabellen
 */

require_once __DIR__ . '/config/database.php';

echo "=== Riders Table Structure ===\n\n";

try {
    // Visa kolumner
    $stmt = $pdo->query("DESCRIBE riders");
    $columns = $stmt->fetchAll();
    
    echo "Columns in riders table:\n";
    echo str_repeat("-", 80) . "\n";
    printf("%-25s %-20s %-10s %-10s\n", "Field", "Type", "Null", "Key");
    echo str_repeat("-", 80) . "\n";
    
    foreach ($columns as $col) {
        printf("%-25s %-20s %-10s %-10s\n", 
            $col['Field'], 
            $col['Type'], 
            $col['Null'], 
            $col['Key']
        );
    }
    
    // Visa antal riders
    $stmt = $pdo->query("SELECT COUNT(*) as total FROM riders");
    $count = $stmt->fetch();
    
    echo "\nTotal riders: " . $count['total'] . "\n";
    
    // Visa hur många som har UCI ID
    $stmt = $pdo->query("SELECT COUNT(*) as total FROM riders WHERE uci_id IS NOT NULL AND uci_id != ''");
    $uciCount = $stmt->fetch();
    
    echo "Riders with UCI ID: " . $uciCount['total'] . "\n";
    
    // Visa ett exempel
    $stmt = $pdo->query("SELECT * FROM riders WHERE uci_id IS NOT NULL LIMIT 1");
    $example = $stmt->fetch();
    
    if ($example) {
        echo "\nExample rider data:\n";
        echo str_repeat("-", 80) . "\n";
        foreach ($example as $key => $value) {
            if (!is_numeric($key)) {
                echo "$key: $value\n";
            }
        }
    }
    
} catch (Exception $e) {
    echo "Error: " . $e->getMessage() . "\n";
}

echo "\n=== Done ===\n";
?>
