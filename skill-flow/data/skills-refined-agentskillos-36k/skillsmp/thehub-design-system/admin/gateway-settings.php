<?php
/**
 * Gateway Settings - Configure payment gateways per recipient
 */
require_once __DIR__ . '/../config.php';
require_admin();

$db = getDB();

$recipientId = intval($_GET['id'] ?? 0);

if (!$recipientId) {
    header('Location: /admin/payment-recipients.php');
    exit;
}

// Get payment recipient
$recipient = $db->getRow("
    SELECT * FROM payment_recipients WHERE id = ?
", [$recipientId]);

if (!$recipient) {
    $_SESSION['flash_error'] = 'Betalningsmottagare hittades inte';
    header('Location: /admin/payment-recipients.php');
    exit;
}

$message = '';
$messageType = 'info';

// Handle form submission
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    checkCsrf();

    $gatewayType = $_POST['gateway_type'] ?? 'manual';
    $gatewayEnabled = isset($_POST['gateway_enabled']) ? 1 : 0;

    // Gateway-specific config
    $gatewayConfig = [];

    if ($gatewayType === 'swish_handel') {
        $gatewayConfig = [
            'environment' => $_POST['swish_environment'] ?? 'production',
            'payee_alias' => preg_replace('/[^0-9]/', '', $_POST['swish_payee_alias'] ?? '')
        ];
    } elseif ($gatewayType === 'stripe') {
        // Stripe uses Connected Accounts, configured separately
        $gatewayConfig = [
            'platform_fee_percent' => floatval($_POST['stripe_platform_fee'] ?? 2)
        ];
    }

    try {
        $db->update('payment_recipients', [
            'gateway_type' => $gatewayType,
            'gateway_enabled' => $gatewayEnabled,
            'gateway_config' => json_encode($gatewayConfig)
        ], 'id = ?', [$recipientId]);

        $message = 'Gateway-inställningar sparade!';
        $messageType = 'success';

        // Reload recipient
        $recipient = $db->getRow("SELECT * FROM payment_recipients WHERE id = ?", [$recipientId]);

    } catch (Exception $e) {
        $message = 'Fel: ' . $e->getMessage();
        $messageType = 'error';
    }
}

$gatewayConfig = json_decode($recipient['gateway_config'] ?? '{}', true) ?: [];

