<?php
/**
 * Club Admins Management - Simple search tool
 * Search activated rider → Make them admin for their own club
 */
ini_set('display_errors', 1);
error_reporting(E_ALL);

require_once __DIR__ . '/../config.php';
require_admin();

if (!hasRole('admin')) {
    http_response_code(403);
    die('Access denied');
}

$pdo = $GLOBALS['pdo'];
$currentAdmin = getCurrentAdmin();
$message = '';
$messageType = '';

// Check if club_admins table exists
$tableExists = true;
try {
    $pdo->query("SELECT 1 FROM club_admins LIMIT 1");
} catch (Exception $e) {
    $tableExists = false;
    $message = 'Tabellen club_admins saknas. Kör migration 091 först.';
    $messageType = 'error';
}

// Handle actions
if ($_SERVER['REQUEST_METHOD'] === 'POST' && $tableExists) {
    $action = $_POST['action'] ?? '';

    if ($action === 'add') {
        $riderId = (int)($_POST['rider_id'] ?? 0);

        if ($riderId) {
            try {
                // Get rider info with club
                $stmt = $pdo->prepare("
                    SELECT r.id, r.firstname, r.lastname, r.email, r.club_id, c.name as club_name
                    FROM riders r
                    LEFT JOIN clubs c ON r.club_id = c.id
                    WHERE r.id = ? AND r.password IS NOT NULL AND r.password != ''
                ");
                $stmt->execute([$riderId]);
                $rider = $stmt->fetch(PDO::FETCH_ASSOC);

                if (!$rider) {
                    $message = 'Rider hittades inte eller har inte aktiverat konto';
                    $messageType = 'error';
                } elseif (!$rider['club_id']) {
                    $message = $rider['firstname'] . ' ' . $rider['lastname'] . ' saknar klubbkoppling';
                    $messageType = 'error';
                } else {
                    // Check if rider already has admin account
                    $stmt = $pdo->prepare("SELECT id FROM admin_users WHERE email = ?");
                    $stmt->execute([$rider['email']]);
                    $existingUser = $stmt->fetch(PDO::FETCH_ASSOC);

                    if ($existingUser) {
                        $userId = $existingUser['id'];
                    } else {
                        // Create new admin user
                        $username = strtolower(preg_replace('/[^a-z0-9]/', '', $rider['firstname'] . $rider['lastname']));
                        $baseUsername = $username ?: 'user';
                        $counter = 1;

                        $stmt = $pdo->prepare("SELECT id FROM admin_users WHERE username = ?");
                        $stmt->execute([$username]);
                        while ($stmt->fetch()) {
                            $username = $baseUsername . $counter++;
                            $stmt->execute([$username]);
                        }

                        $stmt = $pdo->prepare("
                            INSERT INTO admin_users (username, email, full_name, role, active, created_at)
                            VALUES (?, ?, ?, 'rider', 1, NOW())
                        ");
                        $stmt->execute([$username, $rider['email'], $rider['firstname'] . ' ' . $rider['lastname']]);
                        $userId = $pdo->lastInsertId();
                    }

                    // Check if already admin for this club
                    $stmt = $pdo->prepare("SELECT id FROM club_admins WHERE user_id = ? AND club_id = ?");
                    $stmt->execute([$userId, $rider['club_id']]);

                    if ($stmt->fetch()) {
                        $message = $rider['firstname'] . ' ' . $rider['lastname'] . ' är redan admin för ' . $rider['club_name'];
                        $messageType = 'warning';
                    } else {
                        $stmt = $pdo->prepare("
                            INSERT INTO club_admins (user_id, club_id, can_edit_profile, can_upload_logo, granted_by, created_at)
                            VALUES (?, ?, 1, 1, ?, NOW())
                        ");
                        $stmt->execute([$userId, $rider['club_id'], $currentAdmin['id']]);

                        $message = $rider['firstname'] . ' ' . $rider['lastname'] . ' är nu admin för ' . $rider['club_name'];
                        $messageType = 'success';
                    }
                }
            } catch (Exception $e) {
                $message = 'Fel: ' . $e->getMessage();
                $messageType = 'error';
            }
        }
    } elseif ($action === 'remove') {
        $id = (int)($_POST['id'] ?? 0);
        if ($id) {
            try {
                $stmt = $pdo->prepare("DELETE FROM club_admins WHERE id = ?");
                $stmt->execute([$id]);
                $message = 'Klubb-admin borttagen';
                $messageType = 'success';
            } catch (Exception $e) {
                $message = 'Fel: ' . $e->getMessage();
                $messageType = 'error';
            }
        }
    }
}

// Get current club admins
$clubAdmins = [];
if ($tableExists) {
    try {
        // First check if table has correct columns
        $cols = $pdo->query("DESCRIBE club_admins")->fetchAll(PDO::FETCH_COLUMN);
        if (!in_array('user_id', $cols)) {
            // Table has wrong structure - need to recreate
            $message = 'Tabellen club_admins har fel struktur. Kör: DROP TABLE club_admins; och sedan migration 091 igen.';
            $messageType = 'error';
        } else {
            $stmt = $pdo->query("
                SELECT
                    ca.id,
                    au.full_name,
                    au.email,
                    c.name as club_name
                FROM club_admins ca
                JOIN admin_users au ON ca.user_id = au.id
                JOIN clubs c ON ca.club_id = c.id
                ORDER BY c.name, au.full_name
            ");
            $clubAdmins = $stmt->fetchAll(PDO::FETCH_ASSOC);
        }
    } catch (Exception $e) {
        $message = 'Kunde inte hämta klubb-admins: ' . $e->getMessage();
        $messageType = 'error';
    }
}

$page_title = 'Klubb-admin';
$breadcrumbs = [['label' => 'Användare', 'url' => '/admin/users.php'], ['label' => 'Klubb-admin']];
include __DIR__ . '/components/unified-layout.php';
?>

<?php if ($message): ?>
<div class="alert alert--<?= $messageType ?>" style="margin-bottom: var(--space-md);">
    <?= htmlspecialchars($message) ?>
</div>
<?php endif; ?>

<div class="card mb-lg">
    <div class="card-header">
        <h2>Lägg till klubb-admin</h2>
    </div>
    <div class="card-body">
        <p class="text-secondary mb-md">Sök efter deltagare med aktiverat konto. De blir automatiskt admin för sin egen klubb.</p>

        <form method="POST" id="addForm">
            <input type="hidden" name="action" value="add">
            <input type="hidden" name="rider_id" id="riderId">

            <div class="search-container">
                <input type="text" id="searchInput" class="form-input" placeholder="Sök namn..." autocomplete="off">
                <div id="searchResults" class="search-results"></div>
            </div>

            <div id="selectedRider" class="selected-box" style="display:none;"></div>

            <button type="submit" id="submitBtn" class="btn btn--primary mt-md" disabled>
                <i data-lucide="plus"></i> Lägg till som klubb-admin
            </button>
        </form>
    </div>
</div>

<div class="card">
    <div class="card-header">
        <h2>Nuvarande klubb-admins (<?= count($clubAdmins) ?>)</h2>
    </div>
    <div class="card-body">
        <?php if (empty($clubAdmins)): ?>
            <p class="text-secondary">Inga klubb-administratörer.</p>
        <?php else: ?>
            <div class="admin-list">
                <?php foreach ($clubAdmins as $ca): ?>
                <div class="admin-row">
                    <div class="admin-info">
                        <strong><?= h($ca['full_name'] ?: $ca['email']) ?></strong>
                        <span class="text-secondary"><?= h($ca['club_name']) ?></span>
                    </div>
                    <form method="POST" onsubmit="return confirm('Ta bort?')">
                        <input type="hidden" name="action" value="remove">
                        <input type="hidden" name="id" value="<?= $ca['id'] ?>">
                        <button class="btn btn--danger btn--sm"><i data-lucide="x"></i></button>
                    </form>
                </div>
                <?php endforeach; ?>
            </div>
        <?php endif; ?>
    </div>
</div>

<style>
.search-container { position: relative; max-width: 400px; }
.search-results {
    position: absolute; top: 100%; left: 0; right: 0;
    background: #fff; border: 1px solid var(--color-border);
    border-radius: var(--radius-md); max-height: 300px; overflow-y: auto;
    z-index: 100; display: none; box-shadow: var(--shadow-lg);
}
.search-results.show { display: block; }
.search-item {
    padding: var(--space-sm) var(--space-md);
    cursor: pointer; border-bottom: 1px solid var(--color-border);
}
.search-item:hover { background: var(--color-bg-sunken); }
.search-item:last-child { border-bottom: none; }
.search-item-name { font-weight: 600; }
.search-item-club { font-size: 0.875rem; color: var(--color-text-secondary); }
.selected-box {
    margin-top: var(--space-md); padding: var(--space-md);
    background: rgba(97,206,112,0.1); border: 1px solid var(--color-accent);
    border-radius: var(--radius-md); max-width: 400px;
}
.selected-box .name { font-weight: 600; }
.selected-box .club { color: var(--color-text-secondary); }
.selected-box .clear { float: right; cursor: pointer; color: var(--color-text-secondary); }
.selected-box .clear:hover { color: var(--color-danger); }
.admin-list { display: flex; flex-direction: column; gap: var(--space-sm); }
.admin-row {
    display: flex; justify-content: space-between; align-items: center;
    padding: var(--space-sm) var(--space-md);
    background: var(--color-bg-sunken); border-radius: var(--radius-sm);
}
.admin-info { display: flex; flex-direction: column; gap: 2px; }
@media (min-width: 600px) {
    .admin-info { flex-direction: row; gap: var(--space-md); align-items: center; }
}
</style>

<script>
document.addEventListener('DOMContentLoaded', function() {
    const input = document.getElementById('searchInput');
    const results = document.getElementById('searchResults');
    const selected = document.getElementById('selectedRider');
    const riderId = document.getElementById('riderId');
    const submitBtn = document.getElementById('submitBtn');
    let timeout;

    input.addEventListener('input', function() {
        clearTimeout(timeout);
        const q = this.value.trim();
        if (q.length < 2) { results.classList.remove('show'); return; }

        timeout = setTimeout(() => {
            fetch('/api/search-riders.php?q=' + encodeURIComponent(q) + '&activated=1&with_club=1&limit=20')
                .then(r => r.json())
                .then(data => {
                    if (data.riders?.length) {
                        results.innerHTML = data.riders.map(r => `
                            <div class="search-item" data-id="${r.id}" data-name="${r.firstname} ${r.lastname}" data-club="${r.club_name || 'Ingen klubb'}">
                                <div class="search-item-name">${r.firstname} ${r.lastname}</div>
                                <div class="search-item-club">${r.club_name || 'Ingen klubb'}</div>
                            </div>
                        `).join('');
                    } else {
                        results.innerHTML = '<div class="search-item"><em>Inga träffar</em></div>';
                    }
                    results.classList.add('show');
                });
        }, 250);
    });

    results.addEventListener('click', function(e) {
        const item = e.target.closest('.search-item');
        if (item?.dataset.id) {
            riderId.value = item.dataset.id;
            selected.innerHTML = `<span class="clear" onclick="clearSelection()">✕</span>
                <div class="name">${item.dataset.name}</div>
                <div class="club">${item.dataset.club}</div>`;
            selected.style.display = 'block';
            input.style.display = 'none';
            results.classList.remove('show');
            submitBtn.disabled = false;
        }
    });

    window.clearSelection = function() {
        riderId.value = '';
        selected.style.display = 'none';
        input.style.display = 'block';
        input.value = '';
        submitBtn.disabled = true;
    };

    document.addEventListener('click', e => {
        if (!e.target.closest('.search-container')) results.classList.remove('show');
    });
});
</script>

<?php include __DIR__ . '/components/unified-layout-footer.php'; ?>
