<?php
/**
 * Series Pricing, Registration & Class Rules
 * Configure pricing, registration settings and license restrictions for a series
 */

require_once __DIR__ . '/../config.php';
require_admin();

$db = getDB();

// Get series ID
$seriesId = isset($_GET['id']) ? intval($_GET['id']) : 0;

if ($seriesId <= 0) {
    $_SESSION['flash_message'] = 'Välj en serie';
    $_SESSION['flash_type'] = 'warning';
    header('Location: /admin/series.php');
    exit;
}

// Fetch series
$series = $db->getRow("SELECT * FROM series WHERE id = ?", [$seriesId]);

if (!$series) {
    $_SESSION['flash_message'] = 'Serie hittades inte';
    $_SESSION['flash_type'] = 'error';
    header('Location: /admin/series.php');
    exit;
}

// Fetch pricing templates for dropdown
$pricingTemplates = $db->getAll("SELECT id, name, is_default FROM pricing_templates ORDER BY is_default DESC, name ASC");

// Fetch events in this series
$seriesEvents = $db->getAll("
    SELECT id, name, date, location, registration_deadline, registration_opens, pricing_template_id
    FROM events
    WHERE series_id = ?
    ORDER BY date ASC
", [$seriesId]);

// Initialize message
$message = '';
$messageType = 'info';

// Handle POST actions
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    checkCsrf();
    $action = $_POST['action'] ?? '';

    // Save series-level registration settings
    if ($action === 'save_series_registration') {
        $registrationEnabled = isset($_POST['registration_enabled']) ? 1 : 0;
        $pricingTemplateId = !empty($_POST['pricing_template_id']) ? intval($_POST['pricing_template_id']) : null;

        $db->update('series', [
            'registration_enabled' => $registrationEnabled,
            'pricing_template_id' => $pricingTemplateId
        ], 'id = ?', [$seriesId]);

        // Refresh series data
        $series = $db->getRow("SELECT * FROM series WHERE id = ?", [$seriesId]);

        $message = 'Serieinställningar sparade!';
        $messageType = 'success';
    }

    // Save series pass (season pass) settings
    elseif ($action === 'save_series_pass') {
        $allowSeriesRegistration = isset($_POST['allow_series_registration']) ? 1 : 0;
        $seriesPriceType = $_POST['series_price_type'] ?? 'calculated';
        $seriesDiscountPercent = floatval($_POST['series_discount_percent'] ?? 15);
        $fullSeriesPrice = !empty($_POST['full_series_price']) ? floatval($_POST['full_series_price']) : null;

        $db->update('series', [
            'allow_series_registration' => $allowSeriesRegistration,
            'series_price_type' => $seriesPriceType,
            'series_discount_percent' => $seriesDiscountPercent,
            'full_series_price' => $fullSeriesPrice
        ], 'id = ?', [$seriesId]);

        // Refresh series data
        $series = $db->getRow("SELECT * FROM series WHERE id = ?", [$seriesId]);

        $message = 'Serie-pass inställningar sparade!';
        $messageType = 'success';
    }

    // Save individual event registration times
    elseif ($action === 'save_event_registration') {
        $eventIds = $_POST['event_id'] ?? [];
        $opensDate = $_POST['opens_date'] ?? [];
        $opensTime = $_POST['opens_time'] ?? [];
        $closesDate = $_POST['closes_date'] ?? [];
        $closesTime = $_POST['closes_time'] ?? [];

        $saved = 0;
        foreach ($eventIds as $index => $eventId) {
            $eventId = intval($eventId);
            $regOpens = !empty($opensDate[$index]) ? $opensDate[$index] . ' ' . ($opensTime[$index] ?? '00:00:00') : null;
            $regCloses = !empty($closesDate[$index]) ? $closesDate[$index] . ' ' . ($closesTime[$index] ?? '23:59:59') : null;

            $db->update('events', [
                'registration_opens' => $regOpens,
                'registration_deadline' => $regCloses
            ], 'id = ?', [$eventId]);
            $saved++;
        }

        // Refresh events
        $seriesEvents = $db->getAll("
            SELECT id, name, date, location, registration_deadline, registration_opens, pricing_template_id
            FROM events
            WHERE series_id = ?
            ORDER BY date ASC
        ", [$seriesId]);

        $message = "Sparade anmälningstider för $saved events";
        $messageType = 'success';
    }

    // Save class lock settings
    elseif ($action === 'save_class_locks') {
        $classIds = $_POST['class_id'] ?? [];
        $isLocked = $_POST['is_locked'] ?? [];

        // Clear existing locks for this series
        $db->query("DELETE FROM series_class_rules WHERE series_id = ?", [$seriesId]);

        $saved = 0;
        foreach ($classIds as $classId) {
            $locked = isset($isLocked[$classId]) ? 1 : 0;
            if ($locked) {
                $db->insert('series_class_rules', [
                    'series_id' => $seriesId,
                    'class_id' => intval($classId),
                    'is_active' => 0 // Locked = not active for registration
                ]);
                $saved++;
            }
        }

        $message = "Sparade klasslåsningar ($saved klasser låsta)";
        $messageType = 'success';
    }
}

// Get active tab - default to registration
$activeTab = $_GET['tab'] ?? 'registration';

// Fetch data for pricing tab
$pricingTemplate = null;
$templatePrices = [];
if ($series['pricing_template_id']) {
    $pricingTemplate = $db->getRow("SELECT * FROM pricing_templates WHERE id = ?", [$series['pricing_template_id']]);
    if ($pricingTemplate) {
        $templatePrices = $db->getAll("
            SELECT ptr.*, c.name AS class_name, c.display_name
            FROM pricing_template_rules ptr
            JOIN classes c ON c.id = ptr.class_id
            WHERE ptr.template_id = ?
            ORDER BY c.sort_order ASC
        ", [$pricingTemplate['id']]);
    }
}

// Fetch data for rules tab
$allClasses = $db->getAll("SELECT id, name, display_name, gender FROM classes WHERE active = 1 ORDER BY sort_order ASC");

// Get locked classes for this series
$lockedClasses = [];
$lockedRows = $db->getAll("SELECT class_id FROM series_class_rules WHERE series_id = ? AND is_active = 0", [$seriesId]);
foreach ($lockedRows as $row) {
    $lockedClasses[$row['class_id']] = true;
}

// Determine event license class based on series (for license matrix)
$eventLicenseClass = 'sportmotion'; // Default
if (stripos($series['name'], 'SM') !== false || stripos($series['name'], 'Swedish Championship') !== false) {
    $eventLicenseClass = 'national';
}

// Get license matrix data
$licenseTypes = $db->getAll("SELECT code, name FROM license_types WHERE is_active = 1 ORDER BY priority DESC");
$licenseMatrix = [];
try {
    $matrixRows = $db->getAll("
        SELECT cle.class_id, cle.license_type_code
        FROM class_license_eligibility cle
        WHERE cle.event_license_class = ? AND cle.is_allowed = 1
    ", [$eventLicenseClass]);
    foreach ($matrixRows as $row) {
        $licenseMatrix[$row['class_id']][$row['license_type_code']] = true;
    }
} catch (Exception $e) {
    // Table might not exist
}

// Page config for admin layout
$page_title = 'Anmälan & Priser - ' . $series['name'];
$breadcrumbs = [
    ['label' => 'Serier', 'url' => '/admin/series.php'],
    ['label' => $series['name']]
];

include __DIR__ . '/components/unified-layout.php';
?>

<!-- Header -->
<div class="flex justify-between items-center mb-lg">
    <div>
        <p class="text-secondary text-sm">
            Konfigurera anmälan, priser och klassregler
        </p>
    </div>
    <a href="/admin/series.php" class="btn-admin btn-admin-secondary">
        <i data-lucide="arrow-left"></i>
        Tillbaka
    </a>
</div>

<?php if ($message): ?>
<div class="alert alert-<?= $messageType ?> mb-lg">
    <?= htmlspecialchars($message) ?>
</div>
<?php endif; ?>

<!-- Tabs -->
<div class="admin-tabs mb-lg">
    <a href="?id=<?= $seriesId ?>&tab=registration" class="admin-tab <?= $activeTab === 'registration' ? 'active' : '' ?>">
        <i data-lucide="clipboard-list"></i>
        Anmälan
    </a>
    <a href="?id=<?= $seriesId ?>&tab=pricing" class="admin-tab <?= $activeTab === 'pricing' ? 'active' : '' ?>">
        <i data-lucide="credit-card"></i>
        Priser
    </a>
    <a href="?id=<?= $seriesId ?>&tab=rules" class="admin-tab <?= $activeTab === 'rules' ? 'active' : '' ?>">
        <i data-lucide="shield-check"></i>
        Klassregler
    </a>
</div>

<?php if ($activeTab === 'registration'): ?>
<!-- Registration Tab -->

<!-- Series-level settings -->
<div class="admin-card mb-lg">
    <div class="admin-card-header">
        <h2>
            <i data-lucide="settings"></i>
            Serieinställningar
        </h2>
    </div>
    <div class="admin-card-body">
        <form method="POST">
            <?= csrf_field() ?>
            <input type="hidden" name="action" value="save_series_registration">

            <div class="admin-form-row">
                <div class="admin-form-group">
                    <label class="admin-form-label">
                        <input type="checkbox" name="registration_enabled" value="1"
                            <?= ($series['registration_enabled'] ?? 0) ? 'checked' : '' ?>>
                        Anmälan aktiverad för serien
                    </label>
                    <small class="admin-form-help">Aktivera för att tillåta anmälan till events i denna serie</small>
                </div>

                <div class="admin-form-group">
                    <label class="admin-form-label">Standard prismall</label>
                    <select name="pricing_template_id" class="admin-form-select">
                        <option value="">-- Välj prismall --</option>
                        <?php foreach ($pricingTemplates as $template): ?>
                            <option value="<?= $template['id'] ?>"
                                <?= ($series['pricing_template_id'] ?? '') == $template['id'] ? 'selected' : '' ?>>
                                <?= htmlspecialchars($template['name']) ?>
                                <?= $template['is_default'] ? '(Standard)' : '' ?>
                            </option>
                        <?php endforeach; ?>
                    </select>
                    <small class="admin-form-help">
                        Används som default för alla events i serien.
                        <a href="/admin/pricing-templates.php">Hantera prismallar</a>
                    </small>
                </div>
            </div>

            <div class="mt-md">
                <button type="submit" class="btn-admin btn-admin-primary">
                    <i data-lucide="save"></i>
                    Spara serieinställningar
                </button>
            </div>
        </form>
    </div>
</div>

<!-- Serie-pass (Season Pass) Settings -->
<div class="admin-card mb-lg">
    <div class="admin-card-header">
        <h2>
            <i data-lucide="ticket"></i>
            Serie-pass (Hela säsongen)
        </h2>
    </div>
    <div class="admin-card-body">
        <form method="POST">
            <?= csrf_field() ?>
            <input type="hidden" name="action" value="save_series_pass">

            <div class="admin-form-group mb-lg">
                <label class="admin-form-label" style="display: flex; align-items: center; gap: var(--space-sm);">
                    <input type="checkbox" name="allow_series_registration" value="1"
                        <?= ($series['allow_series_registration'] ?? 0) ? 'checked' : '' ?>>
                    <strong>Tillåt köp av serie-pass</strong>
                </label>
                <small class="admin-form-help">
                    När aktiverat kan deltagare köpa ett pass för ALLA events i serien till rabatterat pris.
                </small>
            </div>

            <div class="admin-form-row">
                <div class="admin-form-group">
                    <label class="admin-form-label">Prismodell</label>
                    <select name="series_price_type" class="admin-form-select" id="series_price_type" onchange="togglePriceFields()">
                        <option value="calculated" <?= ($series['series_price_type'] ?? 'calculated') === 'calculated' ? 'selected' : '' ?>>
                            Beräknat (summa av alla event minus rabatt)
                        </option>
                        <option value="fixed" <?= ($series['series_price_type'] ?? '') === 'fixed' ? 'selected' : '' ?>>
                            Fast pris
                        </option>
                    </select>
                </div>

                <div class="admin-form-group" id="discount_field">
                    <label class="admin-form-label">Rabatt vid serieanmälan (%)</label>
                    <input type="number" name="series_discount_percent" class="admin-form-input"
                           value="<?= htmlspecialchars($series['series_discount_percent'] ?? 15) ?>"
                           min="0" max="50" step="1">
                    <small class="admin-form-help">
                        T.ex. 15% = betala 85% av totalpriset för alla events
                    </small>
                </div>

                <div class="admin-form-group" id="fixed_price_field" style="display: none;">
                    <label class="admin-form-label">Fast pris för hela serien (kr)</label>
                    <input type="number" name="full_series_price" class="admin-form-input"
                           value="<?= htmlspecialchars($series['full_series_price'] ?? '') ?>"
                           min="0" step="50" placeholder="T.ex. 2500">
                    <small class="admin-form-help">
                        Samma pris oavsett klass
                    </small>
                </div>
            </div>

            <?php
            // Calculate example prices
            $eventCount = count($seriesEvents);
            $exampleEventPrice = 450; // Typical price
            $discountPercent = floatval($series['series_discount_percent'] ?? 15);
            $totalWithoutDiscount = $eventCount * $exampleEventPrice;
            $totalWithDiscount = $totalWithoutDiscount * (1 - $discountPercent / 100);
            ?>
            <?php if ($eventCount > 0): ?>
            <div class="p-md mb-lg" style="background: var(--color-bg-tertiary); border-radius: var(--radius-md);">
                <strong>Exempel:</strong> <?= $eventCount ?> events × <?= $exampleEventPrice ?> kr = <?= number_format($totalWithoutDiscount, 0) ?> kr
                <br>
                Med <?= $discountPercent ?>% rabatt: <strong><?= number_format($totalWithDiscount, 0) ?> kr</strong>
                (spara <?= number_format($totalWithoutDiscount - $totalWithDiscount, 0) ?> kr)
            </div>
            <?php endif; ?>

            <div class="mt-md">
                <button type="submit" class="btn-admin btn-admin-primary">
                    <i data-lucide="save"></i>
                    Spara serie-pass inställningar
                </button>
            </div>
        </form>
    </div>
</div>

<script>
function togglePriceFields() {
    const priceType = document.getElementById('series_price_type').value;
    document.getElementById('discount_field').style.display = priceType === 'calculated' ? 'block' : 'none';
    document.getElementById('fixed_price_field').style.display = priceType === 'fixed' ? 'block' : 'none';
}
// Run on page load
document.addEventListener('DOMContentLoaded', togglePriceFields);
</script>

<!-- Event-specific registration times -->
<div class="admin-card">
    <div class="admin-card-header">
        <h2>
            <i data-lucide="calendar"></i>
            Anmälningstider per event
        </h2>
    </div>
    <div class="admin-card-body">
        <?php if (empty($seriesEvents)): ?>
            <p class="text-secondary">Inga events finns i denna serie ännu.</p>
        <?php else: ?>
            <form method="POST">
                <?= csrf_field() ?>
                <input type="hidden" name="action" value="save_event_registration">

                <div class="admin-table-container">
                    <table class="admin-table">
                        <thead>
                            <tr>
                                <th>Event</th>
                                <th>Datum</th>
                                <th>Anmälan öppnar</th>
                                <th>Anmälan stänger</th>
                            </tr>
                        </thead>
                        <tbody>
                            <?php foreach ($seriesEvents as $event):
                                $opensDate = $event['registration_opens'] ? date('Y-m-d', strtotime($event['registration_opens'])) : '';
                                $opensTime = $event['registration_opens'] ? date('H:i', strtotime($event['registration_opens'])) : '00:00';
                                $closesDate = $event['registration_deadline'] ? date('Y-m-d', strtotime($event['registration_deadline'])) : '';
                                $closesTime = $event['registration_deadline'] ? date('H:i', strtotime($event['registration_deadline'])) : '23:59';
                            ?>
                            <tr>
                                <td>
                                    <input type="hidden" name="event_id[]" value="<?= $event['id'] ?>">
                                    <strong><?= htmlspecialchars($event['name']) ?></strong>
                                    <small class="text-secondary d-block"><?= htmlspecialchars($event['location'] ?? '') ?></small>
                                </td>
                                <td>
                                    <span class="text-muted"><?= date('Y-m-d', strtotime($event['date'])) ?></span>
                                </td>
                                <td>
                                    <div class="flex gap-xs items-center">
                                        <input type="date" name="opens_date[]" class="admin-form-input"
                                            value="<?= $opensDate ?>" style="width: 140px;">
                                        <input type="time" name="opens_time[]" class="admin-form-input"
                                            value="<?= $opensTime ?>" style="width: 100px;">
                                    </div>
                                </td>
                                <td>
                                    <div class="flex gap-xs items-center">
                                        <input type="date" name="closes_date[]" class="admin-form-input"
                                            value="<?= $closesDate ?>" style="width: 140px;">
                                        <input type="time" name="closes_time[]" class="admin-form-input"
                                            value="<?= $closesTime ?>" style="width: 100px;">
                                    </div>
                                </td>
                            </tr>
                            <?php endforeach; ?>
                        </tbody>
                    </table>
                </div>

                <div class="mt-lg">
                    <button type="submit" class="btn-admin btn-admin-primary">
                        <i data-lucide="save"></i>
                        Spara anmälningstider
                    </button>
                </div>
            </form>
        <?php endif; ?>
    </div>
</div>

<?php elseif ($activeTab === 'pricing'): ?>
<!-- Pricing Tab -->
<div class="admin-card">
    <div class="admin-card-header">
        <h2>
            <i data-lucide="credit-card"></i>
            Prismall
        </h2>
    </div>
    <div class="admin-card-body">
        <?php if (!$pricingTemplate): ?>
            <div class="admin-alert admin-alert-warning">
                <i data-lucide="alert-triangle"></i>
                <div>
                    <strong>Ingen prismall vald</strong><br>
                    Välj en prismall under fliken "Anmälan" för att se priser.
                </div>
            </div>
        <?php else: ?>
            <div class="mb-lg">
                <h3 style="margin-bottom: var(--space-sm);"><?= htmlspecialchars($pricingTemplate['name']) ?></h3>
                <?php if ($pricingTemplate['description']): ?>
                    <p class="text-secondary"><?= htmlspecialchars($pricingTemplate['description']) ?></p>
                <?php endif; ?>
            </div>

            <!-- Template settings -->
            <div class="grid grid-cols-2 gap-lg mb-lg" style="max-width: 600px;">
                <div class="admin-card" style="background: var(--color-bg-surface);">
                    <div class="admin-card-body">
                        <div class="text-sm text-secondary mb-xs">Early Bird rabatt</div>
                        <div class="text-lg font-bold text-success">
                            <?= $pricingTemplate['early_bird_percent'] ?>%
                        </div>
                        <div class="text-xs text-muted">
                            <?= $pricingTemplate['early_bird_days_before'] ?> dagar före
                        </div>
                    </div>
                </div>
                <div class="admin-card" style="background: var(--color-bg-surface);">
                    <div class="admin-card-body">
                        <div class="text-sm text-secondary mb-xs">Sen anmälningsavgift</div>
                        <div class="text-lg font-bold text-warning">
                            +<?= $pricingTemplate['late_fee_percent'] ?>%
                        </div>
                        <div class="text-xs text-muted">
                            <?= $pricingTemplate['late_fee_days_before'] ?> dagar före
                        </div>
                    </div>
                </div>
                <?php if (($pricingTemplate['championship_fee'] ?? 0) > 0): ?>
                <div class="admin-card" style="background: var(--color-bg-surface);">
                    <div class="admin-card-body">
                        <div class="text-sm text-secondary mb-xs">SM-tillägg</div>
                        <div class="text-lg font-bold text-accent">
                            +<?= number_format($pricingTemplate['championship_fee'], 0) ?> kr
                        </div>
                        <?php if ($pricingTemplate['championship_fee_description']): ?>
                            <div class="text-xs text-muted">
                                <?= htmlspecialchars($pricingTemplate['championship_fee_description']) ?>
                            </div>
                        <?php endif; ?>
                    </div>
                </div>
                <?php endif; ?>
            </div>

            <!-- Class prices -->
            <?php if (!empty($templatePrices)): ?>
                <h4 style="margin-bottom: var(--space-md);">Klasspriser</h4>
                <div class="admin-table-container">
                    <table class="admin-table">
                        <thead>
                            <tr>
                                <th>Klass</th>
                                <th class="text-right">Grundpris</th>
                                <th class="text-right">Early Bird</th>
                                <th class="text-right">Sen anmälan</th>
                            </tr>
                        </thead>
                        <tbody>
                            <?php foreach ($templatePrices as $price):
                                $basePrice = $price['base_price'];
                                $earlyBird = $basePrice * (1 - $pricingTemplate['early_bird_percent'] / 100);
                                $lateFee = $basePrice * (1 + $pricingTemplate['late_fee_percent'] / 100);
                            ?>
                            <tr>
                                <td>
                                    <strong><?= htmlspecialchars($price['display_name'] ?: $price['class_name']) ?></strong>
                                </td>
                                <td class="text-right">
                                    <?= number_format($basePrice, 0) ?> kr
                                </td>
                                <td class="text-right text-success">
                                    <?= number_format($earlyBird, 0) ?> kr
                                </td>
                                <td class="text-right text-warning">
                                    <?= number_format($lateFee, 0) ?> kr
                                </td>
                            </tr>
                            <?php endforeach; ?>
                        </tbody>
                    </table>
                </div>
            <?php else: ?>
                <div class="admin-alert admin-alert-info">
                    <i data-lucide="info"></i>
                    <div>Inga klasspriser har konfigurerats i denna mall ännu.</div>
                </div>
            <?php endif; ?>

            <div class="mt-lg">
                <a href="/admin/pricing-template-edit.php?id=<?= $pricingTemplate['id'] ?>" class="btn-admin btn-admin-secondary">
                    <i data-lucide="pencil"></i>
                    Redigera prismall
                </a>
            </div>
        <?php endif; ?>
    </div>
</div>

<?php else: ?>
<!-- Class Rules Tab -->
<div class="admin-card">
    <div class="admin-card-header">
        <h2>
            <i data-lucide="shield-check"></i>
            Klassregler & Licensmatris
        </h2>
        <span class="badge badge-info ml-md"><?= ucfirst($eventLicenseClass) ?></span>
    </div>
    <div class="admin-card-body">
        <p class="text-secondary mb-lg">
            Nedan visas vilka licenstyper som får anmäla sig till respektive klass enligt
            <a href="/admin/license-class-matrix.php?tab=<?= $eventLicenseClass ?>">licensmatrisen</a>.
            Du kan låsa klasser som inte ska vara tillgängliga för anmälan i denna serie.
        </p>

        <form method="POST">
            <?= csrf_field() ?>
            <input type="hidden" name="action" value="save_class_locks">

            <div class="admin-table-container">
                <table class="admin-table">
                    <thead>
                        <tr>
                            <th>Klass</th>
                            <?php foreach ($licenseTypes as $lt): ?>
                                <th class="text-center" style="font-size: 0.75rem; padding: var(--space-xs);">
                                    <?= htmlspecialchars($lt['name']) ?>
                                </th>
                            <?php endforeach; ?>
                            <th class="text-center">Låst</th>
                        </tr>
                    </thead>
                    <tbody>
                        <?php foreach ($allClasses as $class): ?>
                        <tr class="<?= isset($lockedClasses[$class['id']]) ? 'opacity-50' : '' ?>">
                            <td>
                                <input type="hidden" name="class_id[]" value="<?= $class['id'] ?>">
                                <strong><?= htmlspecialchars($class['display_name'] ?: $class['name']) ?></strong>
                                <?php if ($class['gender'] === 'M'): ?>
                                    <span class="badge badge-info" style="font-size: 0.65rem;">M</span>
                                <?php elseif ($class['gender'] === 'K' || $class['gender'] === 'F'): ?>
                                    <span class="badge badge-accent" style="font-size: 0.65rem;">K</span>
                                <?php endif; ?>
                            </td>
                            <?php foreach ($licenseTypes as $lt): ?>
                                <td class="text-center">
                                    <?php if (isset($licenseMatrix[$class['id']][$lt['code']])): ?>
                                        <i data-lucide="check" style="width: 16px; height: 16px; color: var(--color-success);"></i>
                                    <?php else: ?>
                                        <span class="text-muted">-</span>
                                    <?php endif; ?>
                                </td>
                            <?php endforeach; ?>
                            <td class="text-center">
                                <input type="checkbox" name="is_locked[<?= $class['id'] ?>]" value="1"
                                    <?= isset($lockedClasses[$class['id']]) ? 'checked' : '' ?>>
                            </td>
                        </tr>
                        <?php endforeach; ?>
                    </tbody>
                </table>
            </div>

            <div class="admin-alert admin-alert-info mt-lg">
                <i data-lucide="info"></i>
                <div>
                    <strong>Låsta klasser</strong> kan inte väljas vid anmälan.
                    Licensmatrisen hanteras under <a href="/admin/license-class-matrix.php">Konfiguration &rarr; Licens-Klass Matris</a>.
                </div>
            </div>

            <div class="mt-lg">
                <button type="submit" class="btn-admin btn-admin-primary">
                    <i data-lucide="save"></i>
                    Spara klasslåsningar
                </button>
            </div>
        </form>
    </div>
</div>
<?php endif; ?>

<style>
.opacity-50 {
    opacity: 0.5;
}
</style>

<?php include __DIR__ . '/components/unified-layout-footer.php'; ?>
