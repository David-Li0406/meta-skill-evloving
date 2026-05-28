<?php
/**
 * TheHUB Search API
 * Live search endpoint for riders and clubs
 * Respects public_riders_display setting from admin
 */

require_once dirname(__DIR__) . '/config.php';

header('Content-Type: application/json');
header('Cache-Control: no-store');

$query = trim($_GET['q'] ?? '');
$type = $_GET['type'] ?? 'all';
$limit = min(intval($_GET['limit'] ?? 10), 20);

// Load filter setting from admin configuration
$publicSettings = @include(dirname(__DIR__) . '/config/public_settings.php');
$filter = $publicSettings['public_riders_display'] ?? 'all';

if (strlen($query) < 2) {
    echo json_encode(['results' => [], 'query' => $query]);
    exit;
}

try {
    // Use global $pdo from config.php (hub_db() is only in hub-config.php)
    global $pdo;
    $results = [];

    // Search riders
    if ($type === 'all' || $type === 'riders') {
        // Build query based on filter setting
        if ($filter === 'with_results') {
            // Only show riders who have at least one result
            $stmt = $pdo->prepare("
                SELECT DISTINCT r.id, r.firstname, r.lastname, c.name as club_name
                FROM riders r
                LEFT JOIN clubs c ON r.club_id = c.id
                INNER JOIN results res ON r.id = res.cyclist_id
                WHERE (CONCAT(r.firstname, ' ', r.lastname) LIKE ?
                   OR r.firstname LIKE ?
                   OR r.lastname LIKE ?)
                ORDER BY
                    CASE
                        WHEN CONCAT(r.firstname, ' ', r.lastname) LIKE ? THEN 1
                        WHEN r.firstname LIKE ? THEN 2
                        ELSE 3
                    END,
                    r.lastname, r.firstname
                LIMIT ?
            ");
        } else {
            // Show all riders
            $stmt = $pdo->prepare("
                SELECT r.id, r.firstname, r.lastname, c.name as club_name
                FROM riders r
                LEFT JOIN clubs c ON r.club_id = c.id
                WHERE CONCAT(r.firstname, ' ', r.lastname) LIKE ?
                   OR r.firstname LIKE ?
                   OR r.lastname LIKE ?
                ORDER BY
                    CASE
                        WHEN CONCAT(r.firstname, ' ', r.lastname) LIKE ? THEN 1
                        WHEN r.firstname LIKE ? THEN 2
                        ELSE 3
                    END,
                    r.lastname, r.firstname
                LIMIT ?
            ");
        }

        $searchPattern = "%{$query}%";
        $startPattern = "{$query}%";
        $stmt->execute([$searchPattern, $searchPattern, $searchPattern, $startPattern, $startPattern, $limit]);

        foreach ($stmt->fetchAll(PDO::FETCH_ASSOC) as $row) {
            $results[] = [
                'id' => $row['id'],
                'type' => 'rider',
                'firstname' => $row['firstname'],
                'lastname' => $row['lastname'],
                'club_name' => $row['club_name'] ?? ''
            ];
        }
    }

    // Search clubs
    if ($type === 'all' || $type === 'clubs') {
        $remainingLimit = $limit - count($results);
        if ($remainingLimit > 0) {
            $stmt = $pdo->prepare("
                SELECT c.id, c.name, COUNT(r.id) as member_count
                FROM clubs c
                LEFT JOIN riders r ON c.id = r.club_id
                WHERE c.name LIKE ?
                GROUP BY c.id
                ORDER BY
                    CASE WHEN c.name LIKE ? THEN 1 ELSE 2 END,
                    c.name
                LIMIT ?
            ");

            $searchPattern = "%{$query}%";
            $startPattern = "{$query}%";
            $stmt->execute([$searchPattern, $startPattern, $remainingLimit]);

            foreach ($stmt->fetchAll(PDO::FETCH_ASSOC) as $row) {
                $results[] = [
                    'id' => $row['id'],
                    'type' => 'club',
                    'name' => $row['name'],
                    'member_count' => $row['member_count']
                ];
            }
        }
    }

    echo json_encode([
        'results' => $results,
        'query' => $query,
        'type' => $type,
        'count' => count($results)
    ]);

} catch (Exception $e) {
    http_response_code(500);
    echo json_encode([
        'error' => true,
        'message' => 'Search error: ' . $e->getMessage(),
        'query' => $query
    ]);
    error_log('Search API error: ' . $e->getMessage());
}
