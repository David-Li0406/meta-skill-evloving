<?php
/**
 * Pricing Template Edit (Simplified)
 * Allows promotors/admins to edit a specific pricing template for their event
 */

require_once __DIR__ . '/../config.php';
require_admin();

$db = getDB();
$templateId = intval($_GET['id'] ?? 0);
$eventId = intval($_GET['event'] ?? 0);

if (!$templateId) {
    set_flash('error', 'Ingen prismall angiven');
    redirect('/admin/');
}

// Verify access - either super_admin, or promotor with access to an event using this template
$hasAccess = false;
$backUrl = '/admin/';

if (isRole('super_admin')) {
    $hasAccess = true;
    $backUrl = '/admin/pricing-templates.php';
} else {
    // Check if user is promotor with access to this template via event
    if ($eventId) {
        $promotorEvents = getPromotorEvents();
        $promotorEventIds = array_column($promotorEvents, 'id');

        if (in_array($eventId, $promotorEventIds)) {
            // Check that this event actually uses this template
            $event = $db->getRow("SELECT id, pricing_template_id FROM events WHERE id = ?", [$eventId]);
            if ($event && intval($event['pricing_template_id']) === $templateId) {
                $hasAccess = true;
                $backUrl = '/admin/event-edit.php?id=' . $eventId;
            }
        }
    }

    // Also check if admin (not super_admin) - they can edit if linked to their events
    if (!$hasAccess && isRole('admin')) {
        $hasAccess = true;
        $backUrl = $eventId ? '/admin/event-edit.php?id=' . $eventId : '/admin/events.php';
    }
}

if (!$hasAccess) {
    set_flash('error', 'Du har inte behörighet att redigera denna prismall');
    redirect('/admin/');
}

// Load the template
$template = $db->getRow("SELECT * FROM pricing_templates WHERE id = ?", [$templateId]);
if (!$template) {
    set_flash('error', 'Prismallen hittades inte');
    redirect($backUrl);
}

// Load template rules
$rules = $db->getAll("SELECT * FROM pricing_template_rules WHERE template_id = ?", [$templateId]);
$templateRules = [];
foreach ($rules as $rule) {
    $templateRules[$rule['class_id']] = $rule;
}

// Load classes
$classes = $db->getAll("SELECT id, name, display_name FROM classes ORDER BY sort_order ASC");

// Handle POST
$message = '';
$messageType = 'info';

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    checkCsrf();
    $action = $_POST['action'] ?? '';

    if ($action === 'update_settings') {
        $earlyBirdPercent = floatval($_POST['early_bird_percent'] ?? 15);
        $earlyBirdDays = intval($_POST['early_bird_days'] ?? 21);
        $lateFeePercent = floatval($_POST['late_fee_percent'] ?? 25);
        $lateFeeDays = intval($_POST['late_fee_days'] ?? 3);
        $championshipFee = floatval($_POST['championship_fee'] ?? 0);
        $championshipFeeDesc = trim($_POST['championship_fee_description'] ?? '');

        $db->update('pricing_templates', [
            'early_bird_percent' => $earlyBirdPercent,
            'early_bird_days_before' => $earlyBirdDays,
            'late_fee_percent' => $lateFeePercent,
            'late_fee_days_before' => $lateFeeDays,
            'championship_fee' => $championshipFee,
            'championship_fee_description' => $championshipFeeDesc ?: null
        ], 'id = ?', [$templateId]);

        // Reload template
        $template = $db->getRow("SELECT * FROM pricing_templates WHERE id = ?", [$templateId]);
        $message = 'Inställningar sparade!';
        $messageType = 'success';
    }

    elseif ($action === 'save_prices') {
        $classIds = $_POST['class_id'] ?? [];
        $basePrices = $_POST['base_price'] ?? [];

        $saved = 0;
        foreach ($classIds as $index => $classId) {
            $basePrice = floatval($basePrices[$index] ?? 0);

            if ($basePrice > 0) {
                $existing = $db->getRow("SELECT id FROM pricing_template_rules WHERE template_id = ? AND class_id = ?", [$templateId, $classId]);

                if ($existing) {
                    $db->update('pricing_template_rules', ['base_price' => $basePrice], 'id = ?', [$existing['id']]);
                } else {
                    $db->insert('pricing_template_rules', [
                        'template_id' => $templateId,
                        'class_id' => $classId,
                        'base_price' => $basePrice
                    ]);
                }
                $saved++;
            } else {
                $db->delete('pricing_template_rules', 'template_id = ? AND class_id = ?', [$templateId, $classId]);
            }
        }

        // Reload rules
        $rules = $db->getAll("SELECT * FROM pricing_template_rules WHERE template_id = ?", [$templateId]);
        $templateRules = [];
        foreach ($rules as $rule) {
            $templateRules[$rule['class_id']] = $rule;
        }

        $message = "Sparade $saved priser";
        $messageType = 'success';
    }
}

