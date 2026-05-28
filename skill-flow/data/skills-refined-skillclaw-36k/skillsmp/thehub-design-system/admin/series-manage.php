<?php
/**
 * Admin Series Manage - Unified Series Management with Tabs
 * All series configuration in one place: Info, Events, Registration, Payment, Results
 */
require_once __DIR__ . '/../config.php';
require_once __DIR__ . '/../includes/series-points.php';

// Require login (admin OR promotor)
if (!isLoggedIn()) {
    header('Location: /login?redirect=' . urlencode($_SERVER['REQUEST_URI']));
    exit;
}

$db = getDB();

// Get series ID from URL
$id = 0;
if (isset($_GET['id'])) {
    $id = intval($_GET['id']);
} else {
    $uri = $_SERVER['REQUEST_URI'];
    if (preg_match('#/admin/series/manage/(\d+)#', $uri, $matches)) {
        $id = intval($matches[1]);
    }
}

if ($id <= 0) {
    $_SESSION['flash_message'] = 'Ogiltigt serie-ID';
    $_SESSION['flash_type'] = 'error';
    header('Location: /admin/series');
    exit;
}

// Check access
if (!canAccessSeries($id)) {
    $_SESSION['flash_message'] = 'Du har inte behörighet att hantera denna serie';
    $_SESSION['flash_type'] = 'error';
    header('Location: /admin/series');
    exit;
}

// Fetch series
$series = $db->getRow("SELECT * FROM series WHERE id = ?", [$id]);
if (!$series) {
    $_SESSION['flash_message'] = 'Serie hittades inte';
    $_SESSION['flash_type'] = 'error';
    header('Location: /admin/series');
    exit;
}

// Get active tab
$activeTab = $_GET['tab'] ?? 'info';
$validTabs = ['info', 'events', 'registration', 'payment', 'results'];
if (!in_array($activeTab, $validTabs)) {
    $activeTab = 'info';
}

// Initialize message
$message = '';
$messageType = 'info';

// Check for flash message
if (isset($_SESSION['flash_message'])) {
    $message = $_SESSION['flash_message'];
    $messageType = $_SESSION['flash_type'] ?? 'info';
    unset($_SESSION['flash_message'], $_SESSION['flash_type']);
}

