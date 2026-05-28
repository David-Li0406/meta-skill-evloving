<?php
/**
 * Certificate Management - Upload and manage Swish certificates
 */
require_once __DIR__ . '/../config.php';
require_admin();

$db = getDB();
$recipientId = intval($_GET['id'] ?? 0);

if (!$recipientId) {
    header('Location: /admin/payment-recipients.php');
    exit;
}

$recipient = $db->getRow("SELECT * FROM payment_recipients WHERE id = ?", [$recipientId]);

if (!$recipient) {
    $_SESSION['flash_error'] = 'Betalningsmottagare hittades inte';
    header('Location: /admin/payment-recipients.php');
    exit;
}

$message = '';
$messageType = 'info';

// Handle certificate upload
if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_FILES['certificate'])) {
    checkCsrf();

    $certType = $_POST['cert_type'] ?? 'swish_production';
    $certPassword = $_POST['cert_password'] ?? '';

    $file = $_FILES['certificate'];

    if ($file['error'] === UPLOAD_ERR_OK) {
        // Validate file type
        $allowedExtensions = ['p12', 'pfx'];
        $extension = strtolower(pathinfo($file['name'], PATHINFO_EXTENSION));

        if (!in_array($extension, $allowedExtensions)) {
            $message = 'Endast .p12 och .pfx filer tillåtna';
            $messageType = 'error';
        } elseif ($file['size'] > 1024 * 1024) { // 1MB limit
            $message = 'Filen är för stor (max 1MB)';
            $messageType = 'error';
        } else {
            $certData = file_get_contents($file['tmp_name']);

            try {
                // Deactivate old certificates of same type
                $db->query("
                    UPDATE gateway_certificates
                    SET active = 0
                    WHERE payment_recipient_id = ? AND cert_type = ?
                ", [$recipientId, $certType]);

                // Insert new certificate
                $db->insert('gateway_certificates', [
                    'payment_recipient_id' => $recipientId,
                    'cert_type' => $certType,
                    'cert_data' => $certData,
                    'cert_password' => $certPassword,
                    'uploaded_by' => $_SESSION['admin_user_id'] ?? null,
                    'active' => 1
                ]);

                $message = 'Certifikat uppladdat!';
                $messageType = 'success';

            } catch (Exception $e) {
                $message = 'Fel vid uppladdning: ' . $e->getMessage();
                $messageType = 'error';
            }
        }
    } else {
        $uploadErrors = [
            UPLOAD_ERR_INI_SIZE => 'Filen är för stor (server-gräns)',
            UPLOAD_ERR_FORM_SIZE => 'Filen är för stor',
            UPLOAD_ERR_PARTIAL => 'Filen laddades endast delvis upp',
            UPLOAD_ERR_NO_FILE => 'Ingen fil vald',
            UPLOAD_ERR_NO_TMP_DIR => 'Temporär mapp saknas',
            UPLOAD_ERR_CANT_WRITE => 'Kunde inte skriva filen',
        ];
        $message = 'Fel vid filuppladdning: ' . ($uploadErrors[$file['error']] ?? 'Okänt fel');
        $messageType = 'error';
    }
}

// Handle certificate deletion
if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['delete_cert'])) {
    checkCsrf();
    $certId = intval($_POST['delete_cert']);

    try {
        $db->delete('gateway_certificates', 'id = ? AND payment_recipient_id = ?', [$certId, $recipientId]);
        $message = 'Certifikat borttaget!';
        $messageType = 'success';
    } catch (Exception $e) {
        $message = 'Fel: ' . $e->getMessage();
        $messageType = 'error';
    }
}

