<?php
/**
 * API: Save Data Quality Metrics
 *
 * Sparar datakvalitetsmatning till databasen.
 */

header('Content-Type: application/json');

require_once __DIR__ . '/../../config/database.php';
require_once __DIR__ . '/../../includes/auth.php';

// Krav: Admin eller statistics permission
if (!isAdmin() && !hasPermission('statistics')) {
    http_response_code(403);
    echo json_encode(['success' => false, 'error' => 'Unauthorized']);
    exit;
}

require_once __DIR__ . '/../../analytics/includes/KPICalculator.php';

$year = isset($_GET['year']) ? (int)$_GET['year'] : (int)date('Y');

if ($year < 2010 || $year > 2030) {
    echo json_encode(['success' => false, 'error' => 'Invalid year']);
    exit;
}

try {
    $pdo = hub_db();
    $kpi = new KPICalculator($pdo);

    $success = $kpi->saveDataQualityMetrics($year);

    echo json_encode([
        'success' => $success,
        'year' => $year,
        'timestamp' => date('Y-m-d H:i:s'),
    ]);

} catch (Exception $e) {
    http_response_code(500);
    echo json_encode([
        'success' => false,
        'error' => $e->getMessage(),
    ]);
}
