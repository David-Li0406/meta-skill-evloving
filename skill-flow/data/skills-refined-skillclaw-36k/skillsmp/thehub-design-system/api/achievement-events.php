<?php
/**
 * API endpoint to get events related to a specific achievement type for a rider
 */
require_once __DIR__ . '/../config.php';

header('Content-Type: application/json');

$riderId = isset($_GET['rider_id']) ? (int)$_GET['rider_id'] : 0;
$achievementType = isset($_GET['type']) ? trim($_GET['type']) : '';

if (!$riderId || !$achievementType) {
    http_response_code(400);
    echo json_encode(['error' => 'Missing rider_id or type parameter']);
    exit;
}

$db = getDB();
$events = [];

try {
    switch ($achievementType) {
        case 'gold':
            // Events where rider got 1st place
            $events = $db->getAll("
                SELECT e.id, e.name, e.date, e.location, r.position, c.name as class_name
                FROM results r
                JOIN events e ON r.event_id = e.id
                LEFT JOIN classes c ON r.class_id = c.id
                WHERE r.cyclist_id = ? AND r.position = 1 AND r.status = 'finished'
                ORDER BY e.date DESC
            ", [$riderId]);
            break;

        case 'silver':
            // Events where rider got 2nd place
            $events = $db->getAll("
                SELECT e.id, e.name, e.date, e.location, r.position, c.name as class_name
                FROM results r
                JOIN events e ON r.event_id = e.id
                LEFT JOIN classes c ON r.class_id = c.id
                WHERE r.cyclist_id = ? AND r.position = 2 AND r.status = 'finished'
                ORDER BY e.date DESC
            ", [$riderId]);
            break;

        case 'bronze':
            // Events where rider got 3rd place
            $events = $db->getAll("
                SELECT e.id, e.name, e.date, e.location, r.position, c.name as class_name
                FROM results r
                JOIN events e ON r.event_id = e.id
                LEFT JOIN classes c ON r.class_id = c.id
                WHERE r.cyclist_id = ? AND r.position = 3 AND r.status = 'finished'
                ORDER BY e.date DESC
            ", [$riderId]);
            break;

        case 'hot_streak':
            // Get podium finishes to show streak periods
            $podiums = $db->getAll("
                SELECT e.id, e.name, e.date, e.location, r.position, c.name as class_name
                FROM results r
                JOIN events e ON r.event_id = e.id
                LEFT JOIN classes c ON r.class_id = c.id
                WHERE r.cyclist_id = ? AND r.position <= 3 AND r.status = 'finished'
                ORDER BY e.date ASC
            ", [$riderId]);

            // Find streak sequences
            $streakEvents = [];
            $currentStreak = [];

            foreach ($podiums as $podium) {
                $currentStreak[] = $podium;
                if (count($currentStreak) >= 3) {
                    // This is part of a hot streak
                    foreach ($currentStreak as $ev) {
                        $streakEvents[$ev['id']] = $ev;
                    }
                }
            }

            // Reset streak on non-podium (simplified - just show all podiums that contributed to streaks)
            $events = array_values($streakEvents);
            usort($events, fn($a, $b) => strtotime($b['date']) - strtotime($a['date']));
            break;

        case 'series_completed':
        case 'finisher_100':
            // Series where rider completed 100% - from rider_achievements table
            $events = $db->getAll("
                SELECT s.id, s.name as series_name, s.year, ra.season_year
                FROM rider_achievements ra
                JOIN series s ON ra.series_id = s.id
                WHERE ra.rider_id = ? AND ra.achievement_type = 'finisher_100'
                ORDER BY ra.season_year DESC, s.name
            ", [$riderId]);
            break;

        case 'series_leader':
            // Current series where rider is leading - from rider_achievements table
            $events = $db->getAll("
                SELECT s.id, s.name as series_name, s.year, ra.season_year
                FROM rider_achievements ra
                JOIN series s ON ra.series_id = s.id
                WHERE ra.rider_id = ? AND ra.achievement_type = 'series_leader'
                ORDER BY ra.season_year DESC, s.name
            ", [$riderId]);
            break;

        case 'series_champion':
        case 'series_wins':
            // Series won by rider - from rider_achievements table
            $events = $db->getAll("
                SELECT s.id, s.name as series_name, s.year, ra.season_year
                FROM rider_achievements ra
                JOIN series s ON ra.series_id = s.id
                WHERE ra.rider_id = ? AND ra.achievement_type = 'series_champion'
                ORDER BY ra.season_year DESC, s.name
            ", [$riderId]);
            break;

        case 'swedish_champion':
        case 'sm_wins':
            // SM events won - from rider_achievements table
            $events = $db->getAll("
                SELECT ra.id, ra.achievement_value as series_name, ra.season_year as year
                FROM rider_achievements ra
                WHERE ra.rider_id = ? AND ra.achievement_type = 'swedish_champion'
                ORDER BY ra.season_year DESC
            ", [$riderId]);
            break;

        default:
            // Generic - return recent finishes
            $events = $db->getAll("
                SELECT e.id, e.name, e.date, e.location, r.position, c.name as class_name
                FROM results r
                JOIN events e ON r.event_id = e.id
                LEFT JOIN classes c ON r.class_id = c.id
                WHERE r.cyclist_id = ? AND r.status = 'finished'
                ORDER BY e.date DESC
                LIMIT 10
            ", [$riderId]);
    }

    echo json_encode([
        'success' => true,
        'type' => $achievementType,
        'events' => $events
    ]);

} catch (Exception $e) {
    http_response_code(500);
    echo json_encode(['error' => 'Database error: ' . $e->getMessage()]);
}
