<?php
/**
 * API: Add Comment to Race Report
 * POST /api/news/comment.php
 */

header('Content-Type: application/json');

require_once __DIR__ . '/../../hub-config.php';

// Check if user is logged in
$currentUser = function_exists('hub_current_user') ? hub_current_user() : null;

if (!$currentUser) {
    http_response_code(401);
    echo json_encode(['success' => false, 'error' => 'Du maste vara inloggad for att kommentera.']);
    exit;
}

// Get request data
$data = json_decode(file_get_contents('php://input'), true);
$reportId = (int)($data['report_id'] ?? 0);
$comment = trim($data['comment'] ?? '');
$parentId = !empty($data['parent_id']) ? (int)$data['parent_id'] : null;

if ($reportId <= 0) {
    http_response_code(400);
    echo json_encode(['success' => false, 'error' => 'Ogiltigt inlaggs-ID.']);
    exit;
}

if (empty($comment)) {
    http_response_code(400);
    echo json_encode(['success' => false, 'error' => 'Kommentaren kan inte vara tom.']);
    exit;
}

if (strlen($comment) > 2000) {
    http_response_code(400);
    echo json_encode(['success' => false, 'error' => 'Kommentaren ar for lang (max 2000 tecken).']);
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

// Check if comments are allowed
if (!$report['allow_comments']) {
    http_response_code(403);
    echo json_encode(['success' => false, 'error' => 'Kommentarer ar inte tillatet pa detta inlagg.']);
    exit;
}

// Add comment
$commentId = $reportManager->addComment($reportId, $currentUser['id'], $comment, $parentId);

if ($commentId) {
    echo json_encode([
        'success' => true,
        'comment_id' => $commentId,
        'message' => 'Kommentar tillagd!'
    ]);
} else {
    http_response_code(500);
    echo json_encode(['success' => false, 'error' => 'Kunde inte spara kommentar.']);
}
