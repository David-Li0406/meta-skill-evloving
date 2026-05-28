<?php
require_once __DIR__ . '/../config.php';
require_once __DIR__ . '/../includes/point-calculations.php';

header('Content-Type: application/json');

$db = getDB();

if (!isset($_GET['scale_id'])) {
    http_response_code(400);
    echo json_encode(['error' => 'scale_id required']);
    exit;
}

$scaleId = (int)$_GET['scale_id'];

$values = getScaleValues($db, $scaleId);

echo json_encode($values);
