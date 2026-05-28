<?php
ini_set('display_errors', 1);
error_reporting(E_ALL);

/**
 * Club Points System for TheHUB
 *
 * Calculates and caches club standings for series with format='Team'.
 * Uses events linked to the series via series_id.
 *
 * Point Rules:
 * - Best rider from each club per class/event: 100% of earned points
 * - Second best rider from same club/class/event: 50% of earned points
 * - All other riders from same club/class/event: 0% (not counted)
 */

/**
 * Calculate club points for a specific event in a series
 */
function calculateEventClubPoints($db, $eventId, $seriesId) {
    $stats = [
        'clubs_processed' => 0,
        'riders_processed' => 0,
        'total_points' => 0
    ];

    // Clear existing points for this event/series
    $db->delete('club_rider_points', 'event_id = ? AND series_id = ?', [$eventId, $seriesId]);
    $db->delete('club_event_points', 'event_id = ? AND series_id = ?', [$eventId, $seriesId]);

    // Get the event year for club membership lookup
    $eventInfo = $db->getRow("SELECT YEAR(date) as event_year FROM events WHERE id = ?", [$eventId]);
    $eventYear = $eventInfo['event_year'] ?? date('Y');

    // Get all results for this event grouped by club and class
    // Only include riders with clubs and finished status
    // IMPORTANT: Uses rider_club_seasons for the event year, falls back to riders.club_id
    $results = $db->getAll("
        SELECT
            r.id as result_id,
            r.cyclist_id,
            r.class_id,
            r.points,
            COALESCE(rcs.club_id, rd.club_id) as club_id,
            rd.firstname,
            rd.lastname
        FROM results r
        JOIN riders rd ON r.cyclist_id = rd.id
        JOIN classes c ON r.class_id = c.id
        LEFT JOIN rider_club_seasons rcs ON rcs.rider_id = rd.id AND rcs.season_year = ?
        WHERE r.event_id = ?
        AND r.status = 'finished'
        AND COALESCE(rcs.club_id, rd.club_id) IS NOT NULL
        AND r.points > 0
        AND COALESCE(c.series_eligible, 1) = 1
        AND COALESCE(c.awards_points, 1) = 1
        ORDER BY COALESCE(rcs.club_id, rd.club_id), r.class_id, r.points DESC
    ", [$eventYear, $eventId]);

    if (empty($results)) {
        return $stats;
    }

    // Group results by club and class
    $clubClassResults = [];
    foreach ($results as $result) {
        $key = $result['club_id'] . '_' . $result['class_id'];
        if (!isset($clubClassResults[$key])) {
            $clubClassResults[$key] = [];
        }
        $clubClassResults[$key][] = $result;
    }

    // Calculate points for each club/class combination
    $clubEventPoints = [];

    foreach ($clubClassResults as $key => $riders) {
        list($clubId, $classId) = explode('_', $key);

        if (!isset($clubEventPoints[$clubId])) {
            $clubEventPoints[$clubId] = [
                'total_points' => 0,
                'participants_count' => 0,
                'scoring_riders' => 0
            ];
        }

        $rank = 1;
        foreach ($riders as $rider) {
            $originalPoints = (float)$rider['points'];
            $clubPoints = 0;
            $percentage = 0;

            if ($rank === 1) {
                $clubPoints = $originalPoints;
                $percentage = 100;
            } elseif ($rank === 2) {
                $clubPoints = round($originalPoints * 0.5, 2);
                $percentage = 50;
            }

            // Insert rider points record
            $db->insert('club_rider_points', [
                'club_id' => $clubId,
                'event_id' => $eventId,
                'series_id' => $seriesId,
                'rider_id' => $rider['cyclist_id'],
                'class_id' => $classId,
                'original_points' => $originalPoints,
                'club_points' => $clubPoints,
                'rider_rank_in_club' => $rank,
                'percentage_applied' => $percentage
            ]);

            $clubEventPoints[$clubId]['total_points'] += $clubPoints;
            $clubEventPoints[$clubId]['participants_count']++;
            if ($clubPoints > 0) {
                $clubEventPoints[$clubId]['scoring_riders']++;
            }

            $stats['riders_processed']++;
            $stats['total_points'] += $clubPoints;
            $rank++;
        }
    }

    // Insert club event points
    foreach ($clubEventPoints as $clubId => $data) {
        $db->insert('club_event_points', [
            'club_id' => $clubId,
            'event_id' => $eventId,
            'series_id' => $seriesId,
            'total_points' => $data['total_points'],
            'participants_count' => $data['participants_count'],
            'scoring_riders' => $data['scoring_riders']
        ]);
        $stats['clubs_processed']++;
    }

    return $stats;
}

/**
 * Recalculate all club points for a series
 */
function recalculateSeriesClubPoints($db, $seriesId) {
    $stats = [
        'events_processed' => 0,
        'total_clubs' => 0,
        'total_points' => 0
    ];

    // Get all events in this series via junction table
    $events = $db->getAll("
        SELECT e.id, e.name, e.date
        FROM series_events se
        JOIN events e ON se.event_id = e.id
        WHERE se.series_id = ?
        ORDER BY se.sort_order ASC, e.date ASC
    ", [$seriesId]);

    // Calculate points for each event
    foreach ($events as $event) {
        $eventStats = calculateEventClubPoints($db, $event['id'], $seriesId);
        $stats['events_processed']++;
        $stats['total_points'] += $eventStats['total_points'];
    }

    // Refresh the standings cache
    $cacheStats = refreshSeriesStandingsCache($db, $seriesId);
    $stats['total_clubs'] = $cacheStats['clubs_updated'];

    return $stats;
}

/**
 * Refresh the standings cache for a series
 */
function refreshSeriesStandingsCache($db, $seriesId) {
    $stats = ['clubs_updated' => 0];

    // Clear existing cache
    $db->delete('club_standings_cache', 'series_id = ?', [$seriesId]);

    // Aggregate club points with unique rider count
    $clubStats = $db->getAll("
        SELECT
            cep.club_id,
            SUM(cep.total_points) as total_points,
            (SELECT COUNT(DISTINCT rider_id) FROM club_rider_points
             WHERE club_id = cep.club_id AND series_id = ?) as total_participants,
            COUNT(cep.event_id) as events_count,
            MAX(cep.total_points) as best_event_points
        FROM club_event_points cep
        WHERE cep.series_id = ?
        GROUP BY cep.club_id
        HAVING SUM(cep.total_points) > 0
        ORDER BY SUM(cep.total_points) DESC
    ", [$seriesId, $seriesId]);

    // Insert with rankings
    $rank = 1;
    $prevPoints = null;
    $prevRank = 1;

    foreach ($clubStats as $club) {
        // Handle ties
        if ($prevPoints !== null && $club['total_points'] == $prevPoints) {
            $currentRank = $prevRank;
        } else {
            $currentRank = $rank;
            $prevRank = $rank;
        }
        $prevPoints = $club['total_points'];

        $db->insert('club_standings_cache', [
            'club_id' => $club['club_id'],
            'series_id' => $seriesId,
            'total_points' => $club['total_points'],
            'total_participants' => $club['total_participants'],
            'events_count' => $club['events_count'],
            'best_event_points' => $club['best_event_points'],
            'ranking' => $currentRank
        ]);

        $stats['clubs_updated']++;
        $rank++;
    }

    return $stats;
}

/**
 * Get club standings for a series
 */
function getClubStandings($db, $seriesId, $limit = 0) {
    $sql = "
        SELECT
            csc.ranking,
            csc.total_points,
            csc.total_participants,
            csc.events_count,
            csc.best_event_points,
            c.id as club_id,
            c.name as club_name,
            c.short_name,
            c.city,
            c.region,
            c.logo
        FROM club_standings_cache csc
        JOIN clubs c ON csc.club_id = c.id
        WHERE csc.series_id = ?
        ORDER BY csc.ranking ASC, csc.total_points DESC
    ";

    if ($limit > 0) {
        $sql .= " LIMIT " . (int)$limit;
    }

    return $db->getAll($sql, [$seriesId]);
}

/**
 * Get detailed club breakdown for a series
 */
function getClubPointsDetail($db, $clubId, $seriesId) {
    // Get club info
    $club = $db->getRow("SELECT * FROM clubs WHERE id = ?", [$clubId]);
    if (!$club) {
        return null;
    }

    // Get standing info
    $standing = $db->getRow("
        SELECT * FROM club_standings_cache
        WHERE club_id = ? AND series_id = ?
    ", [$clubId, $seriesId]);

    // Get event breakdown
    $events = $db->getAll("
        SELECT
            cep.event_id,
            cep.total_points,
            cep.participants_count,
            cep.scoring_riders,
            e.name as event_name,
            e.date as event_date,
            e.location
        FROM club_event_points cep
        JOIN events e ON cep.event_id = e.id
        WHERE cep.club_id = ? AND cep.series_id = ?
        ORDER BY e.date ASC
    ", [$clubId, $seriesId]);

    // Get rider breakdown per event
    $riderDetails = [];
    foreach ($events as $event) {
        $riders = $db->getAll("
            SELECT
                crp.rider_id,
                crp.class_id,
                crp.original_points,
                crp.club_points,
                crp.rider_rank_in_club,
                crp.percentage_applied,
                r.firstname,
                r.lastname,
                cls.display_name as class_name
            FROM club_rider_points crp
            JOIN riders r ON crp.rider_id = r.id
            LEFT JOIN classes cls ON crp.class_id = cls.id
            WHERE crp.club_id = ? AND crp.event_id = ? AND crp.series_id = ?
            ORDER BY crp.club_points DESC, crp.original_points DESC
        ", [$clubId, $event['event_id'], $seriesId]);

        $riderDetails[$event['event_id']] = $riders;
    }

    return [
        'club' => $club,
        'standing' => $standing,
        'events' => $events,
        'rider_details' => $riderDetails
    ];
}

/**
 * Get all series with format='Team' (club point series)
 */
function getTeamSeries($db) {
    return $db->getAll("
        SELECT
            s.*,
            COUNT(se.event_id) as event_count
        FROM series s
        LEFT JOIN series_events se ON s.id = se.series_id
        WHERE s.format = 'Team'
        GROUP BY s.id
        ORDER BY s.year DESC, s.name ASC
    ");
}

/**
 * Get series info with event count
 */
function getSeriesWithEvents($db, $seriesId) {
    $series = $db->getRow("SELECT * FROM series WHERE id = ?", [$seriesId]);
    if (!$series) {
        return null;
    }

    $events = $db->getAll("
        SELECT e.id, e.name, e.date, e.location
        FROM series_events se
        JOIN events e ON se.event_id = e.id
        WHERE se.series_id = ?
        ORDER BY se.sort_order ASC, e.date ASC
    ", [$seriesId]);

    $series['events'] = $events;
    return $series;
}

/**
 * Check if club points tables exist
 */
function clubPointsTablesExist($db) {
    try {
        $tables = $db->getAll("SHOW TABLES LIKE 'club_standings_cache'");
        return !empty($tables);
    } catch (Exception $e) {
        return false;
    }
}
