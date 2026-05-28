<?php
/**
 * Admin Users Management - V3 Unified Design System
 * Only accessible by super_admin
 */
require_once __DIR__ . '/../config.php';
require_admin();

// Only super_admin can access this page
if (!hasRole('super_admin')) {
    http_response_code(403);
    die('Access denied: Only super administrators can manage users.');
}

global $pdo;
$db = getDB();

// Handle search and filters
$search = $_GET['search'] ?? '';
$roleFilter = $_GET['role'] ?? '';
$activeFilter = isset($_GET['active']) ? $_GET['active'] : '';

// Build query filters - exclude riders (they are managed via rider-edit.php)
$where = ["role != 'rider'"];
$params = [];

if ($search) {
    $where[] = "(username LIKE ? OR email LIKE ? OR full_name LIKE ?)";
    $params[] = "%$search%";
    $params[] = "%$search%";
    $params[] = "%$search%";
}

if ($roleFilter && $roleFilter !== 'rider') {
    $where[] = "role = ?";
    $params[] = $roleFilter;
}

if ($activeFilter !== '') {
    $where[] = "active = ?";
    $params[] = (int)$activeFilter;
}

$whereClause = 'WHERE ' . implode(' AND ', $where);

$sql = "SELECT
    id, username, email, full_name, role, active, last_login, created_at
FROM admin_users
$whereClause
ORDER BY
    CASE role
        WHEN 'super_admin' THEN 1
        WHEN 'admin' THEN 2
        WHEN 'promotor' THEN 3
        WHEN 'rider' THEN 4
    END,
    username ASC";

$users = $db->getAll($sql, $params);

// Get role counts for stats
$roleCounts = $db->getAll("SELECT role, COUNT(*) as count FROM admin_users GROUP BY role");
$roleStats = [];
foreach ($roleCounts as $row) {
    $roleStats[$row['role']] = $row['count'];
}

// Get count of activated rider accounts (riders with password set)
$activatedRidersCount = $db->getRow("SELECT COUNT(*) as count FROM riders WHERE password IS NOT NULL AND password != ''");
$roleStats['activated_riders'] = $activatedRidersCount['count'] ?? 0;

// Get promotors - simply from admin_users table
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
    // Ignore errors
}

