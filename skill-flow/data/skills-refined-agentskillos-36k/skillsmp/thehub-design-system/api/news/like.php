<?php
/**
 * API: Toggle Like on Race Report
 * POST /api/news/like.php
 */

header('Content-Type: application/json');

require_once __DIR__ . '/../../hub-config.php';

// Check if user is logged in
$currentUser = function_exists('hub_current_user') ? hub_current_user() : null;

if (!$currentUser) {
    http_response_code(401);
    echo json_encode(['success' => false, 'error' => 'Du maste vara inloggad for att gilla inlagg.']);
    exit;
}

// Get request data
$data = json_decode(file_get_contents('php://input'), true);
$reportId = (int)($data['report_id'] ?? 0);

if ($reportId <= 0) {
    http_response_code(400);
    echo json_encode(['success' => false, 'error' => 'Ogiltigt inlaggs-ID.']);
    exit;
}

$pdo = hub_db();

// Include RaceReportManager
require_once HUB_ROOT . '/includes/RaceReportManager.php';
$reportManager = new RaceReportManager($pdo);

// Verify report exists and is published
$report = $reportManager->getReport($reportId, true);
if (!$report) {
    http_response_code(404);
    echo json_encode(['success' => false, 'error' => 'Inlagg hittades inte.']);
    exit;
}

// Toggle like
$liked = $reportManager->toggleLike($reportId, $currentUser['id']);

// Get updated like count
$stmt = $pdo->prepare("SELECT likes FROM race_reports WHERE id = ?");
$stmt->execute([$reportId]);
$likes = (int)$stmt->fetchColumn();

echo json_encode([
    'success' => true,
    'liked' => $liked,
    'likes' => $likes
]);
