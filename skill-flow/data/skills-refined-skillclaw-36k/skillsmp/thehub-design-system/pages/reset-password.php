<?php
/**
 * TheHUB V1.0 - Reset Password
 * Set new password with reset token
 *
 * When setting password, links all other profiles with same email
 * to this account (for family account management)
 */

// If already logged in, redirect to profile
if (hub_is_logged_in()) {
    header('Location: /profile');
    exit;
}

$pdo = hub_db();
$token = $_GET['token'] ?? '';
$isActivation = isset($_GET['activate']);
$message = '';
$messageType = '';
$validToken = false;
$rider = null;
$adminUser = null;
$accountType = null; // 'rider' or 'admin'
$linkedProfilesCount = 0;

// Validate token - check both riders and admin_users
if (!empty($token)) {
    // First check riders table
    $stmt = $pdo->prepare("
        SELECT id, firstname, lastname, email
        FROM riders
        WHERE password_reset_token = ?
        AND password_reset_expires > NOW()
        LIMIT 1
    ");
    $stmt->execute([$token]);
    $rider = $stmt->fetch(PDO::FETCH_ASSOC);

    if ($rider) {
        $validToken = true;
        $accountType = 'rider';

        // Count other profiles with same email that will be linked
        $countStmt = $pdo->prepare("
            SELECT COUNT(*) as count FROM riders
            WHERE email = ? AND id != ?
        ");
        $countStmt->execute([$rider['email'], $rider['id']]);
        $linkedProfilesCount = (int)$countStmt->fetch(PDO::FETCH_ASSOC)['count'];
    } else {
        // Check admin_users table
        $adminStmt = $pdo->prepare("
            SELECT id, full_name, email
            FROM admin_users
            WHERE password_reset_token = ?
            AND password_reset_expires > NOW()
            LIMIT 1
        ");
        $adminStmt->execute([$token]);
        $adminUser = $adminStmt->fetch(PDO::FETCH_ASSOC);

        if ($adminUser) {
            $validToken = true;
            $accountType = 'admin';
        } else {
            $message = 'Ogiltig eller utgången återställningslänk. Begär en ny länk.';
            $messageType = 'error';
        }
    }
}

// Handle form submission
if ($_SERVER['REQUEST_METHOD'] === 'POST' && $validToken) {
    $password = $_POST['password'] ?? '';
    $passwordConfirm = $_POST['password_confirm'] ?? '';

    if (strlen($password) < 8) {
        $message = 'Lösenordet måste vara minst 8 tecken';
        $messageType = 'error';
    } elseif ($password !== $passwordConfirm) {
        $message = 'Lösenorden matchar inte';
        $messageType = 'error';
    } else {
        // Hash new password
        $hashedPassword = password_hash($password, PASSWORD_DEFAULT);

        if ($accountType === 'admin') {
            // Update admin_users
            $updateStmt = $pdo->prepare("
                UPDATE admin_users SET
                    password_hash = ?,
                    password_reset_token = NULL,
                    password_reset_expires = NULL
                WHERE id = ?
            ");
            $updateStmt->execute([$hashedPassword, $adminUser['id']]);

            $message = 'Lösenord återställt! Du kan nu logga in.';
            $messageType = 'success';
            $validToken = false;
        } else {
            // Update riders table
            $updateStmt = $pdo->prepare("
                UPDATE riders SET
                    password = ?,
                    password_reset_token = NULL,
                    password_reset_expires = NULL,
                    linked_to_rider_id = NULL
                WHERE id = ?
            ");
            $updateStmt->execute([$hashedPassword, $rider['id']]);

            // Link all other riders with same email to this primary account
            $linkStmt = $pdo->prepare("
                UPDATE riders SET
                    linked_to_rider_id = ?,
                    password = NULL,
                    password_reset_token = NULL,
                    password_reset_expires = NULL
                WHERE email = ? AND id != ?
            ");
            $linkStmt->execute([$rider['id'], $rider['email'], $rider['id']]);

            // Get count of actually linked profiles
            $linkedCount = $linkStmt->rowCount();

            if ($isActivation) {
                if ($linkedCount > 0) {
                    $message = "Konto aktiverat! Du har nu tillgång till " . ($linkedCount + 1) . " profiler med samma inloggning.";
                } else {
                    $message = 'Konto aktiverat! Du kan nu logga in.';
                }
            } else {
                if ($linkedCount > 0) {
                    $message = "Lösenord återställt! Alla " . ($linkedCount + 1) . " profiler är tillgängliga med samma inloggning.";
                } else {
                    $message = 'Lösenord återställt! Du kan nu logga in.';
                }
            }
            $messageType = 'success';
            $validToken = false; // Hide form
        }
    }
}

$pageTitle = $isActivation ? 'Aktivera konto' : 'Återställ lösenord';
?>

<div class="auth-container">
    <div class="auth-card">
        <div class="auth-header">
            <h1><?= $pageTitle ?></h1>
            <?php if ($rider): ?>
                <p>
                    <?= $isActivation ? 'Skapa' : 'Ange nytt' ?> lösenord för
                    <strong><?= htmlspecialchars($rider['firstname'] . ' ' . $rider['lastname']) ?></strong>
                </p>
            <?php elseif ($adminUser): ?>
                <p>
                    Ange nytt lösenord för
                    <strong><?= htmlspecialchars($adminUser['full_name'] ?: $adminUser['email']) ?></strong>
                </p>
            <?php else: ?>
                <p>Ange din återställningskod eller begär en ny</p>
            <?php endif; ?>
        </div>

        <?php if ($message): ?>
            <div class="alert alert--<?= $messageType ?>">
                <?= htmlspecialchars($message) ?>
            </div>
        <?php endif; ?>

        <?php if ($messageType === 'success'): ?>
            <a href="/login" class="btn btn--primary btn--block">Gå till inloggning</a>

        <?php elseif ($validToken): ?>
            <?php if ($linkedProfilesCount > 0): ?>
                <div class="info-box mb-md">
                    <strong><?= $linkedProfilesCount + 1 ?> profiler kommer att kopplas</strong>
                    <p>Alla profiler med e-postadressen <?= htmlspecialchars($rider['email']) ?> kommer att vara tillgängliga med detta lösenord.</p>
                </div>
            <?php endif; ?>

            <form method="POST" class="auth-form">
                <div class="form-group">
                    <label for="password">
                        <?= $isActivation ? 'Välj lösenord' : 'Nytt lösenord' ?>
                    </label>
                    <input type="password" id="password" name="password" required
                           placeholder="Minst 8 tecken"
                           minlength="8">
                </div>

                <div class="form-group">
                    <label for="password_confirm">Bekräfta lösenord</label>
                    <input type="password" id="password_confirm" name="password_confirm" required
                           placeholder="Samma lösenord igen"
                           minlength="8">
                </div>

                <button type="submit" class="btn btn--primary btn--block">
                    <?= $isActivation ? 'Aktivera konto' : 'Spara nytt lösenord' ?>
                </button>
            </form>

        <?php else: ?>
            <p class="text-center">Ingen giltig återställningskod angiven.</p>
            <a href="/forgot-password" class="btn btn--primary btn--block mt-md">
                Begär ny återställningslänk
            </a>
        <?php endif; ?>

        <div class="auth-footer">
            <a href="/login">&larr; Tillbaka till inloggning</a>
        </div>
    </div>
</div>

<style>
.info-box {
    padding: var(--space-md);
    background: var(--color-bg-sunken, #f8f9fa);
    border-radius: var(--radius-md);
    border-left: 4px solid var(--color-accent);
}

.info-box strong {
    display: block;
    margin-bottom: var(--space-xs);
    color: var(--color-text-primary);
}

.info-box p {
    margin: 0;
    font-size: var(--text-sm);
    color: var(--color-text-secondary);
}

.mb-md {
    margin-bottom: var(--space-md);
}
</style>