// Get club admins
$clubAdmins = [];
try {
    $stmt = $pdo->query("
        SELECT
            ca.id,
            ca.club_id,
            c.name as club_name,
            au.full_name,
            au.email
        FROM club_admins ca
        JOIN clubs c ON ca.club_id = c.id
        JOIN admin_users au ON ca.user_id = au.id
        ORDER BY c.name, au.full_name
    ");
    $clubAdmins = $stmt->fetchAll(PDO::FETCH_ASSOC);
} catch (Exception $e) {
    // Table might not exist or have wrong structure
}

// Page config
$page_title = 'Användarhantering';
$breadcrumbs = [
    ['label' => 'Användare']
];
$page_actions = '<a href="/admin/role-management.php" class="btn btn--primary">
    <i data-lucide="star"></i>
    Koppla promotor
</a>
<a href="/admin/club-admins.php" class="btn btn--secondary">
    <i data-lucide="building"></i>
    Koppla klubb-admin
</a>
<a href="/admin/user-edit.php" class="btn btn--secondary">
    <i data-lucide="user-plus"></i>
    Ny användare
</a>';

// Include unified layout (uses same layout as public site)
include __DIR__ . '/components/unified-layout.php';
?>

<!-- Info about riders -->
<div class="alert alert-info">
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="icon-md"><circle cx="12" cy="12" r="10"/><line x1="12" x2="12" y1="16" y2="12"/><line x1="12" x2="12.01" y1="8" y2="8"/></svg>
    <span>
        <strong>Rider-användare</strong> hanteras via
        <a href="/admin/riders" style="color: var(--color-accent);">Deltagare</a> →
        Redigera deltagare → Användarkonto-sektionen.
    </span>
</div>

<!-- Role Stats -->
<div class="admin-stats-grid">
    <a href="/admin/users.php?role=super_admin" class="admin-stat-card" style="text-decoration: none; color: inherit;">
        <div class="admin-stat-icon stat-icon-error">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="icon-lg"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>
        </div>
        <div class="stat-content">
            <div class="stat-value"><?= $roleStats['super_admin'] ?? 0 ?></div>
            <div class="stat-label">Super Admin</div>
        </div>
    </a>
    <a href="/admin/users.php?role=admin" class="admin-stat-card" style="text-decoration: none; color: inherit;">
        <div class="admin-stat-icon stat-icon-accent">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="icon-lg"><path d="M12.22 2h-.44a2 2 0 0 0-2 2v.18a2 2 0 0 1-1 1.73l-.43.25a2 2 0 0 1-2 0l-.15-.08a2 2 0 0 0-2.73.73l-.22.38a2 2 0 0 0 .73 2.73l.15.1a2 2 0 0 1 1 1.72v.51a2 2 0 0 1-1 1.74l-.15.09a2 2 0 0 0-.73 2.73l.22.38a2 2 0 0 0 2.73.73l.15-.08a2 2 0 0 1 2 0l.43.25a2 2 0 0 1 1 1.73V20a2 2 0 0 0 2 2h.44a2 2 0 0 0 2-2v-.18a2 2 0 0 1 1-1.73l.43-.25a2 2 0 0 1 2 0l.15.08a2 2 0 0 0 2.73-.73l.22-.39a2 2 0 0 0-.73-2.73l-.15-.08a2 2 0 0 1-1-1.74v-.5a2 2 0 0 1 1-1.74l.15-.09a2 2 0 0 0 .73-2.73l-.22-.38a2 2 0 0 0-2.73-.73l-.15.08a2 2 0 0 1-2 0l-.43-.25a2 2 0 0 1-1-1.73V4a2 2 0 0 0-2-2z"/><circle cx="12" cy="12" r="3"/></svg>
        </div>
        <div class="stat-content">
            <div class="stat-value"><?= $roleStats['admin'] ?? 0 ?></div>
            <div class="stat-label">Admin</div>
        </div>
    </a>
    <a href="#promotors-section" class="admin-stat-card" style="text-decoration: none; color: inherit;">
        <div class="admin-stat-icon stat-icon-info">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="icon-lg"><rect width="18" height="18" x="3" y="4" rx="2" ry="2"/><line x1="16" x2="16" y1="2" y2="6"/><line x1="8" x2="8" y1="2" y2="6"/><line x1="3" x2="21" y1="10" y2="10"/><path d="m9 16 2 2 4-4"/></svg>
        </div>
        <div class="stat-content">
            <div class="stat-value"><?= $roleStats['promotor'] ?? 0 ?></div>
            <div class="stat-label">Promotor</div>
        </div>
    </a>
    <a href="/admin/riders?activated=1" class="admin-stat-card" style="text-decoration: none; color: inherit;">
        <div class="admin-stat-icon stat-icon-warning">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="icon-lg"><path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>
        </div>
        <div class="stat-content">
            <div class="stat-value"><?= $roleStats['activated_riders'] ?? 0 ?></div>
            <div class="stat-label">Rider-konton</div>
        </div>
    </a>
</div>

<!-- Filters -->
<div class="card">
    <div class="card-body">
        <form method="GET" class="admin-form-row" style="align-items: flex-end;">
            <div class="admin-form-group flex-1">
                <label for="search" class="admin-form-label">Sök</label>
                <input
                    type="text"
                    name="search"
                    id="search"
                    class="admin-form-input"
                    placeholder="Sök efter namn, email eller användarnamn..."
                    value="<?= htmlspecialchars($search) ?>"
                >
            </div>
            <div class="admin-form-group" style="margin-bottom: 0;">
                <label for="role" class="admin-form-label">Roll</label>
                <select name="role" id="role" class="admin-form-select min-w-140">
                    <option value="">Alla roller</option>
                    <option value="super_admin" <?= $roleFilter === 'super_admin' ? 'selected' : '' ?>>Super Admin</option>
                    <option value="admin" <?= $roleFilter === 'admin' ? 'selected' : '' ?>>Admin</option>
                    <option value="promotor" <?= $roleFilter === 'promotor' ? 'selected' : '' ?>>Promotor</option>
                </select>
            </div>
            <div class="admin-form-group" style="margin-bottom: 0;">
                <label for="active" class="admin-form-label">Status</label>
                <select name="active" id="active" class="admin-form-select min-w-120">
                    <option value="">Alla status</option>
                    <option value="1" <?= $activeFilter === '1' ? 'selected' : '' ?>>Aktiva</option>
                    <option value="0" <?= $activeFilter === '0' ? 'selected' : '' ?>>Inaktiva</option>
                </select>
            </div>
            <button type="submit" class="btn-admin btn-admin-primary btn-admin-sm">
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="icon-xs"><circle cx="11" cy="11" r="8"/><line x1="21" x2="16.65" y1="21" y2="16.65"/></svg>
                Sök
            </button>
            <?php if ($search || $roleFilter || $activeFilter !== ''): ?>
                <a href="/admin/users" class="btn-admin btn-admin-secondary btn-admin-sm">
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="icon-xs"><path d="M18 6 6 18"/><path d="m6 6 12 12"/></svg>
                    Rensa
                </a>
            <?php endif; ?>
        </form>
    </div>
</div>

<!-- Users Table -->
<div class="card">
    <div class="card-header">
        <h2><?= count($users) ?> användare</h2>
    </div>
    <div class="card-body p-0">
        <?php if (empty($users)): ?>
            <div class="admin-empty-state">
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>
                <h3>Inga användare hittades</h3>
                <p>Prova att ändra dina sökfilter.</p>
            </div>
        <?php else: ?>
            <div class="admin-table-container">
                <table class="admin-table">
                    <thead>
                        <tr>
                            <th>Användare</th>
                            <th>Roll</th>
                            <th>Status</th>
                            <th>Senaste inloggning</th>
                            <th>Skapad</th>
                            <th style="width: 100px; text-align: right;">Åtgärder</th>
                        </tr>
                    </thead>
                    <tbody>
                        <?php foreach ($users as $user): ?>
                            <tr>
                                <td>
                                    <div class="flex items-center gap-sm">
                                        <div style="width: 32px; height: 32px; border-radius: 50%; background: var(--color-accent); color: white; display: flex; align-items: center; justify-content: center; font-weight: 600; font-size: 12px;">
                                            <?= strtoupper(substr($user['username'], 0, 1)) ?>
                                        </div>
                                        <div>
                                            <div class="font-medium"><?= htmlspecialchars($user['full_name'] ?: $user['username']) ?></div>
                                            <div class="text-xs text-secondary"><?= htmlspecialchars($user['email']) ?></div>
                                        </div>
                                    </div>
                                </td>
                                <td>
                                    <?php
                                    $roleColors = [
                                        'super_admin' => 'admin-badge-error',
                                        'admin' => 'admin-badge-warning',
                                        'promotor' => 'admin-badge-info',
                                        'rider' => 'admin-badge-success'
                                    ];
                                    $roleLabels = [
                                        'super_admin' => 'Super Admin',
                                        'admin' => 'Admin',
                                        'promotor' => 'Promotor',
                                        'rider' => 'Rider'
                                    ];
                                    $badgeClass = $roleColors[$user['role']] ?? 'admin-badge-secondary';
                                    $label = $roleLabels[$user['role']] ?? $user['role'];
                                    ?>
                                    <span class="admin-badge <?= $badgeClass ?>"><?= htmlspecialchars($label) ?></span>
                                </td>
                                <td>
                                    <?php if ($user['active']): ?>
                                        <span class="admin-badge admin-badge-success">Aktiv</span>
                                    <?php else: ?>
                                        <span class="admin-badge" style="background: var(--color-bg-sunken); color: var(--color-text-secondary);">Inaktiv</span>
                                    <?php endif; ?>
                                </td>
                                <td class="text-secondary">
                                    <?php if ($user['last_login']): ?>
                                        <?= date('Y-m-d H:i', strtotime($user['last_login'])) ?>
                                    <?php else: ?>
                                        <span class="text-muted">Aldrig</span>
                                    <?php endif; ?>
                                </td>
                                <td class="text-secondary">
                                    <?= date('Y-m-d', strtotime($user['created_at'])) ?>
                                </td>
                                <td class="text-right">
                                    <div class="table-actions justify-end">
                                        <a href="/admin/users/edit/<?= $user['id'] ?>" class="btn-admin btn-admin-sm btn-admin-secondary" title="Redigera">
                                            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="icon-xs"><path d="M17 3a2.85 2.83 0 1 1 4 4L7.5 20.5 2 22l1.5-5.5Z"/><path d="m15 5 4 4"/></svg>
                                        </a>
                                        <?php if ($user['role'] === 'promotor'): ?>
                                            <a href="/admin/user-events?id=<?= $user['id'] ?>" class="btn-admin btn-admin-sm btn-admin-secondary" title="Hantera events">
                                                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="icon-xs"><rect width="18" height="18" x="3" y="4" rx="2" ry="2"/><line x1="16" x2="16" y1="2" y2="6"/><line x1="8" x2="8" y1="2" y2="6"/><line x1="3" x2="21" y1="10" y2="10"/></svg>
                                            </a>
                                        <?php endif; ?>
                                    </div>
                                </td>
                            </tr>
                        <?php endforeach; ?>
                    </tbody>
                </table>
            </div>
        <?php endif; ?>
    </div>
</div>

<!-- Promotors List -->
<div class="card mb-lg" id="promotors-section">
    <div class="card-header flex justify-between items-center">
        <h2>
            <i data-lucide="star"></i>
            Promotörer (<?= count($promotors) ?>)
        </h2>
        <a href="/admin/role-management.php" class="btn btn--primary btn--sm">
            <i data-lucide="plus"></i> Lägg till
        </a>
    </div>
    <div class="card-body">
        <?php if (empty($promotors)): ?>
        <p class="text-secondary">Inga promotörer kopplade ännu.</p>
        <?php else: ?>
        <div class="table-responsive">
            <table class="table">
                <thead>
                    <tr>
                        <th>Namn</th>
                        <th>E-post</th>
                        <th></th>
                    </tr>
                </thead>
                <tbody>
                    <?php foreach ($promotors as $p): ?>
                    <tr>
                        <td>
                            <a href="/admin/user-edit.php?id=<?= $p['user_id'] ?>" class="link">
                                <?= h($p['full_name'] ?: $p['username']) ?>
                            </a>
                        </td>
                        <td class="text-secondary"><?= h($p['email']) ?></td>
                        <td class="text-right">
                            <a href="/admin/user-events.php?id=<?= $p['user_id'] ?>" class="btn btn--secondary btn--sm" title="Hantera events">
                                <i data-lucide="calendar"></i>
                            </a>
                        </td>
                    </tr>
                    <?php endforeach; ?>
                </tbody>
            </table>
        </div>
        <?php endif; ?>
    </div>
</div>

<!-- Club Admins List -->
<div class="card mb-lg" id="club-admins-section">
    <div class="card-header flex justify-between items-center">
        <h2>
            <i data-lucide="building"></i>
            Klubb-administratörer (<?= count($clubAdmins) ?>)
        </h2>
        <a href="/admin/club-admins.php" class="btn btn--primary btn--sm">
            <i data-lucide="plus"></i> Lägg till
        </a>
    </div>
    <div class="card-body">
        <?php if (empty($clubAdmins)): ?>
        <p class="text-secondary">Inga klubb-administratörer kopplade ännu.</p>
        <?php else: ?>
        <div class="table-responsive">
            <table class="table">
                <thead>
                    <tr>
                        <th>Namn</th>
                        <th>Klubb</th>
                        <th>E-post</th>
                        <th></th>
                    </tr>
                </thead>
                <tbody>
                    <?php foreach ($clubAdmins as $ca): ?>
                    <tr>
                        <td><?= h($ca['full_name'] ?: $ca['email']) ?></td>
                        <td>
                            <a href="/admin/club-edit.php?id=<?= $ca['club_id'] ?>" class="link">
                                <?= h($ca['club_name']) ?>
                            </a>
                        </td>
                        <td class="text-secondary"><?= h($ca['email'] ?? '-') ?></td>
                        <td class="text-right">
                            <a href="/admin/club-admins.php" class="btn btn--secondary btn--sm">
                                <i data-lucide="pencil"></i>
                            </a>
                        </td>
                    </tr>
                    <?php endforeach; ?>
                </tbody>
            </table>
        </div>
        <?php endif; ?>
    </div>
</div>

<!-- Role Description -->
<div class="card">
    <div class="card-header">
        <h2>Rollbeskrivningar</h2>
    </div>
    <div class="card-body">
        <div class="grid-auto-250">
            <div>
                <h3 style="font-weight: var(--weight-medium); color: var(--color-error); margin-bottom: var(--space-xs); display: flex; align-items: center; gap: var(--space-xs);">
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="icon-sm"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>
                    Super Admin
                </h3>
                <p class="text-sm text-secondary">Full tillgång till allt. Kan hantera användare, systeminställningar och alla andra funktioner.</p>
            </div>
            <div>
                <h3 style="font-weight: var(--weight-medium); color: var(--color-accent); margin-bottom: var(--space-xs); display: flex; align-items: center; gap: var(--space-xs);">
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="icon-sm"><path d="M12.22 2h-.44a2 2 0 0 0-2 2v.18a2 2 0 0 1-1 1.73l-.43.25a2 2 0 0 1-2 0l-.15-.08a2 2 0 0 0-2.73.73l-.22.38a2 2 0 0 0 .73 2.73l.15.1a2 2 0 0 1 1 1.72v.51a2 2 0 0 1-1 1.74l-.15.09a2 2 0 0 0-.73 2.73l.22.38a2 2 0 0 0 2.73.73l.15-.08a2 2 0 0 1 2 0l.43.25a2 2 0 0 1 1 1.73V20a2 2 0 0 0 2 2h.44a2 2 0 0 0 2-2v-.18a2 2 0 0 1 1-1.73l.43-.25a2 2 0 0 1 2 0l.15.08a2 2 0 0 0 2.73-.73l.22-.39a2 2 0 0 0-.73-2.73l-.15-.08a2 2 0 0 1-1-1.74v-.5a2 2 0 0 1 1-1.74l.15-.09a2 2 0 0 0 .73-2.73l-.22-.38a2 2 0 0 0-2.73-.73l-.15.08a2 2 0 0 1-2 0l-.43-.25a2 2 0 0 1-1-1.73V4a2 2 0 0 0-2-2z"/><circle cx="12" cy="12" r="3"/></svg>
                    Admin
                </h3>
                <p class="text-sm text-secondary">Kan hantera events, serier, riders, klubbar och importera data. Har inte tillgång till användarhantering.</p>
            </div>
            <div>
                <h3 style="font-weight: var(--weight-medium); color: #3b82f6; margin-bottom: var(--space-xs); display: flex; align-items: center; gap: var(--space-xs);">
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="icon-sm"><rect width="18" height="18" x="3" y="4" rx="2" ry="2"/><line x1="16" x2="16" y1="2" y2="6"/><line x1="8" x2="8" y1="2" y2="6"/><line x1="3" x2="21" y1="10" y2="10"/><path d="m9 16 2 2 4-4"/></svg>
                    Promotor
                </h3>
                <p class="text-sm text-secondary">Kan endast hantera tilldelade events - redigera eventinfo, hantera resultat och registreringar.</p>
            </div>
        </div>
    </div>
</div>

<?php include __DIR__ . '/components/unified-layout-footer.php'; ?>
