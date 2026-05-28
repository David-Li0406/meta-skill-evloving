<?php
/**
 * API endpoint to get classes for a specific event
 */
require_once __DIR__ . '/../../config.php';
require_admin();

header('Content-Type: application/json');

$eventId = (int)($_GET['event_id'] ?? 0);

if (!$eventId) {
    echo json_encode([]);
    exit;
}

$db = getDB();

$classes = $db->getAll("
    SELECT DISTINCT c.id, c.display_name, c.sort_order
    FROM classes c
    INNER JOIN results r ON c.id = r.class_id
    WHERE r.event_id = ?
    ORDER BY c.sort_order
", [$eventId]);

echo json_encode($classes);
