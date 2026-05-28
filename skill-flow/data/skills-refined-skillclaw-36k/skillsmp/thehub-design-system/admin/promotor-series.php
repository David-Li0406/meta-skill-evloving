<?php
/**
 * Promotor Series Settings
 * Manage Swish settings and series registration for promotor's series
 * Shows events in each series below
 */
require_once __DIR__ . '/../config.php';
require_admin();

// Only for promotors
if (!hasRole('promotor')) {
    redirect('/admin/dashboard');
}

$db = getDB();
$currentAdmin = getCurrentAdmin();
$userId = $currentAdmin['id'];

$message = '';
$messageType = 'info';

// Handle form submission
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    checkCsrf();
    $action = $_POST['action'] ?? '';

    if ($action === 'save_series_settings') {
        $seriesId = intval($_POST['series_id'] ?? 0);
        $swishNumber = trim($_POST['swish_number'] ?? '');
        $swishName = trim($_POST['swish_name'] ?? '');
        $allowSeriesRegistration = isset($_POST['allow_series_registration']) ? 1 : 0;
        $seriesDiscountPercent = floatval($_POST['series_discount_percent'] ?? 15);

        // Verify promotor owns this series
        $owns = $db->getRow("SELECT 1 FROM promotor_series WHERE user_id = ? AND series_id = ?", [$userId, $seriesId]);

        if ($owns && $seriesId) {
            // Update series table for registration settings
            $db->update('series', [
                'allow_series_registration' => $allowSeriesRegistration,
                'series_discount_percent' => $seriesDiscountPercent
            ], 'id = ?', [$seriesId]);

            // Check if payment_configs entry exists for this series
            $existing = $db->getRow("SELECT id FROM payment_configs WHERE series_id = ?", [$seriesId]);

            if ($existing) {
                $db->update('payment_configs', [
                    'swish_enabled' => 1,
                    'swish_number' => $swishNumber ?: null,
                    'swish_name' => $swishName ?: null
                ], 'id = ?', [$existing['id']]);
            } else {
                $db->insert('payment_configs', [
                    'series_id' => $seriesId,
                    'swish_enabled' => 1,
                    'swish_number' => $swishNumber ?: null,
                    'swish_name' => $swishName ?: null
                ]);
            }

            $message = 'Inställningar sparade!';
            $messageType = 'success';
        } else {
            $message = 'Du har inte behörighet att ändra denna serie.';
            $messageType = 'danger';
        }
    }
}

