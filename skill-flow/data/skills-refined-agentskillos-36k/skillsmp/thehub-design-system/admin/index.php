<?php
/**
 * Admin Index - Redirects to dashboard
 */
require_once __DIR__ . '/../config.php';
require_admin();
redirect('/admin/dashboard.php');