// Check for active certificate
$hasCertificate = false;
try {
    $cert = $db->getRow("
        SELECT id, cert_type, uploaded_at
        FROM gateway_certificates
        WHERE payment_recipient_id = ? AND active = 1
        ORDER BY uploaded_at DESC
        LIMIT 1
    ", [$recipientId]);
    $hasCertificate = !empty($cert);
} catch (Exception $e) {
    // Table might not exist yet
}

$page_title = 'Gateway - ' . h($recipient['name']);
$page_group = 'economy';
$breadcrumbs = [
    ['label' => 'Betalningar', 'url' => '/admin/orders'],
    ['label' => 'Mottagare', 'url' => '/admin/payment-recipients.php'],
    ['label' => $recipient['name']]
];
include __DIR__ . '/components/unified-layout.php';
?>

<div class="admin-header mb-lg">
    <div class="admin-header-content">
        <a href="/admin/payment-recipients.php" class="btn-admin btn-admin-ghost">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="icon-sm">
                <path d="M19 12H5M12 19l-7-7 7-7"/>
            </svg>
            Tillbaka
        </a>
    </div>
</div>

<?php if ($message): ?>
<div class="alert alert-<?= $messageType === 'success' ? 'success' : ($messageType === 'error' ? 'error' : 'info') ?> mb-lg">
    <?= h($message) ?>
</div>
<?php endif; ?>

<div class="admin-card mb-lg">
    <div class="admin-card-header">
        <h2>
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="icon-md">
                <path d="M12.22 2h-.44a2 2 0 0 0-2 2v.18a2 2 0 0 1-1 1.73l-.43.25a2 2 0 0 1-2 0l-.15-.08a2 2 0 0 0-2.73.73l-.22.38a2 2 0 0 0 .73 2.73l.15.1a2 2 0 0 1 1 1.72v.51a2 2 0 0 1-1 1.74l-.15.09a2 2 0 0 0-.73 2.73l.22.38a2 2 0 0 0 2.73.73l.15-.08a2 2 0 0 1 2 0l.43.25a2 2 0 0 1 1 1.73V20a2 2 0 0 0 2 2h.44a2 2 0 0 0 2-2v-.18a2 2 0 0 1 1-1.73l.43-.25a2 2 0 0 1 2 0l.15.08a2 2 0 0 0 2.73-.73l.22-.39a2 2 0 0 0-.73-2.73l-.15-.08a2 2 0 0 1-1-1.74v-.5a2 2 0 0 1 1-1.74l.15-.09a2 2 0 0 0 .73-2.73l-.22-.38a2 2 0 0 0-2.73-.73l-.15.08a2 2 0 0 1-2 0l-.43-.25a2 2 0 0 1-1-1.73V4a2 2 0 0 0-2-2z"/>
                <circle cx="12" cy="12" r="3"/>
            </svg>
            Gateway-inställningar för <?= h($recipient['name']) ?>
        </h2>
    </div>
    <div class="admin-card-body">
        <form method="post">
            <?= csrf_field() ?>

            <div class="admin-form-group">
                <label class="admin-form-label">Betalningsgateway</label>
                <select name="gateway_type" class="admin-form-select" id="gatewayTypeSelect">
                    <option value="manual" <?= ($recipient['gateway_type'] ?? 'manual') === 'manual' ? 'selected' : '' ?>>
                        Manuell Swish (standard)
                    </option>
                    <option value="swish_handel" <?= ($recipient['gateway_type'] ?? '') === 'swish_handel' ? 'selected' : '' ?>>
                        Swish Handel API (automatisk bekräftelse)
                    </option>
                    <option value="stripe" <?= ($recipient['gateway_type'] ?? '') === 'stripe' ? 'selected' : '' ?>>
                        Stripe Connect (kort / Apple Pay / Google Pay)
                    </option>
                </select>
                <small class="text-secondary">Välj hur betalningar ska hanteras för denna mottagare</small>
            </div>

            <div class="admin-form-group">
                <label class="admin-form-label flex items-center gap-sm cursor-pointer">
                    <input type="checkbox" name="gateway_enabled" value="1"
                        <?= ($recipient['gateway_enabled'] ?? 0) ? 'checked' : '' ?>>
                    Gateway aktiverad
                </label>
                <small class="text-secondary">Måste vara aktiverad för att använda automatiska betalningar</small>
            </div>

            <!-- Manual Gateway Info -->
            <div id="manualSettings" class="gateway-settings">
                <div class="alert alert-info">
                    <strong>Manuell Swish</strong><br>
                    Betalare får en Swish-länk och QR-kod att betala med. Admin bekräftar betalningen manuellt.
                    Detta är standardalternativet och kräver ingen extra konfiguration.
                </div>
            </div>

            <!-- Swish Handel Settings -->
            <div id="swishHandelSettings" class="gateway-settings" style="display: none;">
                <hr class="my-lg">
                <h3 class="mb-md">Swish Handel API</h3>

                <div class="admin-form-row">
                    <div class="admin-form-group">
                        <label class="admin-form-label">Miljö</label>
                        <select name="swish_environment" class="admin-form-select">
                            <option value="test" <?= ($gatewayConfig['environment'] ?? '') === 'test' ? 'selected' : '' ?>>
                                Test (MSS - Merchant Swish Simulator)
                            </option>
                            <option value="production" <?= ($gatewayConfig['environment'] ?? 'production') === 'production' ? 'selected' : '' ?>>
                                Produktion
                            </option>
                        </select>
                    </div>

                    <div class="admin-form-group">
                        <label class="admin-form-label">Swish-nummer (Payee Alias)</label>
                        <input type="text" name="swish_payee_alias" class="admin-form-input"
                               value="<?= h($gatewayConfig['payee_alias'] ?? $recipient['swish_number'] ?? '') ?>"
                               placeholder="1234567890">
                        <small class="text-secondary">10-siffrigt nummer (endast siffror)</small>
                    </div>
                </div>

                <?php if ($hasCertificate): ?>
                <div class="alert alert-success">
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="icon-sm">
                        <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/>
                    </svg>
                    Certifikat uppladdat (<?= date('Y-m-d', strtotime($cert['uploaded_at'])) ?>)
                    <a href="/admin/certificates.php?id=<?= $recipientId ?>" class="ml-md">Hantera certifikat</a>
                </div>
                <?php else: ?>
                <div class="alert alert-warning">
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="icon-sm">
                        <path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3Z"/>
                        <line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/>
                    </svg>
                    <strong>Certifikat krävs!</strong>
                    Swish Handel kräver ett .p12-certifikat från din bank.
                    <a href="/admin/certificates.php?id=<?= $recipientId ?>" class="btn-admin btn-admin-primary btn-admin-sm ml-md">
                        Ladda upp certifikat
                    </a>
                </div>
                <?php endif; ?>
            </div>

            <!-- Stripe Settings -->
            <div id="stripeSettings" class="gateway-settings" style="display: none;">
                <hr class="my-lg">
                <h3 class="mb-md">Stripe Connect</h3>

                <?php if (!empty($recipient['stripe_account_id'])): ?>
                    <div class="alert alert-<?= $recipient['stripe_account_status'] === 'active' ? 'success' : 'warning' ?>">
                        <strong>Stripe-konto:</strong> <?= h($recipient['stripe_account_id']) ?><br>
                        <strong>Status:</strong>
                        <?php
                        $statusLabels = [
                            'active' => 'Aktivt',
                            'pending' => 'Väntar på verifiering',
                            'disabled' => 'Inaktiverat'
                        ];
                        echo $statusLabels[$recipient['stripe_account_status']] ?? 'Okänd';
                        ?>
                    </div>
                <?php else: ?>
                    <div class="alert alert-info">
                        <strong>Stripe-konto inte anslutet</strong><br>
                        För att ta emot kortbetalningar behöver organisationen genomgå Stripe onboarding.
                        <br><br>
                        <a href="/admin/stripe-onboarding.php?id=<?= $recipientId ?>" class="btn-admin btn-admin-primary">
                            Starta Stripe Onboarding
                        </a>
                    </div>
                <?php endif; ?>

                <div class="admin-form-group mt-md">
                    <label class="admin-form-label">Plattformsavgift (%)</label>
                    <input type="number" name="stripe_platform_fee" class="admin-form-input" style="max-width: 100px;"
                           value="<?= h($gatewayConfig['platform_fee_percent'] ?? 2) ?>"
                           min="0" max="50" step="0.1">
                    <small class="text-secondary">Avgift som går till TheHUB (default 2%)</small>
                </div>
            </div>

            <div class="admin-form-actions mt-lg">
                <button type="submit" class="btn-admin btn-admin-primary">
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="icon-sm">
                        <path d="M19 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11l5 5v11a2 2 0 0 1-2 2z"/>
                        <polyline points="17 21 17 13 7 13 7 21"/><polyline points="7 3 7 8 15 8"/>
                    </svg>
                    Spara inställningar
                </button>
            </div>
        </form>
    </div>
</div>

<style>
.admin-form-row {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: var(--space-md);
}

@media (max-width: 600px) {
    .admin-form-row {
        grid-template-columns: 1fr;
    }
}

.my-lg {
    margin-top: var(--space-lg);
    margin-bottom: var(--space-lg);
}

.ml-md {
    margin-left: var(--space-md);
}

.mt-md {
    margin-top: var(--space-md);
}

.mt-lg {
    margin-top: var(--space-lg);
}
</style>

<script>
document.addEventListener('DOMContentLoaded', function() {
    const gatewaySelect = document.getElementById('gatewayTypeSelect');
    const manualSettings = document.getElementById('manualSettings');
    const swishSettings = document.getElementById('swishHandelSettings');
    const stripeSettings = document.getElementById('stripeSettings');

    function updateVisibility() {
        const value = gatewaySelect.value;

        manualSettings.style.display = value === 'manual' ? 'block' : 'none';
        swishSettings.style.display = value === 'swish_handel' ? 'block' : 'none';
        stripeSettings.style.display = value === 'stripe' ? 'block' : 'none';
    }

    gatewaySelect.addEventListener('change', updateVisibility);
    updateVisibility();
});
</script>

<?php include __DIR__ . '/components/unified-layout-footer.php'; ?>
