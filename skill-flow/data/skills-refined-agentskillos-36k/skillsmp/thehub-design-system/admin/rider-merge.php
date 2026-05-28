<?php
/**
 * Rider Merge - Redirect wrapper
 *
 * Parses comma-separated IDs and redirects to merge-specific-riders.php
 */
require_once __DIR__ . '/../config.php';
require_admin();

$ids = $_GET['ids'] ?? '';

// Parse comma-separated IDs
$idArray = array_map('intval', array_filter(preg_split('/[,\s]+/', $ids)));

if (count($idArray) < 2) {
    header('Location: /admin/find-duplicates');
    exit;
}

// Redirect to merge-specific-riders with first two IDs
$id1 = $idArray[0];
$id2 = $idArray[1];

header("Location: /admin/merge-specific-riders.php?id1={$id1}&id2={$id2}");
exit;
