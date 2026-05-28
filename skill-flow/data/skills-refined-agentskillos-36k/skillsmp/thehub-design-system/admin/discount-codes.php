<?php
/**
 * Discount Codes Management - Admin & Promotor Page
 * TheHUB - Manage discount codes for event registrations
 * Promotors can only see/manage codes for their own events/series
 */
require_once __DIR__ . '/../config.php';
require_admin();

$db = getDB();

// Determine user access level
$isAdmin = hasRole('admin');
$userId = $_SESSION['admin_id'] ?? null;

// Get promotor's accessible series and events (if not admin)
$promotorSeriesIds = [];
$promotorEventIds = [];
if (!$isAdmin && $userId) {
    $promotorSeries = getPromotorSeries();
    $promotorSeriesIds = array_column($promotorSeries, 'id');

    $promotorEvents = getPromotorEvents();
    $promotorEventIds = array_column($promotorEvents, 'id');
}

// Handle form submissions
$message = '';
$error = '';

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    checkCsrf();
    $action = $_POST['action'] ?? '';

    if ($action === 'create') {
        $code = strtoupper(trim($_POST['code'] ?? ''));
        $description = trim($_POST['description'] ?? '');
        $discountType = $_POST['discount_type'] ?? 'fixed';
        $discountValue = floatval($_POST['discount_value'] ?? 0);
        $maxUses = !empty($_POST['max_uses']) ? intval($_POST['max_uses']) : null;
        $maxUsesPerUser = !empty($_POST['max_uses_per_user']) ? intval($_POST['max_uses_per_user']) : 1;
        $validFrom = !empty($_POST['valid_from']) ? $_POST['valid_from'] : null;
        $validUntil = !empty($_POST['valid_until']) ? $_POST['valid_until'] : null;
        $applicableTo = $_POST['applicable_to'] ?? 'all';
        $eventId = !empty($_POST['event_id']) ? intval($_POST['event_id']) : null;
        $seriesId = !empty($_POST['series_id']) ? intval($_POST['series_id']) : null;
        $isActive = isset($_POST['is_active']) ? 1 : 0;

        // Validate access for promotors
        $accessError = false;
        if (!$isAdmin) {
            if ($applicableTo === 'all') {
                $accessError = true;
                $error = 'Du kan endast skapa koder för dina egna event eller serier';
            } elseif ($applicableTo === 'event' && $eventId && !in_array($eventId, $promotorEventIds)) {
                $accessError = true;
                $error = 'Du har inte behörighet till detta event';
            } elseif ($applicableTo === 'series' && $seriesId && !in_array($seriesId, $promotorSeriesIds)) {
                $accessError = true;
                $error = 'Du har inte behörighet till denna serie';
            }
        }

        if ($accessError) {
            // Error already set
        } elseif (empty($code)) {
            $error = 'Rabattkod är obligatorisk';
        } elseif ($discountValue <= 0) {
            $error = 'Rabattvärde måste vara större än 0';
        } else {
            try {
                $db->insert('discount_codes', [
                    'code' => $code,
                    'description' => $description,
                    'discount_type' => $discountType,
                    'discount_value' => $discountValue,
                    'max_uses' => $maxUses,
                    'max_uses_per_user' => $maxUsesPerUser,
                    'valid_from' => $validFrom,
                    'valid_until' => $validUntil,
                    'applicable_to' => $applicableTo,
                    'event_id' => $eventId,
                    'series_id' => $seriesId,
                    'is_active' => $isActive,
                    'created_by' => $_SESSION['user_id'] ?? null
                ]);
                $message = "Rabattkod '$code' skapad!";
            } catch (Exception $e) {
                if (strpos($e->getMessage(), 'Duplicate') !== false) {
                    $error = "Rabattkoden '$code' finns redan";
                } else {
                    $error = "Kunde inte skapa rabattkod: " . $e->getMessage();
                }
            }
        }
    } elseif ($action === 'toggle') {
        $id = intval($_POST['id']);
        // Check access for promotors
        if (!$isAdmin) {
            $code = $db->getRow("SELECT event_id, series_id FROM discount_codes WHERE id = ?", [$id]);
            if ($code) {
                $canAccess = ($code['event_id'] && in_array($code['event_id'], $promotorEventIds)) ||
                             ($code['series_id'] && in_array($code['series_id'], $promotorSeriesIds));
                if (!$canAccess) {
                    $error = "Du har inte behörighet att ändra denna rabattkod";
                }
            }
        }
        if (!$error) {
            $db->query("UPDATE discount_codes SET is_active = NOT is_active WHERE id = ?", [$id]);
            $message = "Status uppdaterad";
        }
    } elseif ($action === 'delete') {
        $id = intval($_POST['id']);
        // Check access for promotors
        if (!$isAdmin) {
            $code = $db->getRow("SELECT event_id, series_id FROM discount_codes WHERE id = ?", [$id]);
            if ($code) {
                $canAccess = ($code['event_id'] && in_array($code['event_id'], $promotorEventIds)) ||
                             ($code['series_id'] && in_array($code['series_id'], $promotorSeriesIds));
                if (!$canAccess) {
                    $error = "Du har inte behörighet att ta bort denna rabattkod";
                }
            }
        }
        if (!$error) {
            $db->query("DELETE FROM discount_codes WHERE id = ?", [$id]);
            $message = "Rabattkod borttagen";
        }
    }
}