// Page config
$page_title = 'Redigera Prismall - ' . $template['name'];
$breadcrumbs = [
    ['label' => 'Prismall', 'url' => $backUrl],
    ['label' => $template['name']]
];

include __DIR__ . '/components/unified-layout.php';
?>

<style>
input[type="number"]::-webkit-inner-spin-button,
input[type="number"]::-webkit-outer-spin-button {
    -webkit-appearance: none;
    margin: 0;
}
input[type="number"] {
    -moz-appearance: textfield;
}
</style>

<div class="card mb-lg">
    <div class="card-body">
        <div class="flex justify-between items-center">
            <div>
                <h1>
                    <i data-lucide="file-text"></i>
                    <?= htmlspecialchars($template['name']) ?>
                </h1>
                <p class="text-secondary text-sm">
                    Konfigurera priser för denna mall
                </p>
            </div>
            <a href="<?= $backUrl ?>" class="btn btn--secondary">
                <i data-lucide="arrow-left"></i>
                Tillbaka
            </a>
        </div>
    </div>
</div>

<?php if ($message): ?>
<div class="alert alert-<?= $messageType ?> mb-lg">
    <?= htmlspecialchars($message) ?>
</div>
<?php endif; ?>

<!-- Pricing Settings -->
<div class="card mb-lg">
    <div class="card-header">
        <h2>
            <i data-lucide="settings"></i>
            Prisregler
        </h2>
    </div>
    <div class="card-body">
        <form method="POST">
            <?= csrf_field() ?>
            <input type="hidden" name="action" value="update_settings">

            <div class="grid grid-cols-1 md-grid-cols-2 gap-md">
                <div class="card p-md" style="background: var(--gs-success-bg, #f0fdf4);">
                    <label class="label text-success">Early Bird (rabatt)</label>
                    <div class="flex gap-sm items-center mt-sm flex-wrap">
                        <input type="number" name="early_bird_percent" class="input"
                            value="<?= $template['early_bird_percent'] ?? 15 ?>"
                            min="0" max="100" style="width: 80px;">
                        <span>% rabatt,</span>
                        <input type="number" name="early_bird_days" class="input"
                            value="<?= $template['early_bird_days_before'] ?? 21 ?>"
                            min="0" max="90" style="width: 80px;">
                        <span>dagar före event</span>
                    </div>
                </div>
                <div class="card p-md" style="background: var(--gs-warning-bg, #fffbeb);">
                    <label class="label text-warning">Efteranmälan (tillägg)</label>
                    <div class="flex gap-sm items-center mt-sm flex-wrap">
                        <input type="number" name="late_fee_percent" class="input"
                            value="<?= $template['late_fee_percent'] ?? 25 ?>"
                            min="0" max="100" style="width: 80px;">
                        <span>% tillägg,</span>
                        <input type="number" name="late_fee_days" class="input"
                            value="<?= $template['late_fee_days_before'] ?? 3 ?>"
                            min="0" max="30" style="width: 80px;">
                        <span>dagar före event</span>
                    </div>
                </div>
            </div>

            <!-- Championship Fee -->
            <div class="card p-md mt-md" style="background: var(--color-accent-light, rgba(55, 212, 214, 0.1)); border: 1px solid var(--color-accent);">
                <label class="label" style="color: var(--color-accent);">
                    <i data-lucide="trophy"></i>
                    SM-tillägg (Svenska Mästerskap)
                </label>
                <p class="text-sm text-secondary mb-sm">
                    Automatiskt pristillägg för events markerade som Svenska Mästerskap.
                </p>
                <div class="flex gap-sm items-center mt-sm flex-wrap">
                    <input type="number" name="championship_fee" class="input"
                        value="<?= $template['championship_fee'] ?? 0 ?>"
                        min="0" step="1" style="width: 100px;">
                    <span>kr tillägg per anmälan</span>
                </div>
                <div class="mt-sm">
                    <label class="label text-sm">Beskrivning (visas för deltagare)</label>
                    <input type="text" name="championship_fee_description" class="input"
                        value="<?= htmlspecialchars($template['championship_fee_description'] ?? '') ?>"
                        placeholder="T.ex. 'SM-avgift till Svenska Cykelförbundet'"
                        style="width: 100%; max-width: 400px;">
                </div>
            </div>

            <div class="mt-md">
                <button type="submit" class="btn btn--primary">
                    <i data-lucide="save"></i>
                    Spara inställningar
                </button>
            </div>
        </form>
    </div>
