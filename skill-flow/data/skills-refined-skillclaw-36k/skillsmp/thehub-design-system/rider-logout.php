<?php
require_once __DIR__ . '/config.php';
require_once __DIR__ . '/includes/rider-auth.php';

rider_logout();

// Redirect to homepage or login page
header('Location: /rider-login.php?logged_out=1');
exit;
