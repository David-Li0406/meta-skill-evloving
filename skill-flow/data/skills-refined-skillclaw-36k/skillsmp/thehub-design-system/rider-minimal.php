<?php
error_reporting(E_ALL);
ini_set('display_errors', 1);

require_once __DIR__ . '/config.php';
$db = getDB();

$riderId = isset($_GET['id']) ? (int)$_GET['id'] : 7761;

// Fetch rider
$rider = $db->getRow("
    SELECT
        r.id,
        r.firstname,
        r.lastname,
        r.birth_year,
        r.gender,
        r.club_id,
        r.license_number,
        r.license_type,
        r.license_year,
        c.name as club_name
    FROM riders r
    LEFT JOIN clubs c ON r.club_id = c.id
    WHERE r.id = ?
", [$riderId]);

if (!$rider) {
    die("Rider not found");
}

$currentYear = date('Y');
$age = $rider['birth_year'] ? ($currentYear - $rider['birth_year']) : null;

// Check license
$licenseCheck = checkLicense($rider);

// Simple HTML output
?>
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title><?= h($rider['firstname'] . ' ' . $rider['lastname']) ?></title>
    <style>
        body { font-family: Arial; padding: 20px; }
        .card { border: 1px solid #ccc; padding: 20px; max-width: 600px; }
        .success { color: green; }
        .danger { color: red; }
    </style>
</head>
<body>
    <div class="card">
        <h1><?= h($rider['firstname']) ?> <?= h($rider['lastname']) ?></h1>

        <p><strong>ID:</strong> <?= $rider['id'] ?></p>
        <p><strong>License Number:</strong> <?= h($rider['license_number']) ?></p>
        <p><strong>License Type:</strong> <?= h($rider['license_type']) ?></p>
        <p><strong>License Year:</strong> <?= $rider['license_year'] ?></p>

        <p><strong>License Status:</strong>
            <span class="<?= $licenseCheck['valid'] ? 'success' : 'danger' ?>">
                <?= $licenseCheck['message'] ?>
            </span>
        </p>

        <p><strong>Ålder:</strong> <?= $age ?> år</p>
        <p><strong>Kön:</strong> <?= $rider['gender'] === 'M' ? 'Man' : 'Kvinna' ?></p>
        <p><strong>Klubb:</strong> <?= h($rider['club_name']) ?></p>

        <hr>
        <p><a href="/riders.php">← Tillbaka till deltagare</a></p>
        <p><a href="/rider.php?id=<?= $rider['id'] ?>">View full rider.php (may be blank)</a></p>
    </div>
</body>
</html>
