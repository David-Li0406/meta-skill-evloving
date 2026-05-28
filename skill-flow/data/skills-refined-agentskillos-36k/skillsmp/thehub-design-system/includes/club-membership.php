<?php
/**
 * Club Membership Functions
 *
 * Handles year-based club membership tracking.
 * Club membership is locked per season/year:
 * - A rider cannot change club during a season
 * - A rider can change clubs between seasons
 */

/**
 * Get a rider's club for a specific season/year
 *
 * Logic:
 * 1. Check rider_club_seasons table for that year
 * 2. If not found, use rider's current club and optionally create entry
 *
 * @param object $db Database connection
 * @param int $riderId Rider ID
 * @param int $year Season year
 * @param bool $createIfMissing If true, creates entry if missing
 * @return int|null Club ID or null if not found
 */
function getRiderClubForYear($db, $riderId, $year, $createIfMissing = false) {
    // First check if we have a record for this rider/year
    $seasonClub = $db->getRow(
        "SELECT club_id FROM rider_club_seasons WHERE rider_id = ? AND season_year = ?",
        [$riderId, $year]
    );

    if ($seasonClub) {
        return $seasonClub['club_id'];
    }

    // No record - get the rider's current club
    $rider = $db->getRow("SELECT club_id FROM riders WHERE id = ?", [$riderId]);
    if (!$rider || !$rider['club_id']) {
        return null;
    }

    // Create entry for this year if requested
    if ($createIfMissing) {
        try {
            $db->insert('rider_club_seasons', [
                'rider_id' => $riderId,
                'club_id' => $rider['club_id'],
                'season_year' => $year,
                'locked' => 0  // Not locked yet (no results)
            ]);
        } catch (Exception $e) {
            // Might fail due to race condition - that's OK
        }
    }

    return $rider['club_id'];
}

/**
 * Set a rider's club for a specific season/year
 * Only allowed if the season is not locked (no results yet), unless force is true
 *
 * @param object $db Database connection
 * @param int $riderId Rider ID
 * @param int $clubId Club ID
 * @param int $year Season year
 * @param bool $force Force update even if locked (super admin only)
 * @return array ['success' => bool, 'message' => string]
 */
function setRiderClubForYear($db, $riderId, $clubId, $year, $force = false) {
    try {
        // Check if there's an existing locked entry
        $existing = $db->getRow(
            "SELECT id, locked FROM rider_club_seasons WHERE rider_id = ? AND season_year = ?",
            [$riderId, $year]
        );

        if ($existing) {
            if ($existing['locked'] && !$force) {
                return [
                    'success' => false,
                    'message' => "Kan inte byta klubb för {$year} - åkaren har redan resultat det året"
                ];
            }

            // Update existing entry (force allows updating locked entries)
            $result = $db->update('rider_club_seasons', [
                'club_id' => $clubId
            ], 'id = ?', [$existing['id']]);

            $forceNote = $force && $existing['locked'] ? ' (forced by super admin)' : '';
            error_log("setRiderClubForYear: Updated existing entry{$forceNote}, result={$result}");
        } else {
            // Create new entry
            $insertId = $db->insert('rider_club_seasons', [
                'rider_id' => $riderId,
                'club_id' => $clubId,
                'season_year' => $year,
                'locked' => 0
            ]);

            error_log("setRiderClubForYear: Created new entry, insertId={$insertId}");

            if (!$insertId) {
                return [
                    'success' => false,
                    'message' => "Kunde inte skapa klubbkoppling - kontrollera att tabellen rider_club_seasons finns"
                ];
            }
        }

        return [
            'success' => true,
            'message' => "Klubb uppdaterad för {$year}"
        ];
    } catch (Exception $e) {
        error_log("setRiderClubForYear: Exception - " . $e->getMessage());
        return [
            'success' => false,
            'message' => "Databasfel: " . $e->getMessage()
        ];
    }
}

/**
 * Lock a rider's club for a season (called when result is added)
 *
 * @param object $db Database connection
 * @param int $riderId Rider ID
 * @param int $year Season year
 */
function lockRiderClubForYear($db, $riderId, $year) {
    $db->query(
        "UPDATE rider_club_seasons SET locked = 1 WHERE rider_id = ? AND season_year = ?",
        [$riderId, $year]
    );
}

/**
 * Get a rider's club history (all seasons)
 *
 * @param object $db Database connection
 * @param int $riderId Rider ID
 * @return array List of club memberships by year
 */
function getRiderClubHistory($db, $riderId) {
    return $db->getAll("
        SELECT rcs.season_year, rcs.club_id, c.name as club_name, rcs.locked,
               (SELECT COUNT(*) FROM results r
                JOIN events e ON r.event_id = e.id
                WHERE r.cyclist_id = rcs.rider_id AND YEAR(e.date) = rcs.season_year) as results_count
        FROM rider_club_seasons rcs
        JOIN clubs c ON rcs.club_id = c.id
        WHERE rcs.rider_id = ?
        ORDER BY rcs.season_year DESC
    ", [$riderId]);
}

/**
 * Check if a rider can change club for a given year
 *
 * @param object $db Database connection
 * @param int $riderId Rider ID
 * @param int $year Season year
 * @return bool True if club can be changed
 */
function canChangeClubForYear($db, $riderId, $year) {
    // Check if there's already a club set for this year
    $existingClub = $db->getRow(
        "SELECT club_id FROM rider_club_seasons WHERE rider_id = ? AND season_year = ?",
        [$riderId, $year]
    );

    // If no club is set yet, allow setting one (even if results exist)
    if (!$existingClub || !$existingClub['club_id']) {
        return true;
    }

    // If club is already set, only allow changing if no results exist
    $hasResults = $db->getRow("
        SELECT 1 FROM results r
        JOIN events e ON r.event_id = e.id
        WHERE r.cyclist_id = ? AND YEAR(e.date) = ?
        LIMIT 1
    ", [$riderId, $year]);

    return !$hasResults;
}

/**
 * Get club ID from result's club_id or from season table
 * Used when displaying results to ensure correct club is shown
 *
 * @param object $db Database connection
 * @param array $result Result row with at least cyclist_id and event_id
 * @param string $eventDate Event date (Y-m-d format)
 * @return int|null Club ID
 */
function getClubIdForResult($db, $result, $eventDate) {
    // If result already has club_id, use it
    if (!empty($result['club_id'])) {
        return $result['club_id'];
    }

    // Otherwise look up from rider_club_seasons
    $year = (int)date('Y', strtotime($eventDate));
    return getRiderClubForYear($db, $result['cyclist_id'], $year, false);
}
