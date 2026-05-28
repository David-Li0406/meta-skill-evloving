<?php
/**
 * Event Data Quality Analysis Tool
 *
 * Analyzes completeness of venue_id, organizer_club_id, and location data
 * for events. Used to prepare for Event Participation Analysis module.
 *
 * Run from CLI: php admin/tools/analyze-event-data-quality.php
 * Or access via browser (requires admin)
 */

// Handle both CLI and web
$isCli = php_sapi_name() === 'cli';

if (!$isCli) {
    require_once __DIR__ . '/../../config.php';
    require_admin();
    header('Content-Type: text/plain; charset=utf-8');
} else {
    require_once __DIR__ . '/../../config.php';
}

try {
    $pdo = new PDO(
        "mysql:host=" . DB_HOST . ";dbname=" . DB_NAME . ";charset=" . DB_CHARSET,
        DB_USER,
        DB_PASS,
        [PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION]
    );
} catch (PDOException $e) {
    die("Database connection failed: " . $e->getMessage() . "\n");
}

echo "========================================================\n";
echo "   EVENT DATA QUALITY ANALYSIS\n";
echo "   Generated: " . date('Y-m-d H:i:s') . "\n";
echo "========================================================\n\n";

// 1. Overall event statistics
echo "1. OVERALL EVENT STATISTICS\n";
echo "--------------------------------------------------------\n";

