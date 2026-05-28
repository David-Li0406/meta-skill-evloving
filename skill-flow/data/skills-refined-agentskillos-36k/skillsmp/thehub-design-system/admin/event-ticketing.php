<?php
/**
 * Event Ticketing - Redirect to Event Payment
 * All ticketing/payment config is now in event-payment.php
 */

require_once __DIR__ . '/../config.php';
require_admin();

$eventId = isset($_GET['id']) ? intval($_GET['id']) : 0;

if ($eventId > 0) {
    header('Location: /admin/event-payment.php?id=' . $eventId);
} else {
    header('Location: /admin/orders.php');
}
exit;
