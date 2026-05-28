<?php
/**
 * DEBUG: Varför hittas inte Milton-dubbletterna?
 */
require_once __DIR__ . '/../config.php';
require_admin();

$db = getDB();

// ============================================
// MATCHING FUNKTIONER (samma som cleanup)
// ============================================

function splitName($fullName) {
  if (!$fullName) return ['', []];
  $fullName = trim($fullName);
  $parts = preg_split('/\s+/', $fullName, -1, PREG_SPLIT_NO_EMPTY);
  if (count($parts) < 2) {
    return [$parts[0] ?? '', []];
  }
  $firstName = array_shift($parts);
  $lastNames = $parts;
  return [$firstName, $lastNames];
}

function normalizeString($str) {
  return mb_strtolower(trim($str), 'UTF-8');
}

function stringsSimilar($str1, $str2, $maxDistance = 1) {
  $norm1 = normalizeString($str1);
  $norm2 = normalizeString($str2);
  if ($norm1 === $norm2) return true;
  $distance = levenshtein($norm1, $norm2);
  return $distance <= $maxDistance;
}

function getRiderClasses($db, $riderId) {
  $classes = $db->getAll("
    SELECT DISTINCT c.name as class_name
    FROM results r
    LEFT JOIN classes c ON r.class_id = c.id
    WHERE r.cyclist_id = ?
    AND c.name IS NOT NULL
  ", [$riderId]);
  
  return array_map(fn($c) => normalizeString($c['class_name']), $classes);
}

?>
<!DOCTYPE html>
<html>
<head>
    <title>DEBUG: Milton Matching</title>
    <style>
        body { font-family: Arial; margin: 20px; background: #f5f5f5; }
        .box { background: white; padding: 15px; margin: 15px 0; border-radius: 5px; border-left: 4px solid #0066cc; }
        table { border-collapse: collapse; width: 100%; }
        th, td { border: 1px solid #ddd; padding: 10px; text-align: left; }
        th { background: #f2f2f2; }
        .match { background: #90EE90; }
        .nomatch { background: #ffcccc; }
        h2 { color: #333; }
        pre { background: #f9f9f9; padding: 10px; overflow-x: auto; border-radius: 3px; }
        code { background: #f0f0f0; padding: 2px 5px; border-radius: 2px; }
    </style>
</head>
<body>
    <h1>DEBUG: Varför hittas inte Milton-dubbletterna?</h1>

    <?php
    try {
        // 1. Hämta alla riders
        echo '<div class="box">';
        echo '<h2>1. Alla riders med resultat</h2>';
        
        $allRiders = $db->getAll("
            SELECT DISTINCT r.id, r.firstname, r.lastname, r.license_number,
                   (SELECT COUNT(*) FROM results WHERE cyclist_id = r.id) as result_count
            FROM riders r
            WHERE EXISTS (SELECT 1 FROM results WHERE cyclist_id = r.id)
            ORDER BY r.firstname, r.lastname
        ");
        
        echo '<p>Totalt: <strong>' . count($allRiders) . '</strong> riders med resultat</p>';
        
        echo '<table>';
        echo '<tr><th>ID</th><th>Namn</th><th>UCI-ID</th><th>Resultat</th></tr>';
        foreach ($allRiders as $r) {
            echo '<tr>';
            echo '<td>' . $r['id'] . '</td>';
            echo '<td>' . h($r['firstname'] . ' ' . $r['lastname']) . '</td>';
            echo '<td>' . ($r['license_number'] ?: '<em>ingen</em>') . '</td>';
            echo '<td>' . $r['result_count'] . '</td>';
            echo '</tr>';
        }
        echo '</table>';
        echo '</div>';
        
        // 2. Test Milton-specifikt
        echo '<div class="box">';
        echo '<h2>2. Test: Milton-matching</h2>';
        
        $milton = array_filter($allRiders, fn($r) => stripos($r['firstname'], 'milton') !== false || stripos($r['lastname'], 'grundberg') !== false);
        
        echo '<p>Milton-riders hittade: <strong>' . count($milton) . '</strong></p>';
        
        if (count($milton) >= 2) {
            echo '<table>';
            echo '<tr><th>ID</th><th>Namn</th><th>Förnamn split</th><th>Efternamn split</th></tr>';
            foreach ($milton as $m) {
                [$fname, $lnames] = splitName($m['firstname'] . ' ' . $m['lastname']);
                echo '<tr>';
                echo '<td>' . $m['id'] . '</td>';
                echo '<td>' . h($m['firstname'] . ' ' . $m['lastname']) . '</td>';
                echo '<td><code>' . h($fname) . '</code></td>';
                echo '<td><code>' . implode(', ', $lnames) . '</code></td>';
                echo '</tr>';
            }
            echo '</table>';
            
            // Testa matching mellan första två
            if (count($milton) >= 2) {
                $m1 = array_values($milton)[0];
                $m2 = array_values($milton)[1];
                
                echo '<h3>Matching test mellan ID ' . $m1['id'] . ' och ID ' . $m2['id'] . '</h3>';
                
                [$fname1, $lnames1] = splitName($m1['firstname'] . ' ' . $m1['lastname']);
                [$fname2, $lnames2] = splitName($m2['firstname'] . ' ' . $m2['lastname']);
                
                echo '<p><strong>Förnamn:</strong></p>';
                echo '<pre>';
                echo "Rider 1: '$fname1'\n";
                echo "Rider 2: '$fname2'\n";
                echo "Similar: " . (stringsSimilar($fname1, $fname2, 1) ? 'JA ✓' : 'NEJ ✗') . "\n";
                echo "Levenshtein: " . levenshtein(normalizeString($fname1), normalizeString($fname2)) . "\n";
                echo '</pre>';
                
                echo '<p><strong>Efternamn:</strong></p>';
                echo '<pre>';
                echo "Rider 1: [" . implode(', ', array_map(fn($x) => "'$x'", $lnames1)) . "]\n";
                echo "Rider 2: [" . implode(', ', array_map(fn($x) => "'$x'", $lnames2)) . "]\n";
                $lastnameMatch = false;
                foreach ($lnames1 as $ln1) {
                    foreach ($lnames2 as $ln2) {
                        $sim = stringsSimilar($ln1, $ln2, 1);
                        echo "Compare: '$ln1' vs '$ln2' = " . ($sim ? 'MATCH ✓' : 'no') . "\n";
                        if ($sim) $lastnameMatch = true;
                    }
                }
                echo "Resultat: " . ($lastnameMatch ? 'JA ✓' : 'NEJ ✗') . "\n";
                echo '</pre>';
                
                echo '<p><strong>Klassdata:</strong></p>';
                $classes1 = getRiderClasses($db, $m1['id']);
                $classes2 = getRiderClasses($db, $m2['id']);
                echo '<pre>';
                echo "Rider 1: [" . implode(', ', $classes1) . "] (count: " . count($classes1) . ")\n";
                echo "Rider 2: [" . implode(', ', $classes2) . "] (count: " . count($classes2) . ")\n";
                if (!empty($classes1) && !empty($classes2)) {
                    $common = array_intersect($classes1, $classes2);
                    echo "Gemensam: [" . implode(', ', $common) . "]\n";
                    echo "Resultat: " . (empty($common) ? 'NEJ ✗' : 'JA ✓') . "\n";
                } else {
                    echo "Resultat: OPTIONAL (klassdata saknas) ✓\n";
                }
                echo '</pre>';
            }
        } else {
            echo '<p style="color: red;"><strong>PROBLEM:</strong> Inte tillräckligt många Milton-riders för test!</p>';
        }
        
        echo '</div>';
        
        // 3. Testa matchnings-funktion direkt
        echo '<div class="box">';
        echo '<h2>3. Full matching-test</h2>';
        
        if (count($milton) >= 2) {
            echo '<p>Testar <code>isSamePerson()</code> mellan alla Milton-par:</p>';
            echo '<table>';
            echo '<tr><th>Rider 1</th><th>Rider 2</th><th>Är samma?</th></tr>';
            
            for ($i = 0; $i < count($milton); $i++) {
                for ($j = $i + 1; $j < count($milton); $j++) {
                    $r1 = array_values($milton)[$i];
                    $r2 = array_values($milton)[$j];
                    
                    // Testa matching
                    $r1Data = $db->getRow("SELECT firstname, lastname, license_number FROM riders WHERE id = ?", [$r1['id']]);
                    $r2Data = $db->getRow("SELECT firstname, lastname, license_number FROM riders WHERE id = ?", [$r2['id']]);
                    
                    $r1HasUCI = !empty($r1Data['license_number']);
                    $r2HasUCI = !empty($r2Data['license_number']);
                    
                    $match = false;
                    if ($r1HasUCI && $r2HasUCI && $r1Data['license_number'] !== $r2Data['license_number']) {
                        $match = false;
                    } else {
                        [$fname1, $lnames1] = splitName($r1['firstname'] . ' ' . $r1['lastname']);
                        [$fname2, $lnames2] = splitName($r2['firstname'] . ' ' . $r2['lastname']);
                        
                        $fnameMatch = stringsSimilar($fname1, $fname2, 1);
                        $lastnameMatch = false;
                        foreach ($lnames1 as $ln1) {
                            foreach ($lnames2 as $ln2) {
                                if (stringsSimilar($ln1, $ln2, 1)) {
                                    $lastnameMatch = true;
                                    break 2;
                                }
                            }
                        }
                        
                        $match = $fnameMatch && $lastnameMatch;
                    }
                    
                    echo '<tr class="' . ($match ? 'match' : 'nomatch') . '">';
                    echo '<td>ID ' . $r1['id'] . ' (' . h($r1['firstname'] . ' ' . $r1['lastname']) . ')</td>';
                    echo '<td>ID ' . $r2['id'] . ' (' . h($r2['firstname'] . ' ' . $r2['lastname']) . ')</td>';
                    echo '<td>' . ($match ? '✓ JA' : '✗ NEJ') . '</td>';
                    echo '</tr>';
                }
            }
            echo '</table>';
        }
        
        echo '</div>';
        
    } catch (Exception $e) {
        echo '<div class="box" style="border-left-color: #cc0000;">';
        echo '<strong style="color: red;">FEL:</strong> ' . h($e->getMessage());
        echo '<pre>' . h($e->getTraceAsString()) . '</pre>';
        echo '</div>';
    }
    ?>

</body>
</html>