$stmt = $pdo->query("
    SELECT
        COUNT(*) as total_events,
        COUNT(DISTINCT series_id) as series_with_events,
        MIN(YEAR(date)) as first_year,
        MAX(YEAR(date)) as last_year,
        COUNT(DISTINCT YEAR(date)) as years_span
    FROM events
    WHERE date IS NOT NULL
");
$stats = $stmt->fetch(PDO::FETCH_ASSOC);

echo "Total events:          " . number_format($stats['total_events']) . "\n";
echo "Series with events:    " . $stats['series_with_events'] . "\n";
echo "Date range:            " . $stats['first_year'] . " - " . $stats['last_year'] . " (" . $stats['years_span'] . " years)\n\n";

// 2. Venue completeness
echo "2. VENUE DATA COMPLETENESS\n";
echo "--------------------------------------------------------\n";

$stmt = $pdo->query("
    SELECT
        COUNT(*) as total,
        SUM(CASE WHEN venue_id IS NOT NULL THEN 1 ELSE 0 END) as has_venue_id,
        SUM(CASE WHEN location IS NOT NULL AND location != '' THEN 1 ELSE 0 END) as has_location,
        SUM(CASE WHEN venue_id IS NOT NULL OR (location IS NOT NULL AND location != '') THEN 1 ELSE 0 END) as has_any_location
    FROM events
");
$venue = $stmt->fetch(PDO::FETCH_ASSOC);

$pctVenue = round(100 * $venue['has_venue_id'] / $venue['total'], 1);
$pctLocation = round(100 * $venue['has_location'] / $venue['total'], 1);
$pctAny = round(100 * $venue['has_any_location'] / $venue['total'], 1);

echo "Has venue_id:          " . number_format($venue['has_venue_id']) . " / " . number_format($venue['total']) . " ({$pctVenue}%)\n";
echo "Has location (text):   " . number_format($venue['has_location']) . " / " . number_format($venue['total']) . " ({$pctLocation}%)\n";
echo "Has ANY location:      " . number_format($venue['has_any_location']) . " / " . number_format($venue['total']) . " ({$pctAny}%)\n\n";

// 3. Organizer completeness
echo "3. ORGANIZER DATA COMPLETENESS\n";
echo "--------------------------------------------------------\n";

// Check if organizer_club_id column exists
$stmt = $pdo->query("SHOW COLUMNS FROM events LIKE 'organizer_club_id'");
$hasOrganizerClubId = $stmt->rowCount() > 0;

$stmt = $pdo->query("
    SELECT
        COUNT(*) as total,
        SUM(CASE WHEN organizer IS NOT NULL AND organizer != '' THEN 1 ELSE 0 END) as has_organizer_text
        " . ($hasOrganizerClubId ? ", SUM(CASE WHEN organizer_club_id IS NOT NULL THEN 1 ELSE 0 END) as has_organizer_club_id" : "") . "
    FROM events
");
$org = $stmt->fetch(PDO::FETCH_ASSOC);

$pctOrgText = round(100 * $org['has_organizer_text'] / $org['total'], 1);

echo "Has organizer (text):  " . number_format($org['has_organizer_text']) . " / " . number_format($org['total']) . " ({$pctOrgText}%)\n";
if ($hasOrganizerClubId) {
    $pctOrgClub = round(100 * $org['has_organizer_club_id'] / $org['total'], 1);
    echo "Has organizer_club_id: " . number_format($org['has_organizer_club_id']) . " / " . number_format($org['total']) . " ({$pctOrgClub}%)\n";
} else {
    echo "Column organizer_club_id: DOES NOT EXIST (migration 053 not run)\n";
}
echo "\n";

// 4. Series breakdown
echo "4. DATA COMPLETENESS BY SERIES\n";
echo "--------------------------------------------------------\n";

$stmt = $pdo->query("
    SELECT
        s.id,
        s.name,
        COUNT(e.id) as event_count,
        SUM(CASE WHEN e.venue_id IS NOT NULL THEN 1 ELSE 0 END) as has_venue,
        SUM(CASE WHEN e.location IS NOT NULL AND e.location != '' THEN 1 ELSE 0 END) as has_location,
        SUM(CASE WHEN e.organizer IS NOT NULL AND e.organizer != '' THEN 1 ELSE 0 END) as has_organizer
    FROM series s
    LEFT JOIN events e ON e.series_id = s.id
    GROUP BY s.id, s.name
    HAVING event_count > 0
    ORDER BY event_count DESC
    LIMIT 20
");

printf("%-35s %6s %8s %8s %8s\n", "Series", "Events", "Venue%", "Loc%", "Org%");
printf("%s\n", str_repeat("-", 75));

while ($row = $stmt->fetch(PDO::FETCH_ASSOC)) {
    $pctV = $row['event_count'] > 0 ? round(100 * $row['has_venue'] / $row['event_count']) : 0;
    $pctL = $row['event_count'] > 0 ? round(100 * $row['has_location'] / $row['event_count']) : 0;
    $pctO = $row['event_count'] > 0 ? round(100 * $row['has_organizer'] / $row['event_count']) : 0;

    $name = mb_substr($row['name'], 0, 33);
    printf("%-35s %6d %7d%% %7d%% %7d%%\n", $name, $row['event_count'], $pctV, $pctL, $pctO);
}
echo "\n";

// 5. Venues table statistics
echo "5. VENUES TABLE\n";
echo "--------------------------------------------------------\n";

$stmt = $pdo->query("SELECT COUNT(*) FROM venues");
$venueCount = $stmt->fetchColumn();

$stmt = $pdo->query("
    SELECT
        COUNT(DISTINCT v.id) as used_venues,
        COUNT(DISTINCT e.id) as events_with_venue
    FROM venues v
    JOIN events e ON e.venue_id = v.id
");
$venueUsage = $stmt->fetch(PDO::FETCH_ASSOC);

echo "Total venues:          " . number_format($venueCount) . "\n";
echo "Venues in use:         " . number_format($venueUsage['used_venues']) . "\n";
echo "Events with venue:     " . number_format($venueUsage['events_with_venue']) . "\n\n";

// 6. Location text patterns (for potential venue matching)
echo "6. TOP LOCATION TEXT VALUES (for venue matching)\n";
echo "--------------------------------------------------------\n";

$stmt = $pdo->query("
    SELECT
        location,
        COUNT(*) as event_count,
        COUNT(DISTINCT series_id) as series_count
    FROM events
    WHERE location IS NOT NULL
      AND location != ''
      AND venue_id IS NULL
    GROUP BY location
    ORDER BY event_count DESC
    LIMIT 15
");

printf("%-40s %6s %6s\n", "Location (no venue_id)", "Events", "Series");
printf("%s\n", str_repeat("-", 55));

while ($row = $stmt->fetch(PDO::FETCH_ASSOC)) {
    $loc = mb_substr($row['location'], 0, 38);
    printf("%-40s %6d %6d\n", $loc, $row['event_count'], $row['series_count']);
}
echo "\n";

// 7. Organizer text patterns
echo "7. TOP ORGANIZER TEXT VALUES\n";
echo "--------------------------------------------------------\n";

$stmt = $pdo->query("
    SELECT
        organizer,
        COUNT(*) as event_count
    FROM events
    WHERE organizer IS NOT NULL
      AND organizer != ''
    GROUP BY organizer
    ORDER BY event_count DESC
    LIMIT 15
");

printf("%-45s %6s\n", "Organizer", "Events");
printf("%s\n", str_repeat("-", 55));

while ($row = $stmt->fetch(PDO::FETCH_ASSOC)) {
    $org = mb_substr($row['organizer'], 0, 43);
    printf("%-45s %6d\n", $org, $row['event_count']);
}
echo "\n";

// 8. Year-over-year event counts (for retention analysis feasibility)
echo "8. EVENTS PER YEAR (for retention analysis)\n";
echo "--------------------------------------------------------\n";

$stmt = $pdo->query("
    SELECT
        YEAR(date) as year,
        COUNT(*) as events,
        COUNT(DISTINCT series_id) as series,
        (SELECT COUNT(DISTINCT cyclist_id) FROM results r
         JOIN events e2 ON r.event_id = e2.id
         WHERE YEAR(e2.date) = YEAR(e.date)) as participants
    FROM events e
    WHERE date IS NOT NULL
    GROUP BY YEAR(date)
    ORDER BY year DESC
    LIMIT 10
");

printf("%6s %8s %8s %12s\n", "Year", "Events", "Series", "Participants");
printf("%s\n", str_repeat("-", 40));

while ($row = $stmt->fetch(PDO::FETCH_ASSOC)) {
    printf("%6d %8d %8d %12s\n",
        $row['year'],
        $row['events'],
        $row['series'],
        number_format($row['participants'])
    );
}
echo "\n";

// 9. Recommendations
echo "9. RECOMMENDATIONS\n";
echo "========================================================\n";

$recommendations = [];

if ($pctVenue < 50) {
    $recommendations[] = "- PRIORITY: Only {$pctVenue}% of events have venue_id. Consider:\n  1. Creating venues from unique location text values\n  2. Building admin tool to bulk-assign venues";
}

if (!$hasOrganizerClubId) {
    $recommendations[] = "- organizer_club_id column missing. Run migration 053 to add it.";
}

if ($pctOrgText > 50 && (!$hasOrganizerClubId || $org['has_organizer_club_id'] < $org['has_organizer_text'] * 0.3)) {
    $recommendations[] = "- Many events have organizer text but no club link. Consider:\n  1. Matching organizer text to clubs table\n  2. Building admin tool for organizer→club mapping";
}

if (empty($recommendations)) {
    $recommendations[] = "- Data quality looks good! Ready for Event Participation Analysis.";
}

foreach ($recommendations as $rec) {
    echo $rec . "\n\n";
}

echo "========================================================\n";
echo "   Analysis complete.\n";
echo "========================================================\n";
