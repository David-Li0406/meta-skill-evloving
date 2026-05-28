<?php
/**
 * Setup Roger Edvinsson user account
 * Run this once to create the user, then DELETE this file!
 */

require_once __DIR__ . '/../config.php';
require_once __DIR__ . '/../hub-config.php';

// Basic HTML output
header('Content-Type: text/html; charset=utf-8');
echo "<!DOCTYPE html><html><head><title>Setup Roger</title>";
echo "<style>body{font-family:sans-serif;padding:2rem;max-width:600px;margin:0 auto}";
echo ".success{background:#d4edda;border:1px solid #c3e6cb;padding:1rem;border-radius:4px;margin:1rem 0}";
echo ".error{background:#f8d7da;border:1px solid #f5c6cb;padding:1rem;border-radius:4px;margin:1rem 0}";
echo ".info{background:#cce5ff;border:1px solid #b8daff;padding:1rem;border-radius:4px;margin:1rem 0}";
echo "pre{background:#f8f9fa;padding:1rem;border-radius:4px;overflow-x:auto}</style>";
echo "</head><body>";
echo "<h1>Setup: Roger Edvinsson</h1>";

$pdo = hub_db();

// User data
// NOTE: personnummer is no longer stored - only birth_year is used
$userData = [
    'firstname' => 'Roger',
    'lastname' => 'Edvinsson',
    'birth_year' => 1975,
    // personnummer removed 2025-12-01 - no longer stored in database
    'email' => 'roger@ecab.bike',
    'license_number' => '10079720543', // UCI-ID
    'gender' => 'M',
    'active' => 1
];

// Default password: "Gravity2025!" (change after first login)
$defaultPassword = 'Gravity2025!';
$passwordHash = password_hash($defaultPassword, PASSWORD_DEFAULT);

// Step 1: Find or create club
echo "<h2>Steg 1: Klubb</h2>";

$clubName = 'Bike Adventure CC';
$stmt = $pdo->prepare("SELECT id FROM clubs WHERE name = ?");
$stmt->execute([$clubName]);
$club = $stmt->fetch(PDO::FETCH_ASSOC);

if ($club) {
    $clubId = $club['id'];
    echo "<div class='info'>Klubb finns redan: <strong>$clubName</strong> (ID: $clubId)</div>";
} else {
    $stmt = $pdo->prepare("INSERT INTO clubs (name, country, active) VALUES (?, 'Sverige', 1)");
    $stmt->execute([$clubName]);
    $clubId = $pdo->lastInsertId();
    echo "<div class='success'>Skapade klubb: <strong>$clubName</strong> (ID: $clubId)</div>";
}

// Step 2: Check if rider exists
echo "<h2>Steg 2: Åkare</h2>";

$stmt = $pdo->prepare("SELECT id, email, password FROM riders WHERE email = ?");
$stmt->execute([$userData['email']]);
$existingRider = $stmt->fetch(PDO::FETCH_ASSOC);

if ($existingRider) {
    $riderId = $existingRider['id'];
    echo "<div class='info'>Åkare finns redan med e-post <strong>{$userData['email']}</strong> (ID: $riderId)</div>";

    // Update password if not set
    if (empty($existingRider['password'])) {
        $stmt = $pdo->prepare("UPDATE riders SET password = ? WHERE id = ?");
        $stmt->execute([$passwordHash, $riderId]);
        echo "<div class='success'>Lösenord uppdaterat!</div>";
    } else {
        echo "<div class='info'>Lösenord redan satt (ej ändrat)</div>";
    }
} else {
    // Check what columns exist in riders table
    $columns = $pdo->query("DESCRIBE riders")->fetchAll(PDO::FETCH_COLUMN);

    // Build insert query based on existing columns
    $insertFields = ['firstname', 'lastname', 'email', 'password', 'active', 'club_id'];
    $insertValues = [$userData['firstname'], $userData['lastname'], $userData['email'], $passwordHash, 1, $clubId];

    if (in_array('birth_year', $columns)) {
        $insertFields[] = 'birth_year';
        $insertValues[] = $userData['birth_year'];
    }
    // NOTE: personnummer column removed 2025-12-01 - no longer stored
    if (in_array('license_number', $columns)) {
        $insertFields[] = 'license_number';
        $insertValues[] = $userData['license_number'];
    }
    if (in_array('gender', $columns)) {
        $insertFields[] = 'gender';
        $insertValues[] = $userData['gender'];
    }
    if (in_array('role_id', $columns)) {
        $insertFields[] = 'role_id';
        $insertValues[] = ROLE_SUPER_ADMIN;
    }
    if (in_array('is_admin', $columns)) {
        $insertFields[] = 'is_admin';
        $insertValues[] = 1;
    }

    $placeholders = implode(', ', array_fill(0, count($insertFields), '?'));
    $fieldList = implode(', ', $insertFields);

    $stmt = $pdo->prepare("INSERT INTO riders ($fieldList) VALUES ($placeholders)");
    $stmt->execute($insertValues);
    $riderId = $pdo->lastInsertId();

    echo "<div class='success'>Skapade åkare: <strong>{$userData['firstname']} {$userData['lastname']}</strong> (ID: $riderId)</div>";
}

