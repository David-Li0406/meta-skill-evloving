<?php
/**
 * TheHUB V1.0 - Rider Registration
 * Connect email to a rider profile (Super Admin only)
 */

// Get rider ID from URL
$riderId = (int)($pageInfo['params']['id'] ?? 0);

if (!$riderId) {
    header('Location: /database');
    exit;
}

// Check if user is super admin
$isSuperAdmin = function_exists('hub_is_super_admin') && hub_is_super_admin();
if (!$isSuperAdmin) {
    header('Location: /rider/' . $riderId);
    exit;
}

$pdo = hub_db();
$message = '';
$messageType = '';
$success = false;

// Fetch rider info
try {
    $stmt = $pdo->prepare("
        SELECT id, firstname, lastname, email, birth_year
        FROM riders
        WHERE id = ?
    ");
    $stmt->execute([$riderId]);
    $rider = $stmt->fetch(PDO::FETCH_ASSOC);

    if (!$rider) {
        $message = 'Profilen hittades inte';
        $messageType = 'error';
    } elseif (!empty($rider['email'])) {
        $message = 'Denna profil har redan en e-postadress kopplad.';
        $messageType = 'warning';
    }

    // Count results for this rider
    $resultsStmt = $pdo->prepare("SELECT COUNT(*) FROM results WHERE cyclist_id = ?");
    $resultsStmt->execute([$riderId]);
    $resultsCount = (int)$resultsStmt->fetchColumn();

} catch (Exception $e) {
    $message = 'Ett fel uppstod vid hämtning av profil';
    $messageType = 'error';
    $rider = null;
}

$fullName = $rider ? trim($rider['firstname'] . ' ' . $rider['lastname']) : '';
?>

<div class="auth-container">
    <div class="auth-card register-card">
        <div class="auth-header">
            <h1>Begär e-postkoppling</h1>
            <p>Skicka förfrågan om att koppla e-post till profil</p>
        </div>

        <?php if ($message): ?>
            <div class="alert alert--<?= $messageType ?>">
                <?= htmlspecialchars($message) ?>
            </div>
            <?php if ($messageType === 'warning' || $messageType === 'error'): ?>
                <div class="auth-footer">
                    <a href="/rider/<?= $riderId ?>">Tillbaka till profil</a>
                </div>
            <?php endif; ?>
        <?php endif; ?>

        <?php if ($rider && empty($rider['email'])): ?>
            <!-- Profile Info -->
            <div class="register-profile-card">
                <div class="register-profile-label">Profil utan e-post</div>
                <div class="register-profile-name"><?= htmlspecialchars($fullName) ?></div>
                <div class="register-profile-meta"><?= $resultsCount ?> resultat</div>
            </div>

            <!-- Registration Form -->
            <form id="registerForm" class="auth-form">
                <div class="form-group">
                    <label for="email">E-postadress <span class="required">*</span></label>
                    <input type="email" id="email" name="email" required
                           placeholder="namn@example.com"
                           autocomplete="email">
                </div>

                <div class="form-group">
                    <label for="phone">Telefonnummer <span class="required">*</span></label>
                    <input type="tel" id="phone" name="phone" required
                           placeholder="070-123 45 67"
                           autocomplete="tel">
                    <span class="field-hint">Obligatoriskt för verifiering</span>
                </div>

                <div class="form-divider">
                    <span>Sociala medier (valfritt)</span>
                </div>

                <div class="social-grid">
                    <div class="form-group">
                        <label for="instagram">
                            <i data-lucide="instagram"></i>
                            Instagram
                        </label>
                        <input type="text" id="instagram" name="instagram"
                               placeholder="@användarnamn">
                    </div>

                    <div class="form-group">
                        <label for="facebook">
                            <i data-lucide="facebook"></i>
                            Facebook
                        </label>
                        <input type="text" id="facebook" name="facebook"
                               placeholder="Profilnamn eller URL">
                    </div>
                </div>

                <div class="form-group">
                    <label for="reason">Anteckning (valfritt)</label>
                    <textarea id="reason" name="reason" rows="2"
                              placeholder="T.ex. verifierad via telefon..."></textarea>
                </div>

                <input type="hidden" name="target_rider_id" value="<?= $riderId ?>">

                <div id="formMessage" class="alert" style="display: none;"></div>

                <button type="submit" class="btn btn--primary btn--block" id="submitBtn">
                    <i data-lucide="send"></i>
                    Skicka förfrågan
                </button>
            </form>

            <!-- Success State (hidden initially) -->
            <div id="successState" class="register-success" style="display: none;">
                <i data-lucide="clock"></i>
                <h3>Förfrågan skickad!</h3>
                <p>En admin kommer att granska och godkänna förfrågan. Aktiveringslänk skickas därefter till angiven e-postadress.</p>
                <a href="/rider/<?= $riderId ?>" class="btn btn--primary btn--block">
                    Tillbaka till profil
                </a>
            </div>

            <div class="auth-footer">
                <a href="/rider/<?= $riderId ?>">Avbryt</a>
            </div>
        <?php endif; ?>
    </div>
</div>

<style>
.register-card {
    max-width: 480px;
}

.register-profile-card {
    padding: var(--space-md);
    background: var(--color-bg-secondary);
    border: 2px solid var(--color-accent);
    border-radius: var(--radius-md);
    text-align: center;
    margin-bottom: var(--space-lg);
}

.register-profile-label {
    font-size: var(--text-xs);
    color: var(--color-text-secondary);
    text-transform: uppercase;
    letter-spacing: 0.05em;
    margin-bottom: var(--space-xs);
}

.register-profile-name {
    font-weight: 600;
    font-size: var(--text-lg);
    color: var(--color-text);
}

.register-profile-meta {
    font-size: var(--text-sm);
    color: var(--color-text-secondary);
    margin-top: 2px;
}

.required {
    color: var(--color-danger);
}

.field-hint {
    display: block;
    font-size: var(--text-xs);
    color: var(--color-text-secondary);
    margin-top: var(--space-2xs);
}

.form-divider {
    display: flex;
    align-items: center;
    gap: var(--space-md);
    margin: var(--space-lg) 0;
    color: var(--color-text-secondary);
    font-size: var(--text-sm);
}

.form-divider::before,
.form-divider::after {
    content: '';
    flex: 1;
    height: 1px;
    background: var(--color-border);
}

.social-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: var(--space-md);
}

