<?php
/**
 * TheHUB V3 API - Content Endpoint
 *
 * This file serves as a placeholder for future API endpoints.
 * Add database connectivity and data fetching logic here.
 */

require_once __DIR__ . '/../config.php';

header('Content-Type: application/json; charset=utf-8');
header('X-Content-Type-Options: nosniff');

// Simple API response helper
function api_response(array $data, int $status = 200): void {
    http_response_code($status);
    echo json_encode($data, JSON_UNESCAPED_UNICODE | JSON_PRETTY_PRINT);
    exit;
}

// Get request type
$action = $_GET['action'] ?? '';

switch ($action) {
    case 'ping':
        api_response([
            'status' => 'ok',
            'version' => HUB_VERSION,
            'timestamp' => date('c')
        ]);
        break;

    default:
        api_response([
            'error' => 'Unknown action',
            'available_actions' => ['ping']
        ], 400);
}