// Step 3: Ensure role_id column exists and is set
echo "<h2>Steg 3: Roll</h2>";

// Check if role_id column exists
$columns = $pdo->query("DESCRIBE riders")->fetchAll(PDO::FETCH_COLUMN);

if (!in_array('role_id', $columns)) {
    // Add role_id column
    $pdo->exec("ALTER TABLE riders ADD COLUMN role_id INT DEFAULT 1 AFTER active");
    echo "<div class='success'>Lade till role_id kolumn</div>";
}

if (!in_array('is_admin', $columns)) {
    // Add is_admin column for legacy compatibility
    $pdo->exec("ALTER TABLE riders ADD COLUMN is_admin TINYINT(1) DEFAULT 0 AFTER role_id");
    echo "<div class='success'>Lade till is_admin kolumn</div>";
}

// Update role to SUPER_ADMIN (4)
$stmt = $pdo->prepare("UPDATE riders SET role_id = ?, is_admin = 1 WHERE id = ?");
$stmt->execute([ROLE_SUPER_ADMIN, $riderId]);
echo "<div class='success'>Satte roll till <strong>SUPER_ADMIN</strong> (level 4)</div>";

// Step 4: Display summary
echo "<h2>Sammanfattning</h2>";
echo "<div class='success'>";
echo "<p><strong>Användare skapad!</strong></p>";
echo "<ul>";
echo "<li>Namn: {$userData['firstname']} {$userData['lastname']}</li>";
echo "<li>E-post: {$userData['email']}</li>";
echo "<li>Klubb: $clubName</li>";
echo "<li>UCI-ID: {$userData['license_number']}</li>";
echo "<li>Roll: Super Admin</li>";
echo "</ul>";
echo "<p><strong>Inloggningsuppgifter:</strong></p>";
echo "<ul>";
echo "<li>E-post: <code>{$userData['email']}</code></li>";
echo "<li>Lösenord: <code>$defaultPassword</code></li>";
echo "</ul>";
echo "<p style='color:#856404;background:#fff3cd;padding:0.5rem;border-radius:4px;margin-top:1rem;'>";
echo "⚠️ Byt lösenord efter första inloggningen!";
echo "</p>";
echo "</div>";

// Verify
echo "<h2>Verifiering</h2>";
$stmt = $pdo->prepare("
    SELECT r.*, c.name as club_name
    FROM riders r
    LEFT JOIN clubs c ON r.club_id = c.id
    WHERE r.id = ?
");
$stmt->execute([$riderId]);
$rider = $stmt->fetch(PDO::FETCH_ASSOC);

echo "<pre>";
echo "ID: " . $rider['id'] . "\n";
echo "Namn: " . $rider['firstname'] . " " . $rider['lastname'] . "\n";
echo "E-post: " . $rider['email'] . "\n";
echo "Klubb: " . $rider['club_name'] . "\n";
echo "Födelseår: " . ($rider['birth_year'] ?? 'Ej satt') . "\n";
echo "UCI-ID: " . ($rider['license_number'] ?? 'Ej satt') . "\n";
echo "Roll: " . ($rider['role_id'] ?? 'Ej satt') . " (" . hub_get_role_name($rider['role_id'] ?? 1) . ")\n";
echo "is_admin: " . ($rider['is_admin'] ?? 0) . "\n";
echo "Lösenord satt: " . (!empty($rider['password']) ? 'Ja' : 'Nej') . "\n";
echo "</pre>";

echo "<h2>Nästa steg</h2>";
echo "<ol>";
echo "<li>Logga in med e-post <code>{$userData['email']}</code> och lösenord <code>$defaultPassword</code></li>";
echo "<li>Byt lösenord under din profil</li>";
echo "<li><strong style='color:red;'>RADERA denna fil!</strong> <code>/admin/setup-roger.php</code></li>";
echo "</ol>";

echo "<p><a href='/login'>Gå till inloggning →</a></p>";

echo "</body></html>";
