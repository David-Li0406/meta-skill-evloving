<?php
/**
 * TheHUB V1.0 - Forgot Password
 * Request password reset link
 *
 * Finds the primary account (with password) when profiles are linked
 */

// If already logged in, redirect to profile
if (hub_is_logged_in()) {
    header('Location: /profile');
    exit;
}

// Include mail helper
require_once HUB_ROOT . '/includes/mail.php';

$pdo = hub_db();
$message = '';
$messageType = '';
$showResetLink = false;
$resetLink = '';
$emailSent = false;
$linkedProfilesCount = 0;

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $email = trim($_POST['email'] ?? '');

    if (empty($email)) {
        $message = 'Ange din e-postadress';
        $messageType = 'error';
    } else {
        $accountFound = false;
        $accountType = null; // 'rider' or 'admin'
        $accountId = null;
        $accountName = '';
        $accountEmail = '';

        // First check admin_users table (promotors, admins)
        $adminStmt = $pdo->prepare("
            SELECT id, full_name, email, password_hash
            FROM admin_users
            WHERE email = ? AND active = 1
            LIMIT 1
        ");
        $adminStmt->execute([$email]);
        $adminUser = $adminStmt->fetch(PDO::FETCH_ASSOC);

        if ($adminUser) {
            $accountFound = true;
            $accountType = 'admin';
            $accountId = $adminUser['id'];
            $accountName = $adminUser['full_name'] ?: 'Användare';
            $accountEmail = $adminUser['email'];
        } else {
            // Check riders table
            $stmt = $pdo->prepare("
                SELECT r.id, r.firstname, r.lastname, r.email, r.password
                FROM riders r
                WHERE r.email = ? AND r.password IS NOT NULL AND r.password != ''
                ORDER BY r.id
                LIMIT 1
            ");
            $stmt->execute([$email]);
            $primaryRider = $stmt->fetch(PDO::FETCH_ASSOC);

            if ($primaryRider) {
                $accountFound = true;
                $accountType = 'rider';
                $accountId = $primaryRider['id'];
                $accountName = trim($primaryRider['firstname'] . ' ' . $primaryRider['lastname']);
                $accountEmail = $primaryRider['email'];
            }
        }

        if (!$accountFound) {
            // Check if rider email exists but not activated
            $checkStmt = $pdo->prepare("SELECT COUNT(*) as count FROM riders WHERE email = ?");
            $checkStmt->execute([$email]);
            $hasProfiles = $checkStmt->fetch(PDO::FETCH_ASSOC)['count'] > 0;

            if ($hasProfiles) {
                $message = 'Kontot är inte aktiverat ännu. Gå till "Aktivera konto" för att skapa ett lösenord.';
                $messageType = 'warning';
            } else {
                // Security: Don't reveal if email exists or not
                $message = 'Om e-postadressen finns i systemet kommer du få ett mail med instruktioner.';
                $messageType = 'info';
            }
        } else {
            // Generate reset token
            $token = bin2hex(random_bytes(32));
            $expires = date('Y-m-d H:i:s', strtotime('+1 hour'));

            if ($accountType === 'admin') {
                // Save token to admin_users
                $updateStmt = $pdo->prepare("
                    UPDATE admin_users SET
                        password_reset_token = ?,
                        password_reset_expires = ?
                    WHERE id = ?
                ");
                $updateStmt->execute([$token, $expires, $accountId]);
                $linkedProfilesCount = 0;
            } else {
                // Save token to riders
                $updateStmt = $pdo->prepare("
                    UPDATE riders SET
                        password_reset_token = ?,
                        password_reset_expires = ?
                    WHERE id = ?
                ");
                $updateStmt->execute([$token, $expires, $accountId]);

                // Count linked profiles for riders
                $countStmt = $pdo->prepare("
                    SELECT COUNT(*) as count FROM riders
                    WHERE (email = ? OR linked_to_rider_id = ?) AND id != ?
                ");
                $countStmt->execute([$accountEmail, $accountId, $accountId]);
                $linkedProfilesCount = (int)$countStmt->fetch(PDO::FETCH_ASSOC)['count'];
            }

            // Build reset link
            $baseUrl = (isset($_SERVER['HTTPS']) && $_SERVER['HTTPS'] === 'on' ? 'https' : 'http')
                     . '://' . $_SERVER['HTTP_HOST'];
            $resetLink = $baseUrl . '/reset-password?token=' . $token;

            // Send email
            $emailSent = hub_send_password_reset_email($accountEmail, $accountName, $resetLink);

            if ($emailSent) {
                if ($linkedProfilesCount > 0) {
                    $totalProfiles = $linkedProfilesCount + 1;
                    $message = "Ett mail med återställningslänk har skickats till " . htmlspecialchars($email) .
                               ". Lösenordet gäller för alla {$totalProfiles} kopplade profiler.";
                } else {
                    $message = 'Ett mail med återställningslänk har skickats till ' . htmlspecialchars($email);
                }
                $messageType = 'success';
            } else {
                // Email failed - show link as fallback
                $showResetLink = true;
                $message = 'Kunde inte skicka mail. Här är återställningslänken:';
                $messageType = 'warning';
                error_log("Password reset email failed for {$email}: {$resetLink}");
            }
        }
    }
}
?>

<div class="auth-container">
    <div class="auth-card">
        <div class="auth-header">
            <h1>Glömt lösenord</h1>
            <p>Ange din e-postadress så skapar vi en återställningslänk</p>
        </div>

        <?php if ($message): ?>
            <div class="alert alert--<?= $messageType ?>">
                <?= $message ?>
            </div>
        <?php endif; ?>

        <?php if ($emailSent): ?>
            <!-- Email sent successfully -->
            <div class="success-info">
                <p>Kontrollera din inkorg (och skräppost) för att hitta återställningslänken.</p>
                <p class="note">Länken är giltig i 1 timme.</p>
            </div>
            <a href="/login" class="btn btn--primary btn--block mt-md">
                Tillbaka till inloggning
            </a>

        <?php elseif ($showResetLink): ?>
            <!-- Email failed - show link as fallback -->
            <div class="reset-link-box">
                <p><strong>Återställningslänk:</strong></p>
                <div class="reset-link-input">
                    <input type="text" value="<?= htmlspecialchars($resetLink) ?>" readonly id="resetLink">
                    <button type="button" onclick="copyLink()" class="btn btn--primary btn--sm">Kopiera</button>
                </div>
                <p class="reset-note">Länken är giltig i 1 timme.</p>
                <a href="<?= htmlspecialchars($resetLink) ?>" class="btn btn--primary btn--block mt-md">
                    Gå till återställning
                </a>
            </div>

        <?php elseif ($messageType === 'warning'): ?>
            <!-- Account not activated -->
            <a href="/activate-account" class="btn btn--primary btn--block mt-md">
                Aktivera konto
            </a>
            <a href="/login" class="btn btn--secondary btn--block mt-sm">
                Tillbaka till inloggning
            </a>

        <?php else: ?>
            <form method="POST" class="auth-form">
                <div class="form-group">
                    <label for="email">E-postadress</label>
                    <input type="email" id="email" name="email" required
                           placeholder="din@email.se"
                           value="<?= htmlspecialchars($_POST['email'] ?? '') ?>">
                </div>

                <button type="submit" class="btn btn--primary btn--block">
                    Skicka återställningslänk
                </button>
            </form>

            <div class="info-box">
                <strong>Flera profiler?</strong>
                <p>Om du har flera kopplade profiler gäller lösenordet för alla.</p>
            </div>
        <?php endif; ?>

        <div class="auth-footer">
            <a href="/login">&larr; Tillbaka till inloggning</a>
        </div>
    </div>
</div>

<style>
.info-box {
    margin-top: var(--space-md);
    padding: var(--space-md);
    background: var(--color-bg-sunken, #f8f9fa);
    border-radius: var(--radius-md);
    font-size: var(--text-sm);
}

.info-box strong {
    display: block;
    margin-bottom: var(--space-xs);
    color: var(--color-text-primary);
}

.info-box p {
    color: var(--color-text-secondary);
    margin: 0;
}
</style>

<script>
function copyLink() {
    const input = document.getElementById('resetLink');
    input.select();
    document.execCommand('copy');
    alert('Länk kopierad!');
}
</script>
