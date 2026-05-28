<?php
require_once __DIR__ . '/../config.php';
require_once __DIR__ . '/../hub-config.php';

header('Content-Type: application/json');

$riderId = 23988;
global $pdo;

// Check admin status
$isSuperAdmin = function_exists('hub_is_super_admin') && hub_is_super_admin();

// Get rider data
$stmt = $pdo->prepare("SELECT id, email, password, firstname, lastname FROM riders WHERE id = ?");
$stmt->execute([$riderId]);
$rider = $stmt->fetch(PDO::FETCH_ASSOC);

echo json_encode([
    'session' => [
        'admin_logged_in' => $_SESSION['admin_logged_in'] ?? null,
        'admin_role' => $_SESSION['admin_role'] ?? null,
        'admin_username' => $_SESSION['admin_username'] ?? null,
        'hub_user_role' => $_SESSION['hub_user_role'] ?? null,
    ],
    'checks' => [
        'hub_is_super_admin_exists' => function_exists('hub_is_super_admin'),
        'isSuperAdmin' => $isSuperAdmin,
        'canActivateProfile' => $isSuperAdmin && $rider && !empty($rider['email']) && empty($rider['password']),
    ],
    'rider' => $rider ? [
        'id' => $rider['id'],
        'name' => $rider['firstname'] . ' ' . $rider['lastname'],
        'has_email' => !empty($rider['email']),
        'email' => $rider['email'] ?? '(none)',
        'has_password' => !empty($rider['password']),
    ] : null,
], JSON_PRETTY_PRINT);
