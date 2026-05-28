<?php
/**
 * Swish Accounts - Unified Swish Management
 * All Swish configuration in one place
 */
require_once __DIR__ . '/../config.php';
require_admin();

$db = getDB();
$isSuperAdmin = hasRole('super_admin');

$message = '';
$messageType = 'info';

// Check for flash messages
if (isset($_SESSION['flash_message'])) {
    $message = $_SESSION['flash_message'];
    $messageType = $_SESSION['flash_type'] ?? 'info';
    unset($_SESSION['flash_message'], $_SESSION['flash_type']);
}

// Handle POST actions
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    checkCsrf();
    $action = $_POST['action'] ?? '';

    if ($action === 'create') {
        $name = trim($_POST['name'] ?? '');
        $swishNumber = preg_replace('/[^0-9]/', '', $_POST['swish_number'] ?? '');
        $swishName = trim($_POST['swish_name'] ?? '');
        $gatewayType = $_POST['gateway_type'] ?? 'manual';

        if (empty($name) || empty($swishNumber)) {
            $message = 'Namn och Swish-nummer krävs';
            $messageType = 'error';
        } else {
            try {
                $db->insert('payment_recipients', [
                    'name' => $name,
                    'swish_number' => $swishNumber,
                    'swish_name' => $swishName ?: $name,
                    'gateway_type' => $gatewayType,
                    'is_active' => 1,
                    'created_at' => date('Y-m-d H:i:s')
                ]);
                $message = 'Swish-konto skapat!';
                $messageType = 'success';
            } catch (Exception $e) {
                $message = 'Fel: ' . $e->getMessage();
                $messageType = 'error';
            }
        }
    }

    elseif ($action === 'update') {
        $recipientId = intval($_POST['recipient_id']);
        $name = trim($_POST['name'] ?? '');
        $swishNumber = preg_replace('/[^0-9]/', '', $_POST['swish_number'] ?? '');
        $swishName = trim($_POST['swish_name'] ?? '');
        $gatewayType = $_POST['gateway_type'] ?? 'manual';
        $isActive = isset($_POST['is_active']) ? 1 : 0;

        if (empty($name) || empty($swishNumber)) {
            $message = 'Namn och Swish-nummer krävs';
            $messageType = 'error';
        } else {
            try {
                $db->update('payment_recipients', [
                    'name' => $name,
                    'swish_number' => $swishNumber,
                    'swish_name' => $swishName ?: $name,
                    'gateway_type' => $gatewayType,
                    'is_active' => $isActive
                ], 'id = ?', [$recipientId]);
                $message = 'Swish-konto uppdaterat!';
                $messageType = 'success';
            } catch (Exception $e) {
                $message = 'Fel: ' . $e->getMessage();
                $messageType = 'error';
            }
        }
    }

    elseif ($action === 'delete' && $isSuperAdmin) {
        $recipientId = intval($_POST['recipient_id']);
        try {
            $db->delete('payment_recipients', 'id = ?', [$recipientId]);
            $message = 'Swish-konto borttaget';
            $messageType = 'success';
        } catch (Exception $e) {
            $message = 'Fel: ' . $e->getMessage();
            $messageType = 'error';
        }
    }
}

// Fetch all payment recipients
$recipients = $db->getAll("
    SELECT pr.*,
           (SELECT COUNT(*) FROM series WHERE payment_recipient_id = pr.id) as series_count,
           (SELECT COUNT(*) FROM events WHERE payment_recipient_id = pr.id) as events_count
    FROM payment_recipients pr
    ORDER BY pr.is_active DESC, pr.name ASC
");

// Check for certificates
$certificates = [];
try {
    $certs = $db->getAll("SELECT payment_recipient_id, cert_type, active FROM gateway_certificates WHERE active = 1");
    foreach ($certs as $c) {
        $certificates[$c['payment_recipient_id']] = $c;
    }
} catch (Exception $e) {}

// Editing mode
$editRecipient = null;
if (isset($_GET['edit']) && is_numeric($_GET['edit'])) {
    $editRecipient = $db->getRow("SELECT * FROM payment_recipients WHERE id = ?", [intval($_GET['edit'])]);
}

// Page config
$page_title = 'Swish-konton';
$breadcrumbs = [
    ['label' => 'Ekonomi', 'url' => '/admin/ekonomi'],
    ['label' => 'Swish-konton']
];
include __DIR__ . '/components/unified-layout.php';
?>

<style>
.swish-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
    gap: var(--space-lg);
}

.swish-card {
    background: var(--color-bg-card);
    border: 1px solid var(--color-border);
    border-radius: var(--radius-lg);
    overflow: hidden;
    transition: all 0.2s ease;
}

.swish-card:hover {
    border-color: var(--color-accent);
}

.swish-card.inactive {
    opacity: 0.6;
}

.swish-card-header {
    display: flex;
    align-items: center;
    gap: var(--space-md);
    padding: var(--space-lg);
    background: var(--color-bg-surface);
    border-bottom: 1px solid var(--color-border);
}