.social-grid .form-group label {
    display: flex;
    align-items: center;
    gap: var(--space-xs);
}

.social-grid .form-group label i {
    width: 16px;
    height: 16px;
    color: var(--color-text-secondary);
}

.register-success {
    text-align: center;
    padding: var(--space-xl) 0;
}

.register-success i {
    width: 48px;
    height: 48px;
    color: var(--color-success);
    margin-bottom: var(--space-md);
}

.register-success h3 {
    margin: 0 0 var(--space-sm);
    color: var(--color-text);
}

.register-success p {
    color: var(--color-text-secondary);
    margin-bottom: var(--space-lg);
}

@media (max-width: 480px) {
    .social-grid {
        grid-template-columns: 1fr;
    }
}
</style>

<script>
document.getElementById('registerForm')?.addEventListener('submit', async function(e) {
    e.preventDefault();

    const form = e.target;
    const submitBtn = document.getElementById('submitBtn');
    const formMessage = document.getElementById('formMessage');
    const originalHtml = submitBtn.innerHTML;

    // Disable and show loading
    submitBtn.disabled = true;
    submitBtn.innerHTML = '<i data-lucide="loader-2" class="animate-spin"></i> Skickar...';
    if (typeof lucide !== 'undefined') lucide.createIcons();

    formMessage.style.display = 'none';

    try {
        const formData = new FormData(form);
        const response = await fetch('/api/rider-claim.php', {
            method: 'POST',
            body: formData
        });

        const result = await response.json();

        if (result.success) {
            // Hide form, show success
            form.style.display = 'none';
            document.querySelector('.auth-footer').style.display = 'none';
            document.getElementById('successState').style.display = 'block';
            if (typeof lucide !== 'undefined') lucide.createIcons();
        } else {
            // Show error
            formMessage.className = 'alert alert--error';
            formMessage.textContent = result.error || 'Ett fel uppstod';
            formMessage.style.display = 'block';
            submitBtn.disabled = false;
            submitBtn.innerHTML = originalHtml;
            if (typeof lucide !== 'undefined') lucide.createIcons();
        }
    } catch (error) {
        formMessage.className = 'alert alert--error';
        formMessage.textContent = 'Ett fel uppstod vid anslutning till servern';
        formMessage.style.display = 'block';
        submitBtn.disabled = false;
        submitBtn.innerHTML = originalHtml;
        if (typeof lucide !== 'undefined') lucide.createIcons();
    }
});
</script>
