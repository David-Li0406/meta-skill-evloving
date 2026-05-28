<?php
/**
 * Promotor Management - Simple search tool
 * Search activated rider → Make them promotor
 */
ini_set('display_errors', 1);
error_reporting(E_ALL);

require_once __DIR__ . '/../config.php';
require_admin();

if (!hasRole('admin')) {
    http_response_code(403);
    die('Access denied');
}

$db = getDB();
$pdo = $GLOBALS['pdo'];
$currentAdmin = getCurrentAdmin();
$message = '';
$messageType = '';

// Handle actions
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $action = $_POST['action'] ?? '';

    if ($action === 'add') {
        $riderId = (int)($_POST['rider_id'] ?? 0);

        if ($riderId) {
            try {
                // Get rider info
                $stmt = $pdo->prepare("
                    SELECT r.id, r.firstname, r.lastname, r.email, r.password, c.name as club_name
                    FROM riders r
                    LEFT JOIN clubs c ON r.club_id = c.id
                    WHERE r.id = ? AND r.password IS NOT NULL AND r.password != ''
                ");
                $stmt->execute([$riderId]);
                $rider = $stmt->fetch(PDO::FETCH_ASSOC);

                if (!$rider) {
                    $message = 'Rider hittades inte eller har inte aktiverat konto';
                    $messageType = 'error';
                } else {
                    // Check if rider already has admin account
                    $stmt = $pdo->prepare("
                        SELECT au.id, au.role
                        FROM admin_users au
                        WHERE au.email = ?
                    ");
                    $stmt->execute([$rider['email']]);
                    $existingUser = $stmt->fetch(PDO::FETCH_ASSOC);

                    if ($existingUser) {
                        if ($existingUser['role'] === 'promotor') {
                            $message = $rider['firstname'] . ' ' . $rider['lastname'] . ' är redan promotör';
                            $messageType = 'warning';
                        } else {
                            $stmt = $pdo->prepare("UPDATE admin_users SET role = 'promotor' WHERE id = ?");
                            $stmt->execute([$existingUser['id']]);
                            $message = $rider['firstname'] . ' ' . $rider['lastname'] . ' är nu promotör';
                            $messageType = 'success';
                        }
                    } else {
                        // Create new admin user
                        $username = strtolower(preg_replace('/[^a-z0-9]/', '', $rider['firstname'] . $rider['lastname']));
                        $counter = 1;
                        $baseUsername = $username ?: 'user';

                        // Check for unique username
                        $stmt = $pdo->prepare("SELECT id FROM admin_users WHERE username = ?");
                        $stmt->execute([$username]);
                        while ($stmt->fetch()) {
                            $username = $baseUsername . $counter++;
                            $stmt->execute([$username]);
                        }

                        $stmt = $pdo->prepare("
                            INSERT INTO admin_users (username, email, full_name, role, active, created_at)
                            VALUES (?, ?, ?, 'promotor', 1, NOW())
                        ");
                        $stmt->execute([$username, $rider['email'], $rider['firstname'] . ' ' . $rider['lastname']]);

                        $message = $rider['firstname'] . ' ' . $rider['lastname'] . ' är nu promotör';
                        $messageType = 'success';
                    }
                }
            } catch (Exception $e) {
                $message = 'Fel: ' . $e->getMessage();
                $messageType = 'error';
            }
        }
    } elseif ($action === 'remove') {
        $userId = (int)($_POST['user_id'] ?? 0);
        if ($userId) {
            try {
                $stmt = $pdo->prepare("UPDATE admin_users SET role = 'rider' WHERE id = ?");
                $stmt->execute([$userId]);

                // Try to delete from promotor_events if table exists
                try {
                    $stmt = $pdo->prepare("DELETE FROM promotor_events WHERE user_id = ?");
                    $stmt->execute([$userId]);
                } catch (Exception $e) {
                    // Table might not exist, ignore
                }

                $message = 'Promotör-rollen borttagen';
                $messageType = 'success';
            } catch (Exception $e) {
                $message = 'Fel: ' . $e->getMessage();
                $messageType = 'error';
            }
        }
    }
}

// Get current promotors - just from admin_users table
$promotors = [];
try {
    $stmt = $pdo->query("
        SELECT
            au.id as user_id,
            au.full_name,
            au.email,
            au.username
        FROM admin_users au
        WHERE au.role = 'promotor' AND au.active = 1
        ORDER BY au.full_name
    ");
    $promotors = $stmt->fetchAll(PDO::FETCH_ASSOC);
} catch (Exception $e) {
    $message = 'Kunde inte hämta promotörer: ' . $e->getMessage();
    $messageType = 'error';
}

$page_title = 'Promotörer';
$breadcrumbs = [['label' => 'Användare', 'url' => '/admin/users.php'], ['label' => 'Promotörer']];
include __DIR__ . '/components/unified-layout.php';
?>

<?php if ($message): ?>
<div class="alert alert--<?= $messageType ?>" style="margin-bottom: var(--space-md);">
    <?= htmlspecialchars($message) ?>
</div>
<?php endif; ?>

<div class="card mb-lg">
    <div class="card-header">
        <h2>Lägg till promotör</h2>
    </div>
    <div class="card-body">
        <p class="text-secondary mb-md">Sök efter deltagare med aktiverat konto.</p>

        <form method="POST" id="addForm">
            <input type="hidden" name="action" value="add">
            <input type="hidden" name="rider_id" id="riderId">

            <div class="search-container">
                <input type="text" id="searchInput" class="form-input" placeholder="Sök namn..." autocomplete="off">
                <div id="searchResults" class="search-results"></div>
            </div>

            <div id="selectedRider" class="selected-box" style="display:none;"></div>

            <button type="submit" id="submitBtn" class="btn btn--primary mt-md" disabled>
                <i data-lucide="star"></i> Gör till promotör
            </button>
        </form>
    </div>
</div>

<div class="card">
    <div class="card-header">
        <h2>Nuvarande promotörer (<?= count($promotors) ?>)</h2>
    </div>
    <div class="card-body">
        <?php if (empty($promotors)): ?>
            <p class="text-secondary">Inga promotörer.</p>
        <?php else: ?>
            <div class="admin-list">
                <?php foreach ($promotors as $p): ?>
                <div class="admin-row">
                    <div class="admin-info">
                        <strong><?= h($p['full_name'] ?: $p['username']) ?></strong>
                        <span class="text-secondary"><?= h($p['email']) ?></span>
                    </div>
                    <form method="POST" onsubmit="return confirm('Ta bort promotör-rollen?')">
                        <input type="hidden" name="action" value="remove">
                        <input type="hidden" name="user_id" value="<?= $p['user_id'] ?>">
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
.badge-sm { font-size: 0.75rem; padding: 2px 6px; }
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
            fetch('/api/search-riders.php?q=' + encodeURIComponent(q) + '&activated=1&limit=20')
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