.swish-icon {
    width: 48px;
    height: 48px;
    background: linear-gradient(135deg, #00a3ad, #007a82);
    border-radius: var(--radius-md);
    display: flex;
    align-items: center;
    justify-content: center;
    color: white;
}

.swish-icon svg {
    width: 24px;
    height: 24px;
}

.swish-title {
    flex: 1;
}

.swish-title h3 {
    margin: 0;
    font-size: var(--text-lg);
    color: var(--color-text-primary);
}

.swish-title small {
    color: var(--color-text-muted);
}

.swish-card-body {
    padding: var(--space-lg);
}

.swish-info {
    display: grid;
    gap: var(--space-sm);
    margin-bottom: var(--space-md);
}

.swish-info-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: var(--space-xs) 0;
    border-bottom: 1px solid var(--color-border);
}

.swish-info-row:last-child {
    border-bottom: none;
}

.swish-info-label {
    font-size: var(--text-sm);
    color: var(--color-text-secondary);
}

.swish-info-value {
    font-weight: 500;
    font-family: monospace;
}

.swish-card-actions {
    display: flex;
    gap: var(--space-sm);
    flex-wrap: wrap;
}

.usage-badges {
    display: flex;
    gap: var(--space-xs);
    margin-top: var(--space-sm);
}

/* Create form */
.create-form {
    background: var(--color-bg-card);
    border: 2px dashed var(--color-border);
    border-radius: var(--radius-lg);
    padding: var(--space-xl);
}

.create-form h3 {
    margin: 0 0 var(--space-lg) 0;
    display: flex;
    align-items: center;
    gap: var(--space-sm);
}

.form-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: var(--space-md);
}
</style>

<?php if ($message): ?>
<div class="alert alert-<?= $messageType === 'success' ? 'success' : ($messageType === 'error' ? 'error' : 'info') ?> mb-lg">
    <?= htmlspecialchars($message) ?>
</div>
<?php endif; ?>

<!-- Create/Edit Form -->
<div class="create-form mb-xl">
    <h3>
        <i data-lucide="<?= $editRecipient ? 'edit' : 'plus-circle' ?>"></i>
        <?= $editRecipient ? 'Redigera Swish-konto' : 'Skapa nytt Swish-konto' ?>
    </h3>

    <form method="POST">
        <?= csrf_field() ?>
        <input type="hidden" name="action" value="<?= $editRecipient ? 'update' : 'create' ?>">
        <?php if ($editRecipient): ?>
        <input type="hidden" name="recipient_id" value="<?= $editRecipient['id'] ?>">
        <?php endif; ?>

        <div class="form-grid">
            <div class="admin-form-group">
                <label class="admin-form-label">Namn *</label>
                <input type="text" name="name" class="admin-form-input" required
                       value="<?= htmlspecialchars($editRecipient['name'] ?? '') ?>"
                       placeholder="T.ex. Arrangörsnamn">
            </div>

            <div class="admin-form-group">
                <label class="admin-form-label">Swish-nummer *</label>
                <input type="text" name="swish_number" class="admin-form-input" required
                       value="<?= htmlspecialchars($editRecipient['swish_number'] ?? '') ?>"
                       placeholder="1234567890">
                <small class="text-secondary">10 siffror (mobilnr eller företagsnr)</small>
            </div>

            <div class="admin-form-group">
                <label class="admin-form-label">Visningsnamn</label>
                <input type="text" name="swish_name" class="admin-form-input"
                       value="<?= htmlspecialchars($editRecipient['swish_name'] ?? '') ?>"
                       placeholder="Visas vid betalning">
            </div>

            <div class="admin-form-group">
                <label class="admin-form-label">Betalningstyp</label>
                <select name="gateway_type" class="admin-form-select">
                    <option value="manual" <?= ($editRecipient['gateway_type'] ?? 'manual') === 'manual' ? 'selected' : '' ?>>
                        Manuell Swish (användare verifierar)
                    </option>
                    <option value="swish_handel" <?= ($editRecipient['gateway_type'] ?? '') === 'swish_handel' ? 'selected' : '' ?>>
                        Swish Handel API (automatisk)
                    </option>
                </select>
            </div>

            <?php if ($editRecipient): ?>
            <div class="admin-form-group">
                <label class="admin-form-label flex items-center gap-sm">
                    <input type="checkbox" name="is_active" value="1"
                           <?= ($editRecipient['is_active'] ?? 1) ? 'checked' : '' ?>>
                    Aktiv
                </label>
            </div>
            <?php endif; ?>
        </div>

        <div class="flex gap-md mt-lg">
            <button type="submit" class="btn-admin btn-admin-primary">
                <i data-lucide="<?= $editRecipient ? 'save' : 'plus' ?>"></i>
                <?= $editRecipient ? 'Spara ändringar' : 'Skapa konto' ?>
            </button>
            <?php if ($editRecipient): ?>
            <a href="/admin/swish-accounts" class="btn-admin btn-admin-secondary">Avbryt</a>
            <?php endif; ?>
        </div>
    </form>
</div>

<!-- Existing Accounts -->
<h2 class="mb-lg flex items-center gap-sm">
    <i data-lucide="smartphone"></i>
    Befintliga Swish-konton (<?= count($recipients) ?>)
