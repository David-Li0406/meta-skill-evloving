<?php
/**
 * Verification script - Göteborg 2024 participants
 * Temporary debug script
 */
require_once __DIR__ . '/../../config.php';
require_admin();

global $pdo;

echo "<pre style='font-family: monospace; padding: 20px;'>";
echo "=== VERIFIERING: GÖTEBORG 2024 ===\n\n";

// 1. Hitta Göteborg-eventet
$stmt = $pdo->prepare("
    SELECT e.id, e.name, e.date, e.location
    FROM events e
    WHERE (e.name LIKE '%Göteborg%' OR e.location LIKE '%Göteborg%' OR e.location LIKE '%Lackarebacken%')
    AND YEAR(e.date) = 2024
    ORDER BY e.date
");
$stmt->execute();
$events = $stmt->fetchAll(PDO::FETCH_ASSOC);

echo "1. EVENTS SOM MATCHAR 'GÖTEBORG' 2024:\n";
echo str_repeat("-", 60) . "\n";
foreach ($events as $e) {
    echo "   ID: {$e['id']} | {$e['name']} | {$e['date']} | {$e['location']}\n";
}
echo "\n";

// 2. För varje event, räkna deltagare
echo "2. DELTAGARE PER EVENT:\n";
echo str_repeat("-", 60) . "\n";

foreach ($events as $e) {
    $stmt = $pdo->prepare("SELECT COUNT(DISTINCT cyclist_id) as cnt FROM results WHERE event_id = ?");
    $stmt->execute([$e['id']]);
    $count = $stmt->fetchColumn();
    echo "   Event ID {$e['id']}: {$count} unika deltagare\n";

    // Kolla också hur många resultatrader
    $stmt = $pdo->prepare("SELECT COUNT(*) as cnt FROM results WHERE event_id = ?");
    $stmt->execute([$e['id']]);
    $rows = $stmt->fetchColumn();
    echo "   (totalt {$rows} resultatrader)\n\n";
}

// 3. Kolla Swecup-koppling (brand_id = 5)
echo "3. SWECUP-KOPPLING (brand_id = 5):\n";
echo str_repeat("-", 60) . "\n";

$stmt = $pdo->prepare("
    SELECT e.id, e.name, e.date, s.name as series_name, s.brand_id
    FROM events e
    JOIN series_events se ON se.event_id = e.id
    JOIN series s ON s.id = se.series_id
    WHERE s.brand_id = 5
    AND YEAR(e.date) = 2024
    ORDER BY e.date
");
$stmt->execute();
$swecupEvents = $stmt->fetchAll(PDO::FETCH_ASSOC);

echo "   Swecup-events 2024:\n";
foreach ($swecupEvents as $e) {
    echo "   - ID {$e['id']}: {$e['name']} ({$e['date']}) - Serie: {$e['series_name']}\n";
}
echo "\n";

// 4. Hitta specifikt Göteborg Swecup event
echo "4. GÖTEBORG I SWECUP 2024:\n";
echo str_repeat("-", 60) . "\n";

$stmt = $pdo->prepare("
    SELECT e.id, e.name, e.date, e.location,
           COUNT(DISTINCT r.cyclist_id) as unique_riders,
           COUNT(r.id) as total_results
    FROM events e
    JOIN series_events se ON se.event_id = e.id
    JOIN series s ON s.id = se.series_id
    LEFT JOIN results r ON r.event_id = e.id
    WHERE s.brand_id = 5
    AND YEAR(e.date) = 2024
    AND (e.name LIKE '%Göteborg%' OR e.location LIKE '%Göteborg%' OR e.location LIKE '%Lackarebacken%')
    GROUP BY e.id
");
$stmt->execute();
$goteborg = $stmt->fetchAll(PDO::FETCH_ASSOC);

if (empty($goteborg)) {
    echo "   INGEN MATCH för Göteborg i Swecup 2024!\n";

    // Kolla vad Lackarebacken-eventet är kopplat till
    echo "\n   Kollar Lackarebacken-events och deras seriekopplingar:\n";
    $stmt = $pdo->prepare("
        SELECT e.id, e.name, e.date, e.location, s.name as series_name, s.brand_id, sb.name as brand_name
        FROM events e
        LEFT JOIN series_events se ON se.event_id = e.id
        LEFT JOIN series s ON s.id = se.series_id
        LEFT JOIN series_brands sb ON sb.id = s.brand_id
        WHERE e.location LIKE '%Lackarebacken%'
        AND YEAR(e.date) = 2024
    ");
    $stmt->execute();
    $lackare = $stmt->fetchAll(PDO::FETCH_ASSOC);
    foreach ($lackare as $l) {
        echo "   - ID {$l['id']}: {$l['name']} | Serie: " . ($l['series_name'] ?? 'INGEN') . " | Brand: " . ($l['brand_name'] ?? 'INGEN') . "\n";
    }
} else {
    foreach ($goteborg as $g) {
        echo "   Event ID {$g['id']}: {$g['name']}\n";
        echo "   Plats: {$g['location']}\n";
        echo "   Datum: {$g['date']}\n";
        echo "   Unika deltagare: {$g['unique_riders']}\n";
        echo "   Totalt resultatrader: {$g['total_results']}\n";
    }
}

echo "\n";

// 5. Visa alla Swecup 2024 events med deltagarantal
echo "5. ALLA SWECUP 2024 EVENTS MED DELTAGARE:\n";
echo str_repeat("-", 60) . "\n";

$stmt = $pdo->prepare("
    SELECT e.id, e.name, e.date, e.location,
           COUNT(DISTINCT r.cyclist_id) as unique_riders
    FROM events e
    JOIN series_events se ON se.event_id = e.id
    JOIN series s ON s.id = se.series_id
    LEFT JOIN results r ON r.event_id = e.id
    WHERE s.brand_id = 5
    AND YEAR(e.date) = 2024
    GROUP BY e.id
    ORDER BY e.date
");
$stmt->execute();
$allSwecup = $stmt->fetchAll(PDO::FETCH_ASSOC);

$total = 0;
foreach ($allSwecup as $e) {
    echo "   {$e['date']} | {$e['name']} | {$e['location']} | {$e['unique_riders']} deltagare\n";
    $total += $e['unique_riders'];
}
echo "\n   TOTALT: {$total} starter (ej unika)\n";

// 6. Bryt ner per klass för att se om det är hobby vs tävling
echo "6. GÖTEBORG/LACKAREBACKEN - UPPDELAT PER KLASS:\n";
echo str_repeat("-", 60) . "\n";

$stmt = $pdo->prepare("
    SELECT e.id, e.name, e.date
    FROM events e
    WHERE (e.location LIKE '%Lackarebacken%' OR e.name LIKE '%Göteborg%')
    AND YEAR(e.date) = 2024
    LIMIT 1
");
$stmt->execute();
$gbgEvent = $stmt->fetch(PDO::FETCH_ASSOC);

if ($gbgEvent) {
    echo "   Event: {$gbgEvent['name']} (ID: {$gbgEvent['id']})\n\n";

    $stmt = $pdo->prepare("
        SELECT
            c.name as class_name,
            c.id as class_id,
            COUNT(DISTINCT r.cyclist_id) as riders
        FROM results r
        LEFT JOIN classes c ON c.id = r.class_id
        WHERE r.event_id = ?
        GROUP BY r.class_id
        ORDER BY riders DESC
    ");
    $stmt->execute([$gbgEvent['id']]);
    $classes = $stmt->fetchAll(PDO::FETCH_ASSOC);

    $totalCompetition = 0;
    $totalHobby = 0;

    foreach ($classes as $c) {
        $className = $c['class_name'] ?? 'Okänd klass';
        $isHobby = (stripos($className, 'hobby') !== false ||
                    stripos($className, 'motion') !== false ||
                    stripos($className, 'open') !== false ||
                    stripos($className, 'öppen') !== false);

        $type = $isHobby ? '[HOBBY/MOTION]' : '[TÄVLING]';
        echo "   {$type} {$className}: {$c['riders']} deltagare\n";

        if ($isHobby) {
            $totalHobby += $c['riders'];
        } else {
            $totalCompetition += $c['riders'];
        }
    }

    echo "\n   SUMMERING:\n";
    echo "   - Tävlingsklasser: {$totalCompetition} deltagare\n";
    echo "   - Hobby/Motion: {$totalHobby} deltagare\n";
    echo "   - TOTALT: " . ($totalCompetition + $totalHobby) . " deltagare\n";
}

echo "\n=== SLUT ===\n";
echo "</pre>";