// Fetch discount codes - filtered for promotors
if ($isAdmin) {
    // Admins see all codes
    $codes = $db->getAll("
        SELECT dc.*,
               e.name as event_name,
               s.name as series_name
        FROM discount_codes dc
        LEFT JOIN events e ON dc.event_id = e.id
        LEFT JOIN series s ON dc.series_id = s.id
        ORDER BY dc.created_at DESC
    ");
} else {
    // Promotors see only their codes (linked to their events/series)
    $codes = [];
    if (!empty($promotorEventIds) || !empty($promotorSeriesIds)) {
        $eventPlaceholders = !empty($promotorEventIds) ? implode(',', array_fill(0, count($promotorEventIds), '?')) : '0';
        $seriesPlaceholders = !empty($promotorSeriesIds) ? implode(',', array_fill(0, count($promotorSeriesIds), '?')) : '0';

        $params = array_merge($promotorEventIds, $promotorSeriesIds);
        $codes = $db->getAll("
            SELECT dc.*,
                   e.name as event_name,
                   s.name as series_name
            FROM discount_codes dc
            LEFT JOIN events e ON dc.event_id = e.id
            LEFT JOIN series s ON dc.series_id = s.id
            WHERE dc.event_id IN ($eventPlaceholders)
               OR dc.series_id IN ($seriesPlaceholders)
            ORDER BY dc.created_at DESC
        ", $params);
    }
}

// Fetch events and series for dropdowns - filtered for promotors
if ($isAdmin) {
    $events = $db->getAll("SELECT id, name, date FROM events WHERE date >= CURDATE() ORDER BY date ASC LIMIT 50");
    $seriesList = $db->getAll("SELECT id, name, year FROM series WHERE status = 'active' ORDER BY year DESC, name ASC");
} else {
    // Promotors see only their events/series
    $events = [];
    $seriesList = [];

    if (!empty($promotorEventIds)) {
        $placeholders = implode(',', array_fill(0, count($promotorEventIds), '?'));
        $events = $db->getAll("SELECT id, name, date FROM events WHERE id IN ($placeholders) AND date >= CURDATE() ORDER BY date ASC", $promotorEventIds);
    }

    if (!empty($promotorSeriesIds)) {
        $placeholders = implode(',', array_fill(0, count($promotorSeriesIds), '?'));
        $seriesList = $db->getAll("SELECT id, name, year FROM series WHERE id IN ($placeholders) ORDER BY year DESC, name ASC", $promotorSeriesIds);
    }
}

// Page config
$page_title = 'Rabattkoder';
$breadcrumbs = [
    ['label' => 'Ekonomi', 'url' => '/admin/payment-settings.php'],
    ['label' => 'Rabattkoder']
];

include __DIR__ . '/components/unified-layout.php';
?>

<style>
.code-card {
    background: var(--color-bg-surface);
    border: 1px solid var(--color-border);
    border-radius: var(--radius-md);
    padding: var(--space-md);
    margin-bottom: var(--space-md);
}
.code-card.inactive {
    opacity: 0.6;
}
.code-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: var(--space-sm);
}
.code-value {
    font-family: monospace;
    font-size: 1.25rem;
    font-weight: 700;
    color: var(--color-accent);
    background: var(--color-bg-page);
    padding: var(--space-xs) var(--space-sm);
    border-radius: var(--radius-sm);
}
.code-discount {
    font-size: 1.125rem;
    font-weight: 600;
}
.code-discount.percentage { color: var(--color-success); }
.code-discount.fixed { color: var(--color-accent); }
.code-meta {
    display: flex;
    flex-wrap: wrap;
    gap: var(--space-md);
    font-size: 0.875rem;
    color: var(--color-text-secondary);
    margin-bottom: var(--space-sm);
}
.code-meta-item {
    display: flex;
    align-items: center;
    gap: var(--space-2xs);
}
.code-actions {
    display: flex;
    gap: var(--space-xs);
    margin-top: var(--space-sm);
    padding-top: var(--space-sm);
    border-top: 1px solid var(--color-border);
}
.create-form {
    background: var(--color-bg-surface);
    border: 1px solid var(--color-border);
    border-radius: var(--radius-md);
    padding: var(--space-lg);
    margin-bottom: var(--space-lg);
}
.form-row {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: var(--space-md);
    margin-bottom: var(--space-md);
}
.form-group label {
    display: block;
    font-size: 0.875rem;
    font-weight: 500;
    color: var(--color-text-secondary);
    margin-bottom: var(--space-2xs);
}
.form-group input,
.form-group select {
    width: 100%;
    padding: var(--space-sm);
    border: 1px solid var(--color-border);
    border-radius: var(--radius-sm);
    background: var(--color-bg-page);
    color: var(--color-text-primary);
}
.stats-row {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
    gap: var(--space-md);
    margin-bottom: var(--space-lg);
}
.stat-card {
    background: var(--color-bg-surface);
    border: 1px solid var(--color-border);
    border-radius: var(--radius-md);
    padding: var(--space-md);
    text-align: center;
}
.stat-value {
    font-size: 2rem;
    font-weight: 700;
    color: var(--color-accent);
}
.stat-label {
    font-size: 0.875rem;
    color: var(--color-text-muted);
}
</style>

<?php if ($message): ?>
    <div class="alert alert-success" style="margin-bottom: var(--space-md);"><?= htmlspecialchars($message) ?></div>
<?php endif; ?>
<?php if ($error): ?>
    <div class="alert alert-danger" style="margin-bottom: var(--space-md);"><?= htmlspecialchars($error) ?></div>
<?php endif; ?>

<!-- Stats -->
<div class="stats-row">
    <div class="stat-card">
        <div class="stat-value"><?= count($codes) ?></div>
        <div class="stat-label">Totalt koder</div>
    </div>
    <div class="stat-card">
        <div class="stat-value"><?= count(array_filter($codes, fn($c) => $c['is_active'])) ?></div>
        <div class="stat-label">Aktiva</div>
    </div>
    <div class="stat-card">
        <div class="stat-value"><?= array_sum(array_column($codes, 'current_uses')) ?></div>
        <div class="stat-label">Totala användningar</div>
    </div>
</div>

<!-- Create Form -->
<details class="create-form" open>
    <summary style="cursor: pointer; font-weight: 600; margin-bottom: var(--space-md);">
        <i data-lucide="plus"></i> Skapa ny rabattkod
    </summary>

    <form method="POST">
        <?= csrf_field() ?>
        <input type="hidden" name="action" value="create">

        <div class="form-row">
            <div class="form-group">
                <label>Rabattkod *</label>
                <input type="text" name="code" required placeholder="T.ex. SUMMER2026" style="text-transform: uppercase;">
            </div>
            <div class="form-group">
                <label>Beskrivning</label>
                <input type="text" name="description" placeholder="Intern beskrivning">
            </div>
        </div>

        <div class="form-row">
            <div class="form-group">
                <label>Rabattyp</label>
                <select name="discount_type">
                    <option value="fixed">Fast belopp (SEK)</option>
                    <option value="percentage">Procent (%)</option>
                </select>
            </div>
            <div class="form-group">
                <label>Rabattvärde *</label>
                <input type="number" name="discount_value" required min="1" step="1" placeholder="50">
            </div>
            <div class="form-group">
                <label>Max användningar</label>
                <input type="number" name="max_uses" min="1" placeholder="Obegränsat">
            </div>
            <div class="form-group">
                <label>Max per användare</label>
                <input type="number" name="max_uses_per_user" min="1" value="1">
            </div>
        </div>

        <div class="form-row">
            <div class="form-group">
                <label>Giltig från</label>
                <input type="datetime-local" name="valid_from">
            </div>
            <div class="form-group">
                <label>Giltig till</label>
                <input type="datetime-local" name="valid_until">
            </div>
        </div>

        <div class="form-row">
            <div class="form-group">
                <label>Gäller för</label>
                <select name="applicable_to" onchange="toggleRestriction(this.value)">
                    <?php if ($isAdmin): ?>
                    <option value="all">Alla anmälningar</option>
                    <?php endif; ?>
                    <option value="event" <?= !$isAdmin ? 'selected' : '' ?>>Specifikt event</option>
                    <option value="series">Specifik serie</option>
                </select>
            </div>
            <div class="form-group" id="event-select" style="display: none;">
                <label>Välj event</label>
                <select name="event_id">
                    <option value="">Välj...</option>
                    <?php foreach ($events as $event): ?>
                        <option value="<?= $event['id'] ?>"><?= htmlspecialchars($event['name']) ?> (<?= $event['date'] ?>)</option>
                    <?php endforeach; ?>
                </select>
            </div>
            <div class="form-group" id="series-select" style="display: none;">
                <label>Välj serie</label>
                <select name="series_id">
                    <option value="">Välj...</option>
                    <?php foreach ($seriesList as $series): ?>
                        <option value="<?= $series['id'] ?>"><?= htmlspecialchars($series['name']) ?> (<?= $series['year'] ?>)</option>
                    <?php endforeach; ?>
                </select>
            </div>
        </div>

        <div class="form-row">
            <div class="form-group">
                <label>
                    <input type="checkbox" name="is_active" value="1" checked>
                    Aktiv
                </label>
            </div>
        </div>

        <button type="submit" class="btn btn-primary">
            <i data-lucide="plus"></i> Skapa rabattkod
        </button>
    </form>
</details>

<!-- Existing Codes -->
<h3 style="margin-bottom: var(--space-md);">Befintliga rabattkoder (<?= count($codes) ?>)</h3>

<?php if (empty($codes)): ?>
    <div class="card">
        <div class="card-body" style="text-align: center; padding: var(--space-2xl);">
            <i data-lucide="ticket" style="width: 48px; height: 48px; color: var(--color-text-muted);"></i>
            <p style="margin-top: var(--space-md); color: var(--color-text-muted);">
                Inga rabattkoder skapade än. Skapa din första rabattkod ovan.
            </p>
        </div>
    </div>
<?php else: ?>
    <?php foreach ($codes as $code): ?>
        <div class="code-card <?= $code['is_active'] ? '' : 'inactive' ?>">
            <div class="code-header">
                <span class="code-value"><?= htmlspecialchars($code['code']) ?></span>
                <span class="code-discount <?= $code['discount_type'] ?>">
                    <?php if ($code['discount_type'] === 'percentage'): ?>
                        -<?= intval($code['discount_value']) ?>%
                    <?php else: ?>
                        -<?= number_format($code['discount_value'], 0) ?> kr
                    <?php endif; ?>
                </span>
            </div>

            <?php if ($code['description']): ?>
                <p style="margin-bottom: var(--space-sm); color: var(--color-text-secondary);">
                    <?= htmlspecialchars($code['description']) ?>
                </p>
            <?php endif; ?>

            <div class="code-meta">
                <span class="code-meta-item">
                    <i data-lucide="hash"></i>
                    <?= $code['current_uses'] ?><?= $code['max_uses'] ? '/' . $code['max_uses'] : '' ?> användningar
                </span>

                <?php if ($code['valid_from'] || $code['valid_until']): ?>
                    <span class="code-meta-item">
                        <i data-lucide="calendar"></i>
                        <?= $code['valid_from'] ? date('Y-m-d', strtotime($code['valid_from'])) : 'Start' ?>
                        -
                        <?= $code['valid_until'] ? date('Y-m-d', strtotime($code['valid_until'])) : 'Ingen slut' ?>
                    </span>
                <?php endif; ?>

                <?php if ($code['applicable_to'] !== 'all'): ?>
                    <span class="code-meta-item">
                        <i data-lucide="target"></i>
                        <?php if ($code['event_name']): ?>
                            Event: <?= htmlspecialchars($code['event_name']) ?>
                        <?php elseif ($code['series_name']): ?>
                            Serie: <?= htmlspecialchars($code['series_name']) ?>
                        <?php endif; ?>
                    </span>
                <?php endif; ?>

                <span class="code-meta-item">
                    <i data-lucide="<?= $code['is_active'] ? 'check-circle' : 'x-circle' ?>"></i>
                    <?= $code['is_active'] ? 'Aktiv' : 'Inaktiv' ?>
                </span>
            </div>

            <div class="code-actions">
                <form method="POST" style="display: inline;">
                    <?= csrf_field() ?>
                    <input type="hidden" name="action" value="toggle">
                    <input type="hidden" name="id" value="<?= $code['id'] ?>">
                    <button type="submit" class="btn btn-ghost btn-sm">
                        <i data-lucide="<?= $code['is_active'] ? 'pause' : 'play' ?>"></i>
                        <?= $code['is_active'] ? 'Inaktivera' : 'Aktivera' ?>
                    </button>
                </form>
                <form method="POST" style="display: inline;" onsubmit="return confirm('Ta bort denna rabattkod?');">
                    <?= csrf_field() ?>
                    <input type="hidden" name="action" value="delete">
                    <input type="hidden" name="id" value="<?= $code['id'] ?>">
                    <button type="submit" class="btn btn-ghost btn-sm">
                        <i data-lucide="trash-2"></i> Ta bort
                    </button>
                </form>
            </div>
        </div>
    <?php endforeach; ?>
<?php endif; ?>

<script>
function toggleRestriction(value) {
    document.getElementById('event-select').style.display = value === 'event' ? 'block' : 'none';
    document.getElementById('series-select').style.display = value === 'series' ? 'block' : 'none';
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
    const select = document.querySelector('select[name="applicable_to"]');
    if (select) {
        toggleRestriction(select.value);
    }
});

lucide.createIcons();
</script>

<?php include __DIR__ . '/components/unified-layout-footer.php'; ?>
