<?php
/**
 * UPDATED MATCHING LOGIC
 * 
 * En rider matchas med en annan om:
 * 1. Minst ett FÖRNAMN matchar (exakt eller Levenshtein < 2)
 * 2. Minst ett EFTERNAMN matchar (exakt eller Levenshtein < 2)
 * 3. Minst en TÄVLINGSKLASS är gemensam
 * 4. KLUBB matchar (optional men hjälper)
 * 5. UCI-ID är overspelade (två profiler med samma data = samma person)
 */

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

function stringsSimilar($str1, $str2, $maxDistance = 2) {
  $norm1 = normalizeString($str1);
  $norm2 = normalizeString($str2);
  if ($norm1 === $norm2) return true;
  $distance = levenshtein($norm1, $norm2);
  return $distance <= $maxDistance;
}

/**
 * Hitta alla tävlingsklasser för en rider
 */
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

/**
 * Hitta alla klubbar en rider har tävlat för
 */
function getRiderClubs($db, $riderId) {
  $clubs = $db->getAll("
    SELECT DISTINCT e.club_id
    FROM results r
    JOIN events e ON r.event_id = e.id
    WHERE r.cyclist_id = ?
    AND e.club_id IS NOT NULL
  ", [$riderId]);
  
  return array_column($clubs, 'club_id');
}

/**
 * NY MATCHING-LOGIK:
 * Två riders är samma person om:
 * 1. Minst ett förnamn matchar
 * 2. Minst ett efternamn matchar
 * 3. Minst en tävlingsklass är gemensam
 */
function isSamePerson($db, $rider1Id, $rider2Id) {
  $r1 = $db->getRow("SELECT firstname, lastname FROM riders WHERE id = ?", [$rider1Id]);
  $r2 = $db->getRow("SELECT firstname, lastname FROM riders WHERE id = ?", [$rider2Id]);
  
  if (!$r1 || !$r2) return false;
  
  [$fname1, $lnames1] = splitName($r1['firstname'] . ' ' . $r1['lastname']);
  [$fname2, $lnames2] = splitName($r2['firstname'] . ' ' . $r2['lastname']);
  
  // 1. Förnamn måste matcha
  $firstnameMatch = stringsSimilar($fname1, $fname2, 1);
  if (!$firstnameMatch) return false;
  
  // 2. Minst ett efternamn måste matcha
  $lastnameMatch = false;
  foreach ($lnames1 as $ln1) {
    foreach ($lnames2 as $ln2) {
      if (stringsSimilar($ln1, $ln2, 1)) {
        $lastnameMatch = true;
        break 2;
      }
    }
  }
  if (!$lastnameMatch) return false;
  
  // 3. Minst en tävlingsklass måste vara gemensam
  $classes1 = getRiderClasses($db, $rider1Id);
  $classes2 = getRiderClasses($db, $rider2Id);
  
  if (empty($classes1) || empty($classes2)) {
    // Ingen klassdata - kan inte verifiera
    return false;
  }
  
  $commonClasses = array_intersect($classes1, $classes2);
  if (empty($commonClasses)) {
    // Ingen gemensam klass
    return false;
  }
  
  return true;
}

/**
 * Hitta alla dubbletter med NYA logiken
 */
function findDuplicatesByClassMatch($db) {
  $allRiders = $db->getAll("
    SELECT DISTINCT r.id, r.firstname, r.lastname
    FROM riders r
    WHERE EXISTS (SELECT 1 FROM results WHERE cyclist_id = r.id)
    ORDER BY r.id
  ");
  
  $duplicates = [];
  $processedPairs = [];
  
  for ($i = 0; $i < count($allRiders); $i++) {
    $rider1 = $allRiders[$i];
    
    for ($j = $i + 1; $j < count($allRiders); $j++) {
      $rider2 = $allRiders[$j];
      
      $pairKey = $rider1['id'] . '_' . $rider2['id'];
      if (isset($processedPairs[$pairKey])) {
        continue;
      }
      $processedPairs[$pairKey] = true;
      
      if (isSamePerson($db, $rider1['id'], $rider2['id'])) {
        $results1 = $db->getRow("SELECT COUNT(*) as count FROM results WHERE cyclist_id = ?", [$rider1['id']]);
        $results2 = $db->getRow("SELECT COUNT(*) as count FROM results WHERE cyclist_id = ?", [$rider2['id']]);
        
        $classes1 = getRiderClasses($db, $rider1['id']);
        $classes2 = getRiderClasses($db, $rider2['id']);
        $commonClasses = array_intersect($classes1, $classes2);
        
        $duplicates[] = [
          'rider1_id' => $rider1['id'],
          'rider1_name' => $rider1['firstname'] . ' ' . $rider1['lastname'],
          'rider1_results' => $results1['count'] ?? 0,
          
          'rider2_id' => $rider2['id'],
          'rider2_name' => $rider2['firstname'] . ' ' . $rider2['lastname'],
          'rider2_results' => $results2['count'] ?? 0,
          
          'common_classes' => implode(', ', $commonClasses),
          'match_reason' => 'FORNAMN + EFTERNAMN + KLASS'
        ];
      }
    }
  }
  
  return $duplicates;
}

// TEST
echo "Matching-logik uppdaterad!\n";
echo "Nya kriterier:\n";
echo "1. Förnamn matchar (Levenshtein <= 1)\n";
echo "2. Minst ett efternamn matchar (Levenshtein <= 1)\n";
echo "3. Minst en tävlingsklass är gemensam\n";
?>