</div>

<!-- Pricing per Class -->
<div class="card">
    <div class="card-header">
        <h2>
            <i data-lucide="credit-card"></i>
            Grundpriser per klass
        </h2>
    </div>
    <div class="card-body">
        <form method="POST">
            <?= csrf_field() ?>
            <input type="hidden" name="action" value="save_prices">

            <?php
            $ebPercent = $template['early_bird_percent'] ?? 15;
            $latePercent = $template['late_fee_percent'] ?? 25;
            ?>

            <div class="table-responsive">
                <table class="table">
                    <thead>
                        <tr>
                            <th>Klass</th>
                            <th>Ordinarie pris</th>
                            <th>Early Bird (-<?= $ebPercent ?>%)</th>
                            <th>Efteranmälan (+<?= $latePercent ?>%)</th>
                        </tr>
                    </thead>
                    <tbody>
                        <?php foreach ($classes as $class):
                            $rule = $templateRules[$class['id']] ?? null;
                            $basePrice = $rule['base_price'] ?? 0;
                            $ebPrice = $basePrice * (1 - $ebPercent / 100);
                            $latePrice = $basePrice * (1 + $latePercent / 100);
                        ?>
                        <tr data-row="<?= $class['id'] ?>">
                            <td>
                                <input type="hidden" name="class_id[]" value="<?= $class['id'] ?>">
                                <strong><?= htmlspecialchars($class['display_name'] ?: $class['name']) ?></strong>
                            </td>
                            <td>
                                <div class="flex items-center gap-xs">
                                    <input type="number" name="base_price[]" class="input"
                                        data-class="<?= $class['id'] ?>"
                                        value="<?= $basePrice ?: '' ?>"
                                        min="0" step="1" style="width: 100px;"
                                        oninput="calculatePrices(<?= $class['id'] ?>, <?= $ebPercent ?>, <?= $latePercent ?>)">
                                    <span class="text-secondary">kr</span>
                                </div>
                            </td>
                            <td>
                                <span id="eb-<?= $class['id'] ?>" class="text-success font-bold">
                                    <?= $basePrice > 0 ? number_format($ebPrice, 0) . ' kr' : '-' ?>
                                </span>
                            </td>
                            <td>
                                <span id="late-<?= $class['id'] ?>" class="text-warning font-bold">
                                    <?= $basePrice > 0 ? number_format($latePrice, 0) . ' kr' : '-' ?>
                                </span>
                            </td>
                        </tr>
                        <?php endforeach; ?>
                    </tbody>
                </table>
            </div>

            <div class="mt-lg">
                <button type="submit" class="btn btn--primary">
                    <i data-lucide="save"></i>
                    Spara priser
                </button>
            </div>
        </form>
    </div>
</div>

<script>
function calculatePrices(classId, ebPercent, latePercent) {
    const input = document.querySelector(`input[data-class="${classId}"]`);
    const basePrice = parseFloat(input.value) || 0;

    const ebPrice = basePrice * (1 - ebPercent / 100);
    const latePrice = basePrice * (1 + latePercent / 100);

    document.getElementById(`eb-${classId}`).textContent =
        basePrice > 0 ? Math.round(ebPrice).toLocaleString('sv-SE') + ' kr' : '-';
    document.getElementById(`late-${classId}`).textContent =
        basePrice > 0 ? Math.round(latePrice).toLocaleString('sv-SE') + ' kr' : '-';
}

// Initialize Lucide icons
if (typeof lucide !== 'undefined') {
    lucide.createIcons();
}
</script>

<?php include __DIR__ . '/components/unified-layout-footer.php'; ?>