</h2>

<?php if (empty($recipients)): ?>
<div class="alert alert-info">
    <i data-lucide="info"></i>
    Inga Swish-konton skapade ännu. Använd formuläret ovan för att skapa ett.
</div>
<?php else: ?>
<div class="swish-grid">
    <?php foreach ($recipients as $r):
        $hasCert = isset($certificates[$r['id']]);
        $isAuto = $r['gateway_type'] === 'swish_handel';
    ?>
    <div class="swish-card <?= !$r['is_active'] ? 'inactive' : '' ?>">
        <div class="swish-card-header">
            <div class="swish-icon">
                <i data-lucide="smartphone"></i>
            </div>
            <div class="swish-title">
                <h3><?= htmlspecialchars($r['name']) ?></h3>
                <small>
                    <?= $isAuto ? 'Swish Handel (automatisk)' : 'Manuell Swish' ?>
                    <?php if (!$r['is_active']): ?>
                        <span class="badge badge-secondary">Inaktiv</span>
                    <?php endif; ?>
                </small>
            </div>
        </div>

        <div class="swish-card-body">
            <div class="swish-info">
                <div class="swish-info-row">
                    <span class="swish-info-label">Swish-nummer</span>
                    <span class="swish-info-value"><?= htmlspecialchars($r['swish_number']) ?></span>
                </div>
                <div class="swish-info-row">
                    <span class="swish-info-label">Visningsnamn</span>
                    <span class="swish-info-value"><?= htmlspecialchars($r['swish_name'] ?: '-') ?></span>
                </div>
                <?php if ($isAuto): ?>
                <div class="swish-info-row">
                    <span class="swish-info-label">Certifikat</span>
                    <span class="swish-info-value">
                        <?php if ($hasCert): ?>
                            <span class="badge badge-success">Uppladdat</span>
                        <?php else: ?>
                            <span class="badge badge-warning">Saknas</span>
                        <?php endif; ?>
                    </span>
                </div>
                <?php endif; ?>
            </div>

            <div class="usage-badges">
                <?php if ($r['series_count'] > 0): ?>
                <span class="badge badge-info"><?= $r['series_count'] ?> serier</span>
                <?php endif; ?>
                <?php if ($r['events_count'] > 0): ?>
                <span class="badge badge-info"><?= $r['events_count'] ?> events</span>
                <?php endif; ?>
                <?php if ($r['series_count'] == 0 && $r['events_count'] == 0): ?>
                <span class="badge badge-secondary">Inte använd</span>
                <?php endif; ?>
            </div>

            <div class="swish-card-actions mt-md">
                <a href="?edit=<?= $r['id'] ?>" class="btn-admin btn-admin-sm btn-admin-secondary">
                    <i data-lucide="edit"></i> Redigera
                </a>
                <?php if ($isAuto && $isSuperAdmin): ?>
                <a href="/admin/certificates?id=<?= $r['id'] ?>" class="btn-admin btn-admin-sm btn-admin-secondary">
                    <i data-lucide="shield-check"></i> Certifikat
                </a>
                <?php endif; ?>
                <?php if ($isSuperAdmin && $r['series_count'] == 0 && $r['events_count'] == 0): ?>
                <form method="POST" class="inline" onsubmit="return confirm('Ta bort detta Swish-konto?');">
                    <?= csrf_field() ?>
                    <input type="hidden" name="action" value="delete">
                    <input type="hidden" name="recipient_id" value="<?= $r['id'] ?>">
                    <button type="submit" class="btn-admin btn-admin-sm btn-admin-danger">
                        <i data-lucide="trash-2"></i>
                    </button>
                </form>
                <?php endif; ?>
            </div>
        </div>
    </div>
    <?php endforeach; ?>
</div>
<?php endif; ?>

<!-- Help Section -->
<div class="admin-card mt-xl">
    <div class="admin-card-header">
        <h2><i data-lucide="help-circle"></i> Hur fungerar Swish-betalningar?</h2>
    </div>
    <div class="admin-card-body">
        <div class="grid grid-cols-1 gs-md-grid-cols-2 gap-lg">
            <div>
                <h4 class="text-accent mb-sm">Manuell Swish</h4>
                <p class="text-secondary text-sm">
                    Deltagaren får en Swish-länk och betalar manuellt. Admin bekräftar betalningen i orderhanteringen.
                    Kräver ingen extra konfiguration.
                </p>
            </div>
            <div>
                <h4 class="text-accent mb-sm">Swish Handel (automatisk)</h4>
                <p class="text-secondary text-sm">
                    Betalningen bekräftas automatiskt via Swish API.
                    Kräver avtal med banken och ett .p12-certifikat som laddas upp under "Certifikat".
                </p>
            </div>
        </div>
    </div>
</div>

<script>
document.addEventListener('DOMContentLoaded', function() {
    if (typeof lucide !== 'undefined') {
        lucide.createIcons();
    }
});
</script>

<?php include __DIR__ . '/components/unified-layout-footer.php'; ?>