// ============================================================
// HANDLE POST ACTIONS
// ============================================================
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    checkCsrf();
    $action = $_POST['action'] ?? '';

    // INFO TAB ACTIONS
    if ($action === 'save_info') {
        $name = trim($_POST['name'] ?? '');
        $year = !empty($_POST['year']) ? intval($_POST['year']) : null;

        if (empty($name)) {
            $message = 'Namn är obligatoriskt';
            $messageType = 'error';
        } elseif (empty($year)) {
            $message = 'År är obligatoriskt';
            $messageType = 'error';
        } else {
            $seriesData = [
                'name' => $name,
                'year' => $year,
                'type' => trim($_POST['type'] ?? ''),
                'format' => $_POST['format'] ?? 'Championship',
                'status' => $_POST['status'] ?? 'planning',
                'description' => trim($_POST['description'] ?? ''),
                'organizer' => trim($_POST['organizer'] ?? ''),
            ];

            // Brand ID if exists
            try {
                $columns = $db->getAll("SHOW COLUMNS FROM series LIKE 'brand_id'");
                if (!empty($columns) && isset($_POST['brand_id'])) {
                    $seriesData['brand_id'] = !empty($_POST['brand_id']) ? intval($_POST['brand_id']) : null;
                }
            } catch (Exception $e) {}

            $db->update('series', $seriesData, 'id = ?', [$id]);
            $series = $db->getRow("SELECT * FROM series WHERE id = ?", [$id]);
            $message = 'Serie uppdaterad!';
            $messageType = 'success';
        }
    }

    // EVENTS TAB ACTIONS
    elseif ($action === 'add_event') {
        $eventId = intval($_POST['event_id']);
        $templateId = !empty($_POST['template_id']) ? intval($_POST['template_id']) : null;

        $existing = $db->getRow("SELECT id FROM series_events WHERE series_id = ? AND event_id = ?", [$id, $eventId]);
        if ($existing) {
            $message = 'Detta event finns redan i serien';
            $messageType = 'error';
        } else {
            $maxOrder = $db->getRow("SELECT MAX(sort_order) as max_order FROM series_events WHERE series_id = ?", [$id]);
            $sortOrder = ($maxOrder['max_order'] ?? 0) + 1;

            $db->insert('series_events', [
                'series_id' => $id,
                'event_id' => $eventId,
                'template_id' => $templateId,
                'sort_order' => $sortOrder
            ]);

            if ($templateId) {
                $stats = recalculateSeriesEventPoints($db, $id, $eventId);
                $message = "Event tillagt! {$stats['inserted']} seriepoäng beräknade.";
            } else {
                $message = 'Event tillagt i serien!';
            }
            $messageType = 'success';
        }
        $activeTab = 'events';
    }

    elseif ($action === 'remove_event') {
        $seriesEventId = intval($_POST['series_event_id']);
        $db->delete('series_events', 'id = ? AND series_id = ?', [$seriesEventId, $id]);
        $message = 'Event borttaget från serien';
        $messageType = 'success';
        $activeTab = 'events';
    }

    elseif ($action === 'update_template') {
        $seriesEventId = intval($_POST['series_event_id']);
        $templateId = !empty($_POST['template_id']) ? intval($_POST['template_id']) : null;

        $seriesEvent = $db->getRow("SELECT event_id FROM series_events WHERE id = ? AND series_id = ?", [$seriesEventId, $id]);
        if ($seriesEvent) {
            $db->update('series_events', ['template_id' => $templateId], 'id = ? AND series_id = ?', [$seriesEventId, $id]);
            $stats = recalculateSeriesEventPoints($db, $id, $seriesEvent['event_id']);
            $message = "Poängmall uppdaterad! {$stats['inserted']} poäng omräknade.";
            $messageType = 'success';
        }
        $activeTab = 'events';
    }

    // REGISTRATION TAB ACTIONS
    elseif ($action === 'save_registration') {
        $registrationEnabled = isset($_POST['registration_enabled']) ? 1 : 0;
        $pricingTemplateId = !empty($_POST['pricing_template_id']) ? intval($_POST['pricing_template_id']) : null;

        $db->update('series', [
            'registration_enabled' => $registrationEnabled,
            'pricing_template_id' => $pricingTemplateId
        ], 'id = ?', [$id]);

        $series = $db->getRow("SELECT * FROM series WHERE id = ?", [$id]);
        $message = 'Anmälningsinställningar sparade!';
        $messageType = 'success';
        $activeTab = 'registration';
    }

    elseif ($action === 'save_event_times') {
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

        $message = "Sparade anmälningstider för $saved events";
        $messageType = 'success';
        $activeTab = 'registration';
    }

    // PAYMENT TAB ACTIONS
    elseif ($action === 'save_payment') {
        $paymentRecipientId = !empty($_POST['payment_recipient_id']) ? intval($_POST['payment_recipient_id']) : null;
        $gravityIdDiscount = floatval($_POST['gravity_id_discount'] ?? 0);

        $updateData = ['gravity_id_discount' => $gravityIdDiscount];

        // Check if payment_recipient_id column exists
        try {
            $columns = $db->getAll("SHOW COLUMNS FROM series LIKE 'payment_recipient_id'");
            if (!empty($columns)) {
                $updateData['payment_recipient_id'] = $paymentRecipientId;
            }
        } catch (Exception $e) {}

        // Check for legacy swish columns
        try {
            $columns = $db->getAll("SHOW COLUMNS FROM series LIKE 'swish_number'");
            if (!empty($columns)) {
                $updateData['swish_number'] = trim($_POST['swish_number'] ?? '') ?: null;
                $updateData['swish_name'] = trim($_POST['swish_name'] ?? '') ?: null;
            }
        } catch (Exception $e) {}

        $db->update('series', $updateData, 'id = ?', [$id]);
        $series = $db->getRow("SELECT * FROM series WHERE id = ?", [$id]);
        $message = 'Betalningsinställningar sparade!';
        $messageType = 'success';
        $activeTab = 'payment';
    }

    // RESULTS TAB ACTIONS
    elseif ($action === 'recalculate_all') {
        $totalStats = recalculateAllSeriesPoints($db, $id);
        $totalChanged = $totalStats['inserted'] + $totalStats['updated'];
        $message = "Alla poäng omräknade! {$totalStats['events']} events, {$totalChanged} resultat.";
        $messageType = 'success';
        $activeTab = 'results';
    }

    elseif ($action === 'update_count_best') {
        $countBest = $_POST['count_best_results'];
        $countBestValue = ($countBest === '' || $countBest === 'null') ? null : intval($countBest);

        $db->update('series', ['count_best_results' => $countBestValue], 'id = ?', [$id]);
        $series = $db->getRow("SELECT * FROM series WHERE id = ?", [$id]);
        $message = $countBestValue === null ? 'Alla resultat räknas nu' : "Räknar nu de {$countBestValue} bästa resultaten";
        $messageType = 'success';
        $activeTab = 'results';
    }
}

// ============================================================
// FETCH DATA FOR TABS
// ============================================================

// Get brands for dropdown
$brands = [];
try {
    $tables = $db->getAll("SHOW TABLES LIKE 'series_brands'");
    if (!empty($tables)) {
        $brands = $db->getAll("SELECT id, name FROM series_brands WHERE active = 1 ORDER BY display_order ASC, name ASC");
    }
} catch (Exception $e) {}