// Get existing certificates
$certificates = [];
try {
    $certificates = $db->getAll("
        SELECT gc.*, au.full_name as uploaded_by_name
        FROM gateway_certificates gc
        LEFT JOIN admin_users au ON gc.uploaded_by = au.id
        WHERE gc.payment_recipient_id = ?
        ORDER BY gc.uploaded_at DESC
    ", [$recipientId]);
} catch (Exception $e) {
    // Table might not exist
}

$page_title = 'Certifikat - ' . h($recipient['name']);
$page_group = 'economy';
$breadcrumbs = [
    ['label' => 'Betalningar', 'url' => '/admin/orders'],
    ['label' => 'Mottagare', 'url' => '/admin/payment-recipients.php'],
    ['label' => $recipient['name'], 'url' => '/admin/gateway-settings.php?id=' . $recipientId],
    ['label' => 'Certifikat']
];
include __DIR__ . '/components/unified-layout.php';
?>

<div class="admin-header mb-lg">
    <div class="admin-header-content">
        <a href="/admin/gateway-settings.php?id=<?= $recipientId ?>" class="btn-admin btn-admin-ghost">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="icon-sm">
                <path d="M19 12H5M12 19l-7-7 7-7"/>
            </svg>
            Tillbaka till gateway
        </a>
    </div>
</div>

<?php if ($message): ?>
<div class="alert alert-<?= $messageType === 'success' ? 'success' : ($messageType === 'error' ? 'error' : 'info') ?> mb-lg">
    <?= h($message) ?>
</div>
<?php endif; ?>

<!-- Info -->
<div class="admin-card mb-lg">
    <div class="admin-card-body">
        <div class="flex items-start gap-md">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="icon-lg flex-shrink-0" style="color: var(--color-accent);">
                <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>
            </svg>
            <div>
                <h3 style="margin: 0 0 var(--space-xs) 0;">Swish Certifikat</h3>
                <ul class="text-secondary" style="margin: 0; padding-left: var(--space-lg);">
                    <li>Certifikatet (.p12-fil) får du från din bank när du aktiverar Swish Handel</li>
                    <li>Test-certifikat används i MSS (Merchant Swish Simulator)</li>
                    <li>Produktions-certifikat används för riktiga betalningar</li>
                    <li>Certifikat måste förnyas årligen</li>
                    <li>Lösenordet som krävs får du tillsammans med certifikatet</li>
                </ul>
            </div>
        </div>
    </div>
</div>

<!-- Upload form -->
<div class="admin-card mb-lg">
    <div class="admin-card-header">
        <h2>
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="icon-md">
                <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
                <polyline points="17 8 12 3 7 8"/>
                <line x1="12" y1="3" x2="12" y2="15"/>
            </svg>
            Ladda upp certifikat
        </h2>
    </div>
    <div class="admin-card-body">
        <form method="post" enctype="multipart/form-data">
            <?= csrf_field() ?>

            <div class="admin-form-row">
                <div class="admin-form-group">
                    <label class="admin-form-label">Certifikat-typ</label>
                    <select name="cert_type" class="admin-form-select">
                        <option value="swish_test">Test (MSS)</option>
                        <option value="swish_production" selected>Produktion</option>
                    </select>
                </div>

                <div class="admin-form-group">
                    <label class="admin-form-label">Certifikat-lösenord</label>
                    <input type="password" name="cert_password" class="admin-form-input"
                           placeholder="Lösenord från banken">
                </div>
            </div>

            <div class="admin-form-group">
                <label class="admin-form-label">Certifikat-fil (.p12 / .pfx)</label>
                <input type="file" name="certificate" class="admin-form-input" accept=".p12,.pfx" required>
                <small class="text-secondary">Max 1MB</small>
            </div>

            <div class="admin-form-actions">
                <button type="submit" class="btn-admin btn-admin-primary">
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="icon-sm">
                        <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
                        <polyline points="17 8 12 3 7 8"/>
                        <line x1="12" y1="3" x2="12" y2="15"/>
                    </svg>
                    Ladda upp certifikat
                </button>
            </div>
        </form>
    </div>
</div>

<!-- Existing certificates -->
<?php if (!empty($certificates)): ?>
<div class="admin-card">
    <div class="admin-card-header">
        <h2>
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="icon-md">
                <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
                <polyline points="14 2 14 8 20 8"/>
            </svg>
            Uppladdade certifikat (<?= count($certificates) ?>)
        </h2>
    </div>
    <div class="admin-card-body gs-p-0">
        <div class="table-responsive">
            <table class="admin-table">
                <thead>
                    <tr>
                        <th>Typ</th>
                        <th>Uppladdat</th>
                        <th>Av</th>
                        <th>Status</th>
                        <th></th>
                    </tr>
                </thead>
                <tbody>
                    <?php foreach ($certificates as $cert): ?>
                    <tr>
                        <td>
                            <?php if ($cert['cert_type'] === 'swish_test'): ?>
                                <span class="badge badge-warning">Test</span>
                            <?php else: ?>
                                <span class="badge badge-success">Produktion</span>
                            <?php endif; ?>
                        </td>
                        <td><?= date('Y-m-d H:i', strtotime($cert['uploaded_at'])) ?></td>
                        <td><?= h($cert['uploaded_by_name'] ?? 'Okänd') ?></td>
                        <td>
                            <?php if ($cert['active']): ?>
                                <span class="badge badge-success">Aktivt</span>
                            <?php else: ?>
                                <span class="badge badge-secondary">Inaktivt</span>
                            <?php endif; ?>
                        </td>
                        <td class="text-right">
                            <form method="POST" class="inline">
                                <?= csrf_field() ?>
                                <input type="hidden" name="delete_cert" value="<?= $cert['id'] ?>">
                                <button type="submit" class="btn-admin btn-admin-danger btn-admin-sm"
                                        onclick="return confirm('Ta bort detta certifikat?')">
                                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="icon-xs">
                                        <path d="M3 6h18"/><path d="M19 6v14c0 1-1 2-2 2H7c-1 0-2-1-2-2V6"/><path d="M8 6V4c0-1 1-2 2-2h4c1 0 2 1 2 2v2"/>
                                    </svg>
                                </button>
                            </form>
                        </td>
                    </tr>
                    <?php endforeach; ?>
                </tbody>
            </table>
        </div>
    </div>
</div>
<?php endif; ?>

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

.btn-admin-sm {
    padding: var(--space-xs) var(--space-sm);
}
</style>

<?php include __DIR__ . '/components/unified-layout-footer.php'; ?>
