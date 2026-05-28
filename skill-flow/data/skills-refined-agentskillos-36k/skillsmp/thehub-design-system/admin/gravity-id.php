<?php
/**
 * Gravity ID Management Panel
 * TheHUB - Manage Gravity ID members and discounts
 */
require_once __DIR__ . '/../config.php';
require_admin();

$db = getDB();

// Handle form submissions
$message = '';
$error = '';

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    checkCsrf();
    $action = $_POST['action'] ?? '';

    if ($action === 'update_settings') {
        $defaultDiscount = floatval($_POST['default_discount'] ?? 50);
        $enabled = isset($_POST['enabled']) ? '1' : '0';

        try {
            $db->query("INSERT INTO gravity_id_settings (setting_key, setting_value) VALUES ('default_discount', ?)
                        ON DUPLICATE KEY UPDATE setting_value = ?", [$defaultDiscount, $defaultDiscount]);
            $db->query("INSERT INTO gravity_id_settings (setting_key, setting_value) VALUES ('enabled', ?)
                        ON DUPLICATE KEY UPDATE setting_value = ?", [$enabled, $enabled]);
            $message = "Inställningar sparade!";
        } catch (Exception $e) {
            $error = "Kunde inte spara: " . $e->getMessage();
        }
    } elseif ($action === 'add_gravity_id') {
        $riderId = intval($_POST['rider_id']);
        $gravityId = trim($_POST['gravity_id']);

        if ($riderId && $gravityId) {
            try {
                $db->query("UPDATE riders SET gravity_id = ? WHERE id = ?", [$gravityId, $riderId]);
                $message = "Gravity ID tilldelat!";
            } catch (Exception $e) {
                $error = "Kunde inte tilldela: " . $e->getMessage();
            }
        }
    } elseif ($action === 'remove_gravity_id') {
        $riderId = intval($_POST['rider_id']);
        try {
            $db->query("UPDATE riders SET gravity_id = NULL WHERE id = ?", [$riderId]);
            $message = "Gravity ID borttaget";
        } catch (Exception $e) {
            $error = "Kunde inte ta bort: " . $e->getMessage();
        }
    }
}

// Get settings
$settings = [];
try {
    $settingsRows = $db->getAll("SELECT setting_key, setting_value FROM gravity_id_settings");
    foreach ($settingsRows as $row) {
        $settings[$row['setting_key']] = $row['setting_value'];
    }
} catch (Exception $e) {
    // Table might not exist yet
}

$defaultDiscount = $settings['default_discount'] ?? 0;
$enabled = ($settings['enabled'] ?? '0') === '1';

// Get members with Gravity ID
$members = [];
$hasExtendedColumns = true;
$queryError = null;

try {
    // Try with extended columns first (after migration 103)
    $members = $db->getAll("
        SELECT r.id, r.firstname, r.lastname, r.gravity_id, r.gravity_id_since, r.gravity_id_valid_until,
               r.email, r.club_id, c.name as club_name,
               0 as reg_count
        FROM riders r
        LEFT JOIN clubs c ON r.club_id = c.id
        WHERE r.gravity_id IS NOT NULL AND r.gravity_id != ''
        ORDER BY r.lastname ASC
    ");
} catch (Exception $e) {
    // Extended columns don't exist - try basic query
    $hasExtendedColumns = false;
    try {
        $members = $db->getAll("
            SELECT r.id, r.firstname, r.lastname, r.gravity_id,
                   NULL as gravity_id_since, NULL as gravity_id_valid_until,
                   r.email, r.club_id, c.name as club_name,
                   0 as reg_count
            FROM riders r
            LEFT JOIN clubs c ON r.club_id = c.id
            WHERE r.gravity_id IS NOT NULL AND r.gravity_id != ''
            ORDER BY r.lastname ASC
        ");
    } catch (Exception $e2) {
        // gravity_id column doesn't exist at all
        $queryError = $e2->getMessage();
        $error = "Databasfel: " . $e2->getMessage();
    }
}

// Get stats
$totalMembers = count($members);

// For search
$searchRiders = [];
if (isset($_GET['search']) && strlen($_GET['search']) >= 2) {
    $search = '%' . $_GET['search'] . '%';
    $searchRiders = $db->getAll("
        SELECT id, firstname, lastname, email, gravity_id
        FROM riders
        WHERE (firstname LIKE ? OR lastname LIKE ? OR email LIKE ?) AND gravity_id IS NULL
        LIMIT 20
    ", [$search, $search, $search]);
}

// Page config
$page_title = 'Gravity ID';
$breadcrumbs = [
    ['label' => 'Ekonomi', 'url' => '/admin/payment-settings.php'],
    ['label' => 'Gravity ID']
];

include __DIR__ . '/components/unified-layout.php';
?>

<style>
.gid-stats {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
    gap: var(--space-md);
    margin-bottom: var(--space-lg);
}
.gid-stat {
    background: var(--color-bg-surface);
    border: 1px solid var(--color-border);
    border-radius: var(--radius-md);
    padding: var(--space-lg);
    text-align: center;
}
.gid-stat-value {
    font-size: 2.5rem;
    font-weight: 700;
    color: var(--color-accent);
}
.gid-stat-label {
    font-size: 0.875rem;
    color: var(--color-text-muted);
    margin-top: var(--space-xs);
}
.settings-card, .add-card {
    background: var(--color-bg-surface);
    border: 1px solid var(--color-border);
    border-radius: var(--radius-md);
    padding: var(--space-lg);
    margin-bottom: var(--space-lg);
}
.settings-card h3, .add-card h3 {
    margin: 0 0 var(--space-md);
    display: flex;
    align-items: center;
    gap: var(--space-sm);
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
.member-table {
    width: 100%;
    border-collapse: collapse;
}
.member-table th,
.member-table td {
    padding: var(--space-sm);
    text-align: left;
    border-bottom: 1px solid var(--color-border);
}
.member-table th {
    background: var(--color-bg-page);
    font-weight: 600;
    color: var(--color-text-secondary);
    font-size: 0.875rem;
}
.gid-badge {
    font-family: monospace;
    font-weight: 600;
    color: var(--color-accent);
    background: var(--color-accent-light);
    padding: 2px 8px;
    border-radius: var(--radius-sm);
}
.sortable {
    cursor: pointer;
    user-select: none;
    white-space: nowrap;
}
.sortable:hover {
    color: var(--color-accent);
}
.sortable .sort-icon {
    width: 14px;
    height: 14px;
    vertical-align: middle;
    opacity: 0.5;
    margin-left: 4px;
}
.sortable.asc .sort-icon,
.sortable.desc .sort-icon {
    opacity: 1;
    color: var(--color-accent);
}
.search-results {
    background: var(--color-bg-surface);
    border: 1px solid var(--color-border);
    border-radius: var(--radius-sm);
    margin-top: var(--space-sm);
    max-height: 300px;
    overflow-y: auto;
}
.search-result {
    padding: var(--space-sm);
    border-bottom: 1px solid var(--color-border);
    display: flex;
    justify-content: space-between;
    align-items: center;
}
.search-result:last-child {
    border-bottom: none;
}
.search-result:hover {
    background: var(--color-bg-hover);
}
</style>

<?php if ($message): ?>
    <div class="alert alert-success" style="margin-bottom: var(--space-md);"><?= htmlspecialchars($message) ?></div>
<?php endif; ?>
<?php if ($error): ?>
    <div class="alert alert-danger" style="margin-bottom: var(--space-md);"><?= htmlspecialchars($error) ?></div>
<?php endif; ?>

<!-- Stats -->
<div class="gid-stats">
    <div class="gid-stat">
        <div class="gid-stat-value"><?= $totalMembers ?></div>
        <div class="gid-stat-label">Medlemmar</div>
    </div>
    <div class="gid-stat">
        <div class="gid-stat-value"><?= number_format($defaultDiscount, 0) ?> kr</div>
        <div class="gid-stat-label">Rabatt per event</div>
    </div>
</div>

<!-- Settings -->
<div class="settings-card">
    <h3><i data-lucide="settings"></i> Inställningar</h3>

    <form method="POST">
        <?= csrf_field() ?>
        <input type="hidden" name="action" value="update_settings">

        <div class="form-row">
            <div class="form-group">
                <label>Rabatt per event (SEK)</label>
                <input type="number" name="default_discount" value="<?= $defaultDiscount ?>" min="0" step="1">
            </div>
            <div class="form-group">
                <label style="display: flex; align-items: center; gap: var(--space-sm); margin-top: var(--space-md);">
                    <input type="checkbox" name="enabled" value="1" <?= $enabled ? 'checked' : '' ?>>
                    Aktivera Gravity ID-rabatter
                </label>
            </div>
        </div>

        <button type="submit" class="btn btn-primary">
            <i data-lucide="save"></i> Spara inställningar
        </button>
    </form>
</div>

<!-- Add New Member -->
<div class="add-card">
    <h3><i data-lucide="user-plus"></i> Lägg till Gravity ID</h3>

    <form method="GET" id="search-form">
        <div class="form-group">
            <label>Sök åkare (namn eller e-post)</label>
            <input type="text" name="search" id="rider-search" placeholder="Skriv minst 2 tecken..."
                   value="<?= htmlspecialchars($_GET['search'] ?? '') ?>" autocomplete="off">
        </div>
    </form>

    <?php if (!empty($searchRiders)): ?>
        <div class="search-results">
            <?php foreach ($searchRiders as $rider): ?>
                <div class="search-result">
                    <div>
                        <strong><?= htmlspecialchars($rider['firstname'] . ' ' . $rider['lastname']) ?></strong>
                        <span style="color: var(--color-text-muted); font-size: 0.875rem;">
                            (<?= htmlspecialchars($rider['email'] ?? 'ingen e-post') ?>)
                        </span>
                    </div>
                    <form method="POST" style="display: flex; gap: var(--space-xs); align-items: center;">
                        <?= csrf_field() ?>
                        <input type="hidden" name="action" value="add_gravity_id">
                        <input type="hidden" name="rider_id" value="<?= $rider['id'] ?>">
                        <input type="text" name="gravity_id" placeholder="GID-XXXXX" required
                               style="width: 120px; padding: var(--space-xs);">
                        <button type="submit" class="btn btn-primary btn-sm">
                            <i data-lucide="plus"></i>
                        </button>
                    </form>
                </div>
            <?php endforeach; ?>
        </div>
    <?php elseif (isset($_GET['search']) && strlen($_GET['search']) >= 2): ?>
        <p style="color: var(--color-text-muted); padding: var(--space-md);">
            Inga åkare hittades utan Gravity ID som matchar "<?= htmlspecialchars($_GET['search']) ?>"
        </p>
    <?php endif; ?>
</div>

<!-- Members List -->
<div class="settings-card">
    <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: var(--space-sm); margin-bottom: var(--space-md);">
        <h3 style="margin: 0;"><i data-lucide="users"></i> Medlemmar med Gravity ID (<?= $totalMembers ?>)</h3>
        <a href="/admin/import-gravity-id.php" class="btn btn-secondary btn-sm">
            <i data-lucide="upload"></i> Importera CSV
        </a>
    </div>

    <?php if (empty($members)): ?>
        <div style="text-align: center; padding: var(--space-xl); background: var(--color-bg-page); border-radius: var(--radius-md);">
            <i data-lucide="badge-check" style="width: 48px; height: 48px; color: var(--color-text-muted); margin-bottom: var(--space-md); display: block; margin-left: auto; margin-right: auto;"></i>
            <p style="color: var(--color-text-muted); margin-bottom: var(--space-md);">
                Inga medlemmar med Gravity ID ännu.
            </p>
            <p style="color: var(--color-text-muted); font-size: 0.875rem;">
                Sök efter en åkare ovan och lägg till Gravity ID manuellt,<br>
                eller importera flera via CSV-knappen.
            </p>
        </div>
    <?php else: ?>
        <div style="overflow-x: auto;">
            <table class="member-table">
                <thead>
                    <tr>
                        <th class="sortable" data-sort="gid" data-type="string">Gravity ID <i data-lucide="chevrons-up-down" class="sort-icon"></i></th>
                        <th class="sortable" data-sort="name" data-type="string">Namn <i data-lucide="chevrons-up-down" class="sort-icon"></i></th>
                        <th class="sortable" data-sort="club" data-type="string">Klubb <i data-lucide="chevrons-up-down" class="sort-icon"></i></th>
                        <th>E-post</th>
                        <th></th>
                    </tr>
                </thead>
                <tbody>
                    <?php foreach ($members as $member): ?>
                        <tr data-gid="<?= htmlspecialchars($member['gravity_id']) ?>"
                            data-name="<?= htmlspecialchars($member['lastname'] . ' ' . $member['firstname']) ?>"
                            data-club="<?= htmlspecialchars($member['club_name'] ?? '') ?>">
                            <td><span class="gid-badge"><?= htmlspecialchars($member['gravity_id']) ?></span></td>
                            <td>
                                <a href="/rider/<?= $member['id'] ?>" style="color: var(--color-text-primary);">
                                    <?= htmlspecialchars($member['firstname'] . ' ' . $member['lastname']) ?>
                                </a>
                            </td>
                            <td><?= htmlspecialchars($member['club_name'] ?? '-') ?></td>
                            <td style="color: var(--color-text-muted); font-size: 0.875rem;"><?= htmlspecialchars($member['email'] ?? '-') ?></td>
                            <td>
                                <form method="POST" style="display: inline;" onsubmit="return confirm('Ta bort Gravity ID för denna åkare?');">
                                    <?= csrf_field() ?>
                                    <input type="hidden" name="action" value="remove_gravity_id">
                                    <input type="hidden" name="rider_id" value="<?= $member['id'] ?>">
                                    <button type="submit" class="btn btn-ghost btn-sm" title="Ta bort">
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

<script>
// Table sorting
document.querySelectorAll('.sortable').forEach(header => {
    header.addEventListener('click', function() {
        const table = this.closest('table');
        const tbody = table.querySelector('tbody');
        const rows = Array.from(tbody.querySelectorAll('tr'));
        const sortKey = this.dataset.sort;
        const isAsc = this.classList.contains('asc');

        // Remove sort classes from all headers
        table.querySelectorAll('.sortable').forEach(h => h.classList.remove('asc', 'desc'));

        // Add sort class to clicked header
        this.classList.add(isAsc ? 'desc' : 'asc');

        // Sort rows
        rows.sort((a, b) => {
            let aVal = a.dataset[sortKey] || '';
            let bVal = b.dataset[sortKey] || '';

            // Natural sort for GID numbers
            if (sortKey === 'gid') {
                const aNum = parseInt(aVal.replace(/\D/g, '')) || 0;
                const bNum = parseInt(bVal.replace(/\D/g, '')) || 0;
                return isAsc ? bNum - aNum : aNum - bNum;
            }

            // String sort for name/club
            return isAsc
                ? bVal.localeCompare(aVal, 'sv')
                : aVal.localeCompare(bVal, 'sv');
        });

        // Reorder rows
        rows.forEach(row => tbody.appendChild(row));
    });
});

lucide.createIcons();
</script>

<?php include __DIR__ . '/components/unified-layout-footer.php'; ?>