// Get promotor's series with their events and registration settings
$series = $db->getAll("
    SELECT DISTINCT s.id, s.name, s.year, s.logo,
           s.allow_series_registration, s.series_discount_percent,
           s.default_pricing_template_id,
           pc.swish_number, pc.swish_name, pc.swish_enabled,
           pt.name as template_name, pt.early_bird_percent, pt.early_bird_days_before,
           CASE WHEN ps.user_id IS NOT NULL THEN 1 ELSE 0 END as can_edit_swish
    FROM series s
    LEFT JOIN promotor_series ps ON ps.series_id = s.id AND ps.user_id = ?
    LEFT JOIN payment_configs pc ON pc.series_id = s.id
    LEFT JOIN pricing_templates pt ON pt.id = s.default_pricing_template_id
    LEFT JOIN events e ON e.series_id = s.id
    LEFT JOIN promotor_events pe ON pe.event_id = e.id AND pe.user_id = ?
    WHERE ps.user_id IS NOT NULL OR pe.user_id IS NOT NULL
    ORDER BY s.year DESC, s.name
", [$userId, $userId]);

// Get events for each series with pricing info
$seriesEvents = [];
foreach ($series as $s) {
    if ($s['can_edit_swish']) {
        // Has series-level access - show all events in series with pricing
        $seriesEvents[$s['id']] = $db->getAll("
            SELECT e.id, e.name, e.date, e.location, e.pricing_template_id,
                   pt.name as template_name, pt.early_bird_percent, pt.early_bird_days_before,
                   DATE_SUB(e.date, INTERVAL COALESCE(pt.early_bird_days_before, 21) DAY) as early_bird_ends
            FROM events e
            LEFT JOIN pricing_templates pt ON pt.id = e.pricing_template_id
            WHERE e.series_id = ?
            ORDER BY e.date ASC
        ", [$s['id']]);
    } else {
        // Only event-level access - show only assigned events
        $seriesEvents[$s['id']] = $db->getAll("
            SELECT e.id, e.name, e.date, e.location, e.pricing_template_id,
                   pt.name as template_name, pt.early_bird_percent, pt.early_bird_days_before,
                   DATE_SUB(e.date, INTERVAL COALESCE(pt.early_bird_days_before, 21) DAY) as early_bird_ends
            FROM events e
            JOIN promotor_events pe ON pe.event_id = e.id AND pe.user_id = ?
            LEFT JOIN pricing_templates pt ON pt.id = e.pricing_template_id
            WHERE e.series_id = ?
            ORDER BY e.date ASC
        ", [$userId, $s['id']]);
    }
}

$page_title = 'Serie-inställningar';
include __DIR__ . '/components/unified-layout.php';
?>

<?php if ($message): ?>
<div class="alert alert-<?= h($messageType) ?> mb-lg">
    <?= h($message) ?>
</div>
<?php endif; ?>

<?php if (empty($series)): ?>
<div class="card">
    <div class="card-body">
        <p class="text-muted">Du har inga tilldelade serier.</p>
    </div>
</div>
<?php else: ?>

<?php foreach ($series as $s): ?>
<div class="card mb-lg">
    <div class="card-header">
        <h2>
            <?php if ($s['logo']): ?>
            <img src="<?= h($s['logo']) ?>" alt="" style="height: 24px; margin-right: var(--space-sm); vertical-align: middle;">
            <?php endif; ?>
            <?= h($s['name']) ?>
            <?php if ($s['year']): ?>
            <span style="font-weight: 400; color: var(--color-text-secondary);"><?= h($s['year']) ?></span>
            <?php endif; ?>
        </h2>
    </div>
    <div class="card-body">
        <?php if ($s['can_edit_swish']): ?>
        <form method="POST" class="mb-lg">
            <?= csrf_field() ?>
            <input type="hidden" name="action" value="save_series_settings">
            <input type="hidden" name="series_id" value="<?= $s['id'] ?>">

            <!-- Serieanmälan section -->
            <div class="settings-section mb-lg" style="background: var(--color-bg-sunken); padding: var(--space-md); border-radius: var(--radius-md);">
                <h3 class="mb-md" style="font-size: 1rem; color: var(--color-text-secondary);">
                    <i data-lucide="ticket" style="width: 18px; height: 18px; vertical-align: middle;"></i>
                    Serieanmälan
                </h3>

                <div class="grid grid-2 gap-md">
                    <div class="form-group" style="margin-bottom: 0;">
                        <label style="display: flex; align-items: center; gap: var(--space-sm); cursor: pointer;">
                            <input type="checkbox" name="allow_series_registration" value="1"
                                   <?= ($s['allow_series_registration'] ?? 0) ? 'checked' : '' ?>
                                   style="width: 18px; height: 18px;">
                            <span class="form-label" style="margin: 0;">Aktivera serieanmälan</span>
                        </label>
                        <small class="text-muted" style="display: block; margin-top: var(--space-xs);">
                            Tillåter åkare att anmäla sig till alla tävlingar i serien
                        </small>
                    </div>
                    <div class="form-group" style="margin-bottom: 0;">
                        <label class="form-label">Rabattsats (%)</label>
                        <input type="number" name="series_discount_percent" class="form-input"
                               value="<?= h($s['series_discount_percent'] ?? 15) ?>"
                               min="0" max="50" step="1"
                               placeholder="15" style="max-width: 100px;">
                        <small class="text-muted" style="display: block; margin-top: var(--space-xs);">
                            Rabatt vid serieanmälan
                        </small>
                    </div>
                </div>
            </div>

            <!-- Swish Settings -->
            <h3 class="mb-md" style="font-size: 1rem; color: var(--color-text-secondary);">
                <i data-lucide="smartphone" style="width: 18px; height: 18px; vertical-align: middle;"></i>
                Swish-inställningar
            </h3>

            <div class="grid grid-2 gap-md">
                <div class="form-group">
                    <label class="form-label">Swish-nummer</label>
                    <input type="text" name="swish_number" class="form-input"
                           value="<?= h($s['swish_number'] ?? '') ?>"
                           placeholder="073-123 45 67">
                </div>
                <div class="form-group">
                    <label class="form-label">Mottagare</label>
                    <input type="text" name="swish_name" class="form-input"
                           value="<?= h($s['swish_name'] ?? '') ?>"
                           placeholder="Namn på mottagaren">
                </div>
            </div>

            <button type="submit" class="btn btn-primary">
                <i data-lucide="save"></i>
                Spara inställningar
            </button>

            <?php if ($s['swish_number']): ?>
            <span class="badge badge-success ml-md">Swish aktivt</span>
            <?php endif; ?>
            <?php if ($s['allow_series_registration']): ?>
            <span class="badge badge-info ml-md">Serieanmälan aktiv (<?= h($s['series_discount_percent'] ?? 15) ?>% rabatt)</span>
            <?php endif; ?>
        </form>
        <?php else: ?>
        <div class="mb-lg">
            <p class="text-muted" style="font-size: 0.9rem;">
                <i data-lucide="info" style="width: 16px; height: 16px; vertical-align: middle;"></i>
                Du har tillgång via tilldelade tävlingar. Kontakta admin för att få serie-behörighet om du behöver ändra inställningar.
            </p>
            <?php if ($s['swish_number']): ?>
            <p style="margin-top: var(--space-sm);">
                <strong>Swish:</strong> <?= h($s['swish_number']) ?>
                <?php if ($s['swish_name']): ?> (<?= h($s['swish_name']) ?>)<?php endif; ?>
            </p>
            <?php endif; ?>
        </div>
        <?php endif; ?>

        <!-- Prismall info -->
        <?php if ($s['template_name']): ?>
        <div class="mb-lg" style="background: var(--color-bg-sunken); padding: var(--space-md); border-radius: var(--radius-md);">
            <h3 class="mb-sm" style="font-size: 1rem; color: var(--color-text-secondary);">
                <i data-lucide="tag" style="width: 18px; height: 18px; vertical-align: middle;"></i>
                Prismall: <?= h($s['template_name']) ?>
            </h3>
            <p class="text-muted" style="font-size: 0.875rem; margin: 0;">
                Early bird: <?= h($s['early_bird_percent'] ?? 15) ?>% rabatt (<?= h($s['early_bird_days_before'] ?? 21) ?> dagar före tävling)
            </p>
        </div>
        <?php endif; ?>

        <!-- Events in this series with pricing info -->
        <?php if (!empty($seriesEvents[$s['id']])): ?>
        <h3 class="mb-md" style="font-size: 1rem; color: var(--color-text-secondary);">
            <i data-lucide="calendar" style="width: 18px; height: 18px; vertical-align: middle;"></i>
            Tävlingar i serien (<?= count($seriesEvents[$s['id']]) ?>)
        </h3>
        <div class="table-responsive">
            <table class="table">
                <thead>
                    <tr>
                        <th>Tävling</th>
                        <th>Datum</th>
                        <th>Plats</th>
                        <th>Early bird slutar</th>
                    </tr>
                </thead>
                <tbody>
                    <?php foreach ($seriesEvents[$s['id']] as $event): ?>
                    <?php
                        $eventDate = strtotime($event['date']);
                        $earlyBirdEnds = $event['early_bird_ends'] ? strtotime($event['early_bird_ends']) : null;
                        $isPast = $eventDate < time();
                        $earlyBirdActive = $earlyBirdEnds && $earlyBirdEnds > time();
                    ?>
                    <tr style="<?= $isPast ? 'opacity: 0.5;' : '' ?>">
                        <td>
                            <a href="/admin/event-edit.php?id=<?= $event['id'] ?>" style="text-decoration: none; color: inherit;">
                                <?= h($event['name']) ?>
                            </a>
                            <?php if ($event['template_name']): ?>
                            <br><small class="text-muted"><?= h($event['template_name']) ?></small>
                            <?php endif; ?>
                        </td>
                        <td>
                            <?= date('j M Y', $eventDate) ?>
                            <?php if ($isPast): ?>
                            <span class="badge badge-secondary" style="font-size: 0.65rem;">Avslutad</span>
                            <?php endif; ?>
                        </td>
                        <td><?= h($event['location'] ?? '-') ?></td>
                        <td>
                            <?php if ($earlyBirdEnds): ?>
                                <?php if ($earlyBirdActive): ?>
                                <span style="color: var(--color-success);">
                                    <?= date('j M', $earlyBirdEnds) ?>
                                    <small>(<?= ceil(($earlyBirdEnds - time()) / 86400) ?> dagar kvar)</small>
                                </span>
                                <?php else: ?>
                                <span class="text-muted"><?= date('j M', $earlyBirdEnds) ?></span>
                                <?php endif; ?>
                            <?php else: ?>
                            <span class="text-muted">-</span>
                            <?php endif; ?>
                        </td>
                    </tr>
                    <?php endforeach; ?>
                </tbody>
            </table>
        </div>
        <?php else: ?>
        <p class="text-muted">Inga tävlingar i denna serie ännu.</p>
        <?php endif; ?>
    </div>
</div>
<?php endforeach; ?>

<?php endif; ?>

<style>
.grid-2 {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
}
@media (max-width: 767px) {
    .grid-2 {
        grid-template-columns: 1fr;
    }
}
.gap-md {
    gap: var(--space-md);
}
.ml-md {
    margin-left: var(--space-md);
}
</style>

<?php include __DIR__ . '/components/unified-layout-footer.php'; ?>