// Get events in this series
$seriesEvents = $db->getAll("
    SELECT se.*, e.name as event_name, e.date as event_date, e.location, e.discipline,
           e.series_id as event_series_id, ps.name as template_name,
           e.registration_opens, e.registration_deadline
    FROM series_events se
    JOIN events e ON se.event_id = e.id
    LEFT JOIN point_scales ps ON se.template_id = ps.id
    WHERE se.series_id = ?
    ORDER BY e.date ASC
", [$id]);

// Get events not in series (for adding)
$eventsNotInSeries = $db->getAll("
    SELECT e.id, e.name, e.date, e.location, YEAR(e.date) as event_year
    FROM events e
    WHERE e.id NOT IN (SELECT event_id FROM series_events WHERE series_id = ?)
    AND e.active = 1
    ORDER BY e.date DESC
", [$id]);

// Separate by year match
$seriesYear = $series['year'] ?? null;
$matchingYearEvents = [];
$otherYearEvents = [];
foreach ($eventsNotInSeries as $ev) {
    if ($seriesYear && $ev['event_year'] == $seriesYear) {
        $matchingYearEvents[] = $ev;
    } else {
        $otherYearEvents[] = $ev;
    }
}

// Get point scales (templates)
$pointScales = $db->getAll("SELECT id, name FROM point_scales WHERE active = 1 ORDER BY name");

// Get pricing templates
$pricingTemplates = [];
try {
    $pricingTemplates = $db->getAll("SELECT id, name, is_default FROM pricing_templates ORDER BY is_default DESC, name ASC");
} catch (Exception $e) {}

// Get payment recipients
$paymentRecipients = [];
try {
    $tables = $db->getAll("SHOW TABLES LIKE 'payment_recipients'");
    if (!empty($tables)) {
        $paymentRecipients = $db->getAll("SELECT id, name, swish_number, swish_name FROM payment_recipients WHERE is_active = 1 ORDER BY name ASC");
    }
} catch (Exception $e) {}

// Check legacy swish columns
$hasLegacySwish = false;
try {
    $columns = $db->getAll("SHOW COLUMNS FROM series LIKE 'swish_number'");
    $hasLegacySwish = !empty($columns);
} catch (Exception $e) {}

// Count stats
$eventsCount = count($seriesEvents);
$eventsWithResults = 0;
foreach ($seriesEvents as $se) {
    $hasResults = $db->getRow("SELECT COUNT(*) as cnt FROM results WHERE event_id = ? AND status = 'finished'", [$se['event_id']]);
    if (($hasResults['cnt'] ?? 0) > 0) {
        $eventsWithResults++;
    }
}

// Get unique participants
$uniqueParticipants = $db->getRow("
    SELECT COUNT(DISTINCT r.cyclist_id) as cnt
    FROM results r
    JOIN series_events se ON r.event_id = se.event_id
    WHERE se.series_id = ? AND r.status = 'finished'
", [$id])['cnt'] ?? 0;

// ============================================================
// PAGE CONFIG
// ============================================================
$page_title = 'Hantera: ' . htmlspecialchars($series['name']);
$breadcrumbs = [
    ['label' => 'Serier', 'url' => '/admin/series'],
    ['label' => htmlspecialchars($series['name'])]
];
include __DIR__ . '/components/unified-layout.php';
?>

<style>
/* Series Manage Tabs */
.series-tabs {
    display: flex;
    gap: var(--space-xs);
    margin-bottom: var(--space-lg);
    border-bottom: 2px solid var(--color-border);
    padding-bottom: var(--space-xs);
    overflow-x: auto;
    -webkit-overflow-scrolling: touch;
}

.series-tab {
    display: flex;
    align-items: center;
    gap: var(--space-xs);
    padding: var(--space-sm) var(--space-md);
    border-radius: var(--radius-md) var(--radius-md) 0 0;
    text-decoration: none;
    color: var(--color-text-secondary);
    font-weight: 500;
    font-size: var(--text-sm);
    white-space: nowrap;
    transition: all 0.15s ease;
    border: 1px solid transparent;
    border-bottom: none;
}

.series-tab:hover {
    color: var(--color-accent);
    background: var(--color-bg-hover);
}

.series-tab.active {
    color: var(--color-accent);
    background: var(--color-bg-card);
    border-color: var(--color-border);
    margin-bottom: -2px;
    border-bottom: 2px solid var(--color-bg-card);
}

.series-tab svg {
    width: 16px;
    height: 16px;
}

.series-tab .badge {
    font-size: 10px;
    padding: 2px 6px;
}

/* Quick Stats */
.quick-stats {
    display: flex;
    gap: var(--space-md);
    margin-bottom: var(--space-lg);
    flex-wrap: wrap;
}

.quick-stat {
    display: flex;
    align-items: center;
    gap: var(--space-sm);
    padding: var(--space-sm) var(--space-md);
    background: var(--color-bg-card);
    border: 1px solid var(--color-border);
    border-radius: var(--radius-md);
}

.quick-stat-value {
    font-size: var(--text-xl);
    font-weight: 700;
    color: var(--color-accent);
}

.quick-stat-label {
    font-size: var(--text-sm);
    color: var(--color-text-secondary);
}

/* Tab content */
.tab-content {
    display: none;
}

.tab-content.active {
    display: block;
}

/* Event table */
.event-table {
    width: 100%;
}

.event-table th,
.event-table td {
    padding: var(--space-sm) var(--space-md);
    text-align: left;
    border-bottom: 1px solid var(--color-border);
}

.event-table th {
    font-weight: 600;
    color: var(--color-text-secondary);
    font-size: var(--text-sm);
    background: var(--color-bg-surface);
}

.template-select {
    min-width: 150px;
}

/* Registration times grid */
.reg-times-grid {
    display: grid;
    gap: var(--space-md);
}

.reg-time-row {
    display: grid;
    grid-template-columns: 2fr 1fr 1fr 1fr;
    gap: var(--space-md);
    align-items: center;
    padding: var(--space-md);
    background: var(--color-bg-surface);
    border-radius: var(--radius-md);
}

@media (max-width: 768px) {
    .reg-time-row {
        grid-template-columns: 1fr;
    }

    .series-tabs {
        gap: var(--space-2xs);
    }

    .series-tab {
        padding: var(--space-xs) var(--space-sm);
        font-size: var(--text-xs);
    }

    .series-tab svg {
        width: 14px;
        height: 14px;
    }
}

/* Info grid */
.info-grid {
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

<!-- Quick Stats -->
<div class="quick-stats">
    <div class="quick-stat">
        <div class="quick-stat-value"><?= $eventsCount ?></div>
        <div class="quick-stat-label">Events</div>
    </div>
    <div class="quick-stat">
        <div class="quick-stat-value"><?= $eventsWithResults ?>/<?= $eventsCount ?></div>
        <div class="quick-stat-label">Med resultat</div>
    </div>
    <div class="quick-stat">
        <div class="quick-stat-value"><?= number_format($uniqueParticipants) ?></div>
        <div class="quick-stat-label">Deltagare</div>
    </div>
    <div class="quick-stat">
        <span class="badge badge-<?= $series['status'] === 'active' ? 'success' : ($series['status'] === 'completed' ? 'info' : 'secondary') ?>">
            <?= ucfirst($series['status'] ?? 'planning') ?>
        </span>
    </div>
</div>

<!-- Tabs Navigation -->
<nav class="series-tabs">
    <a href="?id=<?= $id ?>&tab=info" class="series-tab <?= $activeTab === 'info' ? 'active' : '' ?>">
        <i data-lucide="settings"></i>
        Info
    </a>
    <a href="?id=<?= $id ?>&tab=events" class="series-tab <?= $activeTab === 'events' ? 'active' : '' ?>">
        <i data-lucide="calendar"></i>
        Events
        <span class="badge badge-secondary"><?= $eventsCount ?></span>
    </a>
    <a href="?id=<?= $id ?>&tab=registration" class="series-tab <?= $activeTab === 'registration' ? 'active' : '' ?>">
        <i data-lucide="clipboard-list"></i>
        Anmälan
        <?php if ($series['registration_enabled'] ?? 0): ?>
            <span class="badge badge-success">ON</span>
        <?php endif; ?>
    </a>
    <a href="?id=<?= $id ?>&tab=payment" class="series-tab <?= $activeTab === 'payment' ? 'active' : '' ?>">
        <i data-lucide="credit-card"></i>
        Betalning
    </a>
    <a href="?id=<?= $id ?>&tab=results" class="series-tab <?= $activeTab === 'results' ? 'active' : '' ?>">
        <i data-lucide="trophy"></i>
        Resultat
    </a>
</nav>

<!-- ============================================================ -->
<!-- INFO TAB -->
<!-- ============================================================ -->
<div class="tab-content <?= $activeTab === 'info' ? 'active' : '' ?>" id="tab-info">
    <form method="POST">
        <?= csrf_field() ?>
        <input type="hidden" name="action" value="save_info">

        <div class="admin-card">
            <div class="admin-card-header">
                <h2><i data-lucide="settings"></i> Grundinformation</h2>
            </div>
            <div class="admin-card-body">
                <?php if (!empty($brands)): ?>
                <div class="admin-form-group mb-md">
                    <label class="admin-form-label">Huvudserie (Varumärke)</label>
                    <select name="brand_id" class="admin-form-select">
                        <option value="">-- Ingen --</option>
                        <?php foreach ($brands as $brand): ?>
                        <option value="<?= $brand['id'] ?>" <?= ($series['brand_id'] ?? '') == $brand['id'] ? 'selected' : '' ?>>
                            <?= htmlspecialchars($brand['name']) ?>
                        </option>
                        <?php endforeach; ?>
                    </select>
                </div>
                <?php endif; ?>

                <div class="info-grid">
                    <div class="admin-form-group">
                        <label class="admin-form-label">Serienamn *</label>
                        <input type="text" name="name" class="admin-form-input" required
                               value="<?= htmlspecialchars($series['name'] ?? '') ?>">
                    </div>
                    <div class="admin-form-group">
                        <label class="admin-form-label">År *</label>
                        <input type="number" name="year" class="admin-form-input" required
                               value="<?= htmlspecialchars($series['year'] ?? date('Y')) ?>"
                               min="2000" max="2100">
                    </div>
                    <div class="admin-form-group">
                        <label class="admin-form-label">Typ</label>
                        <input type="text" name="type" class="admin-form-input"
                               value="<?= htmlspecialchars($series['type'] ?? '') ?>"
                               placeholder="Enduro, DH, XC...">
                    </div>
                    <div class="admin-form-group">
                        <label class="admin-form-label">Status</label>
                        <select name="status" class="admin-form-select">
                            <option value="planning" <?= ($series['status'] ?? '') === 'planning' ? 'selected' : '' ?>>Planering</option>
                            <option value="active" <?= ($series['status'] ?? '') === 'active' ? 'selected' : '' ?>>Aktiv</option>
                            <option value="completed" <?= ($series['status'] ?? '') === 'completed' ? 'selected' : '' ?>>Avslutad</option>
                            <option value="cancelled" <?= ($series['status'] ?? '') === 'cancelled' ? 'selected' : '' ?>>Inställd</option>
                        </select>
                    </div>
                </div>

                <div class="admin-form-group mt-md">
                    <label class="admin-form-label">Arrangör</label>
                    <input type="text" name="organizer" class="admin-form-input"
                           value="<?= htmlspecialchars($series['organizer'] ?? '') ?>">
                </div>

                <div class="admin-form-group">
                    <label class="admin-form-label">Beskrivning</label>
                    <textarea name="description" class="admin-form-input" rows="3"><?= htmlspecialchars($series['description'] ?? '') ?></textarea>
                </div>

                <div class="mt-lg">
                    <button type="submit" class="btn-admin btn-admin-primary">
                        <i data-lucide="save"></i> Spara
                    </button>
                </div>
            </div>
        </div>
    </form>
</div>

<!-- ============================================================ -->
<!-- EVENTS TAB -->
<!-- ============================================================ -->
<div class="tab-content <?= $activeTab === 'events' ? 'active' : '' ?>" id="tab-events">
    <div class="grid grid-cols-1 gs-lg-grid-cols-3 gap-lg">
        <!-- Add Event -->
        <div>
            <div class="admin-card">
                <div class="admin-card-header">
                    <h2><i data-lucide="plus"></i> Lägg till Event</h2>
                </div>
                <div class="admin-card-body">
                    <?php if (empty($eventsNotInSeries)): ?>
                        <p class="text-secondary">Alla events är redan tillagda.</p>
                    <?php else: ?>
                    <form method="POST">
                        <?= csrf_field() ?>
                        <input type="hidden" name="action" value="add_event">

                        <div class="admin-form-group">
                            <label class="admin-form-label">Välj event</label>
                            <select name="event_id" class="admin-form-select" required>
                                <option value="">-- Välj --</option>
                                <?php if (!empty($matchingYearEvents)): ?>
                                <optgroup label="Matchar serieåret (<?= $seriesYear ?>)">
                                    <?php foreach ($matchingYearEvents as $ev): ?>
                                    <option value="<?= $ev['id'] ?>">
                                        <?= htmlspecialchars($ev['name']) ?>
                                        <?php if ($ev['date']): ?>(<?= date('Y-m-d', strtotime($ev['date'])) ?>)<?php endif; ?>
                                    </option>
                                    <?php endforeach; ?>
                                </optgroup>
                                <?php endif; ?>
                                <?php if (!empty($otherYearEvents)): ?>
                                <optgroup label="Andra år">
                                    <?php foreach ($otherYearEvents as $ev): ?>
                                    <option value="<?= $ev['id'] ?>">
                                        <?= htmlspecialchars($ev['name']) ?>
                                        <?php if ($ev['date']): ?>(<?= date('Y-m-d', strtotime($ev['date'])) ?>)<?php endif; ?>
                                    </option>
                                    <?php endforeach; ?>
                                </optgroup>
                                <?php endif; ?>
                            </select>
                        </div>

                        <div class="admin-form-group">
                            <label class="admin-form-label">Poängmall (valfritt)</label>
                            <select name="template_id" class="admin-form-select">
                                <option value="">-- Ingen --</option>
                                <?php foreach ($pointScales as $scale): ?>
                                <option value="<?= $scale['id'] ?>"><?= htmlspecialchars($scale['name']) ?></option>
                                <?php endforeach; ?>
                            </select>
                        </div>

                        <button type="submit" class="btn-admin btn-admin-primary w-full">
                            <i data-lucide="plus"></i> Lägg till
                        </button>
                    </form>
                    <?php endif; ?>
                </div>
            </div>
        </div>

        <!-- Events List -->
        <div class="gs-lg-col-span-2">
            <div class="admin-card">
                <div class="admin-card-header">
                    <h2><i data-lucide="list"></i> Events i serien (<?= $eventsCount ?>)</h2>
                </div>
                <div class="admin-card-body" style="padding: 0;">
                    <?php if (empty($seriesEvents)): ?>
                        <p class="text-secondary p-lg">Inga events tillagda ännu.</p>
                    <?php else: ?>
                    <div class="table-responsive">
                        <table class="event-table">
                            <thead>
                                <tr>
                                    <th>#</th>
                                    <th>Event</th>
                                    <th>Datum</th>
                                    <th>Poängmall</th>
                                    <th></th>
                                </tr>
                            </thead>
                            <tbody>
                                <?php $num = 1; foreach ($seriesEvents as $se): ?>
                                <tr>
                                    <td><span class="badge badge-primary"><?= $num++ ?></span></td>
                                    <td>
                                        <strong><?= htmlspecialchars($se['event_name']) ?></strong>
                                        <?php if ($se['location']): ?>
                                        <br><small class="text-secondary"><?= htmlspecialchars($se['location']) ?></small>
                                        <?php endif; ?>
                                    </td>
                                    <td><?= $se['event_date'] ? date('Y-m-d', strtotime($se['event_date'])) : '-' ?></td>
                                    <td>
                                        <form method="POST" class="flex gap-xs">
                                            <?= csrf_field() ?>
                                            <input type="hidden" name="action" value="update_template">
                                            <input type="hidden" name="series_event_id" value="<?= $se['id'] ?>">
                                            <select name="template_id" class="admin-form-select template-select">
                                                <option value="">-- Ingen --</option>
                                                <?php foreach ($pointScales as $scale): ?>
                                                <option value="<?= $scale['id'] ?>" <?= $se['template_id'] == $scale['id'] ? 'selected' : '' ?>>
                                                    <?= htmlspecialchars($scale['name']) ?>
                                                </option>
                                                <?php endforeach; ?>
                                            </select>
                                            <button type="submit" class="btn-admin btn-admin-sm btn-admin-secondary" title="Spara">
                                                <i data-lucide="check"></i>
                                            </button>
                                        </form>
                                    </td>
                                    <td>
                                        <form method="POST" onsubmit="return confirm('Ta bort event från serien?');">
                                            <?= csrf_field() ?>
                                            <input type="hidden" name="action" value="remove_event">
                                            <input type="hidden" name="series_event_id" value="<?= $se['id'] ?>">
                                            <button type="submit" class="btn-admin btn-admin-sm btn-admin-danger">
                                                <i data-lucide="trash-2"></i>
                                            </button>
                                        </form>
                                    </td>
                                </tr>
                                <?php endforeach; ?>
                            </tbody>
                        </table>
                    </div>
                    <?php endif; ?>
                </div>
            </div>
        </div>
    </div>
</div>

<!-- ============================================================ -->
<!-- REGISTRATION TAB -->
<!-- ============================================================ -->
<div class="tab-content <?= $activeTab === 'registration' ? 'active' : '' ?>" id="tab-registration">
    <!-- Registration Settings -->
    <div class="admin-card mb-lg">
        <div class="admin-card-header">
            <h2><i data-lucide="settings"></i> Anmälningsinställningar</h2>
        </div>
        <div class="admin-card-body">
            <form method="POST">
                <?= csrf_field() ?>
                <input type="hidden" name="action" value="save_registration">

                <div class="info-grid">
                    <div class="admin-form-group">
                        <label class="admin-form-label flex items-center gap-sm">
                            <input type="checkbox" name="registration_enabled" value="1"
                                   <?= ($series['registration_enabled'] ?? 0) ? 'checked' : '' ?>>
                            Anmälan aktiverad
                        </label>
                        <small class="text-secondary">Tillåt anmälan till events i serien</small>
                    </div>

                    <div class="admin-form-group">
                        <label class="admin-form-label">Prismall</label>
                        <select name="pricing_template_id" class="admin-form-select">
                            <option value="">-- Välj --</option>
                            <?php foreach ($pricingTemplates as $pt): ?>
                            <option value="<?= $pt['id'] ?>" <?= ($series['pricing_template_id'] ?? '') == $pt['id'] ? 'selected' : '' ?>>
                                <?= htmlspecialchars($pt['name']) ?> <?= $pt['is_default'] ? '(Standard)' : '' ?>
                            </option>
                            <?php endforeach; ?>
                        </select>
                        <small class="text-secondary">
                            <a href="/admin/pricing-templates" class="text-accent">Hantera prismallar</a>
                        </small>
                    </div>
                </div>

                <div class="mt-md">
                    <button type="submit" class="btn-admin btn-admin-primary">
                        <i data-lucide="save"></i> Spara
                    </button>
                </div>
            </form>
        </div>
    </div>

    <!-- Event Times -->
    <?php if (!empty($seriesEvents)): ?>
    <div class="admin-card">
        <div class="admin-card-header">
            <h2><i data-lucide="clock"></i> Anmälningstider per event</h2>
        </div>
        <div class="admin-card-body">
            <form method="POST">
                <?= csrf_field() ?>
                <input type="hidden" name="action" value="save_event_times">

                <div class="reg-times-grid">
                    <?php foreach ($seriesEvents as $se):
                        $opensDate = $se['registration_opens'] ? date('Y-m-d', strtotime($se['registration_opens'])) : '';
                        $opensTime = $se['registration_opens'] ? date('H:i', strtotime($se['registration_opens'])) : '00:00';
                        $closesDate = $se['registration_deadline'] ? date('Y-m-d', strtotime($se['registration_deadline'])) : '';
                        $closesTime = $se['registration_deadline'] ? date('H:i', strtotime($se['registration_deadline'])) : '23:59';
                    ?>
                    <div class="reg-time-row">
                        <div>
                            <input type="hidden" name="event_id[]" value="<?= $se['event_id'] ?>">
                            <strong><?= htmlspecialchars($se['event_name']) ?></strong>
                            <br><small class="text-muted"><?= date('Y-m-d', strtotime($se['event_date'])) ?></small>
                        </div>
                        <div>
                            <label class="text-xs text-secondary">Öppnar</label>
                            <div class="flex gap-xs">
                                <input type="date" name="opens_date[]" class="admin-form-input" value="<?= $opensDate ?>">
                                <input type="time" name="opens_time[]" class="admin-form-input" value="<?= $opensTime ?>" style="width: 100px;">
                            </div>
                        </div>
                        <div>
                            <label class="text-xs text-secondary">Stänger</label>
                            <div class="flex gap-xs">
                                <input type="date" name="closes_date[]" class="admin-form-input" value="<?= $closesDate ?>">
                                <input type="time" name="closes_time[]" class="admin-form-input" value="<?= $closesTime ?>" style="width: 100px;">
                            </div>
                        </div>
                        <div></div>
                    </div>
                    <?php endforeach; ?>
                </div>

                <div class="mt-lg">
                    <button type="submit" class="btn-admin btn-admin-primary">
                        <i data-lucide="save"></i> Spara anmälningstider
                    </button>
                </div>
            </form>
        </div>
    </div>
    <?php endif; ?>
</div>

<!-- ============================================================ -->
<!-- PAYMENT TAB -->
<!-- ============================================================ -->
<div class="tab-content <?= $activeTab === 'payment' ? 'active' : '' ?>" id="tab-payment">
    <form method="POST">
        <?= csrf_field() ?>
        <input type="hidden" name="action" value="save_payment">

        <?php if (!empty($paymentRecipients)): ?>
        <!-- Modern Payment Recipients -->
        <div class="admin-card mb-lg">
            <div class="admin-card-header">
                <h2><i data-lucide="building-2"></i> Betalningsmottagare</h2>
            </div>
            <div class="admin-card-body">
                <p class="text-secondary mb-md">
                    Välj vem som tar emot betalningar för denna serie. Event utan egen mottagare använder seriens.
                </p>

                <div class="admin-form-group">
                    <label class="admin-form-label">Mottagare</label>
                    <select name="payment_recipient_id" class="admin-form-select">
                        <option value="">-- Ingen (betalning inaktiverad) --</option>
                        <?php foreach ($paymentRecipients as $r): ?>
                        <option value="<?= $r['id'] ?>" <?= ($series['payment_recipient_id'] ?? '') == $r['id'] ? 'selected' : '' ?>>
                            <?= htmlspecialchars($r['name']) ?> (<?= htmlspecialchars($r['swish_number']) ?>)
                        </option>
                        <?php endforeach; ?>
                    </select>
                    <small class="text-secondary">
                        <a href="/admin/payment-recipients" class="text-accent">Hantera mottagare</a> |
                        <a href="/admin/swish-accounts" class="text-accent">Swish-konton</a>
                    </small>
                </div>
            </div>
        </div>
        <?php elseif ($hasLegacySwish): ?>
        <!-- Legacy Swish Fields -->
        <div class="admin-card mb-lg">
            <div class="admin-card-header">
                <h2><i data-lucide="smartphone"></i> Swish-betalning</h2>
            </div>
            <div class="admin-card-body">
                <div class="info-grid">
                    <div class="admin-form-group">
                        <label class="admin-form-label">Swish-nummer</label>
                        <input type="text" name="swish_number" class="admin-form-input"
                               value="<?= htmlspecialchars($series['swish_number'] ?? '') ?>"
                               placeholder="070-123 45 67">
                    </div>
                    <div class="admin-form-group">
                        <label class="admin-form-label">Mottagarnamn</label>
                        <input type="text" name="swish_name" class="admin-form-input"
                               value="<?= htmlspecialchars($series['swish_name'] ?? '') ?>"
                               placeholder="Seriens namn">
                    </div>
                </div>
            </div>
        </div>
        <?php else: ?>
        <div class="alert alert-info mb-lg">
            <i data-lucide="info"></i>
            Betalningssystemet är inte konfigurerat. Kontakta administratören.
        </div>
        <?php endif; ?>

        <!-- Gravity ID Discount -->
        <div class="admin-card mb-lg">
            <div class="admin-card-header">
                <h2><i data-lucide="badge-check"></i> Gravity ID-rabatt</h2>
            </div>
            <div class="admin-card-body">
                <p class="text-secondary mb-md">
                    Medlemmar med Gravity ID kan få rabatt på anmälan.
                </p>

                <div class="admin-form-group">
                    <label class="admin-form-label">Rabatt (SEK)</label>
                    <input type="number" name="gravity_id_discount" class="admin-form-input" style="max-width: 150px;"
                           value="<?= htmlspecialchars($series['gravity_id_discount'] ?? 0) ?>"
                           min="0" step="1">
                    <small class="text-secondary">0 = inaktiverat</small>
                </div>
            </div>
        </div>

        <button type="submit" class="btn-admin btn-admin-primary">
            <i data-lucide="save"></i> Spara betalningsinställningar
        </button>
    </form>
</div>

<!-- ============================================================ -->
<!-- RESULTS TAB -->
<!-- ============================================================ -->
<div class="tab-content <?= $activeTab === 'results' ? 'active' : '' ?>" id="tab-results">
    <div class="grid grid-cols-1 gs-lg-grid-cols-3 gap-lg">
        <!-- Settings -->
        <div>
            <div class="admin-card mb-lg">
                <div class="admin-card-header">
                    <h2><i data-lucide="calculator"></i> Poängräkning</h2>
                </div>
                <div class="admin-card-body">
                    <form method="POST">
                        <?= csrf_field() ?>
                        <input type="hidden" name="action" value="update_count_best">

                        <div class="admin-form-group">
                            <label class="admin-form-label">Räkna bästa resultat</label>
                            <select name="count_best_results" class="admin-form-select" onchange="this.form.submit()">
                                <option value="null" <?= ($series['count_best_results'] ?? null) === null ? 'selected' : '' ?>>
                                    Alla resultat
                                </option>
                                <?php for ($i = 1; $i <= 10; $i++): ?>
                                <option value="<?= $i ?>" <?= ($series['count_best_results'] ?? null) == $i ? 'selected' : '' ?>>
                                    Bästa <?= $i ?> av <?= $eventsCount ?>
                                </option>
                                <?php endfor; ?>
                            </select>
                            <small class="text-secondary">
                                Stryker sämsta resultat från totalen
                            </small>
                        </div>
                    </form>
                </div>
            </div>

            <div class="admin-card">
                <div class="admin-card-header">
                    <h2><i data-lucide="refresh-cw"></i> Omräkna poäng</h2>
                </div>
                <div class="admin-card-body">
                    <p class="text-secondary mb-md">
                        Beräkna om alla seriepoäng baserat på resultat och poängmallar.
                    </p>
                    <form method="POST">
                        <?= csrf_field() ?>
                        <input type="hidden" name="action" value="recalculate_all">
                        <button type="submit" class="btn-admin btn-admin-primary w-full"
                                onclick="return confirm('Beräkna om alla seriepoäng?');">
                            <i data-lucide="refresh-cw"></i> Beräkna om
                        </button>
                    </form>
                </div>
            </div>
        </div>

        <!-- Stats & Links -->
        <div class="gs-lg-col-span-2">
            <div class="admin-card">
                <div class="admin-card-header">
                    <h2><i data-lucide="bar-chart-3"></i> Statistik</h2>
                </div>
                <div class="admin-card-body">
                    <div class="grid grid-stats grid-gap-md mb-lg">
                        <div class="admin-stat-card">
                            <div class="admin-stat-value"><?= $eventsWithResults ?>/<?= $eventsCount ?></div>
                            <div class="admin-stat-label">Events med resultat</div>
                        </div>
                        <div class="admin-stat-card">
                            <div class="admin-stat-value"><?= number_format($uniqueParticipants) ?></div>
                            <div class="admin-stat-label">Unika deltagare</div>
                        </div>
                    </div>

                    <div class="flex gap-md flex-wrap">
                        <a href="/series/<?= $id ?>" class="btn-admin btn-admin-secondary" target="_blank">
                            <i data-lucide="external-link"></i> Visa serietabell
                        </a>
                        <a href="/admin/club-points?series=<?= $id ?>" class="btn-admin btn-admin-secondary">
                            <i data-lucide="building-2"></i> Klubbpoäng
                        </a>
                        <a href="/admin/import-results" class="btn-admin btn-admin-secondary">
                            <i data-lucide="upload"></i> Importera resultat
                        </a>
                    </div>
                </div>
            </div>

            <?php if ($eventsCount > 0 && $eventsWithResults >= $eventsCount && $series['status'] !== 'completed'): ?>
            <div class="alert alert-success mt-lg">
                <i data-lucide="check-circle"></i>
                <strong>Alla events har resultat!</strong>
                Du kan nu markera serien som "Avslutad" under Info-fliken för att beräkna seriemästare.
            </div>
            <?php endif; ?>
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
