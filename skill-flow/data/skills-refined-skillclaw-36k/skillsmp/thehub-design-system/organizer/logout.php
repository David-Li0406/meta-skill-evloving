<?php
/**
 * Organizer App - Logout
 */

require_once __DIR__ . '/config.php';

logout();

header('Location: index.php');
exit;
