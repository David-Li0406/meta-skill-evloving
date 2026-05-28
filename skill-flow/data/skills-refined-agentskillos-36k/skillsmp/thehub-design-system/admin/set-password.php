<?php
/**
 * Set password for a rider account
 * Only accessible to already logged in admin or via CLI
 */

require_once __DIR__ . '/../config.php';

// Security: Only allow from CLI or logged in admin
$isCli = php_sapi_name() === 'cli';
$isAdmin = isset($_SESSION['admin_logged_in']) && $_SESSION['admin_logged_in'] === true;

if (!$isCli && !$isAdmin) {
    die('Access denied. Login to admin panel first or run from CLI.');
}

$pdo = $GLOBALS['pdo'];

// CLI mode
if ($isCli) {
    if ($argc < 3) {
        echo "Usage: php set-password.php <email> <new_password>\n";
        echo "Example: php set-password.php roger@example.com MyNewPassword123\n";
        exit(1);
    }

    $email = $argv[1];
    $newPassword = $argv[2];

    // Find rider
    $stmt = $pdo->prepare("SELECT id, email, firstname, lastname, role_id FROM riders WHERE email = ?");
    $stmt->execute([$email]);
    $rider = $stmt->fetch();

    if (!$rider) {
        echo "Error: No rider found with email: $email\n";
        exit(1);
    }

    // Hash and update password
    $hash = password_hash($newPassword, PASSWORD_DEFAULT);
    $stmt = $pdo->prepare("UPDATE riders SET password = ? WHERE id = ?");
    $stmt->execute([$hash, $rider['id']]);

    echo "Password updated for: {$rider['firstname']} {$rider['lastname']} ({$rider['email']})\n";
    echo "Role ID: {$rider['role_id']}\n";
    exit(0);
}

// Web mode - show form
$message = '';
$error = '';

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $email = trim($_POST['email'] ?? '');
    $newPassword = $_POST['new_password'] ?? '';

    if (empty($email) || empty($newPassword)) {
        $error = 'Fyll i både e-post och nytt lösenord.';
    } elseif (strlen($newPassword) < 6) {
        $error = 'Lösenordet måste vara minst 6 tecken.';
    } else {
        // Find rider
        $stmt = $pdo->prepare("SELECT id, email, firstname, lastname, role_id FROM riders WHERE email = ?");
        $stmt->execute([$email]);
        $rider = $stmt->fetch();

        if (!$rider) {
            $error = "Ingen rider hittades med e-post: $email";
        } else {
            // Hash and update password
            $hash = password_hash($newPassword, PASSWORD_DEFAULT);
            $stmt = $pdo->prepare("UPDATE riders SET password = ? WHERE id = ?");
            $stmt->execute([$hash, $rider['id']]);

            $message = "Lösenord uppdaterat för: {$rider['firstname']} {$rider['lastname']} (roll: {$rider['role_id']})";
        }
    }
}

// List riders with role_id >= 3 (admins)
$admins = $pdo->query("
    SELECT id, email, firstname, lastname, role_id,
           CASE WHEN password IS NOT NULL AND password != '' THEN 'Ja' ELSE 'Nej' END as has_password
    FROM riders
    WHERE role_id >= 3
    ORDER BY role_id DESC, lastname
")->fetchAll();
?>
<!DOCTYPE html>
<html>
<head>
    <title>Sätt lösenord - TheHUB Admin</title>
    <style>
        body { font-family: system-ui, sans-serif; max-width: 600px; margin: 50px auto; padding: 20px; }
        .message { padding: 10px; margin: 10px 0; border-radius: 5px; }
        .success { background: #d4edda; color: #155724; }
        .error { background: #f8d7da; color: #721c24; }
        form { margin: 20px 0; }
        input { padding: 10px; margin: 5px 0; width: 100%; box-sizing: border-box; }
        button { padding: 10px 20px; background: #007bff; color: white; border: none; cursor: pointer; }
        table { width: 100%; border-collapse: collapse; margin-top: 20px; }
        th, td { padding: 8px; text-align: left; border-bottom: 1px solid #ddd; }
        th { background: #f5f5f5; }
    </style>
</head>
<body>
    <h1>Sätt lösenord för rider</h1>

    <?php if ($message): ?>
        <div class="message success"><?= htmlspecialchars($message) ?></div>
    <?php endif; ?>

    <?php if ($error): ?>
        <div class="message error"><?= htmlspecialchars($error) ?></div>
    <?php endif; ?>

    <form method="post">
        <input type="email" name="email" placeholder="E-postadress" required>
        <input type="password" name="new_password" placeholder="Nytt lösenord (minst 6 tecken)" required>
        <button type="submit">Sätt lösenord</button>
    </form>

    <h2>Administratörer (role_id >= 3)</h2>
    <table>
        <tr>
            <th>Namn</th>
            <th>E-post</th>
            <th>Roll</th>
            <th>Lösenord?</th>
        </tr>
        <?php foreach ($admins as $admin): ?>
        <tr>
            <td><?= htmlspecialchars($admin['firstname'] . ' ' . $admin['lastname']) ?></td>
            <td><?= htmlspecialchars($admin['email']) ?></td>
            <td><?= $admin['role_id'] ?></td>
            <td><?= $admin['has_password'] ?></td>
        </tr>
        <?php endforeach; ?>
    </table>

    <p><a href="/admin/">← Tillbaka till admin</a></p>
</body>
</html>
