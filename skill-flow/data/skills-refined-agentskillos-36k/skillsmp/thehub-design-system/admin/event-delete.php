<?php
require_once __DIR__ . '/../config.php';
require_admin();

$db = getDB();

// Only accept POST requests
if ($_SERVER['REQUEST_METHOD'] !==  'POST') {
    header('Location: /admin/events.php');
    exit;
}

checkCsrf();

$id = isset($_POST['id']) ? intval($_POST['id']) : 0;

if ($id <= 0) {
    $_SESSION['message'] = 'Ogiltigt event-ID';
    $_SESSION['messageType'] = 'error';
    header('Location: /admin/events.php');
    exit;
}

try {
    // Get event name for confirmation
    $event = $db->getRow("SELECT name FROM events WHERE id = ?", [$id]);

    if (!$event) {
        $_SESSION['message'] = 'Event hittades inte';
        $_SESSION['messageType'] = 'error';
    } else {
        // Delete the event
        $db->delete('events', 'id = ?', [$id]);
        $_SESSION['message'] = 'Event "' . htmlspecialchars($event['name']) . '" borttaget!';
        $_SESSION['messageType'] = 'success';
    }
} catch (Exception $e) {
    $_SESSION['message'] = 'Ett fel uppstod: ' . $e->getMessage();
    $_SESSION['messageType'] = 'error';
}

header('Location: /admin/events.php');
exit;
