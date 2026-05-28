<?php
/**
 * API: Search Riders
 * Returns matching riders for registration form and admin user linking
 *
 * Parameters:
 * - q: search query (required, min 2 chars)
 * - limit: max results (default 10, max 50)
 * - activated: if set, only return riders with activated accounts (password set)
 * - with_club: if set, only return riders with a club assigned
 */

require_once __DIR__ . '/../config.php';

header('Content-Type: application/json');

$query = trim($_GET['q'] ?? '');
$limit = isset($_GET['limit']) ? min(50, max(1, intval($_GET['limit']))) : 10;
$activatedOnly = isset($_GET['activated']);
$withClubOnly = isset($_GET['with_club']);

if (strlen($query) < 2) {
    echo json_encode(['riders' => []]);
    exit;
}

$db = getDB();

// Search by name, UCI ID, or email
$searchTerm = '%' . $query . '%';
$currentYear = (int)date('Y');

// Build WHERE conditions
$conditions = [
    "(r.firstname LIKE ? OR r.lastname LIKE ? OR CONCAT(r.firstname, ' ', r.lastname) LIKE ? OR r.license_number LIKE ? OR r.email LIKE ?)"
];
$params = [$currentYear, $searchTerm, $searchTerm, $searchTerm, $searchTerm, $searchTerm];

if ($activatedOnly) {
    $conditions[] = "r.password IS NOT NULL AND r.password != ''";
}

if ($withClubOnly) {
    $conditions[] = "r.club_id IS NOT NULL";
}

$whereClause = implode(' AND ', $conditions);

$riders = $db->getAll("
    SELECT
        r.id,
        r.firstname,
        r.lastname,
        r.license_number,
        r.license_number as uci_id,
        r.email,
        r.gravity_id,
        r.license_type,
        r.license_year,
        r.license_valid_until,
        r.birth_year,
        r.gender,
        r.club_id,
        COALESCE(c.name, c_season.name) as club_name,
        CASE
            WHEN r.license_year = ? AND r.license_type IS NOT NULL AND r.license_type != ''
                AND r.license_type NOT IN ('engangslicens', 'Engångslicens', 'sweid', 'SWE ID')
            THEN 1
            WHEN r.license_valid_until >= CURDATE() AND r.license_type IS NOT NULL AND r.license_type != ''
                AND r.license_type NOT IN ('engangslicens', 'Engångslicens', 'sweid', 'SWE ID')
            THEN 1
            ELSE 0
        END as has_active_license
    FROM riders r
    LEFT JOIN clubs c ON r.club_id = c.id
    LEFT JOIN (
        SELECT rider_id, club_id
        FROM rider_club_seasons rcs1
        WHERE season_year = (SELECT MAX(season_year) FROM rider_club_seasons rcs2 WHERE rcs2.rider_id = rcs1.rider_id)
    ) rcs_latest ON rcs_latest.rider_id = r.id AND r.club_id IS NULL
    LEFT JOIN clubs c_season ON rcs_latest.club_id = c_season.id
    WHERE {$whereClause}
    ORDER BY r.lastname, r.firstname
    LIMIT {$limit}
", $params);

echo json_encode(['riders' => $riders]);
